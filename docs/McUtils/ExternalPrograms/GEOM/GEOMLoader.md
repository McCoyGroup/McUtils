## <a id="McUtils.ExternalPrograms.GEOM.GEOMLoader">GEOMLoader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM.py#L44)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L44?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
MolStub: MolStub
CHECK_LOADED_BONDS: str
PERMUTE_ATOMS: NoneType
```
<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, root: 'Union[str, Path]', subset: 'str', summary_path: 'str' = 'summary_dic.json', jump_index_path: 'Optional[Union[str, Path]]' = None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM.py#L46)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L46?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.compile_jump_indices" class="docs-object-method">&nbsp;</a> 
```python
compile_jump_indices(self, out_path: 'Union[str, Path]' = 'geom_jump_indices.npz') -> 'Path': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L175?message=Update%20Docs)]
</div>
Fully scan the archive once (every *.pickle, any subset), recording
each member's tar header offset, and save the name -> offset
mapping as a compressed .npz with arrays "keys" and "offsets".
Pass the resulting file back in as `jump_index_path` on a future
GEOMLoader(...) call to skip scanning for any path it covers.


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.supports_random_access" class="docs-object-method">&nbsp;</a> 
```python
supports_random_access(self) -> 'bool': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L292)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L292?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self) -> 'int': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L295)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L295?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.get_molecule_records" class="docs-object-method">&nbsp;</a> 
```python
get_molecule_records(self, index: 'int', max_confs_per_mol: 'Optional[int]' = None, create_mols=True) -> 'list[tuple[RDMolecule, dict]]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L504)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L504?message=Update%20Docs)]
</div>
Return every (record, meta) conformer pair for molecule `index`.


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.get_record" class="docs-object-method">&nbsp;</a> 
```python
get_record(self, index: 'int', conformer_index: 'int' = 0, create_mols: 'bool' = True) -> 'tuple[RDMolecule, dict]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L524)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L524?message=Update%20Docs)]
</div>
Return a single (record, meta) for molecule `index`, conformer `conformer_index`.


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, index: 'int') -> 'tuple': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L542)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L542?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.iter_geom_records" class="docs-object-method">&nbsp;</a> 
```python
iter_geom_records(self, max_mols: 'Optional[int]' = None, max_confs_per_mol: 'Optional[int]' = None, create_mols: 'bool' = True) -> 'Iterator[tuple[RDMolecule, dict]]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L697)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L697?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L728)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L728?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self) -> "'GEOMLoader'": 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L733)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L733?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMLoader.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc, tb) -> 'None': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L736)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMLoader.py#L736?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L44?message=Update%20Docs)   
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