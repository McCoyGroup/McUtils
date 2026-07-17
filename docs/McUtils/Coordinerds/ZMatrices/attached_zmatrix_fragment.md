# <a id="McUtils.Coordinerds.ZMatrices.attached_zmatrix_fragment">attached_zmatrix_fragment</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L1121)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L1121?message=Update%20Docs)]
</div>

```python
attached_zmatrix_fragment(n, zm, fragment, attachment_points): 
```
**LLM Docstring**

Translate a fragment Z-matrix from local indices and negative placeholders into a larger Z-matrix.

Negative entries index backward through `attachment_points`; nonnegative fragment-local indices are shifted by `n`. Before substitution, negative attachment points are resolved to clean references from the existing Z-matrix when possible.
  - `n`: `int`
    > Number of atoms already present; used as the local-index offset.
  - `zm`: `Sequence[Sequence[int]]`
    > Existing Z-matrix used to resolve attachment references.
  - `fragment`: `Sequence[Sequence[int]]`
    > Fragment rows in local index space.
  - `attachment_points`: `Sequence[int]`
    > External atoms replacing `-1`, `-2`, and `-3` placeholders.
  - `:returns`: `list[list[int]]`
    > Fragment rows expressed in the combined Z-matrix index space.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/attached_zmatrix_fragment.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/attached_zmatrix_fragment.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/attached_zmatrix_fragment.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/attached_zmatrix_fragment.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L1121?message=Update%20Docs)   
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