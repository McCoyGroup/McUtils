## <a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceConstants">FchkForceConstants</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L15?message=Update%20Docs)]
</div>

Holder class for force constants coming out of an fchk file.
Allows us to construct the force constant matrix in lazy fashion if we want.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceConstants.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, fcs, num_atoms=None, reader=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L20?message=Update%20Docs)]
</div>
**LLM Docstring**

Hold the flattened force-constant (lower-triangle) data, optionally with the atom
count (or a reader that can supply it).
  - `fcs`: `np.ndarray`
    > the flattened lower-triangle force constants
  - `num_atoms`: `int | None`
    > the number of atoms (inferred lazily if omitted)
  - `reader`: `object | None`
    > a reader from which to pull the atom count


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceConstants.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceConstants.py#L43)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceConstants.py#L43?message=Update%20Docs)]
</div>
**LLM Docstring**

The length of the raw flattened force-constant data.
  - `:returns`: `int`
    > the number of stored values


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceConstants.n" class="docs-object-method">&nbsp;</a> 
```python
@property
n(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceConstants.py#L63)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceConstants.py#L63?message=Update%20Docs)]
</div>
**LLM Docstring**

The number of atoms, inferred from the data length if not supplied.
  - `:returns`: `int`
    > the atom count


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceConstants.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceConstants.py#L74)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceConstants.py#L74?message=Update%20Docs)]
</div>
**LLM Docstring**

The shape of the full force-constant matrix, `(3n, 3n)`.
  - `:returns`: `tuple[int, int]`
    > the matrix shape


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceConstants.array" class="docs-object-method">&nbsp;</a> 
```python
@property
array(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceConstants.py#L97)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceConstants.py#L97?message=Update%20Docs)]
</div>
**LLM Docstring**

The full, symmetrized `(3n, 3n)` force-constant matrix reconstructed from the
lower-triangle data.
  - `:returns`: `np.ndarray`
    > the force-constant matrix
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceConstants.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceConstants.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceConstants.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceConstants.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L15?message=Update%20Docs)   
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