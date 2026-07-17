# <a id="McUtils.Coordinerds.ZMatrices.format_zmatrix_string">format_zmatrix_string</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L699)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L699?message=Update%20Docs)]
</div>

```python
format_zmatrix_string(atoms, zmat, ordering=None, units='Angstroms', in_radians=False, float_fmt='{:11.8f}', index_padding=1, variables=None, variable_modifications=None, distance_variable_format='r{i}', angle_variable_format='a{i}', dihedral_variable_format='d{i}'): 
```
**LLM Docstring**

Format atoms, references, and values as a Gaussian-style Z-matrix string.

Combined alternating reference/value rows are separated when `ordering` is omitted. Distances are converted from Bohr to `units`; angles are converted from radians to degrees unless requested otherwise. Optional generated variable names replace numeric values, coordinate-specific modifications can append scan/freeze suffixes, indices receive `index_padding`, and all columns are width-aligned. A `Variables:` block is appended when variables are present.
  - `atoms`: `Sequence[str]`
    > Atom labels in output order.
  - `zmat`: `array-like | Sequence`
    > Z-matrix values or alternating reference/value rows.
  - `ordering`: `Sequence[Sequence[int]] | None`
    > Reference-index rows, optionally including explicit atom indices.
  - `units`: `str`
    > Distance unit for formatted output.
  - `in_radians`: `bool`
    > Keep angular values in radians instead of converting to degrees.
  - `float_fmt`: `str`
    > Format string used for numeric values.
  - `index_padding`: `int`
    > Offset added to nonnegative atom references, normally 1 for Gaussian indexing.
  - `variables`: `dict | bool | None`
    > Existing variable mapping, `True` to generate one variable per defined coordinate, or `None` for inline values.
  - `variable_modifications`: `dict | None`
    > Mapping from coordinate tuples to suffix text appended to variable definitions.
  - `distance_variable_format`: `str`
    > Template for generated distance symbols.
  - `angle_variable_format`: `str`
    > Template for generated angle symbols.
  - `dihedral_variable_format`: `str`
    > Template for generated dihedral symbols.
  - `:returns`: `str`
    > Aligned Z-matrix text with an optional variable block.











---


<div markdown="1" class="text-secondary">
<div class="container">
  <div class="row">
   <div class="col" markdown="1">
**Feedback**   
</div>
   <div class="col" markdown="1">
**Examples**   
</div>
   <div class="col" markdown="1">
**Templates**   
</div>
   <div class="col" markdown="1">
**Documentation**   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Bug](https://github.com/McCoyGroup/McUtils/issues/new?title=Documentation%20Improvement%20Needed)/[Request](https://github.com/McCoyGroup/McUtils/issues/new?title=Example%20Request)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/format_zmatrix_string.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/format_zmatrix_string.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/format_zmatrix_string.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/format_zmatrix_string.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L699?message=Update%20Docs)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>
</div>