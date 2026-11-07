"""
Values the server fills in: a model (or a person) writes ``{r3.frequency[2]}`` in a paragraph instead of typing
``3803.3``, and the server writes the number *and its unit* as the readout labels it: ``3803.3 cm⁻¹``. Writing the
placeholder is the preferred way to state a value, because a value that is filled in cannot be mistyped, misread
or given in the wrong unit.

A reference is ``BLOCK.NAME`` or ``BLOCK.NAME[ROW]``: ``BLOCK`` a readout block id, ``NAME`` a column or field of its
data (the last part of its flat-data key, its label in lower case with ``_`` for spaces, or a dotted tail such as
``bonds.value`` when the last part is ambiguous), ``ROW`` a 1-based row as in the tables `peek` shows. A reference
without a row is the whole column (only useful inside a function when derived values are on). Text columns work the
same way: ``{r3.mode[2]}`` writes the label in that row.

Units. The unit is the shorthand label of the data's unit (`unit_shorthand`: the readout theme's label for the
`UnitsData` unit name, ``Wavenumbers`` -> ``cm⁻¹``). A unit typed after the closing brace (``{r3.frequency[2]} cm-1``)
is swallowed and replaced by that canonical label; a unit that is not the data's (``{r3.frequency[2]} eV``), or one
typed after a value that has none, is an error (``unit_mismatch``). A trailing format spec
(``{r3.frequency[2]:.0f}``) changes the number's format. By default a single value is written with the decimals the
data's text shows.

Derived values (``{mean(r3.frequency[2], r3.frequency[3])}``: ``+ - * /`` and `FUNCTIONS`) are off unless the caller
opts in (``allow_derived=True``; ``--derived`` on the server): a sum/difference/mean is written with the most
decimals of its inputs and the inputs' unit, a product or ratio with four significant digits and no unit.

`fill_text` returns the text with the values written in and a `Fill` per value (its expression, the text written,
whether it was derived and the evidence it used). Filled values are exact by construction, so the number check skips
them (`check_grounding(skip=...)`), and `refill` recomputes them later (a stored report records its fills, so a
checker can confirm a value still follows from the data).
"""

import ast
import math
import re

from .Document import ReportOperationError
from .Grounding import unit_after, unit_shorthand

__all__ = ["Fill", "FUNCTIONS", "find_references", "fill_text", "refill", "column_names", "ref_for"]

_REF = re.compile(r"\b(?P<block>[a-z]\d+)\.(?P<name>[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)"
                  r"(?:\[(?P<row>\d+)\])?")
_BRACE = re.compile(r"\{([^{}\n]{1,300})\}")


def _mean(*xs):
    xs = _flat(xs)
    return sum(xs) / len(xs)


def _flat(xs):
    out = []
    for x in xs:
        out.extend(x if isinstance(x, list) else [x])
    if not out:
        raise ValueError("no values")
    return out


FUNCTIONS = {
    "mean": _mean,
    "sum": lambda *xs: sum(_flat(xs)),
    "min": lambda *xs: min(_flat(xs)),
    "max": lambda *xs: max(_flat(xs)),
    "abs": lambda x: abs(x),
    "diff": lambda a, b: a - b,
    "ratio": lambda a, b: a / b,
}
_ADDITIVE = {"mean", "sum", "min", "max", "abs", "diff"}


class Fill:
    """
    One value written by the server.

    :ivar expr: the expression as written (without the braces and format spec)
    :ivar spec: the format spec, or ``None``
    :ivar text: what was written into the text: the number and its unit label (``3803.3 cm⁻¹``), or a text value
    :ivar number: the number or text part of ``text`` (``3803.3``)
    :ivar unit: the unit label written after the number (``cm⁻¹``), or ``None``
    :ivar value: its value (a string for a text column)
    :ivar derived: ``True`` unless the expression is a single reference
    :ivar inputs: the `EvidenceItem`s it used
    :ivar span: ``(start, end)`` of ``text`` in the filled text
    :ivar style: the unit label style it was written in (``None``: `UnitsData`'s default), stored by `record`
    """

    def __init__(self, expr, spec, text, value, derived, inputs, span, number=None, unit=None, kind="single", style=None):
        self.expr, self.spec, self.text, self.value = expr, spec, text, value
        self.derived, self.inputs, self.span = derived, list(inputs), span
        self.number, self.unit, self.kind = text if number is None else number, unit, kind
        self.style = style

    def to_dict(self):
        """What the tools report: ``{expr, value, derived, inputs}``."""
        return {"expr": self.expr, "value": self.text, "derived": self.derived,
                "inputs": [e.describe() for e in self.inputs]}

    def record(self):
        """What a report stores with its paragraph: ``{"expr": ..., "text": ...}`` (plus ``spec`` if given)."""
        out = {"expr": self.expr, "text": self.text}
        if self.spec:
            out["spec"] = self.spec
        if self.style and self.unit:       # only a value with a unit label depends on the style
            out["style"] = self.style
        return out


