## <a id="McUtils.Jupyter.Apps.Apps.App">App</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps.py#L94)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps.py#L94?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L127)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L127?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, body=None, header=None, footer=None, sidebar=None, toolbar=None, theme='primary', layout='grid', cls='app border', output=None, capture_output=None, vars=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L138)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L138?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L169?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L178)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L178?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.body" class="docs-object-method">&nbsp;</a> 
```python
@property
body(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L186)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L186?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.header" class="docs-object-method">&nbsp;</a> 
```python
@property
header(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L196)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L196?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.sidebar" class="docs-object-method">&nbsp;</a> 
```python
@property
sidebar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L206)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L206?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.toolbar" class="docs-object-method">&nbsp;</a> 
```python
@property
toolbar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L216)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L216?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.footer" class="docs-object-method">&nbsp;</a> 
```python
@property
footer(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L226)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L226?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.prep_head_item" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_head_item(cls, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L236)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L236?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_navbar_item" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct_navbar_item(cls, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L245)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L245?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_header" class="docs-object-method">&nbsp;</a> 
```python
construct_header(self, header, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L258)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L258?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_footer" class="docs-object-method">&nbsp;</a> 
```python
construct_footer(self, footer, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L280)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L280?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_sidebar_item" class="docs-object-method">&nbsp;</a> 
```python
construct_sidebar_item(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L298)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L298?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_sidebar" class="docs-object-method">&nbsp;</a> 
```python
construct_sidebar(self, sidebar, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L313)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L313?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_toolbar_item" class="docs-object-method">&nbsp;</a> 
```python
construct_toolbar_item(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L332)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L332?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_toolbar" class="docs-object-method">&nbsp;</a> 
```python
construct_toolbar(self, toolbar, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L339)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L339?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.wrap_body" class="docs-object-method">&nbsp;</a> 
```python
wrap_body(self, fn, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L355)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L355?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_body_item" class="docs-object-method">&nbsp;</a> 
```python
construct_body_item(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L360)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L360?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_body" class="docs-object-method">&nbsp;</a> 
```python
construct_body(self, body): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L374)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L374?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.construct_layout" class="docs-object-method">&nbsp;</a> 
```python
construct_layout(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L383)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L383?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Apps.App.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Apps/App.py#L469)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps/App.py#L469?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Apps.py#L94?message=Update%20Docs)   
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