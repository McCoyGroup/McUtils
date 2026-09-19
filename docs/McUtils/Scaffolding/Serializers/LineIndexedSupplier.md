## <a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier">LineIndexedSupplier</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L3146)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L3146?message=Update%20Docs)]
</div>

Stream and randomly access objects serialized one per line.

``deserialization_function`` receives one raw line (normally ``bytes``)
and returns the corresponding object.  A line-index is an ndarray of
byte offsets.  A jump database is an uncompressed tar containing the
source lines, that ndarray, metadata, and optional index-aligned arrays.

Subclasses configure the default name of the source member with
``STORED_FILE_NAME``.  ``stored_file_name=`` on
name is recorded in the database metadata and honored when it is loaded.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
STORED_FILE_NAME: str
INDEX_FILE_NAME: str
META_FILE_NAME: str
```
<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, data_file, line_indices=None, name=None, size=1000, managed_streams=None, deserialization_function=None, metadata_arrays=None, stored_file_name=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L3166)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L3166?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.from_jump_database" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_jump_database(cls, database_file, name=None, deserialization_function=None, metadata_arrays=None, create=False, **extra): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3202)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3202?message=Update%20Docs)]
</div>
Open a packaged or expanded jump database.

When ``create=True``, ``database_file`` is treated as an expanded
database directory. The directory and any missing empty database
files are created before opening it. Existing database files are
never truncated or replaced.


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.to_mp_state" class="docs-object-method">&nbsp;</a> 
```python
to_mp_state(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3385)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3385?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.from_mp_state" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mp_state(cls, state, line_indices=None, **extra): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3393)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3393?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3405)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3405?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3434)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3434?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.__del__" class="docs-object-method">&nbsp;</a> 
```python
__del__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3446)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3446?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3451)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3451?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.find_object" class="docs-object-method">&nbsp;</a> 
```python
find_object(self, n, block_size=None, include_metadata=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3472)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3472?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.consume_iter" class="docs-object-method">&nbsp;</a> 
```python
consume_iter(self, start_at=None, upto=None, include_metadata=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3505)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3505?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.__next__" class="docs-object-method">&nbsp;</a> 
```python
__next__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3536)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3536?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3549)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3549?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.create_line_index" class="docs-object-method">&nbsp;</a> 
```python
create_line_index(self, upto=None, return_index=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3563)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3563?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.save_line_index" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
save_line_index(cls, file, line_index): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3582)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3582?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.write_jump_database" class="docs-object-method">&nbsp;</a> 
```python
write_jump_database(self, target, **options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3591)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/LineIndexedSupplier.py#L3591?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.LineIndexedSupplier.build_jump_database" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
build_jump_database(cls, supplier_or_data_file, out_file, line_indices=None, name=None, metadata_arrays=None, stored_file_name=None, overwrite=False, extra_metadata=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3609)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3609?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/LineIndexedSupplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/LineIndexedSupplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/LineIndexedSupplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/LineIndexedSupplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L3146?message=Update%20Docs)   
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