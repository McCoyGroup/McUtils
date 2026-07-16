# <a id="McUtils.Numputils.PermutationOps.enumerate_permutations">enumerate_permutations</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/PermutationOps.py#L536)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L536?message=Update%20Docs)]
</div>

```python
enumerate_permutations(perm, cycle_orders=None): 
```
**LLM Docstring**

Enumerate the cyclic powers of a permutation (the subgroup it generates).

Repeatedly composes the permutation with itself, producing one array per power
up to its order. Batched inputs are handled per structure.
  - `perm`: `np.ndarray`
    > the permutation(s)
  - `cycle_orders`: `int | np.ndarray | None`
    > precomputed order(s) (computed if omitted)
  - `:returns`: `np.ndarray | list`
    > t
h
e
 
g
e
n
e
r
a
t
e
d
 
p
e
r
m
u
t
a
t
i
o
n
s
 
(
a
 
s
t
a
c
k
,
 
o
r
 
a
 
p
e
r
-
s
t
r
u
c
t
u
r
e
 
l
i
s
t
)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/PermutationOps/enumerate_permutations.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/PermutationOps/enumerate_permutations.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/PermutationOps/enumerate_permutations.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/PermutationOps/enumerate_permutations.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/PermutationOps.py#L536?message=Update%20Docs)   
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