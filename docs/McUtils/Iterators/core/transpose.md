# <a id="McUtils.Iterators.core.transpose">transpose</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Iterators/core.py#L289)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L289?message=Update%20Docs)]
</div>

```python
transpose(data, default=None, pad=False): 
```
**LLM Docstring**

Transpose nested data, optionally padding shorter fixed-size rows.

Fixed-size rows are indexed up to the maximum row length. With `pad=False`, missing elements are omitted from each transposed row; with `pad=True`, they are replaced by `default`.
If the outer container is fixed-size but its first row has no `__len__`, the function returns `transpose_iter` without first converting the rows to iterators.
Non-fixed outer inputs are fully materialized and processed recursively.
  - `data`: `collections.abc.Iterable`
    > Nested sequence or iterable to transpose.
  - `default`: `object`
    > Padding value used by padded or iterator-based transposition.
  - `pad`: `bool`
    > Whether fixed-size rows should be padded instead of skipped.
  - `:returns`: `list | collections.abc.Iterator`
    > A list of transposed rows or an iterator from `transpose_iter`.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Iterators/core/transpose.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Iterators/core/transpose.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Iterators/core/transpose.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Iterators/core/transpose.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L289?message=Update%20Docs)   
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