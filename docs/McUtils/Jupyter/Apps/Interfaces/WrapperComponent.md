## <a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent">WrapperComponent</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces.py#L246)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces.py#L246?message=Update%20Docs)]
</div>

Extends the base component interface to allow for the
construction of interesting compound interfaces (using `JHTML.Compound`).
Takes a `dict` of `wrappers` naming the successive levels of the interface
along with a `theme` that provides style declarations for each level.

Used primarily to create `Bootstrap`-based interfaces.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
wrappers: dict
theme: dict
```
<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, items: Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, Tuple[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType], Mapping], NoneType, Iterable[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, Tuple[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType], Mapping]]]], wrappers=None, theme=None, extend_base_theme=True, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L257)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L257?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.handle_variants" class="docs-object-method">&nbsp;</a> 
```python
handle_variants(self, theme): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L288)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L288?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.manage_theme" class="docs-object-method">&nbsp;</a> 
```python
manage_theme(self, theme, extend_base_theme=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L304?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.merge_themes" class="docs-object-method">&nbsp;</a> 
```python
merge_themes(theme: 'None|dict', attrs: dict, merge_keys=('cls',)): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L315)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L315?message=Update%20Docs)]
</div>
Needs to handle cases where a `theme` is provided
which includes things like `cls` declarations and then the
`attrs` may also include `cls` declarations and the `attrs`
declarations get appended to the theme


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.manage_items" class="docs-object-method">&nbsp;</a> 
```python
manage_items(items, attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L349)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L349?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.get_child" class="docs-object-method">&nbsp;</a> 
```python
get_child(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L373)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L373?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.set_child" class="docs-object-method">&nbsp;</a> 
```python
set_child(self, which, new): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L375)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L375?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.insert_child" class="docs-object-method">&nbsp;</a> 
```python
insert_child(self, where, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L377)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L377?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.wrap_items" class="docs-object-method">&nbsp;</a> 
```python
wrap_items(self, items): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L402)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L402?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self, parent=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L412)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/WrapperComponent.py#L412?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces.py#L246?message=Update%20Docs)   
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