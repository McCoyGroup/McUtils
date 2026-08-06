## <a id="McUtils.ExternalPrograms.GEOM.GEOMLoader">GEOMLoader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM.py#L40)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L40?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, root: 'Union[str, Path]', subset: 'str', summary_path: 'str' = 'summary_dic.json'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM.py#L42)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L42?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.supports_random_access" class="docs-object-method">&nbsp;</a> 
```python
supports_random_access(self) -> 'bool': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L94)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L94?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self) -> 'int': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L97)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L97?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.get_molecule_records" class="docs-object-method">&nbsp;</a> 
```python
get_molecule_records(self, index: 'int', max_confs_per_mol: 'Optional[int]' = None) -> 'list[tuple[RDMolecule, dict]]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L158)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L158?message=Update%20Docs)]
</div>
Return every (record, meta) conformer pair for molecule `index`.


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.get_record" class="docs-object-method">&nbsp;</a> 
```python
get_record(self, index: 'int', conformer_index: 'int' = 0) -> 'tuple[RDMolecule, dict]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L174)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L174?message=Update%20Docs)]
</div>
Return a single (record, meta) for molecule `index`, conformer `conformer_index`.


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, index: 'int') -> 'tuple': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L190)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L190?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.iter_geom_records" class="docs-object-method">&nbsp;</a> 
```python
iter_geom_records(self, max_mols: 'Optional[int]' = None, max_confs_per_mol: 'Optional[int]' = None) -> 'Iterator[tuple[RDMolecule, dict]]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L271?message=Update%20Docs)]
</div>
Yield (record, meta) pairs, one per conformer, in whatever order the
underlying storage returns molecules.

record:
    - if return_mols=False: (smiles, coords), coords an
      (n_atoms, 3) float64 numpy array of Angstrom coordinates.
    - if return_mols=True: the RDKit Chem.Mol for that conformer.

meta:
    dict with smiles, pickle_path, conformer_index, n_atoms,
    atomic_numbers, total_energy, boltzmann_weight.

Gzip-tar mode is a strict single forward pass: re-decompresses
from the start on every call. Directory and plain-tar modes are
cheap to call repeatedly.


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.close" class="docs-object-method">&nbsp;</a> 
```python
close(self) -> 'None': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L301)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L301?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self) -> "'GEOMLoader'": 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L306)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L306?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc, tb) -> 'None': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L309)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L309?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/GEOM/GEOMLoader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/GEOM/GEOMLoader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/GEOM/GEOMLoader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/GEOM/GEOMLoader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L40?message=Update%20Docs)   
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