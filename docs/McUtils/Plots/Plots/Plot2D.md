## <a id="McUtils.Plots.Plots.Plot2D">Plot2D</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots.py#L890)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots.py#L890?message=Update%20Docs)]
</div>

A base class for plots of 3D data but plotted on 2D axes







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
known_styles: set
method: str
```
<a id="McUtils.Plots.Plots.Plot2D.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *params, plot_style=None, colorbar=None, figure=None, axes=None, subplot_kw=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots.py#L898)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots.py#L898?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Plots/Plot2D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Plots/Plot2D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Plots/Plot2D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Plots/Plot2D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots.py#L890?message=Update%20Docs)   
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