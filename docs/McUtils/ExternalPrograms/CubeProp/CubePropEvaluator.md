## <a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator">CubePropEvaluator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp.py#L11)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp.py#L11?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, origin, axes, steps, values, base_data=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp.py#L12)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp.py#L12?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.from_file" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_file(cls, file, **interpolation_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L24)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L24?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.element_volume" class="docs-object-method">&nbsp;</a> 
```python
@property
element_volume(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L30)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L30?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.coords_from_grid" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
coords_from_grid(cls, origin, axes, steps): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L36)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L36?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.grid_coords" class="docs-object-method">&nbsp;</a> 
```python
@property
grid_coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L51)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L51?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.get_value_interpolator" class="docs-object-method">&nbsp;</a> 
```python
get_value_interpolator(self, steps, values, **interpolation_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L57)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L57?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.interpolator" class="docs-object-method">&nbsp;</a> 
```python
@property
interpolator(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L65)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L65?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.inverse_axes" class="docs-object-method">&nbsp;</a> 
```python
@property
inverse_axes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L71)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L71?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.embed_points" class="docs-object-method">&nbsp;</a> 
```python
embed_points(self, points): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L76)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L76?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.unembed_points" class="docs-object-method">&nbsp;</a> 
```python
unembed_points(self, points): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L80)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L80?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.evaluate" class="docs-object-method">&nbsp;</a> 
```python
evaluate(self, points): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L83)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L83?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.CubeProp.CubePropEvaluator.get_isosurface" class="docs-object-method">&nbsp;</a> 
```python
get_isosurface(self, isoval, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L86)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.py#L86?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/CubeProp/CubePropEvaluator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/CubeProp.py#L11?message=Update%20Docs)   
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