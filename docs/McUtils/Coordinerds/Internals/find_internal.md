# <a id="McUtils.Coordinerds.Internals.find_internal">find_internal</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L2231)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L2231?message=Update%20Docs)]
</div>

```python
find_internal(coords, coord, missing_val: "'Any'" = 'raise', canonicalize=True, allow_negation=False, indices=None): 
```
**LLM Docstring**

Find a coordinate in a coordinate list after optional canonicalization. The search can accept the sign-reversed equivalent of directed coordinates and can restrict matching to a supplied index subset.
  - `coords`: `Any`
    > Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
  - `coord`: `Any`
    > A single coordinate specification or target coordinate.
  - `missing_val`: `'Any'`
    > Value to return for a missing coordinate, or `"raise"` to raise.
  - `canonicalize`: `Any`
    > Whether to put coordinates in canonical orientation before comparison or storage.
  - `allow_negation`: `Any`
    > Whether sign-reversed directed coordinates count as matches.
  - `indices`: `Any`
    > Atom indices defining the coordinate, or a restricted search index set.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Internals/find_internal.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Internals/find_internal.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Internals/find_internal.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Internals/find_internal.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L2231?message=Update%20Docs)   
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