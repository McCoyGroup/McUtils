## <a id="McUtils.McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder">EigenvalueFollowingStepFinder</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L1504)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L1504?message=Update%20Docs)]
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
<a id="McUtils.McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, func, jacobian, hessian, initial_beta=1, damping_parameter=None, damping_exponent=None, line_search=False, restart_interval=1, restart_hessian_norm=1e-05, hessian_approximator='bofill', approximation_mode='direct', target_mode=None, logger=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1507)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1507?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.identities" class="docs-object-method">&nbsp;</a> 
```python
identities(self, guess, mask): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1546)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1546?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.initialize_hessians" class="docs-object-method">&nbsp;</a> 
```python
initialize_hessians(self, guess, mask): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1553)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1553?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.get_hessian_update" class="docs-object-method">&nbsp;</a> 
```python
get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1556)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1556?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.get_shift" class="docs-object-method">&nbsp;</a> 
```python
get_shift(self, evals, tf_new, target_mode): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1562)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1562?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.get_jacobian_updates" class="docs-object-method">&nbsp;</a> 
```python
get_jacobian_updates(self, guess, mask): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1582)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1582?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.restart_hessian_approximation" class="docs-object-method">&nbsp;</a> 
```python
restart_hessian_approximation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1591)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1591?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Numputils.Optimization.EigenvalueFollowingStepFinder.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, guess, mask, projector=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1597)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/EigenvalueFollowingStepFinder.py#L1597?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L1504?message=Update%20Docs)   
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