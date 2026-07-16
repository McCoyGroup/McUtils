# <a id="McUtils.Numputils.PermutationOps.commutator_evaluate">commutator_evaluate</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/PermutationOps.py#L329)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L329?message=Update%20Docs)]
</div>

```python
commutator_evaluate(commutator, expansion_terms, normalized=False, direct=None, recursive=False): 
```
**LLM Docstring**

Evaluate a nested operator commutator given the matrices for the individual
operators.

Three strategies are available: a `recursive` direct evaluation of `a @ b - b @
a`; a `direct` stack-based evaluation that memoizes sub-expressions; and an
expanded evaluation that sums the signed operator products from
`commutator_terms`. The strategy is auto-detected from the input shape when not
forced.
  - `commutator`: `Sequence`
    > the commutator specification (or precomputed term data)
  - `expansion_terms`: `Sequence[np.ndarray]`
    > the operator matrices indexed by label
  - `normalized`: `bool`
    > whether `commutator` is already expanded into terms
  - `direct`: `bool | None`
    > force (or disable) the stack-based direct evaluation
  - `recursive`: `bool`
    > force the recursive evaluation
  - `:returns`: `np.ndarray`
    > t
h
e
 
e
v
a
l
u
a
t
e
d
 
c
o
m
m
u
t
a
t
o
r
 
m
a
t
r
i
x











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/PermutationOps/commutator_evaluate.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/PermutationOps/commutator_evaluate.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/PermutationOps/commutator_evaluate.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/PermutationOps/commutator_evaluate.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L329?message=Update%20Docs)   
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