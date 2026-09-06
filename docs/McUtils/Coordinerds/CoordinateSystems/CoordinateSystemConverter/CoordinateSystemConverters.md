## <a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters">CoordinateSystemConverters</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L167)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L167?message=Update%20Docs)]
</div>

A coordinate converter class. It's a singleton so can't be instantiated.

Registry keys are, by default, the system objects themselves -- cheap identity-based
hashing, exactly like the original implementation, with no string work at all. That's fine
for the overwhelming majority of registrations (typically short-lived, per-molecule
instances that never need to be looked up across an `importlib.reload` boundary in
practice, since they get rebuilt from scratch whenever the thing that reload affected --
e.g. a molecule -- gets rebuilt too).

Only systems explicitly marked *final* -- via an `is_final_coordinate_system` attribute, or
by having a `.name` in `cls.final_system_names` -- get resolved to a stable string key
instead. Those are the small set of canonical, singleton-ish types (`CartesianCoordinates3D`,
`ZMatrixCoordinateSystem`, etc.) that are actually defined in code subject to reload, and are
therefore the only ones where object identity is untrustworthy across a reload. Confining the
string resolution (and the "alias across compatible systems" registration pass, which is the
expensive part) to just those systems keeps registration/deregistration/lookup for everything
else at the original O(1)-ish cost.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
converters: OrderedDict
converter_graph: NoneType
converters_dir: str
converters_package: str
converter_type: CoordinateSystemConverter
default_anonymous_name_format: str
final_system_names: frozenset
```
<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L214)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L214?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters.get_coordinates" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_coordinates(self, coordinate_set): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L217)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L217?message=Update%20Docs)]
</div>
Extracts coordinates from a coordinate_set


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters.load_converter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_converter(cls, converter): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L338)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L338?message=Update%20Docs)]
</div>


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters.get_converter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_converter(cls, system1, system2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L385)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L385?message=Update%20Docs)]
</div>
Gets the appropriate converter for two CoordinateSystem objects
  - `system1`: `CoordinateSystem`
    > 
  - `system2`: `CoordinateSystem`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters.register_converter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
register_converter(cls, system1, system2, converter, check=True, name_format=None, final=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L448)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L448?message=Update%20Docs)]
</div>
Registers a converter between two coordinate systems
  - `system1`: `CoordinateSystem`
    > 
  - `system2`: `CoordinateSystem`
    > 
  - `final`: `Any`
    > force the "final" (string-keyed) treatment on or off for this
    registration, instead of relying on auto-detection via `_is_final`. Pass a single
    bool for both systems, or a `(final1, final2)` pair to set them independently.
  - `:returns`: `_`
    >


<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverters.deregister_converter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
deregister_converter(cls, system1, system2, converter, check=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L473)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L473?message=Update%20Docs)]
</div>
Registers a converter between two coordinate systems
  - `system1`: `CoordinateSystem`
    > 
  - `system2`: `CoordinateSystem`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverters.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverters.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverters.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverters.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py#L167?message=Update%20Docs)   
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