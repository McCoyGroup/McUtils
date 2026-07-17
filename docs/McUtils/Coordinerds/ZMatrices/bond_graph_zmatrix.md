# <a id="McUtils.Coordinerds.ZMatrices.bond_graph_zmatrix">bond_graph_zmatrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L2350)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L2350?message=Update%20Docs)]
</div>

```python
bond_graph_zmatrix(bonds, fragments, edge_map=None, reindex=True, validate_additions=True, required_coordinates=None, isolated_coordinates=None, root_coordinates=None, enforce_requirements=True): 
```
**LLM Docstring**

Construct a Z-matrix spanning a bonded graph, including disconnected or fused fragments.

Fragments and an edge map are obtained from the supplied `EdgeGraph` or bond list. Provided backbone fragments are fused first; missing graph fragments receive submatrices and are attached through graph edges. The combined local ordering is reindexed to original atom labels. Optional required, root, and isolated coordinates are enforced after assembly.
  - `bonds`: `Sequence[tuple[int, int]] | EdgeGraph`
    > Bond pairs or an `EdgeGraph` describing molecular connectivity.
  - `fragments`: `Sequence[Sequence[int]] | None`
    > Optional atom-index fragments; inferred from the graph when omitted.
  - `submats`: `Sequence[Sequence[Sequence[int]]] | None`
    > Optional Z-matrix ordering for each fragment.
  - `backbone`: `Sequence | None`
    > Optional initial atom ordering or fragment backbone.
  - `edge_map`: `dict | None`
    > Precomputed adjacency mapping.
  - `reindex`: `bool`
    > Map the assembled local ordering back to original atom labels.
  - `validate_additions`: `bool`
    > Validate intermediate fragment attachments.
  - `required_coordinates`: `Sequence | None`
    > Coordinates that must be represented after assembly.
  - `isolated_coordinates`: `Sequence | None`
    > Coordinates to keep isolated from unrelated parent references.
  - `root_coordinates`: `Sequence | None`
    > Coordinates to place near the root chain.
  - `enforce_requirements`: `bool`
    > Apply coordinate reparenting after graph assembly.
  - `:returns`: `list[list[int]]`
    > Z-matrix ordering spanning the graph.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/bond_graph_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/bond_graph_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/bond_graph_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/bond_graph_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L2350?message=Update%20Docs)   
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