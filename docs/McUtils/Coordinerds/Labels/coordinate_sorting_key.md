# <a id="McUtils.Coordinerds.Labels.coordinate_sorting_key">coordinate_sorting_key</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Labels.py#L157)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Labels.py#L157?message=Update%20Docs)]
</div>

```python
coordinate_sorting_key(label, type_ordering=None, atom_ordering=None): 
```
**LLM Docstring**

Construct a sortable tuple that orders coordinates first by type and then by their constituent atom symbols.

Plain strings are interpreted as atom-symbol motifs and sorted first by motif length. Structured labels use `label.type` and `label.atoms`; unknown coordinate types receive rank `3`, and unknown atoms receive rank `-1`. Atom ranks are sorted internally, so endpoint orientation does not affect the key.
  - `label`: `str | coordinate_label`
    > Atom-symbol string or structured coordinate label with `type` and `atoms` fields.
  - `type_ordering`: `dict[str, int] | None`
    > Mapping from coordinate type names to primary sort ranks.
  - `atom_ordering`: `collections.abc.Sequence[str] | dict[str, int] | None`
    > Atom-symbol order, supplied as either a sequence or a rank mapping.
  - `:returns`: `tuple[int, ...]`
    > Tuple suitable for use as a sorting key.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Labels/coordinate_sorting_key.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Labels/coordinate_sorting_key.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Labels/coordinate_sorting_key.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Labels/coordinate_sorting_key.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Labels.py#L157?message=Update%20Docs)   
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