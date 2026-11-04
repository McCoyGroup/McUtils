Get all partitions of `3`

<!-- readout(id="mcutils-combinatorics-1", isolated=True) -->
```python
IntegerPartitioner.partitions(3)
```

Count the number of partitions up to 10

<!-- readout(id="mcutils-combinatorics-2", isolated=True) -->
```python
IntegerPartitioner.count_partitions(10)
```

Count the number of partitions of `4` of length exactly `2`
with minimum component between `2` and `4`

<!-- readout(id="mcutils-combinatorics-3", isolated=True) -->
```python
IntegerPartitioner.count_exact_length_partitions_in_range(4, 4, 2, 2)
```

Get all unique permutations of the first integer partition of 10

```python
lens, parts = IntegerPartitioner.partitions(10, pad=True, return_lens=True)
perms = UniquePermutations(parts[0]).permutations()
```

Get all 9D state vectors and indices for states with up to 4 quanta of excitation

<!-- readout(id="mcutils-combinatorics-5", isolated=True) -->
```python
SymmetricGroupGenerator(9).get_terms([1, 2, 3, 4])
```

**LLM Examples**

### Enumerate vibrational basis states

<!-- readout(id="mcutils-combinatorics-6", isolated=True, display="both") -->
```python
import numpy as np
from McUtils.Combinatorics import SymmetricGroupGenerator

generator = SymmetricGroupGenerator(4)
states = generator.get_terms([0, 1, 2, 3], flatten=True)
indices = generator.to_indices(states)
restored = generator.from_indices(indices)
assert np.array_equal(restored, states)
print("basis size:", len(states))
print("first excited states:", states[np.sum(states, axis=1) == 1])
```

### Rank and unrank multiset permutations

```python
import numpy as np
from McUtils.Combinatorics import UniquePermutations

space = UniquePermutations([3, 2, 2, 1])
permutations = space.permutations()
indices = space.index_permutations(permutations)
selected = space.permutations_from_indices([0, len(permutations) // 2, len(permutations) - 1])
assert len(permutations) == space.num_permutations()
assert np.array_equal(space.permutations_from_indices(indices), permutations)
print(selected)
```

### Generate standard Young tableaux

```python
from McUtils.Combinatorics import YoungTableauxGenerator

generator = YoungTableauxGenerator(5)
partition = [3, 2]
count = generator.count_standard_tableaux(partition)
tableaux = generator.standard_partition_tableaux(partition)
hooks = generator.hook_numbers(partition)
assert len(tableaux) == count
print("hook lengths:", hooks)
generator.print_tableaux(tableaux)
```

### Encode and decode arbitrary permutations

<!-- readout(id="mcutils-combinatorics-9", isolated=True, display="both") -->
```python
import numpy as np
from McUtils.Combinatorics import lehmer_encode, lehmer_decode

permutations = np.array([[0, 1, 2, 3], [3, 2, 1, 0], [1, 3, 0, 2]])
codes = lehmer_encode(permutations)
restored = lehmer_decode(4, codes)
assert np.array_equal(restored, permutations)
print("Lehmer codes:", codes)
```

### Generate low-discrepancy integration points

<!-- readout(id="mcutils-combinatorics-10", isolated=True, display="both") -->
```python
from McUtils.Combinatorics import halton_sequence, sobol_sequence

halton = halton_sequence(256, 3)
sobol = sobol_sequence(256, 3)
assert halton.shape == sobol.shape == (256, 3)
print("Halton centroid:", halton.mean(axis=0))
print("Sobol centroid:", sobol.mean(axis=0))
```

### Traverse lattice-path rules

```python
from McUtils.Combinatorics import LatticePathGenerator

paths = LatticePathGenerator([-1, 1], [-2, 0, 2], max_len=4)
tree = paths.tree
rules = paths.rules
endpoints = paths.get_path([1, -2])
print("reachable endpoints:", endpoints)
print("tree depth:", len(paths.subtrees))
```
