## <a id="McUtils.Jupyter.Apps.Apps.App">App</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps.py#L132)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps.py#L132?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L165)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L165?message=Update%20Docs)]
</div>
**LLM Docstring**

Recursively merge two theme dicts (the second overriding/extending the first).
  - `theme_1`: `dict`
    > the base theme
  - `theme_2`: `dict`
    > the overriding theme
  - `:returns`: `dict`
    > the merged theme


<a id="McUtils.Jupyter.Apps.Apps.App.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, body=None, header=None, footer=None, sidebar=None, toolbar=None, theme='primary', layout='grid', cls='app border', output=None, capture_output=None, vars=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps.py#L188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps.py#L188?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a Jupyter app framework from optional header/footer/sidebar/toolbar/body
sections, a theme, and a layout, tracking the app stack and its output/variable
context.
  - `body`: `Any`
    > the body content
  - `header`: `Any`
    > the header content
  - `footer`: `Any`
    > the footer content
  - `sidebar`: `Any`
    > the sidebar content
  - `toolbar`: `Any`
    > the toolbar content
  - `theme`: `Any`
    > the theme name or overrides
  - `layout`: `str`
    > the layout style (e.g. `'grid'`)
  - `cls`: `Any`
    > the root CSS classes
  - `output`: `Any`
    > the output area (created if omitted)
  - `capture_output`: `bool | None`
    > show a captured-output panel (defaults to top-level only)
  - `vars`: `Any`
    > the variable set (resolved from the default if omitted)
  - `attrs`: `Any`
    > extra layout attributes


<a id="McUtils.Jupyter.Apps.Apps.App.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L241)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L241?message=Update%20Docs)]
</div>
**LLM Docstring**

Enter the app context: activate its variable set and default output widget and
push it onto the app stack (reentrant via a depth counter).
  - `:returns`: `App`
    > the app


<a id="McUtils.Jupyter.Apps.Apps.App.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L259)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L259?message=Update%20Docs)]
</div>
**LLM Docstring**

Exit the app context, restoring the variable set/output widget and popping the app
stack when fully unwound.
  - `exc_type`: `Any`
    > the exception type, if any
  - `exc_val`: `Any`
    > the exception value, if any
  - `exc_tb`: `Any`
    > the traceback, if any


<a id="McUtils.Jupyter.Apps.Apps.App.body" class="docs-object-method">&nbsp;</a> 
```python
@property
body(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L277)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L277?message=Update%20Docs)]
</div>
**LLM Docstring**

The app's body component, constructed lazily (within the app context) from the
supplied body spec on first access. The setter resets the cached component.
  - `:returns`: `_`
    > the body component


<a id="McUtils.Jupyter.Apps.Apps.App.header" class="docs-object-method">&nbsp;</a> 
```python
@property
header(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L303)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L303?message=Update%20Docs)]
</div>
**LLM Docstring**

The app's header component, constructed lazily (within the app context) from the
supplied header spec on first access. The setter resets the cached component.
  - `:returns`: `_`
    > the header component


<a id="McUtils.Jupyter.Apps.Apps.App.sidebar" class="docs-object-method">&nbsp;</a> 
```python
@property
sidebar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L329)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L329?message=Update%20Docs)]
</div>
**LLM Docstring**

The app's sidebar component, constructed lazily (within the app context) from the
supplied sidebar spec on first access. The setter resets the cached component.
  - `:returns`: `_`
    > the sidebar component


<a id="McUtils.Jupyter.Apps.Apps.App.toolbar" class="docs-object-method">&nbsp;</a> 
```python
@property
toolbar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L355)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L355?message=Update%20Docs)]
</div>
**LLM Docstring**

The app's toolbar component, constructed lazily (within the app context) from the
supplied toolbar spec on first access. The setter resets the cached component.
  - `:returns`: `_`
    > the toolbar component


<a id="McUtils.Jupyter.Apps.Apps.App.footer" class="docs-object-method">&nbsp;</a> 
```python
@property
footer(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L381)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L381?message=Update%20Docs)]
</div>
**LLM Docstring**

The app's footer component, constructed lazily (within the app context) from the
supplied footer spec on first access. The setter resets the cached component.
  - `:returns`: `_`
    > the footer component


<a id="McUtils.Jupyter.Apps.Apps.App.prep_head_item" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_head_item(cls, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L407)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L407?message=Update%20Docs)]
</div>
**LLM Docstring**

Coerce a `(label, callback)` head item into a `Button`.
  - `item`: `Any`
    > the head item
  - `:returns`: `_`
    > the prepared item


<a id="McUtils.Jupyter.Apps.Apps.App.construct_navbar_item" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct_navbar_item(cls, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L424)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L424?message=Update%20Docs)]
</div>
**LLM Docstring**

Coerce a navbar item spec into a component: a `(label, sub-items)` pair becomes a
`Dropdown`, a `(label, callback)` pair becomes a `Button`.
  - `item`: `Any`
    > the navbar item spec
  - `:returns`: `_`
    > the navbar item


<a id="McUtils.Jupyter.Apps.Apps.App.construct_header" class="docs-object-method">&nbsp;</a> 
```python
construct_header(self, header, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L446)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L446?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the header `Navbar` from its spec (a list, a `(spec, opts)` pair, or an
`items` dict), theming it.
  - `header`: `Any`
    > the header spec
  - `opts`: `Any`
    > extra navbar options
  - `:returns`: `_`
    > the header component


