# <a id="McUtils.Numputils.TransformationMatrices.apply_symmetries">apply_symmetries</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TransformationMatrices.py#L1487)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1487?message=Update%20Docs)]
</div>

```python
apply_symmetries(coords, symmetry_elements: 'list[np.ndarray]', labels=None, tol=0.1): 
```
**LLM Docstring**

Grow a set of coordinates by repeatedly applying symmetry operations, keeping
only the newly generated (non-duplicate) points.

For each operation the transformed points are compared against the current set
(within tolerance `tol`) and only distinct new points are appended; optional
`labels` are propagated alongside.
  - `coords`: `np.ndarray`
    > the seed coordinates
  - `symmetry_elements`: `list[np.ndarray]`
    > the symmetry operation matrices to apply
  - `labels`: `Iterable | bool | None`
    > optional per-point labels to carry along
  - `tol`: `float`
    > duplicate-detection tolerance
  - `:returns`: `np.ndarray | tuple`
    > the expanded coordinates (and labels if provided)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TransformationMatrices/apply_symmetries.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TransformationMatrices/apply_symmetries.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TransformationMatrices/apply_symmetries.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TransformationMatrices/apply_symmetries.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1487?message=Update%20Docs)   
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