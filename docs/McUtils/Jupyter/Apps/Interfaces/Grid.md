## <a id="McUtils.Jupyter.Apps.Interfaces.Grid">Grid</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L2949)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L2949?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
Item: GridItem
```
<a id="McUtils.Jupyter.Apps.Interfaces.Grid.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, elements, rows=None, cols=None, alignment=None, justification=None, row_spacing=None, col_spacing=None, item_attrs=None, row_height='auto', column_width='1fr', **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces.py#L2951)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L2951?message=Update%20Docs)]
</div>
**LLM Docstring**

A CSS-grid layout of elements (given as a list of rows).
  - `elements`: `Any`
    > the grid rows of elements
  - `rows`: `Any`
    > the number of rows (inferred if omitted)
  - `cols`: `Any`
    > the number of columns (inferred if omitted)
  - `alignment`: `Any`
    > the item alignment
  - `justification`: `Any`
    > the item justification
  - `row_spacing`: `Any`
    > the row gap
  - `col_spacing`: `Any`
    > the column gap
  - `item_attrs`: `Any`
    > default per-item attributes
  - `row_height`: `Any`
    > the row track sizing
  - `column_width`: `Any`
    > the column track sizing
  - `attrs`: `Any`
    > extra attributes


<a id="McUtils.Jupyter.Apps.Interfaces.Grid.setup_layout" class="docs-object-method">&nbsp;</a> 
```python
setup_layout(self, grid, attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Grid.py#L2990)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Grid.py#L2990?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap each non-empty grid cell as a positioned item and infer the row/column counts.
  - `grid`: `Any`
    > the grid of elements
  - `attrs`: `Any`
    > the per-item attributes
  - `:returns`: `tuple`
    > `(settings, items)`


<a id="McUtils.Jupyter.Apps.Interfaces.Grid.wrap_item" class="docs-object-method">&nbsp;</a> 
```python
wrap_item(self, e, attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Grid.py#L3021)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Grid.py#L3021?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap a grid element as a positioned `GridItem`, filling in its row/column.
  - `e`: `Any`
    > the element
  - `attrs`: `Any`
    > the item attributes (row/col)
  - `:returns`: `_`
    > the grid item


<a id="McUtils.Jupyter.Apps.Interfaces.Grid.get_grid_styles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_grid_styles(cls, rows=None, cols=None, alignment=None, justification=None, row_gap=None, col_gap=None, row_height='1fr', col_width='1fr'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3044)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3044?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the CSS grid-container styles (template rows/columns, gaps, alignment).
  - `rows`: `Any`
    > the number of rows
  - `cols`: `Any`
    > the number of columns
  - `alignment`: `Any`
    > the item alignment
  - `justification`: `Any`
    > the item justification
  - `row_gap`: `Any`
    > the row gap
  - `col_gap`: `Any`
    > the column gap
  - `row_height`: `Any`
    > the row track sizing
  - `col_width`: `Any`
    > the column track sizing
  - `:returns`: `dict`
    > the styles


<a id="McUtils.Jupyter.Apps.Interfaces.Grid.get_layout_styles" class="docs-object-method">&nbsp;</a> 
```python
get_layout_styles(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/Apps/Interfaces/Grid.py#L3092)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces/Grid.py#L3092?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the grid container's styles.
  - `:returns`: `dict`
    > the styles
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/Grid.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/Grid.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/Grid.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/Grid.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/Apps/Interfaces.py#L2949?message=Update%20Docs)   
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