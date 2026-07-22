# <a id="McUtils.Iterators">McUtils.Iterators</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Iterators/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/__init__.py#L1?message=Update%20Docs)]
</div>
    
Useful little iteration tools

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[is_fixed_size](Iterators/core/is_fixed_size.md)   
</div>
   <div class="col" markdown="1">
[consume](Iterators/core/consume.md)   
</div>
   <div class="col" markdown="1">
[chunked](Iterators/core/chunked.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[take_lists](Iterators/core/take_lists.md)   
</div>
   <div class="col" markdown="1">
[split](Iterators/core/split.md)   
</div>
   <div class="col" markdown="1">
[split_by](Iterators/core/split_by.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[counts](Iterators/core/counts.md)   
</div>
   <div class="col" markdown="1">
[dict_diff](Iterators/core/dict_diff.md)   
</div>
   <div class="col" markdown="1">
[transpose](Iterators/core/transpose.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[riffle](Iterators/core/riffle.md)   
</div>
   <div class="col" markdown="1">
[flatten](Iterators/core/flatten.md)   
</div>
   <div class="col" markdown="1">
[first](Iterators/core/first.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[delete_duplicates](Iterators/core/delete_duplicates.md)   
</div>
   <div class="col" markdown="1">
[unique_product](Iterators/core/unique_product.md)   
</div>
   <div class="col" markdown="1">
[zigzag_product](Iterators/core/zigzag_product.md)   
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
# LLM Examples

## Batch a stream of calculations

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

## Flatten nested results while preserving records

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

## Traverse a Cartesian product in zigzag order

```python
from McUtils.Iterators import zigzag_product

temperatures = [200, 250, 300]
pressures = [1, 5, 10, 20]
scan = list(zigzag_product(temperatures, pressures))
for temperature, pressure in scan:
    print(f"T={temperature} K, P={pressure} bar")
```

## Transpose ragged result streams

```python
from McUtils.Iterators import transpose

rows = [["HF", -75.98, 12], ["MP2", -76.23], ["CCSD(T)", -76.24, 180]]
columns = transpose(rows, default=None, pad=True)
methods, energies, timings = columns
print(methods)
print(energies)
print(timings)
```

## Interleave atomic positions and footer info

```python
from McUtils.Iterators import riffle

atoms = ["O", "H", "H"]
coordinates = [[0, 0, 0], [.958, 0, 0], [-.240, .927, 0]]
joins = [">", ">>"]
records = zip(atoms, coordinates)
for block in riffle(records, joins):
    print(block)
```

## Find the first converged result

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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Iterators.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Iterators.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Iterators.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Iterators.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Iterators/__init__.py#L1?message=Update%20Docs)   
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