def find_references(text):
    """The ``{...}`` groups of ``text`` that contain at least one block reference: ``[(span, inner)]``."""
    return [(m.span(), m.group(1)) for m in _BRACE.finditer(text) if _REF.search(m.group(1))]


def column_names(items, block):
    """The names a reference can use for the data of ``block`` (shortest unambiguous form of each column)."""
    keys = list(dict.fromkeys(e.key for e in items if e.block == block and e.origin == "data" and e.key))
    out = []
    for k in keys:
        parts = k.split("/")
        for n in range(1, len(parts) + 1):
            tail = parts[-n:]
            if sum(1 for o in keys if o.split("/")[-n:] == tail) == 1:
                out.append(".".join(tail))
                break
    return out


def ref_for(item, items):
    """The reference that names ``item`` (``r3.frequency[2]``)."""
    parts = item.key.split("/")
    keys = {e.key for e in items if e.block == item.block and e.origin == "data" and e.key}
    for n in range(1, len(parts) + 1):
        if sum(1 for o in keys if o.split("/")[-n:] == parts[-n:]) == 1:
            name = ".".join(parts[-n:])
            break
    else:
        name = ".".join(parts)
    return f"{item.block}.{name}" + (f"[{item.row}]" if item.row is not None else "")


def _norm(s):
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_")


def _column(items, block, name):
    """The data items of ``block``'s column ``name`` (see the module docs for the names accepted)."""
    data = [e for e in items if e.block == block and e.origin == "data" and e.key]
    if not data:
        raise ReportOperationError("bad_reference", f"{block!r} is not a cited readout block with data; cite it or "
                                   f"use a readout block id from outline", block_id=block)
    want = name.split(".")
    keys = list(dict.fromkeys(e.key for e in data))
    hits = [k for k in keys if k.split("/")[-len(want):] == want]
    if not hits and len(want) == 1:
        hits = list(dict.fromkeys(e.key for e in data if _norm(e.label) == _norm(name)))
    if len(hits) != 1:
        choices = column_names(items, block)
        what = "is ambiguous" if hits else "is not a column of"
        raise ReportOperationError("bad_reference", f"{name!r} {what} block {block!r}; its columns are {choices}",
                                   block_id=block, choices=choices)
    return [e for e in data if e.key == hits[0]]


def _resolve(items, block, name, row):
    col = _column(items, block, name)
    if row is None:
        return col if len(col) > 1 else col[0]
    row = int(row)
    for e in col:
        if (e.row or 1) == row:
            return e
    raise ReportOperationError("bad_reference", f"{block}.{name} has rows 1 to {len(col)}, not {row}",
                               block_id=block, rows=len(col))


class _Eval(ast.NodeVisitor):
    def __init__(self, env):
        self.env, self.kind = env, "single"

    def generic_visit(self, node):
        raise ValueError(f"{type(node).__name__} is not allowed")

    def visit_Expression(self, node):
        if not isinstance(node.body, ast.Name):
            self.kind = "additive"
        return self.visit(node.body)

    def visit_Name(self, node):
        if node.id not in self.env:
            raise ValueError(f"unknown name {node.id!r}")
        return self.env[node.id]

    def visit_Constant(self, node):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise ValueError("only numbers are allowed")
        return node.value

    def visit_UnaryOp(self, node):
        v = self.visit(node.operand)
        if isinstance(node.op, ast.USub):
            return -v
        if isinstance(node.op, ast.UAdd):
            return v
        raise ValueError("only + and - signs are allowed")

    def visit_BinOp(self, node):
        a, b = self.visit(node.left), self.visit(node.right)
        if isinstance(a, list) or isinstance(b, list):
            raise ValueError("a whole column can only be passed to mean, sum, min or max")
        if isinstance(node.op, ast.Add):
            return a + b
        if isinstance(node.op, ast.Sub):
            return a - b
        if isinstance(node.op, (ast.Mult, ast.Div)):
            self.kind = "multiplicative"
            return a * b if isinstance(node.op, ast.Mult) else a / b
        raise ValueError("only + - * / are allowed")

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name) or node.func.id not in FUNCTIONS or node.keywords:
            raise ValueError(f"the functions are {sorted(FUNCTIONS)}")
        if node.func.id == "ratio":
            self.kind = "multiplicative"
        args = [self.visit(a) for a in node.args]
        if node.func.id in ("abs", "diff", "ratio") and any(isinstance(a, list) for a in args):
            raise ValueError(f"{node.func.id} takes single values, not a whole column")
        return FUNCTIONS[node.func.id](*args)


