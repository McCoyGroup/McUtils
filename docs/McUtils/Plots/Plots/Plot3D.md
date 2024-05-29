## <a id="McUtils.Plots.Plots.Plot3D">Plot3D</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Plots.py#L1041)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Plots.py#L1041?message=Update%20Docs)]
</div>

A base class for 3D plots







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_plot_style: dict
style_mapping: dict
known_styles: set
method: str
plot_classes: dict
```
<a id="McUtils.Plots.Plots.Plot3D.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *params, plot_style=None, method=None, colorbar=None, figure=None, axes=None, subplot_kw=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Plots/Plot3D.py#L1048)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Plots/Plot3D.py#L1048?message=Update%20Docs)]
</div>

  - `params`: `Any`
    > either _empty_ or _x_, _y_, _z_ arrays or _function_, _xrange_, _yrange_
  - `plot_style`: `dict | None`
    > the plot styling options to be fed into the plot method
  - `method`: `str`
    > the method name as a string
  - `figure`: `Graphics | None`
    > the Graphics object on which to plot (None means make a new one)
  - `axes`: `None`
    > the axes on which to plot (used in constructing a Graphics, None means make a new one)
  - `subplot_kw`: `dict | None`
    > the keywords to pass on when initializing the plot
  - `colorbar`: `None | bool | dict`
    > whether to use a colorbar or what options to pass to the colorbar
  - `opts`: `Any`
    > options to be fed in when initializing the Graphics


<a id="McUtils.Plots.Plots.Plot3D.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, *params, **plot_style): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Plots/Plot3D.py#L1117)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Plots/Plot3D.py#L1117?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Plots.Plot3D.add_colorbar" class="docs-object-method">&nbsp;</a> 
```python
add_colorbar(self, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Plots/Plot3D.py#L1123)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Plots/Plot3D.py#L1123?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Plots.Plot3D.resolve_method" class="docs-object-method">&nbsp;</a> 
```python
resolve_method(mpl_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Plots/Plot3D.py#L1131)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Plots/Plot3D.py#L1131?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Plots.Plot3D.register" class="docs-object-method">&nbsp;</a> 
```python
register(plot_class): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Plots/Plot3D.py#L1137)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Plots/Plot3D.py#L1137?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Plots/Plots/Plot3D.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Plots/Plots/Plot3D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Plots/Plots/Plot3D.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Plots/Plots/Plot3D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Plots.py#L1041?message=Update%20Docs)   
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