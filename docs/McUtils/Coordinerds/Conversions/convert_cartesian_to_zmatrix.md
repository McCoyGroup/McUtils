# <a id="McUtils.Coordinerds.Conversions.convert_cartesian_to_zmatrix">convert_cartesian_to_zmatrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Conversions.py#L42)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Conversions.py#L42?message=Update%20Docs)]
</div>

```python
convert_cartesian_to_zmatrix(coords, *, ordering, use_rad=True, return_derivs=None, order=None, strip_embedding=False, derivative_method='new'): 
```
The ordering should be specified like:

[
[n1],
[n2, n1]
[n3, n1/n2, n1/n2]
[n4, n1/n2/n3, n1/n2/n3, n1/n2/n3]
[n5, ...]
...
]
  - `coords`: `np.ndarray`
    > array of cartesian coordinates
  - `use_rad`: `bool`
    > whether to user radians or not
  - `ordering`: `None or tuple of ints or tuple of tuple of ints`
    > optional ordering parameter for the z-matrix
  - `kw`: `Any`
    > ignored key-word arguments
  - `:returns`: `np.ndarray`
    > z
-
m
a
t
r
i
x
 
c
o
o
r
d
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Conversions/convert_cartesian_to_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Conversions/convert_cartesian_to_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Conversions/convert_cartesian_to_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Conversions/convert_cartesian_to_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Conversions.py#L42?message=Update%20Docs)   
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