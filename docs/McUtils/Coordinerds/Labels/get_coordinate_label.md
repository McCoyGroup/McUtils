# <a id="McUtils.Coordinerds.Labels.get_coordinate_label">get_coordinate_label</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Labels.py#L21)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Labels.py#L21?message=Update%20Docs)]
</div>

```python
get_coordinate_label(coord, atom_labels, atom_order=None): 
```
**LLM Docstring**

Build a structured label describing the chemical motif and optional ring/group membership of an internal coordinate.

Distance, bend, and dihedral coordinates are recognized either from an explicit tag or from integer tuples of length two, three, or four. Endpoint atom symbols are oriented canonically according to `atom_order`; bends and dihedrals may therefore be reversed. A ring or group label is retained only when the participating atoms satisfy the function's shared-membership rules. Unrecognized coordinates are labeled by concatenating the atom symbols in their supplied order (or across nested coordinate tuples).
  - `coord`: `tuple | dict | str`
    > Coordinate specification. It may be an atom-index tuple, a one-entry `{coordinate: tag}` mapping, or a string tag paired through the function's string-swapping convention.
  - `atom_labels`: `collections.abc.Sequence`
    > Per-atom records exposing `atom`, `ring`, and `group` attributes.
  - `atom_order`: `collections.abc.Sequence[str] | dict[str, int] | None`
    > Atom-symbol precedence used to orient endpoint-equivalent coordinates. A sequence is converted to a symbol-to-rank mapping.
  - `:returns`: `coordinate_label`
    > `(ring, group, atoms, type)` label for the coordinate.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Labels/get_coordinate_label.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Labels/get_coordinate_label.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Labels/get_coordinate_label.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Labels/get_coordinate_label.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Labels.py#L21?message=Update%20Docs)   
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