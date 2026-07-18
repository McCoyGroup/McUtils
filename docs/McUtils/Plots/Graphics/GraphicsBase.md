## <a id="McUtils.Plots.Graphics.GraphicsBase">GraphicsBase</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics.py#L154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics.py#L154?message=Update%20Docs)]
</div>

The base class for all things Graphics
Defines the common parts of the interface







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
opt_keys: set
layout_keys: set
known_keys: set
axes_params: set
inset_options: dict
axes_keys: set
```
<a id="McUtils.Plots.Graphics.GraphicsBase.get_raw_attr" class="docs-object-method">&nbsp;</a> 
```python
get_raw_attr(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L204)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L204?message=Update%20Docs)]
</div>
**LLM Docstring**

Read the stored (underscore-prefixed) value for an option, checking the object
itself and then its property manager.
  - `key`: `str`
    > the option name
  - `:returns`: `_`
    > the stored value


<a id="McUtils.Plots.Graphics.GraphicsBase.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *args, name=None, figure=None, tighten=False, axes=None, subplot_kw=None, parent=None, image_size=None, padding=None, aspect_ratio=None, interactive=None, reshowable=None, backend='matplotlib', backend_options=None, theme=None, prop_manager=<class 'McUtils.Plots.Properties.GraphicsPropertyManager'>, theme_manager=<class 'McUtils.Plots.Styling.ThemeManager'>, managed=None, strict=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics.py#L321)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics.py#L321?message=Update%20Docs)]
</div>

  - `args`: `Any`
    > 
  - `figure`: `GraphicsFigure | None`
    > 
  - `axes`: `GraphicsAxes | None`
    > 
  - `subplot_kw`: `dict | None`
    > 
  - `parent`: `GraphicsBase | None`
    > 
  - `opts`: `Any`
    >


<a id="McUtils.Plots.Graphics.GraphicsBase.initialize_figure_and_axes" class="docs-object-method">&nbsp;</a> 
```python
initialize_figure_and_axes(self, figure, axes, *args, **kw) -> 'tuple[GraphicsFigure, GraphicsAxes]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L468)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L468?message=Update%20Docs)]
</div>
Initializes the subplots for the Graphics object
  - `figure`: `Any`
    > 
  - `axes`: `Any`
    > 
  - `args`: `Any`
    > 
  - `kw`: `Any`
    > 
  - `:returns`: `GraphicsFigure, GraphicsAxes`
    > figure, axes


<a id="McUtils.Plots.Graphics.GraphicsBase.parent" class="docs-object-method">&nbsp;</a> 
```python
@property
parent(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L510)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L510?message=Update%20Docs)]
</div>
**LLM Docstring**

The owning graphics object for this figure/axes (self if this is the parent).
  - `:returns`: `GraphicsBase`
    > the parent graphics


<a id="McUtils.Plots.Graphics.GraphicsBase.figure_parent" class="docs-object-method">&nbsp;</a> 
```python
@property
figure_parent(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L524)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L524?message=Update%20Docs)]
</div>
**LLM Docstring**

The graphics object that owns this object's backend figure.
  - `:returns`: `GraphicsBase`
    > the figure's owner


<a id="McUtils.Plots.Graphics.GraphicsBase.inset" class="docs-object-method">&nbsp;</a> 
```python
@property
inset(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L535)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L535?message=Update%20Docs)]
</div>
**LLM Docstring**

Whether this graphics object is an inset (its axes differ from the figure
parent's axes and it isn't managed).
  - `:returns`: `bool`
    > whether it's an inset


<a id="McUtils.Plots.Graphics.GraphicsBase.children" class="docs-object-method">&nbsp;</a> 
```python
@property
children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L548)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L548?message=Update%20Docs)]
</div>
**LLM Docstring**

The child graphics registered against this object's figure/axes (or `None` if
this isn't the parent).
  - `:returns`: `_`
    > the child graphics


<a id="McUtils.Plots.Graphics.GraphicsBase.event_handlers" class="docs-object-method">&nbsp;</a> 
```python
@property
event_handlers(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L566)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L566?message=Update%20Docs)]
</div>
**LLM Docstring**

The bound event-handler data, if any.
  - `:returns`: `_`
    > the event handlers


<a id="McUtils.Plots.Graphics.GraphicsBase.animated" class="docs-object-method">&nbsp;</a> 
```python
@property
animated(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L581)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L581?message=Update%20Docs)]
</div>
**LLM Docstring**

The animation specification for this figure.
  - `:returns`: `_`
    > the animation spec


<a id="McUtils.Plots.Graphics.GraphicsBase.bind_events" class="docs-object-method">&nbsp;</a> 
```python
bind_events(self, *handlers, **events): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L592)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L592?message=Update%20Docs)]
</div>
**LLM Docstring**

