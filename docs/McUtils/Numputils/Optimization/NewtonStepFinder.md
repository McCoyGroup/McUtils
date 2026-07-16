## <a id="McUtils.Numputils.Optimization.NewtonStepFinder">NewtonStepFinder</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L1974)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L1974?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
supports_hessian: bool
```
<a id="McUtils.Numputils.Optimization.NewtonStepFinder.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, func, jacobian=None, hessian=None, *, check_generator=True, logger=None, **generator_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L1976)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L1976?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize a Newton step finder, building a direct-Hessian generator from the
supplied Jacobian/Hessian unless one is already provided.
  - `func`: `Callable`
    > the objective function
  - `jacobian`: `Callable | None`
    > the gradient function (or a ready generator)
  - `hessian`: `Callable | None`
    > the Hessian function
  - `check_generator`: `bool`
    > build a generator when needed
  - `logger`: `object | None`
    > optional logger
  - `generator_opts`: `Any`
    > extra options for the generator


<a id="McUtils.Numputils.Optimization.NewtonStepFinder.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, guess, mask, return_vals=False, projector=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/NewtonStepFinder.py#L2030)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/NewtonStepFinder.py#L2030?message=Update%20Docs)]
</div>
**LLM Docstring**

Produce a Newton step for the active members.
  - `guess`: `np.ndarray`
    > current parameters
  - `mask`: `np.ndarray | tuple`
    > active-member indices (or chain-minimizer tuple)
  - `return_vals`: `bool`
    > unsupported
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Optimization/NewtonStepFinder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Optimization/NewtonStepFinder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Optimization/NewtonStepFinder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Optimization/NewtonStepFinder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L1974?message=Update%20Docs)   
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