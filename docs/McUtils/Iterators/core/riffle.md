# <a id="McUtils.Iterators.core.riffle">riffle</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Iterators/core.py#L327)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L327?message=Update%20Docs)]
</div>

```python
riffle(a, b, *extras): 
```
**LLM Docstring**

Interleave corresponding values from multiple iterables.

The first iterable determines the target length and is materialized when it lacks `__len__`.
For each zipped tuple except the last first-iterable position, every tuple element is yielded; at the last position only the value from `a` is yielded.
Any remaining tail of `a` is then emitted. Consequently values from the other iterables aligned with the final item of `a` are omitted.
  - `a`: `collections.abc.Iterable`
    > Primary iterable controlling output length and tail handling.
  - `b`: `collections.abc.Iterable`
    > First iterable to interleave with `a`.
  - `extras`: `collections.abc.Iterable`
    > Additional iterables to interleave.
  - `:returns`: `collections.abc.Iterator`
    > Iterator over the interleaved values.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Iterators/core/riffle.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Iterators/core/riffle.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Iterators/core/riffle.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Iterators/core/riffle.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L327?message=Update%20Docs)   
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