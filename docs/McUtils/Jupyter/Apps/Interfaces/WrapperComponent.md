## <a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent">WrapperComponent</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L611)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L611?message=Update%20Docs)]
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
__init__(self, items: Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType, Tuple[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType], Mapping], NoneType, Iterable[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType, Tuple[Union[str, Mapping, McUtils.Jupyter.Apps.types.HTMLableType, McUtils.Jupyter.Apps.types.WidgetableType, McUtils.Jupyter.Apps.types.IPyHTMLableType, McUtils.Jupyter.Apps.types.ImageableType], Mapping]]]], wrappers=None, theme=None, extend_base_theme=True, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L622)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L622?message=Update%20Docs)]
</div>
**LLM Docstring**

A component that renders its items inside one or more themed wrapper elements
(the basis for Bootstrap interfaces).
  - `items`: `Any`
    > the wrapped items
  - `wrappers`: `dict | None`
    > the named wrapper element classes
  - `theme`: `dict | None`
    > the per-wrapper style theme
  - `extend_base_theme`: `bool`
    > merge with the class's base theme
  - `attrs`: `Any`
    > extra attributes (merged into the outer wrapper's theme)


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.handle_variants" class="docs-object-method">&nbsp;</a> 
```python
handle_variants(self, theme): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L671)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L671?message=Update%20Docs)]
</div>
**LLM Docstring**

Expand a theme's `variant`/`base-cls` shorthand into the concrete
`base-cls-variant` CSS class.
  - `theme`: `dict`
    > the theme
  - `:returns`: `dict`
    > the expanded theme


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.manage_theme" class="docs-object-method">&nbsp;</a> 
```python
manage_theme(self, theme, extend_base_theme=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L698)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L698?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve the effective theme, optionally merging it over the class's base theme.
  - `theme`: `Any`
    > the supplied theme (the class theme if `None`)
  - `extend_base_theme`: `bool`
    > merge with the base theme
  - `:returns`: `dict`
    > the resolved theme


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.merge_themes" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
merge_themes(cls, theme: 'None|dict', attrs: dict, merge_keys=('cls',)): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L720)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L720?message=Update%20Docs)]
</div>
Needs to handle cases where a `theme` is provided
which includes things like `cls` declarations and then the
`attrs` may also include `cls` declarations and the `attrs`
declarations get appended to the theme


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.manage_items" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
manage_items(cls, items, attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L768)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L768?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize the items spec into a `(items_list, attrs)` pair, pulling out any
attribute dict (from a dict body or a `(items, opts)` pair) and wrapping a scalar
item in a list.
  - `items`: `Any`
    > the items spec
  - `attrs`: `dict`
    > the base attributes
  - `:returns`: `tuple`
    > `(items_list, attrs)`


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.get_child" class="docs-object-method">&nbsp;</a> 
```python
get_child(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L808)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L808?message=Update%20Docs)]
</div>
**LLM Docstring**

Get a wrapped item by index.
  - `key`: `Any`
    > the item index
  - `:returns`: `_`
    > the item


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.set_child" class="docs-object-method">&nbsp;</a> 
```python
set_child(self, which, new): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L818)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L818?message=Update%20Docs)]
</div>
**LLM Docstring**

Set a wrapped item by index.
  - `which`: `Any`
    > the item index
  - `new`: `Any`
    > the new item


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.insert_child" class="docs-object-method">&nbsp;</a> 
```python
insert_child(self, where, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L828)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L828?message=Update%20Docs)]
</div>
**LLM Docstring**

Insert a wrapped item at a position (appending if `where` is `None`).
  - `where`: `Any`
    > the index
  - `child`: `Any`
    > the item


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.wrap_items" class="docs-object-method">&nbsp;</a> 
```python
wrap_items(self, items): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L861)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L861?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the items inside the wrapper element(s), applying the themed attributes.
  - `items`: `Any`
    > the items to wrap
  - `:returns`: `_`
    > the wrapper element


<a id="McUtils.Jupyter.Apps.Interfaces.WrapperComponent.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self, parent=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L879)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/WrapperComponent.py#L879?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the component by wrapping its items.
  - `parent`: `Any`
    > the parent component
  - `:returns`: `_`
    > the JHTML element
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L611?message=Update%20Docs)   
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