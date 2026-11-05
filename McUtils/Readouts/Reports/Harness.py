"""
`ReportHarness`: composes a `ReportDocument` from a `SourceCatalog` with a staged workflow of small model decisions.

Each stage is one `DecisionPoint` whose answer schema is built from the catalog, so the model only ever picks from
closed lists (section names, item ids) or writes short text that is then checked (length, document rules and, under the
``grounded`` policy, that every number in it appears in the evidence the model was shown). Everything is applied to the
document through `ReportDocument` operations; the model never writes Markdown, code or markers.

Stages: ``select_content`` -> ``outline`` -> ``caption`` per block -> ``section_text`` per section -> ``summary``
(see `ReportHarness.compose` for which run under which writing policy).
"""

import numpy as np

from ...JobDrivers import DecisionPoint, DecisionRunner, Evidence, CheckResult
from .Document import ReportDocument, ReportOperationError
from .Grounding import WritingPolicy, check_grounding, evidence_numbers, extract_numbers
from .Templates import ReportTemplate, find_report_template

__all__ = ["ReportLimits", "ComposeResult", "ReportHarness", "UNCHECKED_NOTE"]

UNCHECKED_NOTE = "This report contains model-written text that was not checked against the data."

# Stage questions. Changing any of them means bumping ReportHarness.PROMPT_VERSION.
Q_SELECT = ("Choose which sections of each data source belong in a short scientific report titled {title!r}. "
            "Prefer sections with numbers a reader needs; skip raw or redundant ones.")
Q_OUTLINE = ("Group the chosen items into at most {max_sections} report sections, in reading order, and give each "
             "section a short plain heading (at most {heading_chars} characters). Use every item exactly once.")
Q_CAPTION = ("Write a one-sentence caption (at most {caption_chars} characters) for this block of a report titled "
             "{title!r}. State values exactly as shown; do not compute new numbers.")
Q_SECTION = ("Write {paragraphs} short paragraph(s) or fewer (each at most {paragraph_chars} characters) introducing "
             "the section {heading!r} of a report titled {title!r}. State values exactly as shown in the evidence; "
             "do not compute new numbers.")
Q_SUMMARY = ("Write a summary of at most {summary_words} words for a report titled {title!r}, using only the "
             "headings, captions and text shown. State values exactly as shown; do not compute new numbers.")


class ReportLimits:
    """Caps on what the model may produce and see."""

    def __init__(self, max_blocks=12, max_sections=6, heading_chars=60, caption_chars=200, paragraphs=3,
                 paragraph_chars=600, summary_words=120, evidence_tokens=None, rel_tol=1e-3, small_int_max=10):
        self.max_blocks, self.max_sections = max_blocks, max_sections
        self.heading_chars, self.caption_chars = heading_chars, caption_chars
        self.paragraphs, self.paragraph_chars, self.summary_words = paragraphs, paragraph_chars, summary_words
        self.evidence_tokens = {"select_content": 1500, "outline": 800, "caption": 600, "section_text": 1500,
                                "summary": 1500}
        self.evidence_tokens.update(evidence_tokens or {})
        self.rel_tol, self.small_int_max = rel_tol, small_int_max

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


class ComposeResult:
    """``doc``; the ledger ``records`` this run wrote; ``cost`` (calls, tokens, wall_s, cost_units); ``calls`` (model calls)."""

    def __init__(self, doc, records, cost):
        self.doc, self.records, self.cost = doc, records, cost

    @property
    def calls(self):
        return self.cost["calls"]

    def __repr__(self):
        return f"ComposeResult(blocks={len(self.doc.blocks)}, decisions={len(self.records)}, calls={self.calls})"


# ---------------------------------------------------------------------------------------------------------- #
def _fit(text, cap_tokens):
    """Hard-trim ``text`` so that ``len // 4 <= cap_tokens``."""
    limit = cap_tokens * 4
    if len(text) <= limit:
        return text
    return text[:max(limit - 1, 0)].rstrip() + "…"


