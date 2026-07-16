# <a id="McUtils.Numputils.Optimization.iterative_chain_minimize">iterative_chain_minimize</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L814)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L814?message=Update%20Docs)]
</div>

```python
iterative_chain_minimize(chain_guesses, step_predictors, jacobian=None, hessian=None, *, method=None, unitary=False, function=None, climb=None, climbing_nodes=None, climbing_node_identifier=None, generate_rotation=False, dtype='float64', orthogonal_directions=None, orthogonal_projection_generator=None, prevent_oscillations=None, region_constraints=None, convergence_metric=None, termination_function=None, reparametrizer=None, max_displacement=None, max_displacement_norm=None, tol=1e-08, max_iterations=100, use_max_for_error=True, periodic=False, reembed=None, embedding_options=None, fixed_images=None, return_trajectory=False, logger=None, log_guess=False): 
```
**LLM Docstring**

Minimize a chain of images (e.g. a reaction path) by applying per-image step
finders, with optional climbing-image, spring/NEB, reparametrization, and
re-embedding support.

Generalizes `iterative_step_minimize` to a `(batch, n_images, n)` chain: each
image is stepped by its own step finder (which sees its neighbours through the
chain step-finder wrappers), climbing images are handled specially, and the
chain can be reparametrized/re-embedded between iterations.
  - `chain_guesses`: `np.ndarray`
    > the initial chain(s), shape `(..., n_images, n)`
  - `step_predictors`: `Callable | Iterable`
    > one step finder (broadcast) or one per image
  - `jacobian`: `Callable | None`
    > the per-image gradient function
  - `hessian`: `Callable | None`
    > the per-image Hessian function
  - `method`: `str | type | None`
    > the optimization method name/class
  - `unitary`: `bool`
    > constrain images to the unit sphere
  - `function`: `Callable | None`
    > the image objective (for climbing detection / tracking)
  - `climb`: `bool | None`
    > enable climbing-image behavior
  - `climbing_nodes`: `Iterable[int] | None`
    > explicit climbing-image indices
  - `climbing_node_identifier`: `Callable | None`
    > callable choosing the climbing image(s)
  - `generate_rotation`: `bool`
    > also return unitary rotations (unsupported)
  - `dtype`: `str`
    > working dtype
  - `orthogonal_directions`: `np.ndarray | None`
    > directions to project out of every step
  - `orthogonal_projection_generator`: `Callable | None`
    > per-guess projector generator
  - `prevent_oscillations`: `bool | int | None`
    > oscillation-detection history length
  - `region_constraints`: `np.ndarray | None`
    > per-coordinate bounds
  - `convergence_metric`: `Callable | None`
    > unused placeholder
  - `termination_function`: `Callable | None`
    > optional early-termination predicate
  - `reparametrizer`: `Callable | None`
    > callable redistributing images along the path
  - `max_displacement`: `float | None`
    > cap on the max per-coordinate step
  - `max_displacement_norm`: `float | None`
    > cap on the step norm
  - `tol`: `float`
    > gradient convergence tolerance
  - `max_iterations`: `int`
    > maximum iterations
  - `use_max_for_error`: `bool`
    > use max-abs gradient rather than its norm as the error
  - `periodic`: `bool`
    > treat the chain as periodic (wrap endpoints)
  - `reembed`: `bool | None`
    > re-embed images between iterations
  - `embedding_options`: `dict | None`
    > options for the re-embedding
  - `fixed_images`: `Iterable[int] | None`
    > image indices to hold fixed (e.g. endpoints)
  - `return_trajectory`: `bool`
    > also return the trajectory
  - `logger`: `object | None`
    > optional logger
  - `log_guess`: `bool`
    > log each image guess
  - `:returns`: `tuple`
    > `(chain, converged, (errors, iterations))` (plus trajectory if requested)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Optimization/iterative_chain_minimize.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Optimization/iterative_chain_minimize.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Optimization/iterative_chain_minimize.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Optimization/iterative_chain_minimize.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L814?message=Update%20Docs)   
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