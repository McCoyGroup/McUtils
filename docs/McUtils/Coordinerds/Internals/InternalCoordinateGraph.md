## <a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph">InternalCoordinateGraph</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L6396)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L6396?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals.py#L6402)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L6402?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize a mutable graph of internal coordinates, derive its triangulation and bond graph, and create caches for target conversions, expanded coordinates, and completed intermediates.
  - `internals`: `Any`
    > Available internal-coordinate specifications or their numerical values.
  - `atoms`: `Any`
    > Atoms to include or place.
  - `triangles_and_dihedrons`: `Any`
    > Precomputed triangle and dihedron records used instead of rebuilding the triangulation.
  - `:returns`: `None`
    > None.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.get_target_triangulation" class="docs-object-method">&nbsp;</a> 
```python
get_target_triangulation(self, internals, target): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L6433)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L6433?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the subset of the current triangulation needed to support a target coordinate.
  - `internals`: `Any`
    > Available internal-coordinate specifications or their numerical values.
  - `target`: `Any`
    > Target coordinate whose supporting records are requested.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.enumerate_matching_dihedrons" class="docs-object-method">&nbsp;</a> 
```python
enumerate_matching_dihedrons(self, target_coord): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L6447)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L6447?message=Update%20Docs)]
</div>
**LLM Docstring**

Yield dihedron records and permutations that contain the target coordinate’s atoms in a usable arrangement.
  - `target_coord`: `Any`
    > Coordinate for which matching dihedrons are sought.
  - `:returns`: `Iterator`
    > An iterator yielding the candidates described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.find_conversions" class="docs-object-method">&nbsp;</a> 
```python
find_conversions(self, target_internals, unconvertable_atoms=None, allow_recursive_completions=False, allow_ambiguous_completions=False, find_unreachable=True, verbose=False, create_single=False, missing_val=None, depth=0, max_depth=5, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L6566)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L6566?message=Update%20Docs)]
</div>
**LLM Docstring**

Find or construct conversions from the graph’s current coordinates to one or more target coordinates, reusing cached direct, triangle, dihedron, paired-dihedron, and completion conversions where possible.
  - `target_internals`: `Any`
    > Coordinates for which conversions are requested from the mutable graph.
  - `unconvertable_atoms`: `Any`
    > Atoms that may not participate in inferred or completed conversion paths.
  - `allow_recursive_completions`: `Any`
    > Whether completing one coordinate may recursively request additional intermediate completions.
  - `allow_ambiguous_completions`: `Any`
    > Whether a missing intermediate may be accepted when more than one completion path exists.
  - `find_unreachable`: `Any`
    > Whether the search also identifies targets that cannot be reached from current coordinates.
  - `verbose`: `Any`
    > Whether diagnostic information is emitted during the search.
  - `create_single`: `Any`
    > Whether a single requested target is returned as one callable instead of a list.
  - `missing_val`: `Any`
    > Value to return for a missing coordinate, or `"raise"` to raise.
  - `depth`: `Any`
    > Current recursive search depth.
  - `max_depth`: `Any`
    > Maximum recursive completion depth before the target is declared unreachable.
  - `etc`: `Any`
    > Additional conversion-search options forwarded to nested searches.
  - `:returns`: `Any`
    > The value or updated object described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.get_bond_graph" class="docs-object-method">&nbsp;</a> 
```python
get_bond_graph(self, dist_set=None, return_conversions=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L6817)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L6817?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the bond graph implied by the graph’s current coordinates and triangulation, optionally rebuilding it or including metadata.
  - `dist_set`: `Any`
    > Optional known canonical distance set.
  - `return_conversions`: `Any`
    > Whether conversion objects and provenance are returned rather than only converted values.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.checkpoint" class="docs-object-method">&nbsp;</a> 
```python
checkpoint(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L6923)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L6923?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a context manager for making temporary changes to the internal-coordinate graph.
  - `:returns`: `Any`
    > The value or updated object described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.add_internals" class="docs-object-method">&nbsp;</a> 
```python
add_internals(self, internals): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L6934)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L6934?message=Update%20Docs)]
</div>
**LLM Docstring**

Add coordinates to the graph, update triangulation and bond data, and refresh conversion caches for targets that become directly or indirectly available.
  - `internals`: `Any`
    > Available internal-coordinate specifications or their numerical values.
  - `:returns`: `Any`
    > The value or updated object described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateGraph.remove_internals" class="docs-object-method">&nbsp;</a> 
```python
remove_internals(self, internals): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L7018)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateGraph.py#L7018?message=Update%20Docs)]
</div>
**LLM Docstring**

A non-implemented stub for future development.

Remove coordinates from the graph, rebuild affected triangulation data, and invalidate cached conversions that depended on the removed coordinates.
  - `internals`: `Any`
    > Available internal-coordinate specifications or their numerical values.
  - `:returns`: `Any`
    > The value or updated object described above.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals.py#L6396?message=Update%20Docs)   
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