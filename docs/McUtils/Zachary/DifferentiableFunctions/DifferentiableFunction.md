## <a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction">DifferentiableFunction</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L19?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, inds=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L20?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.reindex" class="docs-object-method">&nbsp;</a> 
```python
reindex(self, idx_perm): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L23)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L23?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.get_consistent_inds" class="docs-object-method">&nbsp;</a> 
```python
get_consistent_inds(self, funcs: 'list[DifferentiableFunction]'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L31)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L31?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, coords, order=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L38)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L38?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.evaluate" class="docs-object-method">&nbsp;</a> 
```python
evaluate(self, coords, order=0) -> list[numpy.ndarray]: 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L57)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L57?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.get_children" class="docs-object-method">&nbsp;</a> 
```python
get_children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L61)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L61?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L65)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L65?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__radd__" class="docs-object-method">&nbsp;</a> 
```python
__radd__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L78)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L78?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L80)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L80?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__truediv__" class="docs-object-method">&nbsp;</a> 
```python
__truediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L93)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L93?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__rtruediv__" class="docs-object-method">&nbsp;</a> 
```python
__rtruediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L106)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L106?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__rmul__" class="docs-object-method">&nbsp;</a> 
```python
__rmul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L108)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L108?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.__neg__" class="docs-object-method">&nbsp;</a> 
```python
__neg__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L110)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L110?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.DifferentiableFunctions.DifferentiableFunction.flip" class="docs-object-method">&nbsp;</a> 
```python
flip(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L116)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.py#L116?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/DifferentiableFunctions/DifferentiableFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/DifferentiableFunctions.py#L19?message=Update%20Docs)   
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