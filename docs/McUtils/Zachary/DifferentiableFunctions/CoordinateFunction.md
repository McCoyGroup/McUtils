## <a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction">CoordinateFunction</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions.py#L1007)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L1007?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, conversion, expr: McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions.py#L1008)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L1008?message=Update%20Docs)]
</div>
**LLM Docstring**

Compose a coordinate-system conversion with a differentiable expression, so the
expression (defined in internal coordinates) can be evaluated on raw (e.g.
Cartesian) inputs.
  - `conversion`: `Any`
    > the coordinate conversion (a callable or an internal-coordinate spec)
  - `expr`: `DifferentiableFunction`
    > the expression in the converted coordinates


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.canonicalize_conversion" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_conversion(cls, conv): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1024)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1024?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize a conversion specification into `(canonical_spec, conversion_function)`,
building an internal-coordinate conversion function when a coordinate spec is
given.
  - `conv`: `Any`
    > the conversion (callable or internal-coordinate spec)
  - `:returns`: `tuple`
    > `(canonical_spec, conversion_function)`


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, coords, order=0, preconverted=False, reexpress=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1045)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1045?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate the composed function: convert the input coordinates (to the requested
order), evaluate the expression, and re-express its derivatives back in the input
coordinates via the chain rule.
  - `coords`: `np.ndarray`
    > the input coordinates
  - `order`: `int`
    > the highest derivative order
  - `preconverted`: `bool`
    > treat `coords` as already in the expression's coordinates
  - `reexpress`: `bool`
    > re-express the derivatives in the input coordinates
  - `:returns`: `tuple`
    > `(coordinate_expansion, expression_expansion)`


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.merge_conversion_functions" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
merge_conversion_functions(cls, conv_1, conv_2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1082)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1082?message=Update%20Docs)]
</div>
**LLM Docstring**

Merge two coordinate-conversion specs into one, returning the reindexing that
maps the second spec's coordinates onto the merged set.
  - `conv_1`: `Any`
    > the first conversion spec
  - `conv_2`: `Any`
    > the second conversion spec
  - `:returns`: `tuple`
    > `(reindexing_for_conv_2, merged_conversion)`


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1110)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1110?message=Update%20Docs)]
</div>
**LLM Docstring**

Add another coordinate function (merging their conversions and reindexing) or a
constant.
  - `other`: `Any`
    > the addend
  - `:returns`: `CoordinateFunction`
    > the sum coordinate function


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.__radd__" class="docs-object-method">&nbsp;</a> 
```python
__radd__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1129)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1129?message=Update%20Docs)]
</div>
**LLM Docstring**

Right addition, delegating to `__add__`.
  - `other`: `Any`
    > the addend
  - `:returns`: `CoordinateFunction`
    > the sum coordinate function


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1140)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1140?message=Update%20Docs)]
</div>
**LLM Docstring**

Multiply by another coordinate function (merging their conversions) or a
constant.
  - `other`: `Any`
    > the multiplier
  - `:returns`: `CoordinateFunction`
    > the product coordinate function


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.__rmul__" class="docs-object-method">&nbsp;</a> 
```python
__rmul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1159)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1159?message=Update%20Docs)]
</div>
**LLM Docstring**

Right multiplication, delegating to `__mul__`.
  - `other`: `Any`
    > the multiplier
  - `:returns`: `CoordinateFunction`
    > the product coordinate function


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.__truediv__" class="docs-object-method">&nbsp;</a> 
```python
__truediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1170)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1170?message=Update%20Docs)]
</div>
**LLM Docstring**

Divide by another coordinate function (merging their conversions) or a constant.
  - `other`: `Any`
    > the divisor
  - `:returns`: `CoordinateFunction`
    > the quotient coordinate function


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.__rtruediv__" class="docs-object-method">&nbsp;</a> 
```python
__rtruediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1188?message=Update%20Docs)]
</div>
**LLM Docstring**

Right division (`other / self`).
  - `other`: `Any`
    > the numerator
  - `:returns`: `CoordinateFunction`
    > the quotient coordinate function


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.__neg__" class="docs-object-method">&nbsp;</a> 
```python
__neg__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1199)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.py#L1199?message=Update%20Docs)]
</div>
**LLM Docstring**

Negate the coordinate function.
  - `:returns`: `CoordinateFunction`
    > the negated coordinate function


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.polynomial" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
polynomial(cls, coord_spec, *, coeffs, center, ref): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1210)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1210?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a coordinate function from a polynomial expression in the given
coordinate(s) (1-D `Poly1D` or multi-D `PolynomialFunction`).
  - `coord_spec`: `Any`
    > the coordinate spec the polynomial acts on
  - `coeffs`: `Any`
    > the polynomial coefficients
  - `center`: `Any`
    > the expansion center
  - `ref`: `Any`
    > the reference value
  - `:returns`: `CoordinateFunction`
    > the coordinate function


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.morse" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
morse(cls, coord, *, re, a=None, de=None, w=None, wx=None, g=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1241)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1241?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a coordinate function from a Morse potential in the given coordinate,
either from explicit `(de, a)` or from spectroscopic constants.
  - `coord`: `Any`
    > the coordinate spec
  - `re`: `Any`
    > the equilibrium position
  - `a`: `Any`
    > the range parameter
  - `de`: `Any`
    > the well depth
  - `w`: `Any`
    > the harmonic frequency (alternative parametrization)
  - `wx`: `Any`
    > the anharmonicity constant
  - `g`: `Any`
    > the reduced-mass factor
  - `:returns`: `CoordinateFunction`
    > the coordinate function


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.sin" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sin(cls, coord, *, n=1, l=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1264)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1264?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a coordinate function from a sine in the given coordinate.
  - `coord`: `Any`
    > the coordinate spec
  - `n`: `Any`
    > the numerator parameter
  - `l`: `Any`
    > the denominator parameter
  - `:returns`: `CoordinateFunction`
    > the coordinate function


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.cos" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
cos(cls, coord, *, n=1, l=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1278)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1278?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a coordinate function from a cosine in the given coordinate.
  - `coord`: `Any`
    > the coordinate spec
  - `n`: `Any`
    > the numerator parameter
  - `l`: `Any`
    > the denominator parameter
  - `:returns`: `CoordinateFunction`
    > the coordinate function


<a id="McUtils.Zachary.DifferentiableFunctions.CoordinateFunction.exp" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
exp(cls, coord, *, s=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1292)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1292?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a coordinate function from an exponential in the given coordinate.
  - `coord`: `Any`
    > the coordinate spec
  - `s`: `Any`
    > the exponential rate
  - `:returns`: `CoordinateFunction`
    > the coordinate function
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/DifferentiableFunctions/CoordinateFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L1007?message=Update%20Docs)   
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