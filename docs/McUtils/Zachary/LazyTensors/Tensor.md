## <a id="McUtils.McUtils.Zachary.LazyTensors.Tensor">Tensor</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors.py#L19?message=Update%20Docs)]
</div>

A semi-symbolic representation of a tensor. Allows for lazy processing of tensor operations.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, a, shape=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L21)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L21?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.from_array" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_array(cls, a, shape=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L24)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L24?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.array" class="docs-object-method">&nbsp;</a> 
```python
@property
array(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L30)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L30?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.get_shape" class="docs-object-method">&nbsp;</a> 
```python
get_shape(self, a): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L37)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L37?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L39)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L39?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.get_dim" class="docs-object-method">&nbsp;</a> 
```python
get_dim(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L42)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L42?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.dim" class="docs-object-method">&nbsp;</a> 
```python
@property
dim(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L44)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L44?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.add" class="docs-object-method">&nbsp;</a> 
```python
add(self, other, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L48?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.mul" class="docs-object-method">&nbsp;</a> 
```python
mul(self, other, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L50)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L50?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.dot" class="docs-object-method">&nbsp;</a> 
```python
dot(self, other, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L52)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L52?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.transpose" class="docs-object-method">&nbsp;</a> 
```python
transpose(self, axes, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L54)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L54?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.pow" class="docs-object-method">&nbsp;</a> 
```python
pow(self, other, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L56)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L56?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L59)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L59?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.__rmul__" class="docs-object-method">&nbsp;</a> 
```python
__rmul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L64)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L64?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L69)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L69?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.__pow__" class="docs-object-method">&nbsp;</a> 
```python
__pow__(self, power, modulo=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L71)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L71?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.handle_missing_indices" class="docs-object-method">&nbsp;</a> 
```python
handle_missing_indices(self, missing, extant): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L74)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L74?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.pull_index" class="docs-object-method">&nbsp;</a> 
```python
pull_index(self, *idx): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L77)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L77?message=Update%20Docs)]
</div>
Defines custom logic for handling how we pull indices
  - `idx`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L103)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L103?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.LazyTensors.Tensor.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/LazyTensors/Tensor.py#L109)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors/Tensor.py#L109?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/LazyTensors/Tensor.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/LazyTensors/Tensor.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/LazyTensors/Tensor.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/LazyTensors/Tensor.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/LazyTensors.py#L19?message=Update%20Docs)   
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