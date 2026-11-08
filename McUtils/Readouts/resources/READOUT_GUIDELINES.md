# Readout guidelines: writing sources that work in reports

For anyone adding or changing a readout (a `ReadoutAdapter`, `@readout_section`, `Field`, `Column`) that a
`SourceCatalog` may offer to a report, whether a person or a model writes the report. Everything here follows from how
the report layer (`McUtils.Readouts.Reports`, V4) reads a readout: it never looks at the object, only at the
readout's sections, their text and their flat data (`readout.to_flat_data()` -> `(data, metadata)`). This file ships with the package (`McUtils/Readouts/resources/`).

## 1. What the report layer sees

| It reads | From | Used for |
|---|---|---|
| Section names, `description`, `default`, `available` | `@readout_section(...)` | the menu (`describe_source`), what `apply_template` and `add_readout` can name |
| The section's text | `readout.to_text()` of the section | `peek`, and as a second pool of evidence numbers |
| Flat data: key, array/scalar value | `to_flat_data()[0]` | the values a placeholder or a typed number is checked against |
| Per key: `label`, `unit`, `quantity` | `to_flat_data()[1]` (from `Field`/`Column`) | placeholder names, the unit label that is written, the unit and quantity checks |

Nothing else counts. A value that is only in the object, or only in a figure, cannot be stated in a report.

## 2. How a model states a value

The report tells a model, at every context level, to write a **placeholder** instead of a number:
`{r3.frequency[2]}` is "block `r3`, column `frequency`, row 2 (1-based, as `peek` shows)". The server replaces it with
the value and its unit label (`3803.3 cm⁻¹`). A person can do the same with `ReportDocument.add_text`.

Typed numbers are **allowed**: there are good reasons to state a number that is not in a readout (a temperature the
user gave, a literature value), and the number check is off by default (`--policy unchecked`). The report encourages
placeholders instead of requiring them:

- Readout data is shown to the model as placeholders, not expanded. `peek(handle, section)` lists a section's columns,
  the placeholder of each (`{r3.frequency[ROW]}`), its rows and one example value; `peek(..., expand=true)` gives the
  text with the values, and `values(block_id, column)` lists every row with its placeholder. The receipts of
  `add_readout` / `apply_template` list the placeholders of the blocks they add.
- A paragraph reads back as it was written (`compile(full_text=true)`; `ReportDocument.written_text`), so the model
  sees the pattern it should keep writing.
- A number that is not in the data is marked `{=300 K}` (or listed in `literals`): the report writes it as given and
  records it as a *given value*, so it is distinguishable from a number someone typed and forgot to check.
- A text result carries `notes` about the numbers it typed: a value of the data gets its placeholder; any other is
  pointed at the `{=...}` marker. Notes never refuse a text. `autolink` (off by default, `--autolink`) rewrites a typed
  number that is exactly one value of the data into its placeholder.
- A paragraph can say what it is about (`basis`: `data`, `background`, `user_input`), and `compile` reports the
  `coverage`: placeholders, given values and typed numbers (and how many typed ones were values of the data).

The strict mode is opt-in (`--policy grounded`): text must cite readouts and every typed number must match a cited value
in the same unit; a refusal names the placeholder that matches. So the better a readout's data serves placeholders, the
more a report is made of values the server wrote, and the less it depends on any check.

**Write the readout for the placeholder.** Concretely:

1. **Column / field names are the placeholder names.** `r3.frequency[2]` resolves `frequency` as the last part of the
   flat-data key (`molecule/normal_modes/frequencies/frequency`) or, failing that, the label in lower case with `_`
   for spaces. Use short, stable, unique names. If two columns of one block end in the same word the placeholder needs
   a longer tail (`bonds.value`), which a model gets wrong more often.
2. **Row order is the display order**, and the first row is `[1]`. Do not reorder between the table text and the data.
3. **One quantity per column.** A column that mixes units or mixes numbers and codes cannot be given a unit.
4. **Put what you want stated in the data, not only in a caption or a picture.** If a report should be able to say
   "mode 1 is the bend", the readout needs a string column (`mode_label`, `assignment`) that says so; then
   `{r3.mode_label[1]}` writes it. If the source does not provide an interpretation, do not hide it in prose text.
5. **String columns are first-class.** Label columns (`atom`, `formula`, `mode`) are filled like numbers
   (`{r4.atom[2]}` -> `H`). They take no format spec and are not combined in expressions.

## 3. Units

The unit written after a filled value is the **`UnitsData` label for the unit's name** (`Wavenumbers` -> `cm⁻¹`,
`Hartrees` -> `Eₕ`, `Angstroms` -> `Å`, `KilometersPerMole` -> `km/mol`). The labels live in
`McUtils.Data.UnitsData` (`UnitsData.unit_label(name, style=None)`); the readout theme and
`McUtils.Readouts.Reports.unit_shorthand` both use it, so a label is defined once.

