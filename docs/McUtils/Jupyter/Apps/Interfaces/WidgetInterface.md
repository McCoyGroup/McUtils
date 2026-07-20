## <a id="McUtils.Jupyter.Apps.Interfaces.WidgetInterface">WidgetInterface</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L107)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L107?message=Update%20Docs)]
</div>

Provides the absolute minimum necessary for hooking
an interface that creates an `ipywidget` into the
Jupyter display runtime







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
bootstrap_js_bundle_opts: dict
bootstrap_jquery_bundle_opts: dict
bootstrap_css_opts: dict
```
<a id="McUtils.Jupyter.Apps.Interfaces.WidgetInterface.to_widget" class="docs-object-method">&nbsp;</a> 
```python
to_widget(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.py#L113)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.py#L113?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: render this interface to an `ipywidget`.
  - `:returns`: `_`
    > the widget


<a id="McUtils.Jupyter.Apps.Interfaces.WidgetInterface.initialize" class="docs-object-method">&nbsp;</a> 
```python
initialize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.py#L124)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.py#L124?message=Update%20Docs)]
</div>
**LLM Docstring**

Hook run after display; overridable for post-display setup (no-op by default).


<a id="McUtils.Jupyter.Apps.Interfaces.WidgetInterface.to_static_html" class="docs-object-method">&nbsp;</a> 
```python
to_static_html(self, include_bootstrap=True, create_body=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.py#L171)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.py#L171?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the interface to static HTML, optionally embedding the Bootstrap links and
wrapping it in a full document.
  - `include_bootstrap`: `bool`
    > embed the Bootstrap links
  - `create_body`: `bool`
    > wrap in a full `<html><body>` document
  - `:returns`: `_`
    > the static HTML element


<a id="McUtils.Jupyter.Apps.Interfaces.WidgetInterface.display" class="docs-object-method">&nbsp;</a> 
```python
display(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.py#L200)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.py#L200?message=Update%20Docs)]
</div>
**LLM Docstring**

Display the interface (guarded against re-entrant display calls).


<a id="McUtils.Jupyter.Apps.Interfaces.WidgetInterface.get_mime_bundle" class="docs-object-method">&nbsp;</a> 
```python
get_mime_bundle(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.py#L212)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.py#L212?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the widget's MIME bundle for rich display.
  - `:returns`: `dict`
    > the MIME bundle
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/WidgetInterface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L107?message=Update%20Docs)   
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