## <a id="McUtils.Jupyter.Apps.Interfaces.Container">Container</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L889)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L889?message=Update%20Docs)]
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
__init__(self, items: Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType, Tuple[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType], Mapping], NoneType, Iterable[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType, Tuple[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType], Mapping]]]], wrappers: dict = None, **attrs) -> None: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L897)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L897?message=Update%20Docs)]
</div>
**LLM Docstring**

A `WrapperComponent` with an outer wrapper plus a per-item element (e.g. a list
group with a `list-group` wrapper and `list-item` children).
  - `items`: `Any`
    > the item bodies
  - `wrappers`: `dict | None`
    > the wrapper-plus-item element classes
  - `attrs`: `Any`
    > extra attributes


<a id="McUtils.Jupyter.Apps.Interfaces.Container.items" class="docs-object-method">&nbsp;</a> 
```python
@property
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Container.py#L946)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Container.py#L946?message=Update%20Docs)]
</div>
**LLM Docstring**

The wrapped items, each built via `create_item`. Assigning is disallowed once
initialized.
  - `:returns`: `list`
    > the built items


<a id="McUtils.Jupyter.Apps.Interfaces.Container.create_item" class="docs-object-method">&nbsp;</a> 
```python
create_item(self, i, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Container.py#L1005)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Container.py#L1005?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an item element from a spec: pass a `raw` element through, expand a dict
body, or wrap a bare body.
  - `i`: `Any`
    > the item spec
  - `kw`: `Any`
    > extra per-item options
  - `:returns`: `_`
    > the item element


<a id="McUtils.Jupyter.Apps.Interfaces.Container.update_widget_child" class="docs-object-method">&nbsp;</a> 
```python
update_widget_child(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Container.py#L1029)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Container.py#L1029?message=Update%20Docs)]
</div>
**LLM Docstring**

Rebuild an item and push it into the live widget cache.
  - `key`: `Any`
    > the item index
  - `value`: `Any`
    > the new item spec


<a id="McUtils.Jupyter.Apps.Interfaces.Container.insert_widget_child" class="docs-object-method">&nbsp;</a> 
```python
insert_widget_child(self, where, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Container.py#L1039)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Container.py#L1039?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an item and insert it into the live widget cache.
  - `where`: `Any`
    > the index
  - `child`: `Any`
    > the item spec
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L889?message=Update%20Docs)   
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