## <a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier">SMILESSupplier</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L108)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L108?message=Update%20Docs)]
</div>

Provides fast, offset-indexed random access into large `.smi` files.

Normally this needs *two* files: the `.smi` file itself and a `.npy`
array of line-start byte offsets (see `known_suppliers`, e.g.
`ZINC20.smi` + `ZINC20_idx.npy`). It can also transparently load a
single packaged `line_index_smiles_database` archive -- an uncompressed
tar file bundling both together plus a little metadata -- produced by
`build_line_index_smiles_database`/`package_known_supplier`. Just pass
the archive's path as `smiles_file` and leave `line_indices` unset:

    supplier = SMILESSupplier("ZINC20.tar")
    with supplier:
        for smi in supplier.consume_iter(upto=10):
            print(smi)







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
LISMI_SMI_MEMBER: str
LISMI_IDX_MEMBER: str
LISMI_META_MEMBER: str
known_suppliers: dict
```
<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, smiles_file, line_indices=None, name=None, size=1000, split_idx=0, split_char=None, managed_streams=None, line_parser=None, metadata_arrays=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L131)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L131?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a streaming reader over a (potentially very large) SMILES file, using a
line-offset index for random access.
  - `smiles_file`: `str`
    > the SMILES file (path or stream)
  - `line_indices`: `np.ndarray | str | None`
    > precomputed byte offsets, or a `.npy` path to load them from
  - `name`: `str | None`
    > an optional name for the supplier
  - `size`: `int`
    > the initial offset-index size
  - `split_idx`: `int`
    > which whitespace/`split_char`-delimited field holds the SMILES
  - `split_char`: `str | bytes | None`
    > the field separator (defaults to whitespace)
  - `line_parser`: `Callable | None`
    > a custom line-to-SMILES parser


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.from_name" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_name(cls, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L199)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L199?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.from_line_index_database" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_line_index_database(cls, database_file, name=None, split_idx=<McUtils.Devutils.core.DefaultType instance>, split_char=None, metadata_arrays=None, **extra): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L203)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L203?message=Update%20Docs)]
</div>
Explicit, self-documenting alias for constructing a supplier
directly from a packaged `line_index_smiles_database` archive.
(`SMILESSupplier(database_file)` works identically, since the
archive is auto-detected in `__init__`.)

`database_file` may also be a *directory* holding the same
members as plain files -- e.g. the result of expanding a packaged
archive with `tar -xf whatever.tar -C some_dir/` -- in which
case everything is loaded directly as normal files (no tar
streaming or held-open handles involved).

Any `metadata_arrays` packaged into the archive (see
`build_line_index_smiles_database_from_source`) are loaded back
automatically. Passing `metadata_arrays` here adds to/overrides
those by key, rather than replacing them outright.


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.to_mp_state" class="docs-object-method">&nbsp;</a> 
```python
to_mp_state(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L368)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L368?message=Update%20Docs)]
</div>
**LLM Docstring**

Serialize the minimal state needed to rebuild this supplier in a worker process.
  - `:returns`: `tuple`
    > the picklable state tuple


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.from_mp_state" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mp_state(cls, state, line_indices=None, **extra): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L384)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L384?message=Update%20Docs)]
</div>
**LLM Docstring**

Rebuild a supplier from the state produced by `to_mp_state`, optionally with a
fresh offset index.
  - `state`: `tuple`
    > the state tuple from `to_mp_state`
  - `line_indices`: `np.ndarray | None`
    > precomputed byte offsets for this worker's block
  - `extra`: `Any`
    > extra constructor overrides
  - `:returns`: `SMILESSupplier`
    > the supplier


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L414)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L414?message=Update%20Docs)]
</div>
**LLM Docstring**

Open the underlying stream (reentrantly), initializing the offset index and
default parser on the outermost entry.
  - `:returns`: `object`
    > the opened stream


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L460)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L460?message=Update%20Docs)]
</div>
**LLM Docstring**

Close the underlying stream on the outermost exit, restoring the offset index and
parser.
  - `exc_type`: `Any`
    > the exception type, if any
  - `exc_val`: `Any`
    > the exception value, if any
  - `exc_tb`: `Any`
    > the traceback, if any


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__del__" class="docs-object-method">&nbsp;</a> 
```python
__del__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L482)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L482?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L487)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L487?message=Update%20Docs)]
</div>
**LLM Docstring**

The number of entries in the file, building the full line index if it isn't
already known.
  - `:returns`: `int`
    > the entry count


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.find_smi" class="docs-object-method">&nbsp;</a> 
```python
find_smi(self, n, block_size=None, include_metadata=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L565)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L565?message=Update%20Docs)]
</div>
**LLM Docstring**

