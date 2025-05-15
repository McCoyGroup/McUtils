## <a id="McUtils.McUtils.Zachary.FittableModels.FittedModel">FittedModel</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels.py#L17)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels.py#L17?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_fit_method: str
```
<a id="McUtils.McUtils.Zachary.FittableModels.FittedModel.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, fit_basis, expansion_coeffs=None, basis_parameters=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/FittedModel.py#L18)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/FittedModel.py#L18?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.FittableModels.FittedModel.canonicalize_basis" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_basis(cls, fit_basis, basis_parameters): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L28)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L28?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.FittableModels.FittedModel.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, pts, order=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/FittedModel.py#L37)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/FittedModel.py#L37?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.FittableModels.FittedModel.evaluate_kernel" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
evaluate_kernel(cls, fit_basis, basis_parameters, pts, coeffs=None, order=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L48?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.FittableModels.FittedModel.get_kernel_and_opts" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_kernel_and_opts(cls, k): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L110)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L110?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.FittableModels.FittedModel.parse_kernel_specs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_kernel_specs(cls, kernels): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L126)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L126?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.FittableModels.FittedModel.nonlinear_fit" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
nonlinear_fit(cls, kernel_specs, pts, observations, include_expansion_coefficients=True, **fit_params): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L141)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L141?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.FittableModels.FittedModel.get_fit_methods" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_fit_methods(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L192)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L192?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.FittableModels.FittedModel.get_fit_dispatch" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_fit_dispatch(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L200)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L200?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.FittableModels.FittedModel.fit" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
fit(cls, kernels, pts, observations, method=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L212)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L212?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/FittableModels/FittedModel.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/FittableModels/FittedModel.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/FittableModels/FittedModel.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/FittableModels/FittedModel.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels.py#L17?message=Update%20Docs)   
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