## <a id="McUtils.Zachary.DifferentiableFunctions.MorseFunction">MorseFunction</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions.py#L797)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L797?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.DifferentiableFunctions.MorseFunction.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *, de, a, re, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions.py#L798)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L798?message=Update%20Docs)]
</div>
**LLM Docstring**

A Morse oscillator potential `de * (1 - exp(-a (r - re)))^2`.
  - `de`: `Any`
    > the well depth
  - `a`: `Any`
    > the range parameter
  - `re`: `Any`
    > the equilibrium position
  - `inds`: `Sequence[int] | None`
    > the coordinate index


<a id="McUtils.Zachary.DifferentiableFunctions.MorseFunction.from_anharmonicity" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_anharmonicity(cls, w, wx, g, re, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L815)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L815?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a Morse function from spectroscopic constants (harmonic frequency,
anharmonicity, and reduced-mass factor).
  - `w`: `Any`
    > the harmonic frequency
  - `wx`: `Any`
    > the anharmonicity constant
  - `g`: `Any`
    > the reduced-mass / kinetic factor
  - `re`: `Any`
    > the equilibrium position
  - `inds`: `Sequence[int] | None`
    > the coordinate index
  - `:returns`: `MorseFunction`
    > the Morse function


<a id="McUtils.Zachary.DifferentiableFunctions.MorseFunction.evaluate_term" class="docs-object-method">&nbsp;</a> 
```python
evaluate_term(self, r, order=0, previous_terms=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/MorseFunction.py#L838)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/MorseFunction.py#L838?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate the `order`-th derivative of the Morse potential at `r`.
  - `r`: `np.ndarray`
    > the coordinate value
  - `order`: `int`
    > the derivative order
  - `previous_terms`: `Any`
    > earlier terms (unused)
  - `:returns`: `np.ndarray`
    > the term values


<a id="McUtils.Zachary.DifferentiableFunctions.MorseFunction.get_children" class="docs-object-method">&nbsp;</a> 
```python
get_children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/MorseFunction.py#L866)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/MorseFunction.py#L866?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the sub-functions of this Morse function (a leaf).
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/DifferentiableFunctions/MorseFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/DifferentiableFunctions/MorseFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/DifferentiableFunctions/MorseFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/DifferentiableFunctions/MorseFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L797?message=Update%20Docs)   
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