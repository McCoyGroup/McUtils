## <a id="McUtils.Parsers.StorageBackends.StructuredTypeArrayException">StructuredTypeArrayException</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends.py#L76)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L76?message=Update%20Docs)]
</div>

Same name/role as the original exception, extended with structured
fields so a `except StructuredTypeArrayException as e` handler can act
on `e.index` / `e.expected_shape` / `e.actual_shape` /
`e.offending_value` instead of parsing them back out of a message
string that may contain a full array `repr()`.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Parsers.StorageBackends.StructuredTypeArrayException.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, message, *, stype=None, expected_shape=None, actual_shape=None, offending_value=None, index=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends.py#L85)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L85?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.StructuredTypeArrayException.__str__" class="docs-object-method">&nbsp;</a> 
```python
__str__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/StructuredTypeArrayException.py#L102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/StructuredTypeArrayException.py#L102?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/StorageBackends/StructuredTypeArrayException.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/StorageBackends/StructuredTypeArrayException.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/StorageBackends/StructuredTypeArrayException.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/StorageBackends/StructuredTypeArrayException.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L76?message=Update%20Docs)   
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