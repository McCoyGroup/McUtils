## <a id="McUtils.Zachary.DifferentiableFunctions.PolynomialFunction">PolynomialFunction</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions.py#L614)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L614?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.DifferentiableFunctions.PolynomialFunction.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, taylor_poly: McUtils.Zachary.Taylor.FunctionExpansions.FunctionExpansion, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions.py#L615)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L615?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap a `FunctionExpansion` (Taylor polynomial) as a differentiable function.
  - `taylor_poly`: `FunctionExpansion`
    > the backing expansion
  - `inds`: `Sequence[int] | None`
    > the coordinate indices this function acts on


<a id="McUtils.Zachary.DifferentiableFunctions.PolynomialFunction.from_coefficients" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_coefficients(cls, coeffs, center=None, ref=0, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L629)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L629?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a polynomial function from a coefficient tensor, an expansion center, and a
reference value.
  - `coeffs`: `Any`
    > the coefficient tensors
  - `center`: `Any`
    > the expansion center
  - `ref`: `Any`
    > the reference (constant) value
  - `inds`: `Sequence[int] | None`
    > the coordinate indices
  - `:returns`: `PolynomialFunction`
    > the polynomial function


<a id="McUtils.Zachary.DifferentiableFunctions.PolynomialFunction.evaluate" class="docs-object-method">&nbsp;</a> 
```python
evaluate(self, coords, order=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/PolynomialFunction.py#L655)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/PolynomialFunction.py#L655?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate the backing polynomial's expansion at the given coordinates.
  - `coords`: `np.ndarray`
    > the coordinates
  - `order`: `int`
    > the highest derivative order
  - `:returns`: `list[np.ndarray]`
    > the expansion tensors


<a id="McUtils.Zachary.DifferentiableFunctions.PolynomialFunction.get_children" class="docs-object-method">&nbsp;</a> 
```python
get_children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/PolynomialFunction.py#L669)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/PolynomialFunction.py#L669?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the sub-functions of this polynomial (a leaf).
  - `:returns`: `list[DifferentiableFunction]`
    > the child functions
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/DifferentiableFunctions/PolynomialFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/DifferentiableFunctions/PolynomialFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/DifferentiableFunctions/PolynomialFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/DifferentiableFunctions/PolynomialFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L614?message=Update%20Docs)   
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