## <a id="McUtils.Zachary.Polynomials.DensePolynomial">DensePolynomial</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials.py#L54)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials.py#L54?message=Update%20Docs)]
</div>

A straightforward dense n-dimensional polynomial data structure with
multiplications and shifts







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Polynomials.DensePolynomial.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, coeffs, prefactor=None, shift=None, stack_dim=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L59)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L59?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L71)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L71?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.from_tensors" class="docs-object-method">&nbsp;</a> 
```python
from_tensors(tensors, prefactor=None, shift=None, rescale=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L73)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L73?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L79)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L79?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.scaling" class="docs-object-method">&nbsp;</a> 
```python
@property
scaling(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L83)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L83?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.coeffs" class="docs-object-method">&nbsp;</a> 
```python
@property
coeffs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L90)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L90?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.coordinate_dim" class="docs-object-method">&nbsp;</a> 
```python
@property
coordinate_dim(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L103)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L103?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other) -> 'DensePolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L244)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L244?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other) -> 'DensePolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L331)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L331?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.shift" class="docs-object-method">&nbsp;</a> 
```python
shift(self, shift) -> 'DensePolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L378)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L378?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.compute_shifted_coeffs" class="docs-object-method">&nbsp;</a> 
```python
compute_shifted_coeffs(poly_coeffs, shift, stack_dim=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L387)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L387?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.fill_tensors" class="docs-object-method">&nbsp;</a> 
```python
fill_tensors(tensors, idx, value, stack_dim, pcache, permute, rescale): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L480)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L480?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.extract_tensors" class="docs-object-method">&nbsp;</a> 
```python
extract_tensors(coeffs, stack_dim=None, permute=True, rescale=True, cutoff=1e-15): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L517)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L517?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.condense_tensors" class="docs-object-method">&nbsp;</a> 
```python
condense_tensors(tensors, rescale=True, allow_sparse=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L554)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L554?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.coefficient_tensors" class="docs-object-method">&nbsp;</a> 
```python
@property
coefficient_tensors(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L619)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L619?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.unscaled_coefficient_tensors" class="docs-object-method">&nbsp;</a> 
```python
@property
unscaled_coefficient_tensors(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L624)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L624?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.transform" class="docs-object-method">&nbsp;</a> 
```python
transform(self, lin_transf): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L629)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L629?message=Update%20Docs)]
</div>
Applies (for now) a linear transformation to the polynomial


<a id="McUtils.Zachary.Polynomials.DensePolynomial.outer" class="docs-object-method">&nbsp;</a> 
```python
outer(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L646)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L646?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.deriv" class="docs-object-method">&nbsp;</a> 
```python
deriv(self, coord): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L664)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L664?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.grad" class="docs-object-method">&nbsp;</a> 
```python
grad(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L770)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L770?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.clip" class="docs-object-method">&nbsp;</a> 
```python
clip(self, threshold=1e-15): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L778)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L778?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Polynomials.DensePolynomial.make_sparse_backed" class="docs-object-method">&nbsp;</a> 
```python
make_sparse_backed(self, threshold=1e-15): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Polynomials/DensePolynomial.py#L791)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials/DensePolynomial.py#L791?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Zachary/Polynomials/DensePolynomial.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Zachary/Polynomials/DensePolynomial.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Zachary/Polynomials/DensePolynomial.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Zachary/Polynomials/DensePolynomial.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Polynomials.py#L54?message=Update%20Docs)   
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