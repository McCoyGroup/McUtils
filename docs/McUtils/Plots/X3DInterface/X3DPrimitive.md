## <a id="McUtils.Plots.X3DInterface.X3DPrimitive">X3DPrimitive</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface.py#L1152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L1152?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
wrapper_class: NoneType
tag_class: NoneType
```
<a id="McUtils.Plots.X3DInterface.X3DPrimitive.get_new_id" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_new_id(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1155)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1155?message=Update%20Docs)]
</div>
**LLM Docstring**

Generate a fresh `x3d-obj-`-prefixed id.
  - `:returns`: `str`
    > the id


<a id="McUtils.Plots.X3DInterface.X3DPrimitive.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *children, id=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface.py#L1166)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L1166?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a primitive holding its child objects and options (under an id).
  - `children`: `Any`
    > the child objects
  - `id`: `Any`
    > the primitive id (auto-generated if omitted)
  - `opts`: `Any`
    > the primitive options


<a id="McUtils.Plots.X3DInterface.X3DPrimitive.id" class="docs-object-method">&nbsp;</a> 
```python
@property
id(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DPrimitive.py#L1183)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DPrimitive.py#L1183?message=Update%20Docs)]
</div>
**LLM Docstring**

The primitive's id.
  - `:returns`: `str`
    > the id


<a id="McUtils.Plots.X3DInterface.X3DPrimitive.split_opts" class="docs-object-method">&nbsp;</a> 
```python
split_opts(self, opts: 'dict'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DPrimitive.py#L1205)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DPrimitive.py#L1205?message=Update%20Docs)]
</div>
**LLM Docstring**

Split options into the non-appearance options and the material/appearance/line/point options.
  - `opts`: `dict`
    > the options
  - `:returns`: `tuple`
    > `(object_opts, appearance_opts)`


<a id="McUtils.Plots.X3DInterface.X3DPrimitive.get_appearance" class="docs-object-method">&nbsp;</a> 
```python
get_appearance(self, appearance_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DPrimitive.py#L1224)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DPrimitive.py#L1224?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the appearance node from the appearance options (or `None` if there are none).
  - `appearance_options`: `dict`
    > the appearance options
  - `:returns`: `_`
    > the appearance element (or `None`)


<a id="McUtils.Plots.X3DInterface.X3DPrimitive.to_x3d" class="docs-object-method">&nbsp;</a> 
```python
to_x3d(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DPrimitive.py#L1238)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DPrimitive.py#L1238?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the primitive to its X3D DOM element, wrapping its children and appearance under the tag/wrapper classes.
  - `:returns`: `_`
    > the X3D element


<a id="McUtils.Plots.X3DInterface.X3DPrimitive.resolve_prop_attr" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_prop_attr(self, prop_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1264)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1264?message=Update%20Docs)]
</div>
**LLM Docstring**

Map a property name to its attribute, routing appearance properties through the appearance node.
  - `prop_name`: `Any`
    > the property name
  - `:returns`: `_`
    > the attribute name


<a id="McUtils.Plots.X3DInterface.X3DPrimitive.get_prop_node_id" class="docs-object-method">&nbsp;</a> 
```python
get_prop_node_id(self, prop_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DPrimitive.py#L1285)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DPrimitive.py#L1285?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the node id carrying a property, routing appearance properties to the appearance node.
  - `prop_name`: `Any`
    > the property name
  - `:returns`: `str`
    > the node id


<a id="McUtils.Plots.X3DInterface.X3DPrimitive.get_children" class="docs-object-method">&nbsp;</a> 
```python
get_children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3DPrimitive.py#L1305)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3DPrimitive.py#L1305?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the primitive's child objects.
  - `:returns`: `list`
    > the children
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/X3DInterface/X3DPrimitive.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/X3DInterface/X3DPrimitive.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/X3DInterface/X3DPrimitive.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/X3DInterface/X3DPrimitive.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L1152?message=Update%20Docs)   
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