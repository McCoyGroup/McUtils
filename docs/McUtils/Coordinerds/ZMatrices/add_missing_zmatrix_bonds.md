# <a id="McUtils.Coordinerds.ZMatrices.add_missing_zmatrix_bonds">add_missing_zmatrix_bonds</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L1607)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L1607?message=Update%20Docs)]
</div>

```python
add_missing_zmatrix_bonds(base_zmat, bonds, max_iterations=None, validate_additions=True): 
```
**LLM Docstring**

Recursively add atoms connected by `bonds` but absent from a partial Z-matrix.

The input is canonicalized to row-index space. For each bond crossing from an included atom to an excluded atom, all newly reachable atoms are appended as a center-bound fragment attached to the included atom. The combined ordering is mapped back to original atom labels and the procedure repeats until no crossing bonds remain or `max_iterations` is exhausted.
  - `base_zmat`: `Sequence[Sequence[int]]`
    > Partial Z-matrix ordering.
  - `bonds`: `Sequence[tuple[int, int]]`
    > Full bond list in original atom-label space.
  - `max_iterations`: `int | None`
    > Maximum recursive expansion depth, or no limit.
  - `validate_additions`: `bool`
    > Validate before canonicalization, after attachment, and after reindexing.
  - `:returns`: `tuple[list[list[int]], dict[int, list[int]]]`
    > Expanded Z-matrix and a mapping from included attachment atoms to atoms discovered from them.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/add_missing_zmatrix_bonds.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/add_missing_zmatrix_bonds.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/add_missing_zmatrix_bonds.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/add_missing_zmatrix_bonds.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L1607?message=Update%20Docs)   
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