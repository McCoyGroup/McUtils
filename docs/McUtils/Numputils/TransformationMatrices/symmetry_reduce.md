# <a id="McUtils.Numputils.TransformationMatrices.symmetry_reduce">symmetry_reduce</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TransformationMatrices.py#L1545)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1545?message=Update%20Docs)]
</div>

```python
symmetry_reduce(coords, op: numpy.ndarray, labels=None): 
```
**LLM Docstring**

Reduce a set of coordinates to one representative per symmetry orbit under a
given operation.

The operation is turned into a permutation, its cycles are found, and the first
atom of each cycle is kept; optional labels are reduced the same way.
  - `coords`: `np.ndarray`
    > the coordinates to reduce
  - `op`: `np.ndarray`
    > the symmetry operation matrix
  - `labels`: `Iterable | None`
    > optional per-point labels
  - `:returns`: `np.ndarray | tuple`
    > the orbit representatives (and reduced labels if provided)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TransformationMatrices/symmetry_reduce.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TransformationMatrices/symmetry_reduce.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TransformationMatrices/symmetry_reduce.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TransformationMatrices/symmetry_reduce.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1545?message=Update%20Docs)   
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