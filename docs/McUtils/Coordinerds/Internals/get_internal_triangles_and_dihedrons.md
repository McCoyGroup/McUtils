# <a id="McUtils.Coordinerds.Internals.get_internal_triangles_and_dihedrons">get_internal_triangles_and_dihedrons</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L3272)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L3272?message=Update%20Docs)]
</div>

```python
get_internal_triangles_and_dihedrons(internals, canonicalize=True, base=None, base_internals=None, construct_shapes=True, prune_incomplete=True, validate=False, allow_partially_defined=True, create_compound_dihedra=True, add_dihedron_triangles=False, create_dihedra=True) -> 'tuple[dict[tuple[int, int, int], nput.TriangleData], dict[tuple[int, int, int, int], nput.DihedralTetrahedronData]]': 
```
**LLM Docstring**

Construct a dependency-ordered triangulation of an internal-coordinate set. It identifies complete triangles and tetrahedra, records how missing pair distances are generated from angles or dihedrals, and can return auxiliary maps describing coordinate provenance and unresolved terms.
  - `internals`: `Any`
    > Available internal-coordinate specifications or their numerical values.
  - `canonicalize`: `Any`
    > Whether to put coordinates in canonical orientation before comparison or storage.
  - `base`: `Any`
    > Existing triangulation data used as the starting point for adding new coordinates.
  - `base_internals`: `Any`
    > Coordinates already accepted by the nonredundancy checker.
  - `construct_shapes`: `Any`
    > Whether explicit triangle and dihedron shape records are constructed rather than only dependency metadata.
  - `prune_incomplete`: `Any`
    > Whether triangle or dihedron candidates lacking enough defining information are discarded.
  - `validate`: `Any`
    > Whether the resulting triangulation is checked for consistency before being returned.
  - `allow_partially_defined`: `Any`
    > Whether shapes with unresolved terms are retained for later completion.
  - `create_compound_dihedra`: `Any`
    > Whether overlapping dihedrons may be combined into compound conversion records.
  - `add_dihedron_triangles`: `Any`
    > Whether triangular faces implied by accepted dihedrons are inserted into the triangle set.
  - `create_dihedra`: `Any`
    > Whether four-atom dihedron records are generated at all.
  - `:returns`: `tuple`
    > Triangle and dihedron triangulation records, with optional auxiliary conversion data selected by the function options.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Internals/get_internal_triangles_and_dihedrons.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Internals/get_internal_triangles_and_dihedrons.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Internals/get_internal_triangles_and_dihedrons.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Internals/get_internal_triangles_and_dihedrons.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L3272?message=Update%20Docs)   
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