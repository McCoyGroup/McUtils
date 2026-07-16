# <a id="McUtils.Numputils.PermutationOps.permutation_cycles">permutation_cycles</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/PermutationOps.py#L415)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L415?message=Update%20Docs)]
</div>

```python
permutation_cycles(perms, return_groups=False): 
```
**LLM Docstring**

Decompose permutations into their disjoint cycles.

Assigns each position a cycle label (an integer group id); with
`return_groups` set, the actual cycle index lists are returned instead. Cannot
be vectorized past 2D, so batched inputs beyond a single stack are rejected when
groups are requested.
  - `perms`: `np.ndarray`
    > the permutation(s)
  - `return_groups`: `bool`
    > return explicit cycle index lists rather than labels
  - `:returns`: `np.ndarray | list`
    > per-position cycle labels, or the cycle groups











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/PermutationOps/permutation_cycles.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/PermutationOps/permutation_cycles.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/PermutationOps/permutation_cycles.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/PermutationOps/permutation_cycles.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L415?message=Update%20Docs)   
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