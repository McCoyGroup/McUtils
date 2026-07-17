## <a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction">DifferentiableFunction</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L19?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L20?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a differentiable function, optionally restricted to act on a subset of the
input coordinates.
  - `inds`: `Sequence[int] | None`
    > the coordinate indices this function depends on (all if `None`)


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.reindex" class="docs-object-method">&nbsp;</a> 
```python
reindex(self, idx_perm): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L32)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L32?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a copy of the function with its coordinate indices remapped under a
permutation of the full coordinate set.
  - `idx_perm`: `np.ndarray`
    > the coordinate permutation
  - `:returns`: `DifferentiableFunction`
    > the reindexed function


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.get_consistent_inds" class="docs-object-method">&nbsp;</a> 
```python
get_consistent_inds(self, funcs: 'list[DifferentiableFunction]'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L51)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L51?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the union of the coordinate indices used by a set of functions and
reindex each onto that shared index set.
  - `funcs`: `list[DifferentiableFunction]`
    > the functions to reconcile
  - `:returns`: `tuple`
    > `(shared_inds, reindexed_funcs)`


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, coords, order=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L69)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L69?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate the function's Taylor expansion (value plus derivatives up to `order`)
at the given coordinates, scattering the result back into the full coordinate
space when the function acts on only a subset of coordinates.
  - `coords`: `np.ndarray`
    > the coordinates, shape `(..., ncoords)`
  - `order`: `int`
    > the highest derivative order to return
  - `:returns`: `list[np.ndarray]`
    > the expansion tensors `[value, grad, hess, ...]`


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.evaluate" class="docs-object-method">&nbsp;</a> 
```python
evaluate(self, coords, order=0) -> list[numpy.ndarray]: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L102?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: evaluate the function's expansion (value and derivatives) at the given
coordinates.
  - `coords`: `np.ndarray`
    > the coordinates
  - `order`: `int`
    > the highest derivative order
  - `:returns`: `list[np.ndarray]`
    > the expansion tensors


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.get_children" class="docs-object-method">&nbsp;</a> 
```python
get_children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L119?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: return the sub-functions this function is built from.
  - `:returns`: `list[DifferentiableFunction]`
    > the child functions


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L131)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L131?message=Update%20Docs)]
</div>
**LLM Docstring**

Add another differentiable function (building/merging a `FunctionSum`) or a
constant (building a `ConstantShiftedFunction`).
  - `other`: `Any`
    > the addend
  - `:returns`: `DifferentiableFunction`
    > the sum function


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__radd__" class="docs-object-method">&nbsp;</a> 
```python
__radd__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L154?message=Update%20Docs)]
</div>
**LLM Docstring**

Right addition, delegating to `__add__`.
  - `other`: `Any`
    > the addend
  - `:returns`: `DifferentiableFunction`
    > the sum function


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L165)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L165?message=Update%20Docs)]
</div>
**LLM Docstring**

Multiply by another differentiable function (building/merging a
`FunctionProduct`) or a constant (building a `ConstantScaledFunction`).
  - `other`: `Any`
    > the multiplier
  - `:returns`: `DifferentiableFunction`
    > the product function


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__truediv__" class="docs-object-method">&nbsp;</a> 
```python
__truediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L188?message=Update%20Docs)]
</div>
**LLM Docstring**

Divide by another differentiable function (multiplying by its reciprocal) or a
constant.
  - `other`: `Any`
    > the divisor
  - `:returns`: `DifferentiableFunction`
    > the quotient function


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__rtruediv__" class="docs-object-method">&nbsp;</a> 
```python
__rtruediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L211)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L211?message=Update%20Docs)]
</div>
**LLM Docstring**

Right division (`other / self`), via the reciprocal of this function.
  - `other`: `Any`
    > the numerator
  - `:returns`: `DifferentiableFunction`
    > the quotient function


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__rmul__" class="docs-object-method">&nbsp;</a> 
```python
__rmul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L222)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L222?message=Update%20Docs)]
</div>
**LLM Docstring**

Right multiplication, delegating to `__mul__`.
  - `other`: `Any`
    > the multiplier
  - `:returns`: `DifferentiableFunction`
    > the product function


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__neg__" class="docs-object-method">&nbsp;</a> 
```python
__neg__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L233)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L233?message=Update%20Docs)]
</div>
**LLM Docstring**

Negate the function (unwrapping a double negation).
  - `:returns`: `DifferentiableFunction`
    > the negated function


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.flip" class="docs-object-method">&nbsp;</a> 
```python
flip(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L247)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L247?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the reciprocal (`1 / self`) as a `ReciprocalFunction`.
  - `:returns`: `ReciprocalFunction`
    > the reciprocal function
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L19?message=Update%20Docs)   
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