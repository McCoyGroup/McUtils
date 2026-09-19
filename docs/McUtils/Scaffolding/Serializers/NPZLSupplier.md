## <a id="McUtils.Scaffolding.Serializers.NPZLSupplier">NPZLSupplier</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L3874)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L3874?message=Update%20Docs)]
</div>

Serialize mappings/arrays as binary, length-framed NPZ records.

    Each record has the form ``<decimal byte length>
<raw npz bytes>
``.
    The explicit byte length is required because an NPZ file is a ZIP stream
    and may contain arbitrary newline bytes internally. Jump indices point to
    the start of each decimal length header.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
STORED_FILE_NAME: str
```
<a id="McUtils.Scaffolding.Serializers.NPZLSupplier.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *args, allow_pickle=False, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L3885)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L3885?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NPZLSupplier.serialize_object" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
serialize_object(cls, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3889)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3889?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NPZLSupplier.write_object" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
write_object(cls, stream, obj): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3900)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3900?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NPZLSupplier.create_line_index" class="docs-object-method">&nbsp;</a> 
```python
create_line_index(self, upto=None, return_index=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NPZLSupplier.py#L3931)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NPZLSupplier.py#L3931?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/NPZLSupplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/NPZLSupplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/NPZLSupplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/NPZLSupplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L3874?message=Update%20Docs)   
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