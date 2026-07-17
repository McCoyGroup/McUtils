# <a id="McUtils.Coordinerds.Generators.get_stretch_angle_dihedrals">get_stretch_angle_dihedrals</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators.py#L48?message=Update%20Docs)]
</div>

```python
get_stretch_angle_dihedrals(stretches, angles): 
```
**LLM Docstring**

Extend an angle by a bonded atom to form candidate dihedral coordinates.

Each stretch is compared with each angle. If both stretch atoms already occur in the angle, it is ignored. If exactly one stretch atom matches any angle position, the other atom is inserted at the corresponding end or adjacent position so the angle remains a contiguous three-atom segment of the resulting four-atom coordinate.
  - `stretches`: `collections.abc.Iterable[tuple[int, int]]`
    > Bond coordinates as atom-index pairs.
  - `angles`: `collections.abc.Iterable[tuple[int, int, int]]`
    > Angle coordinates as `(a, b, c)` triples.
  - `:returns`: `list[tuple[int, int, int, int]]`
    > Candidate four-atom dihedral coordinates.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Generators/get_stretch_angle_dihedrals.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Generators/get_stretch_angle_dihedrals.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Generators/get_stretch_angle_dihedrals.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Generators/get_stretch_angle_dihedrals.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators.py#L48?message=Update%20Docs)   
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