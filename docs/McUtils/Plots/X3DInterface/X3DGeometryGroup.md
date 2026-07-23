## <a id="McUtils.Plots.X3DInterface.X3DGeometryGroup">X3DGeometryGroup</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface.py#L1716)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L1716?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Plots.X3DInterface.X3DGeometryGroup.prep_geometry_opts" class="docs-object-method">&nbsp;</a> 
```python
prep_geometry_opts(self, *args, **opts) -> 'list[dict]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryGroup.py#L1717)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryGroup.py#L1717?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: build a list of per-instance geometry option dicts for this (possibly batched) shape.
  - `args`: `Any`
    > the shape arguments
  - `opts`: `Any`
    > extra options
  - `:returns`: `list`
    > the per-instance geometry options


<a id="McUtils.Plots.X3DInterface.X3DGeometryGroup.get_interpolated_attributes" class="docs-object-method">&nbsp;</a> 
```python
get_interpolated_attributes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryGroup.py#L1730)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryGroup.py#L1730?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the first instance's geometry plus material attributes used for animation.
  - `:returns`: `dict`
    > the attributes


<a id="McUtils.Plots.X3DInterface.X3DGeometryGroup.prep_vecs" class="docs-object-method">&nbsp;</a> 
```python
prep_vecs(self, vecs, nstruct=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryGroup.py#L1740)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryGroup.py#L1740?message=Update%20Docs)]
</div>
**LLM Docstring**

Broadcast a vector (or `None`) across `nstruct` instances.
  - `vecs`: `Any`
    > the vector(s) (or `None`)
  - `nstruct`: `int | None`
    > the number of instances
  - `:returns`: `np.ndarray | list`
    > the per-instance vectors


<a id="McUtils.Plots.X3DInterface.X3DGeometryGroup.prep_mats" class="docs-object-method">&nbsp;</a> 
```python
prep_mats(self, mats, nstruct=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryGroup.py#L1761)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryGroup.py#L1761?message=Update%20Docs)]
</div>
**LLM Docstring**

Broadcast a matrix (or `None`) across `nstruct` instances.
  - `mats`: `Any`
    > the matrix/matrices (or `None`)
  - `nstruct`: `int | None`
    > the number of instances
  - `:returns`: `np.ndarray | list`
    > the per-instance matrices


<a id="McUtils.Plots.X3DInterface.X3DGeometryGroup.prep_const" class="docs-object-method">&nbsp;</a> 
```python
prep_const(self, const, nstruct): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryGroup.py#L1782)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryGroup.py#L1782?message=Update%20Docs)]
</div>
**LLM Docstring**

Broadcast a scalar constant (or `None`) across `nstruct` instances.
  - `const`: `Any`
    > the constant (or `None`)
  - `nstruct`: `int`
    > the number of instances
  - `:returns`: `np.ndarray | list`
    > the per-instance constants


<a id="McUtils.Plots.X3DInterface.X3DGeometryGroup.to_x3d" class="docs-object-method">&nbsp;</a> 
```python
to_x3d(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryGroup.py#L1802)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryGroup.py#L1802?message=Update%20Docs)]
</div>
**LLM Docstring**

Render every instance to its X3D element (wrapped in appearance/transform), grouping them under a single group node.
  - `:returns`: `_`
    > the X3D element
 </div>
</div>












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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/X3DInterface/X3DGeometryGroup.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/X3DInterface/X3DGeometryGroup.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/X3DInterface/X3DGeometryGroup.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/X3DInterface/X3DGeometryGroup.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L1716?message=Update%20Docs)   
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