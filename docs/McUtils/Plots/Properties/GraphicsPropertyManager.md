## <a id="McUtils.Plots.Properties.GraphicsPropertyManager">GraphicsPropertyManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties.py#L15?message=Update%20Docs)]
</div>

Manages properties for Graphics objects so that concrete GraphicsBase instances don't need to duplicate code, but
at the same time things that build off of GraphicsBase don't need to implement all of these properties







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
ticks_label_base_styles: set
ticks_label_style_remapping: dict
```
<a id="McUtils.Plots.Properties.GraphicsPropertyManager.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, graphics, figure, axes, managed=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L21)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L21?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.figure_label" class="docs-object-method">&nbsp;</a> 
```python
@property
figure_label(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L46)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L46?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.plot_label" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_label(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L60)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L60?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.plot_legend" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_legend(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L77)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L77?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.legend_style" class="docs-object-method">&nbsp;</a> 
```python
@property
legend_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L106)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L106?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.axes_labels" class="docs-object-method">&nbsp;</a> 
```python
@property
axes_labels(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L123)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L123?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.plot_range" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_range(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L156?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.ticks" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L193)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L193?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.ticks_style" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L258)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L258?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.frame_style" class="docs-object-method">&nbsp;</a> 
```python
@property
frame_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L288)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L288?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.clean_tick_label_styles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
clean_tick_label_styles(cls, k): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L325)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L325?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.ticks_label_style" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks_label_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L334)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L334?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.aspect_ratio" class="docs-object-method">&nbsp;</a> 
```python
@property
aspect_ratio(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L356)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L356?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.image_size" class="docs-object-method">&nbsp;</a> 
```python
@property
image_size(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L381)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L381?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.axes_bbox" class="docs-object-method">&nbsp;</a> 
```python
@property
axes_bbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L431)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L431?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.background" class="docs-object-method">&nbsp;</a> 
```python
@property
background(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L441)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L441?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.frame" class="docs-object-method">&nbsp;</a> 
```python
@property
frame(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L458)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L458?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.scale" class="docs-object-method">&nbsp;</a> 
```python
@property
scale(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L480)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L480?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding" class="docs-object-method">&nbsp;</a> 
```python
@property
padding(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L509)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L509?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding_left" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_left(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L547)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L547?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding_right" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_right(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L555)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L555?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding_top" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_top(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L563)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L563?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding_bottom" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_bottom(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L571)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L571?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.spacings" class="docs-object-method">&nbsp;</a> 
```python
@property
spacings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L580)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L580?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.colorbar" class="docs-object-method">&nbsp;</a> 
```python
@property
colorbar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Properties/GraphicsPropertyManager.py#L624)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties/GraphicsPropertyManager.py#L624?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Properties/GraphicsPropertyManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Properties/GraphicsPropertyManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Properties/GraphicsPropertyManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Properties/GraphicsPropertyManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Properties.py#L15?message=Update%20Docs)   
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