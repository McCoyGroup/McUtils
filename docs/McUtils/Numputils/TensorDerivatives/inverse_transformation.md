# <a id="McUtils.Numputils.TensorDerivatives.inverse_transformation">inverse_transformation</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TensorDerivatives.py#L891)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L891?message=Update%20Docs)]
</div>

```python
inverse_transformation(forward_expansion, order, reverse_expansion=None, allow_pseudoinverse=False, nonzero_cutoff=None): 
```
**LLM Docstring**

Compute the derivative expansion of the inverse of a transformation from its
forward expansion (i.e. invert a Jacobian-and-higher-derivatives series).

The zeroth-order inverse is the (pseudo)inverse of the leading Jacobian; each
higher order is obtained by re-expanding the current inverse through the forward
expansion and contracting back in the leading inverse.
  - `forward_expansion`: `list`
    > the forward transformation expansion
  - `order`: `int | list[int]`
    > the derivative order
  - `reverse_expansion`: `list | None`
    > a precomputed inverse expansion to extend
  - `allow_pseudoinverse`: `bool`
    > use the pseudoinverse for non-square leading terms
  - `nonzero_cutoff`: `float | None`
    > singular-value cutoff for a regularized inverse
  - `:returns`: `list`
    > the inverse transformation expansion











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TensorDerivatives/inverse_transformation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TensorDerivatives/inverse_transformation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TensorDerivatives/inverse_transformation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TensorDerivatives/inverse_transformation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L891?message=Update%20Docs)   
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