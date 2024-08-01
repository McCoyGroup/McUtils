## <a id="McUtils.Zachary.Polynomials.SparsePolynomial">SparsePolynomial</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials.py#L799)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials.py#L799?message=Update%20Docs)]
</div>

A semi-symbolic representation of a polynomial of tensor
coefficients







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Polynomials.SparsePolynomial.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, terms: dict, prefactor=1, ndim=None, canonicalize=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/SparsePolynomial.py#L804)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/SparsePolynomial.py#L804?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.scaling" class="docs-object-method">&nbsp;</a> 
```python
@property
scaling(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/SparsePolynomial.py#L810)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/SparsePolynomial.py#L810?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.expand" class="docs-object-method">&nbsp;</a> 
```python
expand(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/SparsePolynomial.py#L817)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/SparsePolynomial.py#L817?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.monomial" class="docs-object-method">&nbsp;</a> 
```python
monomial(idx, value=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/SparsePolynomial.py#L823)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/SparsePolynomial.py#L823?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/SparsePolynomial.py#L826)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/SparsePolynomial.py#L826?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/SparsePolynomial.py#L829)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/SparsePolynomial.py#L829?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/SparsePolynomial.py#L850)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/SparsePolynomial.py#L850?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/SparsePolynomial.py#L895)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/SparsePolynomial.py#L895?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.as_dense" class="docs-object-method">&nbsp;</a> 
```python
as_dense(self) -> McUtils.Zachary.Polynomials.DensePolynomial: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/SparsePolynomial.py#L908)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/SparsePolynomial.py#L908?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.shift" class="docs-object-method">&nbsp;</a> 
```python
shift(self, shift) -> 'SparsePolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/SparsePolynomial.py#L947)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/SparsePolynomial.py#L947?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Zachary/Polynomials/SparsePolynomial.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Zachary/Polynomials/SparsePolynomial.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Zachary/Polynomials/SparsePolynomial.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Zachary/Polynomials/SparsePolynomial.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials.py#L799?message=Update%20Docs)   
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