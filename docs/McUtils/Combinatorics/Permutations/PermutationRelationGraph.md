## <a id="McUtils.Combinatorics.Permutations.PermutationRelationGraph">PermutationRelationGraph</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L4699)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L4699?message=Update%20Docs)]
</div>

Takes permutations and a set of relations and builds a graph from
them







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Combinatorics.Permutations.PermutationRelationGraph.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, relations): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L4705)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L4705?message=Update%20Docs)]
</div>

  - `relations`: `Any`
    > sets of rules connecting permutations


<a id="McUtils.Combinatorics.Permutations.PermutationRelationGraph.merge_groups" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
merge_groups(cls, groups): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4712)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4712?message=Update%20Docs)]
</div>
This really needs to be cleaned up...
  - `groups`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.PermutationRelationGraph.make_relation_graph" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
make_relation_graph(cls, relations): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4749)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4749?message=Update%20Docs)]
</div>

  - `relations`: `Iterable[Iterable[Iterable[int]]]`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.PermutationRelationGraph.apply_rels" class="docs-object-method">&nbsp;</a> 
```python
apply_rels(self, states, max_sum=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/PermutationRelationGraph.py#L4769)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/PermutationRelationGraph.py#L4769?message=Update%20Docs)]
</div>
For each state checks if it is divisible by one of the group rules and if so applies the
relevant transformations to it
  - `states`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.PermutationRelationGraph.build_state_graph" class="docs-object-method">&nbsp;</a> 
```python
build_state_graph(self, states, max_sum=None, extra_groups=None, max_iterations=10, raise_iteration_error=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/PermutationRelationGraph.py#L4817)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/PermutationRelationGraph.py#L4817?message=Update%20Docs)]
</div>

  - `states`: `Any`
    > 
  - `max_iterations`: `Any`
    > 
  - `raise_iteration_error`: `Any`
    > 
  - `:returns`: `Iterable[np.ndarray]`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Permutations/PermutationRelationGraph.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Permutations/PermutationRelationGraph.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Permutations/PermutationRelationGraph.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Permutations/PermutationRelationGraph.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L4699?message=Update%20Docs)   
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