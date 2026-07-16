# <a id="McUtils.Numputils.VectorOps.frac_powh">frac_powh</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L1184)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L1184?message=Update%20Docs)]
</div>

```python
frac_powh(A, k, eigsys=None, pow=None, nonzero_cutoff=None): 
```
**LLM Docstring**

Raise a symmetric/Hermitian matrix to a fractional power via its eigen
decomposition.

The matrix is diagonalized with `np.linalg.eigh` (reusing a supplied `eigsys`
if given), each eigenvalue is raised to the power `k` with `pow`, and the matrix
is reassembled. A `nonzero_cutoff` treats near-zero eigenvalues as `1` during
the power and zeros them afterward so they vanish on contraction; non-square
inputs are padded to square first.
  - `A`: `np.ndarray`
    > the symmetric matrix
  - `k`: `float`
    > the exponent
  - `eigsys`: `tuple | None`
    > precomputed `(eigenvalues, eigenvectors)` (optional)
  - `pow`: `Callable | None`
    > elementwise power function (defaults to `np.power`)
  - `nonzero_cutoff`: `float | None`
    > eigenvalue magnitude below which values are treated as zero
  - `:returns`: `np.ndarray`
    > the fractional matrix power











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/frac_powh.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/frac_powh.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/frac_powh.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/frac_powh.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L1184?message=Update%20Docs)   
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