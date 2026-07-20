### `AtomData.py` — Provides a class for handling a compiled set of atomic data
  - **class `AtomDataHandler`** (DataHandler)
    > A DataHandler that's built for use with the atomic data we've collected.
    > Usually used through the `AtomData` object.
    - `__init__()`
    - `load()`

### `BondData.py`
  - **class `BondDataHandler`** (DataHandler)
    > A DataHandler that's built for use with the bond data we've collected.
    > Usually used through the `BondData` object.
    - `__init__()`
    - `load()`
    - `get_distance(key, default=None)`

### `ColorData.py`
  - **class `ColorDataHandler`** (DataHandler)
    - `__init__()`

### `CommonData.py` — Defines a common data handler
  - **class `DataError`** (KeyError)
    > Exception subclass for data error
  - **class `DataHandler`**
    > Defines a general data loader class that we can use for `AtomData` and any other data classes we might find useful.
    - `__init__(data_name, data_key=None, source_key=None, data_dir=None, data_pkg=None, alternate_keys=None, getter=None, record_type=None)`
    - `data_file()`
    - `load(env=None)` — Actually loads the data from `data_file`.
    - `data()`
    - `source()`
  - **class `DataRecord`**
    > Represents an individual record that might be accessed from a `DataHandler`.
    > Implements _most_ of the `dict` interface, but, to make things a bit easier when
    > pickling, is not implemented as a proper subclass of `dict`.
    - `__init__(data_handler, key, records)`
    - `keys()`
    - `values()`
    - `items()`

### `ConstantsData.py` — Provides constants data and conversions between units and unit systems
  - **class `ConversionError`** (Exception)
  - **class `UnitGraph`**
    - `__init__(stuff_to_update=())`
    - `add(node, connection)`
    - `update(iterable)`
    - `keys()`
    - `find_path_bfs(start, end)`
  - **class `UnitsDataHandler`** (DataHandler)
    > A DataHandler that's built for use with the units data we've collected.
    > Usually used through the `UnitsData` object.
    - `__init__()`
    - `load()`
    - `expand_conversions(unit_stuff_1)`
    - `find_conversion(unit, target)` — Attempts to find a conversion between two sets of units.
    - `add_conversion(unit, target, value)`
    - `convert(unit, target)` — Converts base unit into target using the scraped NIST data
    - `constants()`
    - `constant(const)` — Converts base unit into target using the scraped NIST data
    - `hartrees_to_wavenumbers()`
    - `bohr_to_angstroms()`
    - `amu_to_me()`
    - `moles()`

### `PotentialData.py`
  - **class `PotentialDataHandler`** (DataHandler)
    - `__init__()`
  - **class `PotentialDataRecord`** (DataRecord)
    > Represents a simple callable wavefunction...
    - `__init__(data_handler, key, records)`

### `QuantityArray.py` — Provides a QuantityArray class to manage data & units simultaneously
  - **class `QuantityArrayException`** (Exception)
  - **class `QuantityArray`**
    > A little helper for working with NumPy arrays with units.
    > It's mostly just a safety mechanism for imported data, but also helps keep you from messing up when you
    >   do addition and multiplication and stuff.
    - `__init__(array, units)`
    - `shape()`
    - `dtype()`
    - `raise_unit_mismatch(u1, u2)`
    - `convert(units)` — Converts the array from units A to units B
    - `save(file)` — Saves the QuantityArray to a file
    - `load(file)` — Loads a QuantityArray from file
    - `format_header()`
    - `parse_header(line)`
    - `savetxt(file)` — Saves the QuantityArray to a text file
    - `loadtxt(file)` — Loads a QuantityArray from a text file

### `WavefunctionData.py`
  - **class `WavefunctionDataHandler`** (DataHandler)
    - `__init__()`
  - **class `WavefunctionDataRecord`** (DataRecord)
    > Represents a simple callable wavefunction...

### `TheRealMcCoy/PotentialData.py`
- `harmonic(r, *, re=1, freq=1, mass=1, deriv_order=None)`
- `morse(r, *, re=1, De=1, alpha=1, deriv_order=None)`