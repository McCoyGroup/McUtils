## <a id="McUtils.Jupyter.Apps.Interfaces.Table">Table</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L3154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L3154?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
Item: TableItem
```
<a id="McUtils.Jupyter.Apps.Interfaces.Table.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, elements, rows=None, cols=None, alignment=None, justification=None, row_spacing=None, col_spacing=None, item_attrs=None, row_height='1fr', column_width='1fr', table_headings=None, striped=True, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L3156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L3156?message=Update%20Docs)]
</div>
**LLM Docstring**

A table rendered as a CSS grid (`display: contents` rows), optionally with headings
and striping.
  - `elements`: `Any`
    > the table rows of cells
  - `rows`: `Any`
    > the number of rows
  - `cols`: `Any`
    > the number of columns
  - `alignment`: `Any`
    > the cell alignment
  - `justification`: `Any`
    > the cell justification
  - `row_spacing`: `Any`
    > the row gap
  - `col_spacing`: `Any`
    > the column gap
  - `item_attrs`: `Any`
    > default per-cell attributes
  - `row_height`: `Any`
    > the row track sizing
  - `column_width`: `Any`
    > the column track sizing
  - `table_headings`: `Any`
    > the header row cells
  - `striped`: `bool`
    > use striped rows
  - `attrs`: `Any`
    > extra attributes


<a id="McUtils.Jupyter.Apps.Interfaces.Table.wrapper" class="docs-object-method">&nbsp;</a> 
```python
wrapper(self, *elems, cls=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Table.py#L3202)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Table.py#L3202?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap the rows in a `<table>` (with header/body sections and striping).
  - `elems`: `Any`
    > the table rows
  - `cls`: `Any`
    > extra CSS classes
  - `attrs`: `Any`
    > extra attributes
  - `:returns`: `_`
    > the table element


<a id="McUtils.Jupyter.Apps.Interfaces.Table.setup_layout" class="docs-object-method">&nbsp;</a> 
```python
setup_layout(self, grid, attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Table.py#L3230)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Table.py#L3230?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the table rows (including an optional heading row) and infer the row/column counts.
  - `grid`: `Any`
    > the grid of cells
  - `attrs`: `Any`
    > the per-cell attributes
  - `:returns`: `tuple`
    > `(settings, rows)`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/Table.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/Table.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/Table.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/Table.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L3154?message=Update%20Docs)   
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