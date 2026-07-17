# <a id="McUtils.Coordinerds.ZMatrices.zmatrix_unit_convert">zmatrix_unit_convert</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L44)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L44?message=Update%20Docs)]
</div>

```python
zmatrix_unit_convert(zmat, distance_conversion, angle_conversion=None, rad2deg=False, deg2rad=False): 
```
**LLM Docstring**

Scale the distance and angular columns of a Z-matrix value array.

A copy is made when `np.asanyarray` returns the original object. Column 0 is multiplied by `distance_conversion`. Columns 1 and 2 are multiplied by `angle_conversion` when supplied; otherwise they are optionally converted between degrees and radians.
  - `zmat`: `array-like`
    > Z-matrix values whose final two axes are atoms by `(distance, angle, dihedral)`.
  - `distance_conversion`: `float`
    > Multiplicative factor applied to all distances.
  - `angle_conversion`: `float | None`
    > Multiplicative factor applied to bends and dihedrals. When omitted, `rad2deg` or `deg2rad` controls angular conversion.
  - `rad2deg`: `bool`
    > Convert angular columns from radians to degrees when `angle_conversion` is omitted.
  - `deg2rad`: `bool`
    > Convert angular columns from degrees to radians when `angle_conversion` is omitted.
  - `:returns`: `np.ndarray`
    > Converted Z-matrix values, without modifying the input array in place.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/zmatrix_unit_convert.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/zmatrix_unit_convert.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/zmatrix_unit_convert.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/zmatrix_unit_convert.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L44?message=Update%20Docs)   
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