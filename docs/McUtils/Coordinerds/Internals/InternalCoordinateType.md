## <a id="McUtils.Coordinerds.Internals.InternalCoordinateType">InternalCoordinateType</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L36)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L36?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L38)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L38?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_dispatch" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_dispatch(cls) -> 'dev.OptionsMethodDispatch': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L54)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L54?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.resolve" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve(cls, input): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L68)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L68?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.could_be" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
could_be(cls, input): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L85)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L85?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.equivalent_to" class="docs-object-method">&nbsp;</a> 
```python
equivalent_to(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L89)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L89?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.__eq__" class="docs-object-method">&nbsp;</a> 
```python
__eq__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L94)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L94?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.canonicalize" class="docs-object-method">&nbsp;</a> 
```python
canonicalize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L97)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L97?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_indices" class="docs-object-method">&nbsp;</a> 
```python
get_indices(self) -> 'Tuple[int, ...]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L101)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L101?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.__hash__" class="docs-object-method">&nbsp;</a> 
```python
__hash__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L105?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.reindex" class="docs-object-method">&nbsp;</a> 
```python
reindex(self, reindexing): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L107)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L107?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_carried_atoms" class="docs-object-method">&nbsp;</a> 
```python
get_carried_atoms(self, context: 'InternalSpec'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L111)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L111?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_constraint_rads" class="docs-object-method">&nbsp;</a> 
```python
get_constraint_rads(self) -> 'list[Distance | Angle | Dihedral]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L115?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_expansion" class="docs-object-method">&nbsp;</a> 
```python
get_expansion(self, coords, order=None, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L119?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_inverse_expansion" class="docs-object-method">&nbsp;</a> 
```python
get_inverse_expansion(self, coords, order=None, moved_indices=None, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L123)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L123?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L36?message=Update%20Docs)   
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