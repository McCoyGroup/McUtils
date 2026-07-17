# <a id="McUtils.Coordinerds.ZMatrices.parse_zmatrix_string">parse_zmatrix_string</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L541)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L541?message=Update%20Docs)]
</div>

```python
parse_zmatrix_string(zmat, units='Angstroms', in_radians=False, has_values=True, atoms_are_order=False, keep_variables=False, variables=None, dialect='gaussian'): 
```
**LLM Docstring**

Parse a Gaussian-style textual Z-matrix into atoms, ordering, and coordinate values.

The atom/reference/value token stream is split into rows of increasing width for the first three atoms and seven fields thereafter. Positive one-based references are converted to zero-based indices. A `Variables:` block is parsed into constants or scan specifications. Unless variables are retained, symbols are replaced by numeric values, distances are converted from `units` to Bohr, and angles and dihedrals are converted to radians unless already supplied in radians.
  - `zmat`: `str`
    > Gaussian-style Z-matrix text, optionally followed by a `Variables:` block.
  - `units`: `str`
    > Distance unit used by numeric values.
  - `in_radians`: `bool`
    > Treat angular values as radians instead of degrees.
  - `has_values`: `bool`
    > Whether coordinate values alternate with reference indices in each row.
  - `atoms_are_order`: `bool`
    > Interpret the atom column as an explicit one-based atom permutation rather than element symbols.
  - `keep_variables`: `bool`
    > Return unresolved coordinate tokens and the variable table instead of numeric arrays.
  - `variables`: `dict | None`
    > Additional or overriding variable definitions.
  - `dialect`: `str`
    > Input dialect; only `gaussian` is implemented.
  - `:returns`: `tuple`
    > Numeric `(atoms, ordering, coords)`, or `((atoms, ordering, token_coords), variables)` when variables are retained.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/parse_zmatrix_string.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/parse_zmatrix_string.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/parse_zmatrix_string.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/parse_zmatrix_string.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L541?message=Update%20Docs)   
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