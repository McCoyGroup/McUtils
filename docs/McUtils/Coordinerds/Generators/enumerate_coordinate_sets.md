# <a id="McUtils.Coordinerds.Generators.enumerate_coordinate_sets">enumerate_coordinate_sets</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators.py#L1083)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators.py#L1083?message=Update%20Docs)]
</div>

```python
enumerate_coordinate_sets(groups, coords, canonicalize=True): 
```
**LLM Docstring**

Recursively enumerate coordinate sets that complete each supplied atom group.

Existing coordinates are canonicalized into a set by default. For each group, negative padding indices are removed, every completion from `enumerate_coordinate_completions_line` is merged into the current set, and recursion continues through the remaining groups. The outer loop also starts recursion at each group position, so overlapping suffix traversals may yield duplicate sets.
  - `groups`: `collections.abc.Sequence[collections.abc.Sequence[int]]`
    > Sequence of atom-index groups; negative entries are ignored as padding.
  - `coords`: `collections.abc.Iterable[tuple[int, ...]]`
    > Existing internal coordinates.
  - `canonicalize`: `bool`
    > Whether to canonicalize `coords` on the initial call.
  - `:returns`: `collections.abc.Iterator[set[tuple[int, ...]]]`
    > Generator yielding completed coordinate sets.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Generators/enumerate_coordinate_sets.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Generators/enumerate_coordinate_sets.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Generators/enumerate_coordinate_sets.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Generators/enumerate_coordinate_sets.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators.py#L1083?message=Update%20Docs)   
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