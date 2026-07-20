## <a id="McUtils.Plots.X3DInterface.X3DGeometryObject">X3DGeometryObject</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface.py#L1546)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L1546?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
wrapper_class: Shape
transform_props: tuple
```
<a id="McUtils.Plots.X3DInterface.X3DGeometryObject.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *args, id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface.py#L1548)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L1548?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a geometry object, splitting the material options out and preparing the geometry options.
  - `args`: `Any`
    > the geometry-defining arguments
  - `id`: `Any`
    > the object id
  - `opts`: `Any`
    > the geometry and material options


<a id="McUtils.Plots.X3DInterface.X3DGeometryObject.get_interpolated_attributes" class="docs-object-method">&nbsp;</a> 
```python
get_interpolated_attributes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1561)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1561?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the geometry plus material attributes used for animation.
  - `:returns`: `dict`
    > the attributes


<a id="McUtils.Plots.X3DInterface.X3DGeometryObject.prep_geometry_opts" class="docs-object-method">&nbsp;</a> 
```python
prep_geometry_opts(self, *args, **opts) -> 'dict': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1571)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1571?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: build the geometry options for this shape from its defining arguments.
  - `args`: `Any`
    > the shape arguments
  - `opts`: `Any`
    > extra options
  - `:returns`: `dict`
    > the geometry options


<a id="McUtils.Plots.X3DInterface.X3DGeometryObject.create_tag_object" class="docs-object-method">&nbsp;</a> 
```python
create_tag_object(self, **core_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1584)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1584?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the core geometry tag element from the core options.
  - `core_opts`: `Any`
    > the core geometry options
  - `:returns`: `_`
    > the geometry element


<a id="McUtils.Plots.X3DInterface.X3DGeometryObject.create_object" class="docs-object-method">&nbsp;</a> 
```python
create_object(self, translation=None, rotation=None, scale=None, normal=None, up_vector=None, bbox_center=None, **core_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1594)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1594?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the geometry element together with its transform (translation/rotation/
scale), computing the rotation needed to align the shape's up-vector with a
supplied normal.
  - `translation`: `Any`
    > the translation
  - `rotation`: `Any`
    > the base rotation (axis-angle)
  - `scale`: `Any`
    > the scale
  - `normal`: `Any`
    > a normal to orient the shape toward
  - `up_vector`: `Any`
    > the shape's reference up-vector
  - `bbox_center`: `Any`
    > the bounding-box center
  - `core_opts`: `Any`
    > the core geometry options
  - `:returns`: `tuple`
    > `(geometry_element, transform_dict_or_None)`


<a id="McUtils.Plots.X3DInterface.X3DGeometryObject.get_rotation" class="docs-object-method">&nbsp;</a> 
```python
get_rotation(self, axis, up_vector=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1651)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1651?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the axis-angle rotation that aligns an up-vector with a target axis (and the axis norm).
  - `axis`: `Any`
    > the target axis
  - `up_vector`: `Any`
    > the reference up-vector
  - `:returns`: `tuple`
    > `(axis_angle_rotation, axis_norm)`


<a id="McUtils.Plots.X3DInterface.X3DGeometryObject.get_prop_node_id" class="docs-object-method">&nbsp;</a> 
```python
get_prop_node_id(self, prop_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1671)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1671?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the node id carrying a property, routing transform properties to the transform node.
  - `prop_name`: `Any`
    > the property name
  - `:returns`: `str`
    > the node id


<a id="McUtils.Plots.X3DInterface.X3DGeometryObject.to_x3d" class="docs-object-method">&nbsp;</a> 
```python
to_x3d(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1685)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DGeometryObject.py#L1685?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the geometry to its X3D DOM element, wrapping it in its appearance and transform.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/X3DInterface/X3DGeometryObject.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/X3DInterface/X3DGeometryObject.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/X3DInterface/X3DGeometryObject.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/X3DInterface/X3DGeometryObject.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L1546?message=Update%20Docs)   
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