# <a id="McUtils.Numputils.SetOps.vector_take_ix">vector_take_ix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/SetOps.py#L840)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/SetOps.py#L840?message=Update%20Docs)]
</div>

```python
vector_take_ix(base_shape, inds, shared=None): 
```
**LLM Docstring**

Build the fancy-index tuple for a broadcasted `take` over a shared batch
prefix.

Broadcasts the supplied indices against the array's leading (non-shared) axes
and hands off to `vector_ix`, so values can be gathered along the trailing axes
while sharing the first `shared` batch axes.
  - `base_shape`: `tuple[int, ...]`
    > the shape of the array being indexed
  - `inds`: `tuple | np.ndarray`
    > the per-axis index arrays
  - `shared`: `int | None`
    > number of shared leading batch axes (inferred if omitted)
  - `:returns`: `tuple`
    > t
h
e
 
b
r
o
a
d
c
a
s
t
e
d
 
i
n
d
e
x
 
t
u
p
l
e











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/SetOps/vector_take_ix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/SetOps/vector_take_ix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/SetOps/vector_take_ix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/SetOps/vector_take_ix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/SetOps.py#L840?message=Update%20Docs)   
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