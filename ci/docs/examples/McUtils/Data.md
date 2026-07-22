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

**LLM Examples**

### Look up atomic and bond data

```python
from McUtils.Data import AtomData, BondData

for atom in ["H", "D", "C", "O"]:
    print(atom, "mass:", AtomData[atom, "Mass"])
oh_length = BondData["O", "H", 1]
co_length = BondData["C", "O", 2]
print("reference O-H length:", oh_length)
print("reference C=O length:", co_length)
```

### Convert spectroscopic units

```python
import numpy as np
from McUtils.Data import UnitsData

frequencies_hartree = np.array([.0054, .0167, .0171])
to_wavenumbers = UnitsData.convert("Hartrees", "Wavenumbers")
frequencies_cm = frequencies_hartree * to_wavenumbers
energies_ev = frequencies_hartree * UnitsData.convert("Hartrees", "ElectronVolts")
print("frequencies / cm^-1:", frequencies_cm)
print("energies / eV:", energies_ev)
```

### Estimate an isotope shift

```python
from McUtils.Data import AtomData

m_h = AtomData["Hydrogen", "Mass"]
m_d = AtomData["Deuterium", "Mass"]
m_o = AtomData["Oxygen", "Mass"]
mu_oh = m_h * m_o / (m_h + m_o)
mu_od = m_d * m_o / (m_d + m_o)
oh_frequency = 3657.0
od_frequency = oh_frequency * (mu_oh / mu_od) ** .5
print(f"estimated O-D frequency: {od_frequency:.1f} cm^-1")
```

### Inspect named colors

```python
from McUtils.Data import ColorData

for name in ["red", "navy", "forestgreen", "gold"]:
    try:
        print(name, ColorData[name])
    except KeyError:
        print(name, "is not present in this color table")
```

### Compare isotope records

```python
from McUtils.Data import AtomData, DataRecord

protium = AtomData["H1"]
deuterium = AtomData["H2"]
tritium = AtomData["T"]
assert all(isinstance(record, DataRecord) for record in [protium, deuterium, tritium])
print([record["Mass"] for record in [protium, deuterium, tritium]])
```

### Traverse a chain of unit conversions

```python
from McUtils.Data import UnitsData

hartree_to_ev = UnitsData.convert("Hartrees", "ElectronVolts")
ev_to_wavenumbers = UnitsData.convert("ElectronVolts", "Wavenumbers")
direct = UnitsData.convert("Hartrees", "Wavenumbers")
assert abs(hartree_to_ev * ev_to_wavenumbers - direct) < 1e-8
print("1 Eh =", direct, "cm^-1")
```


