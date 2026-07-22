## <a id="McUtils.Graphs.EdgeGraph.GraphSearcher">GraphSearcher</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph.py#L2633)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph.py#L2633?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Graphs.EdgeGraph.GraphSearcher.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, data=None, track_components=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph.py#L2635)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph.py#L2635?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize union-find parent, rank, and optional component-member tables.
  - `data`: `object`
    > Input data consumed by the operation.

  - `track_components`: `object`
    > Whether union-find member sets should be maintained.

  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.Graphs.EdgeGraph.GraphSearcher.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/GraphSearcher.py#L2655)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/GraphSearcher.py#L2655?message=Update%20Docs)]
</div>
**LLM Docstring**

Create an independent copy of the union-find state.
  - `:returns`: `object`
    > An independent `GraphSearcher`.


<a id="McUtils.Graphs.EdgeGraph.GraphSearcher.add" class="docs-object-method">&nbsp;</a> 
```python
add(self, node) -> 'None': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/GraphSearcher.py#L2675)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/GraphSearcher.py#L2675?message=Update%20Docs)]
</div>
**LLM Docstring**

Insert a node as a singleton component if needed and return its current root.
  - `node`: `object`
    > Node identifier.

  - `:returns`: `object`
    > The union-find root of the node.


<a id="McUtils.Graphs.EdgeGraph.GraphSearcher.find" class="docs-object-method">&nbsp;</a> 
```python
find(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/GraphSearcher.py#L2694)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/GraphSearcher.py#L2694?message=Update%20Docs)]
</div>
Find root with path-halving compression.


<a id="McUtils.Graphs.EdgeGraph.GraphSearcher.same_component" class="docs-object-method">&nbsp;</a> 
```python
same_component(self, u, v) -> 'bool': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/GraphSearcher.py#L2702)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/GraphSearcher.py#L2702?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether two nodes have the same union-find root.
  - `u`: `object`
    > First endpoint.

  - `v`: `object`
    > Second endpoint.

  - `:returns`: `object`
    > Whether both nodes have the same root.


<a id="McUtils.Graphs.EdgeGraph.GraphSearcher.union" class="docs-object-method">&nbsp;</a> 
```python
union(self, u, v): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/GraphSearcher.py#L2719)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/GraphSearcher.py#L2719?message=Update%20Docs)]
</div>
Merge the two components (union by rank).


<a id="McUtils.Graphs.EdgeGraph.GraphSearcher.component" class="docs-object-method">&nbsp;</a> 
```python
component(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/EdgeGraph/GraphSearcher.py#L2734)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph/GraphSearcher.py#L2734?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the tracked member set for a node’s component, or `None` when tracking is disabled.
  - `node`: `object`
    > Node identifier.

  - `:returns`: `object`
    > The tracked component member set, or `None`.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Graphs/EdgeGraph/GraphSearcher.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Graphs/EdgeGraph/GraphSearcher.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Graphs/EdgeGraph/GraphSearcher.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Graphs/EdgeGraph/GraphSearcher.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/EdgeGraph.py#L2633?message=Update%20Docs)   
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