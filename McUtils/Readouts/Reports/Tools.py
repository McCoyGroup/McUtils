"""
Tool mode: the operations of a `ReportDocument` as a `McUtils.JobDrivers.ToolSet`, for a model that drives the report
itself. This module is a thin layer over the document's own Python API (`ReportDocument.apply_template`, `lock`,
`snapshot`, `diff`, `transaction`, `check_text`, ...), which is what a person uses directly; the tools add the JSON
schemas, the writing policy, receipts and revision numbers, and never do anything the document can't do itself (through an MCP server, `McUtils.JobDrivers.MCP`, or any other caller). The model never writes Markdown, code
or markers: it reads the sources (`describe_source`, `peek`), applies the source's template or builds blocks one at a
time, and writes captions and prose, which are checked against the data they cite.

Mutating tools answer with a short receipt (the block id, the block count and the document's revision number). The
model reads the whole document with ``compile`` (read-only: it checks the report and counts its text by status) and
sees what changed with ``diff``, relative to a named baseline: ``last_change`` (the most recent mutating request),
``start`` (when the report was opened), ``template`` (right after ``apply_template``), ``checkpoint`` / a label the
model recorded with ``checkpoint``. Every ``diff`` result says which baseline it used. Error results carry a ``hint``
(`REPORT_HINTS`) saying what to do next.

A template can lock parts of the report (``ReportTemplate.locked`` / ``locked_headings``): the blocks `apply_template`
builds for them can't be edited, captioned, moved or removed by the tools (``code="locked"``); the model can still add
text and other blocks around them. The locked block ids are kept in ``doc.meta["locked"]`` (saved with the report), and
the owner can change them with `ReportDocument.lock` / `unlock`.

Under the ``grounded`` policy text must cite readout blocks (``code="needs_citation"``), and a number in it that does
not appear in the cited blocks' data is rejected with ``code="ungrounded"`` and the unmatched numbers, and nothing is
written. Accepted text is marked ``checked`` (a number was verified) or ``no_numbers`` (nothing to verify); the
receipt of an accepted text lists ``numbers``: which cited value (block, label, row, unit) each number matched, and
the placeholder (``use``) that would have written it. The match is unit-aware (see `check_grounding`). ``unchecked``
accepts the text and marks it as unchecked. ``structure_only`` turns the text tools off (``code="writing_disabled"``).

Values should be written as placeholders (``{r3.frequency[2]}``): the server writes the number and its unit label from
the data, so nothing is mistyped or given in the wrong unit (`McUtils.Readouts.Reports.Fill`). Typing the number is
allowed, and then the unit-aware check is the safety net; an ``ungrounded`` refusal shows the placeholder that matches.
Computed values (``{mean(...)}``) are off unless ``allow_derived``; ``apply_edits`` (several edits in one atomic call)
exists only with ``apply_edits=True``.
"""

import re

from ...Data import UnitsData
from ...JobDrivers.Tools import ToolSet
from ...JobDrivers.Answers import validate_answer
from .Document import ReportOperationError, Prose, Heading
from .Grounding import WritingPolicy
from .Templates import find_report_template, template_menu
from .Instructions import context_level as _level_of, report_instructions

__all__ = ["report_toolset", "REPORT_HINTS", "REPORT_RETRY", "LEVEL_TOOLS"]

# What a model should do next after each kind of error (`ToolSet(hints=...)` adds it to the error as ``hint``).
REPORT_HINTS = {
    "locked": "This block is locked by the report's owner. Tell the user it can't be changed and stop: do not "
              "recreate it, rewrite it somewhere else or add text next to it to stand in for the edit, unless the "
              "user separately asks for supplementary text.",
    "ungrounded": "Do not type the number: write the placeholder the error shows (such as {r3.frequency[2]}) and the "
                  "server writes the value with its unit, or leave the number out, and try once more. If it is "
                  "refused again, tell the user.",
    "bad_reference": "A placeholder is {BLOCK.COLUMN[ROW]} with a readout block id, a column from the error's "
                     "`choices` and a 1-based row, such as {r3.frequency[2]}. Correct it and try once more.",
    "unit_mismatch": "Write the placeholder alone, such as {r3.frequency[2]}, with no unit after it: the server adds "
                     "the data's unit. Correct it and try once more.",
    "derived_disabled": "This report only takes values as the data shows them: use single placeholders like "
                        "{r3.frequency[2]}, and leave the computation to the reader.",
    "needs_citation": "Pass `cites`: the ids of the readout blocks the text is about (from outline or compile), then "
                      "try again.",
    "unknown_block": "Block ids (h1, r2, p1, ...) come from outline or compile; a source handle or a section name is "
                     "not a block id.",
    "unknown_source": "Call list_sources for the handles. If the source the user asked about is not listed, tell "
                      "the user which sources are available and stop; do not substitute another source.",
    "unknown_section": "Call describe_source for the section names (dotted parts like normal_modes.frequencies are "
                       "listed there).",
    "unavailable_section": "That section has no data for this source; choose another section or tell the user.",
    "bad_position": "`after` is 'start' or one block id from outline (a block, not a section name); `under` is a "
                    "heading id.",
    "bad_argument": "Correct the argument as the detail says and try once more.",
    "invalid_arguments": "Correct the arguments to match the tool's schema and try once more.",
    "invalid_document": "The report itself has a problem (see the detail); tell the user rather than working around it.",
    "no_template": "This source has no fixed outline: build the report with add_heading and add_readout instead.",
    "writing_disabled": "This report doesn't accept written text; use only add_heading, add_readout and the other "
                        "structure tools.",
    "missing_dependency": "A Python package is missing on the server. Tell the user (the detail says which) and "
                          "continue with the other formats.",
    "unknown_tool": "Use only the tools the server lists.",
    "internal": "This is a server fault, not a mistake in your call. Do not retry in a loop; tell the user.",
}

