# <a id="McUtils.Numputils.CoordOps.delocalized_internal_coordinate_transformation">delocalized_internal_coordinate_transformation</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/CoordOps.py#L5180)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L5180?message=Update%20Docs)]
</div>

```python
delocalized_internal_coordinate_transformation(internals_by_cartesians, untransformed_coordinates=None, masses=None, relocalize=False): 
```
**LLM Docstring**

Construct a set of delocalized (non-redundant) internal coordinates from a
redundant internals-by-Cartesians transformation.

Optionally mass-weights the transformation and separates out any
`untransformed_coordinates` (projecting their contribution out of the remaining
coordinates so the space dimension is preserved). Diagonalizing the internal
`G` matrix and keeping the nonzero-eigenvalue eigenvectors yields the
delocalized transformation, which is optionally relocalized to align with the
untransformed coordinates.
  - `internals_by_cartesians`: `np.ndarray | list[np.ndarray]`
    > the redundant transformation (or its expansion)
  - `untransformed_coordinates`: `Iterable[int] | None`
    > coordinates to keep out of the delocalization
  - `masses`: `np.ndarray | None`
    > per-atom masses for mass-weighting
  - `relocalize`: `bool`
    > whether to relocalize onto the untransformed coordinates
  - `:returns`: `np.ndarray | list[np.ndarray]`
    > the delocalized coordinate transformation











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/CoordOps/delocalized_internal_coordinate_transformation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/CoordOps/delocalized_internal_coordinate_transformation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/CoordOps/delocalized_internal_coordinate_transformation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/CoordOps/delocalized_internal_coordinate_transformation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/CoordOps.py#L5180?message=Update%20Docs)   
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