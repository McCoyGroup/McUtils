"""
The grounding check: every number in model-written prose must appear in the evidence the model was shown.

`extract_numbers` finds the numbers a sentence states (leaving out the digits in ``H2O``, ``cm-1``, ``C2v`` or inline
code), `evidence_numbers` collects the numbers of texts and readout data, and `check_grounding` matches the first
against the second. A prose number matches an evidence value ``e`` if it equals ``e`` rounded to the precision the
prose uses (or is within a relative tolerance); derived quantities (differences, ratios) are not matched.

With `evidence_items` (instead of the plain array of `evidence_numbers`) every evidence value keeps where it came from
(block, label, row), its unit and its quantity, and the match respects them: a number written with a unit only matches
a value in that unit, a percentage only matches a percentage or a plain fraction (never an index, a count or an
intensity), and an integer with a unit is not exempt as a "small integer". `GroundingResult.matches` then says which
value each number matched, and `GroundingResult.reasons` why a number that equals some value was still refused.
"""

import enum
import re

import numpy as np

__all__ = ["NumberToken", "extract_numbers", "evidence_numbers", "EvidenceItem", "EvidenceSet", "evidence_items",
           "canonical_unit", "unit_shorthand", "unit_after", "GroundingResult", "check_grounding", "WritingPolicy"]


class WritingPolicy(enum.Enum):
    """What the model may write and what is checked (see the design, §5.1)."""
    GROUNDED = "grounded"
    STRUCTURE_ONLY = "structure_only"
    UNCHECKED = "unchecked"

    @classmethod
    def coerce(cls, value):
        return value if isinstance(value, cls) else cls(value)


class NumberToken:
    """
    A number stated in text: its ``text``, ``value``, the ``decimals`` it was written with, ``span``, ``percent`` and
    ``unit`` (the canonical unit written right after it, see `canonical_unit`, or ``None``).
    """

    def __init__(self, text, value, decimals, span, percent=False, unit=None):
        self.text, self.value, self.decimals, self.span, self.percent = text, value, decimals, span, percent
        self.unit = "percent" if percent else unit

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

# canonical unit <- the spellings a readout's metadata or a sentence uses (compared lower-case, without spaces)
_UNIT_NAMES = {
    "cm-1": ("wavenumbers", "wavenumber", "cm-1", "cm^-1", "cm⁻¹", "cm−1", "1/cm", "/cm", "cm**-1"),
    "hz": ("hertz", "hz"), "ghz": ("gigahertz", "ghz"), "thz": ("terahertz", "thz"), "mhz": ("megahertz", "mhz"),
    "hartree": ("hartrees", "hartree", "eh", "eₕ", "ha", "e_h"),
    "ev": ("electronvolts", "electronvolt", "ev"), "mev": ("millielectronvolts", "mev"),
    "kcal/mol": ("kilocaloriespermole", "kcal/mol", "kcalmol-1", "kcal·mol-1", "kcal·mol⁻¹"),
    "kj/mol": ("kilojoulespermole", "kj/mol", "kjmol-1", "kj·mol-1", "kj·mol⁻¹"),
    "amu": ("atomicmassunits", "atomicmassunit", "amu", "da", "dalton", "daltons", "g/mol"),
    "angstrom": ("angstroms", "angstrom", "å", "ångström", "ångströms", "ang"),
    "bohr": ("bohrradius", "bohrs", "bohr", "a0", "a₀"), "pm": ("picometers", "pm"), "nm": ("nanometers", "nm"),
    "degree": ("degrees", "degree", "deg", "°"), "radian": ("radians", "radian", "rad"),
    "km/mol": ("kilometerspermole", "km/mol", "kmmol-1", "km·mol-1", "km·mol⁻¹"),
    "kelvin": ("kelvin", "k"), "debye": ("debye", "debyes", "d"),
    "percent": ("percent", "%"),
}
_UNIT_LOOKUP = {alias: canon for canon, names in _UNIT_NAMES.items() for alias in names}
# what can follow a number in prose (longest first); "k" and "d" are only units in metadata, not after a number
_TEXT_UNIT = re.compile(
    r"\s?(?P<u>cm\s?(?:[-−]\s?1|⁻¹|\^\s?-\s?1)|/cm|wavenumbers?|kcal(?:\s?/\s?|\s?·\s?)mol(?:[-−⁻]\s?¹?1?)?|"
    r"kJ(?:\s?/\s?|\s?·\s?)mol(?:[-−⁻]\s?¹?1?)?|km(?:\s?/\s?|\s?·\s?)mol(?:[-−⁻]\s?¹?1?)?|"
    r"hartrees?|E[hₕ]|Ha|Ang|meV|eV|THz|GHz|MHz|Hz|amu|Da|g/mol|Å|ångströms?|angstroms?|bohrs?|a[0₀]|pm|nm|"
    r"degrees?|deg|°|radians?|rad|Debye|K)(?![A-Za-z0-9])")


