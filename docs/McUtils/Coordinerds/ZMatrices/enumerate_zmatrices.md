# <a id="McUtils.Coordinerds.ZMatrices.enumerate_zmatrices">enumerate_zmatrices</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L314)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L314?message=Update%20Docs)]
</div>

```python
enumerate_zmatrices(coords, natoms=None, allow_permutation=True, include_origins=False, canonicalize=True, deduplicate=True, preorder_atoms=True, allow_completions=False): 
```
**LLM Docstring**

Enumerate Z-matrix orderings compatible with supplied internal coordinates.

The coordinate set is canonicalized and deduplicated. When `preorder_atoms` is enabled, atoms are ranked by how often they occur in the coordinate set so highly connected atoms are tried first. The function then considers every allowed atom permutation, rewrites each coordinate into that permutation's index space, asks `_zmatrix_iterate` for every complete choice of introducing dihedrals, and maps each yielded row back to the original atom labels.
  - `coords`: `Sequence[Sequence[int]]`
    > Available bond, angle, and dihedral coordinate tuples.
  - `natoms`: `int | None`
    > Number of atoms; inferred from coordinate indices when omitted.
  - `allow_permutation`: `bool`
    > Try all atom order permutations rather than only the preordered sequence.
  - `include_origins`: `bool`
    > Add the coordinates needed to define the first three atoms.
  - `canonicalize`: `bool`
    > Canonicalize coordinate directions before enumeration.
  - `deduplicate`: `bool`
    > Remove duplicate coordinate tuples.
  - `preorder_atoms`: `bool`
    > Start permutations from atoms sorted by coordinate participation count.
  - `allow_completions`: `bool`
    > Allow rows whose bond or angle prefixes were not explicitly supplied.
  - `:returns`: `Iterator[list[list[int]]]`
    > Z-matrix orderings in original atom-index space.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/enumerate_zmatrices.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/enumerate_zmatrices.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/enumerate_zmatrices.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/enumerate_zmatrices.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L314?message=Update%20Docs)   
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