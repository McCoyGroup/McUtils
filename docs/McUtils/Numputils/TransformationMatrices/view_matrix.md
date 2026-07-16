# <a id="McUtils.Numputils.TransformationMatrices.view_matrix">view_matrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TransformationMatrices.py#L723)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L723?message=Update%20Docs)]
</div>

```python
view_matrix(up_vector, view_vector=(0, 0, 1), output_order=(2, 0, 1)): 
```
**LLM Docstring**

Build a viewing (camera) frame from an up vector and a view direction.

Orthonormalizes a right/up/view axis triple (handling the degenerate case where
the up and view vectors are nearly parallel), then reorders and sign-corrects
the columns according to `output_order` so the returned frame is a proper
rotation.
  - `up_vector`: `np.ndarray`
    > the up direction(s)
  - `view_vector`: `np.ndarray`
    > the view/forward direction
  - `output_order`: `tuple`
    > axis output ordering (indices or `'x'`/`'y'`/`'z'`)
  - `:returns`: `np.ndarray`
    > the viewing frame matrix (or stack)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TransformationMatrices/view_matrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TransformationMatrices/view_matrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TransformationMatrices/view_matrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TransformationMatrices/view_matrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L723?message=Update%20Docs)   
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