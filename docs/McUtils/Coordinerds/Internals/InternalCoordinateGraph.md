## <a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph">InternalCoordinateGraph</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L4573)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L4573?message=Update%20Docs)]
</div>

A graph mapping out the connections between a set of atoms based on the given set of internals







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
GraphCheckpoint: GraphCheckpoint
atoms: member_descriptor
internals: member_descriptor
triangulation: member_descriptor
```
<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, internals, atoms=None, triangles_and_dihedrons=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L4579)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L4579?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.enumerate_matching_dihedrons" class="docs-object-method">&nbsp;</a> 
```python
enumerate_matching_dihedrons(self, target_coord): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L4595)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L4595?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.find_conversions" class="docs-object-method">&nbsp;</a> 
```python
find_conversions(self, target_internals, unconvertable_atoms=None, allow_recursive_completions=False, find_unreachable=True, verbose=False, depth=0, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L4655)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L4655?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.checkpoint" class="docs-object-method">&nbsp;</a> 
```python
checkpoint(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L4786)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L4786?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.add_internals" class="docs-object-method">&nbsp;</a> 
```python
add_internals(self, internals): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L4789)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L4789?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.remove_internals" class="docs-object-method">&nbsp;</a> 
```python
remove_internals(self, internals): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L4855)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L4855?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/Internals/InternalCoordinateGraph.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/Internals/InternalCoordinateGraph.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/Internals/InternalCoordinateGraph.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/Internals/InternalCoordinateGraph.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L4573?message=Update%20Docs)   
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