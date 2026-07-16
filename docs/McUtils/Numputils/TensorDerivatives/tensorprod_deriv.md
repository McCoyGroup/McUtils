# <a id="McUtils.Numputils.TensorDerivatives.tensorprod_deriv">tensorprod_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TensorDerivatives.py#L491)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L491?message=Update%20Docs)]
</div>

```python
tensorprod_deriv(A_expansion, B_expansion, order, axes=None, identical=False): 
```
**LLM Docstring**

Compute the derivative expansion of an outer/tensor product between two
expansions.

Resolves the product axes (`'all'` selects every non-shared axis), infers the
shared batch dimension, and builds the expansion via the generalized Leibniz
rule with a non-contracting operation.
  - `A_expansion`: `list`
    > expansion of the first operand
  - `B_expansion`: `list`
    > expansion of the second operand
  - `order`: `int | list[int]`
    > derivative order(s) to compute
  - `axes`: `list | str | None`
    > the product axes (defaults to `[-1, -1]`; `'all'` for every axis)
  - `identical`: `bool`
    > whether the two operands are the same expansion
  - `:returns`: `list`
    > the outer-product derivative expansion











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TensorDerivatives/tensorprod_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TensorDerivatives/tensorprod_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TensorDerivatives/tensorprod_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TensorDerivatives/tensorprod_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L491?message=Update%20Docs)   
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