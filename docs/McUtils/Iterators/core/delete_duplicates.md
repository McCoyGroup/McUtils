# <a id="McUtils.Iterators.core.delete_duplicates">delete_duplicates</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Iterators/core.py#L404)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L404?message=Update%20Docs)]
</div>

```python
delete_duplicates(iterable, key=None, hashable=None, cache=None): 
```
**LLM Docstring**

Yield the first item associated with each distinct key.

The function uses a set by default and automatically falls back to a list when adding an unhashable key raises `TypeError`. A supplied cache is updated in place and can preserve uniqueness state across calls.
  - `iterable`: `collections.abc.Iterable`
    > Values to filter.
  - `key`: `callable | None`
    > Optional function producing the value used for duplicate detection.
  - `hashable`: `bool | None`
    > Force set-based or list-based storage; `None` enables automatic fallback.
  - `cache`: `set | list | None`
    > Existing membership cache to update.
  - `:returns`: `collections.abc.Iterator`
    > Iterator yielding only the first value for each key.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Iterators/core/delete_duplicates.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Iterators/core/delete_duplicates.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Iterators/core/delete_duplicates.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Iterators/core/delete_duplicates.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L404?message=Update%20Docs)   
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