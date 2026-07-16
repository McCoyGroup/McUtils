# <a id="McUtils.Numputils.VectorOps.fractional_power">fractional_power</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L2061)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L2061?message=Update%20Docs)]
</div>

```python
fractional_power(A, pow, zero_cutoff=1e-08): 
```
**LLM Docstring**

Raise a symmetric matrix to an arbitrary (fractional) power, discarding
near-zero eigenvalues.

The matrix is diagonalized with `np.linalg.eigh`; eigenvalues with magnitude
above `zero_cutoff` are kept and raised to `pow`, and the matrix is reassembled
from the retained eigenpairs. Batched inputs are handled per matrix, returning a
list when the retained rank varies across the batch.
  - `A`: `np.ndarray`
    > the symmetric matrix (or stack)
  - `pow`: `float`
    > the exponent
  - `zero_cutoff`: `float`
    > eigenvalue magnitude below which directions are dropped
  - `:returns`: `np.ndarray | list[np.ndarray]`
    > the fractional matrix power (or a list for ragged batches)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/fractional_power.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/fractional_power.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/fractional_power.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/fractional_power.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L2061?message=Update%20Docs)   
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