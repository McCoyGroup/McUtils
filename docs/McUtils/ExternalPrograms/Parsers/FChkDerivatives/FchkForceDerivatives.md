## <a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceDerivatives">FchkForceDerivatives</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L111)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L111?message=Update%20Docs)]
</div>

Holder class for force constant derivatives coming out of an fchk file







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceDerivatives.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, derivs, num_atoms=None, num_modes=None, reader=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L113)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L113?message=Update%20Docs)]
</div>
**LLM Docstring**

Hold the flattened third/fourth force-constant derivative data, optionally with
the atom and mode counts (or a reader supplying the atom count).
  - `derivs`: `np.ndarray`
    > the flattened derivative data
  - `num_atoms`: `int | None`
    > the number of atoms (inferred lazily if omitted)
  - `num_modes`: `int | None`
    > the number of modes (inferred lazily if omitted)
  - `reader`: `object | None`
    > a reader from which to pull the atom count


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceDerivatives.__len__" class="docs-object-method">&nbsp;</a> 
```python
__len__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L139)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L139?message=Update%20Docs)]
</div>
**LLM Docstring**

The length of the raw flattened derivative data.
  - `:returns`: `int`
    > the number of stored values


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceDerivatives.n" class="docs-object-method">&nbsp;</a> 
```python
@property
n(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L185)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L185?message=Update%20Docs)]
</div>
**LLM Docstring**

The number of atoms, inferred from the data length if not supplied.
  - `:returns`: `int`
    > the atom count


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceDerivatives.num_modes" class="docs-object-method">&nbsp;</a> 
```python
@property
num_modes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L199)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L199?message=Update%20Docs)]
</div>
**LLM Docstring**

The number of modes, inferred from the data length if not supplied.
  - `:returns`: `int`
    > the mode count


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceDerivatives.third_derivs" class="docs-object-method">&nbsp;</a> 
```python
@property
third_derivs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L239)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L239?message=Update%20Docs)]
</div>
**LLM Docstring**

The raw third-derivative data.
  - `:returns`: `np.ndarray`
    > the third-derivative data


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceDerivatives.fourth_derivs" class="docs-object-method">&nbsp;</a> 
```python
@property
fourth_derivs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L251)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L251?message=Update%20Docs)]
</div>
**LLM Docstring**

The raw fourth-derivative data.
  - `:returns`: `np.ndarray`
    > the fourth-derivative data


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceDerivatives.third_deriv_array" class="docs-object-method">&nbsp;</a> 
```python
@property
third_deriv_array(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L297)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L297?message=Update%20Docs)]
</div>
**LLM Docstring**

The third derivatives as a full `(m, 3n, 3n)` tensor, symmetrized from the
lower-triangle data.
  - `:returns`: `np.ndarray`
    > the third-derivative tensor


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkForceDerivatives.fourth_deriv_array" class="docs-object-method">&nbsp;</a> 
```python
@property
fourth_deriv_array(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L320)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.py#L320?message=Update%20Docs)]
</div>
**LLM Docstring**

The fourth derivatives as a sparse tensor built from the diagonal elements
Gaussian provides.
  - `:returns`: `SparseArray`
    > the fourth-derivative tensor
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkForceDerivatives.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L111?message=Update%20Docs)   
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