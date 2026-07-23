## <a id="McUtils.Plots.Plots.Plot">Plot</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots.py#L268)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots.py#L268?message=Update%20Docs)]
</div>

The base plotting class to interface into matplotlib or (someday 3D) VTK.
In the future hopefully we'll be able to make a general-purpose `PlottingBackend` class that doesn't need to be `matplotlib` .
Builds off of the `Graphics` class to make a unified and convenient interface to generating plots.
Some sophisticated legwork unfortunately has to be done vis-a-vis tracking constructed lines and other plotting artefacts,
since `matplotlib` is designed to infuriate.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
line_params: set
patch_parms: set
opt_keys: set
default_plot_style: dict
default_colormap: str
style_mapping: dict
known_styles: set
method: str
known_keys: set
plot_classes: dict
```
<a id="McUtils.Plots.Plots.Plot.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *params, method=None, figure=None, axes=None, subplot_kw=None, plot_style=None, theme=None, display_format=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots.py#L300)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots.py#L300?message=Update%20Docs)]
</div>

  - `params`: `Any`
    > _empty_ or _x_, _y_ arrays or _function_, _xrange_
  - `plot_style`: `dict | None`
    > the plot styling options to be fed into the plot method
  - `method`: `str | function`
    > the method name as a string or functional form of the method to plot
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


<a id="McUtils.Plots.Plots.Plot.filter_options" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
filter_options(cls, opts, allowed=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L367)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L367?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the subset of options recognized by this plot type (its known styles and
keys, or an explicit allowed set).
  - `opts`: `dict`
    > the options to filter
  - `allowed`: `set | None`
    > an explicit allowed-key set
  - `:returns`: `dict`
    > the filtered options


<a id="McUtils.Plots.Plots.Plot.prep_styles" class="docs-object-method">&nbsp;</a> 
```python
prep_styles(self, c=None, edgecolors=None, facecolors=None, cmap=None, prep_colors=False, color_value_rescaling=True, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots/Plot.py#L440)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots/Plot.py#L440?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize color-related styling: when a colormap is supplied and color values are
numeric, rescale them and map them through the colormap (into `c`, `facecolors`,
or `edgecolors`), returning the cleaned style dict.
  - `c`: `Any`
    > the point colors/values
  - `edgecolors`: `Any`
    > the edge colors/values
  - `facecolors`: `Any`
    > the face colors/values
  - `cmap`: `Any`
    > the colormap (name, dict spec, or callable)
  - `prep_colors`: `bool`
    > actually map numeric values through the colormap
  - `color_value_rescaling`: `bool`
    > rescale numeric color values before mapping
  - `styles`: `Any`
    > the remaining styling options
  - `:returns`: `dict`
    > the prepared style dict


<a id="McUtils.Plots.Plots.Plot.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, *params, insert_default_styles=True, **plot_style): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots/Plot.py#L510)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots/Plot.py#L510?message=Update%20Docs)]
</div>
Plots a set of data & stores the result
  - `:returns`: `_`
    > the graphics that matplotlib made


<a id="McUtils.Plots.Plots.Plot.artists" class="docs-object-method">&nbsp;</a> 
```python
@property
artists(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots/Plot.py#L529)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots/Plot.py#L529?message=Update%20Docs)]
</div>
**LLM Docstring**

The backend artist objects produced by the plot (as a list).
  - `:returns`: `list | None`
    > the artists


<a id="McUtils.Plots.Plots.Plot.clear" class="docs-object-method">&nbsp;</a> 
```python
clear(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots/Plot.py#L557)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots/Plot.py#L557?message=Update%20Docs)]
</div>
Removes the plotted data


<a id="McUtils.Plots.Plots.Plot.restyle" class="docs-object-method">&nbsp;</a> 
```python
restyle(self, **plot_style): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots/Plot.py#L564)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots/Plot.py#L564?message=Update%20Docs)]
</div>
Replots the data with updated plot styling
  - `plot_style`: `Any`
    >


<a id="McUtils.Plots.Plots.Plot.data" class="docs-object-method">&nbsp;</a> 
```python
@property
data(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots/Plot.py#L573)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots/Plot.py#L573?message=Update%20Docs)]
</div>
The data that we plotted


<a id="McUtils.Plots.Plots.Plot.plot_style" class="docs-object-method">&nbsp;</a> 
```python
@property
plot_style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots/Plot.py#L581)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots/Plot.py#L581?message=Update%20Docs)]
</div>
The styling options applied to the plot


<a id="McUtils.Plots.Plots.Plot.add_colorbar" class="docs-object-method">&nbsp;</a> 
```python
add_colorbar(self, graphics=None, norm=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots/Plot.py#L592)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots/Plot.py#L592?message=Update%20Docs)]
</div>
Adds a colorbar to the plot


<a id="McUtils.Plots.Plots.Plot.set_graphics_properties" class="docs-object-method">&nbsp;</a> 
```python
set_graphics_properties(self, *which, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots/Plot.py#L601)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots/Plot.py#L601?message=Update%20Docs)]
</div>
**LLM Docstring**

Set backend properties on the plot's artists (all of them, or the selected
indices).
  - `which`: `Any`
    > the artist indices to modify (all if empty)
  - `kw`: `Any`
    > the properties to set


<a id="McUtils.Plots.Plots.Plot.merge" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
merge(cls, main, other, *rest, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L619)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L619?message=Update%20Docs)]
</div>
**LLM Docstring**

Combine this plot with others into a `CompositePlot`.
  - `main`: `Any`
    > the first plot
  - `other`: `Any`
    > the second plot
  - `rest`: `Any`
    > additional plots
  - `kwargs`: `Any`
    > options for the composite
  - `:returns`: `CompositePlot`
    > the composite plot


<a id="McUtils.Plots.Plots.Plot.resolve_method" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve_method(cls, mpl_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L636)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L636?message=Update%20Docs)]
</div>
**LLM Docstring**

Look up the registered plot class for a backend method name.
  - `mpl_name`: `str`
    > the method/class name
  - `:returns`: `type`
    > the plot class


<a id="McUtils.Plots.Plots.Plot.register" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
register(cls, plot_class): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L652)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L652?message=Update%20Docs)]
</div>
**LLM Docstring**

Register a plot class in the class registry, keyed by its backend method name (or
class name if the method is already registered). Usable as a decorator.
  - `plot_class`: `type`
    > the plot class to register
  - `:returns`: `type`
    > the registered class
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Plots/Plot.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Plots/Plot.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Plots/Plot.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Plots/Plot.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots.py#L268?message=Update%20Docs)   
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