<a id="McUtils.Jupyter.Apps.Apps.App.construct_footer" class="docs-object-method">&nbsp;</a> 
```python
construct_footer(self, footer, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L478)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L478?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the footer `Navbar` from its spec, theming it.
  - `footer`: `Any`
    > the footer spec
  - `opts`: `Any`
    > extra navbar options
  - `:returns`: `_`
    > the footer component


<a id="McUtils.Jupyter.Apps.Apps.App.construct_sidebar_item" class="docs-object-method">&nbsp;</a> 
```python
construct_sidebar_item(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L505)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L505?message=Update%20Docs)]
</div>
**LLM Docstring**

Coerce a sidebar item spec into an `Opener` (nesting sub-`Sidebar`s for grouped
items).
  - `item`: `Any`
    > the sidebar item spec
  - `:returns`: `_`
    > the sidebar item


<a id="McUtils.Jupyter.Apps.Apps.App.construct_sidebar" class="docs-object-method">&nbsp;</a> 
```python
construct_sidebar(self, sidebar, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L529)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L529?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the `Sidebar` from its spec (a list, a `(spec, opts)` pair, or an `items`
dict), theming it.
  - `sidebar`: `Any`
    > the sidebar spec
  - `opts`: `Any`
    > extra sidebar options
  - `:returns`: `_`
    > the sidebar component


<a id="McUtils.Jupyter.Apps.Apps.App.construct_toolbar_item" class="docs-object-method">&nbsp;</a> 
```python
construct_toolbar_item(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L558)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L558?message=Update%20Docs)]
</div>
**LLM Docstring**

Coerce a toolbar item spec (a control settings dict) into a `Control`.
  - `item`: `Any`
    > the toolbar item spec
  - `:returns`: `_`
    > the toolbar item


<a id="McUtils.Jupyter.Apps.Apps.App.construct_toolbar" class="docs-object-method">&nbsp;</a> 
```python
construct_toolbar(self, toolbar, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L573)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L573?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the toolbar from its spec, as a `Grid` (for a list of rows) or a `Div`,
theming it.
  - `toolbar`: `Any`
    > the toolbar spec
  - `opts`: `Any`
    > extra toolbar options
  - `:returns`: `_`
    > the toolbar component


<a id="McUtils.Jupyter.Apps.Apps.App.wrap_body" class="docs-object-method">&nbsp;</a> 
```python
wrap_body(self, fn, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L599)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L599?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap a function as a `FunctionDisplay` bound to the app's variables.
  - `fn`: `Callable`
    > the function
  - `styles`: `Any`
    > extra display styles
  - `:returns`: `FunctionDisplay`
    > the function display


<a id="McUtils.Jupyter.Apps.Apps.App.construct_body_item" class="docs-object-method">&nbsp;</a> 
```python
construct_body_item(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L615)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L615?message=Update%20Docs)]
</div>
**LLM Docstring**

Coerce a body item into a component: wrap functions as `FunctionDisplay`s and
`(content, styles)` pairs as displays/spans, passing existing components through.
  - `item`: `Any`
    > the body item spec
  - `:returns`: `_`
    > the body item


<a id="McUtils.Jupyter.Apps.Apps.App.construct_body" class="docs-object-method">&nbsp;</a> 
```python
construct_body(self, body): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L638)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L638?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the body from its spec: a dict becomes `Tabs`, a list becomes a list of
bodies, else a single body item.
  - `body`: `Any`
    > the body spec
  - `:returns`: `_`
    > the body component(s)


<a id="McUtils.Jupyter.Apps.Apps.App.construct_layout" class="docs-object-method">&nbsp;</a> 
```python
construct_layout(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L656)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L656?message=Update%20Docs)]
</div>
**LLM Docstring**

Assemble the app's `Grid` layout from its header/sidebar/toolbar/body/output/footer
sections, computing the row/column spans and sizes.
  - `:returns`: `Grid`
    > the layout grid


<a id="McUtils.Jupyter.Apps.Apps.App.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Apps/App.py#L752)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps/App.py#L752?message=Update%20Docs)]
</div>
**LLM Docstring**

Render the app to its JHTML element (via the constructed layout).
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Apps/App.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Apps/App.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Apps/App.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Apps/App.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Apps.py#L132?message=Update%20Docs)   
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