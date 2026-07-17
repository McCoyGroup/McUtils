## <a id="McUtils.Zachary.Polynomials.DensePolynomial">DensePolynomial</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials.py#L149)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L149?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials.py#L155)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L155?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a dense n-dimensional polynomial from a coefficient tensor, with a deferred
scalar prefactor and variable shift.

The coefficient tensor is indexed by per-variable powers; a leading `stack_dim`
axes hold a batch/stack of polynomials. The `prefactor` and `shift` are applied
lazily the first time the coefficients are materialized.
  - `coeffs`: `np.ndarray | SparseArray`
    > the coefficient tensor (dense or `SparseArray`)
  - `prefactor`: `float | None`
    > an overall scalar multiplier (applied lazily)
  - `shift`: `np.ndarray | None`
    > a per-variable shift to apply (applied lazily)
  - `stack_dim`: `int`
    > the number of leading stack/batch axes


<a id="McUtils.Zachary.Polynomials.DensePolynomial.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L187)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L187?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation showing the coefficient shape and scaling.
  - `:returns`: `str`
    > the representation


<a id="McUtils.Zachary.Polynomials.DensePolynomial.from_tensors" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_tensors(cls, tensors, prefactor=None, shift=None, rescale=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L198)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L198?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a `DensePolynomial` from a list of derivative/coefficient tensors (one per
order), condensing them into a single coefficient tensor.
  - `tensors`: `list`
    > the per-order coefficient tensors
  - `prefactor`: `float | None`
    > an overall scalar multiplier
  - `shift`: `np.ndarray | None`
    > a per-variable shift
  - `rescale`: `bool`
    > divide each tensor entry by its permutation count
  - `:returns`: `DensePolynomial`
    > the polynomial


<a id="McUtils.Zachary.Polynomials.DensePolynomial.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L221)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L221?message=Update%20Docs)]
</div>
**LLM Docstring**

The shape of the coefficient tensor (including the stack axes).
  - `:returns`: `tuple`
    > the coefficient shape


<a id="McUtils.Zachary.Polynomials.DensePolynomial.scaling" class="docs-object-method">&nbsp;</a> 
```python
@property
scaling(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L233)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L233?message=Update%20Docs)]
</div>
**LLM Docstring**

The overall scalar prefactor (1 when unset). Setting it stores a new deferred
prefactor.
  - `:returns`: `float`
    > the scaling factor


<a id="McUtils.Zachary.Polynomials.DensePolynomial.coeffs" class="docs-object-method">&nbsp;</a> 
```python
@property
coeffs(self) -> 'np.ndarray|SparseArray': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L259)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L259?message=Update%20Docs)]
</div>
**LLM Docstring**

The materialized coefficient tensor, applying (and then clearing) any deferred
shift and prefactor on first access. Setting it replaces the raw coefficients.
  - `:returns`: `np.ndarray | SparseArray`
    > the coefficient tensor


<a id="McUtils.Zachary.Polynomials.DensePolynomial.coordinate_dim" class="docs-object-method">&nbsp;</a> 
```python
@property
coordinate_dim(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L291)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L291?message=Update%20Docs)]
</div>
**LLM Docstring**

The number of polynomial variables (the coefficient rank minus the stack axes).
  - `:returns`: `int`
    > the coordinate dimension


<a id="McUtils.Zachary.Polynomials.DensePolynomial.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other) -> 'DensePolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L502)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L502?message=Update%20Docs)]
</div>
**LLM Docstring**

Multiply this polynomial by another (convolving their coefficient tensors) or by
a scalar.
  - `other`: `Any`
    > the multiplier polynomial or scalar
  - `:returns`: `DensePolynomial`
    > the product polynomial (or `0`/`self` for the scalar special cases)


<a id="McUtils.Zachary.Polynomials.DensePolynomial.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other) -> 'DensePolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L659)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L659?message=Update%20Docs)]
</div>
**LLM Docstring**

Add another polynomial (aligning and padding their coefficient tensors) or a
scalar (added to the constant term).
  - `other`: `Any`
    > the addend polynomial or scalar
  - `:returns`: `DensePolynomial`
    > the sum polynomial


<a id="McUtils.Zachary.Polynomials.DensePolynomial.shift" class="docs-object-method">&nbsp;</a> 
```python
shift(self, shift) -> 'DensePolynomial': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L716)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L716?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the polynomial with an added deferred variable shift (`p(x + shift)`).
  - `shift`: `Any`
    > the per-variable shift (scalar or vector)
  - `:returns`: `DensePolynomial`
    > the shifted polynomial


<a id="McUtils.Zachary.Polynomials.DensePolynomial.compute_shifted_coeffs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
compute_shifted_coeffs(cls, poly_coeffs, shift, stack_dim=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L735)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L735?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the coefficient tensor of a polynomial after a variable shift
(`p(x + shift)`), via a factorial-weighted convolution of the coefficients with
the shift powers (a Taylor re-expansion).
  - `poly_coeffs`: `np.ndarray`
    > the original coefficient tensor
  - `shift`: `np.ndarray | float`
    > the per-variable shift
  - `stack_dim`: `int`
    > the number of leading stack axes
  - `:returns`: `np.ndarray`
    > the shifted coefficient tensor


<a id="McUtils.Zachary.Polynomials.DensePolynomial.fill_tensors" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fill_tensors(self, tensors, idx, value, stack_dim, pcache, permute, rescale): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L843)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L843?message=Update%20Docs)]
</div>
**LLM Docstring**

