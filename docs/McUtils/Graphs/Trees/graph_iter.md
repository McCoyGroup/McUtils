# <a id="McUtils.Graphs.Trees.graph_iter">graph_iter</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees.py#L360)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees.py#L360?message=Update%20Docs)]
</div>

```python
graph_iter(graph, root=None, get_item=None, get_children=None, visited: set = None, traversal_ordering='bfs', yield_paths=False, enable_disconnectivity=False): 
```
**LLM Docstring**

Adapt an adjacency mapping to `tree_iter`, enabling cycle-safe graph traversal and optional path enumeration.
  - `graph`: `object`
    > Graph object, adjacency matrix, or adjacency mapping used by the operation.

  - `root`: `object`
    > Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.

  - `get_item`: `object`
    > Callback resolving a child descriptor into a child node.

  - `get_children`: `object`
    > Callback returning child descriptors for a node.

  - `visited`: `set`
    > Mutable or per-path set of nodes already seen.

  - `traversal_ordering`: `object`
    > Traversal order, `"bfs"` or `"dfs"`.

  - `yield_paths`: `object`
    > Whether to yield path records instead of individual traversal payloads.

  - `enable_disconnectivity`: `object`
    > Whether terminal paths should search earlier path nodes for skipped branches.

  - `:returns`: `collections.abc.Iterator`
    > A configured traversal generator.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Graphs/Trees/graph_iter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Graphs/Trees/graph_iter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Graphs/Trees/graph_iter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Graphs/Trees/graph_iter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees.py#L360?message=Update%20Docs)   
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