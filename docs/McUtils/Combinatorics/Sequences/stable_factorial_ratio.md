# <a id="McUtils.Combinatorics.Sequences.stable_factorial_ratio">stable_factorial_ratio</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Sequences.py#L292)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Sequences.py#L292?message=Update%20Docs)]
</div>

```python
stable_factorial_ratio(num_terms, denom_terms, counts=None): 
```
**LLM Docstring**

Evaluate a ratio of products using prime exponents.

Without precomputed `counts`, numerator and denominator terms are deduplicated, factorized, and weighted by their multiplicities. The two prime-count vectors are padded to equal length, subtracted, and exponentiated. Negative exponents trigger floating-point evaluation. Despite its name, the inputs are treated as explicit multiplicative terms rather than factorial arguments.
  - `num_terms`: `array-like`
    > factors in the numerator
  - `denom_terms`: `array-like`
    > factors in the denominator
  - `counts`: `tuple[array-like, array-like] | None`
    > optional pair of precomputed numerator and denominator prime-exponent arrays; when supplied, `num_terms` and `denom_terms` are treated as the corresponding prime lists
  - `:returns`: `int | float | numpy.number`
    > product of the aligned primes raised to the net exponent vector











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Sequences/stable_factorial_ratio.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Sequences/stable_factorial_ratio.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Sequences/stable_factorial_ratio.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Sequences/stable_factorial_ratio.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Sequences.py#L292?message=Update%20Docs)   
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