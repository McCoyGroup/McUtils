## <a id="McUtils.Numputils.Optimization.ConjugateGradientStepFinder">ConjugateGradientStepFinder</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L3022)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L3022?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
supports_hessian: bool
```
<a id="McUtils.Numputils.Optimization.ConjugateGradientStepFinder.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, func, jacobian, approximation_type='polak-ribiere', logger=None, **generator_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L3025)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L3025?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize a conjugate-gradient step finder, selecting the beta formula by name.
  - `func`: `Callable`
    > the objective function
  - `jacobian`: `Callable`
    > the gradient function
  - `approximation_type`: `str`
    > beta scheme (`'polak-ribiere'` or `'fletcher-reeves'`)
  - `logger`: `object | None`
    > optional logger
  - `generator_opts`: `Any`
    > extra options for the step approximator


<a id="McUtils.Numputils.Optimization.ConjugateGradientStepFinder.beta_approximations" class="docs-object-method">&nbsp;</a> 
```python
@property
beta_approximations(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/ConjugateGradientStepFinder.py#L3043)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/ConjugateGradientStepFinder.py#L3043?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the mapping from beta-formula name to its approximator class.
  - `:returns`: `dict`
    > the name-to-class mapping


<a id="McUtils.Numputils.Optimization.ConjugateGradientStepFinder.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/ConjugateGradientStepFinder.py#L3058)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/ConjugateGradientStepFinder.py#L3058?message=Update%20Docs)]
</div>
**LLM Docstring**

Produce a conjugate-gradient step for the active members.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Optimization/ConjugateGradientStepFinder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Optimization/ConjugateGradientStepFinder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Optimization/ConjugateGradientStepFinder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Optimization/ConjugateGradientStepFinder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L3022?message=Update%20Docs)   
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