def _split_spec(inner):
    depth = 0
    for i in range(len(inner) - 1, -1, -1):
        c = inner[i]
        if c in ")]":
            depth += 1
        elif c in "([":
            depth -= 1
        elif c == ":" and depth == 0:
            return inner[:i].strip(), inner[i + 1:].strip()
    return inner.strip(), None


def _shown_decimals(item, items):
    """The decimals the section text shows for ``item``'s value (most precise matching text number), else ``None``."""
    best = None
    for e in items:
        if e.origin == "text" and e.block == item.block and e.decimals is not None:
            if abs(abs(e.value) - abs(item.value)) <= 0.5 * 10.0 ** -e.decimals * (1 + 1e-9):
                best = e.decimals if best is None else max(best, e.decimals)
    return best


def _format(value, spec, kind, inputs, items):
    if kind == "text":
        if spec:
            raise ReportOperationError("bad_reference", f"a text value takes no format spec (got {spec!r})")
        return value
    if spec:
        try:
            return format(value, spec)
        except (ValueError, TypeError) as e:
            raise ReportOperationError("bad_reference", f"bad format spec {spec!r}: {e}")
    if kind == "multiplicative":
        return f"{value:.4g}"
    decs = [d for d in (_shown_decimals(e, items) for e in inputs) if d is not None]
    if decs:
        return f"{value:.{max(decs)}f}"
    return f"{value:.6g}"


def _unit_label(inputs, kind, expr, style=None):
    """The shorthand label written after the value, or ``None`` (text values, products and ratios, unitless data)."""
    if kind in ("text", "multiplicative"):
        return None
    labels = list(dict.fromkeys(unit_shorthand(e.unit_name, style) for e in inputs if e.unit_name))
    if len(labels) > 1:
        raise ReportOperationError("unit_mismatch", f"{{{expr}}} combines values in different units "
                                   f"({', '.join(labels)})", expr=expr)
    return labels[0] if labels else None


_NO_SPACE = ("%", "°", r"^{\circ}", r"\%")


def _join(number, label, style=None):
    """The number and its unit label as written: ``3803.3 cm⁻¹``, ``90.0°``, or in LaTeX ``$3803.3\\,\\mathrm{cm^{-1}}$``"""
    if not label:
        return number
    if style == "latex":
        return "$" + number + ("" if label in _NO_SPACE else r"\,") + label + "$"
    return number + ("" if label in _NO_SPACE else " ") + label


def example_value(style=None, number="3803.3", unit="Wavenumbers"):
    """A value as the server writes it in ``style``, for the examples in the instructions: ``3803.3 cm⁻¹``."""
    from ...Data import UnitsData
    style = style or UnitsData.label_style
    return _join(number, unit_shorthand(unit, style), style)


def _evaluate(inner, items, allow_derived):
    expr, spec = _split_spec(inner)
    env, used, refs = {}, [], {}

    def sub(m):
        key = m.group(0)
        if key not in refs:
            val = _resolve(items, m.group("block"), m.group("name"), m.group("row"))
            name = f"_v{len(refs)}"
            refs[key] = name
            vals = val if isinstance(val, list) else [val]
            used.extend(vals)
            if any(e.is_text for e in vals):
                env[name] = [e.text for e in vals] if isinstance(val, list) else val.text
            else:
                env[name] = [e.value for e in vals] if isinstance(val, list) else val.value
        return refs[key]

    py = _REF.sub(sub, expr)
    if any(e.is_text for e in used):
        if isinstance(env.get("_v0"), list):
            raise ReportOperationError("bad_reference", f"{{{inner}}} is a whole column; give a row, like "
                                       f"{expr}[1]", expr=inner)
        if len(refs) != 1 or py.strip() != "_v0":
            raise ReportOperationError("bad_reference", f"{{{inner}}}: a text value can only be filled in on its own "
                                       f"({{r3.mode[2]}}), not combined with other values", expr=inner)
        return expr, spec, env["_v0"], False, used, "text"
    try:
        tree = ast.parse(py, mode="eval")
        ev = _Eval(env)
        value = ev.visit(tree)
    except ReportOperationError:
        raise
    except (ValueError, SyntaxError, TypeError, ZeroDivisionError) as e:
        raise ReportOperationError("bad_reference", f"can't compute {{{inner}}}: {e}. Write a block reference like "
                                   f"r3.frequency[2]", expr=inner)
    if isinstance(value, list):
        raise ReportOperationError("bad_reference", f"{{{inner}}} is a whole column; give a row, like "
                                   f"{expr}[1]", expr=inner)
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ReportOperationError("bad_reference", f"{{{inner}}} is not a finite number", expr=inner)
    derived = ev.kind != "single"
    if derived and not allow_derived:
        raise ReportOperationError("derived_disabled", f"{{{inner}}} computes a value, and this report only accepts "
                                   f"values as the data shows them (a single reference like {{r3.frequency[2]}})",
                                   expr=inner)
    return expr, spec, float(value), derived, used, ev.kind


