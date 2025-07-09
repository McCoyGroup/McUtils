# <a id="McUtils.Data">McUtils.Data</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Data/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Data/__init__.py#L1?message=Update%20Docs)]
</div>
    
Provides a small data framework for wrapping up datasets into classes for access and loading.

The basic structure for a new dataset is defined in `CommonData.DataHandler`.
A simple, concrete example is in `AtomData.AtomData`.
A slightly more involved example is in `ConstantsData.UnitsData`.

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[DataHandler](Data/CommonData/DataHandler.md)   
</div>
   <div class="col" markdown="1">
[DataError](Data/CommonData/DataError.md)   
</div>
   <div class="col" markdown="1">
[DataRecord](Data/CommonData/DataRecord.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[AtomData](Data/AtomData/AtomData.md)   
</div>
   <div class="col" markdown="1">
[AtomDataHandler](Data/AtomData/AtomDataHandler.md)   
</div>
   <div class="col" markdown="1">
[UnitsData](Data/ConstantsData/UnitsData.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[UnitsDataHandler](Data/ConstantsData/UnitsDataHandler.md)   
</div>
   <div class="col" markdown="1">
[BondData](Data/BondData/BondData.md)   
</div>
   <div class="col" markdown="1">
[BondDataHandler](Data/BondData/BondDataHandler.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[WavefunctionData](Data/WavefunctionData/WavefunctionData.md)   
</div>
   <div class="col" markdown="1">
[PotentialData](Data/PotentialData/PotentialData.md)   
</div>
   <div class="col" markdown="1">
[ColorData](Data/ColorData/ColorData.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
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















<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#Tests-1f2004" markdown="1"> Tests</a> <a class="float-right" data-toggle="collapse" href="#Tests-1f2004"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Tests-1f2004" markdown="1">
 - [AtomData](#AtomData)
- [AtomMasses](#AtomMasses)
- [Conversions](#Conversions)
- [AtomicUnits](#AtomicUnits)
- [BondData](#BondData)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#Setup-00c0be" markdown="1"> Setup</a> <a class="float-right" data-toggle="collapse" href="#Setup-00c0be"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Setup-00c0be" markdown="1">
 
Before we can run our examples we should get a bit of setup out of the way.
Since these examples were harvested from the unit tests not all pieces
will be necessary for all situations.

All tests are wrapped in a test class
```python
class DataTests(TestCase):
```

 </div>
</div>

#### <a name="AtomData">AtomData</a>
```python
    def test_AtomData(self):
        self.assertIsInstance(AtomData["H"], DataRecord)
        self.assertIsInstance(AtomData["Hydrogen"], DataRecord)
        self.assertIsInstance(AtomData["Helium3"], DataRecord)
        self.assertIs(AtomData["Hydrogen2"], AtomData["Deuterium"])
        self.assertIs(AtomData["H2"], AtomData["Deuterium"])
        self.assertIs(AtomData["H1"], AtomData["Hydrogen"])
        self.assertIs(AtomData[8], AtomData["Oxygen"])
```

#### <a name="AtomMasses">AtomMasses</a>
```python
    def test_AtomMasses(self):
        self.assertLess(AtomData["Helium3", "Mass"], AtomData["T"]["Mass"])
```

#### <a name="Conversions">Conversions</a>
```python
    def test_Conversions(self):
        # print(AtomData["T"]["Mass"]-AtomData["Helium3", "Mass"], file=sys.stderr)
        self.assertGreater(UnitsData.data[("Hartrees", "InverseMeters")]["Value"], 21947463.13)
        self.assertLess(UnitsData.data[("Hartrees", "InverseMeters")]["Value"], 21947463.14)
        self.assertAlmostEqual(
            UnitsData.convert("Hartrees", "Wavenumbers"),
            UnitsData.convert("Hartrees", "InverseMeters") / 100
        )
        self.assertAlmostEqual(
            UnitsData.convert("Hartrees", "Wavenumbers"),
            UnitsData.convert("Centihartrees", "InverseMeters")
        )
```

#### <a name="AtomicUnits">AtomicUnits</a>
```python
    def test_AtomicUnits(self):
        # print(UnitsData["AtomicUnitOfMass"])
        self.assertAlmostEqual(UnitsData.convert("AtomicMassUnits", "AtomicUnitOfMass"), 1822.888486217313)
```

#### <a name="BondData">BondData</a>
```python
    def test_BondData(self):
        self.assertIsInstance(BondData["H"], dict)
        self.assertLess(BondData["H", "H", 1], 1)
        self.assertLess(BondData["H", "O", 1], 1)
        self.assertGreater(BondData["H", "C", 1], 1)
```

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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Data.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Data.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Data.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Data.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Data/__init__.py#L1?message=Update%20Docs)   
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