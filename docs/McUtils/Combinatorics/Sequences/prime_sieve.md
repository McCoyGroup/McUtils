# <a id="McUtils.Combinatorics.Sequences.prime_sieve">prime_sieve</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Sequences.py#L127)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Sequences.py#L127?message=Update%20Docs)]
</div>

```python
prime_sieve(ints, k, max_its=None): 
```
**LLM Docstring**

Remove repeated factors of `k` from one or more integers.

Scalar inputs are temporarily promoted to length-one arrays and converted back before returning. When `max_its` is omitted, the function derives an upper bound from `log(max(ints)) / log(k)`.
  - `ints`: `int | array-like`
    > scalar or array of integers to factor by `k`
  - `k`: `int`
    > factor to divide out repeatedly
  - `max_its`: `int | None`
    > optional cap on the number of divisions
  - `:returns`: `tuple[int | numpy.ndarray, int | numpy.ndarray]`
    > a pair containing the residual integers and multiplicities of `k`, with the input shape preserved











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Sequences/prime_sieve.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Sequences/prime_sieve.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Sequences/prime_sieve.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Sequences/prime_sieve.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Sequences.py#L127?message=Update%20Docs)   
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