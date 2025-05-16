## <a id="McUtils.Parsers.StructuredType.StructuredType">StructuredType</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/StructuredType.py#L11)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/StructuredType.py#L11?message=Update%20Docs)]
</div>

Represents a structured type with a defined calculus to simplify the construction of combined types when writing
parsers that take multi-typed data

Supports a compound StructuredType where the types are keyed







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Parsers.StructuredType.StructuredType.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, base_type, shape=None, is_alternative=False, is_optional=False, default_value=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/StructuredType/StructuredType.py#L18)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/StructuredType/StructuredType.py#L18?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredType.is_simple" class="docs-object-method">&nbsp;</a> 
```python
@property
is_simple(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/StructuredType/StructuredType.py#L57)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/StructuredType/StructuredType.py#L57?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredType.add_types" class="docs-object-method">&nbsp;</a> 
```python
add_types(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/StructuredType/StructuredType.py#L63)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/StructuredType/StructuredType.py#L63?message=Update%20Docs)]
</div>
Constructs a new type by treating the two objects as siblings, that is if they can be merged due to type and
shape similarity they will be, otherwise a non-nesting structure will be constructed from them

We'll also want a nesting version of this I'm guessing, which probably we hook into __call__
  - `other`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredType.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/StructuredType/StructuredType.py#L136)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/StructuredType/StructuredType.py#L136?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredType.compound_types" class="docs-object-method">&nbsp;</a> 
```python
compound_types(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/StructuredType/StructuredType.py#L139)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/StructuredType/StructuredType.py#L139?message=Update%20Docs)]
</div>
Creates a structured type where rather than merging types they simply compound onto one another
  - `other`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredType.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/StructuredType/StructuredType.py#L148)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/StructuredType/StructuredType.py#L148?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredType.repeat" class="docs-object-method">&nbsp;</a> 
```python
repeat(self, n=None, m=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/StructuredType/StructuredType.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/StructuredType/StructuredType.py#L152?message=Update%20Docs)]
</div>
Returns a new version of the type, but with the appropriate shape for being repeated n-to-m times
  - `n`: `Any`
    > 
  - `m`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredType.drop_axis" class="docs-object-method">&nbsp;</a> 
```python
drop_axis(self, axis=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/StructuredType/StructuredType.py#L175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/StructuredType/StructuredType.py#L175?message=Update%20Docs)]
</div>
Returns a new version of the type, but with the appropriate shape for dropping an axis
  - `axis`: `int`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredType.extend_shape" class="docs-object-method">&nbsp;</a> 
```python
extend_shape(self, base_shape): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/StructuredType/StructuredType.py#L197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/StructuredType/StructuredType.py#L197?message=Update%20Docs)]
</div>
Extends the shape of the type such that base_shape precedes the existing shape
  - `base_shape`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredType.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/StructuredType/StructuredType.py#L235)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/StructuredType/StructuredType.py#L235?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/StructuredType/StructuredType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/StructuredType/StructuredType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/StructuredType/StructuredType.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/StructuredType/StructuredType.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/StructuredType.py#L11?message=Update%20Docs)   
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