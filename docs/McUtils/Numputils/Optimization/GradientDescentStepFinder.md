## <a id="McUtils.Numputils.Optimization.GradientDescentStepFinder">GradientDescentStepFinder</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L1771)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L1771?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
supports_hessian: bool
line_search: ArmijoSearch
```
<a id="McUtils.Numputils.Optimization.GradientDescentStepFinder.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, func, jacobian, damping_parameter=None, damping_exponent=None, line_search=True, restart_interval=10, logger=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L1775)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L1775?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize a gradient-descent step finder.
  - `func`: `Callable`
    > the objective function
  - `jacobian`: `Callable`
    > the gradient function
  - `damping_parameter`: `float | None`
    > base step-damping factor
  - `damping_exponent`: `float | None`
    > damping decay exponent
  - `line_search`: `bool | Callable`
    > `True` to use the default line search, `False`/`None` to disable
  - `restart_interval`: `int`
    > damping restart interval
  - `logger`: `object | None`
    > optional logger


<a id="McUtils.Numputils.Optimization.GradientDescentStepFinder.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/GradientDescentStepFinder.py#L1812)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/GradientDescentStepFinder.py#L1812?message=Update%20Docs)]
</div>
**LLM Docstring**

Produce a gradient-descent step (the negative gradient, optionally projected,
line-searched, and damped) for the active members.
  - `guess`: `np.ndarray`
    > current parameters
  - `mask`: `np.ndarray | tuple`
    > active-member indices (or `(mask, chain_data)` for chain minimizers)
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Optimization/GradientDescentStepFinder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Optimization/GradientDescentStepFinder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Optimization/GradientDescentStepFinder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Optimization/GradientDescentStepFinder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L1771?message=Update%20Docs)   
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