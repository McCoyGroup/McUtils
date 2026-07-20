## <a id="McUtils.Graphs.Trees.TreeWrapper">TreeWrapper</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees.py#L407)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees.py#L407?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Graphs.Trees.TreeWrapper.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, tree): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees.py#L408)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees.py#L408?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap a nested mapping or sequence with traversal and path-indexing conveniences.
  - `tree`: `object`
    > The nested container or adjacency structure to traverse.

  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.Graphs.Trees.TreeWrapper.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees/TreeWrapper.py#L422)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees/TreeWrapper.py#L422?message=Update%20Docs)]
</div>
**LLM Docstring**

Format the wrapped tree using `pprint.pformat`.
  - `:returns`: `str`
    > A concise string representation.


<a id="McUtils.Graphs.Trees.TreeWrapper.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees/TreeWrapper.py#L434)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees/TreeWrapper.py#L434?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the number of top-level entries in the wrapped tree.
  - `:returns`: `object`
    > The number of contained elements.


<a id="McUtils.Graphs.Trees.TreeWrapper.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees/TreeWrapper.py#L444)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees/TreeWrapper.py#L444?message=Update%20Docs)]
</div>
**LLM Docstring**

Iterate over the wrapped container.
  - `:returns`: `collections.abc.Iterator`
    > An iterator over contained elements.


<a id="McUtils.Graphs.Trees.TreeWrapper.condense_subtrees" class="docs-object-method">&nbsp;</a> 
```python
condense_subtrees(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees/TreeWrapper.py#L454)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees/TreeWrapper.py#L454?message=Update%20Docs)]
</div>
**LLM Docstring**

Merge a top-level sequence of mapping subtrees into one mapping when every element is dictionary-like.
  - `:returns`: `object`
    > `self` when condensation is not possible, otherwise a new wrapper around the merged mapping.


<a id="McUtils.Graphs.Trees.TreeWrapper.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees/TreeWrapper.py#L472)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees/TreeWrapper.py#L472?message=Update%20Docs)]
</div>
**LLM Docstring**

Return mapping keys when the wrapped tree is mapping-like; otherwise return `None`.
  - `:returns`: `object`
    > A mapping key view, or `None`.


<a id="McUtils.Graphs.Trees.TreeWrapper.values" class="docs-object-method">&nbsp;</a> 
```python
values(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees/TreeWrapper.py#L485)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees/TreeWrapper.py#L485?message=Update%20Docs)]
</div>
**LLM Docstring**

Return mapping values or the sequence itself for non-mapping trees.
  - `:returns`: `object`
    > A mapping value view or the wrapped sequence.


<a id="McUtils.Graphs.Trees.TreeWrapper.find_subtree" class="docs-object-method">&nbsp;</a> 
```python
find_subtree(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees/TreeWrapper.py#L498)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees/TreeWrapper.py#L498?message=Update%20Docs)]
</div>
**LLM Docstring**

Find the first direct subtree associated with one of the requested keys.
  - `key`: `object`
    > Index, path, or mapping key selecting an item.

  - `:returns`: `object`
    > The first matching direct subtree, or `None`.


<a id="McUtils.Graphs.Trees.TreeWrapper.get_tree_item" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_tree_item(cls, tree, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L521)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L521?message=Update%20Docs)]
</div>
**LLM Docstring**

Follow a path through nested mappings and sequences, translating integer positions into mapping-key order where needed.
  - `tree`: `object`
    > The nested container or adjacency structure to traverse.

  - `item`: `object`
    > Index, path, or item to retrieve.

  - `:returns`: `object`
    > The nested object reached by the path.


<a id="McUtils.Graphs.Trees.TreeWrapper.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees/TreeWrapper.py#L565)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees/TreeWrapper.py#L565?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a nested path through the wrapped tree.
  - `item`: `object`
    > Index, path, or item to retrieve.

  - `:returns`: `object`
    > The nested object selected by `item`.


<a id="McUtils.Graphs.Trees.TreeWrapper.bfs" class="docs-object-method">&nbsp;</a> 
```python
bfs(self, callback, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees/TreeWrapper.py#L578)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees/TreeWrapper.py#L578?message=Update%20Docs)]
</div>
**LLM Docstring**

Run `tree_traversal` in breadth-first order.
  - `callback`: `object`
    > Function called with traversal context for each visited node.

  - `opts`: `object`
    > Additional options forwarded to the delegated operation.

  - `:returns`: `object`
    > The first non-`None` callback result, or `None`.


<a id="McUtils.Graphs.Trees.TreeWrapper.dfs" class="docs-object-method">&nbsp;</a> 
```python
dfs(self, callback, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Graphs/Trees/TreeWrapper.py#L595)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees/TreeWrapper.py#L595?message=Update%20Docs)]
</div>
**LLM Docstring**

Run `tree_traversal` in depth-first order.
  - `callback`: `object`
    > Function called with traversal context for each visited node.

  - `opts`: `object`
    > Additional options forwarded to the delegated operation.

  - `:returns`: `object`
    > The first non-`None` callback result, or `None`.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Graphs/Trees/TreeWrapper.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Graphs/Trees/TreeWrapper.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Graphs/Trees/TreeWrapper.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Graphs/Trees/TreeWrapper.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Graphs/Trees.py#L407?message=Update%20Docs)   
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