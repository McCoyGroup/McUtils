"""
Encouraging placeholders without requiring them.

The number check (`McUtils.Readouts.Reports.Grounding`) is off by default: a model may type a number when it has a
reason to (a value from the user's request, a literature value, a count), and the report records which numbers were
written by the server (placeholders), which were given from outside the data (literals, ``{=300 K}``) and which were
simply typed. This module is what makes the placeholder the easy path:

* `column_summary` / `column_values`: the placeholders of a readout block (``{r3.frequency[ROW]}``, its rows, its unit
  and an example), for the receipts of ``add_readout`` / ``apply_template``, the ``values`` tool and the footer of
  ``peek``;
* `advise`: notes on the numbers a paragraph typed (matches a value in the data: here is the placeholder; is not in the
  data: mark it ``{=...}`` if it is meant to come from outside). Notes never block a text;
* `autolink`: rewrite typed numbers that are exactly a value of the data into placeholders (opt-in);
* `coverage`: how many numbers of a report are placeholders, literals or typed, and how many typed ones are values of
  the data (``ReportDocument.number_coverage``).
"""

from .Document import ReadoutBlock, Prose
from .Fill import ref_for, fill_text, find_markers, fill_spans, _column
from .Grounding import (extract_numbers, unit_after, unit_shorthand, _is_exempt, _skipped, _near, _compatible)

__all__ = ["column_summary", "column_values", "typed_numbers", "matching_items", "advise", "autolink", "coverage",
           "default_cites"]

_NOT_VALUES = ("index", "int", "count")


def default_cites(doc, cites, limit=8):
    """``cites`` if there are any, else the readout blocks of ``doc`` (the data a paragraph without citations could be about)."""
    if cites:
        return list(cites)
    return [b.id for b in doc.blocks if isinstance(b, ReadoutBlock)][:limit]


# ---- the placeholders of a block ------------------------------------------------------------------- #
def _columns(items, block):
    cols = {}
    for e in items:
        if e.block == block and e.origin == "data" and e.key:
            cols.setdefault(e.key, []).append(e)
    return list(cols.items())


def _value_text(ref, items, style):
    return fill_text("{" + ref + "}", items, style=style)[0]


def column_summary(items, block, style=None, section=None, limit=10):
    """
    The columns and fields of readout block ``block`` as placeholders, from the `EvidenceSet` of the block:
    ``[{"column", "rows", "unit", "use", "example", "line"}]``. ``use`` writes the first row (``{r3.frequency[1]}``); a
    column of several rows is written ``{r3.frequency[ROW]}`` with ``ROW`` from 1 to ``rows``. ``line`` is the one-line
    form the receipts show: ``{r3.frequency[ROW]} (rows 1-9): {r3.frequency[1]} = 3803.3 cm⁻¹``. With ``section`` only
    the columns under that section name are listed (all of them if it matches none).
    """
    cols = _columns(items, block)
    if section is not None:
        want = set(section.split("."))
        part = [(k, es) for k, es in cols if want & set(k.split("/"))]
        cols = part or cols
    out = []
    for key, es in cols[:limit]:
        first = es[0]
        ref = ref_for(first, items)
        name = ref.split(".", 1)[1].split("[", 1)[0]
        example = _value_text(ref, items, style)
        unit = unit_shorthand(first.unit_name, style) if first.unit_name else None
        many = first.row is not None
        shown = f"'{example}'" if first.is_text else example
        if many:
            tag = ", ".join(("rows 1-" + str(len(es)),) + (("text",) if first.is_text else ()))
            line = f"{{{block}.{name}[ROW]}} ({tag}): {{{ref}}} = {shown}"
        else:
            line = f"{{{ref}}} = {shown}"
        out.append({"column": name, "rows": len(es) if many else None, "unit": unit, "use": "{" + ref + "}",
                    "example": example, "line": line})
    return out


def column_values(items, block, column, style=None, limit=60):
    """
    Every row of one column of ``block`` as ``[{"row", "use", "value"}]``, and the number of rows: ``(rows, total)``.
    ``column`` is a name as `column_summary` lists it (``bad_reference`` otherwise).
    """
    col = _column(items, block, column)
    rows = []
    for e in col[:limit]:
        ref = ref_for(e, items)
        row = {"use": "{" + ref + "}", "value": _value_text(ref, items, style)}
        if e.row is not None:
            row = {"row": e.row, **row}
        rows.append(row)
    return rows, len(col)


# ---- typed numbers ---------------------------------------------------------------------------------- #
def typed_numbers(text, skip=(), small_int_max=10, year_range=(1900, 2100)):
    """The numbers of ``text`` a reader would take as stated values: not in ``skip`` spans, not small integers or years."""
    year_range = (1, 0) if year_range is None else year_range
    return [t for t in extract_numbers(text) if not _skipped(t, skip) and not _is_exempt(t, small_int_max, year_range)]


def matching_items(tok, items, rel_tol=1e-3):
    """
    The data values of ``items`` the number ``tok`` could state: equal within half a unit of its last digit (or
    ``rel_tol`` of the value), a percentage of a fraction included, and compatible in unit and quantity. Numbers read
    from the section text are not data values and are not returned.
    """
    tol, x = 0.5 * 10.0 ** (-max(tok.decimals, 0)), abs(tok.value)
    out = []
    for e in items:
        if e.origin != "data" or e.is_text:
            continue
        same = _near(x, tol, e.value, rel_tol) or (
            tok.percent and not (e.percent or e.unit == "percent") and _near(x / 100, tol / 100, e.value, rel_tol))
        if same and _compatible(tok, e) is None:
            out.append(e)
    return out


