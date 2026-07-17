## <a id="McUtils.Coordinerds.Redundant.RedundantCoordinateGenerator">RedundantCoordinateGenerator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant.py#L13)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant.py#L13?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Coordinerds.Redundant.RedundantCoordinateGenerator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, coordinate_specs, angle_ordering='ijk', untransformed_coordinates=None, masses=None, relocalize=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant.py#L15?message=Update%20Docs)]
</div>
**LLM Docstring**

Store the coordinate specification and options used to construct nonredundant combinations of redundant internals.

`angle_ordering` is inserted into the option dictionary passed to internal-coordinate tensor generation. Optional fixed coordinates, masses, and relocalization behavior become defaults for later calls to `compute_redundant_expansions`.
  - `coordinate_specs`: `collections.abc.Sequence`
    > Internal-coordinate definitions consumed by `internal_coordinate_tensors`.
  - `angle_ordering`: `str`
    > Angular derivative/index convention forwarded as an option.
  - `untransformed_coordinates`: `collections.abc.Sequence[int] | None`
    > Coordinate positions that should remain explicit rather than mixed into the redundant transformation.
  - `masses`: `np.ndarray | None`
    > Atom or Cartesian-component masses used for mass weighting.
  - `relocalize`: `bool`
    > Whether to rotate the nonredundant basis toward selected original coordinates.
  - `opts`: `dict`
    > Additional options forwarded to internal-coordinate tensor generation.
  - `:returns`: `None`
    > None.


<a id="McUtils.Coordinerds.Redundant.RedundantCoordinateGenerator.base_redundant_transformation" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
base_redundant_transformation(cls, expansion, untransformed_coordinates=None, masses=None, relocalize=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L115?message=Update%20Docs)]
</div>
**LLM Docstring**

Extract an orthonormal basis for the non-null internal-coordinate subspace from a Cartesian-to-internal derivative expansion.

The first expansion tensor is optionally mass weighted by `1/sqrt(mass)`; atom masses are repeated over Cartesian components when necessary. When fixed coordinates are requested, their derivative columns are placed first and projected out of the remaining columns so they stay explicit without reducing rank. The internal metric `G = B.T @ B` is diagonalized, eigenvectors with eigenvalues above `1e-10` are retained, and their order is reversed. Optional relocalization rotates this basis toward original coordinate axes.
  - `expansion`: `collections.abc.Sequence[np.ndarray]`
    > Derivative expansion whose first element is the Cartesian-to-internal Jacobian `B`.
  - `untransformed_coordinates`: `collections.abc.Sequence[int] | None`
    > Internal-coordinate column indices that should remain explicit in the basis.
  - `masses`: `np.ndarray | None`
    > Atom masses or Cartesian-component masses for mass weighting.
  - `relocalize`: `bool`
    > Whether to rotate the retained eigenvector basis toward original coordinate axes.
  - `:returns`: `np.ndarray | list[np.ndarray]`
    > Transformation matrix or per-batch list mapping redundant internals to the retained non-null basis.


<a id="McUtils.Coordinerds.Redundant.RedundantCoordinateGenerator.get_redundant_transformation" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_redundant_transformation(cls, base_expansions, untransformed_coordinates=None, masses=None, relocalize=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L217)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L217?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct the nonredundant transformation and re-expand derivative tensors into that basis.

The input may be a single 2-D Jacobian, a derivative expansion sequence, or `(forward_expansions, inverse_expansions)`. After `base_redundant_transformation` determines the basis, `tensor_reexpand` applies it to every derivative order. If inverse expansions are supplied, they are transformed with the transposed basis and returned alongside the forward expansions. Batched transformations represented as a list are processed independently.
  - `base_expansions`: `np.ndarray | collections.abc.Sequence | tuple`
    > Forward derivative tensors, optionally paired with inverse derivative tensors.
  - `untransformed_coordinates`: `collections.abc.Sequence[int] | None`
    > Coordinate indices preserved explicitly in the transformation.
  - `masses`: `np.ndarray | None`
    > Masses used to weight the base Jacobian.
  - `relocalize`: `bool`
    > Whether to rotate the basis toward original coordinate axes.
  - `:returns`: `tuple`
    > `(transformation, transformed_expansions)`, where transformed expansions may itself be `(forward, inverse)`.


<a id="McUtils.Coordinerds.Redundant.RedundantCoordinateGenerator.compute_redundant_expansions" class="docs-object-method">&nbsp;</a> 
```python
compute_redundant_expansions(self, coords, order=None, untransformed_coordinates=None, expansions=None, relocalize=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Redundant/RedundantCoordinateGenerator.py#L274)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant/RedundantCoordinateGenerator.py#L274?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate Cartesian derivatives of the configured redundant coordinates and transform them to a nonredundant basis.

Unless derivative tensors are supplied directly, `internal_coordinate_tensors` is evaluated for `coords` and `self.specs`; its coordinate values are discarded and derivative orders are retained. The requested order defaults to one. Instance defaults for fixed coordinates, masses, relocalization, angle ordering, and other options are then passed to `get_redundant_transformation`.
  - `coords`: `np.ndarray`
    > Cartesian coordinates at which internal-coordinate derivatives are evaluated.
  - `order`: `int | None`
    > Highest derivative order. Defaults to one when omitted.
  - `untransformed_coordinates`: `collections.abc.Sequence[int] | None`
    > Override for coordinate positions kept explicit.
  - `expansions`: `collections.abc.Sequence[np.ndarray] | None`
    > Precomputed derivative expansion, bypassing `internal_coordinate_tensors`.
  - `relocalize`: `bool | None`
    > Override for whether the basis is localized toward original coordinates.
  - `:returns`: `tuple`
    > Nonredundant transformation and transformed derivative expansions.


<a id="McUtils.Coordinerds.Redundant.RedundantCoordinateGenerator.prune_coordinate_specs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prune_coordinate_specs(cls, expansion, masses=None, untransformed_coordinates=None, pruning_mode='loc', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L469)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L469?message=Update%20Docs)]
</div>
**LLM Docstring**

Mass-weight a coordinate Jacobian and dispatch one of the supported column-selection algorithms.

The first expansion tensor is interpreted as a Cartesian-to-internal Jacobian. Atom masses are repeated three times when their count matches one third of the Cartesian row count, then the Jacobian is left-multiplied by `diag(1/sqrt(mass))`. `pruning_mode` selects SVD localization, projector localization, or greedy condition-number pruning.
  - `expansion`: `collections.abc.Sequence[np.ndarray]`
    > Derivative expansion whose first element is the coordinate Jacobian.
  - `masses`: `np.ndarray`
    > Atom or Cartesian-component masses. The implementation requires this argument despite its default of `None`.
  - `untransformed_coordinates`: `collections.abc.Sequence[int] | None`
    > Coordinate columns that must be retained.
  - `pruning_mode`: `str`
    > One of `"svd"`, `"loc"`, or `"gs"`.
  - `opts`: `dict`
    > Additional options passed to the selected pruning helper.
  - `:returns`: `np.ndarray`
    > Selected coordinate-column indices.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Redundant/RedundantCoordinateGenerator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Redundant/RedundantCoordinateGenerator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Redundant/RedundantCoordinateGenerator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Redundant/RedundantCoordinateGenerator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Redundant.py#L13?message=Update%20Docs)   
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