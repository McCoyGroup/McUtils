"""
Tool mode: the operations of a `ReportDocument` as a `McUtils.JobDrivers.ToolSet`, for a model that drives the report
itself. This module is a thin layer over the document's own Python API (`ReportDocument.apply_template`, `lock`,
`snapshot`, `diff`, `transaction`, `check_text`, ...), which is what a person uses directly; the tools add the JSON
schemas, the writing policy, receipts and revision numbers, and never do anything the document can't do itself (through an MCP server, `McUtils.JobDrivers.MCP`, or any other caller). The model never writes Markdown, code
or markers: it reads the sources (`describe_source`, `peek`), applies the source's template or builds blocks one at a
time, and writes captions and prose, which are checked against the data they cite.

Mutating tools answer with a short receipt (the block id, the block count and the document's revision number). The
model reads the whole document with ``compile`` (which also checks it and sets a checkpoint) and sees what changed
with ``diff`` (since the last mutating request, or since the last ``compile``).

A template can lock parts of the report (``ReportTemplate.locked`` / ``locked_headings``): the blocks `apply_template`
builds for them can't be edited, captioned, moved or removed by the tools (``code="locked"``); the model can still add
text and other blocks around them. The locked block ids are kept in ``doc.meta["locked"]`` (saved with the report), and
the owner can change them with `ReportDocument.lock` / `unlock`.

Under the ``grounded`` policy a number in text that does not appear in the cited blocks' data is rejected with
``code="ungrounded"`` and the unmatched numbers, and nothing is written. ``unchecked`` accepts the text and marks it
as unchecked. ``structure_only`` turns the text tools off (``code="writing_disabled"``).
"""

from ...JobDrivers.Tools import ToolSet
from .Document import ReportOperationError, Prose, Heading
from .Grounding import WritingPolicy
from .Templates import find_report_template, template_menu

__all__ = ["report_toolset"]

MAX_PEEK = 4000
_ID = {"type": "string", "minLength": 1, "maxLength": 40}
_AFTER = {"type": "string", "minLength": 1, "maxLength": 40,
          "description": "Insert after this block id, or 'start'. Omit to append at the end."}
_NAMES = {"type": "array", "items": {"type": "string", "minLength": 1, "maxLength": 80}, "maxItems": 40}


