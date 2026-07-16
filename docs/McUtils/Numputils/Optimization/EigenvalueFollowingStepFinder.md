## <a id="McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder">EigenvalueFollowingStepFinder</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L3276)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L3276?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
line_search: ArmijoSearch
negative_eigenvalue_offset: float
positive_eigenvalue_offset: float
mode_tracking_overlap_cutoff: float
```
<a id="McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, func, jacobian, hessian, initial_beta=1, damping_parameter=None, damping_exponent=None, line_search=False, restart_interval=1, restart_hessian_norm=1e-05, hessian_approximator='bofill', approximation_mode='direct', target_mode=None, logger=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L3279)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L3279?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize an eigenvalue-following (P-RFO style) step finder, which shifts the
Hessian eigenvalues to walk toward a chosen stationary point.
  - `func`: `Callable`
    > the objective function
  - `jacobian`: `Callable`
    > the gradient function
  - `hessian`: `Callable`
    > the Hessian function
  - `initial_beta`: `float`
    > initial Hessian scale
  - `damping_parameter`: `float | None`
    > step-damping factor
  - `damping_exponent`: `float | None`
    > damping decay exponent
  - `line_search`: `bool | Callable`
    > line-search setting
  - `restart_interval`: `int`
    > damping restart interval
  - `restart_hessian_norm`: `float`
    > step-norm reset threshold
  - `hessian_approximator`: `str`
    > quasi-Newton scheme for Hessian updates
  - `approximation_mode`: `str`
    > `'direct'` or `'inverse'`
  - `target_mode`: `int | np.ndarray | None`
    > index/vector of the eigenmode to follow
  - `logger`: `object | None`
    > optional logger


<a id="McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.identities" class="docs-object-method">&nbsp;</a> 
```python
identities(self, guess, mask): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3351)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3351?message=Update%20Docs)]
</div>
**LLM Docstring**

Return (cached) identity matrices matching the active members' shape.
  - `guess`: `np.ndarray`
    > the current parameters
  - `mask`: `np.ndarray`
    > active-member indices
  - `:returns`: `np.ndarray`
    > the identity tensors


<a id="McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.initialize_hessians" class="docs-object-method">&nbsp;</a> 
```python
initialize_hessians(self, guess, mask): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3370)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3370?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the exact Hessian at the current point as the initial estimate.
  - `guess`: `np.ndarray`
    > the current parameters
  - `mask`: `np.ndarray`
    > active-member indices
  - `:returns`: `np.ndarray`
    > the Hessian


<a id="McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.get_hessian_update" class="docs-object-method">&nbsp;</a> 
```python
get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3385)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3385?message=Update%20Docs)]
</div>
**LLM Docstring**

Update the Hessian estimate using the configured quasi-Newton approximator.
  - `identities`: `np.ndarray`
    > identity matrices
  - `jacobian_diffs`: `np.ndarray`
    > gradient differences
  - `prev_steps`: `np.ndarray`
    > previous steps
  - `prev_hess`: `np.ndarray`
    > previous Hessian
  - `:returns`: `np.ndarray`
    > the updated Hessian


<a id="McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.get_shift" class="docs-object-method">&nbsp;</a> 
```python
get_shift(self, evals, tf_new, target_mode): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3407)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3407?message=Update%20Docs)]
</div>
**LLM Docstring**

Choose the eigenvalue shift used to control the step, following the target mode
(or the lowest eigenvalue) and offsetting to keep the shifted eigenvalue the
right sign.
  - `evals`: `np.ndarray`
    > the Hessian eigenvalues
  - `tf_new`: `np.ndarray`
    > the eigenvectors
  - `target_mode`: `np.ndarray | None`
    > the mode being followed (or `None`)
  - `:returns`: `np.ndarray`
    > the eigenvalue shift


<a id="McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.get_jacobian_updates" class="docs-object-method">&nbsp;</a> 
```python
get_jacobian_updates(self, guess, mask, gradient_modifer=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3443)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3443?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate the current gradient and its difference from the previous gradient.
  - `guess`: `np.ndarray`
    > the current parameters
  - `mask`: `np.ndarray`
    > active-member indices
  - `gradient_modifer`: `Callable | None`
    > optional gradient transformation
  - `:returns`: `tuple`
    > `(new_jacobians, jacobian_differences)`


<a id="McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.restart_hessian_approximation" class="docs-object-method">&nbsp;</a> 
```python
restart_hessian_approximation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3468)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3468?message=Update%20Docs)]
</div>
**LLM Docstring**

Decide whether to reset the Hessian approximation (on a near-zero previous
step).
  - `:returns`: `bool`
    > whether to restart


<a id="McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3483)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L3483?message=Update%20Docs)]
</div>
**LLM Docstring**

Produce an eigenvalue-following step: update the Hessian, diagonalize it, apply
the eigenvalue shift, and build the step in the eigenbasis (optionally
projected/line-searched/damped).
  - `guess`: `np.ndarray`
    > current parameters
  - `mask`: `np.ndarray | tuple`
    > active-member indices (or chain-minimizer tuple)
  - `return_vals`: `bool`
    > unsupported
  - `gradient_modifer`: `Callable | None`
    > optional gradient transformation
  - `projector`: `np.ndarray | None`
    > optional projector applied to the step
  - `:returns`: `tuple`
    > `(step, gradient)`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L3276?message=Update%20Docs)   
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