# ``retry`` on error results: "no" = tell the user rather than repeating the request; "once" = one corrected attempt;
# "after_fix" = correct the arguments as the detail says and call again.
REPORT_RETRY = {code: "no" for code in ("locked", "unknown_source", "writing_disabled",
                                         "missing_dependency", "internal", "invalid_document", "no_template",
                                         "derived_disabled", "unavailable_section")}
REPORT_RETRY.update({code: "once" for code in ("ungrounded",)})
REPORT_RETRY.update({code: "after_fix" for code in ("needs_citation", "unknown_block", "unknown_section", "bad_position",
                                                    "bad_argument", "invalid_arguments", "bad_reference",
                                                    "unit_mismatch", "unknown_tool")})

# which tools each context level offers (see `McUtils.Readouts.Reports.Instructions`); ``render`` is added whenever
# there is a renderer. At level 1 ``list_sources`` / ``describe_source`` are added back when the catalog is too large
# to list in the instructions.
_ALL = ("list_sources", "describe_source", "peek", "outline", "compile", "checkpoint", "diff", "apply_template",
        "add_heading", "add_readout", "add_text", "set_caption", "edit_text", "move", "move_section", "remove",
        "move_source", "apply_edits", "render")
# ``apply_edits`` is never part of a level: the owner turns it on with ``apply_edits=True`` (``--apply-edits``).
LEVEL_TOOLS = {
    1: ("peek", "compile", "diff", "apply_template", "add_heading", "add_readout", "add_text", "set_caption",
        "edit_text", "move_section", "remove", "move_source", "render"),
    2: tuple(t for t in _ALL if t != "apply_edits"),
    3: tuple(t for t in _ALL if t != "apply_edits"),
}

# one-sentence descriptions for level 1 (the instructions carry the rest)
_SHORT = {
    "list_sources": "The sources: handle, title and template.",
    "describe_source": "A source's sections and its template.",
    "peek": "The data of one section of a source (handle + section name), as the report shows it.",
    "compile": "Reads the whole report back (blocks, text statuses, problems, warnings). Changes nothing.",
    "diff": "What changed since a baseline: 'last_change', 'start' or 'template'.",
    "apply_template": "Builds the source's standard report (headings and tables) in one call.",
    "add_heading": "Adds a section heading.",
    "add_readout": "Adds a table/figure of one source's sections (include: section names).",
    "add_text": "Adds a paragraph. cites: readout ids. Write every number as a placeholder like {r3.frequency[2]} "
                "(the server fills in number and unit); do not type numbers.",
    "set_caption": "Sets a readout block's caption; write numbers as placeholders like {r3.frequency[2]}.",
    "edit_text": "Replaces the text of a paragraph or heading.",
    "move_section": "Moves a heading and everything under it to after a block (or 'start').",
    "move_source": "Moves all sections of one source together to after a block (or 'start').",
    "remove": "Removes a block.",
    "render": "Writes the report as md/html/pptx files and returns their paths.",
}

MAX_PEEK = 4000
_ID = {"type": "string", "minLength": 1, "maxLength": 40}
_HANDLE = {"type": "string", "minLength": 1, "maxLength": 40, "description": "A source handle from `list_sources`, such as hoh; not a report block id."}
_UNDER = {"type": "string", "minLength": 1, "maxLength": 40,
          "description": "A heading id: add at the end of that heading's section (instead of `after`)."}
RESERVED = frozenset({"last_change", "start", "template", "checkpoint"})
_AFTER = {"type": "string", "minLength": 1, "maxLength": 40,
          "description": "Insert after this single block id, or 'start'. Omit to append at the end. To place prose "
                         "below a table, pass the table's id, not its heading's id (or use `under`)."}
_NAMES = {"type": "array", "items": {"type": "string", "minLength": 1, "maxLength": 80}, "maxItems": 40}


