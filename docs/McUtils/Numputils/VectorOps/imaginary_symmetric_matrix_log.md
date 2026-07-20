# <a id="McUtils.Numputils.VectorOps.imaginary_symmetric_matrix_log">imaginary_symmetric_matrix_log</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L2262)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L2262?message=Update%20Docs)]
</div>

```python
imaginary_symmetric_matrix_log(mats_real, mats_imag): 
```
**LLM Docstring**

Recover the symmetric generator `A` from the real and imaginary parts of
`exp(i A)`.

The real part is diagonalized to obtain `arccos` of its eigenvalues, the
imaginary part is rotated into the same basis to supply `arcsin`, and the
generator is rebuilt in that eigenbasis.
  - `mats_real`: `np.ndarray`
    > real part of `exp(i A)`
  - `mats_imag`: `np.ndarray`
    > imaginary part of `exp(i A)`
  - `:returns`: `np.ndarray`
    > the symmetric generator











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/imaginary_symmetric_matrix_log.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/imaginary_symmetric_matrix_log.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/imaginary_symmetric_matrix_log.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/imaginary_symmetric_matrix_log.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L2262?message=Update%20Docs)   
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