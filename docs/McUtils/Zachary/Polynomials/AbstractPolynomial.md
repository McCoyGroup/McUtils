## <a id="McUtils.Zachary.Polynomials.AbstractPolynomial">AbstractPolynomial</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L15?message=Update%20Docs)]
</div>

Provides the general interface an abstract polynomial needs ot support, including
multiplication, addition, shifting, access of coefficients, and evaluation







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.scaling" class="docs-object-method">&nbsp;</a> 
```python
@property
scaling(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L21)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L21?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: the overall scalar prefactor multiplying the polynomial.
  - `:returns`: `float`
    > the scaling factor


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other) -> 'AbstractPolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L34)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L34?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: multiply this polynomial by another polynomial or a scalar.
  - `other`: `Any`
    > the multiplier
  - `:returns`: `AbstractPolynomial`
    > the product polynomial


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other) -> 'AbstractPolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L47)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L47?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: add another polynomial or a scalar to this one.
  - `other`: `Any`
    > the addend
  - `:returns`: `AbstractPolynomial`
    > the sum polynomial


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.shift" class="docs-object-method">&nbsp;</a> 
```python
shift(self, shift) -> 'AbstractPolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L60)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L60?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: return the polynomial shifted in its variables (i.e. `p(x + shift)`).
  - `shift`: `Any`
    > the per-variable shift
  - `:returns`: `AbstractPolynomial`
    > the shifted polynomial


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__rmul__" class="docs-object-method">&nbsp;</a> 
```python
__rmul__(self, other) -> 'AbstractPolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L73)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L73?message=Update%20Docs)]
</div>
**LLM Docstring**

Right multiplication, delegating to `__mul__` (multiplication is commutative
here).
  - `other`: `Any`
    > the multiplier
  - `:returns`: `AbstractPolynomial`
    > the product polynomial


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__radd__" class="docs-object-method">&nbsp;</a> 
```python
__radd__(self, other) -> 'AbstractPolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L86)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L86?message=Update%20Docs)]
</div>
**LLM Docstring**

Right addition, delegating to `__add__`.
  - `other`: `Any`
    > the addend
  - `:returns`: `AbstractPolynomial`
    > the sum polynomial


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__truediv__" class="docs-object-method">&nbsp;</a> 
```python
__truediv__(self, other) -> 'AbstractPolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L98)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L98?message=Update%20Docs)]
</div>
**LLM Docstring**

Divide the polynomial by a scalar (multiply by its reciprocal).
  - `other`: `Any`
    > the scalar divisor
  - `:returns`: `AbstractPolynomial`
    > the scaled polynomial


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__neg__" class="docs-object-method">&nbsp;</a> 
```python
__neg__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L110)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L110?message=Update%20Docs)]
</div>
**LLM Docstring**

Negate the polynomial.
  - `:returns`: `AbstractPolynomial`
    > the negated polynomial


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__sub__" class="docs-object-method">&nbsp;</a> 
```python
__sub__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L121)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L121?message=Update%20Docs)]
</div>
**LLM Docstring**

Subtract another polynomial or scalar (add its negation).
  - `other`: `Any`
    > the subtrahend
  - `:returns`: `AbstractPolynomial`
    > the difference polynomial


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__rsub__" class="docs-object-method">&nbsp;</a> 
```python
__rsub__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L133)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L133?message=Update%20Docs)]
</div>
**LLM Docstring**

Right subtraction (`other - self`), via negation and addition.
  - `other`: `Any`
    > the minuend
  - `:returns`: `AbstractPolynomial`
    > the difference polynomial
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Polynomials/AbstractPolynomial.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Polynomials/AbstractPolynomial.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Polynomials/AbstractPolynomial.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Polynomials/AbstractPolynomial.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L15?message=Update%20Docs)   
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