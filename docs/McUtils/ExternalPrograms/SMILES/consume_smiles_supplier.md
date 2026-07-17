# <a id="McUtils.ExternalPrograms.SMILES.consume_smiles_supplier">consume_smiles_supplier</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L491)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L491?message=Update%20Docs)]
</div>

```python
consume_smiles_supplier(supplier: McUtils.ExternalPrograms.SMILES.SMILESSupplier, consumer, pool=None, start_at=None, upto=None, initializer=None): 
```
**LLM Docstring**

Apply a consumer function to the SMILES entries of a supplier, optionally in
parallel across a multiprocessing pool (splitting the entries into per-worker
blocks).
  - `supplier`: `SMILESSupplier`
    > the SMILES supplier
  - `consumer`: `Callable`
    > the per-SMILES callable (its non-`None` results are collected)
  - `pool`: `object | int | bool | None`
    > a pool, process count, `True` for a default pool, or `None` for serial
  - `start_at`: `int | None`
    > the starting entry index
  - `upto`: `int | None`
    > the exclusive stopping index
  - `initializer`: `Callable | None`
    > a worker initializer
  - `:returns`: `list`
    > the collected results











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/SMILES/consume_smiles_supplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/SMILES/consume_smiles_supplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/SMILES/consume_smiles_supplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/SMILES/consume_smiles_supplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L491?message=Update%20Docs)   
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