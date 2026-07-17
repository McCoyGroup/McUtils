# <a id="McUtils.Coordinerds.Labels.get_mode_labels">get_mode_labels</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Labels.py#L221)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Labels.py#L221?message=Update%20Docs)]
</div>

```python
get_mode_labels(internals, internal_modes_by_coords: numpy.ndarray, norm_cutoff=0.8): 
```
**LLM Docstring**

Identify the internal coordinates that carry each normal mode and infer their common coordinate type.

Each column of `internal_modes_by_coords` is treated as one mode. Coordinate contributions are ranked by squared coefficient magnitude, and the shortest leading subset whose coefficient norm exceeds `norm_cutoff` is retained (or all coordinates if the threshold is never reached). The function then compares the retained tags component-by-component and keeps only type fields shared by every contributing coordinate; incompatible fields become `None`, and a fully incompatible mode receives no inferred type.
  - `internals`: `collections.abc.Sequence | dict`
    > Coordinate labels, or a mapping from externally meaningful coordinate indices to labels.
  - `internal_modes_by_coords`: `np.ndarray`
    > Matrix with coordinates along rows and modes along columns.
  - `norm_cutoff`: `float`
    > Euclidean norm threshold used to select the dominant coordinate subset for each mode.
  - `:returns`: `list[mode_label]`
    > One `mode_label(coefficients, indices, labels, type)` record per mode column.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Labels/get_mode_labels.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Labels/get_mode_labels.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Labels/get_mode_labels.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Labels/get_mode_labels.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Labels.py#L221?message=Update%20Docs)   
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