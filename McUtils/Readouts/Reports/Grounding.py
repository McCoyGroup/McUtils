"""
The grounding check: every number in model-written prose must appear in the evidence the model was shown.

`extract_numbers` finds the numbers a sentence states (leaving out the digits in ``H2O``, ``cm-1``, ``C2v`` or inline
code), `evidence_numbers` collects the numbers of texts and readout data, and `check_grounding` matches the first
against the second. A prose number matches an evidence value ``e`` if it equals ``e`` rounded to the precision the
prose uses (or is within a relative tolerance); derived quantities (differences, ratios) are not matched.
"""

import enum
import re

import numpy as np

__all__ = ["NumberToken", "extract_numbers", "evidence_numbers", "GroundingResult", "check_grounding", "WritingPolicy"]


class WritingPolicy(enum.Enum):
    """What the model may write and what is checked (see the design, §5.1)."""
    GROUNDED = "grounded"
    STRUCTURE_ONLY = "structure_only"
    UNCHECKED = "unchecked"

    @classmethod
    def coerce(cls, value):
        return value if isinstance(value, cls) else cls(value)


class NumberToken:
    """A number stated in text: its ``text``, ``value``, the ``decimals`` it was written with, ``span`` and ``percent``."""

    def __init__(self, text, value, decimals, span, percent=False):
        self.text, self.value, self.decimals, self.span, self.percent = text, value, decimals, span, percent

    def __repr__(self):
        return f"NumberToken({self.text!r}, {self.value:g})"


