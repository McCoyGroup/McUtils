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
written. Accepted text is marked ``checked`` (a number was verified) or ``no_numbers`` (nothing to verify: the claims
were not checked). ``unchecked`` accepts the text and marks it as unchecked. ``structure_only`` turns the text tools off (``code="writing_disabled"``).
"""

import re

from ...JobDrivers.Tools import ToolSet
from .Document import ReportOperationError, Prose, Heading
from .Grounding import WritingPolicy
from .Templates import find_report_template, template_menu

__all__ = ["report_toolset", "REPORT_HINTS"]

# What a model should do next after each kind of error (`ToolSet(hints=...)` adds it to the error as ``hint``).
REPORT_HINTS = {
    "locked": "This block is locked by the report's owner. Tell the user it can't be changed and stop: do not "
              "recreate it, rewrite it somewhere else or add text next to it to stand in for the edit, unless the "
              "user separately asks for supplementary text.",
    "ungrounded": "Rewrite the text using only values exactly as peek or the block shows them (or leave the number "
                  "out) and try once more; do not compute new values. If it is refused again, tell the user.",
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
                   on_change=None, hints=None):
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
    :return: a `ToolSet`; results are plain JSON values
    """
    policy = WritingPolicy.coerce(policy)
    if not (isinstance(rel_tol, (int, float)) and 0 < rel_tol < 1):
        raise ValueError(f"rel_tol must be a number between 0 and 1, got {rel_tol!r}")
    if not (isinstance(small_int_max, int) and small_int_max >= 0):
        raise ValueError(f"small_int_max must be a non-negative integer, got {small_int_max!r}")
    if year_range is not None and not (len(year_range) == 2 and year_range[0] <= year_range[1]):
        raise ValueError(f"year_range must be (low, high) or None, got {year_range!r}")
    if renderer is not None and out_dir is None:
        raise ValueError("a renderer needs out_dir")
    tools = ToolSet(hints=REPORT_HINTS if hints is None else hints)

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

    def peek(handle, section, max_chars=2400):
        return catalog.peek(handle, section, max_chars=min(int(max_chars), MAX_PEEK))

    def flagged(rows):
        lock = set(doc.locked)
        return [dict(r, locked=True) if r["id"] in lock else r for r in rows]

    def outline():
        return flagged(doc.outline())

    tools.add("list_sources", list_sources, {"type": "object", "properties": {}, "additionalProperties": False},
              "The sources a report can show: handle, type, title, number of sections and the name of the report "
              "template that applies. Start here.")
    tools.add("describe_source", describe_source,
              {"type": "object", "properties": {"handle": _HANDLE}, "required": ["handle"], "additionalProperties": False},
              "A source's sections (name, title, description, kind, whether available and why not, whether shown by "
              "default) and its report template: the fixed outline (`template.outline`: headings with the sections "
              "under each) and the optional sections it suggests adding (`template.optional`). Section names can name "
              "a part with a dot, like `normal_modes.frequencies`. Use `apply_template` to build the outline.")
    tools.add("peek", peek,
              {"type": "object", "properties": {"handle": _HANDLE, "section": {"type": "string", "minLength": 1,
                                                                                "maxLength": 80},
                                                "max_chars": {"type": "integer", "minimum": 80, "maximum": MAX_PEEK}},
               "required": ["handle", "section"], "additionalProperties": False},
              "The text of one section of a source (numbers as they will appear), to read before writing about it. "
              f"Cut at {MAX_PEEK} characters.")
    tools.add("outline", outline, {"type": "object", "properties": {}, "additionalProperties": False},
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
                "baselines": list(track["baselines"]),
                "grounding": {"policy": policy.value, "rel_tol": rel_tol, "small_int_max": small_int_max,
                              "year_range": None if year_range is None else list(year_range)}}

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

    tools.add("compile", compile, {"type": "object", "properties": {"full_text": {"type": "boolean"}},
                                   "additionalProperties": False},
              "Reads the whole report back (it changes nothing): every block in order (text clipped to 80 characters "
              "unless `full_text`), how many captions and paragraphs are checked / no_numbers / unchecked / manual / "
              "from the template, any problems found (unknown sources, changed sources), which blocks are locked, "
              "the baselines `diff` can compare with, and the number-check settings in force.")
    tools.add("checkpoint", checkpoint,
              {"type": "object", "properties": {"label": {"type": "string", "minLength": 1, "maxLength": 30}},
               "additionalProperties": False},
              "Records the report as it is now as a baseline for `diff` (named 'checkpoint', plus `label` if given). "
              "Baselines 'start' (the report when it was opened) and 'template' (right after `apply_template`) "
              "exist already.")
    tools.add("diff", diff, {"type": "object", "properties": {"since": {"type": "string", "minLength": 1,
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

    def _check(text, block_ids):
        """
        Raise ``ungrounded`` if the numbers of ``text`` aren't in the data of the readout blocks ``block_ids``;
        otherwise the status to record: ``checked`` (a number was verified), ``no_numbers`` (nothing to verify) or,
        for a policy that doesn't check, ``unchecked``.
        """
        if policy is not WritingPolicy.GROUNDED:
            return "unchecked"
        res = doc.check_text(text, block_ids, rel_tol=rel_tol, small_int_max=small_int_max, max_chars=MAX_PEEK,
                            year_range=year_range)
        if not res.ok:
            raise ReportOperationError(
                "ungrounded", "; ".join(res.errors()) + ". Nothing was written.",
                unmatched=[t.text for t in res.unmatched], cited=list(block_ids))
        return "checked" if res.checked else "no_numbers"

    def _need_cites(cites, what):
        if policy is WritingPolicy.GROUNDED and not cites:
            raise ReportOperationError(
                "needs_citation", f"{what} must cite the readout blocks it is about (`cites`): the report only "
                f"accepts text that can be checked against data. Nothing was written.")

    def _add_readout_with_caption(handle, include, exclude, caption, after, under):
        # validate the block first, then the caption against it; roll back if the caption is refused
        rec = doc.add_readout(handle, include=include, exclude=exclude, after=after, under=under)
        try:
            status = _check(caption, [rec.block_id])
            doc.set_caption(rec.block_id, caption, status=status)
        except Exception:
            doc.remove(rec.block_id)
            raise
        return {"ok": True, "block_id": rec.block_id, "outline": doc.outline()}

    def add_text(text, cites=None, after=None, under=None):
        _text_allowed()
        cites = list(cites or [])
        for c in cites:
            doc.get(c)
        _need_cites(cites, "a paragraph")
        status = _check(text, cites)
        return doc.add_text(text, cites=cites, after=after, under=under, status=status).to_dict()

    def set_caption(block_id, text):
        doc.check_unlocked(block_id)
        _text_allowed()
        return doc.set_caption(block_id, text, status=_check(text, [block_id])).to_dict()

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
            _need_cites(cites, "a paragraph")
            status = _check(text, cites)
            return doc.edit_text(block_id, text, status=status, cites=cites).to_dict()
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

    obj = lambda props, req=(): {"type": "object", "properties": props, "required": list(req),
                                 "additionalProperties": False}
    tools.add("apply_template", apply_template_tool,
              obj({"handle": _HANDLE, "after": _AFTER, "optional": dict(_NAMES, description="Optional template sections "
                                                                       "to add under 'Additional detail' (see `describe_source`).")},
                  ["handle"]),
              "Builds the source's template outline in one step: headings and readout blocks in the template's order, "
              "with its fixed captions. Sections that are unavailable for this source are skipped and listed. Add "
              "template-suggested extras with `optional`. Errors with `no_template` if the source has no fixed outline. "
              "Blocks the template locks are listed in `locked` and can't be edited, captioned, moved or removed "
              "afterwards (error `locked`); you can still add text and other blocks around them. Records the "
              "baseline 'template' for `diff`.")
    tools.add("add_heading", mutating(add_heading),
              obj({"text": {"type": "string", "minLength": 1, "maxLength": 120}, "level": {"type": "integer", "enum": [2, 3]},
                   "after": _AFTER, "under": _UNDER}, ["text"]),
              "Adds a heading (level 2 starts a section; level 3 a subsection).")
    tools.add("add_readout", mutating(add_readout),
              obj({"handle": _HANDLE, "include": dict(_NAMES, description="Section names from `describe_source` "
                                                      "(dotted parts allowed); omit for the source's default sections."),
                   "exclude": _NAMES, "caption": {"type": "string", "minLength": 1, "maxLength": 300}, "after": _AFTER,
                   "under": _UNDER},
                  ["handle"]),
              "Adds a readout block (a table, figure or fields of one source). The report renders it itself: you only "
              "name the source and sections. A caption is checked like `set_caption`.")
    tools.add("add_text", mutating(add_text),
              obj({"text": {"type": "string", "minLength": 1, "maxLength": 1500},
                   "cites": {"type": "array", "items": _ID, "maxItems": 20, "description": "Readout block ids from "
                             "`outline` or `compile` (required under the grounded policy). Every number in the text "
                             "must appear in their data."}, "after": _AFTER, "under": _UNDER}, ["text"]),
              "Adds a paragraph. Plain prose only (no Markdown headings, code or markers). Under the grounded policy "
              "it must cite readout blocks, and a number that is not in the cited blocks' data is rejected "
              "(`ungrounded`, with the unmatched numbers) and nothing is written: quote values as shown by `peek`, "
              "do not compute new ones.")
    tools.add("set_caption", mutating(set_caption), obj({"block_id": _ID, "text": {"type": "string", "minLength": 1,
                                                                                    "maxLength": 300}},
                                                         ["block_id", "text"]),
              "Sets one line of caption on a readout block; numbers are checked against that block's data.")
    tools.add("edit_text", mutating(edit_text),
              obj({"block_id": _ID, "text": {"type": "string", "minLength": 1, "maxLength": 1500},
                   "cites": {"type": "array", "items": _ID, "maxItems": 20, "description": "Replace the paragraph's "
                             "cited blocks (default: keep them)."}},
                  ["block_id", "text"]),
              "Replaces the text of a paragraph, callout or heading (paragraphs are re-checked against what they cite).")
    tools.add("move", mutating(move), obj({"block_id": _ID, "after": dict(_AFTER, description="'start' or a block id")},
                                          ["block_id", "after"]), "Moves one block after another block (or to 'start'). Moving a heading does not move "
                                          "the blocks below it: use `move_section` to move a whole section.")
    tools.add("move_section", mutating(move_section),
              obj({"heading_id": _ID, "after": dict(_AFTER, description="'start' or a block id; a heading id puts the "
                                                    "section after that heading's whole section")},
                  ["heading_id", "after"]),
              "Moves a heading together with every block under it (up to the next heading of the same or a higher "
              "level). Use this to reorder sections; `move` moves a single block.")
    tools.add("remove", mutating(remove), obj({"block_id": _ID}, ["block_id"]), "Removes a block.")

    if renderer is not None:
        def render(formats=None):
            res = renderer.render(doc, out_dir, formats=tuple(formats or ("md", "html", "pptx")))
            return {"ok": res.ok, "paths": res.paths, "statuses": res.statuses, "problems": res.problems}
        tools.add("render", render,
                  obj({"formats": {"type": "array", "items": {"type": "string", "enum": ["md", "html", "pptx"]},
                                   "maxItems": 3}}),
                  "Writes the report to the output folder as Markdown, HTML and/or PowerPoint (default all three) and "
                  "returns the paths and any problems.")
    return tools
