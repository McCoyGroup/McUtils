## <a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial">PureMonicPolynomial</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials.py#L975)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L975?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, terms: dict, prefactor=1, canonicalize=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L976)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L976?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L985)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L985?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial.as_dense" class="docs-object-method">&nbsp;</a> 
```python
as_dense(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L988)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L988?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial.shift" class="docs-object-method">&nbsp;</a> 
```python
shift(self, shift) -> McUtils.McUtils.Zachary.Polynomials.DensePolynomial: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L990)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L990?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial.monomial" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
monomial(cls, idx, value=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L993)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L993?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial.key_hash" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
key_hash(cls, monomial_tuple): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L997)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L997?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial.canonical_key" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonical_key(cls, monomial_tuple): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L1003)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L1003?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial.direct_multiproduct" class="docs-object-method">&nbsp;</a> 
```python
direct_multiproduct(self, other, key_value_generator): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1008)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1008?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial.direct_product" class="docs-object-method">&nbsp;</a> 
```python
direct_product(self, other, key_func=None, mul=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1036)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1036?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial.rebuild" class="docs-object-method">&nbsp;</a> 
```python
rebuild(self, new_terms, prefactor=None, canonicalize=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1071)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1071?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial.filter" class="docs-object-method">&nbsp;</a> 
```python
filter(self, keys, mode='match'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1077)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1077?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Polynomials.PureMonicPolynomial.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1127)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1127?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Polynomials/PureMonicPolynomial.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Polynomials/PureMonicPolynomial.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Polynomials/PureMonicPolynomial.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Polynomials/PureMonicPolynomial.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L975?message=Update%20Docs)   
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