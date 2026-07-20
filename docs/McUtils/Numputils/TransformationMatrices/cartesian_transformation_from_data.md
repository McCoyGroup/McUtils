# <a id="McUtils.Numputils.TransformationMatrices.cartesian_transformation_from_data">cartesian_transformation_from_data</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TransformationMatrices.py#L1723)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1723?message=Update%20Docs)]
</div>

```python
cartesian_transformation_from_data(scalings, types, axes, roots, orders): 
```
**LLM Docstring**

Rebuild Cartesian transformation matrices from the classification data
produced by `identify_cartesian_transformation_type`.

Each type (identity, inversion, rotation, reflection, improper rotation) is
reconstructed from its axis/root/order, and any scaling is reapplied on top.
  - `scalings`: `np.ndarray | None`
    > per-transformation scaling matrices (or `None`)
  - `types`: `np.ndarray`
    > the transformation type codes
  - `axes`: `np.ndarray`
    > the transformation axes
  - `roots`: `np.ndarray`
    > the rational angle numerators
  - `orders`: `np.ndarray`
    > the rational angle denominators (rotation orders)
  - `:returns`: `np.ndarray`
    > the reconstructed transformation matrices











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TransformationMatrices/cartesian_transformation_from_data.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TransformationMatrices/cartesian_transformation_from_data.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TransformationMatrices/cartesian_transformation_from_data.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TransformationMatrices/cartesian_transformation_from_data.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1723?message=Update%20Docs)   
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