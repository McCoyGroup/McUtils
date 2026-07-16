# <a id="McUtils.Numputils.PermutationOps.levi_cevita_dot">levi_cevita_dot</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/PermutationOps.py#L116)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L116?message=Update%20Docs)]
</div>

```python
levi_cevita_dot(k, a, /, axes, shared=None): 
```
**LLM Docstring**

Contract the rank-`k` Levi-Civita tensor with an array along the given axes,
exploiting its sparsity.

Delegates to `VectorOps.semisparse_tensordot` with the Levi-Civita nonzeros.
  - `k`: `int`
    > the Levi-Civita rank
  - `a`: `np.ndarray`
    > the array to contract against
  - `axes`: `tuple`
    > `(levi_civita_axes, array_axes)` to contract
  - `shared`: `int | None`
    > number of shared leading batch axes
  - `:returns`: `np.ndarray`
    > t
h
e
 
c
o
n
t
r
a
c
t
e
d
 
r
e
s
u
l
t











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/PermutationOps/levi_cevita_dot.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/PermutationOps/levi_cevita_dot.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/PermutationOps/levi_cevita_dot.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/PermutationOps/levi_cevita_dot.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L116?message=Update%20Docs)   
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