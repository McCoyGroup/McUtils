## <a id="McUtils.Zachary.Polynomials.PureMonicPolynomial">PureMonicPolynomial</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials.py#L1677)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L1677?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Polynomials.PureMonicPolynomial.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, terms: dict, prefactor=1, canonicalize=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials.py#L1678)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L1678?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a monic-monomial polynomial from a term mapping, canonicalizing (and
merging) the monomial keys by default.
  - `terms`: `dict`
    > the `{monomial_key_tuple: coefficient}` mapping
  - `prefactor`: `float`
    > an overall scalar multiplier
  - `canonicalize`: `bool`
    > canonicalize and merge the keys


<a id="McUtils.Zachary.Polynomials.PureMonicPolynomial.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1700)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1700?message=Update%20Docs)]
</div>
**LLM Docstring**

Not supported: monic-monomial polynomials have no dense counterpart.


<a id="McUtils.Zachary.Polynomials.PureMonicPolynomial.as_dense" class="docs-object-method">&nbsp;</a> 
```python
as_dense(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1711)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1711?message=Update%20Docs)]
</div>
**LLM Docstring**

Not supported: monic-monomial polynomials have no dense counterpart.


<a id="McUtils.Zachary.Polynomials.PureMonicPolynomial.shift" class="docs-object-method">&nbsp;</a> 
```python
shift(self, shift) -> McUtils.Zachary.Polynomials.DensePolynomial: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1721)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1721?message=Update%20Docs)]
</div>
**LLM Docstring**

Not supported: monic-monomial polynomials have no dense counterpart.
  - `shift`: `Any`
    > the (ignored) shift


<a id="McUtils.Zachary.Polynomials.PureMonicPolynomial.monomial" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
monomial(cls, idx, value=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1732)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1732?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a single-term polynomial for one monomial key.
  - `idx`: `Any`
    > the monomial key
  - `value`: `Any`
    > the coefficient
  - `:returns`: `PureMonicPolynomial`
    > the monomial polynomial


<a id="McUtils.Zachary.Polynomials.PureMonicPolynomial.key_hash" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
key_hash(cls, monomial_tuple): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1746)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1746?message=Update%20Docs)]
</div>
**LLM Docstring**

Cheap order-independent hash of a monomial key (sum of the per-index hashes),
used to quickly test key equivalence.
  - `monomial_tuple`: `tuple`
    > the monomial key
  - `:returns`: `int`
    > the hash


<a id="McUtils.Zachary.Polynomials.PureMonicPolynomial.canonical_key" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonical_key(cls, monomial_tuple): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1763)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1763?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract: put a monomial key into canonical (sorted) form so equivalent keys
compare equal.
  - `monomial_tuple`: `tuple`
    > the monomial key
  - `:returns`: `tuple`
    > the canonicalized key


<a id="McUtils.Zachary.Polynomials.PureMonicPolynomial.direct_multiproduct" class="docs-object-method">&nbsp;</a> 
```python
direct_multiproduct(self, other, key_value_generator): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1779)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1779?message=Update%20Docs)]
</div>
**LLM Docstring**

Multiply with another monic polynomial using a generator that yields the
`(key, value)` contributions for each pair of terms, merging canonicalized keys.
  - `other`: `PureMonicPolynomial`
    > the other polynomial
  - `key_value_generator`: `Callable`
    > yields `(key, value)` pairs for each term pair
  - `:returns`: `PureMonicPolynomial`
    > the product polynomial


<a id="McUtils.Zachary.Polynomials.PureMonicPolynomial.direct_product" class="docs-object-method">&nbsp;</a> 
```python
direct_product(self, other, key_func=None, mul=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1822)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1822?message=Update%20Docs)]
</div>
**LLM Docstring**

Multiply with another monic polynomial (or scalar) using optional key-combining
and value-multiplying callbacks, merging canonicalized keys.
  - `other`: `Any`
    > the other polynomial or a scalar
  - `key_func`: `Callable | None`
    > combines two keys into the product key (concatenation by default)
  - `mul`: `Callable | None`
    > multiplies two coefficients (ordinary product by default)
  - `:returns`: `PureMonicPolynomial`
    > the product polynomial


<a id="McUtils.Zachary.Polynomials.PureMonicPolynomial.rebuild" class="docs-object-method">&nbsp;</a> 
```python
rebuild(self, new_terms, prefactor=None, canonicalize=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1871)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1871?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a new polynomial of the same type from a term mapping, inheriting the
prefactor by default.
  - `new_terms`: `dict`
    > the new term mapping
  - `prefactor`: `float | None`
    > the prefactor (inherited if omitted)
  - `canonicalize`: `bool | None`
    > canonicalize the keys (off by default)
  - `:returns`: `PureMonicPolynomial`
    > the rebuilt polynomial


<a id="McUtils.Zachary.Polynomials.PureMonicPolynomial.filter" class="docs-object-method">&nbsp;</a> 
```python
filter(self, keys, mode='match'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1892)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1892?message=Update%20Docs)]
</div>
**LLM Docstring**

Filter the polynomial's terms by their monomial keys under one of three modes.
  - `keys`: `Any`
    > the keys to test against
  - `mode`: `str`
    > `'match'` (exact key sets), `'include'` (only these keys), or `'exclude'`
  - `:returns`: `PureMonicPolynomial`
    > the filtered polynomial


<a id="McUtils.Zachary.Polynomials.PureMonicPolynomial.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1982)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/PureMonicPolynomial.py#L1982?message=Update%20Docs)]
</div>
**LLM Docstring**

Multiply by another monic polynomial (or scalar) via `direct_product`.
  - `other`: `Any`
    > the multiplier
  - `:returns`: `PureMonicPolynomial`
    > the product polynomial
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L1677?message=Update%20Docs)   
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