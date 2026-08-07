## <a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive">NumpyTreeArchive</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L2937)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L2937?message=Update%20Docs)]
</div>

Wraps a flattened tree (as produced by flatten_tree) plus an optional
jump table, supporting both full eager unflattening and lazy,
path-based sub-record access ("ep_001", "ep_001/obs", ...) without
walking the whole visited_keys sequence.

Usage:
    archive = NumpyTreeArchive.from_tree(data)
    archive.save("dataset.npz")

    archive = NumpyTreeArchive.load("dataset.npz")
    archive["ep_001/obs"]        # lazy sub-record access
    archive.unpack()             # full eager unflatten
    list(archive.keys())         # all indexed paths
    for path, value in archive.items(): ...
    len(archive)                 # number of indexed paths
    "ep_001" in archive







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, serial_tree, jump_table=None, path_sep='/'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L2957)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L2957?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.from_tree" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_tree(cls, tree, allow_pickle=False, build_jt=True, max_depth=0, path_sep='/'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2979)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2979?message=Update%20Docs)]
</div>
Build an archive directly from a nested Python dict.


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.load" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load(cls, file, reader=None, allow_pickle=False, path_sep='/', backend='npz', lazy=True, **reader_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2986)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2986?message=Update%20Docs)]
</div>
Load an archive.
  - `backend`: `Any`
    > 'npz' (default) or 'zarr'. 'zarr' additionally
                accepts `lazy` (default True) to control whether
                the big arrays (visited_keys, per-key values) stay
                as lazy zarr.Array references or get fully
                materialized up front.


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.save" class="docs-object-method">&nbsp;</a> 
```python
save(self, file, writer=None, max_depth=None, backend='npz', save_jump_table=True, **writer_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3009)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3009?message=Update%20Docs)]
</div>
Write this archive.
  - `backend`: `Any`
    > 'npz' (default) or 'zarr'. zarr-specific options
                (`chunks`, `compressors`, `overwrite`) go in
                **writer_options when backend='zarr'.


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.unpack" class="docs-object-method">&nbsp;</a> 
```python
unpack(self, max_leaf_elements=None, prefix_filter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3031)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3031?message=Update%20Docs)]
</div>
Fully unflatten the archive into a nested dict.


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.get" class="docs-object-method">&nbsp;</a> 
```python
get(self, path, default=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3037)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3037?message=Update%20Docs)]
</div>
Lazily unpack the sub-record at `path`, or return `default`.


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, path): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3045)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3045?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, path): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3050)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3050?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3053)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3053?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3056)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3056?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3059)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3059?message=Update%20Docs)]
</div>
All indexed paths (records and, if built with max_depth=None, sub-records).


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.values" class="docs-object-method">&nbsp;</a> 
```python
values(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3063)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3063?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.items" class="docs-object-method">&nbsp;</a> 
```python
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3067)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3067?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Serializers.NumpyTreeArchive.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3071)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers/NumpyTreeArchive.py#L3071?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/NumpyTreeArchive.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/NumpyTreeArchive.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/NumpyTreeArchive.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/NumpyTreeArchive.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L2937?message=Update%20Docs)   
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