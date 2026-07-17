## <a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier">SMILESSupplier</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L16?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
known_suppliers: dict
```
<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, smiles_file, line_indices=None, name=None, size=1000, split_idx=0, split_char=None, line_parser=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L17)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L17?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L80)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L80?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a supplier for one of the known SMILES databases (e.g. `zinc20`,
`emols`, `pubchem`).
  - `name`: `str`
    > the database name
  - `:returns`: `SMILESSupplier`
    > the supplier


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.to_mp_state" class="docs-object-method">&nbsp;</a> 
```python
to_mp_state(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L95)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L95?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L111)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L111?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L141)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L141?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L173)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L173?message=Update%20Docs)]
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


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L194)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L194?message=Update%20Docs)]
</div>
**LLM Docstring**

The number of entries in the file, building the full line index if it isn't
already known.
  - `:returns`: `int`
    > the entry count


<a id="McUtils.ExternalPrograms.SMILES.SMILESSupplier.find_smi" class="docs-object-method">&nbsp;</a> 
```python
find_smi(self, n, block_size=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L266)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L266?message=Update%20Docs)]
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
consume_iter(self, start_at=None, upto=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L303)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L303?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L348)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L348?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L365)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L365?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L394)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESSupplier.py#L394?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L443)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L443?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L16?message=Update%20Docs)   
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