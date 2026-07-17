# <a id="McUtils.ExternalPrograms.SMILES.match_smiles_supplier">match_smiles_supplier</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L622)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L622?message=Update%20Docs)]
</div>

```python
match_smiles_supplier(supplier: McUtils.ExternalPrograms.SMILES.SMILESSupplier, matcher, pool=None, start_at=None, upto=None, quiet=True, out_file=None, initializer=None): 
```
**LLM Docstring**

Match every SMILES entry in a supplier against a SMARTS pattern (or matcher),
optionally in parallel and with RDKit logging suppressed, and optionally write
the matches to a file.
  - `supplier`: `SMILESSupplier`
    > the SMILES supplier
  - `matcher`: `Callable | str`
    > a matcher callable, or a SMARTS pattern string
  - `pool`: `object | int | bool | None`
    > a pool/process count for parallel matching
  - `start_at`: `int | None`
    > the starting entry index
  - `upto`: `int | None`
    > the exclusive stopping index
  - `quiet`: `bool`
    > suppress RDKit logging
  - `out_file`: `str | bool | None`
    > an output file path, or `True` to auto-name one
  - `initializer`: `Callable | None`
    > a worker initializer
  - `:returns`: `list[str]`
    > the matching SMILES strings











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/SMILES/match_smiles_supplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/SMILES/match_smiles_supplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/SMILES/match_smiles_supplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/SMILES/match_smiles_supplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L622?message=Update%20Docs)   
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