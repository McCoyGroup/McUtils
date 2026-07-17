# <a id="McUtils.Coordinerds.ZMatrices.complex_zmatrix">complex_zmatrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L2645)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L2645?message=Update%20Docs)]
</div>

```python
complex_zmatrix(bonds, fragment_inds=None, fragment_zmats=None, distance_matrix=None, attachment_points=None, check_attachment_points=True, graph=None, reindex=True, required_coordinates=None, isolated_coordinates=None, root_coordinates=None, validate_additions=True): 
```
**LLM Docstring**

Assemble a Z-matrix for multiple disconnected fragments using explicit or distance-derived attachment points.

Fragments are inferred from the bond graph when needed and each receives a supplied or generated Z-matrix. Attachments are sorted into a connected traversal. When an attachment is absent, the closest interfragment atom pair is selected from `distance_matrix`; `_attachment_point` supplies the remaining angle and dihedral references from the graph. Fragments are appended with `functionalized_zmatrix`, optionally reindexed to original atoms, validated, and reparented to satisfy requested coordinates.
  - `bonds`: `Sequence[tuple[int, int]] | None`
    > Bond list used to construct the graph when `graph` is omitted.
  - `fragment_inds`: `Sequence[Sequence[int]] | None`
    > Atom indices for each fragment.
  - `fragment_zmats`: `Sequence | None`
    > Z-matrix ordering for each fragment.
  - `distance_matrix`: `np.ndarray | None`
    > Pairwise distances used to choose closest attachment atoms.
  - `attachment_points`: `dict | Sequence | None`
    > Explicit interfragment attachment specifications.
  - `check_attachment_points`: `bool`
    > Validate that attachment references belong to the appropriate fragments.
  - `graph`: `EdgeGraph | None`
    > Connectivity graph used for fragments and neighboring references.
  - `reindex`: `bool`
    > Return rows in original atom-label space.
  - `required_coordinates`: `Sequence | None`
    > Coordinates required in the final ordering.
  - `isolated_coordinates`: `Sequence | None`
    > Coordinates protected from unrelated parent usage.
  - `root_coordinates`: `Sequence | None`
    > Coordinates preferentially placed at the root.
  - `validate_additions`: `bool`
    > Validate fragment assembly and final ordering.
  - `:returns`: `list[list[int]]`
    > Combined complex Z-matrix.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/complex_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/complex_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/complex_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/complex_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L2645?message=Update%20Docs)   
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