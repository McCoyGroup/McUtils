## <a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverter">CoordinateSystemConverter</a>
A base class for type converters

### Properties and Methods
```python
converters: weakref
```
<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverter.types" class="docs-object-method">&nbsp;</a>
```python
@property
types(self): 
```
The types property of a converter returns the types the converter converts

<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverter.convert_many" class="docs-object-method">&nbsp;</a>
```python
convert_many(self, coords_list, **kwargs): 
```
Converts many coordinates. Used in cases where a CoordinateSet has higher dimension
        than its basis dimension. Should be overridden by a converted to provide efficient conversions
        where necessary.
- `coords_list`: `np.ndarray`
    >many sets of coords
- `kwargs`: `Any`
    >No description...

<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverter.convert" class="docs-object-method">&nbsp;</a>
```python
convert(self, coords, **kwargs): 
```
The main necessary implementation method for a converter class.
        Provides the actual function that converts the coords set
- `coords`: `np.ndarray`
    >No description...
- `kwargs`: `Any`
    >No description...

<a id="McUtils.Coordinerds.CoordinateSystems.CoordinateSystemConverter.CoordinateSystemConverter.register" class="docs-object-method">&nbsp;</a>
```python
register(self, where=None, check=True): 
```
Registers the CoordinateSystemConverter
- `:returns`: `_`
    >No description...





___

[Edit Examples](https://github.com/McCoyGroup/McUtils/edit/edit/ci/examples/ci/docs/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.md) or 
[Create New Examples](https://github.com/McCoyGroup/McUtils/new/edit/?filename=ci/examples/ci/docs/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.md) <br/>
[Edit Template](https://github.com/McCoyGroup/McUtils/edit/edit/ci/docs/ci/docs/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.md) or 
[Create New Template](https://github.com/McCoyGroup/McUtils/new/edit/?filename=ci/docs/templates/ci/docs/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter/CoordinateSystemConverter.md) <br/>
[Edit Docstrings](https://github.com/McCoyGroup/McUtils/edit/edit/McUtils/Coordinerds/CoordinateSystems/CoordinateSystemConverter.py?message=Update%20Docs)