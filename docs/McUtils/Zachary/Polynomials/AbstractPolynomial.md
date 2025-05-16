## <a id="McUtils.Zachary.Polynomials.AbstractPolynomial">AbstractPolynomial</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L14?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L20?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other) -> 'AbstractPolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L25)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L25?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other) -> 'AbstractPolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L28)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L28?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.shift" class="docs-object-method">&nbsp;</a> 
```python
shift(self, shift) -> 'AbstractPolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L32)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L32?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__rmul__" class="docs-object-method">&nbsp;</a> 
```python
__rmul__(self, other) -> 'AbstractPolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L36)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L36?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__radd__" class="docs-object-method">&nbsp;</a> 
```python
__radd__(self, other) -> 'AbstractPolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L38)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L38?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__truediv__" class="docs-object-method">&nbsp;</a> 
```python
__truediv__(self, other) -> 'AbstractPolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L40)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L40?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__neg__" class="docs-object-method">&nbsp;</a> 
```python
__neg__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L42)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L42?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__sub__" class="docs-object-method">&nbsp;</a> 
```python
__sub__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L44)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L44?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.AbstractPolynomial.__rsub__" class="docs-object-method">&nbsp;</a> 
```python
__rsub__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L46)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/AbstractPolynomial.py#L46?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L14?message=Update%20Docs)   
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