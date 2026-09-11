## <a id="McUtils.Graphs.UnionMultiGraph.UnionMultiGraph">UnionMultiGraph</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/UnionMultiGraph.py#L12)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/UnionMultiGraph.py#L12?message=Update%20Docs)]
</div>

A multigraph formed as the union of several component graphs defined
over the same node set (e.g. a bond graph and a through-space contact
graph over the same atoms, or several correlation graphs over the same
variables).

Component graphs will usually live on incompatible weight scales
(Angstroms vs. correlation coefficients vs. bond order...), so rather
than teach `GraphLayout`/`GraphPlotter` to juggle several graphs at
once, each component is independently rescaled onto a common footing
and the components are folded into ordinary single-graph data -- an
adjacency matrix, an edge list, and a `{(i, j): weight}` map -- exactly
what a plain weighted `EdgeGraph` carries. `layout`/`plot` are
therefore inherited unchanged; `plot` only adds a thin default so
edges stay colored by their dominant contributing component. Weight
convention matches `EdgeGraph` throughout: larger values mean *more*
graph-theoretic separation (they're fed straight to
`scipy.sparse.csgraph.shortest_path` as costs), so similarity-style
weights should be inverted before being handed in.

Component provenance (raw per-component edges/weights/scale, and which
components contributed to each merged edge) is kept on the side in
`self.components` / `self.edge_components` -- `plot` uses it to draw
every contributing edge separately (fanned out where several overlap
the same node pair) rather than collapsing them; `layout` uses the
single pooled weight per pair instead (see `pool_layout`), since node
*placement* has no use for telling the edges apart.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_combine: str
default_palette: tuple
combine: member_descriptor
components: member_descriptor
edge_components: member_descriptor
pooled_weights: member_descriptor
scales: member_descriptor
```
<a id="McUtils.Graphs.UnionMultiGraph.UnionMultiGraph.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, labels, edges=None, graph=None, edge_map=None, weights=None, allow_self_loops=False, *, components=None, scales=None, combine=None, pool_layout=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/UnionMultiGraph.py#L47)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/UnionMultiGraph.py#L47?message=Update%20Docs)]
</div>
Base-`EdgeGraph`-compatible constructor: with `components=None` this
behaves exactly like `EdgeGraph`, so derived views (`.take()`,
`.break_bonds()`, ...) that call `type(self)(labels, edges)` keep
working -- they just degrade to a plain single graph, since the
induced-subgraph machinery has no notion of "which component". Use
`UnionMultiGraph.from_graphs` to build an actual union.
  - `components`: `Any`
    > pre-built component specs (see `_build_components`); internal
  - `scales`: `Any`
    > per-component rescaling; see `_resolve_scales`
  - `combine`: `Any`
    > how overlapping edges are pooled across components: 'sum' (default),
    'max', 'mean', or a `callable(list[float]) -> float`
  - `pool_layout`: `Any`
    > whether node placement uses the pooled per-pair weight
    (default) or ignores magnitude and lays out on unweighted structure alone;
    either way, `self.pooled_weights` holds the pooled values and `plot` always
    draws each contributing edge on its own, unpooled weight


<a id="McUtils.Graphs.UnionMultiGraph.UnionMultiGraph.from_graphs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_graphs(cls, labels, graphs, names=None, scales=None, combine=None, pool_layout=True, allow_self_loops=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L83)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L83?message=Update%20Docs)]
</div>
Build the union of `graphs` over `labels`.
  - `graphs`: `Any`
    > one entry per component; each is an `EdgeGraph` (sharing `labels`),
    a `{'edges':..., 'weights':...}` dict, or a raw `(i, j[, w])` edge array
  - `names`: `Any`
    > optional per-component names, used for styling/legends
  - `:returns`: `UnionMultiGraph`
    > the union multigraph


<a id="McUtils.Graphs.UnionMultiGraph.UnionMultiGraph.adj_mat" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
adj_mat(cls, num_nodes, edges, weights=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L162)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L162?message=Update%20Docs)]
</div>


<a id="McUtils.Graphs.UnionMultiGraph.UnionMultiGraph.dominant_component" class="docs-object-method">&nbsp;</a> 
```python
dominant_component(self, i, j): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/UnionMultiGraph/UnionMultiGraph.py#L183)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/UnionMultiGraph/UnionMultiGraph.py#L183?message=Update%20Docs)]
</div>
Index of the component contributing the largest rescaled weight to edge (i, j).


<a id="McUtils.Graphs.UnionMultiGraph.UnionMultiGraph.component_legend" class="docs-object-method">&nbsp;</a> 
```python
component_legend(self, colors=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/UnionMultiGraph/UnionMultiGraph.py#L189)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/UnionMultiGraph/UnionMultiGraph.py#L189?message=Update%20Docs)]
</div>
List of `{'name', 'color'}` entries, one per component, for building a legend.


<a id="McUtils.Graphs.UnionMultiGraph.UnionMultiGraph.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, method='default', *, component_colors=None, weight_linewidth=(0.5, 4.0), edge_offset=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/UnionMultiGraph/UnionMultiGraph.py#L197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/UnionMultiGraph/UnionMultiGraph.py#L197?message=Update%20Docs)]
</div>
Like `EdgeGraph.plot`, but when this union carries component
provenance, every contributing edge is drawn on its own -- colored
by its component and widthed by its own (rescaled) weight -- instead
of collapsing same-pair edges into one pooled line. Node placement
still comes from the inherited `layout` (pooled per `pool_layout`);
only drawing is per-edge here. Edges that share a node pair are
fanned out by `edge_offset` (default: `0.6 *` the plotted node
radius) so they stay individually visible rather than overlapping
exactly. An explicit `edge_style`/`edges` in `opts` is left
untouched and simply passed through.
 </div>
</div>












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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Graphs/UnionMultiGraph/UnionMultiGraph.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Graphs/UnionMultiGraph/UnionMultiGraph.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Graphs/UnionMultiGraph/UnionMultiGraph.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Graphs/UnionMultiGraph/UnionMultiGraph.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/UnionMultiGraph.py#L12?message=Update%20Docs)   
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