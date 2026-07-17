# <a id="McUtils.Coordinerds.ZMatrices.spoke_zmatrix">spoke_zmatrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L1356)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L1356?message=Update%20Docs)]
</div>

```python
spoke_zmatrix(m, spoke=1, root=1): 
```
**LLM Docstring**

Construct a root fragment with `m` copies of a spoke fragment attached to its terminal atom.

Integer `root` and `spoke` arguments are expanded as chain Z-matrices. If the root has fewer than three atoms, enough spoke atoms are first incorporated to establish three usable references. Remaining spokes are attached through the root terminal and two selected neighboring references.
  - `m`: `int`
    > Number of spoke copies to attach, reduced by any copies consumed to complete a short root.
  - `spoke`: `int | Sequence[Sequence[int]]`
    > Spoke fragment ordering or atom count for a chain spoke.
  - `root`: `int | Sequence[Sequence[int]]`
    > Root fragment ordering or atom count for a chain root.
  - `:returns`: `list[list[int]]`
    > Combined spoke-style Z-matrix.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/spoke_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/spoke_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/spoke_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/spoke_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L1356?message=Update%20Docs)   
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