Bind interactive event handlers to the figure.
  - `handlers`: `Any`
    > a handlers dict (or handler pairs)
  - `events`: `Any`
    > additional event-name/handler keyword pairs


<a id="McUtils.Plots.Graphics.GraphicsBase.create_animation" class="docs-object-method">&nbsp;</a> 
```python
create_animation(self, *args, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L614)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L614?message=Update%20Docs)]
</div>
**LLM Docstring**

Create (and start) an animator for the figure from the given frame
specification.
  - `args`: `Any`
    > the animation frames/spec
  - `opts`: `Any`
    > options for the animator


<a id="McUtils.Plots.Graphics.GraphicsBase.animate_frames" class="docs-object-method">&nbsp;</a> 
```python
animate_frames(self, frames, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L631)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L631?message=Update%20Docs)]
</div>
**LLM Docstring**

Prepare the figure and animate the supplied frames via the backend.
  - `frames`: `Any`
    > the animation frames
  - `opts`: `Any`
    > animation options
  - `:returns`: `_`
    > the animation


<a id="McUtils.Plots.Graphics.GraphicsBase.set_options" class="docs-object-method">&nbsp;</a> 
```python
set_options(self, event_handlers=None, animated=None, prolog=None, epilog=None, strict=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L660)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L660?message=Update%20Docs)]
</div>
Sets options for the plot
  - `event_handlers`: `Any`
    > 
  - `animated`: `Any`
    > 
  - `opts`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Plots.Graphics.GraphicsBase.prolog" class="docs-object-method">&nbsp;</a> 
```python
@property
prolog(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L693)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L693?message=Update%20Docs)]
</div>
**LLM Docstring**

The prolog graphics primitives drawn before the main content. Setting it records
the change for copying.
  - `:returns`: `_`
    > the prolog primitives


<a id="McUtils.Plots.Graphics.GraphicsBase.epilog" class="docs-object-method">&nbsp;</a> 
```python
@property
epilog(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L718)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L718?message=Update%20Docs)]
</div>
**LLM Docstring**

The epilog graphics primitives drawn after the main content. Setting it records
the change for copying.
  - `:returns`: `_`
    > the epilog primitives


<a id="McUtils.Plots.Graphics.GraphicsBase.opts" class="docs-object-method">&nbsp;</a> 
```python
@property
opts(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L743)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L743?message=Update%20Docs)]
</div>
**LLM Docstring**

The current values of the tracked `opt_keys` options, as a dict.
  - `:returns`: `dict`
    > the options dict


<a id="McUtils.Plots.Graphics.GraphicsBase.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L767)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L767?message=Update%20Docs)]
</div>
Creates a copy of the object with new axes and a new figure
  - `:returns`: `_`
    >


<a id="McUtils.Plots.Graphics.GraphicsBase.change_figure" class="docs-object-method">&nbsp;</a> 
```python
change_figure(self, new, *init_args, figs=None, **init_kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L794)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L794?message=Update%20Docs)]
</div>
Creates a copy of the object with new axes and a new figure
  - `:returns`: `_`
    >


<a id="McUtils.Plots.Graphics.GraphicsBase.prep_show" class="docs-object-method">&nbsp;</a> 
```python
prep_show(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L870)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L870?message=Update%20Docs)]
</div>
**LLM Docstring**

Prepare the whole figure tree (parent and children) for display.
  - `:returns`: `GraphicsBase`
    > self


<a id="McUtils.Plots.Graphics.GraphicsBase.show" class="docs-object-method">&nbsp;</a> 
```python
show(self, reshow=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L889)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L889?message=Update%20Docs)]
</div>
**LLM Docstring**

Display the figure, preparing it first and (temporarily) enabling interactivity
as needed; makes a copy if the figure was already shown and isn't reshowable.
  - `reshow`: `bool | None`
    > force a reshow of an already-shown figure
  - `:returns`: `_`
    > the backend's show result


<a id="McUtils.Plots.Graphics.GraphicsBase.close" class="docs-object-method">&nbsp;</a> 
```python
close(self, force=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L922)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L922?message=Update%20Docs)]
</div>
**LLM Docstring**

Close the figure (or remove the inset axes), cleaning up the figure registration
when this object owns it.
  - `force`: `bool`
    > close even if this object isn't the registered owner


<a id="McUtils.Plots.Graphics.GraphicsBase.__del__" class="docs-object-method">&nbsp;</a> 
```python
__del__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L948)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L948?message=Update%20Docs)]
</div>
**LLM Docstring**

Close the figure on garbage collection (ignoring teardown errors).


<a id="McUtils.Plots.Graphics.GraphicsBase.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L959)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L959?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation showing the type, name/id, and backing figure.
  - `:returns`: `str`
    > the representation


<a id="McUtils.Plots.Graphics.GraphicsBase.clear" class="docs-object-method">&nbsp;</a> 
```python
clear(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L975)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L975?message=Update%20Docs)]
</div>
**LLM Docstring**

