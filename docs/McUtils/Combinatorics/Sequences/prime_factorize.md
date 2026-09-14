# <a id="McUtils.Combinatorics.Sequences.prime_factorize">prime_factorize</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Sequences.py#L291)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Sequences.py#L291?message=Update%20Docs)]
</div>

```python
prime_factorize(ints, primes=None): 
```
**LLM Docstring**

Compute prime-exponent arrays for one or more positive integers.

The function repeatedly applies `_sieve_core` to entries whose residual value exceeds `1`. It accepts either an iterator of individual primes or an iterator of cumulative prime lists, as produced by `prime_iter`. The returned count list contains one array per tested prime and preserves the original input shape.

When `primes` is left as `None` (the default, gapless `prime_iter()`
sequence), trial division stops early for any entry once its residual
drops to `p**2` or below for the current trial prime `p`: every prime
up to and including `p` has already been divided out in order, so a
residual that small can't have a factor <= its own square root other
than itself, meaning it's already prime. That residual is recorded
directly as an extra prime factor instead of continuing to trial-divide
(and generate ever-larger candidate primes) all the way up to its
value -- previously this made factoring a single large prime (or a
number with one) effectively never finish.

When a custom, possibly incomplete `primes` sequence is supplied
instead, that early-exit isn't safe (it can't be assumed gapless), so
instead a `ValueError` is raised if the sequence runs out before every
entry is fully factored, rather than silently returning a partial,
incorrect factorization.
  - `ints`: `int | array-like`
    > positive integer scalar or array to factor
  - `primes`: `iterable[int | list[int]] | None`
    > optional prime or cumulative-prime iterator
  - `:returns`: `tuple[numpy.ndarray, list[int | numpy.ndarray]]`
    > the generated prime array and a list of exponent arrays for those primes











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Sequences/prime_factorize.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Sequences/prime_factorize.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Sequences/prime_factorize.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Sequences/prime_factorize.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Sequences.py#L291?message=Update%20Docs)   
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