# <a id="McUtils.Iterators.Subsequences.find_tree_overlaps">find_tree_overlaps</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Iterators/Subsequences.py#L239)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/Subsequences.py#L239?message=Update%20Docs)]
</div>

```python
find_tree_overlaps(s1: 'Sequence[Any]', s2: 'Sequence[Any]', antecedents1: 'Sequence[int | None]', antecedents2: 'Sequence[int | None]', *, equals: 'Callable[[Any, Any, Any | None, Any | None], bool]', nparents=1, require_contiguous=True, mode='best_forest', maximal_only=True): 
```
Parameters
----------
mode
    ``"best_tree"``:
        Return one highest-scoring rooted match.

    ``"best_forest"``:
        Return one highest-scoring collection of compatible,
        nonnested rooted matches.

    ``"root_alternatives"``:
        Return the best rooted match for every possible root pair.

maximal_only
    In ``"root_alternatives"`` mode, remove alternatives whose
    complete match set is strictly contained in another alternative.












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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Iterators/Subsequences/find_tree_overlaps.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Iterators/Subsequences/find_tree_overlaps.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Iterators/Subsequences/find_tree_overlaps.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Iterators/Subsequences/find_tree_overlaps.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/Subsequences.py#L239?message=Update%20Docs)   
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