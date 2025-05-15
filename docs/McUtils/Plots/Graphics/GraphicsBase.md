## <a id="McUtils.McUtils.Plots.Graphics.GraphicsBase">GraphicsBase</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics.py#L84)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics.py#L84?message=Update%20Docs)]
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
<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.get_raw_attr" class="docs-object-method">&nbsp;</a> 
```python
get_raw_attr(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L122)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L122?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *args, name=None, figure=None, tighten=False, axes=None, subplot_kw=None, parent=None, image_size=None, padding=None, aspect_ratio=None, interactive=None, reshowable=None, backend='matplotlib', backend_options=None, theme=None, prop_manager=<class 'McUtils.McUtils.Plots.Properties.GraphicsPropertyManager'>, theme_manager=<class 'McUtils.McUtils.Plots.Styling.ThemeManager'>, managed=None, strict=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L204)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L204?message=Update%20Docs)]
</div>

  - `args`: `Any`
    > 
  - `figure`: `GraphicsBackend.Figure | None`
    > 
  - `axes`: `GraphicsBackend.Figure.Axes | None`
    > 
  - `subplot_kw`: `dict | None`
    > 
  - `parent`: `GraphicsBase | None`
    > 
  - `opts`: `Any`
    >


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.initialize_figure_and_axes" class="docs-object-method">&nbsp;</a> 
```python
initialize_figure_and_axes(self, figure, axes, *args, **kw) -> 'tuple[GraphicsBackend.Figure, GraphicsBackend.Figure.Axes]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L347)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L347?message=Update%20Docs)]
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
    > f
i
g
u
r
e
,
 
a
x
e
s


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.parent" class="docs-object-method">&nbsp;</a> 
```python
@property
parent(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L389)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L389?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.figure_parent" class="docs-object-method">&nbsp;</a> 
```python
@property
figure_parent(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L395)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L395?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.inset" class="docs-object-method">&nbsp;</a> 
```python
@property
inset(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L398)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L398?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.children" class="docs-object-method">&nbsp;</a> 
```python
@property
children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L402)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L402?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.event_handlers" class="docs-object-method">&nbsp;</a> 
```python
@property
event_handlers(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L412)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L412?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.animated" class="docs-object-method">&nbsp;</a> 
```python
@property
animated(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L420)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L420?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.bind_events" class="docs-object-method">&nbsp;</a> 
```python
bind_events(self, *handlers, **events): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L424)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L424?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.create_animation" class="docs-object-method">&nbsp;</a> 
```python
create_animation(self, *args, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L438)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L438?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.animate_frames" class="docs-object-method">&nbsp;</a> 
```python
animate_frames(self, frames, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L446)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L446?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.set_options" class="docs-object-method">&nbsp;</a> 
```python
set_options(self, event_handlers=None, animated=None, prolog=None, epilog=None, strict=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L456)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L456?message=Update%20Docs)]
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


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.prolog" class="docs-object-method">&nbsp;</a> 
```python
@property
prolog(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L489)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L489?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.epilog" class="docs-object-method">&nbsp;</a> 
```python
@property
epilog(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L498)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L498?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.opts" class="docs-object-method">&nbsp;</a> 
```python
@property
opts(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L507)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L507?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L523)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L523?message=Update%20Docs)]
</div>
Creates a copy of the object with new axes and a new figure
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.change_figure" class="docs-object-method">&nbsp;</a> 
```python
change_figure(self, new, *init_args, figs=None, **init_kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L538)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L538?message=Update%20Docs)]
</div>
Creates a copy of the object with new axes and a new figure
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.prep_show" class="docs-object-method">&nbsp;</a> 
```python
prep_show(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L591)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L591?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.show" class="docs-object-method">&nbsp;</a> 
```python
show(self, reshow=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L602)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L602?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.close" class="docs-object-method">&nbsp;</a> 
```python
close(self, force=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L625)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L625?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.__del__" class="docs-object-method">&nbsp;</a> 
```python
__del__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L642)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L642?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L648)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L648?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.clear" class="docs-object-method">&nbsp;</a> 
```python
clear(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L656)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L656?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.savefig" class="docs-object-method">&nbsp;</a> 
```python
savefig(self, where, format=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L672)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L672?message=Update%20Docs)]
</div>
Saves the image to file
  - `where`: `Any`
    > 
  - `format`: `Any`
    > 
  - `kw`: `Any`
    > 
  - `:returns`: `str`
    > f
i
l
e
 
i
t
 
w
a
s
 
s
a
v
e
d
 
t
o
 
(
I
 
t
h
i
n
k
.
.
.
?
)


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.to_png" class="docs-object-method">&nbsp;</a> 
```python
to_png(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L693)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L693?message=Update%20Docs)]
</div>
Used by Jupyter and friends to make a version of the image that they can display, hence the extra 'tight_layout' call
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.create_colorbar_axis" class="docs-object-method">&nbsp;</a> 
```python
create_colorbar_axis(self, figure=None, size=(20, 200), tick_padding=40): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L714)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L714?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.add_colorbar" class="docs-object-method">&nbsp;</a> 
```python
add_colorbar(self, graphics=None, norm=None, cmap=None, size=(20, 200), tick_padding=40, colorbar_axes=None, cax=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L760)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L760?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Plots.Graphics.GraphicsBase.create_inset" class="docs-object-method">&nbsp;</a> 
```python
create_inset(self, bbox, coordinates='scaled', graphics_class=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Graphics/GraphicsBase.py#L805)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics/GraphicsBase.py#L805?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Graphics/GraphicsBase.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Graphics/GraphicsBase.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Graphics/GraphicsBase.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Graphics/GraphicsBase.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Graphics.py#L84?message=Update%20Docs)   
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