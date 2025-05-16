## <a id="McUtils.Data.CommonData.DataRecord">DataRecord</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData.py#L171)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData.py#L171?message=Update%20Docs)]
</div>

Represents an individual record that might be accessed from a `DataHandler`.
Implements _most_ of the `dict` interface, but, to make things a bit easier when
pickling, is not implemented as a proper subclass of `dict`.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Data.CommonData.DataRecord.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, data_handler, key, records): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataRecord.py#L177)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataRecord.py#L177?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataRecord.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataRecord.py#L182)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataRecord.py#L182?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataRecord.values" class="docs-object-method">&nbsp;</a> 
```python
values(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataRecord.py#L184)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataRecord.py#L184?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataRecord.items" class="docs-object-method">&nbsp;</a> 
```python
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataRecord.py#L186)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataRecord.py#L186?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataRecord.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataRecord.py#L189)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataRecord.py#L189?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataRecord.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataRecord.py#L192)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataRecord.py#L192?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataRecord.__getstate__" class="docs-object-method">&nbsp;</a> 
```python
__getstate__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataRecord.py#L200)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataRecord.py#L200?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataRecord.__setstate__" class="docs-object-method">&nbsp;</a> 
```python
__setstate__(self, state): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataRecord.py#L205)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataRecord.py#L205?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Data/CommonData/DataRecord.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Data/CommonData/DataRecord.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Data/CommonData/DataRecord.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Data/CommonData/DataRecord.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData.py#L171?message=Update%20Docs)   
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