def report_toolset(doc, catalog, renderer=None, policy="grounded", rel_tol=1e-3, small_int_max=10, year_range=(1900, 2100), out_dir=None,
                   on_change=None, hints=None, allow_derived=False, apply_edits=False, context_level=2,
                   include_tools=None, exclude_tools=None, inline_max=8, unit_style=None):
    """
    The tools for editing ``doc`` (a `ReportDocument` built against ``catalog``).

    :param renderer: a `ReportRenderer`; the ``render`` tool is only defined when one is given
    :param policy: a `WritingPolicy` (or its value): ``grounded`` (default), ``unchecked`` or ``structure_only``
    :param out_dir: where ``render`` writes (required with ``renderer``)
    :param rel_tol: relative tolerance of the number check under ``grounded`` (a number also matches within half a unit
        of its last written digit); ``small_int_max``: integers up to this are not checked; ``year_range``: four-digit
        integers in this range are taken to be years and not checked (``None`` checks them)
    :param hints: ``{error code: sentence}`` attached to error results as ``hint`` (see `ToolSet`); the default is
        `REPORT_HINTS`, ``{}`` turns them off
    :param on_change: ``callable(doc)`` called after every successful mutating tool (the MCP server saves the file here)
    :param allow_derived: whether text may contain computed values the server fills in
        (``{mean(r3.frequency[2], r3.frequency[3])}``); off by default. Single placeholders
        (``{r3.frequency[2]}``) are always allowed
    :param apply_edits: whether to offer the ``apply_edits`` tool (several edits in one atomic call); off by default
        (the owner decides), at every context level
    :param context_level: ``1``/``"compact"``, ``2``/``"standard"`` (default) or ``3``/``"full"``: how much the
        model is shown and which conveniences it gets (see `McUtils.Readouts.Reports.Instructions` and
        `LEVEL_TOOLS`); the checks are the same at every level. The returned tool set's ``instructions`` attribute is
        the matching server instructions.
    :param include_tools: tool names to offer on top of the level's
    :param exclude_tools: tool names to leave out
    :param inline_max: list the catalog in the instructions when it has at most this many sources
    :param unit_style: how filled values write their unit: ``"unicode"`` (``3803.3 cm⁻¹``), ``"ascii"``
        (``3803.3 cm-1``) or ``"latex"`` (``$3803.3\\,\\mathrm{cm^{-1}}$``); stored in the report, default
        `UnitsData.label_style`
    :return: a `ToolSet`; results are plain JSON values
    """
    policy = WritingPolicy.coerce(policy)
    if unit_style is not None:
        doc.unit_style = unit_style
    from .Fill import example_value
    example = example_value(doc.unit_style)
    if not (isinstance(rel_tol, (int, float)) and 0 < rel_tol < 1):
        raise ValueError(f"rel_tol must be a number between 0 and 1, got {rel_tol!r}")
    if not (isinstance(small_int_max, int) and small_int_max >= 0):
        raise ValueError(f"small_int_max must be a non-negative integer, got {small_int_max!r}")
    if year_range is not None and not (len(year_range) == 2 and year_range[0] <= year_range[1]):
        raise ValueError(f"year_range must be (low, high) or None, got {year_range!r}")
    if renderer is not None and out_dir is None:
        raise ValueError("a renderer needs out_dir")
    if hints is None:
        hints = dict(REPORT_HINTS)
        if allow_derived:
            hints["ungrounded"] = ("Do not type the number: write the placeholder the error shows (such as "
                                   "{r3.frequency[2]}) and the server writes the value with its unit; a computed "
                                   "value is an expression of placeholders, like {mean(r3.frequency[2], "
                                   "r3.frequency[3])}. Or leave the number out, and try once more. If it is refused "
                                   "again, tell the user.")
            hints["derived_disabled"] = "Use only +, -, *, / and mean, sum, min, max, abs, diff, ratio of placeholders."
    tools = ToolSet(hints=hints, error_fields={k: {"retry": v} for k, v in REPORT_RETRY.items()})
    level = _level_of(context_level)
    inlined = len(catalog) <= inline_max
    named = set(include_tools or ()) | set(exclude_tools or ())
    if "apply_edits" in named:
        raise ValueError("apply_edits is switched on with apply_edits=True (--apply-edits), not with include_tools / "
                         "exclude_tools")
    enabled = set(LEVEL_TOOLS[level]) | set(include_tools or ())
    if apply_edits:
        enabled.add("apply_edits")
    if level == 1 and not inlined:
        enabled |= {"list_sources", "describe_source"}
    enabled -= set(exclude_tools or ())
    unknown = named - set(_ALL)
    if unknown:
        raise ValueError(f"unknown tool names {sorted(unknown)}; the tools are {list(_ALL)}")
    raw = {}           # name -> the unwrapped function (for apply_edits)

    def _strip(schema):
        if level != 1:
            return schema
        props = {k: {kk: vv for kk, vv in v.items() if kk != "description"} for k, v in schema.get("properties", {}).items()}
        return dict(schema, properties=props)

    schemas = {}

    def add(name, func, schema, description):
        schemas[name] = schema
        if name in enabled:
            tools.add(name, func, _strip(schema), _SHORT.get(name, description) if level == 1 else description)

    def order_line():
        """``h1 Structure: r1 r2 | h2 Vibrations: r3 p1`` (level 1 receipts)."""
        parts, cur = [], []
        for b in doc.blocks:
            if isinstance(b, Heading) and b.level == 2:
                if cur:
                    parts.append(" ".join(cur))
                cur = [f"{b.id} {b.text[:24]}:"]
            else:
                cur.append(b.id)
        if cur:
            parts.append(" ".join(cur))
        return " | ".join(parts)

    start = doc.snapshot()
    track = {"revision": 0, "before": start, "before_revision": 0,
             "baselines": {"start": (start, 0)}}     # name -> (snapshot, revision) for diff(since=...)

    def mutating(func):
        """Atomic (a failure restores the document); success returns the receipt without the outline."""
        def run(**kw):
            before = doc.snapshot()
            with doc.transaction():
                out = func(**kw)
            if doc.diff(before):
                track["before"], track["before_revision"] = before, track["revision"]
                track["revision"] += 1
                if on_change is not None:
                    on_change(doc)
            out = {k: v for k, v in out.items() if k != "outline"}
            out.update(n_blocks=len(doc.blocks), revision=track["revision"])
            warn = doc.grouping_warnings()
            if warn:
                out["warnings"] = warn
            if level == 1:
                out["order"] = order_line()
                if warn:
                    out["next"] = warn[0]["detail"]
            return out
        return run

    # ---- reading ----------------------------------------------------------------------------------- #
    def list_sources():
        out = []
        for h in catalog.handles():
            src = catalog.get(h)
            out.append({"handle": h, "type": src.type_name.rsplit(".", 1)[-1], "title": src.title,
                        "n_sections": len(src.section_names()), "template": find_report_template(src).name})
        return out

    def describe_source(handle):
        d = catalog.describe(handle)
        d["template"] = template_menu(catalog.get(handle))
        return d

    def peek(handle, section, max_chars=None):
        if max_chars is None:
            max_chars = 1500 if level == 1 else 2400
        text = catalog.peek(handle, section, max_chars=min(int(max_chars), MAX_PEEK))
        if level == 1:
            lines = text.split("\n")
            if len(lines) > 2 and lines[1] and set(lines[1]) == {"="}:      # the readout's title block
                lines = lines[3:]
                while lines and not lines[0].strip():
                    lines.pop(0)
                text = "\n".join(lines)
        return text

    def flagged(rows):
        lock = set(doc.locked)
        return [dict(r, locked=True) if r["id"] in lock else r for r in rows]

    def outline():
        return flagged(doc.outline())

    add("list_sources", list_sources, {"type": "object", "properties": {}, "additionalProperties": False},
              "The sources a report can show: handle, type, title, number of sections and the name of the report "
              "template that applies. Start here.")
    add("describe_source", describe_source,
              {"type": "object", "properties": {"handle": _HANDLE}, "required": ["handle"], "additionalProperties": False},
              "A source's sections (name, title, description, kind, whether available and why not, whether shown by "
              "default) and its report template: the fixed outline (`template.outline`: headings with the sections "
              "under each) and the optional sections it suggests adding (`template.optional`). Section names can name "
              "a part with a dot, like `normal_modes.frequencies`. Use `apply_template` to build the outline.")
    add("peek", peek,
              {"type": "object", "properties": {"handle": _HANDLE, "section": {"type": "string", "minLength": 1,
                                                                                "maxLength": 80},
                                                "max_chars": {"type": "integer", "minimum": 80, "maximum": MAX_PEEK}},
               "required": ["handle", "section"], "additionalProperties": False},
              "The text of one section of a source (numbers as they will appear), to read before writing about it. "
              f"Cut at {MAX_PEEK} characters.")
    add("outline", outline, {"type": "object", "properties": {}, "additionalProperties": False},
              "The report so far: one row per block (id, kind, text or handle/sections, caption; `locked` if the block "
              "can't be changed). Mutating tools only return a receipt; use this, `compile` or `diff` to see the result.")

    def compile(full_text=False):
        """The whole document, checked, as the model should read it. Read-only: it changes no baseline."""
        if full_text:
            blocks = flagged([{"id": b.id, "kind": b.kind, **{k: v for k, v in vars(b).items()
                                                               if k != "id" and v not in (None, [], False)}}
                              for b in doc.blocks])
        else:
            blocks = flagged(doc.outline())
        return {"revision": track["revision"], "title": doc.title, "n_blocks": len(doc.blocks), "blocks": blocks,
                "locked": doc.locked, "text_status": doc.text_status(), "problems": [e.to_dict() for e in doc.validate()],
                "warnings": doc.grouping_warnings(),
                "baselines": list(track["baselines"]),
                "grounding": {"policy": policy.value, "rel_tol": rel_tol, "small_int_max": small_int_max,
                              "year_range": None if year_range is None else list(year_range),
                              "derived": allow_derived, "apply_edits": apply_edits,
                              "unit_style": doc.unit_style or UnitsData.label_style},
                **({"next": _compile_next()} if level == 1 else {})}

    def _compile_next():
        if doc.validate():
            return "Fix or report the problems listed."
        if doc.grouping_warnings():
            return doc.grouping_warnings()[0]["detail"]
        return "The report is saved. If the user's request is done, answer the user now."

    def checkpoint(label=None):
        """Records the report as it is now as a baseline for ``diff``: ``checkpoint`` (always) and ``label``."""
        names = ["checkpoint"] + ([label] if label else [])
        if label is not None and not re.match(r"^[a-z][a-z0-9_]{0,29}$", label):
            raise ReportOperationError("bad_argument", "a label is lower-case letters, digits and underscores, "
                                       "starting with a letter (at most 30 characters)")
        if label in RESERVED:
            raise ReportOperationError("bad_argument", f"{label!r} is a built-in baseline name; choose another label",
                                       reserved=sorted(RESERVED))
        snap = doc.snapshot()
        for name in names:
            track["baselines"][name] = (snap, track["revision"])
        return {"ok": True, "baselines": list(track["baselines"]), "recorded": names, "revision": track["revision"],
                "n_blocks": len(doc.blocks)}

    def diff(since="last_change"):
        if since == "last_change":
            old, rev = track["before"], track["before_revision"]
        elif since in track["baselines"]:
            old, rev = track["baselines"][since]
        else:
            raise ReportOperationError(
                "bad_argument", f"no baseline {since!r}; use 'last_change' or one of {list(track['baselines'])}",
                choices=["last_change"] + list(track["baselines"]))
        changes = doc.diff(old)
        return {"since": since, "from_revision": rev, "revision": track["revision"], "n_changes": len(changes),
                "changes": changes}

    add("compile", compile, {"type": "object", "properties": {"full_text": {"type": "boolean"}},
                                   "additionalProperties": False},
              "Reads the whole report back (it changes nothing): every block in order (text clipped to 80 characters "
              "unless `full_text`), how many captions and paragraphs are checked / no_numbers / unchecked / manual / "
              "from the template, any problems found (unknown sources, changed sources), which blocks are locked, "
              "the baselines `diff` can compare with, and the number-check settings in force.")
    add("checkpoint", checkpoint,
              {"type": "object", "properties": {"label": {"type": "string", "minLength": 1, "maxLength": 30}},
               "additionalProperties": False},
              "Records the report as it is now as a baseline for `diff` (named 'checkpoint', plus `label` if given). "
              "Baselines 'start' (the report when it was opened) and 'template' (right after `apply_template`) "
              "exist already.")
    add("diff", diff, {"type": "object", "properties": {"since": {"type": "string", "minLength": 1,
                                                                       "maxLength": 30}},
                             "additionalProperties": False},
              "What changed since a baseline: 'last_change' (default: the most recent mutating request), 'start', "
              "'template', 'checkpoint' or a label you gave `checkpoint`. Each change is added (with the block it "
              "follows), removed, changed (field: from, to) or moved. The result says which baseline was used.")

    # ---- building ---------------------------------------------------------------------------------- #
    def apply_template(handle, after=None, optional=None):
        return {"ok": True, **doc.apply_template(handle, after=after, optional=optional or ())}

    def apply_template_tool(**kw):
        out = mutating(apply_template)(**kw)
        track["baselines"]["template"] = (doc.snapshot(), track["revision"])
        return out

    def add_heading(text, level=2, after=None, under=None):
        return doc.add_heading(text, level=level, after=after, under=under).to_dict()

    def add_readout(handle, include=None, exclude=None, caption=None, after=None, under=None):
        if caption is None:
            return doc.add_readout(handle, include=include, exclude=exclude, after=after, under=under).to_dict()
        _text_allowed()
        return _add_readout_with_caption(handle, include, exclude, caption, after, under)

    def _text_allowed():
        if policy is WritingPolicy.STRUCTURE_ONLY:
            raise ReportOperationError("writing_disabled", "this report is structure-only: text and captions are "
                                       "not written by the model", policy=policy.value)

    def _check(text, block_ids, fills=()):
        """
        Raise ``ungrounded`` if the numbers of ``text`` aren't in the data of the readout blocks ``block_ids``;
        otherwise the status to record: ``checked`` (a number was verified), ``no_numbers`` (nothing to verify) or,
        for a policy that doesn't check, ``unchecked``.
        """
        if policy is not WritingPolicy.GROUNDED:
            return "unchecked"
        items = doc.evidence(block_ids, max_chars=MAX_PEEK)
        res = doc.check_text(text, block_ids, rel_tol=rel_tol, small_int_max=small_int_max, max_chars=MAX_PEEK,
                            year_range=year_range, skip=[f.span for f in fills], items=items)
        if not res.ok:
            nearest = {t.text: _nearest(t, items, any_unit=t.text in res.reasons) for t in res.unmatched}
            parts = []
            for t in res.unmatched:
                why = res.reasons.get(t.text)
                part = f"the number {t.text!r} " + (why if why else "does not appear in the cited data")
                if nearest[t.text]:
                    part += ("; the matching placeholder is " if why else "; the closest cited value is ") + \
                        nearest[t.text][0]
                parts.append(part)
            example = next((n[0].split(" = ")[0] for n in nearest.values() if n), None) or \
                next((v.split(" = ")[0] for v in _values(items, 1)), "{r3.frequency[2]}")
            raise ReportOperationError(
                "ungrounded", "; ".join(parts) + f". Write placeholders such as {example} instead of typing "
                "numbers: the server fills in the value and its unit. Nothing was written.",
                unmatched=[t.text for t in res.unmatched], cited=list(block_ids),
                placeholders={k: v for k, v in nearest.items() if v}, values=_values(items))
        last_check["numbers"] = res.provenance(items)
        if fills:
            last_check["filled"] = [f.to_dict() for f in fills]
        return "checked" if (res.checked or any(f.kind != "text" for f in fills)) else "no_numbers"

    def _numeric(items):
        return [e for e in items if e.origin == "data" and e.key and not e.is_text
                and e.quantity not in ("index", "int", "count")]

    def _values(items, limit=12):
        """The cited values as placeholders: ``{r3.frequency[1]} = 1648.23 cm-1``."""
        from .Fill import ref_for
        return [f"{{{ref_for(e, items)}}} = {e.describe().split(' = ', 1)[1]}" for e in _numeric(items)[:limit]]

    def _nearest(tok, items, any_unit=False, limit=2):
        """The placeholders of the cited values closest to the number ``tok`` (``{r3.frequency[1]} = 1648.23 cm-1``)."""
        from .Fill import ref_for
        pool = _numeric(items)
        if tok.percent:
            pool = [e for e in pool if e.percent or e.quantity in ("fraction", "ratio", "percent")] or pool
        elif tok.unit and not any_unit:
            pool = [e for e in pool if e.unit == tok.unit] or pool
        x = abs(tok.value)
        scored = sorted((abs(abs(e.value) - x) / max(x, 1e-12), i, e) for i, e in enumerate(pool))
        return [f"{{{ref_for(e, items)}}} = {e.describe().split(' = ', 1)[1]}" for rel, _, e in scored[:limit]
                if rel <= 0.5]

    def _fill(text, cites):
        return doc.fill_text(text, cites, allow_derived=allow_derived)

    def _fill_caption(text, block_id):
        filled, cites, fills = doc.fill_text(text, [block_id], allow_derived=False)
        if cites != [block_id]:
            raise ReportOperationError("bad_reference", "a caption can only refer to its own block's data",
                                       block_id=block_id)
        return filled, fills

    last_check = {}

    def verified(out):
        """Adds ``numbers`` (which cited value each number matched) to a text tool's result."""
        nums, filled = last_check.pop("numbers", None), last_check.pop("filled", None)
        if nums:
            out["numbers"] = nums
        if filled:
            out["filled"] = filled
        return out

    def _need_cites(cites, what):
        if policy is WritingPolicy.GROUNDED and not cites:
            raise ReportOperationError(
                "needs_citation", f"{what} must cite the readout blocks it is about (`cites`): the report only "
                f"accepts text that can be checked against data. Nothing was written.")

    def _add_readout_with_caption(handle, include, exclude, caption, after, under):
        # validate the block first, then the caption against it; roll back if the caption is refused
        rec = doc.add_readout(handle, include=include, exclude=exclude, after=after, under=under)
        try:
            caption, fills = _fill_caption(caption, rec.block_id)
            status = _check(caption, [rec.block_id], fills)
            doc.set_caption(rec.block_id, caption, status=status)
        except Exception:
            doc.remove(rec.block_id)
            raise
        return verified({"ok": True, "block_id": rec.block_id, "outline": doc.outline()})

    def add_text(text, cites=None, after=None, under=None):
        _text_allowed()
        cites = list(cites or [])
        for c in cites:
            doc.get(c)
        text, cites, fills = _fill(text, cites)
        _need_cites(cites, "a paragraph")
        status = _check(text, cites, fills)
        return verified(doc.add_text(text, cites=cites, after=after, under=under, status=status,
                                     fills=[f.record() for f in fills] or None).to_dict())

    def set_caption(block_id, text):
        doc.check_unlocked(block_id)
        _text_allowed()
        doc.get(block_id)
        text, fills = _fill_caption(text, block_id)
        return verified(doc.set_caption(block_id, text, status=_check(text, [block_id], fills)).to_dict())

    def edit_text(block_id, text, cites=None):
        blk = doc.get(block_id)
        doc.check_unlocked(block_id)
        if isinstance(blk, Heading):
            return doc.edit_text(block_id, text).to_dict()
        _text_allowed()
        if isinstance(blk, Prose):
            cites = list(blk.cites if cites is None else cites)
            for c in cites:
                doc.get(c)
            text, cites, fills = _fill(text, cites)
            _need_cites(cites, "a paragraph")
            status = _check(text, cites, fills)
            return verified(doc.edit_text(block_id, text, status=status, cites=cites,
                                          fills=[f.record() for f in fills] or None).to_dict())
        return doc.edit_text(block_id, text).to_dict()

    def move(block_id, after):
        doc.check_unlocked(block_id)
        return doc.move(block_id, after).to_dict()

    def move_section(heading_id, after):
        for bid in doc.section_ids(heading_id):
            doc.check_unlocked(bid)
        return doc.move_section(heading_id, after).to_dict()

    def remove(block_id):
        doc.check_unlocked(block_id)
        return doc.remove(block_id).to_dict()

    def move_source(handle, after):
        for h in doc.source_sections(handle):
            for bid in doc.section_ids(h):
                doc.check_unlocked(bid)
        return doc.move_source(handle, after).to_dict()

    obj = lambda props, req=(): {"type": "object", "properties": props, "required": list(req),
                                 "additionalProperties": False}
    add("apply_template", apply_template_tool,
              obj({"handle": _HANDLE, "after": _AFTER, "optional": dict(_NAMES, description="Optional template sections "
                                                                       "to add under 'Additional detail' (see `describe_source`).")},
                  ["handle"]),
              "Builds the source's template outline in one step: headings and readout blocks in the template's order, "
              "with its fixed captions. Sections that are unavailable for this source are skipped and listed. Add "
              "template-suggested extras with `optional`. Errors with `no_template` if the source has no fixed outline. "
              "Blocks the template locks are listed in `locked` and can't be edited, captioned, moved or removed "
              "afterwards (error `locked`); you can still add text and other blocks around them. Records the "
              "baseline 'template' for `diff`.")
    add("add_heading", mutating(add_heading),
              obj({"text": {"type": "string", "minLength": 1, "maxLength": 120}, "level": {"type": "integer", "enum": [2, 3]},
                   "after": _AFTER, "under": _UNDER}, ["text"]),
              "Adds a heading (level 2 starts a section; level 3 a subsection).")
    add("add_readout", mutating(add_readout),
              obj({"handle": _HANDLE, "include": dict(_NAMES, description="Section names from `describe_source` "
                                                      "(dotted parts allowed); omit for the source's default sections."),
                   "exclude": _NAMES, "caption": {"type": "string", "minLength": 1, "maxLength": 300}, "after": _AFTER,
                   "under": _UNDER},
                  ["handle"]),
              "Adds a readout block (a table, figure or fields of one source). The report renders it itself: you only "
              "name the source and sections. A caption is written and checked like `set_caption` (numbers as "
              "placeholders).")
    derived_note = (" A computed value is an expression of placeholders, {mean(r3.frequency[2], r3.frequency[3])} "
                    "(+ - * / and mean, sum, min, max, abs, diff, ratio)." if allow_derived else "")
    add("add_text", mutating(add_text),
              obj({"text": {"type": "string", "minLength": 1, "maxLength": 1500},
                   "cites": {"type": "array", "items": _ID, "maxItems": 20, "description": "Readout block ids from "
                             "`outline` or `compile` (required under the grounded policy). Every number in the text "
                             "must appear in their data."}, "after": _AFTER, "under": _UNDER}, ["text"]),
              "Adds a paragraph. Plain prose only (no Markdown headings, code or markers). WRITE EVERY NUMBER AS A "
              "PLACEHOLDER, {r3.frequency[2]} (block id, column, 1-based row): the server writes the number and its "
              f"unit from the data ({example}), so do not type the number or the unit; a text column works the "
              "same way ({r3.mode[2]}). Referenced blocks are cited automatically." + derived_note + " Typing a "
              "number is allowed but risky: under the grounded policy a paragraph must cite readout blocks, and a "
              "typed number that is not in the cited blocks' data, or is given in another unit, is rejected "
              "(`ungrounded`, with the matching placeholder) and nothing is written. The result lists `numbers` "
              "(which value each typed number matched) and `filled` (the values the server wrote).")
    add("set_caption", mutating(set_caption), obj({"block_id": _ID, "text": {"type": "string", "minLength": 1,
                                                                                    "maxLength": 300}},
                                                         ["block_id", "text"]),
              "Sets one line of caption on a readout block. Write numbers as placeholders, {r2.frequency[1]}, "
              "which the server fills in with their unit; typed numbers are checked against that block's data.")
    add("edit_text", mutating(edit_text),
              obj({"block_id": _ID, "text": {"type": "string", "minLength": 1, "maxLength": 1500},
                   "cites": {"type": "array", "items": _ID, "maxItems": 20, "description": "Replace the paragraph's "
                             "cited blocks (default: keep them)."}},
                  ["block_id", "text"]),
              "Replaces the text of a paragraph, callout or heading (paragraphs are re-checked against what they cite).")
    add("move", mutating(move), obj({"block_id": _ID, "after": dict(_AFTER, description="'start' or a block id")},
                                          ["block_id", "after"]), "Moves one block after another block (or to 'start'). Moving a heading does not move "
                                          "the blocks below it: use `move_section` to move a whole section.")
    add("move_section", mutating(move_section),
              obj({"heading_id": _ID, "after": dict(_AFTER, description="'start' or a block id; a heading id puts the "
                                                    "section after that heading's whole section")},
                  ["heading_id", "after"]),
              "Moves a heading together with every block under it (up to the next heading of the same or a higher "
              "level). Use this to reorder sections; `move` moves a single block.")
    add("remove", mutating(remove), obj({"block_id": _ID}, ["block_id"]), "Removes a block.")
    add("move_source", mutating(move_source),
              obj({"handle": _HANDLE, "after": dict(_AFTER, description="'start' or a block id; a heading id puts "
                                                     "the sections after that heading's whole section")},
                  ["handle", "after"]),
              "Moves every section that shows one source (for example all of HOD's Structure and Vibrations) "
              "together to a new place, keeping their order. Use this to reorder whole sources; `move_section` "
              "moves one section.")

    steps = {"add_heading": add_heading, "add_readout": add_readout, "add_text": add_text, "set_caption": set_caption,
             "edit_text": edit_text, "move": move, "move_section": move_section, "move_source": move_source,
             "remove": remove}

    def _subst(value, made):
        if isinstance(value, str) and re.fullmatch(r"\$\d+", value):
            k = int(value[1:])
            if not 1 <= k <= len(made) or made[k - 1] is None:
                raise ReportOperationError("bad_argument", f"{value} refers to step {k}, which has not created a block")
            return made[k - 1]
        if isinstance(value, list):
            return [_subst(v, made) for v in value]
        if isinstance(value, dict):
            return {k: _subst(v, made) for k, v in value.items()}
        return value

    def apply_edits_step(edits):
        made, results = [], []
        for i, step in enumerate(edits, 1):
            name = step["tool"]
            try:
                args = _subst(step.get("args") or {}, made)
                errors = validate_answer(schemas[name], args)
                if errors:
                    raise ReportOperationError("invalid_arguments", "; ".join(errors))
                out = steps[name](**args)
            except Exception as e:
                code, detail = getattr(e, "code", "internal"), getattr(e, "detail", repr(e))
                info = getattr(e, "info", {}) or {}
                raise ReportOperationError(code, f"step {i} ({name}): {detail}. Nothing was changed.", step=i,
                                           tool=name, **{k: v for k, v in info.items() if k not in ("step", "tool")})
            made.append(out.get("block_id"))
            results.append({"tool": name, **{k: v for k, v in out.items() if k not in ("ok", "outline")}})
        return {"ok": True, "steps": results, "order": order_line()}

    add("apply_edits", mutating(apply_edits_step),
        obj({"edits": {"type": "array", "minItems": 1, "maxItems": 20,
                       "items": {"type": "object", "properties": {
                           "tool": {"type": "string", "enum": sorted(steps)},
                           "args": {"type": "object"}}, "required": ["tool"], "additionalProperties": False},
                       "description": "Steps run in order; \"$1\", \"$2\", ... in a step's args stand for the block "
                                      "id that step 1, 2, ... created."}}, ["edits"]),
        "Runs several editing steps (add_heading, add_readout, add_text, set_caption, edit_text, move, move_section, "
        "move_source, remove, with the same arguments) as one change: if any step fails, nothing is changed and the "
        "error says which step. Returns each step's result and the report's block order.")

    if renderer is not None:
        def render(formats=None):
            res = renderer.render(doc, out_dir, formats=tuple(formats or ("md", "html", "pptx")))
            out = {"ok": res.ok, "paths": res.paths, "statuses": res.statuses, "problems": res.problems}
            if level == 1 or res.problems:
                out["next"] = ("Give the user these paths and stop." if not res.problems else
                               "Tell the user what failed (see problems) and give any paths that were written; do "
                               "not render again.")
            return out
        add("render", render,
                  obj({"formats": {"type": "array", "items": {"type": "string", "enum": ["md", "html", "pptx"]},
                                   "maxItems": 3}}),
                  "Writes the report to the output folder as Markdown, HTML and/or PowerPoint (default all three) and "
                  "returns the paths and any problems.")
    tools.context_level = level
    tools.instructions = report_instructions(catalog, level, inline_max=inline_max, derived=allow_derived,
                                             apply_edits=apply_edits, unit_style=doc.unit_style)
    return tools
