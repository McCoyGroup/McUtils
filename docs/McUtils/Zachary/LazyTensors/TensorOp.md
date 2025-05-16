## <a id="McUtils.Zachary.LazyTensors.TensorOp">TensorOp</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/LazyTensors.py#L128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/LazyTensors.py#L128?message=Update%20Docs)]
</div>

A lazy representation of tensor operations to save memory







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.LazyTensors.TensorOp.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, a, b, axis=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/LazyTensors/TensorOp.py#L130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/LazyTensors/TensorOp.py#L130?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.LazyTensors.TensorOp.op" class="docs-object-method">&nbsp;</a> 
```python
op(self, a, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/LazyTensors/TensorOp.py#L148)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/LazyTensors/TensorOp.py#L148?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.LazyTensors.TensorOp.get_shape" class="docs-object-method">&nbsp;</a> 
```python
get_shape(self, a, b): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/LazyTensors/TensorOp.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/LazyTensors/TensorOp.py#L152?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.LazyTensors.TensorOp.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/LazyTensors/TensorOp.py#L154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/LazyTensors/TensorOp.py#L154?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.LazyTensors.TensorOp.array" class="docs-object-method">&nbsp;</a> 
```python
@property
array(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/LazyTensors/TensorOp.py#L157)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/LazyTensors/TensorOp.py#L157?message=Update%20Docs)]
</div>
Ought to always compile down to a proper ndarray
  - `:returns`: `np.ndarray`
    >


<a id="McUtils.Zachary.LazyTensors.TensorOp.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, i): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/LazyTensors/TensorOp.py#L165)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/LazyTensors/TensorOp.py#L165?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/LazyTensors/TensorOp.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/LazyTensors/TensorOp.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/LazyTensors/TensorOp.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/LazyTensors/TensorOp.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/LazyTensors.py#L128?message=Update%20Docs)   
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