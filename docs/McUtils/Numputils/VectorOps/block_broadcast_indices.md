# <a id="McUtils.Numputils.VectorOps.block_broadcast_indices">block_broadcast_indices</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L922)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L922?message=Update%20Docs)]
</div>

```python
block_broadcast_indices(base_pos, block_inds, block_size=None): 
```
**LLM Docstring**

Expand a set of base positions into flattened indices spanning a contiguous
block of size `block_size` around each position.

Typically used to turn atom indices into the flattened Cartesian indices
`3 * atom + component`. `block_inds` may be an integer (a full `0..block_inds`
range) or an explicit set of offsets (in which case `block_size` is required).
  - `base_pos`: `np.ndarray`
    > the base positions (e.g. atom indices)
  - `block_inds`: `int | np.ndarray`
    > block offsets, or an int giving the block width
  - `block_size`: `int | None`
    > stride between base positions (required if offsets given)
  - `:returns`: `np.ndarray`
    > t
h
e
 
f
l
a
t
t
e
n
e
d
 
b
l
o
c
k
 
i
n
d
i
c
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/block_broadcast_indices.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/block_broadcast_indices.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/block_broadcast_indices.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/block_broadcast_indices.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L922?message=Update%20Docs)   
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