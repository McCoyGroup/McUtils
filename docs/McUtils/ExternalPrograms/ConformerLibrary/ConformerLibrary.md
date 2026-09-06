## <a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary">ConformerLibrary</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary.py#L256)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary.py#L256?message=Update%20Docs)]
</div>

A backend-agnostic reader for conformer ensembles stored as
`(smi, coord)` pairs, one entry per molecule.

    lib = ConformerLibrary(conf_lib)                     # raw nested dict/tree
    lib = ConformerLibrary.from_nparchive("confs.npz")
    lib = ConformerLibrary.from_smidb("substances.lismi")
    lib = ConformerLibrary.qm9("qm9.npz")
    lib = ConformerLibrary.geom("rdkit_folder.tar.gz", subset='drugs')

    lib[33]                # {'smi':.., 'coord':..}, or `loader(...)`'s result
    lib.get_smiles(33)     # just the SMILES, cheaply where the backend allows
    len(lib); 33 in lib; list(lib.keys())

`backend` is always the first constructor argument: pass an
explicit `ConformerLibraryBackend` (or any of the per-format
`from_*`/named constructors below), or a raw tree/path/archive to
have it wrapped in the default `NumpyTreeArchiveBackend`.

`loader`, if given, is applied to every raw `{'smi':.., 'coord':..}`
record before it's returned from `__getitem__`/`get_record` -- e.g.
to turn it into a `Molecule` (or list of `Molecule`s) instead of a
plain dict.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
LibraryBackend: ConformerLibraryBackend
```
<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, backend=None, loader=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary.py#L284)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary.py#L284?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L292)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L292?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.__contains__" class="docs-object-method">&nbsp;</a> 
```python
__contains__(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L295)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L295?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L298)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L298?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.keys" class="docs-object-method">&nbsp;</a> 
```python
keys(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L301)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L301?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.get_smiles" class="docs-object-method">&nbsp;</a> 
```python
get_smiles(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L304?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.get_record" class="docs-object-method">&nbsp;</a> 
```python
get_record(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L307)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L307?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L313)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L313?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.items" class="docs-object-method">&nbsp;</a> 
```python
items(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L316)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L316?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.save" class="docs-object-method">&nbsp;</a> 
```python
save(self, file, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L320)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L320?message=Update%20Docs)]
</div>
Persists this library, if its backend supports it (currently
only `NumpyTreeArchiveBackend`).


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L327)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.py#L327?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.from_nparchive" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_nparchive(cls, archive, loader=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L332)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L332?message=Update%20Docs)]
</div>
Builds a library over the default `NumpyTreeArchive` backend
(a path, an open `NumpyTreeArchive`, or a raw nested tree/dict).


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.from_smidb" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_smidb(cls, smiles_file, loader=None, coord_key='coord', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L338)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L338?message=Update%20Docs)]
</div>
Builds a library over a `SMILESSupplier`-backed `.smi`/
`.lismi` database (a path, or an existing `SMILESSupplier`).


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.qm9" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
qm9(cls, qm9_data, loader=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L344)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L344?message=Update%20Docs)]
</div>
Builds a library over a packed QM9 dataset (a path to its
`.npz`, or an existing `QM9` wrapper).


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.geom" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
geom(cls, root, subset='drugs', loader=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L350)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L350?message=Update%20Docs)]
</div>
Builds a library over a GEOM `rdkit_folder` archive/directory
(a path, or an existing `GEOMLoader`).


<a id="McUtils.ExternalPrograms.ConformerLibrary.ConformerLibrary.create_smiles_iterator_archive" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create_smiles_iterator_archive(cls, smi_list, target_file, loader, ensemble_generator=None, keys=None, ensemble_opts=None, save_opts=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L358)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L358?message=Update%20Docs)]
</div>
Builds a `NumpyTreeArchive`-backed conformer library by running
`conformer_generator` over every SMILES in `smi_list`, then
saving the resulting `{key: {'smi':.., 'coord':[...]}}` tree to
`target_file`. This is the default creator for the "first"
(`NumpyTreeArchive`) backend paradigm -- it's just the loop from
that paradigm's own construction idiom, generalized to an
arbitrary iterable of SMILES:

    conf_lib = {}
    for i, smi in enumerate(smi_list):
        confs, engs = generate_conformer_ensemble(Molecule.from_string, smi)
        conf_lib[str(i)] = {'smi': smi, 'coord': [c.coords for c in confs]}
    NumpyTreeArchive.from_tree(conf_lib).save(target_file)

    conf_lib = ConformerLibrary.create_smiles_iterator_archive(
        smi_list, "conformers.npz",
        loader=Molecule.from_string,
        conformer_generator=generate_conformer_ensemble
    )
  - `loader`: `Any`
    > the molecule constructor forwarded as
    `conformer_generator`'s first argument (e.g.
    `Molecule.from_string`)
  - `ensemble_generator`: `Any`
    > `(loader, smi, **ensemble_opts) ->
    (confs, engs)`, where every `conf` in `confs` exposes
    `.coords` -- e.g. a `generate_conformer_ensemble`-style
    ensemble generator. `engs` is accepted (to match that
    idiom's return signature) but not itself stored.
  - `keys`: `Any`
    > optional explicit top-level keys, index-aligned
    with `smi_list` (default: `str(i)` for `i, smi` in
    `enumerate(smi_list)`)
  - `ensemble_opts`: `Any`
    > extra keywords forwarded to
    `conformer_generator`
  - `save_opts`: `Any`
    > extra keywords forwarded to the archive's
    `.save(target_file, ...)`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ConformerLibrary/ConformerLibrary.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary.py#L256?message=Update%20Docs)   
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