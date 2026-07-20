# <a id="McUtils.Graphs.Trees.tree_traversal">tree_traversal</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees.py#L54)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees.py#L54?message=Update%20Docs)]
</div>

```python
tree_traversal(tree, callback, root=None, get_item=None, get_children=None, visited: set = None, check_visited=None, traversal_ordering='bfs', call_order='post'): 
```
**LLM Docstring**

Traverse a tree or graph-like object and invoke a callback before visiting, after marking, or after queuing each node.
  - `tree`: `object`
    > The nested container or adjacency structure to traverse.

  - `callback`: `object`
    > Function called with traversal context for each visited node.

  - `root`: `object`
    > Starting node; `None` is passed through, while `dev.default` selects the first child where implemented.

  - `get_item`: `object`
    > Callback resolving a child descriptor into a child node.

  - `get_children`: `object`
    > Callback returning child descriptors for a node.

  - `visited`: `set`
    > Mutable or per-path set of nodes already seen.

  - `check_visited`: `object`
    > Whether to suppress already-visited nodes.

  - `traversal_ordering`: `object`
    > Traversal order, `"bfs"` or `"dfs"`.

  - `call_order`: `object`
    > Point at which the callback is invoked relative to child expansion.

  - `:returns`: `object`
    > The first non-`None` callback result, or `None` after exhaustion.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Graphs/Trees/tree_traversal.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Graphs/Trees/tree_traversal.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Graphs/Trees/tree_traversal.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Graphs/Trees/tree_traversal.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees.py#L54?message=Update%20Docs)   
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