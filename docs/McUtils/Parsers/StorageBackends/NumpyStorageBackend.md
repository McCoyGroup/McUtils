## <a id="McUtils.Parsers.StorageBackends.NumpyStorageBackend">NumpyStorageBackend</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends.py#L326)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L326?message=Update%20Docs)]
</div>

The default, high-performance backend. Semantically equivalent to the
original inline `numpy`-array code in `StructuredTypeArray`, with the
reliability fixes described above.

`padding_mode` (read off the owning `StructuredTypeArray`, passed in
per-call so the backend stays stateless):
  * ``'fill'``   -- pad short rows with `padding_value` (unchanged
                    default behavior); rows longer than the declared
                    block size raise `StructuredTypeArrayException`
                    (previously they were silently `np.tile`'d to fit,
                    which fabricates data -- that tiling fallback has
                    been removed).
  * ``'ragged'`` -- on any shape mismatch, don't raise: signal to the
                    caller (`StructuredTypeArray`) that this array
                    should be demoted to the Python backend. This is
                    surfaced via `RaggedDataSignal` rather than done
                    silently inside the backend, because *swapping the
                    backend an object uses* is `StructuredTypeArray`'s
                    job, not this backend's.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
name: str
```
<a id="McUtils.Parsers.StorageBackends.NumpyStorageBackend.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, casters: 'Optional[Dict[Any, Callable[[str], Any]]]' = None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends.py#L352)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L352?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.NumpyStorageBackend.empty" class="docs-object-method">&nbsp;</a> 
```python
empty(self, stype, num_elements, growth): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L359)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L359?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.NumpyStorageBackend.append" class="docs-object-method">&nbsp;</a> 
```python
append(self, raw, stype, value, filled_to, growth): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L405)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L405?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.NumpyStorageBackend.extend" class="docs-object-method">&nbsp;</a> 
```python
extend(self, raw, stype, values, filled_to, growth, prepend=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L414)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L414?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.NumpyStorageBackend.fill" class="docs-object-method">&nbsp;</a> 
```python
fill(self, raw, stype, values): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L428)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L428?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.NumpyStorageBackend.cast_to_array" class="docs-object-method">&nbsp;</a> 
```python
cast_to_array(self, raw, stype, txt): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L435)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L435?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.NumpyStorageBackend.view" class="docs-object-method">&nbsp;</a> 
```python
view(self, raw, filled_to): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L445)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L445?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.NumpyStorageBackend.add_axis" class="docs-object-method">&nbsp;</a> 
```python
add_axis(self, raw, stype): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L456)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L456?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.NumpyStorageBackend.set_item" class="docs-object-method">&nbsp;</a> 
```python
set_item(self, raw, stype, key, value, growth): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L459)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L459?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.NumpyStorageBackend.to_numpy" class="docs-object-method">&nbsp;</a> 
```python
to_numpy(self, raw, stype, allow_object=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L465)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L465?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StorageBackends.NumpyStorageBackend.is_ragged" class="docs-object-method">&nbsp;</a> 
```python
is_ragged(self, raw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L468)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/NumpyStorageBackend.py#L468?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/StorageBackends/NumpyStorageBackend.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/StorageBackends/NumpyStorageBackend.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/StorageBackends/NumpyStorageBackend.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/StorageBackends/NumpyStorageBackend.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L326?message=Update%20Docs)   
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