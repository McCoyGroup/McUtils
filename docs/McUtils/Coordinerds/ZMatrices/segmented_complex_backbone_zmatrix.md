# <a id="McUtils.Coordinerds.ZMatrices.segmented_complex_backbone_zmatrix">segmented_complex_backbone_zmatrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L2847)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L2847?message=Update%20Docs)]
</div>

```python
segmented_complex_backbone_zmatrix(bond_graph: McUtils.Graphs.EdgeGraph.EdgeGraph, fragments=None, segments=None, root=None, attachment_points=None, check_attachment_points=True, validate=True, for_fragment=None, fragment_ordering=None, distance_matrix=None): 
```
**LLM Docstring**

Construct a complex Z-matrix by building graph-based backbones for each disconnected fragment.

Disconnected graph fragments are identified first. A single fragment is delegated to `graph_backbone_zmatrix`; multiple fragments are processed recursively to obtain local backbones, then joined with `complex_zmatrix` using graph connectivity, optional distances, and attachment specifications. Optional metadata is propagated with the final ordering.
  - `bond_graph`: `EdgeGraph`
    > Connectivity graph, possibly containing multiple fragments.
  - `root`: `int | None`
    > Preferred root atom or fragment root.
  - `distance_matrix`: `np.ndarray | None`
    > Pairwise distances used to connect disconnected fragments.
  - `attachment_points`: `dict | Sequence | None`
    > Explicit links between fragments.
  - `validate`: `bool`
    > Validate each local and combined ordering.
  - `return_segments`: `bool`
    > Include segment information in the result.
  - `return_graph`: `bool`
    > Include graph metadata in the result.
  - `:returns`: `tuple | list[list[int]]`
    > Combined Z-matrix, optionally with segment and graph metadata.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/segmented_complex_backbone_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/segmented_complex_backbone_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/segmented_complex_backbone_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/segmented_complex_backbone_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L2847?message=Update%20Docs)   
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