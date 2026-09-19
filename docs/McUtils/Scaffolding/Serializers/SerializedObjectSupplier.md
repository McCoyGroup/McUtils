## <a id="McUtils.Scaffolding.Serializers.SerializedObjectSupplier">SerializedObjectSupplier</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L3689)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L3689?message=Update%20Docs)]
</div>

Shared writing and packaging support for concrete object formats.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Scaffolding.Serializers.SerializedObjectSupplier.serialize_object" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
serialize_object(cls, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3692)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3692?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.SerializedObjectSupplier.write_object" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
write_object(cls, stream, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3696)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3696?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.SerializedObjectSupplier.write_objects" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
write_objects(cls, objects, data_file, line_indices_file=None, overwrite=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3702)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3702?message=Update%20Docs)]
</div>
Serialize objects and return a supplier with a complete jump index.


<a id="McUtils.Scaffolding.Serializers.SerializedObjectSupplier.append" class="docs-object-method">&nbsp;</a> 
```python
append(self, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/SerializedObjectSupplier.py#L3732)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/SerializedObjectSupplier.py#L3732?message=Update%20Docs)]
</div>
Append one object and its byte offset to the sidecar jump index.


<a id="McUtils.Scaffolding.Serializers.SerializedObjectSupplier.extend" class="docs-object-method">&nbsp;</a> 
```python
extend(self, objects): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/SerializedObjectSupplier.py#L3736)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/SerializedObjectSupplier.py#L3736?message=Update%20Docs)]
</div>
Append an iterable of objects and atomically update the jump index.

Only suppliers backed by ordinary files are mutable. Packaged jump
databases are intentionally read-only because changing a tar member
would require rebuilding the archive. If serialization or index
persistence fails, the data file is truncated to its original size.


<a id="McUtils.Scaffolding.Serializers.SerializedObjectSupplier.create_jump_database" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create_jump_database(cls, objects, out_file, name=None, metadata_arrays=None, stored_file_name=None, overwrite=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3828)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3828?message=Update%20Docs)]
</div>
Serialize an iterable directly into a packaged jump database.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/SerializedObjectSupplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/SerializedObjectSupplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/SerializedObjectSupplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/SerializedObjectSupplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L3689?message=Update%20Docs)   
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