def report_toolset(doc, catalog, renderer=None, policy="grounded", rel_tol=1e-3, small_int_max=10, year_range=(1900, 2100), out_dir=None,
                   on_change=None):
    """
    The tools for editing ``doc`` (a `ReportDocument` built against ``catalog``).

    :param renderer: a `ReportRenderer`; the ``render`` tool is only defined when one is given
    :param policy: a `WritingPolicy` (or its value): ``grounded`` (default), ``unchecked`` or ``structure_only``
    :param out_dir: where ``render`` writes (required with ``renderer``)
    :param rel_tol: relative tolerance of the number check under ``grounded`` (a number also matches within half a unit
        of its last written digit); ``small_int_max``: integers up to this are not checked; ``year_range``: four-digit
        integers in this range are taken to be years and not checked (``None`` checks them)
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
    tools = ToolSet()

    track = {"revision": 0, "before": doc.snapshot(), "before_revision": 0, "checkpoint": doc.snapshot(),
             "checkpoint_revision": 0}

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
              {"type": "object", "properties": {"handle": _ID}, "required": ["handle"], "additionalProperties": False},
              "A source's sections (name, title, description, kind, whether available and why not, whether shown by "
              "default) and its report template: the fixed outline (`template.outline`: headings with the sections "
              "under each) and the optional sections it suggests adding (`template.optional`). Section names can name "
              "a part with a dot, like `normal_modes.frequencies`. Use `apply_template` to build the outline.")
    tools.add("peek", peek,
              {"type": "object", "properties": {"handle": _ID, "section": {"type": "string", "minLength": 1,
                                                                            "maxLength": 80},
                                                "max_chars": {"type": "integer", "minimum": 80, "maximum": MAX_PEEK}},
               "required": ["handle", "section"], "additionalProperties": False},
              "The text of one section (numbers as they will appear), to read before writing about it. Cut at "
              f"{MAX_PEEK} characters.")
    tools.add("outline", outline, {"type": "object", "properties": {}, "additionalProperties": False},
              "The report so far: one row per block (id, kind, text or handle/sections, caption; `locked` if the block "
              "can't be changed). Mutating tools "
              "only return a receipt; use this, `compile` or `diff` to see the result.")

    def compile(full_text=False):
        """The whole document, checked, as the model should read it; sets the checkpoint ``diff`` can compare with."""
        if full_text:
            blocks = flagged([{"id": b.id, "kind": b.kind, **{k: v for k, v in vars(b).items()
                                                               if k != "id" and v not in (None, [], False)}}
                              for b in doc.blocks])
        else:
            blocks = flagged(doc.outline())
        out = {"revision": track["revision"], "title": doc.title, "n_blocks": len(doc.blocks), "blocks": blocks,
               "locked": doc.locked, "text_status": doc.text_status(), "problems": [e.to_dict() for e in doc.validate()],
               "changes_since_last_compile": len(doc.diff(track["checkpoint"])),
               "grounding": {"policy": policy.value, "rel_tol": rel_tol, "small_int_max": small_int_max,
                             "year_range": None if year_range is None else list(year_range)}}
        track["checkpoint"], track["checkpoint_revision"] = doc.snapshot(), track["revision"]
        return out

    def diff(since="last_change"):
        old, rev = (track["before"], track["before_revision"]) if since == "last_change" else \
            (track["checkpoint"], track["checkpoint_revision"])
        changes = doc.diff(old)
        return {"since": since, "from_revision": rev, "revision": track["revision"], "n_changes": len(changes),
                "changes": changes}

    tools.add("compile", compile, {"type": "object", "properties": {"full_text": {"type": "boolean"}},
                                   "additionalProperties": False},
              "Reads the whole report back: every block in order (text clipped to 80 characters unless "
              "`full_text`), how much text is grounded / unchecked / manual / from the template, any problems found "
              "(unknown sources, changed sources), which blocks are locked, and the grounding settings in force. Also sets the checkpoint that "
              "`diff` with since='compile' compares against. Call it when you have finished a round of edits.")
    tools.add("diff", diff, {"type": "object", "properties": {"since": {"type": "string",
                                                                       "enum": ["last_change", "compile"]}},
                             "additionalProperties": False},
              "What changed: since='last_change' (default) is the effect of the most recent mutating request; "
              "since='compile' is everything since the last `compile` (or since the report was opened). Each change is "
              "added (with the block it follows), removed, changed (field: from, to) or moved.")

    # ---- building ---------------------------------------------------------------------------------- #
    def apply_template(handle, after=None, optional=None):
        return {"ok": True, **doc.apply_template(handle, after=after, optional=optional or ())}

    def add_heading(text, level=2, after=None):
        return doc.add_heading(text, level=level, after=after).to_dict()

    def add_readout(handle, include=None, exclude=None, caption=None, after=None):
        if caption is None:
            return doc.add_readout(handle, include=include, exclude=exclude, after=after).to_dict()
        _text_allowed()
        return _add_readout_with_caption(handle, include, exclude, caption, after)

    def _text_allowed():
        if policy is WritingPolicy.STRUCTURE_ONLY:
            raise ReportOperationError("writing_disabled", "this report is structure-only: text and captions are "
                                       "not written by the model", policy=policy.value)

    def _status():
        return "grounded" if policy is WritingPolicy.GROUNDED else "unchecked"

    def _check(text, block_ids):
        """Raise ``ungrounded`` if the numbers of ``text`` aren't in the data of the readout blocks ``block_ids``."""
        if policy is not WritingPolicy.GROUNDED:
            return
        res = doc.check_text(text, block_ids, rel_tol=rel_tol, small_int_max=small_int_max, max_chars=MAX_PEEK,
                            year_range=year_range)
        if not res.ok:
            hint = "" if block_ids else " (the text cites no blocks, so there is no data to check it against; pass `cites`)"
            raise ReportOperationError(
                "ungrounded", "; ".join(res.errors()) + hint + ". Nothing was written.",
                unmatched=[t.text for t in res.unmatched], cited=list(block_ids))

    def _add_readout_with_caption(handle, include, exclude, caption, after):
        # validate the block first, then the caption against it; roll back if the caption is refused
        rec = doc.add_readout(handle, include=include, exclude=exclude, after=after)
        try:
            _check(caption, [rec.block_id])
            doc.set_caption(rec.block_id, caption, status=_status())
        except Exception:
            doc.remove(rec.block_id)
            raise
        return {"ok": True, "block_id": rec.block_id, "outline": doc.outline()}

    def add_text(text, cites=None, after=None):
        _text_allowed()
        cites = list(cites or [])
        for c in cites:
            doc.get(c)
        _check(text, cites)
        return doc.add_text(text, cites=cites, after=after, status=_status()).to_dict()

    def set_caption(block_id, text):
        doc.check_unlocked(block_id)
        _text_allowed()
        _check(text, [block_id])
        return doc.set_caption(block_id, text, status=_status()).to_dict()

    def edit_text(block_id, text):
        blk = doc.get(block_id)
        doc.check_unlocked(block_id)
        if isinstance(blk, Heading):
            return doc.edit_text(block_id, text).to_dict()
        _text_allowed()
        if isinstance(blk, Prose):
            _check(text, blk.cites)
            return doc.edit_text(block_id, text, status=_status()).to_dict()
        return doc.edit_text(block_id, text).to_dict()

    def move(block_id, after):
        doc.check_unlocked(block_id)
        return doc.move(block_id, after).to_dict()

    def remove(block_id):
        doc.check_unlocked(block_id)
        return doc.remove(block_id).to_dict()

    obj = lambda props, req=(): {"type": "object", "properties": props, "required": list(req),
                                 "additionalProperties": False}
    tools.add("apply_template", mutating(apply_template),
              obj({"handle": _ID, "after": _AFTER, "optional": dict(_NAMES, description="Optional template sections "
                                                                    "to add under 'Additional detail' (see `describe_source`).")},
                  ["handle"]),
              "Builds the source's template outline in one step: headings and readout blocks in the template's order, "
              "with its fixed captions. Sections that are unavailable for this source are skipped and listed. Add "
              "template-suggested extras with `optional`. Errors with `no_template` if the source has no fixed outline. "
              "Blocks the template locks are listed in `locked` and can't be edited, captioned, moved or removed "
              "afterwards (error `locked`); you can still add text and other blocks around them.")
    tools.add("add_heading", mutating(add_heading),
              obj({"text": {"type": "string", "minLength": 1, "maxLength": 120}, "level": {"type": "integer", "enum": [2, 3]},
                   "after": _AFTER}, ["text"]),
              "Adds a heading (level 2 starts a section; level 3 a subsection).")
    tools.add("add_readout", mutating(add_readout),
              obj({"handle": _ID, "include": dict(_NAMES, description="Section names from `describe_source` "
                                                  "(dotted parts allowed); omit for the source's default sections."),
                   "exclude": _NAMES, "caption": {"type": "string", "minLength": 1, "maxLength": 300}, "after": _AFTER},
                  ["handle"]),
              "Adds a readout block (a table, figure or fields of one source). The report renders it itself: you only "
              "name the source and sections. A caption is checked like `set_caption`.")
    tools.add("add_text", mutating(add_text),
              obj({"text": {"type": "string", "minLength": 1, "maxLength": 1500},
                   "cites": {"type": "array", "items": _ID, "maxItems": 20, "description": "Ids of the readout blocks "
                             "this text is about. Under the grounded policy every number in the text must appear in "
                             "their data."}, "after": _AFTER}, ["text"]),
              "Adds a paragraph. Plain prose only (no Markdown headings, code or markers). Under the grounded policy "
              "a number that is not in the cited blocks' data is rejected (`ungrounded`, with the unmatched numbers) "
              "and nothing is written: quote values as shown by `peek`, do not compute new ones.")
    tools.add("set_caption", mutating(set_caption), obj({"block_id": _ID, "text": {"type": "string", "minLength": 1,
                                                                                    "maxLength": 300}},
                                                         ["block_id", "text"]),
              "Sets one line of caption on a readout block; numbers are checked against that block's data.")
    tools.add("edit_text", mutating(edit_text), obj({"block_id": _ID, "text": {"type": "string", "minLength": 1,
                                                                                "maxLength": 1500}},
                                                     ["block_id", "text"]),
              "Replaces the text of a paragraph, callout or heading (paragraphs are re-checked against what they cite).")
    tools.add("move", mutating(move), obj({"block_id": _ID, "after": dict(_AFTER, description="'start' or a block id")},
                                          ["block_id", "after"]), "Moves a block after another block (or to 'start').")
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
