# <a id="McUtils.Numputils.PermutationOps.commutator_terms">commutator_terms</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/PermutationOps.py#L304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L304?message=Update%20Docs)]
</div>

```python
commutator_terms(commutator_strings): 
```
**LLM Docstring**

Expand a commutator specification into all signed operator-product terms.

Normalizes the commutator (`normalize_commutators`) and then materializes every
product ordering with its phase via `_setup_com_terms`.
  - `commutator_strings`: `Sequence`
    > the commutator specification
  - `:returns`: `tuple[np.ndarray, np.ndarray]`
    > `
(
p
h
a
s
e
s
,
 
o
p
e
r
a
t
o
r
_
o
r
d
e
r
i
n
g
s
)
`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/PermutationOps/commutator_terms.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/PermutationOps/commutator_terms.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/PermutationOps/commutator_terms.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/PermutationOps/commutator_terms.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L304?message=Update%20Docs)   
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