**Where labels come from.** The data is `McUtils/Data/TheRealMcCoy/UnitLabelsSupplement.json` (next to the other
`*Supplement.json` files): labels for *base* units (`Meters`, `Hartrees`, `Calories`, ...) and for the SI prefixes. Every
other name is composed from them with the grammar `UnitsData` already uses for conversions: a prefix (`Kilo`, `Milli`,
...), `Inverse` before a name, `Squared`/`Cubed`/... after it, `A/B`, `A B` and `APerB`. So `KilocaloriesPerMole` is
`kcal/mol`, `InverseAngstromsSquared` is `Å⁻²` and `GigaElectronVolts` is `GeV` without being listed; `Wavenumbers`
is an alias of `InverseCentimeters`. A name with a part that has no label (a physical constant used as a unit, say) is
written as it is named. Symbols follow NIST (SP 811 and the CODATA listing the conversions were scraped from).

**Styles.** Every label exists in three styles, and one can be chosen:

| style | `Wavenumbers` | `Hartrees` | `Degrees` | a filled value |
|---|---|---|---|---|
| `unicode` (default) | `cm⁻¹` | `Eₕ` | `°` | `3803.3 cm⁻¹` |
| `ascii` | `cm-1` | `Eh` | `deg` | `3803.3 cm-1` |
| `latex` | `\mathrm{cm^{-1}}` | `E_{\mathrm{h}}` | `^{\circ}` | `$3803.3\,\mathrm{cm^{-1}}$` |

LaTeX labels are math-mode fragments without `$`; the report wraps number and unit together in `$...$`. A style a
unit has no entry for is built from its unicode label by rule (`to_ascii`, `to_latex`). Choose the style:

- globally: `UnitsData.set_label_style("ascii")` (also what themes and reports use when they are not told otherwise);
- per theme: `ReadoutTheme(unit_style="latex")`, with `unit_labels={"Hartrees": "Ha"}` (or `{"Hartrees": {"latex": ...}}`)
  as overrides;
- per report: `report_toolset(doc, catalog, unit_style="ascii")` / `serve_report(..., unit_style=...)` /
  `python -m McUtils.Readouts.Reports --unit-style ascii`. It is stored in the report (`report-meta`), and the
  instructions' examples show the same style. Fills already written keep the style they were written in.

**Labels for new units.** Add a base unit to the supplement file (`{"unicode": ..., "ascii": ..., "latex": ...}`, or
`{"alias": "OtherUnit"}`), at run time with `UnitsData.update_unit_labels({"Debyes": {"unicode": "D", "ascii": "D",
"latex": r"\mathrm{D}"}})`, or merge a JSON table with `UnitsData.load_unit_labels("labels.json", overwrite=False)`. A
style left out is built from the unicode label by rule. Do not list composite units; they are composed.

So, in a readout:

- Give every dimensional `Field` / `Column` a `unit=` that is a `UnitsData` unit name (`"Wavenumbers"`, not
  `"cm^-1"` and not `"cm-1"`). Other spellings are recognised for matching (`cm^-1`, `Hartree`) but the readout
  itself should use the canonical name, so labels and the report agree.
- A unit with no label is written as it is named. Add a label (above) rather than handling it in the readout.
- Convert **before** building the readout (`ReadoutContext.units`), so the data, the table text and the unit label
  all agree. The report cannot convert.
- A dimensionless value (a count, an index, a charge) has **no** unit. A model that types a unit after one gets
  `unit_mismatch`.
- Percentages: `unit="percent"` (written `12.5%`, in LaTeX `$12.5\%$`), or store a fraction and let the reader format
  it. Do not store a percentage as a plain number with no unit.

What the check does with units: a typed number followed by a unit only matches a value in that unit; a percentage only
matches a percentage or a fraction (never an index, count or intensity); an integer with a unit is never exempt as a
"small integer" or a year. A unit typed after a placeholder is swallowed (in any style) and replaced by the label.

## 4. Quantities

Set `quantity=` (`frequency`, `energy`, `length`, `mass`, `intensity`, `charge`, `index`, `int`, `count`, `fraction`,
...). Two values matter most to the checker: `index`, `int` and `count` mark values a unit or a percentage must never
be matched to (a mode number 3 is not "3%"), and `fraction` / `ratio` / `percent` mark values a percentage may be matched
to. Use them honestly for identifiers too (`identifier` for labels, `path` for files).

## 5. Sections

