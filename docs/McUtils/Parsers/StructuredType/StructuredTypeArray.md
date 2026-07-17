## <a id="McUtils.Parsers.StructuredType.StructuredTypeArray">StructuredTypeArray</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType.py#L354)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType.py#L354?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType.py#L368)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType.py#L368?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L394)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L394?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L402)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L402?message=Update%20Docs)]
</div>
**LLM Docstring**

Report whether compound storage is keyed by a dictionary or `OrderedDict`.
  - `:returns`: `bool`
    > `True` when the condition described above holds; otherwise `False`.


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.extension_axis" class="docs-object-method">&nbsp;</a> 
```python
@property
extension_axis(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L413)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L413?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L447)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L447?message=Update%20Docs)]
</div>
**LLM Docstring**

Get the filled shape of simple storage or the component shapes of compound storage; the setter stores an explicit cached shape.
  - `s`: `object`
    > the shape assigned to the object

  - `:returns`: `object`
    > The populated shape for simple storage or component shapes for compound storage.


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.block_size" class="docs-object-method">&nbsp;</a> 
```python
@property
block_size(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L490)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L490?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the number of scalar values in one element along the extension axis, summing component block sizes for compound storage.
  - `:returns`: `object`
    > return the number of scalar values in one element along the extension axis, summing component block sizes for compound storage.


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.append_depth" class="docs-object-method">&nbsp;</a> 
```python
@property
append_depth(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L507)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L507?message=Update%20Docs)]
</div>
**LLM Docstring**

Get or set recursive append depth; changing it propagates the same increment to all compound subarrays.
  - `d`: `object`
    > the new recursive append depth

  - `:returns`: `object`
    > get or set recursive append depth; changing it propagates the same increment to all compound subarrays.


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.dtype" class="docs-object-method">&nbsp;</a> 
```python
@property
dtype(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L597)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L597?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L613)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L613?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L626)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L626?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the filled slice of simple NumPy storage, or the complete tuple/mapping of compound subarrays.
  - `:returns`: `object`
    > The populated NumPy view or compound collection of populated subarrays.


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.axis_shape_indeterminate" class="docs-object-method">&nbsp;</a> 
```python
axis_shape_indeterminate(self, axis): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L659)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L659?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L671)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L671?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L694)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L694?message=Update%20Docs)]
</div>
**LLM Docstring**

Get per-axis populated extents for simple storage or nested extents for compound storage; setting accepts an integer or extent sequence only for simple storage.
  - `filling`: `object`
    > the populated extent or sequence of per-axis extents to record

  - `:returns`: `object`
    > The populated extent of each axis.


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.set_filling" class="docs-object-method">&nbsp;</a> 
```python
set_filling(self, amt, axis=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L745)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L745?message=Update%20Docs)]
</div>
**LLM Docstring**

Set one populated extent directly, propagating the update through compound children.
  - `amt`: `object`
    > the populated extent to assign

  - `axis`: `object`
    > the axis being inspected, changed, or extended

  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.increment_filling" class="docs-object-method">&nbsp;</a> 
```python
increment_filling(self, inc=1, axis=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L768)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L768?message=Update%20Docs)]
</div>
**LLM Docstring**

Increase one populated extent, propagating the increment through compound children.
  - `inc`: `object`
    > the amount added to the populated extent

  - `axis`: `object`
    > the axis being inspected, changed, or extended

  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L792)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L792?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the length of the currently filled array view.
  - `:returns`: `int`
    > The number of populated top-level elements.


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.empty_array" class="docs-object-method">&nbsp;</a> 
```python
empty_array(self, shape=None, num_elements=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L803)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L803?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L846)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L846?message=Update%20Docs)]
</div>
**LLM Docstring**

Grow storage by concatenating an equally shaped empty block along the extension axis, recursively growing compound children.
  - `axis`: `object`
    > the axis being inspected, changed, or extended

  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L876)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L876?message=Update%20Docs)]
</div>
**LLM Docstring**

Assign through `set_part`, including automatic growth and recursive compound dispatch.
  - `key`: `object`
    > the name assigned to a captured group

  - `value`: `object`
    > the value assigned into the structured array

  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.set_part" class="docs-object-method">&nbsp;</a> 
```python
set_part(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L892)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L892?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1016)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1016?message=Update%20Docs)]
</div>
**LLM Docstring**

Read through `get_part` from the filled array view rather than unused capacity.
  - `item`: `object`
    > the child key or array index/slice being accessed

  - `:returns`: `object`
    > The named child or populated array portion selected by the index.


<a id="McUtils.Parsers.StructuredType.StructuredTypeArray.get_part" class="docs-object-method">&nbsp;</a> 
```python
get_part(self, item, use_full_array=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1029)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1029?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1063)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1063?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1157)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1157?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1185)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1185?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1240)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1240?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1344)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1344?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1438)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1438?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1476)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType/StructuredTypeArray.py#L1476?message=Update%20Docs)]
</div>
**LLM Docstring**

Show the populated shape and resolved dtype.
  - `:returns`: `str`
    > The regex source or textual representation constructed by the operation.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StructuredType.py#L354?message=Update%20Docs)   
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