def canonical_unit(name):
    """The canonical spelling of a unit (``"Wavenumbers"``, ``"cm⁻¹"`` -> ``"cm-1"``), or ``None`` if it is not known."""
    if not name:
        return None
    key = re.sub(r"\s+", "", str(name)).lower().replace("−", "-")
    if key in _UNIT_LOOKUP:
        return _UNIT_LOOKUP[key]
    m = _TEXT_UNIT.fullmatch(" " + str(name).strip())
    return _UNIT_LOOKUP.get(re.sub(r"\s+", "", m.group("u")).lower().replace("−", "-")) if m else None


def _unit_after(text, end):
    m = _TEXT_UNIT.match(text, end)
    if not m:
        return None
    u = re.sub(r"\s+", "", m.group("u")).replace("−", "-")
    if u.lower().startswith("cm") or u == "/cm" or u.lower().startswith("wavenumber"):
        return "cm-1"
    if u in ("K",):
        return "kelvin"
    for canon, pat in (("kcal/mol", "kcal"), ("kj/mol", "kj"), ("km/mol", "km")):
        if u.lower().startswith(pat):
            return canon
    return _UNIT_LOOKUP.get(u.lower(), _UNIT_LOOKUP.get(u))


def unit_after(text, end):
    """
    The unit written right after position ``end`` of ``text``: ``(canonical unit, end of the unit text)``, or
    ``(None, end)`` if no unit follows. The unit text includes the space before it.
    """
    m = _TEXT_UNIT.match(text, end)
    if not m:
        return None, end
    return _unit_after(text, end), m.end()


# canonical spelling of a unit (`canonical_unit`) -> the `UnitsData` unit name whose label is written for it
_CANONICAL_NAMES = {
    "cm-1": "Wavenumbers", "hz": "Hertz", "ghz": "GigaHertz", "thz": "TeraHertz", "mhz": "MegaHertz",
    "hartree": "Hartrees", "ev": "ElectronVolts", "mev": "MilliElectronVolts", "kcal/mol": "KilocaloriesPerMole",
    "kj/mol": "KilojoulesPerMole", "km/mol": "KilometersPerMole", "amu": "AtomicMassUnits", "angstrom": "Angstroms",
    "bohr": "BohrRadius", "pm": "Picometers", "nm": "Nanometers", "degree": "Degrees", "radian": "Radians",
    "kelvin": "Kelvins", "debye": "Debyes", "percent": "Percent",
}


def unit_shorthand(name, style=None):
    """
    The short label the report writes for a unit: `UnitsData.unit_label` for the `UnitsData` unit name
    (``"Wavenumbers"`` -> ``"cm⁻¹"``, ``"KilocaloriesPerMole"`` -> ``"kcal/mol"``) in ``style`` (``"unicode"``,
    ``"ascii"``, ``"latex"``; default `UnitsData.label_style`), also for other spellings of the same unit (``"cm^-1"``,
    ``"Hartree"``). A unit with no label is written as it is named; ``None`` for no unit.
    """
    from ...Data import UnitsData
    if not name:
        return None
    label = UnitsData.unit_label(name, style)
    if label != name:
        return label
    unit_name = _CANONICAL_NAMES.get(canonical_unit(name))
    return UnitsData.unit_label(unit_name, style) if unit_name else name


def _blank_code(text):
    return _CODE.sub(lambda m: " " * len(m.group(0)), text)


def _decimals(mantissa):
    return len(mantissa.split(".", 1)[1]) if "." in mantissa else 0


