## <a id="McUtils.Jupyter.Apps.Apps.App">App</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps.py#L100)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps.py#L100?message=Update%20Docs)]
</div>

Provides a framework for making Jupyter Apps with the
elements built out in the Interfaces package







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
themes: dict
```
<a id="McUtils.Jupyter.Apps.Apps.App.merge_themes" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
merge_themes(cls, theme_1, theme_2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L133)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L133?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, body=None, header=None, footer=None, sidebar=None, toolbar=None, theme='primary', layout='grid', cls='app border', output=None, capture_output=None, vars=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps.py#L144)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps.py#L144?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L175?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L184)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L184?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.body" class="docs-object-method">&nbsp;</a> 
```python
@property
body(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L192)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L192?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.header" class="docs-object-method">&nbsp;</a> 
```python
@property
header(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L202)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L202?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.sidebar" class="docs-object-method">&nbsp;</a> 
```python
@property
sidebar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L212)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L212?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.toolbar" class="docs-object-method">&nbsp;</a> 
```python
@property
toolbar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L222)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L222?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.footer" class="docs-object-method">&nbsp;</a> 
```python
@property
footer(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L232)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L232?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.prep_head_item" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_head_item(cls, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L242)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L242?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_navbar_item" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct_navbar_item(cls, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L251)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L251?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_header" class="docs-object-method">&nbsp;</a> 
```python
construct_header(self, header, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L264)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L264?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_footer" class="docs-object-method">&nbsp;</a> 
```python
construct_footer(self, footer, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L286)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L286?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_sidebar_item" class="docs-object-method">&nbsp;</a> 
```python
construct_sidebar_item(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L304?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_sidebar" class="docs-object-method">&nbsp;</a> 
```python
construct_sidebar(self, sidebar, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L319)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L319?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_toolbar_item" class="docs-object-method">&nbsp;</a> 
```python
construct_toolbar_item(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L338)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L338?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_toolbar" class="docs-object-method">&nbsp;</a> 
```python
construct_toolbar(self, toolbar, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L345)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L345?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.wrap_body" class="docs-object-method">&nbsp;</a> 
```python
wrap_body(self, fn, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L361)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L361?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_body_item" class="docs-object-method">&nbsp;</a> 
```python
construct_body_item(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L366)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L366?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_body" class="docs-object-method">&nbsp;</a> 
```python
construct_body(self, body): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L380)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L380?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_layout" class="docs-object-method">&nbsp;</a> 
```python
construct_layout(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L389)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L389?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L475)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L475?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Apps/App.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Apps/App.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Apps/App.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Apps/App.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps.py#L100?message=Update%20Docs)   
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