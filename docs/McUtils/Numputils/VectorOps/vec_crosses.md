# <a id="McUtils.Numputils.VectorOps.vec_crosses">vec_crosses</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L408)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L408?message=Update%20Docs)]
</div>

```python
vec_crosses(vecs1, vecs2, normalize=False, zero_thresh=None, axis=-1): 
```
**LLM Docstring**

Compute the cross products of two stacks of vectors, optionally normalizing the
results.

When `normalize` is set the cross products are divided by their norms, with
near-zero norms (below `zero_thresh`, defaulting to `Options.norm_zero_threshold`)
handled safely so the corresponding results are zeroed rather than producing
NaNs.
  - `vecs1`: `np.ndarray`
    > first stack of vectors
  - `vecs2`: `np.ndarray`
    > second stack of vectors
  - `normalize`: `bool`
    > whether to normalize the cross products
  - `zero_thresh`: `float | None`
    > norm below which a result is treated as zero
  - `axis`: `int`
    > axis holding the vector components
  - `:returns`: `np.ndarray`
    > t
h
e
 
(
o
p
t
i
o
n
a
l
l
y
 
n
o
r
m
a
l
i
z
e
d
)
 
c
r
o
s
s
 
p
r
o
d
u
c
t
s











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/vec_crosses.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/vec_crosses.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/vec_crosses.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/vec_crosses.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L408?message=Update%20Docs)   
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