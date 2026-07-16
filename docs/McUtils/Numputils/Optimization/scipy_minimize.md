# <a id="McUtils.Numputils.Optimization.scipy_minimize">scipy_minimize</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L508)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L508?message=Update%20Docs)]
</div>

```python
scipy_minimize(coords, function, jacobian=None, hessian=None, optimizer_settings=None, unitary=True, orthogonal_projector=None, orthogonal_projection_generator=None, line_search=None, return_trajectory=False, method='bfgs', max_iterations=None, tol=1e-08, line_search_step=None, max_displacement=0.01, region_constraints=None, logger=None): 
```
**LLM Docstring**

Minimize a function with `scipy.optimize.minimize`, wired up for this module's
conventions (batched-style flattening, optional unitary/orthogonal projection,
displacement capping, trajectory logging).

When line search is disabled, `scipy`'s Wolfe line search is temporarily
monkey-patched with a fixed-max-displacement step so each step size is bounded.
  - `coords`: `np.ndarray`
    > the starting coordinates
  - `function`: `Callable`
    > the objective function
  - `jacobian`: `Callable | None`
    > the gradient function
  - `hessian`: `Callable | None`
    > the Hessian function
  - `optimizer_settings`: `dict | None`
    > extra options passed through to `scipy`
  - `unitary`: `bool`
    > apply a unit-sphere projection to the gradient
  - `orthogonal_projector`: `np.ndarray | None`
    > fixed projector applied to the gradient
  - `orthogonal_projection_generator`: `Callable | None`
    > per-guess projector generator
  - `line_search`: `bool | None`
    > whether to use `scipy`'s line search (else fixed steps)
  - `return_trajectory`: `bool`
    > also return the optimization trajectory
  - `method`: `str`
    > the `scipy` method (`'quasi-newton'` maps to BFGS)
  - `max_iterations`: `int | None`
    > maximum iterations
  - `tol`: `float`
    > gradient tolerance
  - `line_search_step`: `float | None`
    > fixed step to return when line search is off
  - `max_displacement`: `float`
    > cap on the max per-coordinate step
  - `region_constraints`: `dict | None`
    > per-coordinate bounds
  - `logger`: `object | None`
    > optional logger
  - `:returns`: `tuple`
    > `(success, result[, scipy_result])`, with a trajectory when requested











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Optimization/scipy_minimize.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Optimization/scipy_minimize.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Optimization/scipy_minimize.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Optimization/scipy_minimize.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L508?message=Update%20Docs)   
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