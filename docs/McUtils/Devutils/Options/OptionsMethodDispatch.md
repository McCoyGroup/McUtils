## <a id="McUtils.Devutils.Options.OptionsMethodDispatch">OptionsMethodDispatch</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options.py#L281)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options.py#L281?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Devutils.Options.OptionsMethodDispatch.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, methods_table: 'dict|Callable[[], dict]', attributes_map=None, default_method=None, methods_enum=None, case_insensitive=True, allow_custom_methods=True, ignore_bad_enum_keys=False, method_key='method'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options.py#L282)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options.py#L282?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a dispatcher that resolves a method specification into a `(method,
options)` pair against a table of named methods.
  - `methods_table`: `dict | Callable`
    > the name-to-method mapping, or a callable producing one
  - `attributes_map`: `dict | None`
    > maps attribute-name sets to a method (for keyword-based dispatch)
  - `default_method`: `Any`
    > the fallback method name
  - `methods_enum`: `Any`
    > an enum used to canonicalize method names
  - `case_insensitive`: `bool`
    > match method names case-insensitively
  - `allow_custom_methods`: `bool`
    > allow passing a callable directly as the method
  - `ignore_bad_enum_keys`: `bool`
    > swallow enum-lookup failures
  - `method_key`: `str`
    > the dict key holding the method name


<a id="McUtils.Devutils.Options.OptionsMethodDispatch.register" class="docs-object-method">&nbsp;</a> 
```python
register(self, method_name, method, base_attributes=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsMethodDispatch.py#L326)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsMethodDispatch.py#L326?message=Update%20Docs)]
</div>
**LLM Docstring**

Register a method under a name, optionally mapping a set of base attributes to
it for keyword-based dispatch.
  - `method_name`: `Any`
    > the method name
  - `method`: `Any`
    > the method (callable)
  - `base_attributes`: `str | Sequence[str] | None`
    > attribute name(s) that select this method


<a id="McUtils.Devutils.Options.OptionsMethodDispatch.load_methods_table" class="docs-object-method">&nbsp;</a> 
```python
load_methods_table(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsMethodDispatch.py#L346)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsMethodDispatch.py#L346?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the methods table, merging any generator-produced entries with the
explicitly registered ones.
  - `:returns`: `dict`
    > the methods table


<a id="McUtils.Devutils.Options.OptionsMethodDispatch.prep_method_spec" class="docs-object-method">&nbsp;</a> 
```python
prep_method_spec(self, method_spec): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsMethodDispatch.py#L385)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsMethodDispatch.py#L385?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize a method specification into a `(method, options)` pair, accepting
strings, enum members, dicts (with a method key), callables, and
`(method, opts)` tuples.
  - `method_spec`: `Any`
    > the method specification
  - `:returns`: `tuple`
    > `(method, options)`


<a id="McUtils.Devutils.Options.OptionsMethodDispatch.resolve" class="docs-object-method">&nbsp;</a> 
```python
resolve(self, method_spec): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Options/OptionsMethodDispatch.py#L415)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options/OptionsMethodDispatch.py#L415?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a method specification into the actual `(method, options)` to use,
looking the method up in the table (canonicalizing via the enum and applying
case-insensitive and default fallbacks as configured).
  - `method_spec`: `Any`
    > the method specification
  - `:returns`: `tuple`
    > `(resolved_method, options)`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/Options/OptionsMethodDispatch.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/Options/OptionsMethodDispatch.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/Options/OptionsMethodDispatch.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/Options/OptionsMethodDispatch.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Options.py#L281?message=Update%20Docs)   
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