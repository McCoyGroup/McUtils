# <a id="McUtils.Coordinerds.ZMatrices.extract_zmatrix_internals">extract_zmatrix_internals</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L392)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L392?message=Update%20Docs)]
</div>

```python
extract_zmatrix_internals(zmat, strip_embedding=True, canonicalize=True): 
```
**LLM Docstring**

Expand a Z-matrix ordering into its bond, angle, and dihedral coordinate tuples.

Three-column orderings are first promoted to four columns by adding the implicit atom index and embedding row. For each row the function emits the bond prefix, then the angle prefix, then the dihedral prefix, skipping the undefined embedding entries for the first three atoms when requested. Returned tuples may be canonicalized to make reversed coordinates equivalent.
  - `zmat`: `Sequence[Sequence[int]]`
    > Three- or four-column Z-matrix ordering.
  - `strip_embedding`: `bool`
    > Omit coordinates that only establish the external frame.
  - `canonicalize`: `bool`
    > Canonicalize each emitted coordinate tuple.
  - `:returns`: `list[tuple[int, ...]]`
    > Ordered list of internal-coordinate tuples represented by the Z-matrix.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/extract_zmatrix_internals.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/extract_zmatrix_internals.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/extract_zmatrix_internals.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/extract_zmatrix_internals.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L392?message=Update%20Docs)   
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