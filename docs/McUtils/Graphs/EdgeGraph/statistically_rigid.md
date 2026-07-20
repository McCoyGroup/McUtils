# <a id="McUtils.Graphs.EdgeGraph.statistically_rigid">statistically_rigid</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph.py#L2934)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph.py#L2934?message=Update%20Docs)]
</div>

```python
statistically_rigid(edges, ndim, l=None, natoms=None, ntest=5, points=None, return_rigidity_matrix=False): 
```
**LLM Docstring**

Estimate generic rigidity by evaluating rigidity-matrix rank on random or supplied coordinates.
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

  - `return_rigidity_matrix`: `object`
    > Whether to return the matrix and computed rank with the Boolean result.

  - `:returns`: `np.ndarray`
    > A rigidity flag, optionally with the rigidity matrix and rank.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Graphs/EdgeGraph/statistically_rigid.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Graphs/EdgeGraph/statistically_rigid.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Graphs/EdgeGraph/statistically_rigid.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Graphs/EdgeGraph/statistically_rigid.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph.py#L2934?message=Update%20Docs)   
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