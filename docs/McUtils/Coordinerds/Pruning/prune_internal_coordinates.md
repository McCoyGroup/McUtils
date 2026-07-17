# <a id="McUtils.Coordinerds.Pruning.prune_internal_coordinates">prune_internal_coordinates</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Pruning.py#L208)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Pruning.py#L208?message=Update%20Docs)]
</div>

```python
prune_internal_coordinates(coords, *args, method='basic', **kwargs): 
```
**LLM Docstring**

Resolve a pruning strategy and apply it to a coordinate collection.

`method` is dispatched through `pruner_dispatch`: `"basic"` yields candidates unchanged, `"unique"` canonicalizes and removes duplicates, and `"b_matrix"` performs geometric/SVD pruning. Options registered with the dispatch entry are merged with `kwargs`, with explicit keyword arguments taking precedence.
  - `coords`: `collections.abc.Sequence`
    > Coordinate specifications to prune.
  - `args`: `tuple`
    > Additional positional arguments passed to the selected pruner.
  - `method`: `str`
    > Registered pruning method or other value understood by `OptionsMethodDispatch.resolve`.
  - `kwargs`: `dict`
    > Options passed to the selected pruner's `prune_coordinates` method.
  - `:returns`: `list`
    > Coordinates retained by the selected pruning strategy.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Pruning/prune_internal_coordinates.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Pruning/prune_internal_coordinates.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Pruning/prune_internal_coordinates.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Pruning/prune_internal_coordinates.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Pruning.py#L208?message=Update%20Docs)   
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