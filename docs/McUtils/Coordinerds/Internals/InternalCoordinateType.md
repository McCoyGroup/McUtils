## <a id="McUtils.Coordinerds.Internals.InternalCoordinateType">InternalCoordinateType</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L35)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L35?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
registry: dict
```
<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.register" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
register(cls, type, typename=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L37)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L37?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_dispatch" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_dispatch(cls) -> 'dev.OptionsMethodDispatch': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L53)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L53?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.resolve" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve(cls, input): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L67)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L67?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.could_be" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
could_be(cls, input): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L84)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L84?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.equivalent_to" class="docs-object-method">&nbsp;</a> 
```python
equivalent_to(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L88)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L88?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.__eq__" class="docs-object-method">&nbsp;</a> 
```python
__eq__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L93)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L93?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.canonicalize" class="docs-object-method">&nbsp;</a> 
```python
canonicalize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L96)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L96?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_indices" class="docs-object-method">&nbsp;</a> 
```python
get_indices(self) -> 'Tuple[int, ...]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L100)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L100?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.__hash__" class="docs-object-method">&nbsp;</a> 
```python
__hash__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L104)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L104?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.reindex" class="docs-object-method">&nbsp;</a> 
```python
reindex(self, reindexing): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L106)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L106?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_carried_atoms" class="docs-object-method">&nbsp;</a> 
```python
get_carried_atoms(self, context: 'InternalSpec'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L110)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L110?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_expansion" class="docs-object-method">&nbsp;</a> 
```python
get_expansion(self, coords, order=None, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L114)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L114?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_inverse_expansion" class="docs-object-method">&nbsp;</a> 
```python
get_inverse_expansion(self, coords, order=None, moved_indices=None, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L118)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L118?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Internals/InternalCoordinateType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Internals/InternalCoordinateType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Internals/InternalCoordinateType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Internals/InternalCoordinateType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L35?message=Update%20Docs)   
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