_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")
_MINUS = "-−–—"      # hyphen, minus sign, en and em dash (the last two only as ranges)
_NUM = r"\d+(?:\.\d+)?"
_PATTERNS = [
    # 1.5 x 10^3, 1.5×10^-3, 2×10⁻³
    ("times10", re.compile(r"(?P<m>\d+(?:\.\d+)?)\s*[×xX]\s*10\s*\^?\s*(?P<e>[-−+]?\d+|[⁻⁺]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)")),
    # 1.2e-3
    ("sci", re.compile(r"(?P<m>\d+(?:\.\d+)?)[eE](?P<e>[-−+]?\d+)")),
    # 1,234.5
    ("thousands", re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?")),
    ("plain", re.compile(_NUM)),
]
_CODE = re.compile(r"`[^`\n]*`")


def _blank_code(text):
    return _CODE.sub(lambda m: " " * len(m.group(0)), text)


def _decimals(mantissa):
    return len(mantissa.split(".", 1)[1]) if "." in mantissa else 0


def extract_numbers(text):
    """
    The numbers ``text`` states, as `NumberToken`s in order. Ranges ``a–b`` give both ends; ``−`` is read as a minus;
    a hyphen before a digit that follows a digit is a range, not a sign. Digits glued to a preceding letter
    (``H2O``, ``cm-1``, ``C2v``, ``r1``) and anything in inline code are skipped.
    """
    clean = _blank_code(text)
    taken = [False] * len(clean)
    found = []
    for kind, rx in _PATTERNS:
        for m in rx.finditer(clean):
            s, e = m.span()
            if any(taken[s:e]):
                continue
            if kind == "plain" and s > 0 and clean[s - 1] == ".":
                continue        # the tail of something like "v1.2.3"; the head was taken or isn't a number
            for i in range(s, e):
                taken[i] = True
            found.append((kind, m))
    tokens = []
    for kind, m in sorted(found, key=lambda km: km[1].start()):
        s, e = m.span()
        prev = clean[s - 1] if s > 0 else ""
        sign, start = 1, s
        if prev and prev in _MINUS + "+":
            before = clean[s - 2] if s > 1 else ""
            if before.isalpha() or before == "_":
                continue                                   # "cm-1", "r-2": glued to a word
            if before.isdigit() or before in ")%" :
                pass                                       # a range "a-b" (or "5%-10%"): positive
            elif prev in "-−":
                sign, start = -1, s - 1
            elif prev == "+":
                start = s - 1
        elif prev.isalpha() or prev == "_":
            continue                                       # "H2O", "C2v", "r1"
        end = e
        percent = clean[e:e + 1] == "%"
        if percent:
            end += 1
        raw = clean[start:end]
        if kind == "times10":
            mant, exp = m.group("m"), int(m.group("e").translate(_SUP).replace("−", "-"))
            value, dec = float(mant) * 10.0 ** exp, max(_decimals(mant) - exp, 0)
        elif kind == "sci":
            mant, exp = m.group("m"), int(m.group("e").replace("−", "-"))
            value, dec = float(mant) * 10.0 ** exp, max(_decimals(mant) - exp, 0)
        elif kind == "thousands":
            body = m.group(0).replace(",", "")
            value, dec = float(body), _decimals(body)
        else:
            value, dec = float(m.group(0)), _decimals(m.group(0))
        tokens.append(NumberToken(raw, sign * value, dec, (start, end), percent))
    return tokens


def _scalars(value, out, cap):
    arr = value
    if isinstance(arr, (bool, np.bool_)):
        return
    try:
        arr = np.asarray(arr)
    except Exception:
        return
    if arr.dtype.kind in "iuf":
        flat = np.asarray(arr, dtype=float).ravel()
        flat = flat[np.isfinite(flat)]
        out.append(flat[:max(cap - sum(len(o) for o in out), 0)])
    elif arr.dtype == object:
        for v in arr.ravel()[:cap]:
            _scalars(v, out, cap)


def evidence_numbers(texts=(), readouts=(), cap=20000):
    """
    A float array of the numbers in ``texts`` (as `extract_numbers` reads them) and every scalar/array value in the
    flat data of each readout (``readout.to_flat_data()[0]``), up to ``cap`` values.
    """
    if isinstance(texts, str):
        texts = (texts,)
    chunks = []
    for t in texts:
        vals = [n.value for n in extract_numbers(t)]
        if vals:
            chunks.append(np.array(vals, dtype=float))
    for ro in readouts:
        data = ro.to_flat_data()[0]
        for v in data.values():
            _scalars(v, chunks, cap)
    arr = np.concatenate(chunks) if chunks else np.zeros(0)
    return arr[:cap]


class GroundingResult:
    """``ok`` if every checked number matched; ``unmatched`` are the `NumberToken`s that didn't; ``checked`` counts the non-exempt ones."""

    def __init__(self, ok, unmatched, checked):
        self.ok, self.unmatched, self.checked = ok, list(unmatched), checked

    def errors(self):
        """Messages for a revision prompt, one per unmatched number."""
        return [f"the number {t.text!r} does not appear in the evidence; state only values that are shown there "
                f"(do not compute new ones)" for t in self.unmatched]

    def __repr__(self):
        return f"GroundingResult(ok={self.ok}, unmatched={self.unmatched}, checked={self.checked})"


def _is_exempt(tok, small_int_max, year_range):
    is_int = tok.decimals == 0 and "." not in tok.text and "e" not in tok.text.lower() and "×" not in tok.text
    if not is_int:
        return False
    if not tok.percent and abs(tok.value) <= small_int_max:
        return True
    digits = tok.text.lstrip("+-−")
    if not tok.percent and len(digits) == 4 and year_range[0] <= tok.value <= year_range[1]:
        return True
    return False


def check_grounding(text, evidence, rel_tol=1e-3, small_int_max=10, year_range=(1900, 2100)):
    """
    Match the numbers of ``text`` against ``evidence`` (an array from `evidence_numbers`, or any iterable of floats).

    A number ``x`` written with ``d`` decimals matches an evidence value ``e`` if ``|x - e| <= 0.5 * 10**-d`` or
    ``|x - e| <= rel_tol * |e|``; a percentage also tries ``x / 100``; the comparison is on absolute values, because
    prose often says "a shift of 12.3" for −12.3. Integers up to ``small_int_max`` and four-digit years in
    ``year_range`` are exempt.
    """
    ev = np.asarray(evidence, dtype=float).ravel()
    unmatched, checked = [], 0
    aev = np.abs(ev)
    for tok in extract_numbers(text):
        if _is_exempt(tok, small_int_max, year_range):
            continue
        checked += 1
        tol = 0.5 * 10.0 ** (-max(tok.decimals, 0))
        cands = [(abs(tok.value), tol)]
        if tok.percent:
            cands.append((abs(tok.value) / 100.0, tol / 100.0))
        ok = False
        if ev.size:
            for x, t in cands:
                diff = np.abs(aev - x)
                if np.any((diff <= t * (1 + 1e-9)) | (diff <= rel_tol * aev)):
                    ok = True
                    break
        if not ok:
            unmatched.append(tok)
    return GroundingResult(not unmatched, unmatched, checked)
