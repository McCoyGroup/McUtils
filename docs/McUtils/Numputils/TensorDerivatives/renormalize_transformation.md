# <a id="McUtils.Numputils.TensorDerivatives.renormalize_transformation">renormalize_transformation</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TensorDerivatives.py#L948)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L948?message=Update%20Docs)]
</div>

```python
renormalize_transformation(forward_transformation, reverse_transformation, nonzero_cutoff=None): 
```
**LLM Docstring**

Rescale a forward/reverse transformation pair so that the singular values of
their product are normalized, keeping the pair mutually consistent.

Uses the SVD of `forward[0] @ reverse[0]` to build symmetric scaling factors
that are folded into the forward expansion from the left and the reverse
expansion from the right.
  - `forward_transformation`: `list`
    > the forward transformation expansion
  - `reverse_transformation`: `list`
    > the reverse transformation expansion
  - `nonzero_cutoff`: `float | None`
    > singular-value cutoff below which directions are dropped
  - `:returns`: `tuple[list, list]`
    > the renormalized `(forward, reverse)` pair











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TensorDerivatives/renormalize_transformation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TensorDerivatives/renormalize_transformation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TensorDerivatives/renormalize_transformation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TensorDerivatives/renormalize_transformation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L948?message=Update%20Docs)   
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