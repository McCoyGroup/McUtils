# <a id="McUtils.Coordinerds.ZMatrices.sort_complex_attachment_points">sort_complex_attachment_points</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L2580)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L2580?message=Update%20Docs)]
</div>

```python
sort_complex_attachment_points(fragment_inds, attachment_points: 'dict|tuple[tuple[int], list[list[int]]]'): 
```
**LLM Docstring**

Orient and order complex-fragment attachment records into a connected fragment traversal.

Attachment endpoints are associated with the fragments containing them. Starting from `start_frag` when supplied, the routine repeatedly selects attachments that connect the current fragment to an unvisited fragment, reversing endpoint order when necessary. It returns fragments in traversal order together with attachment references keyed by the newly reached fragment.
  - `fragment_inds`: `Sequence[Sequence[int]]`
    > Atom indices for each disconnected fragment.
  - `attachment_points`: `dict | Iterable`
    > Mapping or iterable describing atom-level links between fragments.
  - `start_frag`: `int | None`
    > Optional fragment index from which to begin traversal.
  - `:returns`: `tuple[list[tuple[int, ...]], dict]`
    > Reordered fragments and attachment specifications for joining them.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/sort_complex_attachment_points.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/sort_complex_attachment_points.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/sort_complex_attachment_points.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/sort_complex_attachment_points.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L2580?message=Update%20Docs)   
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