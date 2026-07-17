## <a id="McUtils.Devutils.Schema.Schema">Schema</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Schema.py#L391)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Schema.py#L391?message=Update%20Docs)]
</div>

An object that represents a schema that can be used to test
if an object matches that schema or not







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
type_validator: TypeValidator
value_validator: ValueValidator
json_schema_version: str
```
<a id="McUtils.Devutils.Schema.Schema.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, schema, optional_schema=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Schema.py#L399)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Schema.py#L399?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a schema object from a schema specification (and optional additional
optional-key schema).
  - `schema`: `Any`
    > the schema specification
  - `optional_schema`: `Any`
    > extra, non-required properties


<a id="McUtils.Devutils.Schema.Schema.required_keys" class="docs-object-method">&nbsp;</a> 
```python
@property
required_keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Schema/Schema.py#L412)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Schema/Schema.py#L412?message=Update%20Docs)]
</div>
**LLM Docstring**

The set of property keys the schema requires (computed lazily).
  - `:returns`: `set`
    > the required keys


<a id="McUtils.Devutils.Schema.Schema.is_json_schema" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_json_schema(self, schema): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L429)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L429?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether a schema dict is already a JSON schema (has a `$schema` key).
  - `schema`: `Any`
    > the schema dict
  - `:returns`: `bool`
    > whether it's a JSON schema


<a id="McUtils.Devutils.Schema.Schema.canonicalize_schema" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_schema(cls, schema, optional_schema=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L513)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L513?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize any accepted schema form into a JSON schema with validator objects,
folding in the required and optional properties.
  - `schema`: `Any`
    > the schema specification
  - `optional_schema`: `Any`
    > extra optional properties
  - `:returns`: `dict | None`
    > the canonicalized schema (or `None`)


<a id="McUtils.Devutils.Schema.Schema.validate" class="docs-object-method">&nbsp;</a> 
```python
validate(self, obj, throw=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Schema/Schema.py#L643)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Schema/Schema.py#L643?message=Update%20Docs)]
</div>
Validates that `obj` matches the provided schema
and throws an error if not
  - `obj`: `Any`
    > 
  - `throw`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Devutils.Schema.Schema.to_dict" class="docs-object-method">&nbsp;</a> 
```python
to_dict(self, obj, throw=True, ignore_invalid=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Schema/Schema.py#L662)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Schema/Schema.py#L662?message=Update%20Docs)]
</div>
Converts `obj` into a plain `dict` representation
  - `obj`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Devutils.Schema.Schema.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Schema/Schema.py#L686)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Schema/Schema.py#L686?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation showing the canonicalized schema.
  - `:returns`: `str`
    > the representation
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/Schema/Schema.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/Schema/Schema.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/Schema/Schema.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/Schema/Schema.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Schema.py#L391?message=Update%20Docs)   
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