Scatter a single coefficient value into the per-order derivative tensors,
filling every index permutation (optionally rescaling by the permutation count)
so the resulting tensors are symmetric.
  - `tensors`: `list`
    > the per-order tensors being filled (modified in place)
  - `idx`: `tuple`
    > the coefficient's power index (with any stack prefix)
  - `value`: `Any`
    > the coefficient value
  - `stack_dim`: `int`
    > the number of leading stack axes
  - `pcache`: `dict`
    > a cache of index permutations
  - `permute`: `bool`
    > fill all index permutations
  - `rescale`: `bool`
    > divide the value across its permutations


<a id="McUtils.Zachary.Polynomials.DensePolynomial.extract_tensors" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
extract_tensors(cls, coeffs, stack_dim=None, permute=True, rescale=True, cutoff=1e-15): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L902)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L902?message=Update%20Docs)]
</div>
**LLM Docstring**

Decompose a coefficient tensor into a list of per-order (symmetric) derivative
tensors, scattering each nonzero coefficient across its index permutations.
  - `coeffs`: `np.ndarray | SparseArray`
    > the coefficient tensor (dense or sparse)
  - `stack_dim`: `int | None`
    > the number of leading stack axes
  - `permute`: `bool`
    > fill all index permutations
  - `rescale`: `bool`
    > divide each value across its permutations
  - `cutoff`: `float`
    > the magnitude below which dense entries are treated as zero
  - `:returns`: `list`
    > the per-order tensors (index 0 is the constant term)


<a id="McUtils.Zachary.Polynomials.DensePolynomial.condense_tensors" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
condense_tensors(cls, tensors, rescale=True, allow_sparse=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L959)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L959?message=Update%20Docs)]
</div>
**LLM Docstring**

Collapse a list of per-order derivative tensors back into a single (dense or
sparse) coefficient tensor, choosing a sparse representation when the density is
low.
  - `tensors`: `list`
    > the per-order tensors
  - `rescale`: `bool`
    > multiply each entry by its permutation count
  - `allow_sparse`: `bool`
    > allow returning a `SparseArray` when sparse enough
  - `:returns`: `tuple`
    > `(coefficient_tensor, stack_dim)`


<a id="McUtils.Zachary.Polynomials.DensePolynomial.coefficient_tensors" class="docs-object-method">&nbsp;</a> 
```python
@property
coefficient_tensors(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1040)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1040?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-order (permutation-rescaled) derivative tensors of the polynomial,
computed lazily.
  - `:returns`: `list`
    > the per-order coefficient tensors


<a id="McUtils.Zachary.Polynomials.DensePolynomial.unscaled_coefficient_tensors" class="docs-object-method">&nbsp;</a> 
```python
@property
unscaled_coefficient_tensors(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1055)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1055?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-order derivative tensors without permutation rescaling, computed lazily.
  - `:returns`: `list`
    > the per-order unscaled coefficient tensors


<a id="McUtils.Zachary.Polynomials.DensePolynomial.transform" class="docs-object-method">&nbsp;</a> 
```python
transform(self, lin_transf): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1069)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1069?message=Update%20Docs)]
</div>
Applies (for now) a linear transformation to the polynomial


<a id="McUtils.Zachary.Polynomials.DensePolynomial.outer" class="docs-object-method">&nbsp;</a> 
```python
outer(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1086)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1086?message=Update%20Docs)]
</div>
**LLM Docstring**

Form the outer-product polynomial of this one with another coefficient tensor
(no stack dimensions supported).
  - `other`: `Any`
    > the other polynomial/coefficients
  - `:returns`: `DensePolynomial`
    > the outer-product polynomial


<a id="McUtils.Zachary.Polynomials.DensePolynomial.deriv" class="docs-object-method">&nbsp;</a> 
```python
deriv(self, coord): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1130?message=Update%20Docs)]
</div>
**LLM Docstring**

Differentiate the polynomial with respect to one coordinate.
  - `coord`: `int`
    > the coordinate index
  - `:returns`: `DensePolynomial | int`
    > the derivative polynomial (or `0` if constant in that coordinate)


<a id="McUtils.Zachary.Polynomials.DensePolynomial.grad" class="docs-object-method">&nbsp;</a> 
```python
grad(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1309)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1309?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the gradient polynomial, whose leading stack axis indexes the derivative
with respect to each coordinate.
  - `:returns`: `DensePolynomial`
    > the gradient polynomial


<a id="McUtils.Zachary.Polynomials.DensePolynomial.clip" class="docs-object-method">&nbsp;</a> 
```python
clip(self, threshold=1e-15): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1326)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1326?message=Update%20Docs)]
</div>
**LLM Docstring**

Drop coefficients below a magnitude threshold, returning a trimmed polynomial
(or `0` if everything is clipped).
  - `threshold`: `float`
    > the magnitude cutoff
  - `:returns`: `DensePolynomial | int`
    > the clipped polynomial (or `0`)


<a id="McUtils.Zachary.Polynomials.DensePolynomial.make_sparse_backed" class="docs-object-method">&nbsp;</a> 
```python
make_sparse_backed(self, threshold=1e-15): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1350)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials/DensePolynomial.py#L1350?message=Update%20Docs)]
</div>
**LLM Docstring**

Return an equivalent polynomial whose coefficients are stored as a `SparseArray`
(after clipping small entries).
  - `threshold`: `float`
    > the clipping magnitude cutoff
  - `:returns`: `DensePolynomial`
    > the sparse-backed polynomial
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Polynomials/DensePolynomial.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Polynomials/DensePolynomial.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Polynomials/DensePolynomial.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Polynomials/DensePolynomial.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Polynomials.py#L149?message=Update%20Docs)   
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