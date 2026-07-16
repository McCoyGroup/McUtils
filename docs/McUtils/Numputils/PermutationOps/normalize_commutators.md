# <a id="McUtils.Numputils.PermutationOps.normalize_commutators">normalize_commutators</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/PermutationOps.py#L158)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L158?message=Update%20Docs)]
</div>

```python
normalize_commutators(commutator_string): 
```
**LLM Docstring**

Rewrite a nested commutator specification into a canonical sum of nested
commutators over ordered operator labels.

Recursively applies commutator identities (antisymmetry and the Jacobi-style
regroupings) so that the result is expressed as a list of phases, a list of
normalized nested-commutator forms, and the ordered list of operator symbols
involved.
  - `commutator_string`: `Sequence`
    > the `[a, b]` commutator specification (nesting allowed)
  - `:returns`: `tuple[list, list, list]`
    > `(phases, normal_forms, symbols)`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/PermutationOps/normalize_commutators.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/PermutationOps/normalize_commutators.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/PermutationOps/normalize_commutators.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/PermutationOps/normalize_commutators.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L158?message=Update%20Docs)   
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