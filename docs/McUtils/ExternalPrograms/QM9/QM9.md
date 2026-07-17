## <a id="McUtils.ExternalPrograms.QM9.QM9">QM9</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/QM9.py#L13)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/QM9.py#L13?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
property_array_keys: list
```
<a id="McUtils.ExternalPrograms.QM9.QM9.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, qm9_data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/QM9.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/QM9.py#L15?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap a loaded QM9 dataset (or load it from a `.npz` path).
  - `qm9_data`: `str | object`
    > the loaded dataset, or a path to a QM9 `.npz` file


<a id="McUtils.ExternalPrograms.QM9.QM9.build_qm9" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
build_qm9(cls, qm9_dir, pattern='*.xyz', target='qm9.npz'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L29)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L29?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a packed QM9 `.npz` dataset from a directory of extended-XYZ files,
concatenating the per-molecule atoms/coordinates/charges/frequencies into flat
arrays with per-molecule offsets and sizes, alongside the tags, indices, SMILES,
and scalar properties.
  - `qm9_dir`: `str`
    > the directory of QM9 XYZ files
  - `pattern`: `str`
    > the glob pattern for the XYZ files
  - `target`: `str`
    > the output `.npz` path
  - `:returns`: `str`
    > the output path


<a id="McUtils.ExternalPrograms.QM9.QM9.load_qm9" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_qm9(cls, qm9_file): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L104)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L104?message=Update%20Docs)]
</div>
**LLM Docstring**

Load a packed QM9 `.npz` dataset, memory-mapped.
  - `qm9_file`: `str`
    > the `.npz` path
  - `:returns`: `np.lib.npyio.NpzFile`
    > the memory-mapped dataset


<a id="McUtils.ExternalPrograms.QM9.QM9.smiles_query" class="docs-object-method">&nbsp;</a> 
```python
smiles_query(self, pattern, start_at=0, upto=None, track_failures=False, quiet=True, **parser_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/QM9/QM9.py#L119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/QM9/QM9.py#L119?message=Update%20Docs)]
</div>
**LLM Docstring**

Find the dataset entries whose SMILES match a SMARTS pattern, optionally tracking
which entries failed to parse and suppressing RDKit logging.
  - `pattern`: `str`
    > the SMARTS pattern
  - `start_at`: `int`
    > the starting entry index
  - `upto`: `int | None`
    > the exclusive stopping index (or the end)
  - `track_failures`: `bool`
    > also return the indices that failed to parse
  - `quiet`: `bool`
    > suppress RDKit logging
  - `parser_options`: `Any`
    > extra SMILES-parsing options
  - `:returns`: `list | tuple`
    > the matching indices (and failures, if requested)


<a id="McUtils.ExternalPrograms.QM9.QM9.load_data" class="docs-object-method">&nbsp;</a> 
```python
load_data(self, index, props=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/QM9/QM9.py#L205)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/QM9/QM9.py#L205?message=Update%20Docs)]
</div>
**LLM Docstring**

Load the requested properties for a single dataset entry.
  - `index`: `int`
    > the entry index
  - `props`: `list[str] | None`
    > the property names to load (a default set if omitted)
  - `:returns`: `dict`
    > the loaded properties


<a id="McUtils.ExternalPrograms.QM9.QM9.data_iter" class="docs-object-method">&nbsp;</a> 
```python
data_iter(self, props=None, start_at=None, upto=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/QM9/QM9.py#L230)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/QM9/QM9.py#L230?message=Update%20Docs)]
</div>
**LLM Docstring**

Iterate over the dataset entries, yielding the requested properties for each.
  - `props`: `list[str] | None`
    > the property names to load (a default set if omitted)
  - `start_at`: `int | None`
    > the starting entry index
  - `upto`: `int | None`
    > the exclusive stopping index
  - `:returns`: `Iterator[dict]`
    > a generator of per-entry property dicts
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/QM9/QM9.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/QM9/QM9.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/QM9/QM9.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/QM9/QM9.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/QM9.py#L13?message=Update%20Docs)   
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