- `description=` is the model's menu. One sentence, ends with a period, says what is in the section and in what unit.
  No backticks. It is what a model reads before choosing, so say what the data **is**, not how it is built.
- `default=False` for large or optional sections (animations, displacement vectors, dumps).
- `available=` returns `(False, "reason")` when the object lacks the data; the reason is shown to the model.
  Return `(True, ...)` only if the reason is informational.
- Sections that are expensive to build should say so (`cost=`): `describe_source` builds each section to classify it.
- Name a part with a dot (`normal_modes.frequencies`) when a section bundles a table with heavy parts, so a template
  can take the table alone.
- A model may name a section by its key, its `title`, or a heading of the report template (a heading stands for the
  sections under it); the tool says which section it matched. Keep titles and template headings distinct from the keys of
  other sections so that a name means one thing.

## 6. Report templates

A source that should produce a standard report declares a `ReportTemplate` (`sections`, `optional`, `locked`,
`locked_headings`, fixed captions) and attaches it as `report_template` on its readout interface, or registers it
with `register_report_template`. A fixed template needs no model to choose content. Locks are opt-in per template
(`locked = [...]`): the tools then refuse to edit, move or remove those blocks.

Fixed captions are written by the template and carry the status `template`; they are not filled or checked, so they
should state no numbers.

## 7. What the checker does not do

The number check (opt-in, `--policy grounded`) checks **numbers and units only**. It does not check words: a paragraph can still call a mode a "stretch" next to a
correct number, and nothing refuses it. (V3 had a word-list claims check; V4 removed it.) What protects a report from
unsupported interpretation is therefore (a) the data you provide, (b) the instructions telling the model to describe
only what the data shows, and (c) a human reading the result. Write readouts so that the statements a report needs are
in the data (section 2, point 4) and review any interpretation the data does not contain.

Even then it is a matcher, not a proof: a number is compared with the values of the cited blocks pooled together, so a
right value attached to the wrong quantity passes; small integers, years and numbers in backticks are exempt; and
spelled-out numbers are not seen. Placeholders are the only exact way to state a value.

Computed values (`{mean(r3.frequency[2], r3.frequency[3])}`) are **on by default** (`--no-derived` or
`allow_derived=False` turns them off). They exist so that a number the user asks for (a difference, a mean) is written by
the server; the instructions tell the model not to add comparisons nobody asked for. The multi-edit tool `apply_edits` is
off by default and enabled with `--apply-edits` (`apply_edits=True`).

A row can be named by a selector instead of a number: `{r5.y[max]}`, `[min]`, `[first]`, `[last]`, and `{r5.x[max:y]}` for
the x where `y` is largest. A selector is one reference, not a computed value, so it works with derived values off. It
suits long columns (a curve, a convergence history), where "the peak" or "the final value" should not need the model to
find the row; keep the quantity you want to rank numeric and give both columns of a series short, stable names (`x`, `y`).

Long columns (more than 12 rows) are summarised wherever the placeholders are listed (`peek`, `values`, the receipts of
`add_readout`): the line adds the minimum, maximum and last row with the selector placeholder and the row each is in, so
a model can state "the peak is X at row N" without paging through the series. `values(block, column)` lists rows in pages
(`start`, `limit`). The report loads at most 20000 values of a readout; a column cut short by that has no `[min]`, `[max]`
or `[last]` (they would describe part of the data), and the summary says so.

A section that holds only export-only arrays (`ReadoutArray` without `display=True`) shows nothing in a plain readout. In a
report it shows one line instead (`Not displayed (data only): Displacements: shape (2, 4, 3), float64; min 0, max 23. The
values are in the data export.`) and `compile`, and the receipt of `add_readout`, carry a `not_displayed` note, so a block
is never silently missing from the HTML or PowerPoint. If the values matter to the reader, put them in a table, or in a
plot built with `data=` (the numbers of a plot enter the evidence and can be written with placeholders; its text form says
how many points of which columns it plots).

## 8. Checklist

- [ ] Every dimensional column/field has `unit=` set to a `UnitsData` name that has a label (`UnitsData.unit_label(name)`).
- [ ] Every column/field has a short, unique name and a `quantity`.
- [ ] Label columns exist for anything a report may need to name (modes, atoms, states).
- [ ] Row order and numbering match the table text; row 1 is `[1]`.
- [ ] Section `description` is one sentence with the unit; heavy or optional sections are `default=False`.
- [ ] Values are converted when the readout is built.
- [ ] If the source has a standard report, it has a `ReportTemplate` with captions that state no numbers.
- [ ] Tried it: `peek` lists the placeholders you expect, `peek(expand=true)` shows the text, and `{r1.<column>[1]}` fills with
  the unit you expect.
