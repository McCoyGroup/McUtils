# <a id="McUtils.Numputils.TransformationMatrices.identify_cartesian_transformation_type">identify_cartesian_transformation_type</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TransformationMatrices.py#L1596)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1596?message=Update%20Docs)]
</div>

```python
identify_cartesian_transformation_type(x, max_rotation_order=None): 
```
**LLM Docstring**

Classify each Cartesian transformation as identity, inversion, rotation,
reflection, or improper rotation, extracting its defining data.

The matrix is polar-decomposed to separate scaling from the orthogonal part,
then classified by trace/determinant tests; rotations and improper rotations
additionally yield an axis and (when `max_rotation_order` is given) a rational
angle expressed as a root/order pair.
  - `x`: `np.ndarray`
    > the transformation matrix (or stack)
  - `max_rotation_order`: `int | None`
    > largest rotation order to rationalize angles against
  - `:returns`: `tuple`
    > `
(
s
c
a
l
i
n
g
s
,
 
t
y
p
e
s
,
 
a
x
e
s
,
 
r
o
o
t
s
,
 
o
r
d
e
r
s
)
`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TransformationMatrices/identify_cartesian_transformation_type.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TransformationMatrices/identify_cartesian_transformation_type.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TransformationMatrices/identify_cartesian_transformation_type.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TransformationMatrices/identify_cartesian_transformation_type.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TransformationMatrices.py#L1596?message=Update%20Docs)   
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