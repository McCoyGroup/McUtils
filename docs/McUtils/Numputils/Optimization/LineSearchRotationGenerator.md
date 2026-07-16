## <a id="McUtils.Numputils.Optimization.LineSearchRotationGenerator">LineSearchRotationGenerator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L4217)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L4217?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Numputils.Optimization.LineSearchRotationGenerator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, column_function, tol=1e-16, max_iterations=10): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L4218)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L4218?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize a rotation generator that finds each optimal 2x2 rotation angle by a
quadratic-interpolation line search.
  - `column_function`: `Callable`
    > the per-column objective contribution
  - `tol`: `float`
    > convergence tolerance
  - `max_iterations`: `int`
    > maximum line-search iterations


<a id="McUtils.Numputils.Optimization.LineSearchRotationGenerator.quadratic_opt" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
quadratic_opt(self, g0, g1, g2, f0, f1, f2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4236)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4236?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the vertex of the parabola through three `(angle, value)` samples (the
quadratic-interpolation optimum), or `None` when the samples are collinear.
  - `g0`: `float`
    > first angle
  - `g1`: `float`
    > second angle
  - `g2`: `float`
    > third angle
  - `f0`: `float`
    > value at the first angle
  - `f1`: `float`
    > value at the second angle
  - `f2`: `float`
    > value at the third angle
  - `:returns`: `float | None`
    > the interpolated optimum angle, or `None`


<a id="McUtils.Numputils.Optimization.LineSearchRotationGenerator.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, mat, col_i, col_j): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/LineSearchRotationGenerator.py#L4299)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/LineSearchRotationGenerator.py#L4299?message=Update%20Docs)]
</div>
**LLM Docstring**

Find the optimal 2x2 rotation for a pair of columns by quadratic-interpolation
line search over the rotation angle.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Optimization/LineSearchRotationGenerator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Optimization/LineSearchRotationGenerator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Optimization/LineSearchRotationGenerator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Optimization/LineSearchRotationGenerator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L4217?message=Update%20Docs)   
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