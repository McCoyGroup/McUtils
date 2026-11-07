"""
The instructions a report server gives a model (the MCP ``initialize`` text), at three context levels.

``context_level`` trades how much the model is told for how much it has to read on every request:

1. ``compact`` — for small or slow models (tested on a 30B model that ran out of time, not out of rules): the
   sources and their templates are listed in the instructions (no ``list_sources`` / ``describe_source`` round
   trips while the catalog is small), the instructions are short, tool descriptions are one sentence, every change
   returns the report's block order, and results say what to do next (``next``).
2. ``standard`` — the v2 behaviour: full descriptions, receipts without the order, the model reads the report with
   ``outline`` / ``compile``. The default.
3. ``full`` — everything in ``standard`` plus the reasons behind the rules, for models that plan several steps
   ahead.

Every level tells the model, strongly, to write values as placeholders (``{r3.frequency[2]}``): the server writes the
number and its unit, so nothing is mistyped or given in the wrong unit. Two things are switched on by the owner, not
by the level: computed values (``derived``) and the ``apply_edits`` tool; the instructions mention them only when
they are on.

The guards (numbers checked against the data, citations, locks) are the same at every level: a level changes what
the model is shown and which conveniences it gets, never what the server accepts.
"""

from .Templates import find_report_template

__all__ = ["CONTEXT_LEVELS", "context_level", "REPORT_INSTRUCTIONS", "report_instructions", "catalog_summary",
           "DERIVED_NOTE", "APPLY_EDITS_NOTE"]

CONTEXT_LEVELS = {"compact": 1, "standard": 2, "full": 3}


def context_level(level):
    """``1``, ``2`` or ``3`` from a number or a name (``compact``, ``standard``, ``full``)."""
    if isinstance(level, str):
        if level in CONTEXT_LEVELS:
            return CONTEXT_LEVELS[level]
        if level.isdigit():
            level = int(level)
    if isinstance(level, bool) or level not in (1, 2, 3):
        raise ValueError(f"context_level must be 1, 2, 3 or one of {list(CONTEXT_LEVELS)}, got {level!r}")
    return level


REPORT_INSTRUCTIONS = """\
You are building a report from readouts of named sources. You choose and order content and write short captions and
prose; the server renders everything.

Start with list_sources, then describe_source for each source you use: it shows the sections, what each contains, and
the source's report template. If the requested source is not listed, tell the user which sources are available and
stop: do not substitute another source, add a heading implying it exists, or write about it from memory. If the
template has an outline, apply_template builds it in one call (optionally with some of the template's optional
sections); then adjust with add_readout, add_heading, add_text, move, move_section and remove.

Two kinds of names: a source handle (hoh) and section name (frequencies) are for describe_source, peek, add_readout and
apply_template; a block id (h1, r2, p1) comes from outline or compile and is for after, under, cites, move, edit_text,
set_caption and remove. peek reads a source's section, never a block or a paragraph. `after` is one block id; to add
under a heading use `under` with the heading id. Moving a heading does not move what is under it; move_section does.
To reorder whole sources (all of HOD's sections before HOH's), use move_source(handle, after) once per source; a
`warnings` entry in a result says when a source's sections have been split up.

Mutating tools only return a receipt (block id, block count, revision). Call compile to read the whole report back
(it only reads: it checks the report, lists the locked blocks and counts the text by status). To see what you
changed, call diff: since='last_change' is the most recent request; since='template' is everything since
apply_template; since='start' is everything since the report was opened; checkpoint(label) records your own baseline
to give to diff(since=...) later. Say which baseline a summary of changes is relative to.

Blocks marked locked (by the report's template) can't be edited, captioned, moved or removed. If asked to change one,
report that limit to the user and stop; do not recreate its content or add text next to it to simulate the edit, and
add supplementary text around it only if the user separately asks for that.

Never write Markdown headings, code or markers; give plain text only.

WRITE EVERY NUMBER AS A PLACEHOLDER. To state a value from a block, write {BLOCK.COLUMN[ROW]}: the readout block id
(from outline or compile), the column or field name, and the 1-based row as peek shows it, for example
{r3.frequency[2]}. The server replaces it with the value and its unit exactly as the data has them (3803.3 cm⁻¹), so
you never copy a digit, round, convert or choose a unit. Do not type the unit after a placeholder: the server adds it
(a different unit is refused). Text columns work too: {r3.mode[2]} writes the label in that row. If you do not know
the column names, peek shows them. Typing a number yourself is allowed, but it is the risky way: it is checked
against the cited blocks' data, a number with a unit must match a value in that unit, a percentage only matches a
percentage, and a number that is not in the data of the blocks you cite is rejected (ungrounded) with the placeholder
that matches it, and nothing is written. Text under the grounded policy must cite blocks (`cites`; blocks named by
placeholders are cited for you). Statuses: checked means a number in the text was verified against the cited data (or
filled in by the server); no_numbers means the text had nothing to verify. The checker verifies numbers only, so
describe what the data shows and leave out interpretation the source does not give. compile reports the tolerance in
force.

Errors carry a `hint` and `retry`: "no" means tell the user instead of repeating the request, "once" means one
corrected attempt. The report file is saved after every change. A successful compile is enough to finish a
report-writing request (compile(full_text=True) reads the saved prose). Use render only when the user asks for
exported files; when it succeeds, report the paths and finish rather than rendering or inspecting the same output
again.
"""

