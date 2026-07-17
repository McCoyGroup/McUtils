## <a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkDipoleNumDerivatives">FchkDipoleNumDerivatives</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L518)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L518?message=Update%20Docs)]
</div>

Holder class for numerical derivatives coming out of an fchk file.
Gaussian returns first and second derivatives







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkDipoleNumDerivatives.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, derivs, num_atoms=None, num_modes=None, reader=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L523)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L523?message=Update%20Docs)]
</div>
**LLM Docstring**

Hold the flattened numerical dipole derivatives (first and second) with respect
to the modes, optionally with the mode count.
  - `derivs`: `np.ndarray`
    > the flattened numerical derivatives
  - `num_atoms`: `int | None`
    > unused (kept for signature parity)
  - `num_modes`: `int | None`
    > the number of modes (inferred lazily if omitted)
  - `reader`: `object | None`
    > unused (kept for signature parity)


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkDipoleNumDerivatives.num_modes" class="docs-object-method">&nbsp;</a> 
```python
@property
num_modes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkDipoleNumDerivatives.py#L552)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkDipoleNumDerivatives.py#L552?message=Update%20Docs)]
</div>
**LLM Docstring**

The number of modes, inferred from the data length if not supplied.
  - `:returns`: `int`
    > the mode count


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkDipoleNumDerivatives.shape" class="docs-object-method">&nbsp;</a> 
```python
@property
shape(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkDipoleNumDerivatives.py#L563)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkDipoleNumDerivatives.py#L563?message=Update%20Docs)]
</div>
**LLM Docstring**

The shape of one derivative block, `(m, 3)`.
  - `:returns`: `tuple[int, int]`
    > the block shape


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkDipoleNumDerivatives.first_derivatives" class="docs-object-method">&nbsp;</a> 
```python
@property
first_derivatives(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkDipoleNumDerivatives.py#L574)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkDipoleNumDerivatives.py#L574?message=Update%20Docs)]
</div>
**LLM Docstring**

The first numerical dipole derivatives, reshaped to `(m, 3)`.
  - `:returns`: `np.ndarray`
    > the first-derivative array


<a id="McUtils.ExternalPrograms.Parsers.FChkDerivatives.FchkDipoleNumDerivatives.second_derivatives" class="docs-object-method">&nbsp;</a> 
```python
@property
second_derivatives(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkDipoleNumDerivatives.py#L585)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkDipoleNumDerivatives.py#L585?message=Update%20Docs)]
</div>
**LLM Docstring**

The second numerical dipole derivatives, reshaped to `(m, 3)`.
  - `:returns`: `np.ndarray`
    > the second-derivative array
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkDipoleNumDerivatives.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkDipoleNumDerivatives.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkDipoleNumDerivatives.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/FChkDerivatives/FchkDipoleNumDerivatives.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/FChkDerivatives.py#L518?message=Update%20Docs)   
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