# <a id="McUtils.Numputils.Optimization.polyfit_critical_points">polyfit_critical_points</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L4554)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L4554?message=Update%20Docs)]
</div>

```python
polyfit_critical_points(x, y, fit_order=2, check_curvature=None, curvature_test=None): 
```
**LLM Docstring**

Fit a polynomial to `(x, y)` and return the critical points of the fit (roots of
its derivative), optionally filtered by a curvature test.
  - `x`: `np.ndarray`
    > the sample abscissae
  - `y`: `np.ndarray`
    > the sample values
  - `fit_order`: `int`
    > the polynomial degree
  - `check_curvature`: `bool | None`
    > also compute the curvature at each critical point
  - `curvature_test`: `Callable | None`
    > predicate selecting critical points by curvature sign
  - `:returns`: `tuple`
    > `(roots, values[, curvature])`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Optimization/polyfit_critical_points.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Optimization/polyfit_critical_points.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Optimization/polyfit_critical_points.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Optimization/polyfit_critical_points.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L4554?message=Update%20Docs)   
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