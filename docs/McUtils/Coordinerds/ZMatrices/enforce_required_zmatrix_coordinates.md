# <a id="McUtils.Coordinerds.ZMatrices.enforce_required_zmatrix_coordinates">enforce_required_zmatrix_coordinates</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L2005)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L2005?message=Update%20Docs)]
</div>

```python
enforce_required_zmatrix_coordinates(zm, required_coordinates=None, root_coordinates=None, isolated_coordinates=None, reparent_isolated_coordinates=True, reparent_root_coordinates=True, validate=False): 
```
**LLM Docstring**

Reparent a Z-matrix tree so requested bonds, angles, and dihedrals occur as row parent prefixes.

Already satisfied constraints are retained. Isolated coordinates can first be prevented from serving as references for unrelated rows, and root coordinates can be promoted into the initial embedding chain. Missing required coordinates are then tried in both orientations by replacing candidate parent prefixes through `_adjust_zm_parents`; all previously accepted constraints must remain valid. The result is returned in the same row representation as the input.
  - `zm`: `Sequence[Sequence[int]] | dict`
    > Z-matrix rows or tree mapping.
  - `required_coordinates`: `Sequence[Sequence[int]] | None`
    > Coordinates that must appear in either orientation.
  - `root_coordinates`: `Sequence[Sequence[int]] | None`
    > Coordinates preferentially incorporated into the initial chain.
  - `isolated_coordinates`: `Sequence[Sequence[int]] | None`
    > Coordinates whose endpoint atoms should not become unrelated parents.
  - `reparent_isolated_coordinates`: `bool`
    > Remove isolated-coordinate endpoints as references where alternatives exist.
  - `reparent_root_coordinates`: `bool`
    > Attempt to move root coordinates into the root chain.
  - `validate`: `bool`
    > Enable duplicate-parent and intermediate-tree checks.
  - `:returns`: `list[list[int]] | dict`
    > Reparented Z-matrix in the original input representation.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/enforce_required_zmatrix_coordinates.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/enforce_required_zmatrix_coordinates.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/enforce_required_zmatrix_coordinates.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/enforce_required_zmatrix_coordinates.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L2005?message=Update%20Docs)   
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