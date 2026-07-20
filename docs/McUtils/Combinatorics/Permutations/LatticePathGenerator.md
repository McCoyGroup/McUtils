## <a id="McUtils.Combinatorics.Permutations.LatticePathGenerator">LatticePathGenerator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L4455)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L4455?message=Update%20Docs)]
</div>

An object to take direct products of lattice paths and
filter them







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Combinatorics.Permutations.LatticePathGenerator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *steps, max_len=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations.py#L4461)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L4461?message=Update%20Docs)]
</div>

  - `steps`: `Iterable[Iterable[int]]`
    > the steps to take a direct product of


<a id="McUtils.Combinatorics.Permutations.LatticePathGenerator.subtrees" class="docs-object-method">&nbsp;</a> 
```python
@property
subtrees(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4481)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4481?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-depth lattice-path subtrees (position-tracking), generated lazily.
  - `:returns`: `_`
    > the subtrees


<a id="McUtils.Combinatorics.Permutations.LatticePathGenerator.tree" class="docs-object-method">&nbsp;</a> 
```python
@property
tree(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4494)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4494?message=Update%20Docs)]
</div>
**LLM Docstring**

The final (full-depth) lattice-path tree with positions, generated lazily.
  - `:returns`: `_`
    > the tree


<a id="McUtils.Combinatorics.Permutations.LatticePathGenerator.subrules" class="docs-object-method">&nbsp;</a> 
```python
@property
subrules(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4507)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4507?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-depth lattice-path rule trees (without position tracking), generated
lazily.
  - `:returns`: `_`
    > the rule subtrees


<a id="McUtils.Combinatorics.Permutations.LatticePathGenerator.rules" class="docs-object-method">&nbsp;</a> 
```python
@property
rules(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4521)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4521?message=Update%20Docs)]
</div>
**LLM Docstring**

The final (full-depth) lattice-path rule tree, generated lazily.
  - `:returns`: `_`
    > the rule tree


<a id="McUtils.Combinatorics.Permutations.LatticePathGenerator.generate_tree" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
generate_tree(self, rules, max_len=None, track_positions=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L4534)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L4534?message=Update%20Docs)]
</div>
We take the combo of the specified rules, where we take successive products of 1D rules with the
current set of rules following the pattern that
1. a 1D change can apply to any index in an existing rule
2. a 1D change can be appended to an existing rule

We ensure at each step that the rules remain sorted & duplicates are removed so as to keep the rule sets compact.
This is done in simple python loops, because doing it with arrayops seemed harder & not worth it for a relatively cheap operation.
  - `rules`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.LatticePathGenerator.find_paths" class="docs-object-method">&nbsp;</a> 
```python
find_paths(self, end_spots): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4650)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4650?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the starting steps of every lattice path that reaches one of the given end
positions.
  - `end_spots`: `Any`
    > the target end position(s)
  - `:returns`: `list`
    > the qualifying starting steps


<a id="McUtils.Combinatorics.Permutations.LatticePathGenerator.get_path" class="docs-object-method">&nbsp;</a> 
```python
get_path(self, path): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4671)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4671?message=Update%20Docs)]
</div>
Pulls the places one can end up after applying the path
  - `other`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Combinatorics.Permutations.LatticePathGenerator.find_intersections" class="docs-object-method">&nbsp;</a> 
```python
find_intersections(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4687)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations/LatticePathGenerator.py#L4687?message=Update%20Docs)]
</div>
Finds the paths that will make self intersect with other
  - `other`: `LatticePathGenerator`
    > 
  - `:returns`: `_`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Combinatorics/Permutations/LatticePathGenerator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Combinatorics/Permutations/LatticePathGenerator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Combinatorics/Permutations/LatticePathGenerator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Combinatorics/Permutations/LatticePathGenerator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Combinatorics/Permutations.py#L4455?message=Update%20Docs)   
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