def _fit_lines(lines, cap_tokens, shrinkable=None):
    """
    Join ``lines`` under the cap by shortening the lines at ``shrinkable`` indices (default: all) to a common
    maximum length, then hard-trimming as a last resort.
    """
    text = "\n".join(lines)
    if len(text) // 4 <= cap_tokens:
        return text
    idx = list(range(len(lines))) if shrinkable is None else list(shrinkable)
    for width in (160, 100, 60, 40, 24, 12):
        short = [(l if i not in idx or len(l) <= width else l[:width - 1].rstrip() + "…") for i, l in enumerate(lines)]
        text = "\n".join(short)
        if len(text) // 4 <= cap_tokens:
            return text
    return _fit(text, cap_tokens)


def _line_errors(text, what, limit=None):
    """Errors if ``ReportDocument`` would refuse ``text`` as a single line (empty, comments, ``#`` lines, length)."""
    errors = []
    try:
        ReportDocument._check_text(text, what)
    except ReportOperationError as e:
        errors.append(e.detail)
    if limit is not None and isinstance(text, str) and len(text) > limit:
        errors.append(f"{what} is {len(text)} characters; the limit is {limit}")
    return errors


class _Section:
    def __init__(self, heading, item_ids):
        self.heading, self.item_ids = heading, list(item_ids)
        self.heading_id = None
        self.block_ids = []
        self.prose_ids = []


class _State:
    """Everything the stages share during one `compose`."""

    def __init__(self, title, handles, sources, rows, template):
        self.title, self.handles, self.sources, self.rows, self.template = title, handles, sources, rows, template
        self.items = []             # [{"id","handle","section","title","kind","description"}]
        self.item_by_id = {}
        self.sections = []          # [_Section]
        self.doc = None
        self.block_item = {}        # block id -> item
        self.block_text = {}        # block id -> text shown to the model for that block
        self.block_readouts = {}    # block id -> Readout
        self.captions = {}          # block id -> accepted caption
        self.paragraphs = {}        # section index -> [accepted paragraphs]
        self.summary = None


