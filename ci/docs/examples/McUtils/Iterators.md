**LLM Examples**

### Batch a stream of calculations

```python
from McUtils.Iterators import chunked, counts

jobs = [
    {"molecule": "water", "method": "HF"},
    {"molecule": "water", "method": "MP2"},
    {"molecule": "ammonia", "method": "HF"},
    {"molecule": "methane", "method": "CCSD(T)"}
]
print("jobs per molecule:", counts(job["molecule"] for job in jobs))
for batch_number, batch in enumerate(chunked(jobs, 2), 1):
    print("submitting batch", batch_number, batch)
```

### Flatten nested results while preserving records

```python
from McUtils.Iterators import flatten, delete_duplicates

results = [[("water", -76.1), ("water", -76.2)],
           [("ammonia", -56.2), [("methane", -40.4)]]]
records = list(flatten(results, atomic_types=(tuple,)))
molecules = list(delete_duplicates(record[0] for record in records))
energies = [record[1] for record in records]
print("molecules:", molecules)
print("energies:", energies)
```

### Traverse a Cartesian product in zigzag order

```python
from McUtils.Iterators import zigzag_product

temperatures = [200, 250, 300]
pressures = [1, 5, 10, 20]
scan = list(zigzag_product(temperatures, pressures))
for temperature, pressure in scan:
    print(f"T={temperature} K, P={pressure} bar")
```

### Transpose ragged result streams

```python
from McUtils.Iterators import transpose

rows = [["HF", -75.98, 12], ["MP2", -76.23], ["CCSD(T)", -76.24, 180]]
columns = transpose(rows, default=None, pad=True)
methods, energies, timings = columns
print(methods)
print(energies)
print(timings)
```

### Interleave atomic positions and footer info

```python
from McUtils.Iterators import riffle

atoms = ["O", "H", "H"]
coordinates = [[0, 0, 0], [.958, 0, 0], [-.240, .927, 0]]
joins = [">", ">>"]
records = zip(atoms, coordinates)
for block in riffle(records, joins):
    print(block)
```

### Find the first converged result

```python
from McUtils.Iterators import first

steps = [{"iteration": 1, "error": 1e-2},
         {"iteration": 2, "error": 8e-5},
         {"iteration": 3, "error": 4e-9},
         {"iteration": 4, "error": 4e-3},
         {"iteration": 15, "error": 4e-12}]
converged = first(steps, key=lambda step: step["error"] < 1e-6)
print("first converged iteration:", converged["iteration"])
```
