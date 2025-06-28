## <a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.RegularGridFiniteDifference">RegularGridFiniteDifference</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L435)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L435?message=Update%20Docs)]
</div>

Defines a 1D finite difference over a regular grid







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse " id="methods" markdown="1">
 ```python
only_odd_orders: bool
```
<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.RegularGridFiniteDifference.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, order, stencil=None, accuracy=4, end_point_accuracy=2, only_odd_orders=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L440)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L440?message=Update%20Docs)]
</div>

  - `order`: `int`
    > the order of the derivative to take
  - `stencil`: `int | None`
    > the number of stencil points to add
  - `accuracy`: `int | None`
    > the approximate accuracy to target with the method
  - `end_point_accuracy`: `int | None`
    > the extra number of stencil points to add to the end points
  - `kw`: `Any`
    > options passed through to the `FiniteDifferenceMatrix`


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.RegularGridFiniteDifference.finite_difference_data" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
finite_difference_data(cls, order, stencil, end_point_precision): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L470)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L470?message=Update%20Docs)]
</div>
Builds a FiniteDifferenceData object from an order, stencil, and end_point_precision
  - `order`: `Any`
    > 
  - `stencil`: `Any`
    > 
  - `end_point_precision`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.RegularGridFiniteDifference.get_weights" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
get_weights(m, s, n): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L499)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L499?message=Update%20Docs)]
</div>
Extracts the weights for an evenly spaced grid
  - `m`: `Any`
    > 
  - `s`: `Any`
    > 
  - `n`: `Any`
    > 
  - `:returns`: `_`
    >
 </div>
</div>




## Examples
## <a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.RegularGridFiniteDifference">RegularGridFiniteDifference</a>
Defines a 1D finite difference over a regular grid

### Properties and Methods
```python
finite_difference_data: method
```
<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.RegularGridFiniteDifference.__init__" class="docs-object-method">&nbsp;</a>
```python
__init__(self, order, stencil=None, accuracy=4, end_point_accuracy=2, **kw): 
```

- `order`: `int`
    >the order of the derivative to take
- `stencil`: `int | None`
    >the number of stencil points to add
- `accuracy`: `int | None`
    >the approximate accuracy to target with the method
- `end_point_accuracy`: `int | None`
    >the extra number of stencil points to add to the end points
- `kw`: `Any`
    >options passed through to the `FiniteDifferenceMatrix`

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.RegularGridFiniteDifference.get_weights" class="docs-object-method">&nbsp;</a>
```python
get_weights(m, s, n): 
```
Extracts the weights for an evenly spaced grid
- `m`: `Any`
    >No description...
- `s`: `Any`
    >No description...
- `n`: `Any`
    >No description...
- `:returns`: `_`
    >No description...

### Examples


___

[Edit Examples](https://github.com/McCoyGroup/References/edit/gh-pages/Documentation/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/RegularGridFiniteDifference.md) or 
[Create New Examples](https://github.com/McCoyGroup/References/new/gh-pages/?filename=Documentation/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/RegularGridFiniteDifference.md) <br/>
[Edit Template](https://github.com/McCoyGroup/References/edit/gh-pages/Documentation/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/RegularGridFiniteDifference.md) or 
[Create New Template](https://github.com/McCoyGroup/References/new/gh-pages/?filename=Documentation/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/RegularGridFiniteDifference.md) <br/>
[Edit Docstrings](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction.py?message=Update%20Docs)






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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/RegularGridFiniteDifference.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/RegularGridFiniteDifference.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Taylor/FiniteDifferenceFunction/RegularGridFiniteDifference.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/RegularGridFiniteDifference.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L435?message=Update%20Docs)   
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