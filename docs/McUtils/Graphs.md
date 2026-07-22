# <a id="McUtils.Graphs">McUtils.Graphs</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/__init__.py#L1?message=Update%20Docs)]
</div>
    
Simple graph tools, could be in misc but I can imagine building these out

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[EdgeGraph](Graphs/EdgeGraph/EdgeGraph.md)   
</div>
   <div class="col" markdown="1">
[MoleculeEdgeGraph](Graphs/EdgeGraph/MoleculeEdgeGraph.md)   
</div>
   <div class="col" markdown="1">
[GraphSearcher](Graphs/EdgeGraph/GraphSearcher.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[pebble_rigidity](Graphs/EdgeGraph/pebble_rigidity.md)   
</div>
   <div class="col" markdown="1">
[statistically_rigid](Graphs/EdgeGraph/statistically_rigid.md)   
</div>
   <div class="col" markdown="1">
[uniquely_rigid](Graphs/EdgeGraph/uniquely_rigid.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[TreeWrapper](Graphs/Trees/TreeWrapper.md)   
</div>
   <div class="col" markdown="1">
[tree_traversal](Graphs/Trees/tree_traversal.md)   
</div>
   <div class="col" markdown="1">
[tree_iter](Graphs/Trees/tree_iter.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[graph_iter](Graphs/Trees/graph_iter.md)   
</div>
   <div class="col" markdown="1">
[TreeSentinels](Graphs/Trees/TreeSentinels.md)   
</div>
   <div class="col" markdown="1">
[merge_sets](Graphs/utils/merge_sets.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>





## Examples
**LLM Examples**

### Analyze a molecular graph

```python
from McUtils.Graphs import EdgeGraph

labels = ["C", "C", "O", "H", "H", "H", "H", "H", "H"]
edges = [(0, 1), (1, 2), (0, 3), (0, 4), (0, 5),
         (1, 6), (1, 7), (2, 8)]
ethanol = EdgeGraph(labels, edges)
print("C-to-O path:", ethanol.get_path(0, 2))
print("fragments:", ethanol.get_fragments(return_labels=True))
print("three-bond neighborhood:", list(ethanol.neighbor_iterator(0, num=3)))
```

### Detect rings and break a bond

```python
from McUtils.Graphs import EdgeGraph

benzene = EdgeGraph(["C"] * 6, [(i, (i + 1) % 6) for i in range(6)])
rings = benzene.get_rings()
opened = benzene.break_bonds([(0, 1)], return_single_graph=True)
assert len(rings) == 1
assert opened.get_path(0, 1) == (0, 5, 4, 3, 2, 1)
print("ring:", rings[0])
print("opened-chain distances:", opened.get_distances(0))
```

### Traverse nested scientific data

```python
from McUtils.Graphs import tree_iter
from McUtils.Iterators import riffle

workflow = {
    "optimize": {"geometry": {}, "energy": {}},
    "frequency": {"modes": {}, "intensities": {}}
}
for path, is_term in tree_iter(workflow, yield_paths='terminal', traversal_ordering="dfs"):
    print(*riffle(path, [" / "] * len(path)))
```

### Compare two labeled graphs

```python
from McUtils.Graphs import EdgeGraph

first = EdgeGraph(["O", "H", "H"], [(0, 1), (0, 2)])
second = EdgeGraph(["H", "O", "H"], [(1, 0), (1, 2)])
permutation = first.get_reindexing(second)
aligned = second.take(permutation)
print("alignment:", permutation, aligned.labels)
```

### Compute a graph layout and plot it

```python
from McUtils.Graphs import EdgeGraph

graph = EdgeGraph(list("ABCDEF"), [(0, 1), (1, 2), (2, 3),
                                    (3, 4), (4, 5), (5, 0), (0, 3)])
positions = graph.layout(method="kamada_kawai")
print("node positions:", positions)
figure = graph.plot(method="kamada_kawai")
figure.show()
```

### Test generic rigidity

```python
import numpy as np
from McUtils.Graphs import statistically_rigid

points = np.array([[0., 0.], [1., 0.], [0., 1.]])
edges = [(0, 1), (1, 2), (2, 0)]
rigid, (matrix, rank) = statistically_rigid(edges, ndim=2, points=points, return_rigidity_matrix=True)
print("rigidity-matrix rank:", rank, "rigid:", rigid)
```







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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Graphs.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Graphs.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Graphs.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Graphs.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/__init__.py#L1?message=Update%20Docs)   
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