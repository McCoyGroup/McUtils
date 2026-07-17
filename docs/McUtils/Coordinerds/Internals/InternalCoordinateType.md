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
**LLM Docstring**

Register an `InternalCoordinateType` subclass under a dispatch name. Called with a string alone, this returns a decorator that assigns that name to the decorated class; otherwise it invalidates the cached dispatcher, stores the class in `registry`, and returns the class unchanged.
  - `type`: `Any`
    > A coordinate class, or a registration name when using decorator form.
  - `typename`: `Any`
    > The registry key to assign to the coordinate class.
  - `:returns`: `type | Callable[[type], type]`
    > The registered class, or a decorator awaiting the class.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_dispatch" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_dispatch(cls) -> 'dev.OptionsMethodDispatch': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L78)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L78?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the lazily constructed options dispatcher used to turn dictionaries containing a `type` key into registered coordinate classes and their constructor options.
  - `:returns`: `dev.OptionsMethodDispatch`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.resolve" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve(cls, input): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L100)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L100?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert either a typed option dictionary or a bare index sequence into an instantiated coordinate object. Dictionary inputs are dispatched by `type`; bare sequences are tested against each registered class with `could_be`, and an unmatched input raises `ValueError`.
  - `input`: `Any`
    > A typed option mapping or bare coordinate-index sequence.
  - `:returns`: `InternalCoordinateType`
    > An instantiated registered coordinate object.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.could_be" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
could_be(cls, input): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L127)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L127?message=Update%20Docs)]
</div>
**LLM Docstring**

Report whether an input can represent this coordinate type. The base implementation always returns `False` and is intended to be overridden.
  - `input`: `Any`
    > A typed option mapping or bare coordinate-index sequence.
  - `:returns`: `bool`
    > Whether the tested condition is satisfied.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.equivalent_to" class="docs-object-method">&nbsp;</a> 
```python
equivalent_to(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L141)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L141?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether two coordinates have the same concrete type and the same indices after each is put in canonical orientation.
  - `other`: `Any`
    > The coordinate to compare against.
  - `:returns`: `bool`
    > Whether the tested condition is satisfied.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.__eq__" class="docs-object-method">&nbsp;</a> 
```python
__eq__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L156?message=Update%20Docs)]
</div>
**LLM Docstring**

Compare coordinates using canonical coordinate equivalence rather than object identity.
  - `other`: `Any`
    > The coordinate to compare against.
  - `:returns`: `bool`
    > Whether the tested condition is satisfied.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.canonicalize" class="docs-object-method">&nbsp;</a> 
```python
canonicalize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L169?message=Update%20Docs)]
</div>
**LLM Docstring**

Return an equivalent coordinate in the canonical index orientation defined by the concrete coordinate type.
  - `:returns`: `Any`
    > The value or updated object described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_indices" class="docs-object-method">&nbsp;</a> 
```python
get_indices(self) -> 'Tuple[int, ...]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L181)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L181?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the atom indices that define this internal coordinate, in the type-specific ordering.
  - `:returns`: `Tuple[int, ...]`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.__hash__" class="docs-object-method">&nbsp;</a> 
```python
__hash__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L193)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L193?message=Update%20Docs)]
</div>
**LLM Docstring**

Hash the coordinate from its concrete class and stored index tuple so it can be used as a dictionary key or set member.
  - `:returns`: `int`
    > The coordinate hash value.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.reindex" class="docs-object-method">&nbsp;</a> 
```python
reindex(self, reindexing): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L203)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L203?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the same coordinate expressed under a supplied old-index to new-index mapping.
  - `reindexing`: `Any`
    > A mapping from existing atom indices to replacement indices.
  - `:returns`: `Any`
    > The value or updated object described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_carried_atoms" class="docs-object-method">&nbsp;</a> 
```python
get_carried_atoms(self, context: 'InternalSpec'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L217)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L217?message=Update%20Docs)]
</div>
**LLM Docstring**

Determine the atom groups displaced on the two sides of this coordinate when it is varied in an `InternalSpec`.
  - `context`: `InternalSpec`
    > The surrounding coordinate specification used to infer connectivity and moved fragments.
  - `:returns`: `Any`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_constraint_rads" class="docs-object-method">&nbsp;</a> 
```python
get_constraint_rads(self) -> 'list[Distance | Angle | Dihedral]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L231)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L231?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the primitive distance, angle, or dihedral coordinates that must remain available to constrain this coordinate.
  - `:returns`: `list[Distance | Angle | Dihedral]`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_expansion" class="docs-object-method">&nbsp;</a> 
```python
get_expansion(self, coords, order=None, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L243)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L243?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate Cartesian derivatives of this internal coordinate through the requested order.
  - `coords`: `Any`
    > Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
  - `order`: `Any`
    > Highest derivative order to compute.
  - `opts`: `Any`
    > Additional options forwarded to the numerical conversion routine.
  - `:returns`: `List[np.ndarray]`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.


<a id="McUtils.Coordinerds.Internals.InternalCoordinateType.get_inverse_expansion" class="docs-object-method">&nbsp;</a> 
```python
get_inverse_expansion(self, coords, order=None, moved_indices=None, **opts) -> 'List[np.ndarray]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L261)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/Internals/InternalCoordinateType.py#L261?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate derivatives of the Cartesian displacement generated by changing this internal coordinate, optionally restricted to selected moved atoms.
  - `coords`: `Any`
    > Cartesian coordinates, internal-coordinate values, or coordinate specifications as required by the operation.
  - `order`: `Any`
    > Highest derivative order to compute.
  - `moved_indices`: `Any`
    > Explicit pair of atom groups moved on the two sides of a coordinate.
  - `opts`: `Any`
    > Additional options forwarded to the numerical conversion routine.
  - `:returns`: `List[np.ndarray]`
    > The requested coordinate, graph, triangulation, derivative, or conversion data described above.
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