def extract_numbers(text):
    """
    The numbers ``text`` states, as `NumberToken`s in order. Ranges ``a–b`` give both ends; ``−`` is read as a minus;
    a hyphen before a digit that follows a digit is a range, not a sign. Digits glued to a preceding letter
    (``H2O``, ``cm-1``, ``C2v``, ``r1``), digits glued to a following word that is not a unit (``6-31G``, ``6-311++G``,
    ``3D``) and anything in inline code are skipped.
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
            if before.isdigit() or (before and before in ")%"):
                pass                                       # a range "a-b" (or "5%-10%"): positive
            elif prev in "-−":
                sign, start = -1, s - 1
            elif prev == "+":
                start = s - 1
        elif prev.isalpha() or prev == "_":
            continue                                       # "H2O", "C2v", "r1"
        if re.match(r"\+*[A-Za-z]", clean[e:e + 3]) and _unit_after(clean, e) is None:
            continue                                       # "6-31G", "6-311++G", "3D": part of a name
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
        tokens.append(NumberToken(raw, sign * value, dec, (start, end), percent,
                                  unit=None if percent else _unit_after(clean, end)))
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


class EvidenceItem:
    """
    One evidence value and where it came from.

    :ivar value: the number
    :ivar unit: canonical unit (`canonical_unit`) or ``None``
    :ivar quantity: the readout's ``quantity`` metadata (``frequency``, ``index``, ``int``, ...) or ``None``
    :ivar label: the column/field label (``Frequency``), or ``"text"`` for a number read from a section's text
    :ivar block: the id of the block it belongs to (``r3``), if known
    :ivar row: 1-based row of an array value (``None`` for a scalar)
    :ivar origin: ``"data"`` (the readout's flat data) or ``"text"`` (the section text `peek` shows)
    :ivar percent: the text wrote it as a percentage
    :ivar key: the flat-data key (``molecule/normal_modes/frequencies/frequency``), for data values
    :ivar decimals: the decimals a number read from text was written with
    :ivar text: the string of a text value (a label column such as ``mode``); ``None`` for numbers, whose ``value``
        is ``nan`` when ``text`` is set
    :ivar unit_name: the unit as the readout names it (``"Wavenumbers"``), for writing its shorthand
    """
    __slots__ = ("value", "unit", "quantity", "label", "block", "row", "origin", "percent", "key", "decimals", "text",
                 "unit_name")

    def __init__(self, value, unit=None, quantity=None, label=None, block=None, row=None, origin="data",
                 percent=False, key=None, decimals=None, text=None, unit_name=None):
        self.value, self.unit, self.quantity, self.label = float(value), unit, quantity, label
        self.block, self.row, self.origin, self.percent, self.key = block, row, origin, percent, key
        self.decimals, self.text, self.unit_name = decimals, text, unit_name

    @property
    def is_text(self):
        """Whether this is a string value rather than a number."""
        return self.text is not None

    def describe(self):
        """``r3 Frequency row 2 = 3803.29958 cm-1`` (``r3 Mode row 2 = 'bend'`` for a text value)"""
        where = " ".join(x for x in (self.block, self.label) if x)
        if self.row is not None:
            where += f" row {self.row}"
        if self.text is not None:
            return f"{where} = {self.text!r}".strip()
        unit = "%" if self.percent else (f" {self.unit}" if self.unit else "")
        return f"{where} = {self.value:.10g}{unit}".strip()

    def to_dict(self):
        return {k: getattr(self, k) for k in self.__slots__ if getattr(self, k) not in (None, False)}

    def __repr__(self):
        return f"EvidenceItem({self.describe()!r})"


class EvidenceSet(list):
    """
    A list of `EvidenceItem`s (what `evidence_items` returns); `check_grounding` matches against it unit-aware.

    :ivar truncated: ``{(block id, column key): total rows or None}`` for each column the ``cap`` of `evidence_items` cut
        short (``None`` when the full length is not known, or the column was left out). Anything that needs the whole
        column (``[min]``, ``[max]``, ``[last]``) must not be answered from a truncated one.
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.truncated = {}

    def values(self):
        return np.array([e.value for e in self], dtype=float)


_ORDINAL_QUANTITIES = {"index", "int", "count", "charge", "multiplicity"}
_FRACTION_QUANTITIES = {"fraction", "ratio", "percent", "proportion", "probability"}


def _strings(value, cap):
    """The strings of a flat-data value if it is a string (or an array of strings), else ``None``."""
    if isinstance(value, str):
        return [value]
    try:
        arr = np.asarray(value)
    except Exception:  # noqa: BLE001
        return None
    if arr.dtype.kind in "US":
        return [str(x) for x in arr.ravel()[:cap]]
    if arr.dtype == object and arr.size and all(isinstance(x, str) for x in arr.ravel()[:50]):
        return [x for x in arr.ravel()[:cap] if isinstance(x, str)]
    return None


def _total(value):
    try:
        return int(np.asarray(value).size)
    except Exception:  # noqa: BLE001 - ragged data: the length is not known
        return None


def evidence_items(texts=(), readouts=(), cap=20000, max_total=None):
    """
    Like `evidence_numbers`, but an `EvidenceSet` that keeps each value's unit, quantity, label and position.

    A column keeps at most ``cap`` values, so that one very long column does not leave the others out (they are cut at
    the same row); ``max_total`` (default ``10 * cap``) bounds all of them, and columns past it are left out. Both
    are recorded in `EvidenceSet.truncated`.

    :param texts: strings, or ``(block id, string)`` pairs (numbers read from text keep the unit written after them)
    :param readouts: `Readout`s, or ``(block id, Readout)`` pairs; their ``to_flat_data()`` metadata gives each
        value's ``label``, ``unit`` and ``quantity``
    """
    if isinstance(texts, str):
        texts = (texts,)
    out = EvidenceSet()
    max_total = 10 * cap if max_total is None else max_total

    def room():
        return min(cap, max_total - len(out))

    for ro in readouts:
        block, ro = ro if isinstance(ro, tuple) else (None, ro)
        data, meta = ro.to_flat_data()
        for key, v in data.items():
            if room() <= 0:
                out.truncated[(block, key)] = None
                continue
            m = meta.get(key) or {}
            label = m.get("label") or key.rsplit("/", 1)[-1]
            strings = _strings(v, room())
            if strings is not None:
                many = len(strings) > 1
                for j, x in enumerate(strings):
                    out.append(EvidenceItem(float("nan"), None, m.get("quantity"), label, block,
                                            j + 1 if many else None, "data", False, key, text=x))
                continue
            chunks = []
            _scalars(v, chunks, room())
            flat = np.concatenate(chunks) if chunks else np.zeros(0)
            if not flat.size:
                continue
            unit, quantity = canonical_unit(m.get("unit")), m.get("quantity")
            many = flat.size > 1
            taken = flat[:room()]
            total = _total(v)
            if total is not None and total > taken.size:
                out.truncated[(block, key)] = total
            for j, x in enumerate(taken):
                out.append(EvidenceItem(x, unit, quantity, label, block, j + 1 if many else None, "data",
                                        unit == "percent", key, unit_name=m.get("unit") or None))
    for t in texts:
        block, t = t if isinstance(t, tuple) else (None, t)
        for n in extract_numbers(t):
            if len(out) >= max_total:
                break
            out.append(EvidenceItem(n.value, None if n.percent else n.unit, None, "text", block, None, "text",
                                    n.percent, decimals=n.decimals))
    return out


class GroundingResult:
    """
    ``ok`` if every checked number matched; ``unmatched`` are the `NumberToken`s that didn't; ``checked`` counts the
    non-exempt ones; ``matches`` pairs each matched token with the `EvidenceItem` it matched (only when the evidence
    was an `EvidenceSet`); ``reasons`` maps an unmatched token's text to why a value equal to it was not accepted.
    """

    def __init__(self, ok, unmatched, checked, matches=(), reasons=None):
        self.ok, self.unmatched, self.checked = ok, list(unmatched), checked
        self.matches, self.reasons = list(matches), dict(reasons or {})

    def errors(self):
        """Messages for a revision prompt, one per unmatched number."""
        out = []
        for t in self.unmatched:
            why = self.reasons.get(t.text)
            if why:
                out.append(f"the number {t.text!r} {why}")
            else:
                out.append(f"the number {t.text!r} does not appear in the evidence; state only values that are shown "
                           f"there (do not compute new ones)")
        return out

    def provenance(self, items=None):
        """
        ``[{"number": "1622.3", "matched": "r3 Frequency row 1 = 1622.30303 cm-1", "use": "{r3.frequency[1]}"}]`` for
        the matched numbers. ``use`` (given ``items``, the `EvidenceSet` that was checked) is the placeholder that
        writes that value, number and unit, without typing it.
        """
        from .Fill import ref_for
        out = []
        for t, e in self.matches:
            row = {"number": t.text, "matched": e.describe()}
            if items is not None and e.origin == "data" and e.key:
                row["use"] = "{" + ref_for(e, items) + "}"
            out.append(row)
        return out

    def __repr__(self):
        return f"GroundingResult(ok={self.ok}, unmatched={self.unmatched}, checked={self.checked})"


def _is_exempt(tok, small_int_max, year_range):
    is_int = tok.decimals == 0 and "." not in tok.text and "e" not in tok.text.lower() and "×" not in tok.text
    if not is_int or tok.percent or tok.unit:
        return False         # a percentage or a number with a unit is a measurement, not a count or a year
    if abs(tok.value) <= small_int_max:
        return True
    digits = tok.text.lstrip("+-−")
    if len(digits) == 4 and year_range[0] <= tok.value <= year_range[1]:
        return True
    return False


def _near(x, t, e, rel_tol):
    d = abs(abs(e) - x)
    return d <= t * (1 + 1e-9) or d <= rel_tol * abs(e)


def _compatible(tok, item):
    """``None`` if ``tok`` may be read as ``item``, else the reason it may not."""
    what = item.describe()
    if tok.percent:
        if item.percent or item.unit == "percent" or item.quantity in _FRACTION_QUANTITIES:
            return None
        if item.unit is None and item.quantity is None and item.origin == "data" and abs(item.value) <= 1:
            return None      # a plain fraction written as a percentage
        return f"is a percentage, but the only value equal to it is {what}, which is not a percentage or a fraction"
    if tok.unit:
        if item.unit == tok.unit:
            return None
        if item.unit is None and item.quantity is None:
            return None      # nothing says what the value is; accept
        if item.quantity in _ORDINAL_QUANTITIES:
            return f"is given in {tok.unit}, but the only value equal to it is {what}, a {item.quantity}"
        return (f"is given in {tok.unit}, but the only value equal to it is {what}; quote values in the unit the "
                f"data shows")
    return None


def check_grounding(text, evidence, rel_tol=1e-3, small_int_max=10, year_range=(1900, 2100), skip=()):
    """
    Match the numbers of ``text`` against ``evidence``: an `EvidenceSet` from `evidence_items` (unit- and
    quantity-aware, with provenance), or an array from `evidence_numbers` / any iterable of floats (values only).

    A number ``x`` written with ``d`` decimals matches an evidence value ``e`` if ``|x - e| <= 0.5 * 10**-d`` or
    ``|x - e| <= rel_tol * |e|``; a percentage also tries ``x / 100``; the comparison is on absolute values, because
    prose often says "a shift of 12.3" for −12.3. Integers up to ``small_int_max`` and four-digit years in
    ``year_range`` are exempt, unless they carry a unit or a % sign. With an `EvidenceSet`, values from the readouts'
    data take precedence over numbers read from their text, and a match must also fit the number's unit (see
    `_compatible`). ``skip`` is a list of ``(start, end)`` spans of ``text`` not to check (values the server filled in).
    """
    if isinstance(evidence, EvidenceSet):
        return _check_items(text, evidence, rel_tol, small_int_max, year_range, skip)
    ev = np.asarray(evidence, dtype=float).ravel()
    unmatched, checked = [], 0
    aev = np.abs(ev)
    for tok in extract_numbers(text):
        if _skipped(tok, skip) or _is_exempt(tok, small_int_max, year_range):
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


def _skipped(tok, skip):
    return any(tok.span[0] < e and s < tok.span[1] for s, e in skip)


def _check_items(text, items, rel_tol, small_int_max, year_range, skip):
    unmatched, matches, reasons, checked = [], [], {}, 0
    data = [e for e in items if e.origin == "data"]
    texts = [e for e in items if e.origin != "data"]
    for tok in extract_numbers(text):
        if _skipped(tok, skip) or _is_exempt(tok, small_int_max, year_range):
            continue
        checked += 1
        tol = 0.5 * 10.0 ** (-max(tok.decimals, 0))
        x = abs(tok.value)

        def equal(e):
            if _near(x, tol, e.value, rel_tol):
                return True
            # a percentage of a fraction (12.5% for 0.125), unless the value itself is a percentage
            return tok.percent and not (e.percent or e.unit == "percent") and _near(x / 100, tol / 100, e.value, rel_tol)

        found, why = None, None
        for pool in (data, texts):          # text numbers only count when no data value equals the number
            hits = [e for e in pool if equal(e)]
            if not hits:
                continue
            for e in hits:
                r = _compatible(tok, e)
                if r is None:
                    found = e
                    break
                why = why or r
            break
        if found is None:
            unmatched.append(tok)
            if why:
                reasons[tok.text] = why
        else:
            matches.append((tok, found))
    return GroundingResult(not unmatched, unmatched, checked, matches, reasons)
