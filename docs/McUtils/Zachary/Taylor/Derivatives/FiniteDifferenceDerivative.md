## <a id="McUtils.Zachary.Taylor.Derivatives.FiniteDifferenceDerivative">FiniteDifferenceDerivative</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/Derivatives.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/Derivatives.py#L14?message=Update%20Docs)]
</div>

Provides derivatives for a function (scalar or vector valued).
Can be indexed into or the entire tensor of derivatives may be requested.
The potential for optimization undoubtedly exists, but the idea is to provide as _simple_ an interface as possible.
Robustification needs to be done, but is currently used in `CoordinateSystem.jacobian` to good effect.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse " id="methods" markdown="1">
 
<a id="McUtils.Zachary.Taylor.Derivatives.FiniteDifferenceDerivative.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, f, function_shape=(0, 0), parallelizer=None, logger=None, **fd_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.py#L33)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.py#L33?message=Update%20Docs)]
</div>

  - `f`: `FunctionSpec | callable`
    > the function we would like to take derivatives of
  - `function_shape`: `Iterable[Iterable[int] | int] | None`
    > the shape of the function we'd like to take the derivatives of
  - `fd_opts`: `Any`
    > the options to pass to the finite difference function


<a id="McUtils.Zachary.Taylor.Derivatives.FiniteDifferenceDerivative.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, *args, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.py#L57)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.py#L57?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.Derivatives.FiniteDifferenceDerivative.derivatives" class="docs-object-method">&nbsp;</a> 
```python
derivatives(self, center, displacement_function=None, prep=None, lazy=None, mesh_spacing=None, **fd_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.py#L60)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.py#L60?message=Update%20Docs)]
</div>
Generates a differencer object that can be used to get derivs however your little heart desires
  - `center`: `np.ndarray`
    > the center point around which to generate differences
  - `displacement_function`: `Any`
    > 
  - `mesh_spacing`: `Any`
    > 
  - `prep`: `Any`
    > 
  - `fd_opts`: `Any`
    > 
  - `:returns`: `_`
    >
 </div>
</div>




## Examples
## <a id="McUtils.Zachary.Taylor.Derivatives.FiniteDifferenceDerivative">FiniteDifferenceDerivative</a>
Provides derivatives for a function (scalar or vector valued).
Can be indexed into or the entire tensor of derivatives may be requested.
The potential for optimization undoubtedly exists, but the idea is to provide as _simple_ an interface as possible.
Robustification needs to be done, but is currently used in `CoordinateSystem.jacobian` to good effect.

### Properties and Methods
<a id="McUtils.Zachary.Taylor.Derivatives.FiniteDifferenceDerivative.__init__" class="docs-object-method">&nbsp;</a>
```python
__init__(self, f, function_shape=(0, 0), **fd_opts): 
```

- `f`: `FunctionSpec | callable`
    >the function we would like to take derivatives of
- `function_shape`: `Iterable[Iterable[int] | int] | None`
    >the shape of the function we'd like to take the derivatives of
- `fd_opts`: `Any`
    >the options to pass to the finite difference function

<a id="McUtils.Zachary.Taylor.Derivatives.FiniteDifferenceDerivative.__call__" class="docs-object-method">&nbsp;</a>
```python
__call__(self, *args, **opts): 
```

<a id="McUtils.Zachary.Taylor.Derivatives.FiniteDifferenceDerivative.derivatives" class="docs-object-method">&nbsp;</a>
```python
derivatives(self, center, displacement_function=None, prep=None, lazy=None, mesh_spacing=None, **fd_opts): 
```
Generates a differencer object that can be used to get derivs however your little heart desires
- `center`: `np.ndarray`
    >the center point around which to generate differences
- `displacement_function`: `Any`
    >No description...
- `mesh_spacing`: `Any`
    >No description...
- `prep`: `Any`
    >No description...
- `fd_opts`: `Any`
    >No description...
- `:returns`: `_`
    >No description...

### Examples


___

[Edit Examples](https://github.com/McCoyGroup/References/edit/gh-pages/Documentation/examples/McUtils/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.md) or 
[Create New Examples](https://github.com/McCoyGroup/References/new/gh-pages/?filename=Documentation/examples/McUtils/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.md) <br/>
[Edit Template](https://github.com/McCoyGroup/References/edit/gh-pages/Documentation/templates/McUtils/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.md) or 
[Create New Template](https://github.com/McCoyGroup/References/new/gh-pages/?filename=Documentation/templates/McUtils/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.md) <br/>
[Edit Docstrings](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/Derivatives.py?message=Update%20Docs)






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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Taylor/Derivatives/FiniteDifferenceDerivative.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/Derivatives.py#L14?message=Update%20Docs)   
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