# <a id="McUtils.Combinatorics.Sequences.prime_iter">prime_iter</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Sequences.py#L179)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Sequences.py#L179?message=Update%20Docs)]
</div>

```python
prime_iter(primes=None): 
```
**LLM Docstring**

Yield progressively longer lists of prime numbers.

The generator first yields prefixes of the provided seed list. It then searches odd candidates between the current largest prime and twice that value, accepting the first candidate not divisible by the existing primes other than `2`. Each yield is the full prime list accumulated so far.
  - `primes`: `iterable[int] | None`
    > optional initial ordered prime sequence
  - `:returns`: `collections.abc.Iterator[list[int]]`
    > an iterator yielding cumulative prime lists











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Sequences/prime_iter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Sequences/prime_iter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Sequences/prime_iter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Sequences/prime_iter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Sequences.py#L179?message=Update%20Docs)   
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