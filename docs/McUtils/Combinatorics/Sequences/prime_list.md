# <a id="McUtils.Combinatorics.Sequences.prime_list">prime_list</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Sequences.py#L236)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Sequences.py#L236?message=Update%20Docs)]
</div>

```python
prime_list(n, base_primes=None, piter=None): 
```
**LLM Docstring**

Return the first `n` primes, using a shared incremental cache by default.

Three cases, chosen by what's supplied:

- `piter=None`, `base_primes=None` (the default call): both are pulled
  from the module-level `default_prime_iter`/`default_base_prime_list`,
  a cache that's intentionally persistent across calls.
- `piter=None`, `base_primes=<a list>`: a *fresh* iterator is built from
  that list with `prime_iter(base_primes)`, instead of pulling from the
  unrelated global cache. Previously, supplying a custom `base_primes`
  without also supplying a matching `piter` silently ignored the
  supplied list's content -- the shared global generator's cache won
  regardless, so the "custom starting list" argument didn't do what it
  looked like it did.
- `piter=<an iterator>`: used as given; `base_primes` defaults to a new
  empty list if not also supplied (so it isn't tied to the global cache
  unless the caller asks for that explicitly).

In every case `base_primes` is still extended in place and returned;
supplying your own list lets you keep your own independent cache instead
of sharing the module-level one.
  - `n`: `int`
    > number of primes requested
  - `base_primes`: `list[int] | None`
    > mutable cache populated in place; `None` selects the
    shared default cache (or, if `piter` is supplied, a fresh empty list)
  - `piter`: `collections.abc.Iterator[list[int]] | None`
    > cumulative prime-list iterator used to extend the cache;
    `None` selects the shared default iterator, unless `base_primes` was
    supplied, in which case a fresh iterator seeded from it is used
  - `:returns`: `list[int]`
    > the first `n` cached primes











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Sequences/prime_list.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Sequences/prime_list.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Sequences/prime_list.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Sequences/prime_list.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Sequences.py#L236?message=Update%20Docs)   
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