## <a id="McUtils.Zachary.Polynomials.SparsePolynomial">SparsePolynomial</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials.py#L1370)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L1370?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials.py#L1376)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L1376?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a semi-symbolic sparse polynomial from a `{sorted_index_tuple: coefficient}`
term mapping.
  - `terms`: `dict`
    > the term mapping (keys are sorted variable-index tuples)
  - `prefactor`: `float`
    > an overall scalar multiplier
  - `ndim`: `int | None`
    > the number of variables (inferred if omitted)
  - `canonicalize`: `bool`
    > accepted for interface parity


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.scaling" class="docs-object-method">&nbsp;</a> 
```python
@property
scaling(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1397)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1397?message=Update%20Docs)]
</div>
**LLM Docstring**

The overall scalar prefactor (1 when unset). Setting it stores a new prefactor.
  - `:returns`: `float`
    > the scaling factor


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.expand" class="docs-object-method">&nbsp;</a> 
```python
expand(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1421)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1421?message=Update%20Docs)]
</div>
**LLM Docstring**

Fold the prefactor into the term coefficients, returning an equivalent polynomial
with unit prefactor.
  - `:returns`: `SparsePolynomial`
    > the expanded polynomial


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.monomial" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
monomial(cls, idx, value=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1437)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1437?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a single-term polynomial for the monomial at the given index.
  - `idx`: `tuple`
    > the monomial's variable-index tuple
  - `value`: `Any`
    > the coefficient
  - `:returns`: `SparsePolynomial`
    > the monomial polynomial


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1452)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1452?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation showing the terms and prefactor.
  - `:returns`: `str`
    > the representation


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1463)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1463?message=Update%20Docs)]
</div>
**LLM Docstring**

Multiply by another sparse polynomial (merging index tuples and summing
coefficients) or by a scalar.
  - `other`: `Any`
    > the multiplier polynomial or scalar
  - `:returns`: `SparsePolynomial`
    > the product polynomial


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1495)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1495?message=Update%20Docs)]
</div>
**LLM Docstring**

Add another sparse polynomial (merging matching terms) or a scalar (added to the
constant term).
  - `other`: `Any`
    > the addend polynomial or scalar
  - `:returns`: `SparsePolynomial | int`
    > the sum polynomial (or `0` if everything cancels)


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1566)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1566?message=Update%20Docs)]
</div>
**LLM Docstring**

The dense coefficient shape implied by the terms (per-variable max power + 1),
computed lazily.
  - `:returns`: `tuple`
    > the dense shape


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.as_dense" class="docs-object-method">&nbsp;</a> 
```python
as_dense(self) -> McUtils.Zachary.Polynomials.DensePolynomial: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1589)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1589?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert to an equivalent `DensePolynomial`, filling a dense coefficient tensor
from the terms.
  - `:returns`: `DensePolynomial`
    > the dense polynomial


<a id="McUtils.Zachary.Polynomials.SparsePolynomial.shift" class="docs-object-method">&nbsp;</a> 
```python
shift(self, shift) -> 'SparsePolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1638)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/SparsePolynomial.py#L1638?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the polynomial shifted in its variables (`p(x + shift)`), expanding each
term via the binomial theorem.
  - `shift`: `np.ndarray`
    > the per-variable shift
  - `:returns`: `SparsePolynomial`
    > the shifted polynomial
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Polynomials/SparsePolynomial.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Polynomials/SparsePolynomial.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Polynomials/SparsePolynomial.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Polynomials/SparsePolynomial.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L1370?message=Update%20Docs)   
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