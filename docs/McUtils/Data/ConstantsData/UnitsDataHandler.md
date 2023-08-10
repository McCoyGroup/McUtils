## <a id="McUtils.Data.ConstantsData.UnitsDataHandler">UnitsDataHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/ConstantsData.py#L61)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/ConstantsData.py#L61?message=Update%20Docs)]
</div>

A DataHandler that's built for use with the units data we've collected.
Usually used through the `UnitsData` object.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
prefix_map: OrderedDict
postfix_map: OrderedDict
Wavenumbers: str
Hartrees: str
Angstroms: str
BohrRadius: str
ElectronMass: str
AtomicMassUnits: str
```
<a id="McUtils.Data.ConstantsData.UnitsDataHandler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/ConstantsData/UnitsDataHandler.py#L85)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/ConstantsData/UnitsDataHandler.py#L85?message=Update%20Docs)]
</div>


<a id="McUtils.Data.ConstantsData.UnitsDataHandler.load" class="docs-object-method">&nbsp;</a> 
```python
load(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/ConstantsData/UnitsDataHandler.py#L89)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/ConstantsData/UnitsDataHandler.py#L89?message=Update%20Docs)]
</div>


<a id="McUtils.Data.ConstantsData.UnitsDataHandler.find_conversion" class="docs-object-method">&nbsp;</a> 
```python
find_conversion(self, unit, target): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/ConstantsData/UnitsDataHandler.py#L369)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/ConstantsData/UnitsDataHandler.py#L369?message=Update%20Docs)]
</div>
Attempts to find a conversion between two sets of units. Currently only implemented for "plain" units.
  - `unit`: `Any`
    > 
  - `target`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Data.ConstantsData.UnitsDataHandler.add_conversion" class="docs-object-method">&nbsp;</a> 
```python
add_conversion(self, unit, target, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/ConstantsData/UnitsDataHandler.py#L392)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/ConstantsData/UnitsDataHandler.py#L392?message=Update%20Docs)]
</div>


<a id="McUtils.Data.ConstantsData.UnitsDataHandler.convert" class="docs-object-method">&nbsp;</a> 
```python
convert(self, unit, target): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/ConstantsData/UnitsDataHandler.py#L396)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/ConstantsData/UnitsDataHandler.py#L396?message=Update%20Docs)]
</div>
Converts base unit into target using the scraped NIST data
  - `unit`: `Any`
    > 
  - `target`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Data.ConstantsData.UnitsDataHandler.hartrees_to_wavenumbers" class="docs-object-method">&nbsp;</a> 
```python
@property
hartrees_to_wavenumbers(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/ConstantsData/UnitsDataHandler.py#L428)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/ConstantsData/UnitsDataHandler.py#L428?message=Update%20Docs)]
</div>


<a id="McUtils.Data.ConstantsData.UnitsDataHandler.bohr_to_angstroms" class="docs-object-method">&nbsp;</a> 
```python
@property
bohr_to_angstroms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/ConstantsData/UnitsDataHandler.py#L431)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/ConstantsData/UnitsDataHandler.py#L431?message=Update%20Docs)]
</div>


<a id="McUtils.Data.ConstantsData.UnitsDataHandler.amu_to_me" class="docs-object-method">&nbsp;</a> 
```python
@property
amu_to_me(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/ConstantsData/UnitsDataHandler.py#L434)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/ConstantsData/UnitsDataHandler.py#L434?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Data/ConstantsData/UnitsDataHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Data/ConstantsData/UnitsDataHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Data/ConstantsData/UnitsDataHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Data/ConstantsData/UnitsDataHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/ConstantsData.py#L61?message=Update%20Docs)   
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