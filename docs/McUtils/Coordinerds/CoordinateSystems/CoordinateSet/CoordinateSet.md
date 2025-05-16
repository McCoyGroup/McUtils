## <a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSet.CoordinateSet">CoordinateSet</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet.py#L20?message=Update%20Docs)]
</div>

A subclass of np.ndarray that lives in an explicit coordinate system and can convert between them







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSet.CoordinateSet.__new__" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
__new__(cls, coords, system=CoordinateSystem(Cartesian3D, dimension=(None, 3), matrix=None), converter_options=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L26)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L26?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSet.CoordinateSet.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, coords, system=CoordinateSystem(Cartesian3D, dimension=(None, 3), matrix=None), converter_options=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet.py#L32)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet.py#L32?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSet.CoordinateSet.__array_finalize__" class="docs-object-method">&nbsp;</a> 
```python
__array_finalize__(self, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L37)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L37?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSet.CoordinateSet.__str__" class="docs-object-method">&nbsp;</a> 
```python
__str__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L63)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L63?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSet.CoordinateSet.__eq__" class="docs-object-method">&nbsp;</a> 
```python
__eq__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L66)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L66?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSet.CoordinateSet.multiconfig" class="docs-object-method">&nbsp;</a> 
```python
@property
multiconfig(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L72)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L72?message=Update%20Docs)]
</div>
Determines whether self.coords represents multiple configurations of the coordinates
  - `:returns`: `_`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSet.CoordinateSet.transform" class="docs-object-method">&nbsp;</a> 
```python
transform(self, tf): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L81)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L81?message=Update%20Docs)]
</div>
Applies a transformation to the stored coordinates
  - `tf`: `Any`
    > the transformation function to apply to the system
  - `:returns`: `_`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSet.CoordinateSet.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, system, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L93)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L93?message=Update%20Docs)]
</div>
Converts across coordinate systems
  - `system`: `CoordinateSystem`
    > the target coordinate system
  - `:returns`: `CoordinateSet`
    > n
e
w
_
c
o
o
r
d
s


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSet.CoordinateSet.derivatives" class="docs-object-method">&nbsp;</a> 
```python
derivatives(self, function, order=1, coordinates=None, result_shape=None, **fd_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L113)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L113?message=Update%20Docs)]
</div>
Takes derivatives of `function` with respect to the current geometry
  - `function`: `Any`
    > 
  - `order`: `Any`
    > 
  - `coordinates`: `Any`
    > 
  - `fd_options`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSet.CoordinateSet.jacobian" class="docs-object-method">&nbsp;</a> 
```python
jacobian(self, system, order=1, coordinates=None, converter_options=None, all_numerical=False, analytic_deriv_order=None, **fd_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L137)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.py#L137?message=Update%20Docs)]
</div>
Delegates to the jacobian function of the current coordinate system.
  - `system`: `Any`
    > 
  - `order`: `Any`
    > 
  - `mesh_spacing`: `Any`
    > 
  - `prep`: `Any`
    > 
  - `coordinates`: `Any`
    > 
  - `fd_options`: `Any`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/CoordinateSystems/CoordinateSet/CoordinateSet.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSet.py#L20?message=Update%20Docs)   
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