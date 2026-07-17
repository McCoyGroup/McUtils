# <a id="McUtils.Coordinerds.Internals.get_internal_distance_conversion">get_internal_distance_conversion</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L5938)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L5938?message=Update%20Docs)]
</div>

```python
get_internal_distance_conversion(internals, triangles_and_dihedrons=None, dist_set=None, canonicalize=True, allow_completion=True, missing_val='raise', include_shapes=False, return_conversions=False, prep_conversions=True, cache=None): 
```
**LLM Docstring**

Return a callable that transforms internal-coordinate values into the pair distances required by their triangulation, along with optional conversion metadata.
  - `internals`: `Any`
    > Available internal-coordinate specifications or their numerical values.
  - `triangles_and_dihedrons`: `Any`
    > Precomputed triangle and dihedron records used instead of rebuilding the triangulation.
  - `dist_set`: `Any`
    > Optional known canonical distance set.
  - `canonicalize`: `Any`
    > Whether to put coordinates in canonical orientation before comparison or storage.
  - `allow_completion`: `Any`
    > Whether missing intermediate coordinates may be reconstructed.
  - `missing_val`: `Any`
    > Value to return for a missing coordinate, or `"raise"` to raise.
  - `include_shapes`: `Any`
    > Whether shape records supporting each conversion are included in the result metadata.
  - `return_conversions`: `Any`
    > Whether conversion objects and provenance are returned rather than only converted values.
  - `prep_conversions`: `Any`
    > Whether returned conversion specifications are wrapped as directly callable objects.
  - `cache`: `Any`
    > Optional mutable cache of triangulation or conversion results.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Internals/get_internal_distance_conversion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Internals/get_internal_distance_conversion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Internals/get_internal_distance_conversion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Internals/get_internal_distance_conversion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L5938?message=Update%20Docs)   
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