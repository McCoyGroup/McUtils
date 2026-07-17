# <a id="McUtils.Coordinerds.ZMatrices.validate_zmatrix">validate_zmatrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L922)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L922?message=Update%20Docs)]
</div>

```python
validate_zmatrix(ordering, allow_reordering=True, ensure_nonnegative=True, raise_exception=False, return_reason=False): 
```
**LLM Docstring**

Check that a Z-matrix ordering defines atoms before they are referenced and contains valid row references.

Embedding entries are normalized first. With reordering allowed, explicit atom labels are mapped to row positions and validation is repeated. The check rejects undefined atom labels, negative atom labels when prohibited, forward references, references larger than the row atom, duplicate indices within a row, and missing nonnegative references beyond the embedding rows.
  - `ordering`: `Sequence[Sequence[int]]`
    > Z-matrix ordering rows.
  - `allow_reordering`: `bool`
    > Permit arbitrary explicit atom labels by remapping them to row order.
  - `ensure_nonnegative`: `bool`
    > Require all real atom labels and required references to be nonnegative.
  - `raise_exception`: `bool`
    > Raise `ValueError` at the first failed check.
  - `return_reason`: `bool`
    > Return `(valid, reason)` rather than only a Boolean.
  - `:returns`: `bool | tuple[bool, str | None]`
    > Validation status, optionally paired with the failure explanation.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/validate_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/validate_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/validate_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/validate_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L922?message=Update%20Docs)   
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