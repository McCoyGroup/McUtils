## <a id="McUtils.Parsers.StructuredType.StructuredTypeArray">StructuredTypeArray</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType.py#L269)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType.py#L269?message=Update%20Docs)]
</div>

Represents an array of objects defined by the StructuredType spec provided
mostly useful as it dispatches to NumPy where things are simple enough to do so

It has a system to dispatch intelligently based on the type of array provided
The kinds of structures supported are: OrderedDict, list, and np.ndarray

A _simple_ StructuredTypeArray is one that can just be represented as a single np.ndarray
A _compound_ StructuredTypeArray requires either a list or OrderedDict of StructuredTypeArray subarrays







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, stype, num_elements=50, padding_mode='fill', padding_value=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType.py#L283?message=Update%20Docs)]
</div>

  - `stype`: `StructuredType`
    > 
  - `num_elements`: `int`
    > number of default elements in dynamically sized arrays


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.is_simple" class="docs-object-method">&nbsp;</a> 
```python
@property
is_simple(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L309)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L309?message=Update%20Docs)]
</div>
Just returns wheter the core datatype is simple
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.dict_like" class="docs-object-method">&nbsp;</a> 
```python
@property
dict_like(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L317)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L317?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.extension_axis" class="docs-object-method">&nbsp;</a> 
```python
@property
extension_axis(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L320)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L320?message=Update%20Docs)]
</div>
Determines which axis to extend when adding more memory to the array
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L343)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L343?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.block_size" class="docs-object-method">&nbsp;</a> 
```python
@property
block_size(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L364)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L364?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.append_depth" class="docs-object-method">&nbsp;</a> 
```python
@property
append_depth(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L373)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L373?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.dtype" class="docs-object-method">&nbsp;</a> 
```python
@property
dtype(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L433)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L433?message=Update%20Docs)]
</div>
Returns the core data type held by the StructuredType that represents the array
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.stype" class="docs-object-method">&nbsp;</a> 
```python
@property
stype(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L449)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L449?message=Update%20Docs)]
</div>
Returns the StructuredType that the array holds data for
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.array" class="docs-object-method">&nbsp;</a> 
```python
@property
array(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L462)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L462?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.axis_shape_indeterminate" class="docs-object-method">&nbsp;</a> 
```python
axis_shape_indeterminate(self, axis): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L479)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L479?message=Update%20Docs)]
</div>
Tries to determine if an axis has had any data placed into it or otherwise been given a determined shape
  - `axis`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.has_indeterminate_shape" class="docs-object-method">&nbsp;</a> 
```python
@property
has_indeterminate_shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L491)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L491?message=Update%20Docs)]
</div>
Tries to determine if the entire array has a determined shape
  - `axis`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.filled_to" class="docs-object-method">&nbsp;</a> 
```python
@property
filled_to(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L514)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L514?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.set_filling" class="docs-object-method">&nbsp;</a> 
```python
set_filling(self, amt, axis=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L543)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L543?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.increment_filling" class="docs-object-method">&nbsp;</a> 
```python
increment_filling(self, inc=1, axis=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L552)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L552?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L562)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L562?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.empty_array" class="docs-object-method">&nbsp;</a> 
```python
empty_array(self, shape=None, num_elements=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L565)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L565?message=Update%20Docs)]
</div>
Creates empty arrays with (potentially) default elements

The shape handling rules operate like this:
if shape is None, we assume we'll initialize this as an array with a single element to be filled out
if shape is (None,) or (n,) we'll initialize this as an array with multiple elments to be filled out
otherwise we'll just take the specified shape
  - `num_elements`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.extend_array" class="docs-object-method">&nbsp;</a> 
```python
extend_array(self, axis=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L608)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L608?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L627)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L627?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.set_part" class="docs-object-method">&nbsp;</a> 
```python
set_part(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L629)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L629?message=Update%20Docs)]
</div>
Recursively sets parts of an array if not simple, otherwise just delegates to NumPy
  - `key`: `Any`
    > 
  - `value`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L753)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L753?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.get_part" class="docs-object-method">&nbsp;</a> 
```python
get_part(self, item, use_full_array=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L755)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L755?message=Update%20Docs)]
</div>
If simple, delegates to NumPy, otherwise tries to recursively get parts...?
Unclear how slicing is best handled here.
  - `item`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.add_axis" class="docs-object-method">&nbsp;</a> 
```python
add_axis(self, which=0, num_elements=None, change_shape=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L789)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L789?message=Update%20Docs)]
</div>
Adds an axis to the array, generally used for expanding from singular or 1D data to higher dimensional
This happens with parse_all and repeated things like that
  - `which`: `Any`
    > 
  - `num_elements`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.can_cast" class="docs-object-method">&nbsp;</a> 
```python
can_cast(self, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L883)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L883?message=Update%20Docs)]
</div>
Determines whether val can probably be cast to the right return type and shape without further processing or if that's definitely not possible
  - `val`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.append" class="docs-object-method">&nbsp;</a> 
```python
append(self, val, axis=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L911)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L911?message=Update%20Docs)]
</div>
Puts val in the first empty slot in the array
  - `val`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.extend" class="docs-object-method">&nbsp;</a> 
```python
extend(self, val, single=True, prepend=False, axis=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L952)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L952?message=Update%20Docs)]
</div>
Adds the sequence val to the array
  - `val`: `Any`
    > 
  - `single`: `bool`
    > a flag that indicates whether val can be treated as a single object or if it needs to be reshapen when handling in non-simple case
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.fill" class="docs-object-method">&nbsp;</a> 
```python
fill(self, array): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1056)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1056?message=Update%20Docs)]
</div>
Sets the result array to be the passed array
  - `array`: `str | np.ndarray`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.cast_to_array" class="docs-object-method">&nbsp;</a> 
```python
cast_to_array(self, txt): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1150)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1150?message=Update%20Docs)]
</div>
Casts a string of things with a given data type to an array of that type and does some optional
shape coercion
  - `txt`: `str | iterable[str]`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1188?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/StructuredType/StructuredTypeArray.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/StructuredType/StructuredTypeArray.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/StructuredType/StructuredTypeArray.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/StructuredType/StructuredTypeArray.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType.py#L269?message=Update%20Docs)   
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