def _written(text, tok):
    """The number with the unit typed after it, as written in ``text``."""
    end = tok.span[1]
    if tok.unit and not tok.percent:
        end = unit_after(text, end)[1]
    return text[tok.span[0]:end].strip()


# ---- notes ------------------------------------------------------------------------------------------ #
def advise(text, items, cites=(), skip=(), rel_tol=1e-3, small_int_max=10, year_range=(1900, 2100), limit=6):
    """
    Notes on the numbers ``text`` typed, from the data ``items`` (an `EvidenceSet`), as a list of sentences. A number that
    is a value of the data gets the placeholder that writes it (with its unit); a number that is not gets a pointer to the
    literal marker ``{=...}`` for a value that is meant to come from outside the data. Nothing is refused.
    """
    notes, more = [], 0
    has_data = any(e.origin == "data" for e in items)
    for tok in typed_numbers(text, skip, small_int_max, year_range):
        shown = _written(text, tok)
        hits = matching_items(tok, items, rel_tol)
        if hits:
            e = hits[0]
            other = f" (and {len(hits) - 1} other value{'s' if len(hits) > 2 else ''})" if len(hits) > 1 else ""
            note = (f"{shown} matches {e.describe()}{other}: write {{{ref_for(e, items)}}} and the server fills in the "
                    f"value and its unit from the data")
        elif has_data:
            where = f" of {', '.join(cites)}" if cites else ""
            note = (f"{shown} is not a value in the data{where}: if it comes from outside the data (a setup value, a "
                    f"literature value, something the user gave), write it as {{={shown}}} so the report records it as "
                    f"given; otherwise leave it out")
        else:
            continue
        if len(notes) < limit:
            notes.append(note)
        else:
            more += 1
    if more:
        notes.append(f"and {more} more typed number{'s' if more > 1 else ''}")
    return notes


# ---- autolink --------------------------------------------------------------------------------------- #
def autolink(text, items, small_int_max=10, year_range=(1900, 2100)):
    """
    Rewrite the typed numbers of ``text`` that are exactly one value of the data into the placeholder that writes it.

    "Exactly" is conservative: the number equals the value rounded to the digits typed (no relative tolerance, so
    "about 3800" is left alone), the unit typed after it is the data's, the sign agrees, it is not a percentage or a
    plain integer with no unit (those are counts as often as values), and the value is the only one in the data it
    could be. The result is the rewritten text and ``[{"typed", "use"}]``; the caller fills the placeholders in.
    """
    skip = [span for span, _, _ in find_markers(text)]
    edits = []
    for tok in typed_numbers(text, skip, small_int_max, year_range):
        if tok.percent or (not tok.unit and tok.decimals < 1):
            continue
        hits = matching_items(tok, items, rel_tol=0)
        if len(hits) != 1:
            continue
        e = hits[0]
        if e.quantity in _NOT_VALUES or (tok.value < 0) != (e.value < 0):
            continue
        end = tok.span[1]
        if tok.unit:
            canon, end = unit_after(text, end)
            if canon != e.unit:
                continue
        edits.append((tok.span[0], end, "{" + ref_for(e, items) + "}", text[tok.span[0]:end].strip()))
    for start, end, use, _ in reversed(edits):
        text = text[:start] + use + text[end:]
    return text, [{"typed": typed, "use": use} for _, _, use, typed in edits]


# ---- coverage --------------------------------------------------------------------------------------- #
def coverage(doc, rel_tol=1e-3, small_int_max=10, year_range=(1900, 2100), match=True):
    """
    How the numbers of the paragraphs of ``doc`` were written (captions are not counted): ``placeholders`` (filled in by
    the server), ``literals`` (given from outside the data, ``{=300 K}``), ``typed`` (typed by the model or a person) and,
    when ``match``, ``typed_in_data`` (typed numbers that are values of the data the paragraph cites, or of the report's
    readouts if it cites none: each could have been a placeholder). ``paragraphs_with_typed`` lists the paragraphs
    that have typed numbers; ``basis`` counts the paragraphs by their declared basis.
    """
    out = {"paragraphs": 0, "numbers": 0, "placeholders": 0, "literals": 0, "typed": 0}
    if match:
        out["typed_in_data"] = 0
    with_typed, basis, cache = [], {}, {}
    for b in doc.blocks:
        if not isinstance(b, Prose):
            continue
        out["paragraphs"] += 1
        if b.basis:
            basis[b.basis] = basis.get(b.basis, 0) + 1
        recs = b.fills or []
        lits = sum(1 for r in recs if r["expr"].startswith("="))
        out["literals"] += lits
        out["placeholders"] += len(recs) - lits
        toks = typed_numbers(b.text, fill_spans(b.text, recs), small_int_max, year_range)
        out["typed"] += len(toks)
        if toks:
            with_typed.append(b.id)
            if match:
                key = tuple(default_cites(doc, b.cites))
                if key not in cache:
                    cache[key] = doc.evidence(list(key))
                out["typed_in_data"] += sum(1 for t in toks if matching_items(t, cache[key], rel_tol))
    out["numbers"] = out["placeholders"] + out["literals"] + out["typed"]
    out["paragraphs_with_typed"] = with_typed
    if basis:
        out["basis"] = basis
    return out
