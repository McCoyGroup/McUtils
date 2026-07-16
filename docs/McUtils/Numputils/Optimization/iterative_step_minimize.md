# <a id="McUtils.Numputils.Optimization.iterative_step_minimize">iterative_step_minimize</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L271?message=Update%20Docs)]
</div>

```python
iterative_step_minimize(guess, step_predictor, jacobian=None, hessian=None, *, method=None, unitary=False, generate_rotation=False, dtype='float64', orthogonal_directions=None, orthogonal_projection_generator=None, region_constraints=None, function=None, max_displacement=None, max_displacement_norm=None, oscillation_damping_factor=None, termination_function=None, prevent_oscillations=None, tol=1e-08, use_max_for_error=True, max_iterations=100, convergence_metric=None, track_best=False, return_trajectory=False, logger=None, log_guess=True): 
```
**LLM Docstring**

Minimize a function over a batch of starting guesses by repeatedly applying a
step finder until the gradient converges or the iteration cap is hit.

Supports batched guesses, orthogonal/unitary projection, region constraints,
oscillation damping, best-point tracking, and optional trajectory return. Each
iteration only advances the members that have not yet converged.
  - `guess`: `np.ndarray`
    > starting guesses, shape `(..., n)`
  - `step_predictor`: `Callable | dict | object`
    > a step finder, spec, or function
  - `jacobian`: `Callable | None`
    > the gradient function
  - `hessian`: `Callable | None`
    > the Hessian function
  - `method`: `str | type | None`
    > the optimization method name/class
  - `unitary`: `bool`
    > constrain the optimization to the unit sphere
  - `generate_rotation`: `bool`
    > also return the accumulated unitary rotation
  - `dtype`: `str`
    > working dtype for the guesses
  - `orthogonal_directions`: `np.ndarray | None`
    > directions to project out of every step
  - `orthogonal_projection_generator`: `Callable | None`
    > per-guess projector generator
  - `region_constraints`: `np.ndarray | None`
    > `(min, max)` bounds per coordinate
  - `function`: `Callable | None`
    > the objective (needed for best-value tracking)
  - `max_displacement`: `float | None`
    > cap on the max per-coordinate step
  - `max_displacement_norm`: `float | None`
    > cap on the step norm
  - `oscillation_damping_factor`: `float | None`
    > adaptive damping factor for oscillating steps
  - `termination_function`: `Callable | None`
    > optional early-termination predicate
  - `prevent_oscillations`: `bool | int | None`
    > keep this many prior steps for oscillation detection
  - `tol`: `float`
    > gradient convergence tolerance
  - `use_max_for_error`: `bool`
    > use max-abs gradient rather than its norm as the error
  - `max_iterations`: `int`
    > maximum number of iterations
  - `convergence_metric`: `Callable | None`
    > unused placeholder
  - `track_best`: `bool`
    > keep the best point/value seen per member
  - `return_trajectory`: `bool`
    > also return the per-iteration trajectory
  - `logger`: `object | None`
    > optional logger
  - `log_guess`: `bool`
    > log the guess at each iteration
  - `:returns`: `tuple`
    > `(result, converged, (errors, iterations))` (plus trajectory if requested)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Optimization/iterative_step_minimize.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Optimization/iterative_step_minimize.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Optimization/iterative_step_minimize.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Optimization/iterative_step_minimize.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L271?message=Update%20Docs)   
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