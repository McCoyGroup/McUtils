## <a id="McUtils.Jupyter.Apps.Interfaces.Container">Container</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces.py#L426)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces.py#L426?message=Update%20Docs)]
</div>

Extends the base `WrapperComponent` to include a final
`items` spec for cases where there is a base wrapper and a set of items,
e.g. a list group which has the `list-group` outer class and a set of `list-items` inside.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
wrappers: dict
theme: dict
```
<a id="McUtils.Jupyter.Apps.Interfaces.Container.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, items: Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, Tuple[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType], Mapping], NoneType, Iterable[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, Tuple[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType], Mapping]]]], wrappers: dict = None, **attrs) -> None: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Container.py#L434)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Container.py#L434?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Container.items" class="docs-object-method">&nbsp;</a> 
```python
@property
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Container.py#L472)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Container.py#L472?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Container.create_item" class="docs-object-method">&nbsp;</a> 
```python
create_item(self, i, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Container.py#L495)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Container.py#L495?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Container.update_widget_child" class="docs-object-method">&nbsp;</a> 
```python
update_widget_child(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Container.py#L509)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Container.py#L509?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Container.insert_widget_child" class="docs-object-method">&nbsp;</a> 
```python
insert_widget_child(self, where, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Container.py#L511)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Container.py#L511?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/Container.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/Container.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/Container.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/Container.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces.py#L426?message=Update%20Docs)   
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