def _render(inner, items, allow_derived, style=None):
    """``(expr, spec, value, derived, used, kind, number, label, written)`` for the contents of one brace group."""
    expr, spec, value, derived, used, kind = _evaluate(inner, items, allow_derived)
    number = _format(value, spec, kind, used, items)
    label = _unit_label(used, kind, expr, style)
    return expr, spec, value, derived, used, kind, number, label, _join(number, label, style)


def fill_text(text, items, allow_derived=False, style=None):
    """
    Write the values of the ``{...}`` references of ``text`` into it, each with its unit label (``3803.3 cm⁻¹``).

    A unit typed right after a reference is swallowed (the label replaces it); a different unit than the data's is an
    error. Derived expressions need ``allow_derived=True``. ``style`` is the unit label style (``"unicode"``,
    ``"ascii"`` or ``"latex"``; default `UnitsData.label_style`); LaTeX values are wrapped in ``$...$``.

    :param items: the `EvidenceSet` of the blocks the text may refer to (`ReportDocument.evidence`)
    :return: ``(filled text, [Fill])``; text without references comes back unchanged with ``[]``
    :raises ReportOperationError: ``bad_reference`` (unknown block, column or row, or a bad expression),
        ``unit_mismatch`` or ``derived_disabled``
    """
    refs = find_references(text)
    if not refs:
        return text, []
    out, fills, pos, length = [], [], 0, 0
    for (s, e), inner in refs:
        if s < pos:
            continue
        expr, spec, value, derived, used, kind, number, label, written = _render(inner, items, allow_derived, style)
        end = e
        pct = unit_shorthand("Percent", style)
        if label:
            typed, uend = unit_after(text, e)
            if typed is None and label == pct and text[e:e + 1] == "%":
                end = e + 1
            elif typed is not None:
                known = {x.unit for x in used if x.unit_name and x.unit}
                if (typed not in known) if known else (unit_shorthand(typed, style) != label):
                    raise ReportOperationError(
                        "unit_mismatch", f"{{{expr}}} is in {label}, but the text writes {text[e:uend].strip()} after "
                        f"it. Write the placeholder alone, {{{expr}}}: the server adds the unit.", expr=expr)
                end = uend
            elif label != pct and text[e:e + 1] == "%":
                raise ReportOperationError("unit_mismatch", f"{{{expr}}} is in {label}, but the text writes % after "
                                           f"it. Write the placeholder alone, {{{expr}}}.", expr=expr)
        elif kind not in ("text", "multiplicative"):
            typed, uend = unit_after(text, e)
            if typed is not None:
                raise ReportOperationError("unit_mismatch", f"{{{expr}}} has no unit in the data, but the text writes "
                                           f"{text[e:uend].strip()} after it. Leave the unit out.", expr=expr)
        out.append(text[pos:s])
        length += s - pos
        f = Fill(expr, spec, written, value, derived, used, (length, length + len(written)), number=number,
                 unit=label, kind=kind, style=style)
        out.append(written)
        length += len(written)
        fills.append(f)
        pos = end
    out.append(text[pos:])
    return "".join(out), fills


def refill(text, records, items, style=None):
    """
    Recompute stored fills (`Fill.record`) against ``items``: ``(spans, problems)`` where ``spans`` locate each
    recorded value in ``text`` (to skip in the number check) and ``problems`` lists the values that no longer follow
    from the data or are missing from the text.
    """
    spans, problems, pos = [], [], 0
    for r in records or ():
        try:
            written = _render(r["expr"] + (":" + r["spec"] if r.get("spec") else ""), items, True, r.get("style") or style)[-1]
        except ReportOperationError as e:
            problems.append(f"{{{r['expr']}}}: {e.detail}")
            continue
        if written != r["text"]:
            problems.append(f"{{{r['expr']}}} was written as {r['text']} but the data now gives {written}")
        i = text.find(r["text"], pos)
        if i < 0:
            problems.append(f"{{{r['expr']}}} = {r['text']} is no longer in the text")
            continue
        spans.append((i, i + len(r["text"])))
        pos = i + len(r["text"])
    return spans, problems