COMPACT_INSTRUCTIONS = """\
You build a report from the sources listed below; the server renders it. Use as few tool calls as you can and answer
the user as soon as the request is done.

If the user asks for a source that is not listed, tell them which sources are available and stop. apply_template(handle)
builds a source's standard report in one call. peek(handle, section) shows a section's data. Every change returns
`order`, the report's blocks in order (h = heading, r = readout, p = paragraph); use those ids for after, under,
cites, move_section and remove. under=<heading id> adds at the end of that section; after=<block id> adds right after
that block.

add_text writes a paragraph: plain sentences (no Markdown) with cites = readout ids. WRITE EVERY NUMBER AS A
PLACEHOLDER, {r3.frequency[2]} (readout id, column, row): the server fills in the number and its unit (3803.3 cm⁻¹).
Never type a number or a unit yourself; do not add a unit after a placeholder. {r3.mode[2]} writes a text column's
label. peek shows the columns. If you type a number anyway it must be in the cited data in that unit, or the text is
refused (the error shows the matching placeholder) and not saved.

move_section(heading_id, after) moves one section; move_source(handle, after) moves all sections of a source. Locked
blocks can't be changed: tell the user and stop. Errors have a `hint`; if `retry` is "no", tell the user instead of
trying again. diff(since="template", "start" or "last_change") lists changes; say which baseline you used. render only
when the user asks for files; then give the paths and stop.
"""

FULL_EXTRA = """\
Why the rules: the report is checked against its sources, so every number must be traceable to a cited block, and a
placeholder is the one way to state a value that cannot be wrong: it is read from the block when the text is saved
and again whenever the report is checked, so a later change to the data is noticed. Typed numbers are the exception
that needs checking, which is why they can be refused. Say only what the data shows; the checker cannot tell a correct
interpretation from an invented one.
"""

DERIVED_NOTE = """\
Computed values are switched on for this report: a value computed from the data is written as an expression of
placeholders, {mean(r3.frequency[2], r3.frequency[3])} (+ - * / and mean, sum, min, max, abs, diff, ratio); the server
computes it and writes it with the inputs' unit. Never compute a value yourself.
"""

APPLY_EDITS_NOTE = """\
apply_edits runs several changes in one call, all or nothing: a list of {tool, args} steps using the same tools and
arguments as above; "$1", "$2", ... in a later step's arguments stand for the block id the first, second, ... step
created. Prefer it when you know several changes in advance (adding text under two sections, moving several
sections).
"""


def catalog_summary(catalog, level=2, inline_max=8):
    """
    The sources of ``catalog`` as instruction text (handle, title, template outline and optional sections), or
    ``None`` if there are more than ``inline_max`` sources (the model then uses ``list_sources``).
    """
    if catalog is None or len(catalog) > inline_max:
        return None
    lines = ["Sources (handle: title; template outline; optional sections):"]
    for h in catalog.handles():
        src = catalog.get(h)
        t = find_report_template(src)
        if t.is_fixed:
            outline = "; ".join(f"{head} [{', '.join(names)}]" for head, names in t.sections)
        else:
            outline = "no template: build it with add_heading and add_readout; sections " + \
                      ", ".join(src.section_names())
        line = f"- {h}: {src.title or h}; {outline}"
        if t.optional:
            line += f"; optional: {', '.join(t.optional)}"
        if level >= 3:
            line += f"; all sections: {', '.join(src.section_names())}"
        lines.append(line)
    return "\n".join(lines)


def report_instructions(catalog=None, level=2, inline_max=8, derived=False, apply_edits=False, unit_style=None):
    """
    The instructions for ``context_level`` ``level``, with the catalog listed when it is small (see
    `catalog_summary`). ``derived`` / ``apply_edits`` add the notes for computed values and the ``apply_edits`` tool,
    which the owner switches on. ``unit_style`` (``"unicode"``, ``"ascii"``, ``"latex"``) sets how the examples
    show a filled value (default `UnitsData.label_style`).
    """
    level = context_level(level)
    summary = catalog_summary(catalog, level, inline_max)
    if level == 1:
        text = COMPACT_INSTRUCTIONS
        if summary is None:
            text = text.replace("from the sources listed below", "from named sources (call list_sources, then "
                                                                   "describe_source)")
    else:
        text = REPORT_INSTRUCTIONS
        if summary is not None:
            text = text.replace("Start with list_sources, then describe_source for each source you use: it shows "
                                "the sections, what each contains, and\nthe source's report template.",
                                "The sources and their templates are listed below (list_sources gives the same); describe_source shows a source's "
                                "sections and what\neach contains.")
        if level >= 3:
            text = text + "\n" + FULL_EXTRA
    if derived:
        text = text + "\n" + DERIVED_NOTE
    if apply_edits:
        text = text + "\n" + APPLY_EDITS_NOTE
    from .Fill import example_value
    text = text.replace("3803.3 cm⁻¹", example_value(unit_style))
    from ...Data import UnitsData
    if (unit_style or UnitsData.label_style) == "latex":
        text += "\nFilled values are written in LaTeX math ($3803.3\\,\\mathrm{cm^{-1}}$): do not type $ or units yourself."
    return text if summary is None else text + "\n" + summary + "\n"
