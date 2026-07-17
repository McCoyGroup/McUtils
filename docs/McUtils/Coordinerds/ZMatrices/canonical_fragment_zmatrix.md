# <a id="McUtils.Coordinerds.ZMatrices.canonical_fragment_zmatrix">canonical_fragment_zmatrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L2515)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L2515?message=Update%20Docs)]
</div>

```python
canonical_fragment_zmatrix(canonical_framents, validate_additions=False): 
```
**LLM Docstring**

Join preordered atom fragments into one canonical Z-matrix.

Each fragment is represented by a chain Z-matrix. The first fragment becomes the backbone; every later fragment is attached to the previous combined ordering using up to the last three existing atom positions as external references. The final local rows are reindexed to the concatenated original fragment labels.
  - `canonical_framents`: `Sequence[Sequence[int]]`
    > Atom-index fragments in the desired fragment and intra-fragment order.
  - `validate_additions`: `bool`
    > Validate the local and reindexed combined ordering.
  - `:returns`: `list[list[int]]`
    > Combined Z-matrix in original atom-label space.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/canonical_fragment_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/canonical_fragment_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/canonical_fragment_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/canonical_fragment_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L2515?message=Update%20Docs)   
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