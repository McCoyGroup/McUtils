# <a id="McUtils.Coordinerds.ZMatrices.zmatrix_indices">zmatrix_indices</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L82)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L82?message=Update%20Docs)]
</div>

```python
zmatrix_indices(zmat, coords, strip_embedding=True): 
```
**LLM Docstring**

Locate internal coordinates within the ordered coordinate list represented by a Z-matrix.

The Z-matrix is expanded into its bond, angle, and dihedral tuples, optionally excluding embedding coordinates. Both the extracted coordinates and requested coordinates are canonicalized before list lookup. A single coordinate returns one integer; a sequence returns a list.
  - `zmat`: `Sequence[Sequence[int]]`
    > Four-column or reference-only Z-matrix ordering.
  - `coords`: `Sequence[int] | Sequence[Sequence[int]]`
    > One internal-coordinate tuple or a sequence of tuples.
  - `strip_embedding`: `bool`
    > Exclude the translational and rotational embedding entries from the searchable coordinate list.
  - `:returns`: `int | list[int]`
    > Position or positions of the requested coordinates.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/zmatrix_indices.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/zmatrix_indices.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/zmatrix_indices.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/zmatrix_indices.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L82?message=Update%20Docs)   
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