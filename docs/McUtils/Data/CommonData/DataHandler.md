## <a id="McUtils.Data.CommonData.DataHandler">DataHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData.py#L18)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData.py#L18?message=Update%20Docs)]
</div>

Defines a general data loader class that we can use for `AtomData` and any other data classes we might find useful.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Data.CommonData.DataHandler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, data_name, data_key=None, source_key=None, data_dir=None, data_pkg=None, alternate_keys=None, getter=None, record_type=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataHandler.py#L22)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataHandler.py#L22?message=Update%20Docs)]
</div>

  - `data_name`: `str`
    > the name of the dataset
  - `data_key`: `str | None`
    > the key in the loaded dictionary to use for the actual data (`"data"` by default)
  - `source_key`: `str | None`
    > the key in the loaded dictionary for the original data source (`"source"` by default)
  - `data_dir`: `str | None`
    > the main directory data will be loaded from (`.` by default)
  - `data_pkg`: `str | None`
    > the python package to load (`TheRealMcCoy` by default)
  - `alternate_keys`: `Iterable[str] | None`
    > alternate keys that can be used to index into the dataset which can will be populated at runtime
  - `getter`: `callable | None`
    > a function to use to resolve a key
  - `record_type`: `type | None`
    > the class to use for holding data (`DataRecord` by default)


<a id="McUtils.Data.CommonData.DataHandler.data_file" class="docs-object-method">&nbsp;</a> 
```python
@property
data_file(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataHandler.py#L69)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataHandler.py#L69?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataHandler.load" class="docs-object-method">&nbsp;</a> 
```python
load(self, env=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataHandler.py#L81)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataHandler.py#L81?message=Update%20Docs)]
</div>
Actually loads the data from `data_file`.
Currently set up to just use an `import` statement but should
be reimplemented to use a `Deserializer` from `Scaffolding.Serializers`
  - `:returns`: `_`
    >


<a id="McUtils.Data.CommonData.DataHandler.data" class="docs-object-method">&nbsp;</a> 
```python
@property
data(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataHandler.py#L107)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataHandler.py#L107?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataHandler.source" class="docs-object-method">&nbsp;</a> 
```python
@property
source(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataHandler.py#L112)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataHandler.py#L112?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataHandler.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataHandler.py#L143)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataHandler.py#L143?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataHandler.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataHandler.py#L146)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataHandler.py#L146?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataHandler.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataHandler.py#L148)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataHandler.py#L148?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataHandler.__getstate__" class="docs-object-method">&nbsp;</a> 
```python
__getstate__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataHandler.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataHandler.py#L152?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataHandler.__setstate__" class="docs-object-method">&nbsp;</a> 
```python
__setstate__(self, state): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataHandler.py#L160)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataHandler.py#L160?message=Update%20Docs)]
</div>


<a id="McUtils.Data.CommonData.DataHandler.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/CommonData/DataHandler.py#L164)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData/DataHandler.py#L164?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Data/CommonData/DataHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Data/CommonData/DataHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Data/CommonData/DataHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Data/CommonData/DataHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/CommonData.py#L18?message=Update%20Docs)   
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