# <a id="McUtils.Iterators.core.chunked">chunked</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Iterators/core.py#L60)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L60?message=Update%20Docs)]
</div>

```python
chunked(a, upto): 
```
**LLM Docstring**

Yield consecutive chunks from a fixed-size, sliceable object.

For objects with `__len__`, the function slices blocks of at most `upto` items.
The non-fixed-size branch defines a consumer and yields chunks of a given size
  - `a`: `collections.abc.Iterable`
    > Sequence or iterable to divide into chunks.
  - `upto`: `int`
    > Maximum chunk size.
  - `:returns`: `collections.abc.Iterator`
    > Iterator over sequence slices for fixed-size inputs.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Iterators/core/chunked.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Iterators/core/chunked.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Iterators/core/chunked.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Iterators/core/chunked.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/core.py#L60?message=Update%20Docs)   
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