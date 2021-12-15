## <a id="McUtils.Extensions.ArgumentSignature.Argument">Argument</a>
Defines a single Argument for a C-level caller to support default values, etc.
We use a two-pronged approach where we have a set of ArgumentType serializers/deserializers

### Properties and Methods
```python
arg_types: list
```
<a id="McUtils.Extensions.ArgumentSignature.Argument.__init__" class="docs-object-method">&nbsp;</a>
```python
__init__(self, name, dtype, default=None): 
```

- `name`: `str`
    >the name of the argument
- `dtype`: `ArgumentType`
    >the type of the argument; at some point we'll support type inference...
- `default`: `Any`
    >the default value for the argument

<a id="McUtils.Extensions.ArgumentSignature.Argument.infer_type" class="docs-object-method">&nbsp;</a>
```python
infer_type(arg): 
```
Infers the type of an argument
- `arg`: `ArgumentType | str | type | ctypes type`
    >No description...
- `:returns`: `_`
    >No description...

<a id="McUtils.Extensions.ArgumentSignature.Argument.infer_array_type" class="docs-object-method">&nbsp;</a>
```python
infer_array_type(argstr): 
```

<a id="McUtils.Extensions.ArgumentSignature.Argument.inferred_type_string" class="docs-object-method">&nbsp;</a>
```python
inferred_type_string(arg): 
```
returns a type string for the inferred type

<a id="McUtils.Extensions.ArgumentSignature.Argument.cpp_signature" class="docs-object-method">&nbsp;</a>
```python
@property
cpp_signature(self): 
```

<a id="McUtils.Extensions.ArgumentSignature.Argument.__repr__" class="docs-object-method">&nbsp;</a>
```python
__repr__(self): 
```





___

[Edit Examples](https://github.com/McCoyGroup/McUtils/edit/edit/ci/examples/ci/docs/McUtils/Extensions/ArgumentSignature/Argument.md) or 
[Create New Examples](https://github.com/McCoyGroup/McUtils/new/edit/?filename=ci/examples/ci/docs/McUtils/Extensions/ArgumentSignature/Argument.md) <br/>
[Edit Template](https://github.com/McCoyGroup/McUtils/edit/edit/ci/docs/ci/docs/McUtils/Extensions/ArgumentSignature/Argument.md) or 
[Create New Template](https://github.com/McCoyGroup/McUtils/new/edit/?filename=ci/docs/templates/ci/docs/McUtils/Extensions/ArgumentSignature/Argument.md) <br/>
[Edit Docstrings](https://github.com/McCoyGroup/McUtils/edit/edit/McUtils/Extensions/ArgumentSignature.py?message=Update%20Docs)