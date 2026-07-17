# <a id="McUtils.Coordinerds.Labels.sort_internal_coordinates">sort_internal_coordinates</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Labels.py#L186)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Labels.py#L186?message=Update%20Docs)]
</div>

```python
sort_internal_coordinates(coords, atoms=None, sort_key=None): 
```
**LLM Docstring**

Sort internal coordinates or a coordinate-label mapping using a coordinate-aware key.

When `atoms` is supplied, integer index tuples are converted to concatenated atom-symbol strings before sorting. For mappings, values are sorted and a new insertion-ordered `dict` with the original keys is returned. For other iterables, the sorted coordinates are returned as a tuple.
  - `coords`: `collections.abc.Iterable | dict`
    > Coordinate iterable, or mapping whose values are coordinate labels.
  - `atoms`: `collections.abc.Sequence[str] | None`
    > Optional atom-symbol sequence used to translate integer coordinate indices.
  - `sort_key`: `collections.abc.Callable | None`
    > Key function; defaults to `coordinate_sorting_key`.
  - `:returns`: `dict | tuple`
    > Sorted mapping when `coords` is a dictionary, otherwise a sorted tuple.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Labels/sort_internal_coordinates.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Labels/sort_internal_coordinates.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Labels/sort_internal_coordinates.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Labels/sort_internal_coordinates.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Labels.py#L186?message=Update%20Docs)   
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