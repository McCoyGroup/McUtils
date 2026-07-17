# <a id="McUtils.Coordinerds.Internals.find_internal_conversion">find_internal_conversion</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L4601)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L4601?message=Update%20Docs)]
</div>

```python
find_internal_conversion(internals, targets, triangles_and_dihedrons=None, canonicalize=True, allow_completion=True, return_conversions=False, prep_conversions=True, include_shapes=False, indices=None, cache=None, disallowed_conversions=None, update_triangles_and_dihedrons=False, return_completions=False, allow_recursive_completions=None, allow_ambiguous_completions=False, dihedral_intersections=None, index_mapping=None, verbose=False, missing_val='raise'): 
```
**LLM Docstring**

Build a conversion from an available internal-coordinate set to requested target coordinates. It first reuses direct coordinates, then searches triangle and dihedron records, completion relations, and paired tetrahedra, returning conversion callables with provenance for each target.
  - `internals`: `Any`
    > Available internal-coordinate specifications or their numerical values.
  - `targets`: `Any`
    > Coordinates or atom sets whose supporting triangulation is requested.
  - `triangles_and_dihedrons`: `Any`
    > Precomputed triangle and dihedron records used instead of rebuilding the triangulation.
  - `canonicalize`: `Any`
    > Whether to put coordinates in canonical orientation before comparison or storage.
  - `allow_completion`: `Any`
    > Whether missing intermediate coordinates may be reconstructed.
  - `return_conversions`: `Any`
    > Whether conversion objects and provenance are returned rather than only converted values.
  - `prep_conversions`: `Any`
    > Whether returned conversion specifications are wrapped as directly callable objects.
  - `include_shapes`: `Any`
    > Whether shape records supporting each conversion are included in the result metadata.
  - `indices`: `Any`
    > Atom indices defining the coordinate, or a restricted search index set.
  - `cache`: `Any`
    > Optional mutable cache of triangulation or conversion results.
  - `disallowed_conversions`: `Any`
    > Coordinate conversions that must not be used while searching for a target conversion.
  - `update_triangles_and_dihedrons`: `Any`
    > Whether completed intermediate coordinates are inserted back into the working triangulation.
  - `return_completions`: `Any`
    > Whether conversions for newly reconstructed intermediate coordinates are returned.
  - `allow_recursive_completions`: `Any`
    > Whether completing one coordinate may recursively request additional intermediate completions.
  - `allow_ambiguous_completions`: `Any`
    > Whether a missing intermediate may be accepted when more than one completion path exists.
  - `dihedral_intersections`: `Any`
    > Allowed overlap rules when combining multiple dihedron records for a conversion.
  - `index_mapping`: `Any`
    > Optional mapping from canonical coordinate indices to columns in the supplied value array.
  - `verbose`: `Any`
    > Whether diagnostic information is emitted during the search.
  - `missing_val`: `Any`
    > Value to return for a missing coordinate, or `"raise"` to raise.
  - `:returns`: `Any`
    > Conversion objects or a combined callable that produces the requested target coordinates.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Internals/find_internal_conversion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Internals/find_internal_conversion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Internals/find_internal_conversion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Internals/find_internal_conversion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L4601?message=Update%20Docs)   
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