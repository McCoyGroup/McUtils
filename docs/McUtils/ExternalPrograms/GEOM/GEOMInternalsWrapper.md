## <a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper">GEOMInternalsWrapper</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM.py#L876)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L876?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, loader, zdata, managed_store=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM.py#L877)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L877?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.from_files" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_files(cls, root=None, geom_file='geom_dataset.tar.gz', jump_index_path='geom_jump_indices.npz', coords_zip='geom_coordinates.zip'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L891)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L891?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.close" class="docs-object-method">&nbsp;</a> 
```python
close(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L908)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L908?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L912)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L912?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, *exit_args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L915)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L915?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.conformer_offsets" class="docs-object-method">&nbsp;</a> 
```python
@property
conformer_offsets(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L920)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L920?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.system_identifiers" class="docs-object-method">&nbsp;</a> 
```python
@property
system_identifiers(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L926)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L926?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.conformer_identifiers" class="docs-object-method">&nbsp;</a> 
```python
@property
conformer_identifiers(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L932)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L932?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.get_system_offsets" class="docs-object-method">&nbsp;</a> 
```python
get_system_offsets(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L938)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L938?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.system_offset" class="docs-object-method">&nbsp;</a> 
```python
system_offset(self, i, return_nconfs=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L948)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L948?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.total_conformers" class="docs-object-method">&nbsp;</a> 
```python
@property
total_conformers(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L955)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L955?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.total_systems" class="docs-object-method">&nbsp;</a> 
```python
@property
total_systems(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L963)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L963?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.sample_conformers" class="docs-object-method">&nbsp;</a> 
```python
sample_conformers(self, n, replace=False, rng=None, chunk_size=None, check_runs=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L969)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L969?message=Update%20Docs)]
</div>
Uniformly sample `n` conformers at random from the whole dataset
(systems with more conformers are proportionally more likely to
contribute -- this is uniform over *conformers*, not systems;
see sample_systems for the other kind of uniformity).

The sample itself is always `n` fully independent scattered
conformer indices -- chunk_size does not change what gets
sampled or bias it toward correlated neighbors, it only controls
how the resulting reads are batched.

chunk_size: if None (default), read the entire sample in one
oindex call per key -- simplest, but a single call has to
resolve and gather across however many chunks the full scatter
touches. If given, the (already independently sampled) indices
are split into batches of at most `chunk_size` conformers each,
read with separate oindex calls, and concatenated -- bounding
how much data any single zarr call has to touch/materialize at
once, at the cost of issuing more (smaller) calls.

check_runs: passed through to load_chunk for each batch.
Defaults to False since a uniform random sample is essentially
never contiguous, so scanning for runs is wasted work.

Each conformer i occupies the block vals[conformer_offsets[i]:
conformer_offsets[i+1]], not a single row -- so this samples
conformer indices, then load_chunk resolves each to its block.

Returns:
    idx: the sampled conformer indices (sorted)
    data: dict of concatenated 'vals'/'types'/'tags' arrays,
          points from all sampled conformers stacked together
    block_offsets: array such that conformer idx[k]'s points are
          data['vals'][block_offsets[k]:block_offsets[k+1]]
          (mirrors conformer_offsets, but local to this sample)


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.sample_systems" class="docs-object-method">&nbsp;</a> 
```python
sample_systems(self, n, replace=False, rng=None, load_confs=False, load_representative=True, chunk_size=None, check_runs=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1034)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1034?message=Update%20Docs)]
</div>
Uniformly sample `n` systems (molecules) at random, pulling all
(or a representative) conformer(s) per system.

The sample is always `n` fully independent system indices;
chunk_size does not change what gets sampled, only how the
resulting conformer data is read.

chunk_size: if None (default), read all sampled systems'
conformers in one call per key. If given, the flattened
conformer-index array is split into batches of at most
`chunk_size` conformers each and read/concatenated separately,
bounding how much a single zarr call has to gather at once.
Note each sampled system's own conformers are contiguous by
construction, so a batch boundary can occasionally split one
system's block in two -- a minor loss of contiguity within that
one batch, not a correctness issue.

check_runs: passed through to load_chunk. Defaults to True here
(unlike sample_conformers) because each sampled system
contributes a contiguous run of conformers, so the run-scan
reliably finds real structure to collapse into slice reads
rather than scanning fruitlessly.


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.load_chunk" class="docs-object-method">&nbsp;</a> 
```python
load_chunk(self, i, check_runs=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1131)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1131?message=Update%20Docs)]
</div>
Load conformer data for a single index, a contiguous range,
or an arbitrary iterable of indices. Contiguous spans are always
collapsed into one zarr read instead of one-per-index.

check_runs: if True (default), scan the given indices for
accidental contiguous runs before falling back to a scattered
oindex read -- worth it whenever the indices might actually be
block-structured (e.g. sample_conformers(chunk_size=...)).
If False, skip the scan entirely and treat every index as its
own singleton run. Set this when you already know the indices
are essentially all scattered (e.g. a large uniform random
sample) -- the scan would cost O(n) and correctly find nothing,
so skipping it is pure savings.


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.load_conformer" class="docs-object-method">&nbsp;</a> 
```python
load_conformer(self, i): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1183)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1183?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.load_system_chunks" class="docs-object-method">&nbsp;</a> 
```python
load_system_chunks(self, i, load_confs=False, load_representative=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1191)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1191?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.get_internals" class="docs-object-method">&nbsp;</a> 
```python
get_internals(self, mol): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1247)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1247?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.block_iter" class="docs-object-method">&nbsp;</a> 
```python
block_iter(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1251)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1251?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.get_block" class="docs-object-method">&nbsp;</a> 
```python
get_block(self, i): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1258)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1258?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.GEOM.GEOMInternalsWrapper.histogram_vals" class="docs-object-method">&nbsp;</a> 
```python
histogram_vals(self, specs, block_iter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1315)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.py#L1315?message=Update%20Docs)]
</div>
Build histograms over (filtered) 'vals' for several named
quantities in a single streaming pass -- never holds more than
one block plus the running per-spec counts arrays in memory.

specs: dict mapping name -> (filter_fn, bins).
    filter_fn(block) -> ndarray of the values from that block
        you want included for this spec (block is the
        {'tags','types','vals'} dict yielded by block_iter --
        filter on whatever combination of keys you need, e.g.
        `lambda b: b['vals'][b['types'] == 6]`).
    bins: either explicit bin edges (array-like), or a
        (low, high, n_bins) tuple -- two numbers and an int --
        which is expanded once via
        np.linspace(low, high, n_bins + 1). Whatever form you
        pass, it's resolved to fixed edges up front and reused
        for every block, so per-block counts can simply be
        summed. (An integer alone is NOT accepted here, since
        np.histogram would then infer different edges per
        block from that block's own min/max, silently making
        the accumulated result meaningless.)

block_iter: optional iterable of blocks to use instead of
self.block_iter() (e.g. itertools.islice(...) for a partial
pass).

Returns: dict name -> (counts, edges)
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/GEOM/GEOMInternalsWrapper.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/GEOM.py#L876?message=Update%20Docs)   
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