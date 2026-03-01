## <a id="McUtils.Plots.Properties.GraphicsPropertyManager">GraphicsPropertyManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties.py#L16?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties.py#L22)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties.py#L22?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.figure_label" class="docs-object-method">&nbsp;</a> 
```python
@property
figure_label(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L48?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.plot_label" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_label(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L62)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L62?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.style_list" class="docs-object-method">&nbsp;</a> 
```python
@property
style_list(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L78)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L78?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.plot_legend" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_legend(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L101)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L101?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.legend_style" class="docs-object-method">&nbsp;</a> 
```python
@property
legend_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L132)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L132?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.axes_labels" class="docs-object-method">&nbsp;</a> 
```python
@property
axes_labels(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L149)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L149?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.plot_range" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_range(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L182)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L182?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.absolute_plot_range" class="docs-object-method">&nbsp;</a> 
```python
@property
absolute_plot_range(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L219)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L219?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.ticks" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L229)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L229?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.ticks_style" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L378)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L378?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.frame_style" class="docs-object-method">&nbsp;</a> 
```python
@property
frame_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L408)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L408?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.clean_tick_label_styles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
clean_tick_label_styles(cls, k): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L445)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L445?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.ticks_label_style" class="docs-object-method">&nbsp;</a> 
```python
@property
ticks_label_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L454)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L454?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.aspect_ratio" class="docs-object-method">&nbsp;</a> 
```python
@property
aspect_ratio(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L476)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L476?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.image_size" class="docs-object-method">&nbsp;</a> 
```python
@property
image_size(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L501)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L501?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.axes_bbox" class="docs-object-method">&nbsp;</a> 
```python
@property
axes_bbox(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L551)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L551?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.background" class="docs-object-method">&nbsp;</a> 
```python
@property
background(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L561)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L561?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.frame" class="docs-object-method">&nbsp;</a> 
```python
@property
frame(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L578)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L578?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.scale" class="docs-object-method">&nbsp;</a> 
```python
@property
scale(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L600)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L600?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding" class="docs-object-method">&nbsp;</a> 
```python
@property
padding(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L629)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L629?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding_left" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_left(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L667)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L667?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding_right" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_right(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L675)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L675?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding_top" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_top(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L683)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L683?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.padding_bottom" class="docs-object-method">&nbsp;</a> 
```python
@property
padding_bottom(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L691)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L691?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.spacings" class="docs-object-method">&nbsp;</a> 
```python
@property
spacings(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L700)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L700?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Properties.GraphicsPropertyManager.colorbar" class="docs-object-method">&nbsp;</a> 
```python
@property
colorbar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L744)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties/GraphicsPropertyManager.py#L744?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Properties.py#L16?message=Update%20Docs)   
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