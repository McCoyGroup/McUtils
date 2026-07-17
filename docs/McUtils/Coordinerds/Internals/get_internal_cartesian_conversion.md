# <a id="McUtils.Coordinerds.Internals.get_internal_cartesian_conversion">get_internal_cartesian_conversion</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L5993)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L5993?message=Update%20Docs)]
</div>

```python
get_internal_cartesian_conversion(internals, triangles_and_dihedrons=None, canonicalize=True, missing_val='raise'): 
```
**LLM Docstring**

Construct a converter from internal-coordinate values to Cartesian geometries by composing internal-to-distance conversion with distance-geometry embedding.
  - `internals`: `Any`
    > Available internal-coordinate specifications or their numerical values.
  - `triangles_and_dihedrons`: `Any`
    > Precomputed triangle and dihedron records used instead of rebuilding the triangulation.
  - `canonicalize`: `Any`
    > Whether to put coordinates in canonical orientation before comparison or storage.
  - `missing_val`: `Any`
    > Value to return for a missing coordinate, or `"raise"` to raise.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Internals/get_internal_cartesian_conversion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Internals/get_internal_cartesian_conversion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Internals/get_internal_cartesian_conversion.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Internals/get_internal_cartesian_conversion.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L5993?message=Update%20Docs)   
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