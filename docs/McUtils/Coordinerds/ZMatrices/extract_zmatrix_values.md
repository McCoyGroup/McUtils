# <a id="McUtils.Coordinerds.ZMatrices.extract_zmatrix_values">extract_zmatrix_values</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L444)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L444?message=Update%20Docs)]
</div>

```python
extract_zmatrix_values(zmat, inds=None, partial_embedding=False, strip_embedding=True): 
```
**LLM Docstring**

Flatten Z-matrix values and select internal-coordinate entries.

A four-column array is interpreted as containing atom indices in column 0, which are removed before flattening. When no explicit indices are supplied, all values are selected and embedding entries are deleted if requested. Explicit indices are interpreted in the stripped coordinate space when `strip_embedding` is true.
  - `zmat`: `array-like`
    > Z-matrix value array with shape `(..., n_atoms, 3)` or a four-column combined array.
  - `inds`: `Sequence[int] | None`
    > Coordinate positions to extract, or all positions when omitted.
  - `partial_embedding`: `bool`
    > Use the reduced embedding mask when automatically selecting coordinates.
  - `strip_embedding`: `bool`
    > Exclude embedding entries and interpret `inds` relative to the remaining coordinates.
  - `:returns`: `np.ndarray`
    > Selected values with the atom/value axes flattened into one final axis.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/extract_zmatrix_values.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/extract_zmatrix_values.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/extract_zmatrix_values.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/extract_zmatrix_values.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L444?message=Update%20Docs)   
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