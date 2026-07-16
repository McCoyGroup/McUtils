# <a id="McUtils.Numputils.VectorOps.vec_rescale">vec_rescale</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L345)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L345?message=Update%20Docs)]
</div>

```python
vec_rescale(vecs, target_range=None, cur_range=None, midpoint=None, axis=-1, clip=False): 
```
**LLM Docstring**

Linearly rescale values from their current range onto a target range.

The current range is inferred from the data (optionally symmetrized about
`midpoint`) unless supplied explicitly. Values are mapped to `[0, 1]` and then
onto `target_range` (a scalar upper bound or a `(min, max)` pair), with optional
clipping to the target interval.
  - `vecs`: `np.ndarray`
    > the values to rescale
  - `target_range`: `float | tuple | None`
    > destination range (scalar max, or `(min, max)`)
  - `cur_range`: `tuple | None`
    > explicit source range `(min, max)` (inferred if omitted)
  - `midpoint`: `float | None`
    > value to symmetrize the inferred source range about
  - `axis`: `int`
    > axis along which to infer the range
  - `clip`: `bool`
    > whether to clip the result to the target range
  - `:returns`: `np.ndarray`
    > t
h
e
 
r
e
s
c
a
l
e
d
 
v
a
l
u
e
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/vec_rescale.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/vec_rescale.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/vec_rescale.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/vec_rescale.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L345?message=Update%20Docs)   
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