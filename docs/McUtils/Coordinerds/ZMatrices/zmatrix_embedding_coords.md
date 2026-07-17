# <a id="McUtils.Coordinerds.ZMatrices.zmatrix_embedding_coords">zmatrix_embedding_coords</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L128?message=Update%20Docs)]
</div>

```python
zmatrix_embedding_coords(zmat_or_num_atoms, partial_embedding=False, array_inds=False): 
```
**LLM Docstring**

Return the flattened entries occupied by Z-matrix embedding coordinates.

For a molecule with zero, one, two, or at least three atoms, this selects the distance/angle/dihedral entries used to fix overall translation and rotation. With `partial_embedding`, only the three coordinates required by the partially embedded representation are selected. With `array_inds`, flattened positions are converted to `(row, column)` pairs and adjusted for three-column orderings.
  - `zmat_or_num_atoms`: `int | Sequence[Sequence[int]]`
    > Atom count or a Z-matrix-like ordering from which the atom count and column convention are inferred.
  - `partial_embedding`: `bool`
    > Select the reduced embedding used by `zmatrix_from_values(..., partial_embedding=True)`.
  - `array_inds`: `bool`
    > Return two-dimensional array indices instead of flattened indices.
  - `:returns`: `list[int] | list[tuple[int, int]]`
    > Embedding positions in flattened or `(row, column)` form.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/zmatrix_embedding_coords.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/zmatrix_embedding_coords.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/zmatrix_embedding_coords.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/zmatrix_embedding_coords.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L128?message=Update%20Docs)   
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