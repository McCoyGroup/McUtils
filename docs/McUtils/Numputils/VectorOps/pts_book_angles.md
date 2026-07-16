# <a id="McUtils.Numputils.VectorOps.pts_book_angles">pts_book_angles</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L1398)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L1398?message=Update%20Docs)]
</div>

```python
pts_book_angles(pts1, pts2, pts3, pts4, crosses=None, norms=None, return_crosses=False, **opts): 
```
**LLM Docstring**

Compute *book* angles from four sets of points.

Builds the three defining edge vectors from the point sets and defers to
`vec_dihedrals`, so the result is the signed angle between the two half-planes
hinged on the shared edge.
  - `pts1`: `np.ndarray`
    > first point set
  - `pts2`: `np.ndarray`
    > second point set (shared hinge)
  - `pts3`: `np.ndarray`
    > third point set
  - `pts4`: `np.ndarray`
    > fourth point set
  - `crosses`: `np.ndarray | None`
    > precomputed cross products (optional)
  - `norms`: `np.ndarray | None`
    > precomputed norms (optional)
  - `return_crosses`: `bool`
    > also return the cross products
  - `opts`: `Any`
    > extra options forwarded to `vec_dihedrals`
  - `:returns`: `np.ndarray | tuple`
    > t
h
e
 
b
o
o
k
 
a
n
g
l
e
s
 
(
p
l
u
s
 
c
r
o
s
s
e
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/pts_book_angles.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/pts_book_angles.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/pts_book_angles.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/pts_book_angles.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L1398?message=Update%20Docs)   
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