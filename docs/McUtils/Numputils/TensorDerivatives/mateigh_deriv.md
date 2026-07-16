# <a id="McUtils.Numputils.TensorDerivatives.mateigh_deriv">mateigh_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TensorDerivatives.py#L1284)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L1284?message=Update%20Docs)]
</div>

```python
mateigh_deriv(mat_exp, order, *, diagonal_only=True, base_expansion=None): 
```
**LLM Docstring**

Compute the derivative expansion of the symmetric eigen-decomposition
(eigenvalues and eigenvectors) of a matrix expansion.

Applies degenerate perturbation-theory-style recurrences: eigenvalue derivatives
come from the diagonal of the transformed matrix derivative, and eigenvector
derivatives from contracting the matrix derivative against the (regularized)
inverse of the eigenvalue-difference matrix. With `diagonal_only` set only the
diagonal eigenvalue block is tracked.
  - `mat_exp`: `list`
    > expansion of the (symmetric) matrix
  - `order`: `int`
    > the derivative order
  - `diagonal_only`: `bool`
    > track only the diagonal eigenvalue contributions
  - `base_expansion`: `tuple | None`
    > precomputed `(eigenvalue_expansion, eigenvector_expansion)`
  - `:returns`: `tuple[list, list]`
    > `(eigenvalue_expansion, eigenvector_expansion)`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TensorDerivatives/mateigh_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TensorDerivatives/mateigh_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TensorDerivatives/mateigh_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TensorDerivatives/mateigh_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L1284?message=Update%20Docs)   
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