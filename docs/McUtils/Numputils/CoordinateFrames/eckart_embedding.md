# <a id="McUtils.Numputils.CoordinateFrames.eckart_embedding">eckart_embedding</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordinateFrames.py#L988)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L988?message=Update%20Docs)]
</div>

```python
eckart_embedding(ref, coords, masses=None, sel=None, in_paf=False, planar_ref_tolerance=1e-06, proper_rotation=False, permutable_groups=None, reset_com=True, transform_coordinates=True) -> McUtils.Numputils.CoordinateFrames.EckartData: 
```
**LLM Docstring**

Compute the Eckart embedding that rotates a set of coordinates into maximal
alignment with a reference geometry.

Thin public wrapper over the internal `_eckart_embedding`, forwarding all
options (atom selection, principal-axis handling, planarity tolerance,
proper-rotation constraint, permutable groups, center-of-mass reset, and whether
to actually transform the coordinates).
  - `ref`: `np.ndarray`
    > the reference geometry
  - `coords`: `np.ndarray`
    > the coordinates to embed
  - `masses`: `np.ndarray | None`
    > per-atom masses (defaults to unit masses)
  - `sel`: `Iterable[int] | None`
    > optional subset of atoms used to define the embedding
  - `in_paf`: `bool`
    > whether the inputs are already in the principal-axis frame
  - `planar_ref_tolerance`: `float`
    > tolerance for detecting a planar reference
  - `proper_rotation`: `bool`
    > restrict the embedding to proper rotations
  - `permutable_groups`: `Iterable | None`
    > groups of atoms allowed to permute
  - `reset_com`: `bool`
    > re-center on the center of mass after embedding
  - `transform_coordinates`: `bool`
    > apply the rotation to the coordinates
  - `:returns`: `EckartData`
    > t
h
e
 
E
c
k
a
r
t
 
e
m
b
e
d
d
i
n
g
 
d
a
t
a











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordinateFrames/eckart_embedding.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordinateFrames/eckart_embedding.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordinateFrames/eckart_embedding.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordinateFrames/eckart_embedding.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordinateFrames.py#L988?message=Update%20Docs)   
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