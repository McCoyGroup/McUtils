## <a id="McUtils.Numputils.Optimization.OperatorMatrixRotationGenerator">OperatorMatrixRotationGenerator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L4451)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L4451?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Numputils.Optimization.OperatorMatrixRotationGenerator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, one_e_func, matrix_func): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L4452)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L4452?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize a rotation generator that solves each optimal 2x2 rotation
analytically from a supplied 2x2 operator matrix.
  - `one_e_func`: `Callable`
    > the per-column objective contribution
  - `matrix_func`: `Callable`
    > callable giving the `(a, b, c)` operator-matrix entries for a pair


<a id="McUtils.Numputils.Optimization.OperatorMatrixRotationGenerator.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, mat, col_i, col_j): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/OperatorMatrixRotationGenerator.py#L4466)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/OperatorMatrixRotationGenerator.py#L4466?message=Update%20Docs)]
</div>
**LLM Docstring**

Find the optimal 2x2 rotation for a pair of columns by analytically diagonalizing
the supplied 2x2 operator matrix (the closed-form Jacobi angle).
  - `mat`: `np.ndarray`
    > the matrix being localized
  - `col_i`: `int`
    > the first column index
  - `col_j`: `int`
    > the second column index
  - `:returns`: `tuple`
    > `(cos, sin, gain)` for the optimal rotation
 </div>
</div>












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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Optimization/OperatorMatrixRotationGenerator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Optimization/OperatorMatrixRotationGenerator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Optimization/OperatorMatrixRotationGenerator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Optimization/OperatorMatrixRotationGenerator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L4451?message=Update%20Docs)   
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