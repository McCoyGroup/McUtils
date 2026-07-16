# <a id="McUtils.Numputils.SetOps.group_indices">group_indices</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/SetOps.py#L570)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/SetOps.py#L570?message=Update%20Docs)]
</div>

```python
group_indices(keys, sorting=None, return_sizes=None, return_indices=None): 
```
**LLM Docstring**

Group the positional indices `0..len(keys)-1` by their key values.

Convenience wrapper over `group_by` that groups a plain `arange` by `keys`.
  - `keys`: `np.ndarray`
    > the keys to group by
  - `sorting`: `np.ndarray | None`
    > precomputed sorting of the keys
  - `return_sizes`: `bool | None`
    > also return per-group sizes
  - `return_indices`: `bool | None`
    > also return grouping indices
  - `:returns`: `tuple`
    > t
h
e
 
g
r
o
u
p
e
d
 
i
n
d
i
c
e
s
 
(
p
l
u
s
 
e
x
t
r
a
s
 
i
f
 
r
e
q
u
e
s
t
e
d
)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/SetOps/group_indices.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/SetOps/group_indices.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/SetOps/group_indices.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/SetOps/group_indices.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/SetOps.py#L570?message=Update%20Docs)   
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