Clear the drawn content from the axes.


<a id="McUtils.Plots.Graphics.GraphicsBase.get_mime_bundle" class="docs-object-method">&nbsp;</a> 
```python
get_mime_bundle(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L1008)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L1008?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the figure's MIME bundle (HTML or PNG) for rich display.
  - `:returns`: `dict`
    > the MIME bundle


<a id="McUtils.Plots.Graphics.GraphicsBase.savefig" class="docs-object-method">&nbsp;</a> 
```python
savefig(self, where, expanduser=True, format=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L1019)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L1019?message=Update%20Docs)]
</div>
Saves the image to file
  - `where`: `Any`
    > 
  - `format`: `Any`
    > 
  - `kw`: `Any`
    > 
  - `:returns`: `str`
    > file it was saved to (I think...?)


<a id="McUtils.Plots.Graphics.GraphicsBase.to_png" class="docs-object-method">&nbsp;</a> 
```python
to_png(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L1039)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L1039?message=Update%20Docs)]
</div>
Used by Jupyter and friends to make a version of the image that they can display, hence the extra 'tight_layout' call
  - `:returns`: `_`
    >


<a id="McUtils.Plots.Graphics.GraphicsBase.to_widget" class="docs-object-method">&nbsp;</a> 
```python
to_widget(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L1057)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L1057?message=Update%20Docs)]
</div>
**LLM Docstring**

Prepare the figure and return it as an interactive backend widget.
  - `:returns`: `_`
    > the widget


<a id="McUtils.Plots.Graphics.GraphicsBase.create_colorbar_axis" class="docs-object-method">&nbsp;</a> 
```python
create_colorbar_axis(self, figure=None, size=(20, 200), tick_padding=40, origin=None, orientation='vertical', alignment=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L1080)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L1080?message=Update%20Docs)]
</div>
**LLM Docstring**

Create an inset axis positioned to hold a colorbar, expanding the figure padding
(and compensating the panel spacings) so the colorbar fits.
  - `figure`: `Any`
    > the figure to add the axis to (defaults to this one)
  - `size`: `Any`
    > the colorbar `(width, height)` (fractional if < 1)
  - `tick_padding`: `Any`
    > extra space for the colorbar ticks
  - `origin`: `Any`
    > the colorbar origin (auto-placed if omitted)
  - `orientation`: `str`
    > `'vertical'` or `'horizontal'`
  - `alignment`: `Any`
    > the origin alignment within the colorbar box
  - `:returns`: `GraphicsAxes`
    > the colorbar axis


<a id="McUtils.Plots.Graphics.GraphicsBase.add_colorbar" class="docs-object-method">&nbsp;</a> 
```python
add_colorbar(self, graphics=None, norm=None, cmap=None, size=None, orientation='vertical', origin=None, tick_padding=40, colorbar_axes=None, cax=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L1180)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L1180?message=Update%20Docs)]
</div>
**LLM Docstring**

Add a colorbar to the figure, creating (and tracking) a dedicated colorbar axis
if one isn't supplied.
  - `graphics`: `Any`
    > the mappable/graphics the colorbar describes
  - `norm`: `Any`
    > the color normalization
  - `cmap`: `Any`
    > the colormap
  - `size`: `Any`
    > the colorbar size (auto by orientation if omitted)
  - `orientation`: `str`
    > `'vertical'` or `'horizontal'`
  - `origin`: `Any`
    > the colorbar origin
  - `tick_padding`: `Any`
    > space for the ticks
  - `colorbar_axes`: `Any`
    > an explicit colorbar axis
  - `cax`: `Any`
    > an alias for the colorbar graphics
  - `kw`: `Any`
    > extra options for the backend colorbar
  - `:returns`: `_`
    > the colorbar


<a id="McUtils.Plots.Graphics.GraphicsBase.create_inset" class="docs-object-method">&nbsp;</a> 
```python
create_inset(self, bbox, coordinates='scaled', graphics_class=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L1255)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L1255?message=Update%20Docs)]
</div>
**LLM Docstring**

Create an inset graphics object within this figure, converting the bbox from the
requested coordinate system into figure-scaled coordinates.
  - `bbox`: `Any`
    > the inset bounding box
  - `coordinates`: `str`
    > `'scaled'` (within the frame) or `'absolute'`
  - `graphics_class`: `Any`
    > the class of the inset (defaults to this type)
  - `opts`: `Any`
    > options for the inset graphics
  - `:returns`: `GraphicsBase`
    > the inset graphics object
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Graphics/GraphicsBase.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Graphics/GraphicsBase.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Graphics/GraphicsBase.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Graphics/GraphicsBase.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics.py#L154?message=Update%20Docs)   
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