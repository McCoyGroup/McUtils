# <a id="McUtils.Numputils.TransformationMatrices.find_coordinate_matching_permutation">find_coordinate_matching_permutation</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TransformationMatrices.py#L1371)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1371?message=Update%20Docs)]
</div>

```python
find_coordinate_matching_permutation(coords, new_coords, return_row_ordering=False, tol=None): 
```
**LLM Docstring**

Find the permutation that best matches one set of coordinates to another by
iterative nearest-neighbour assignment.

Builds the coordinate distance matrix and greedily pairs up the closest
remaining atoms, optionally enforcing a maximum-deviation `tol`. Either the
combined column permutation or the separate row/column orderings can be returned.
  - `coords`: `np.ndarray`
    > the source coordinates
  - `new_coords`: `np.ndarray`
    > the target coordinates
  - `return_row_ordering`: `bool`
    > return separate row/column orderings
  - `tol`: `float | None`
    > maximum allowed matching deviation (raises if exceeded)
  - `:returns`: `np.ndarray | tuple`
    > t
h
e
 
m
a
t
c
h
i
n
g
 
p
e
r
m
u
t
a
t
i
o
n
 
(
o
r
 
t
h
e
 
r
o
w
/
c
o
l
u
m
n
 
o
r
d
e
r
i
n
g
s
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TransformationMatrices/find_coordinate_matching_permutation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TransformationMatrices/find_coordinate_matching_permutation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TransformationMatrices/find_coordinate_matching_permutation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TransformationMatrices/find_coordinate_matching_permutation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1371?message=Update%20Docs)   
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