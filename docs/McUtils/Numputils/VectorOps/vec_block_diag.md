# <a id="McUtils.Numputils.VectorOps.vec_block_diag">vec_block_diag</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L871)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L871?message=Update%20Docs)]
</div>

```python
vec_block_diag(mats, kroneckerize=True): 
```
**LLM Docstring**

Build block-diagonal matrices from a stack of matrices.

Each stacked matrix is placed on the diagonal of a larger `(stack, stack)`
block array (via `diag_indices`); when `kroneckerize` is set the block structure
is flattened into a single dense `(stack * rows, stack * cols)` matrix.
  - `mats`: `np.ndarray`
    > stack of matrices, shape `(..., stack, rows, cols)`
  - `kroneckerize`: `bool`
    > whether to flatten the block structure into a dense matrix
  - `:returns`: `np.ndarray`
    > t
h
e
 
b
l
o
c
k
-
d
i
a
g
o
n
a
l
 
m
a
t
r
i
c
e
s











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/vec_block_diag.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/vec_block_diag.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/vec_block_diag.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/vec_block_diag.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L871?message=Update%20Docs)   
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