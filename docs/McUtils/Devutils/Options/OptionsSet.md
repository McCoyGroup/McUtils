## <a id="McUtils.Devutils.Options.OptionsSet">OptionsSet</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options.py#L14?message=Update%20Docs)]
</div>

Provides a helpful manager for those cases where
there are way too many options and we need to filter
them across subclasses and things







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Devutils.Options.OptionsSet.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *d, **ops): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options.py#L21)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options.py#L21?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap a set of options (from a dict and/or keyword arguments) for filtering and
binding.
  - `d`: `Any`
    > an optional initial options dict (positional)
  - `ops`: `Any`
    > additional options as keyword arguments


<a id="McUtils.Devutils.Options.OptionsSet.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L39)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L39?message=Update%20Docs)]
</div>
**LLM Docstring**

Get an option by key.
  - `item`: `Any`
    > the option name
  - `:returns`: `_`
    > the option value


<a id="McUtils.Devutils.Options.OptionsSet.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L49)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L49?message=Update%20Docs)]
</div>
**LLM Docstring**

Set an option by key.
  - `key`: `Any`
    > the option name
  - `value`: `Any`
    > the option value


<a id="McUtils.Devutils.Options.OptionsSet.__delitem__" class="docs-object-method">&nbsp;</a> 
```python
__delitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L59)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L59?message=Update%20Docs)]
</div>
**LLM Docstring**

Delete an option by key.
  - `item`: `Any`
    > the option name


<a id="McUtils.Devutils.Options.OptionsSet.__getattr__" class="docs-object-method">&nbsp;</a> 
```python
__getattr__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L68)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L68?message=Update%20Docs)]
</div>
**LLM Docstring**

Get an option via attribute access.
  - `item`: `Any`
    > the option name
  - `:returns`: `_`
    > the option value


<a id="McUtils.Devutils.Options.OptionsSet.__setattr__" class="docs-object-method">&nbsp;</a> 
```python
__setattr__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L78)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L78?message=Update%20Docs)]
</div>
**LLM Docstring**

Set an option via attribute access (the `ops` dict itself is set normally).
  - `key`: `Any`
    > the option name (or `'ops'`)
  - `value`: `Any`
    > the value


<a id="McUtils.Devutils.Options.OptionsSet.__delattr__" class="docs-object-method">&nbsp;</a> 
```python
__delattr__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L91)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L91?message=Update%20Docs)]
</div>
**LLM Docstring**

Delete an option via attribute access.
  - `item`: `Any`
    > the option name


<a id="McUtils.Devutils.Options.OptionsSet.__hasattr__" class="docs-object-method">&nbsp;</a> 
```python
__hasattr__(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L100)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L100?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether an option exists.
  - `key`: `Any`
    > the option name
  - `:returns`: `bool`
    > whether the option is present


<a id="McUtils.Devutils.Options.OptionsSet.update" class="docs-object-method">&nbsp;</a> 
```python
update(self, **ops): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L111)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L111?message=Update%20Docs)]
</div>
**LLM Docstring**

Update the options from keyword arguments.
  - `ops`: `Any`
    > the options to merge in


<a id="McUtils.Devutils.Options.OptionsSet.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L121)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L121?message=Update%20Docs)]
</div>
**LLM Docstring**

The option names.
  - `:returns`: `_`
    > the option keys


<a id="McUtils.Devutils.Options.OptionsSet.items" class="docs-object-method">&nbsp;</a> 
```python
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L130?message=Update%20Docs)]
</div>
**LLM Docstring**

The option `(name, value)` pairs.
  - `:returns`: `_`
    > the option items


<a id="McUtils.Devutils.Options.OptionsSet.save" class="docs-object-method">&nbsp;</a> 
```python
save(self, file, mode=None, attribute=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L140)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L140?message=Update%20Docs)]
</div>
**LLM Docstring**

Serialize the options to a file.
  - `file`: `Any`
    > the destination file
  - `mode`: `Any`
    > the serialization mode
  - `attribute`: `Any`
    > an attribute to serialize under


<a id="McUtils.Devutils.Options.OptionsSet.load" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load(cls, file, mode=None, attribute=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L151)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L151?message=Update%20Docs)]
</div>
**LLM Docstring**

Load options from a file into a new `OptionsSet`.
  - `file`: `Any`
    > the source file
  - `mode`: `Any`
    > the serialization mode
  - `attribute`: `Any`
    > the attribute to read from
  - `:returns`: `OptionsSet`
    > the loaded options


<a id="McUtils.Devutils.Options.OptionsSet.extract_kwarg_keys" class="docs-object-method">&nbsp;</a> 
```python
extract_kwarg_keys(self, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L166)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L166?message=Update%20Docs)]
</div>
**LLM Docstring**

Determine the keyword-argument names of a callable from its signature (the
trailing arguments that have defaults).
  - `obj`: `Any`
    > the callable
  - `:returns`: `tuple | None`
    > the keyword-argument names, or `None`


<a id="McUtils.Devutils.Options.OptionsSet.get_props" class="docs-object-method">&nbsp;</a> 
```python
get_props(self, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L182)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L182?message=Update%20Docs)]
</div>
**LLM Docstring**

Determine the set of option names an object accepts, from its `__props__`,
its annotations, or (failing those) its keyword-argument signature; unions the
results across a list/tuple of objects.
  - `obj`: `Any`
    > the object (or list of objects) to inspect
  - `:returns`: `tuple`
    > the accepted option names


<a id="McUtils.Devutils.Options.OptionsSet.bind" class="docs-object-method">&nbsp;</a> 
```python
bind(self, obj, props=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L220)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L220?message=Update%20Docs)]
</div>
**LLM Docstring**

Set each option that `obj` accepts as an attribute on `obj`.
  - `obj`: `Any`
    > the object to bind onto
  - `props`: `Sequence[str] | None`
    > the option names to consider (inferred if omitted)


<a id="McUtils.Devutils.Options.OptionsSet.filter" class="docs-object-method">&nbsp;</a> 
```python
filter(self, obj, props=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L232)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L232?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the subset of options whose names are accepted by `obj`.
  - `obj`: `Any`
    > the object whose props to filter against
  - `props`: `Sequence[str] | None`
    > the option names (inferred if omitted)
  - `:returns`: `dict`
    > the matching options


<a id="McUtils.Devutils.Options.OptionsSet.exclude" class="docs-object-method">&nbsp;</a> 
```python
exclude(self, obj, props=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L248)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L248?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the subset of options whose names are *not* accepted by `obj`.
  - `obj`: `Any`
    > the object whose props to filter against
  - `props`: `Sequence[str] | None`
    > the option names (inferred if omitted)
  - `:returns`: `dict`
    > the non-matching options


<a id="McUtils.Devutils.Options.OptionsSet.split" class="docs-object-method">&nbsp;</a> 
```python
split(self, obj, props=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsSet.py#L264)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsSet.py#L264?message=Update%20Docs)]
</div>
**LLM Docstring**

Split the options into the `(accepted, excluded)` subsets for `obj`.
  - `obj`: `Any`
    > the object whose props to split against
  - `props`: `Sequence[str] | None`
    > the option names (inferred if omitted)
  - `:returns`: `tuple`
    > `(filtered, excluded)`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/Options/OptionsSet.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/Options/OptionsSet.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/Options/OptionsSet.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/Options/OptionsSet.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options.py#L14?message=Update%20Docs)   
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