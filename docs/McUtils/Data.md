# <a id="McUtils.Data">McUtils.Data</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Data/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/__init__.py#L1?message=Update%20Docs)]
</div>
    
Provides a small data framework for wrapping up datasets into classes for access and loading.

The basic structure for a new dataset is defined in `CommonData.DataHandler`.
A simple, concrete example is in `AtomData.AtomData`.
A slightly more involved example is in `ConstantsData.UnitsData`.

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[DataHandler](McUtils/McUtils/Data/CommonData/DataHandler.md)   
</div>
   <div class="col" markdown="1">
[DataError](McUtils/McUtils/Data/CommonData/DataError.md)   
</div>
   <div class="col" markdown="1">
[DataRecord](McUtils/McUtils/Data/CommonData/DataRecord.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[AtomData](McUtils/McUtils/Data/AtomData/AtomData.md)   
</div>
   <div class="col" markdown="1">
[AtomDataHandler](McUtils/McUtils/Data/AtomData/AtomDataHandler.md)   
</div>
   <div class="col" markdown="1">
[UnitsData](McUtils/McUtils/Data/ConstantsData/UnitsData.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[UnitsDataHandler](McUtils/McUtils/Data/ConstantsData/UnitsDataHandler.md)   
</div>
   <div class="col" markdown="1">
[BondData](McUtils/McUtils/Data/BondData/BondData.md)   
</div>
   <div class="col" markdown="1">
[BondDataHandler](McUtils/McUtils/Data/BondData/BondDataHandler.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[WavefunctionData](McUtils/McUtils/Data/WavefunctionData/WavefunctionData.md)   
</div>
   <div class="col" markdown="1">
[PotentialData](McUtils/McUtils/Data/PotentialData/PotentialData.md)   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>





## Examples
We can work with atomic data. The key can be specified in multiple different ways.

```python
from McUtils.Data import AtomData

assert isinstance(AtomData["H"], dict)
assert isinstance(AtomData["Hydrogen"], dict)
assert isinstance(AtomData["Helium3"], dict)
assert AtomData["Hydrogen2"] is AtomData["Deuterium"]
assert AtomData["H2"] is AtomData["Deuterium"]
assert AtomData["H1"] is AtomData["Hydrogen"]
assert AtomData[8] is AtomData["Oxygen"]
```

A fun property of isotopes

```python
from McUtils.Data import AtomData

assert AtomData["Helium3", "Mass"] < AtomData["T"]["Mass"]
```

We can work with unit conversions. Inverse units are supplied using `"Inverse..."`, prefixes can modify units (e.g. `"Centi"`).

```python
from McUtils.Data import UnitsData

assert UnitsData.data[("Hartrees", "InverseMeters")]["Value"] > 21947463.13
assert UnitsData.data[("Hartrees", "InverseMeters")]["Value"] == UnitsData.convert("Hartrees", "InverseMeters")
assert UnitsData.convert("Hartrees", "Wavenumbers") == UnitsData.convert("Hartrees", "InverseMeters") / 100
assert UnitsData.convert("Hartrees", "Wavenumbers") == UnitsData.convert("Centihartrees", "InverseMeters")
```

Atomic units, as a general system, are supported

```python
from McUtils.Data import UnitsData

assert UnitsData.convert("AtomicMassUnits", "AtomicUnitOfMass") == UnitsData.convert("AtomicMassUnits", "ElectronMass")
assert UnitsData.convert("Wavenumbers", "AtomicUnitOfEnergy") == UnitsData.convert("Wavenumbers", "Hartrees")
```









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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Data.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Data.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Data.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Data.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Data/__init__.py#L1?message=Update%20Docs)   
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