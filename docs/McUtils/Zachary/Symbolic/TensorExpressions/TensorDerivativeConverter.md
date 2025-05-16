## <a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorDerivativeConverter">TensorDerivativeConverter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/TensorExpressions.py#L1691)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/TensorExpressions.py#L1691?message=Update%20Docs)]
</div>

A class that makes it possible to convert expressions
involving derivatives in one coordinate system in another







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
TensorExpansionError: TensorExpansionError
```
<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorDerivativeConverter.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, jacobians, derivatives=None, mixed_terms=None, jacobians_name='Q', values_name='V'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/TensorExpressions.py#L1700)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/TensorExpressions.py#L1700?message=Update%20Docs)]
</div>

  - `jacobians`: `Iterable[np.ndarray]`
    > The Jacobian and higher-order derivatives between the coordinate systems
  - `derivatives`: `Iterable[np.ndarray]`
    > Derivatives of some quantity in the original coordinate system
  - `mixed_terms`: `Iterable[Iterable[None | np.ndarray]]`
    > Mixed derivatives of some quantity involving the new and old coordinates


<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorDerivativeConverter.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, order=None, print_transformations=False, check_arrays=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/TensorExpressions/TensorDerivativeConverter.py#L1739)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/TensorExpressions/TensorDerivativeConverter.py#L1739?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorDerivativeConverter.compute_partition_terms" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
compute_partition_terms(cls, partition): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1764)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1764?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorDerivativeConverter.convert_partition" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
convert_partition(cls, partition, derivs, vals, val_axis=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1788)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1788?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorDerivativeConverter.convert_fast" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
convert_fast(cls, derivs, vals, val_axis=-1, order=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1826)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1826?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Symbolic/TensorExpressions/TensorDerivativeConverter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Symbolic/TensorExpressions/TensorDerivativeConverter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Symbolic/TensorExpressions/TensorDerivativeConverter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Symbolic/TensorExpressions/TensorDerivativeConverter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/TensorExpressions.py#L1691?message=Update%20Docs)   
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