Seek to and read the `n`-th entry (extending the line index if needed),
optionally reading a block of `block_size` consecutive entries.
  - `n`: `int`
    > the entry index
  - `block_size`: `int | None`
    > number of consecutive entries to read
  - `:returns`: `str | list[str]`
    > the SMILES entry, or a list of entries


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.consume_iter" class="docs-object-method">&nbsp;</a> 
```python
consume_iter(self, start_at=None, upto=None, include_metadata=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L616)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L616?message=Update%20Docs)]
</div>
**LLM Docstring**

Iterate over the SMILES entries from `start_at` up to `upto` (or the end),
recording byte offsets as it goes when the index is assignable.
  - `start_at`: `int | None`
    > the starting entry index (defaults to the current position)
  - `upto`: `int | None`
    > the exclusive stopping index (or the end if omitted)
  - `:returns`: `Iterator[str]`
    > a generator of SMILES strings


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__next__" class="docs-object-method">&nbsp;</a> 
```python
__next__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L674)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L674?message=Update%20Docs)]
</div>
**LLM Docstring**

Read the entry at the current cursor position (the supplier must be open).
  - `:returns`: `str`
    > the SMILES entry


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__iter__" class="docs-object-method">&nbsp;</a> 
```python
__iter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L691)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L691?message=Update%20Docs)]
</div>
**LLM Docstring**

Iterate over all entries from the current position.
  - `:returns`: `Iterator[str]`
    > a generator of SMILES strings


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.create_line_index" class="docs-object-method">&nbsp;</a> 
```python
create_line_index(self, upto=None, return_index=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L720)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L720?message=Update%20Docs)]
</div>
**LLM Docstring**

Scan the file to build (or extend) the byte-offset index, up to `upto` entries or
the end of the file.
  - `upto`: `int | None`
    > the entry index to build up to (or the whole file if omitted)
  - `return_index`: `bool`
    > return the offsets rather than just building them
  - `:returns`: `np.ndarray | None`
    > the offset index, or `None`


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.save_line_index" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
save_line_index(cls, file, line_index): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L769)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L769?message=Update%20Docs)]
</div>
**LLM Docstring**

Save a byte-offset index to a `.npy` file, down-casting it to the smallest
unsigned integer dtype that fits.
  - `file`: `str`
    > the output file
  - `line_index`: `np.ndarray`
    > the offset index
  - `:returns`: `_`
    > the result of `np.save`


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.write_database_index" class="docs-object-method">&nbsp;</a> 
```python
write_database_index(self, target, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L790)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L790?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.build_line_index_smiles_database_from_source" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
build_line_index_smiles_database_from_source(cls, supplier_or_smiles_file, out_file, line_indices=None, name=None, split_idx=0, split_char=None, metadata_arrays=None, overwrite=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L818)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L818?message=Update%20Docs)]
</div>
Build a `line_index_smiles_database` archive: a single uncompressed tar
file bundling a `.smi` file together with its line-offset index, so
that `SMILESSupplier(out_file)` can load both at once.
  - `supplier_or_smiles_file`: `Any`
    > either an existing `SMILESSupplier`
    instance (backed by a real file path -- its `.smi` file and, if
    available, its already-computed line index are reused), or a path
    to a raw `.smi`/`.smiles` file.
  - `out_file`: `Any`
    > path to write the archive to.
  - `line_indices`: `Any`
    > path to a prebuilt `.npy` index (as produced by
    `SMILESSupplier.save_line_index`) or an array of offsets. If
    omitted and `supplier_or_smiles_file` doesn't already carry one,
    the index is generated by scanning the SMILES file, which can be
    slow for large databases.
  - `name`: `Any`
    > optional name to record in the archive metadata.
  - `split_idx`: `Any`
    > forwarded to `SMILESSupplier` / recorded in metadata.
  - `split_char`: `Any`
    > forwarded to `SMILESSupplier` / recorded in metadata.
  - `metadata_arrays`: `Any`
    > a `{name: array_like}` dict of per-line
    metadata, index-aligned with the `.smi` file (as consumed by
    `SMILESSupplier(..., metadata_arrays=...)` /
    `find_smi(..., include_metadata=True)`). Each array is saved
    as its own `.npy` archive member; the `name -> member name`
    mapping is recorded under `"metadata_arrays"` in `meta.json`.
    If omitted and `supplier_or_smiles_file` is a `SMILESSupplier`
    that already carries `metadata_arrays`, those are reused.
  - `overwrite`: `Any`
    > if `False` (default), raises if `out_file` exists.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/SMILES/SMILESSupplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/SMILES/SMILESSupplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/SMILES/SMILESSupplier.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/SMILES/SMILESSupplier.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L108?message=Update%20Docs)   
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