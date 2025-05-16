## <a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem">CoordinateSystem</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem.py#L19?message=Update%20Docs)]
</div>

A representation of a coordinate system. It doesn't do much on its own but it *does* provide a way
to unify internal, cartesian, derived type coordinates







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
return_derivs_key: str
deriv_key: str
```
<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name=None, basis=None, matrix=None, inverse=None, dimension=None, origin=None, coordinate_shape=None, jacobian_prep=None, converter_options=None, **extra): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem.py#L24)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem.py#L24?message=Update%20Docs)]
</div>
Sets up the CoordinateSystem object
  - `name`: `str`
    > a name to give to the coordinate system
  - `basis`: `Any`
    > a basis for the coordinate system
  - `matrix`: `np.ndarray | None`
    > an expansion coefficient matrix for the set of coordinates in its basis
  - `dimension`: `Iterable[None | int]`
    > the dimension of a single configuration in the coordinate system (for validation)
  - `jacobian_prep`: `function | None`
    > a function for preparing coordinates to be used in computing the Jacobian
  - `coordinate_shape`: `iterable[int]`
    > the actual shape of a single coordinate in the coordinate system


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, coords, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L79)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L79?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.pre_convert" class="docs-object-method">&nbsp;</a> 
```python
pre_convert(self, system): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L86)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L86?message=Update%20Docs)]
</div>
A hook to allow for handlign details before converting
  - `system`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.basis" class="docs-object-method">&nbsp;</a> 
```python
@property
basis(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L106)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L106?message=Update%20Docs)]
</div>

  - `:returns`: `CoordinateSystem`
    > T
h
e
 
b
a
s
i
s
 
f
o
r
 
t
h
e
 
r
e
p
r
e
s
e
n
t
a
t
i
o
n
 
o
f
 
`
m
a
t
r
i
x
`


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.origin" class="docs-object-method">&nbsp;</a> 
```python
@property
origin(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L113)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L113?message=Update%20Docs)]
</div>

  - `:returns`: `np.ndarray`
    > T
h
e
 
o
r
i
g
i
n
 
f
o
r
 
t
h
e
 
e
x
p
a
n
s
i
o
n
 
d
e
f
i
n
e
d
 
b
y
 
`
m
a
t
r
i
x
`


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.matrix" class="docs-object-method">&nbsp;</a> 
```python
@property
matrix(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L124)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L124?message=Update%20Docs)]
</div>
The matrix representation in the `CoordinateSystem.basis`
`None` is shorthand for the identity matrix
  - `:returns`: `np.ndarray`
    > m
a
t


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.inverse" class="docs-object-method">&nbsp;</a> 
```python
@property
inverse(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L137)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L137?message=Update%20Docs)]
</div>
The inverse of the representation in the `basis`.
`None` is shorthand for the inverse or pseudoinverse of `matrix`.
  - `:returns`: `np.ndarray`
    > i
n
v


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.dimension" class="docs-object-method">&nbsp;</a> 
```python
@property
dimension(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L153)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L153?message=Update%20Docs)]
</div>
The dimension of the coordinate system.
`None` means unspecified dimension
  - `:returns`: `int or None`
    > d
i
m


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.converter" class="docs-object-method">&nbsp;</a> 
```python
converter(self, system): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L164)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L164?message=Update%20Docs)]
</div>
Gets the converter from the current system to a new system
  - `system`: `CoordinateSystem`
    > the target CoordinateSystem
  - `:returns`: `CoordinateSystemConverter`
    > c
o
n
v
e
r
t
e
r
 
o
b
j
e
c
t


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.convert_coords" class="docs-object-method">&nbsp;</a> 
```python
convert_coords(self, coords, system, converter=None, apply_pre_converter=False, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L230)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L230?message=Update%20Docs)]
</div>
Converts coordiantes from the current coordinate system to _system_
  - `coords`: `CoordinateSet`
    > 
  - `system`: `CoordinateSystem`
    > 
  - `kw`: `Any`
    > options to be passed through to the converter object
  - `:returns`: `tuple(np.ndarray, dict)`
    > t
h
e
 
c
o
n
v
e
r
t
e
d
 
c
o
o
r
d
i
a
n
t
e
s


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.rescale" class="docs-object-method">&nbsp;</a> 
```python
rescale(self, scaling, in_place=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L297)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L297?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.rotate" class="docs-object-method">&nbsp;</a> 
```python
rotate(self, rot, in_place=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L309)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L309?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.displacement" class="docs-object-method">&nbsp;</a> 
```python
displacement(self, amts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L323)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L323?message=Update%20Docs)]
</div>
Generates a displacement or matrix of displacements based on the vector or matrix amts
The relevance of this method has become somewhat unclear...
  - `amts`: `np.ndarray`
    > 
  - `:returns`: `np.ndarray`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.derivatives" class="docs-object-method">&nbsp;</a> 
```python
derivatives(self, coords, function, order=1, coordinates=None, result_shape=None, **finite_difference_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L345)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L345?message=Update%20Docs)]
</div>
Computes derivatives for an arbitrary function with respect to this coordinate system.
Basically a more flexible version of `jacobian`.
  - `function`: `Any`
    > 
  - `order`: `Any`
    > 
  - `coordinates`: `Any`
    > 
  - `finite_difference_options`: `Any`
    > 
  - `:returns`: `np.ndarray`
    > d
e
r
i
v
a
t
i
v
e
 
t
e
n
s
o
r


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.jacobian" class="docs-object-method">&nbsp;</a> 
```python
jacobian(self, coords, system, order=1, coordinates=None, converter_options=None, all_numerical=False, analytic_deriv_order=None, **finite_difference_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L459)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L459?message=Update%20Docs)]
</div>
Computes the Jacobian between the current coordinate system and a target coordinate system
  - `system`: `CoordinateSystem`
    > the target CoordinateSystem
  - `order`: `int | Iterable[int]`
    > the order of the Jacobian to compute, 1 for a standard, 2 for the Hessian, etc.
  - `coordinates`: `None | iterable[iterable[int] | None`
    > a spec of which coordinates to generate derivatives for (None means all)
  - `mesh_spacing`: `float | np.ndarray`
    > the spacing to use when displacing
  - `prep`: `None | function`
    > a function for pre-validating the generated coordinate values and grids
  - `fd_options`: `Any`
    > options to be passed straight through to FiniteDifferenceFunction
  - `:returns`: `np.ndarray`
    > d
e
r
i
v
a
t
i
v
e
 
t
e
n
s
o
r


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L616)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L616?message=Update%20Docs)]
</div>
Provides a clean representation of a `CoordinateSystem` for printing
  - `:returns`: `str`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.is_compatible" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_compatible(cls, self, system): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L623)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L623?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystem.CoordinateSystem.has_conversion" class="docs-object-method">&nbsp;</a> 
```python
has_conversion(self, system): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L631)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.py#L631?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem/CoordinateSystem.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystem.py#L19?message=Update%20Docs)   
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