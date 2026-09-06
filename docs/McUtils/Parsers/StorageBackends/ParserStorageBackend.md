## <a id="McUtils.Parsers.StorageBackends.ParserStorageBackend">ParserStorageBackend</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends.py#L210)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L210?message=Update%20Docs)]
</div>

Everything `StructuredTypeArray` needs from "somewhere to put simple
(non-compound) data". A backend instance is stateless -- all mutable
state lives in the opaque `raw` object it hands back from `empty()`
and mutates in place (or replaces, for backends where that's cheaper).

`StructuredTypeArray` is responsible for the *shape/dtype calculus*
(knowing what shape a `Number, shape=(None, 3)` stype implies, deciding
when to recurse into compound children, tracking `filled_to`); a
backend only ever sees "make me room for N more things of this dtype"
and "here is one (or more) matched string(s) or values, put them in."







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
name: str
```
<a id="McUtils.Parsers.StorageBackends.ParserStorageBackend.register" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
register(cls, name: 'str', factory: "Callable[[], 'ParserStorageBackend']" = None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L236)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L236?message=Update%20Docs)]
</div>
Register a backend under `name` so it can be selected by string
from `StringParser(regex, backend=name)` /
`StructuredTypeArray(stype, backend=name)`, the same as the two
built-in backends. `factory` is a zero-arg callable returning a
fresh `ParserStorageBackend` instance (fresh, so state like
`cast_failures` isn't shared across unrelated arrays).


<a id="McUtils.Parsers.StorageBackends.ParserStorageBackend.resolve" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve(cls, backend) -> "'ParserStorageBackend'": 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L252)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L252?message=Update%20Docs)]
</div>
Accepts a backend name (``'numpy'``/``'python'``), a
`ParserStorageBackend` instance (returned as-is), or `None`
(defaults to ``'numpy'``).


<a id="McUtils.Parsers.StorageBackends.ParserStorageBackend.empty" class="docs-object-method">&nbsp;</a> 
```python
empty(self, stype, num_elements: 'int', growth: 'GrowthPolicy'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L272)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L272?message=Update%20Docs)]
</div>
Allocate a fresh, empty raw container sized for `num_elements`.


<a id="McUtils.Parsers.StorageBackends.ParserStorageBackend.append" class="docs-object-method">&nbsp;</a> 
```python
append(self, raw, stype, value, filled_to: 'List[int]', growth: 'GrowthPolicy'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L276)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L276?message=Update%20Docs)]
</div>
Append a single (possibly nested) value; grow if needed.

Returns `(new_raw, new_filled_to)`.


<a id="McUtils.Parsers.StorageBackends.ParserStorageBackend.extend" class="docs-object-method">&nbsp;</a> 
```python
extend(self, raw, stype, values: 'Sequence', filled_to: 'List[int]', growth: 'GrowthPolicy', prepend: 'bool' = False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L283?message=Update%20Docs)]
</div>
Append a whole block of values at once. Returns `(new_raw, new_filled_to)`.


<a id="McUtils.Parsers.StorageBackends.ParserStorageBackend.fill" class="docs-object-method">&nbsp;</a> 
```python
fill(self, raw, stype, values): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L287?message=Update%20Docs)]
</div>
Replace the raw container's contents wholesale. Returns `(new_raw, new_filled_to)`.


<a id="McUtils.Parsers.StorageBackends.ParserStorageBackend.cast_to_array" class="docs-object-method">&nbsp;</a> 
```python
cast_to_array(self, raw, stype, txt: 'str'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L291)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L291?message=Update%20Docs)]
</div>
Parse a raw regex-matched string into this backend's native array form.


<a id="McUtils.Parsers.StorageBackends.ParserStorageBackend.view" class="docs-object-method">&nbsp;</a> 
```python
view(self, raw, filled_to: 'List[int]'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L295)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L295?message=Update%20Docs)]
</div>
Return the externally-visible `.array` view (trimmed to `filled_to`).


<a id="McUtils.Parsers.StorageBackends.ParserStorageBackend.add_axis" class="docs-object-method">&nbsp;</a> 
```python
add_axis(self, raw, stype): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L299)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L299?message=Update%20Docs)]
</div>
Wrap `raw` in one more outer axis. Returns new `raw`.


<a id="McUtils.Parsers.StorageBackends.ParserStorageBackend.set_item" class="docs-object-method">&nbsp;</a> 
```python
set_item(self, raw, stype, key, value, growth: 'GrowthPolicy'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L303)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L303?message=Update%20Docs)]
</div>
`arr[key] = value`, growing as needed. Returns new `raw`.


<a id="McUtils.Parsers.StorageBackends.ParserStorageBackend.to_numpy" class="docs-object-method">&nbsp;</a> 
```python
to_numpy(self, raw, stype, allow_object: 'bool' = True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L307)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L307?message=Update%20Docs)]
</div>
Best-effort conversion to `numpy.ndarray`; default just tries `np.asarray`.


<a id="McUtils.Parsers.StorageBackends.ParserStorageBackend.is_ragged" class="docs-object-method">&nbsp;</a> 
```python
is_ragged(self, raw) -> 'bool': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L319)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends/ParserStorageBackend.py#L319?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/StorageBackends/ParserStorageBackend.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/StorageBackends/ParserStorageBackend.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/StorageBackends/ParserStorageBackend.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/StorageBackends/ParserStorageBackend.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StorageBackends.py#L210?message=Update%20Docs)   
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