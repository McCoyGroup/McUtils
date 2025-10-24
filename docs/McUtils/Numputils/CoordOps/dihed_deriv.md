# <a id="McUtils.Numputils.CoordOps.dihed_deriv">dihed_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L1177)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L1177?message=Update%20Docs)]
</div>

```python
dihed_deriv(coords, i, j, k, l, /, order=1, zero_thresh=None, method='expansion', fixed_atoms=None, expanded_vectors=None): 
```
Gives the derivative of the dihedral between i, j, k, and l with respect to the Cartesians
Currently gives what are sometimes called the `psi` angles.
Can also support more traditional `phi` angles by using a different angle ordering
  - `coords`: `np.ndarray`
    > 
  - `i`: `int | Iterable[int]`
    > 
  - `j`: `int | Iterable[int]`
    > 
  - `k`: `int | Iterable[int]`
    > 
  - `l`: `int | Iterable[int]`
    > 
  - `:returns`: `np.ndarray`
    > d
e
r
i
v
a
t
i
v
e
s
 
o
f
 
t
h
e
 
d
i
h
e
d
r
a
l
 
w
i
t
h
 
r
e
s
p
e
c
t
 
t
o
 
a
t
o
m
s
 
i
,
 
j
,
 
k
,
 
a
n
d
 
l











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/dihed_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/dihed_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/dihed_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/dihed_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L1177?message=Update%20Docs)   
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