class ReportHarness:
    """
    :param catalog: a `SourceCatalog`
    :param runner: a `DecisionRunner` whose clients map the tiers used here (``small``, optionally ``large``)
    :param policy: a `WritingPolicy` or its value: ``grounded`` (default), ``structure_only`` or ``unchecked``
    :param limits: a `ReportLimits`
    :param template: a `ReportTemplate` to use for every source; default: looked up per source
    """
    PROMPT_VERSION = "report-v1"

    def __init__(self, catalog, runner, policy="grounded", limits=None, template=None):
        self.catalog, self.runner = catalog, runner
        self.policy = WritingPolicy.coerce(policy)
        self.limits = limits or ReportLimits()
        self.template = template

    # ---- setup ------------------------------------------------------------------------------------ #
    def _resolve_template(self, handles, sources):
        if self.template is not None:
            return self.template() if isinstance(self.template, type) else self.template
        found = [find_report_template(sources[h]) for h in handles]
        first = found[0]
        if all(type(t) is type(first) for t in found):
            return first
        return ReportTemplate()

    def _fixed(self, template, handles):
        return template.is_fixed and len(handles) == 1

    def _make_items(self, state, chosen):
        """``chosen``: ``{handle: [section names]}`` -> items i1..in in handle order and section-row order."""
        n = 0
        for h in state.handles:
            order = [r["name"] for r in state.rows[h]]
            base = lambda name: name.split(".", 1)[0]       # templates may name a part: ``normal_modes.frequencies``
            for name in sorted(chosen.get(h, []), key=lambda x: (order.index(base(x)), x)):
                n += 1
                row = next(r for r in state.rows[h] if r["name"] == base(name))
                title = row.get("title") or base(name)
                if name != base(name):
                    title = f"{title}: {name.split('.', 1)[1].replace('_', ' ')}"
                item = {"id": f"i{n}", "handle": h, "section": name, "title": title,
                        "kind": row.get("kind") or "unknown", "description": row.get("description") or ""}
                state.items.append(item)
                state.item_by_id[item["id"]] = item

    def _template_choice(self, state):
        """Per handle, the template's sections that are available there, else the source's defaults."""
        chosen = {}
        names = [n for _, ns in state.template.sections for n in ns]
        for h in state.handles:
            avail = [r["name"] for r in state.rows[h] if r["available"]]
            pick = [n for n in names if n.split(".", 1)[0] in avail] if state.template.is_fixed else []
            chosen[h] = pick or state.sources[h].default_sections()
        return chosen

    # ---- stage 1: select_content ------------------------------------------------------------------ #
    def _select_point(self, state):
        lim = self.limits

        def evidence(st):
            lines, shrink = [], []
            for h in st.handles:
                src = st.sources[h]
                lines.append(f"{h} ({src.type_name.rsplit('.', 1)[-1]}): {src.title or h}")
                for r in st.rows[h]:
                    if r["available"]:
                        shrink.append(len(lines))
                        lines.append(f"- {r['name']} [{r['kind']}]: {r['description']}")
            return Evidence(_fit_lines(lines, lim.evidence_tokens["select_content"], shrink))

        def schema(st):
            props = {}
            for h in st.handles:
                names = [r["name"] for r in st.rows[h] if r["available"]]
                props[h] = {"type": "array", "items": {"enum": names}, "uniqueItems": True,
                            "maxItems": min(len(names), lim.max_blocks)}
            return {"type": "object", "properties": props, "required": list(st.handles),
                    "additionalProperties": False}

        def check(st, ans):
            total = sum(len(v) for v in ans.values())
            errors = []
            if total < 1:
                errors.append("choose at least one section in total")
            if total > lim.max_blocks:
                errors.append(f"{total} sections chosen; at most {lim.max_blocks} are allowed in total")
            return CheckResult(not errors, errors)

        def default(st):
            chosen = self._template_choice(st)
            out, budget = {}, lim.max_blocks
            for h in st.handles:
                out[h] = chosen[h][:max(budget, 0)]
                budget -= len(out[h])
            return out

        return DecisionPoint("select_content", Q_SELECT.format(title=state.title), evidence, schema, default,
                             self.PROMPT_VERSION, check, max_evidence_tokens=lim.evidence_tokens["select_content"],
                             escalate_to=self._escalation())

    # ---- stage 2: outline ------------------------------------------------------------------------- #
    def _outline_point(self, state):
        lim = self.limits
        ids = [i["id"] for i in state.items]

        def evidence(st):
            lines = [f"{i['id']}: {i['handle']}.{i['section']} — {i['title']} [{i['kind']}]" for i in st.items]
            return Evidence(_fit_lines(lines, lim.evidence_tokens["outline"]))

        def schema(st):
            return {"type": "object", "properties": {"sections": {
                "type": "array", "minItems": 1, "maxItems": lim.max_sections,
                "items": {"type": "object", "required": ["heading", "items"], "additionalProperties": False,
                          "properties": {"heading": {"type": "string", "minLength": 1, "maxLength": lim.heading_chars},
                                         "items": {"type": "array", "minItems": 1, "items": {"enum": ids}}}}}},
                    "required": ["sections"], "additionalProperties": False}

        def check(st, ans):
            errors, seen, headings = [], {}, set()
            for n, sec in enumerate(ans["sections"]):
                for i in sec["items"]:
                    seen[i] = seen.get(i, 0) + 1
                errors += _line_errors(sec["heading"], f"heading of section {n + 1}", lim.heading_chars)
                key = sec["heading"].strip().lower()
                if key in headings:
                    errors.append(f"heading {sec['heading']!r} is used twice")
                headings.add(key)
            for i in ids:
                if seen.get(i, 0) == 0:
                    errors.append(f"item {i} is not used; every item must appear exactly once")
                elif seen[i] > 1:
                    errors.append(f"item {i} is used {seen[i]} times; every item must appear exactly once")
            return CheckResult(not errors, errors)

        def default(st):
            if st.template.is_fixed and len(st.handles) == 1:
                return self._template_outline(st)
            out = []
            for h in st.handles:
                its = [i["id"] for i in st.items if i["handle"] == h]
                if its:
                    out.append({"heading": (st.sources[h].title or h)[:lim.heading_chars], "items": its})
            return {"sections": out[:lim.max_sections]}

        return DecisionPoint("outline", Q_OUTLINE.format(max_sections=lim.max_sections,
                                                        heading_chars=lim.heading_chars),
                             evidence, schema, default, self.PROMPT_VERSION, check,
                             max_evidence_tokens=lim.evidence_tokens["outline"], escalate_to=self._escalation())

    def _template_outline(self, state):
        out = []
        for heading, names in state.template.sections:
            its = [i["id"] for i in state.items if i["section"] in names]
            if its:
                out.append({"heading": heading[:self.limits.heading_chars], "items": its})
        used = {i for s in out for i in s["items"]}
        rest = [i["id"] for i in state.items if i["id"] not in used]
        if rest:
            out.append({"heading": (state.sources[state.handles[0]].title or state.handles[0]), "items": rest})
        return {"sections": out}

    def _escalation(self):
        return ("large",) if "large" in self.runner.clients else ()

    # ---- stages 3-5: writing ---------------------------------------------------------------------- #
    def _grounding_errors(self, text, texts, readouts):
        if self.policy is not WritingPolicy.GROUNDED:
            return []
        ev = evidence_numbers(texts, readouts)
        res = check_grounding(text, ev, rel_tol=self.limits.rel_tol, small_int_max=self.limits.small_int_max)
        return res.errors()

    def _caption_point(self, state, bid):
        lim, item = self.limits, state.block_item[bid]
        cap = lim.evidence_tokens["caption"]

        def evidence(st):
            head = [f"Block: {item['handle']}.{item['section']} ({item['kind']})"]
            if item["kind"] == "figure":
                head.append("This block is a figure without numeric text; describe what it shows, do not state "
                            "numbers.")
            room = cap * 4 - len("\n".join(head)) - 8
            body = self.catalog.peek(item["handle"], item["section"], max_chars=max(room, 80))
            text = "\n".join(head + [body])
            text = _fit(text, cap)
            st.block_text[bid] = text
            return Evidence(text)

        def check(st, ans):
            errors = _line_errors(ans["caption"], "caption", lim.caption_chars)
            if not errors:
                errors += self._grounding_errors(ans["caption"], [st.block_text[bid]], [st.block_readouts[bid]])
            return CheckResult(not errors, errors)

        schema = {"type": "object", "properties": {"caption": {"type": "string", "minLength": 1,
                                                             "maxLength": lim.caption_chars}},
                  "required": ["caption"], "additionalProperties": False}
        return DecisionPoint("caption", Q_CAPTION.format(caption_chars=lim.caption_chars, title=state.title),
                             evidence, schema, None, self.PROMPT_VERSION, check, max_evidence_tokens=cap,
                             escalate_to=self._escalation())

    def _section_point(self, state, n):
        lim, sec = self.limits, state.sections[n]
        cap = lim.evidence_tokens["section_text"]

        def evidence(st):
            blocks = sec.block_ids
            lines = [f"Section: {sec.heading}"]
            fixed = len("\n".join(lines)) + 60 * len(blocks) + sum(len(st.captions.get(b, "")) for b in blocks)
            share = max((cap * 4 - fixed - 16) // max(len(blocks), 1), 120)
            for b in blocks:
                item = st.block_item[b]
                cap_line = f" — caption: {st.captions[b]}" if b in st.captions else ""
                lines.append(f"[{b}] {item['handle']}.{item['section']} ({item['kind']}){cap_line}")
                lines.append(self.catalog.peek(item["handle"], item["section"], max_chars=share))
            return Evidence(_fit("\n".join(lines), cap))

        def check(st, ans):
            errors = []
            for k, p in enumerate(ans["paragraphs"]):
                errors += [f"paragraph {k + 1}: {e}" for e in _line_errors(p, "paragraph", lim.paragraph_chars)]
            if not errors:
                texts = [st.block_text.get(b, "") for b in sec.block_ids] + list(st.captions.get(b, "")
                                                                                  for b in sec.block_ids)
                errors += self._grounding_errors("\n".join(ans["paragraphs"]), texts,
                                                 [st.block_readouts[b] for b in sec.block_ids])
            return CheckResult(not errors, errors)

        schema = {"type": "object", "properties": {"paragraphs": {
            "type": "array", "minItems": 1, "maxItems": lim.paragraphs,
            "items": {"type": "string", "minLength": 1, "maxLength": lim.paragraph_chars}}},
            "required": ["paragraphs"], "additionalProperties": False}
        return DecisionPoint("section_text", Q_SECTION.format(paragraphs=lim.paragraphs,
                                                             paragraph_chars=lim.paragraph_chars,
                                                             heading=sec.heading, title=state.title),
                             evidence, schema, None, self.PROMPT_VERSION, check, max_evidence_tokens=cap,
                             escalate_to=self._escalation())

    def _summary_point(self, state):
        lim = self.limits
        cap = lim.evidence_tokens["summary"]

        def evidence(st):
            lines = [f"Title: {st.title}"]
            for n, sec in enumerate(st.sections):
                lines.append(f"Section: {sec.heading}")
                for b in sec.block_ids:
                    if b in st.captions:
                        lines.append(f"- caption: {st.captions[b]}")
                for p in st.paragraphs.get(n, []):
                    lines.append(f"- text: {p}")
            return Evidence(_fit_lines(lines, cap))

        def check(st, ans):
            text = ans["summary"]
            errors = _line_errors(text, "summary")
            words = len(text.split())
            if words > lim.summary_words:
                errors.append(f"the summary is {words} words; the limit is {lim.summary_words}")
            if not errors:
                texts = list(st.block_text.values()) + list(st.captions.values())
                texts += [p for ps in st.paragraphs.values() for p in ps]
                errors += self._grounding_errors(text, texts, list(st.block_readouts.values()))
            return CheckResult(not errors, errors)

        schema = {"type": "object", "properties": {"summary": {"type": "string", "minLength": 1,
                                                              "maxLength": 8 * lim.summary_words}},
                  "required": ["summary"], "additionalProperties": False}
        return DecisionPoint("summary", Q_SUMMARY.format(summary_words=lim.summary_words, title=state.title),
                             evidence, schema, None, self.PROMPT_VERSION, check, max_evidence_tokens=cap,
                             escalate_to=self._escalation())

    # ---- compose ---------------------------------------------------------------------------------- #
    def compose(self, title, handles=None):
        """
        Compose a report.

        Under ``grounded`` the model runs ``select_content``, ``outline``, one ``caption`` per block, one
        ``section_text`` per section and ``summary`` (``2 + n_blocks + n_sections + 1`` calls when nothing fails).
        ``structure_only`` runs only the first two; a template with fixed sections and a single source skips them
        too, so the document is built with no model calls. ``unchecked`` runs the same stages as ``grounded`` without
        the grounding check, marks the text ``unchecked`` and puts a note at the top.
        """
        handles = list(self.catalog.handles() if handles is None else handles)
        if not handles:
            raise ReportOperationError("bad_argument", "there are no sources to compose a report from")
        sources = {h: self.catalog.get(h) for h in handles}
        rows = {h: self.catalog.describe(h)["sections"] for h in handles}
        template = self._resolve_template(handles, sources)
        state = _State(title, handles, sources, rows, template)
        runner, policy = self.runner, self.policy
        start = len(runner.ledger.records)

        # stages 1-2 (or the template's fixed outline)
        if self._fixed(template, handles):
            self._make_items(state, self._template_choice(state))
            outline = self._template_outline(state)
        else:
            chosen = runner.decide(self._select_point(state), state, policy=policy.value).answer
            self._make_items(state, chosen)
            outline = runner.decide(self._outline_point(state), state, policy=policy.value).answer
        if not state.items:
            raise ReportOperationError("bad_argument", "no sections were chosen: the sources have no available "
                                       "sections to show")

        # the document: headings and readout blocks
        doc = ReportDocument(title, self.catalog, meta={
            "writing_policy": policy.value, "template": template.name, "prompt_version": self.PROMPT_VERSION,
            "ledger": getattr(runner.ledger, "path", None)})
        state.doc = doc
        for sec in outline["sections"]:
            s = _Section(sec["heading"], sec["items"])
            state.sections.append(s)
            s.heading_id = doc.add_heading(s.heading).block_id
            for iid in s.item_ids:
                item = state.item_by_id[iid]
                bid = doc.add_readout(item["handle"], include=[item["section"]]).block_id
                s.block_ids.append(bid)
                state.block_item[bid] = item
                state.block_readouts[bid] = self.catalog.get(item["handle"]).readout(include=[item["section"]])

        status = "grounded" if policy is WritingPolicy.GROUNDED else "unchecked"
        writes = policy is not WritingPolicy.STRUCTURE_ONLY

        # captions
        for s in state.sections:
            for bid in s.block_ids:
                item = state.block_item[bid]
                if writes and template.captions:
                    out = runner.decide(self._caption_point(state, bid), state, stage=f"caption:{bid}",
                                        policy=policy.value)
                    if not out.defaulted:
                        state.captions[bid] = out.answer["caption"]
                        doc.set_caption(bid, out.answer["caption"], status=status)
                elif not writes:
                    fixed = template.caption_for(item["handle"], item["section"], state.sources[item["handle"]])
                    if fixed:
                        state.captions[bid] = fixed
                        doc.set_caption(bid, fixed, status="template")
                if bid not in state.block_text:     # figure/peek text shown (or what it would have been)
                    state.block_text[bid] = self.catalog.peek(item["handle"], item["section"],
                                                              max_chars=self.limits.evidence_tokens["caption"] * 4)

        # section text, then the summary
        if writes and template.section_text:
            for n, s in enumerate(state.sections):
                out = runner.decide(self._section_point(state, n), state, stage=f"section_text:{s.heading_id}",
                                    policy=policy.value)
                if out.defaulted:
                    continue
                after = s.heading_id
                state.paragraphs[n] = []
                for p in out.answer["paragraphs"]:
                    after = doc.add_text(p, cites=s.block_ids, after=after, status=status).block_id
                    s.prose_ids.append(after)
                    state.paragraphs[n].append(p)
        if writes and template.summary:
            out = runner.decide(self._summary_point(state), state, policy=policy.value)
            if not out.defaulted:
                state.summary = out.answer["summary"]
                doc.add_text(state.summary, after="start", status=status, role="summary")
        if policy is WritingPolicy.UNCHECKED and (state.captions or state.paragraphs or state.summary):
            doc.add_callout(UNCHECKED_NOTE, kind="note", after="start")

        records = runner.ledger.records[start:]
        cost = {"calls": 0, "tokens_in": 0, "tokens_out": 0, "wall_s": 0.0, "cost_units": 0.0}
        for r in records:
            for k in cost:
                cost[k] += r.cost.get(k, 0) if r.cost else 0
        return ComposeResult(doc, list(records), cost)
