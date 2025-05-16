## <a id="McUtils.Plots.Interactive.EventHandler">EventHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive.py#L12)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive.py#L12?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
Event: Event
```
<a id="McUtils.Plots.Interactive.EventHandler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, figure, on_click=None, on_release=None, on_draw=None, on_key_press=None, on_key_release=None, on_move=None, on_select=None, on_resize=None, on_scroll=None, on_figure_entered=None, on_figure_left=None, on_axes_entered=None, on_axes_left=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L13)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L13?message=Update%20Docs)]
</div>
Creates an EventHandler on a Figure that handles most interactivity stuff
  - `figure`: `GraphicsBase`
    > 
  - `on_click`: `Any`
    > 
  - `on_release`: `Any`
    > 
  - `on_draw`: `Any`
    > 
  - `on_key_press`: `Any`
    > 
  - `on_key_release`: `Any`
    > 
  - `on_move`: `Any`
    > 
  - `on_select`: `Any`
    > 
  - `on_resize`: `Any`
    > 
  - `on_scroll`: `Any`
    > 
  - `on_figure_entered`: `Any`
    > 
  - `on_figure_left`: `Any`
    > 
  - `on_axes_entered`: `Any`
    > 
  - `on_axes_left`: `Any`
    >


<a id="McUtils.Plots.Interactive.EventHandler.bind" class="docs-object-method">&nbsp;</a> 
```python
bind(self, **handlers): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L105?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.handlers" class="docs-object-method">&nbsp;</a> 
```python
@property
handlers(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L110)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L110?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.ButtonPressedEvent" class="docs-object-method">&nbsp;</a> 
```python
ButtonPressedEvent(self, handler, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L158)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L158?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.ButtonReleasedEvent" class="docs-object-method">&nbsp;</a> 
```python
ButtonReleasedEvent(self, handler, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L166)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L166?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.DrawEvent" class="docs-object-method">&nbsp;</a> 
```python
DrawEvent(self, handler, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L174)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L174?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.KeyPressedEvent" class="docs-object-method">&nbsp;</a> 
```python
KeyPressedEvent(self, handler, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L182)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L182?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.KeyReleasedEvent" class="docs-object-method">&nbsp;</a> 
```python
KeyReleasedEvent(self, handler, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L195)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L195?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.MoveEvent" class="docs-object-method">&nbsp;</a> 
```python
MoveEvent(self, handler, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L208)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L208?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.SelectEvent" class="docs-object-method">&nbsp;</a> 
```python
SelectEvent(self, handler, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L216)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L216?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.ScrollEvent" class="docs-object-method">&nbsp;</a> 
```python
ScrollEvent(self, handler, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L224)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L224?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.FigureEnterEvent" class="docs-object-method">&nbsp;</a> 
```python
FigureEnterEvent(self, handler, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L232)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L232?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.FigureLeaveEvent" class="docs-object-method">&nbsp;</a> 
```python
FigureLeaveEvent(self, handler, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L240)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L240?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.AxesEnterEvent" class="docs-object-method">&nbsp;</a> 
```python
AxesEnterEvent(self, handler, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L248)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L248?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Interactive.EventHandler.AxesLeaveEvent" class="docs-object-method">&nbsp;</a> 
```python
AxesLeaveEvent(self, handler, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Interactive/EventHandler.py#L256)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive/EventHandler.py#L256?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Interactive/EventHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Interactive/EventHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Interactive/EventHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Interactive/EventHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Interactive.py#L12?message=Update%20Docs)   
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