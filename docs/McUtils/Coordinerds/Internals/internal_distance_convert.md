# <a id="McUtils.Coordinerds.Internals.internal_distance_convert">internal_distance_convert</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L2884)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L2884?message=Update%20Docs)]
</div>

```python
internal_distance_convert(coords, specs, canonicalize=True, shift_dihedrals=True, abs_dihedrals=True, check_distance_spec=True): 
```
**LLM Docstring**

Convert internal-coordinate values to pair distances using a precomputed or newly generated conversion specification, optionally returning only generated values or validating distance completeness.
  - `coords`: `Any`
    > Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
  - `specs`: `Any`
    > Coordinate specifications associated with the numerical values.
  - `canonicalize`: `Any`
    > Whether to put coordinates in canonical orientation before comparison or storage.
  - `shift_dihedrals`: `Any`
    > Whether periodic dihedral values are shifted to the expected reconstruction branch.
  - `abs_dihedrals`: `Any`
    > Whether dihedral magnitudes are used for distance reconstruction.
  - `check_distance_spec`: `Any`
    > Whether the supplied distance-conversion specification is checked for completeness.
  - `:returns`: `Any`
    > The value or updated object described above.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Internals/internal_distance_convert.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Internals/internal_distance_convert.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Internals/internal_distance_convert.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Internals/internal_distance_convert.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L2884?message=Update%20Docs)   
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