# <a id="McUtils.Numputils.TensorDerivatives.nca_op_deriv">nca_op_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TensorDerivatives.py#L201)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L201?message=Update%20Docs)]
</div>

```python
nca_op_deriv(op, A_expansion, B_expansion, order, axes, contract, shared=None, identical=False): 
```
**LLM Docstring**

Compute the derivative expansion of a binary tensor operation (a contraction
or an outer product) applied to two expansions, via the generalized Leibniz
rule.

Normalizes the operand axes, determines where the new derivative axes will
appear, and sums the Leibniz terms at each requested order. For outer products
the operated axes are required to be the trailing axes of each operand.
  - `op`: `Callable`
    > the binary operation
  - `A_expansion`: `list`
    > expansion of the first operand
  - `B_expansion`: `list`
    > expansion of the second operand
  - `order`: `int | list[int]`
    > derivative order(s) to compute
  - `axes`: `tuple`
    > `(a_axes, b_axes)` operated on
  - `contract`: `bool`
    > whether the operation contracts (vs. outer-products) the axes
  - `shared`: `int | None`
    > number of shared leading batch axes
  - `identical`: `bool`
    > whether the two operands are the same expansion
  - `:returns`: `list`
    > the list of derivative tensors, one per requested order











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TensorDerivatives/nca_op_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TensorDerivatives/nca_op_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TensorDerivatives/nca_op_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TensorDerivatives/nca_op_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L201?message=Update%20Docs)   
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