# <a id="McUtils.Graphs.EdgeGraph.uniquely_rigid">uniquely_rigid</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph.py#L2986)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph.py#L2986?message=Update%20Docs)]
</div>

```python
uniquely_rigid(edges, ndim, l=None, natoms=None, ntest=5, points=None, return_components=False, return_rigid_subgraphs=False): 
```
**LLM Docstring**

Estimate global rigidity using generic rigidity plus the rank of a random equilibrium stress matrix.
  - `edges`: `object`
    > Undirected edges as endpoint pairs, optionally carrying weights.

  - `ndim`: `object`
    > Spatial dimension of the rigidity problem.

  - `l`: `object`
    > Sparsity offset; defaults to rigid-body motions for the dimension.

  - `natoms`: `object`
    > Number of vertices represented by the edge list.

  - `ntest`: `object`
    > Number of random coordinate realizations to test.

  - `points`: `object`
    > Coordinates with trailing shape `(n_atoms, ndim)`.

  - `return_components`: `object`
    > Whether to include rank and stress diagnostics.

  - `return_rigid_subgraphs`: `object`
    > Request for an unimplemented rigid-subgraph analysis.

  - `:returns`: `object`
    > A global-rigidity flag, optionally with rigidity and stress diagnostics.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Graphs/EdgeGraph/uniquely_rigid.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Graphs/EdgeGraph/uniquely_rigid.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Graphs/EdgeGraph/uniquely_rigid.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Graphs/EdgeGraph/uniquely_rigid.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph.py#L2986?message=Update%20Docs)   
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