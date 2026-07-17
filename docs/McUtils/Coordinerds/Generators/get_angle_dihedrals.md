# <a id="McUtils.Coordinerds.Generators.get_angle_dihedrals">get_angle_dihedrals</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Generators.py#L125)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators.py#L125?message=Update%20Docs)]
</div>

```python
get_angle_dihedrals(angles): 
```
**LLM Docstring**

Join compatible pairs of angles across a shared bond to form dihedrals.

The function recognizes angle pairs whose central bonds coincide after either endpoint orientation. It appends the nonshared endpoint from the second angle to the first angle, or prepends it when the shared bond is reversed. Cases that would repeat the first angle's remaining endpoint are skipped.
  - `angles`: `collections.abc.Sequence[tuple[int, int, int]]`
    > Angle triples `(endpoint_1, vertex, endpoint_2)`.
  - `:returns`: `list[tuple[int, int, int, int]]`
    > Four-atom dihedral coordinates assembled from compatible angle pairs.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Generators/get_angle_dihedrals.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Generators/get_angle_dihedrals.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Generators/get_angle_dihedrals.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Generators/get_angle_dihedrals.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Generators.py#L125?message=Update%20Docs)   
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