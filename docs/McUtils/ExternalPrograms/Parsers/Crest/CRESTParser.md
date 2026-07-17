## <a id="McUtils.ExternalPrograms.Parsers.Crest.CRESTParser">CRESTParser</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Crest.py#L112)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Crest.py#L112?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
opt_log_file: str
confgen_log_file: str
ensemble_energies_file: str
ensembe_file: str
conformers_best_file: str
conformers_file: str
rotamers_file: str
CRESTConformers: CRESTConformers
CRESTRotamers: CRESTRotamers
```
<a id="McUtils.ExternalPrograms.Parsers.Crest.CRESTParser.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, parse_dir, opt_log_file=None, confgen_log_file=None, ensemble_energies_file=None, conformers_file=None, conformers_best_file=None, rotamers_file=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Crest.py#L121)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Crest.py#L121?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a parser over a CREST output directory, locating each of the standard
output files (optimization log, confgen log, ensemble energies, conformers,
best conformers, rotamers).
  - `parse_dir`: `str`
    > the CREST output directory
  - `opt_log_file`: `str | None`
    > override for the optimization-log file name
  - `confgen_log_file`: `str | None`
    > override for the confgen-log file name
  - `ensemble_energies_file`: `str | None`
    > override for the ensemble-energies file name
  - `conformers_file`: `str | None`
    > override for the conformers file name
  - `conformers_best_file`: `str | None`
    > override for the best-conformers file name
  - `rotamers_file`: `str | None`
    > override for the rotamers file name


<a id="McUtils.ExternalPrograms.Parsers.Crest.CRESTParser.parse_optimized_structures" class="docs-object-method">&nbsp;</a> 
```python
parse_optimized_structures(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.py#L158)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.py#L158?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse the optimization-log file into its sequence of structures.
  - `:returns`: `list`
    > the optimization structures


<a id="McUtils.ExternalPrograms.Parsers.Crest.CRESTParser.parse_ensemble_enegies" class="docs-object-method">&nbsp;</a> 
```python
parse_ensemble_enegies(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.py#L171)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.py#L171?message=Update%20Docs)]
</div>
**LLM Docstring**

Load the ensemble-energies file as a numeric array.
  - `:returns`: `np.ndarray`
    > the ensemble energies


<a id="McUtils.ExternalPrograms.Parsers.Crest.CRESTParser.parse_conformers" class="docs-object-method">&nbsp;</a> 
```python
parse_conformers(self, conformers_file=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.py#L183)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.py#L183?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse a conformers XYZ file into atoms, per-conformer energies, and coordinates.
  - `conformers_file`: `str | None`
    > the conformers file (defaults to the located one)
  - `:returns`: `CRESTParser.CRESTConformers`
    > the parsed `(atoms, energies, coords)`


<a id="McUtils.ExternalPrograms.Parsers.Crest.CRESTParser.parse_best_conformers" class="docs-object-method">&nbsp;</a> 
```python
parse_best_conformers(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.py#L203)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.py#L203?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse the best-conformers XYZ file.
  - `:returns`: `CRESTParser.CRESTConformers`
    > the parsed `(atoms, energies, coords)`


<a id="McUtils.ExternalPrograms.Parsers.Crest.CRESTParser.parse_rotamers" class="docs-object-method">&nbsp;</a> 
```python
parse_rotamers(self, rotamers_file=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.py#L215)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.py#L215?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse a rotamers XYZ file into atoms, energies, weights, and coordinates.
  - `rotamers_file`: `str | None`
    > the rotamers file (defaults to the located one)
  - `:returns`: `CRESTParser.CRESTRotamers`
    > the parsed `(atoms, energies, weights, coords)`


<a id="McUtils.ExternalPrograms.Parsers.Crest.CRESTParser.parse_log" class="docs-object-method">&nbsp;</a> 
```python
parse_log(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.py#L235)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.py#L235?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse the conformer-generation log file.
  - `:returns`: `dict`
    > the parsed log data
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/Crest/CRESTParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/Crest.py#L112?message=Update%20Docs)   
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