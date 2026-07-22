**LLM Examples**

### Inspect a point-group character table

```python
from McUtils.Symmetry import CharacterTable

table = CharacterTable.point_group("Cv", 3)
print(table.format())
axis_rep = table.axis_representation()
decomposition = table.decompose_representation(axis_rep)
print("Cartesian-axis representation:", decomposition)
```

### Reduce the Cartesian modes of water

```python
import numpy as np
from McUtils.Symmetry import CharacterTable

water = np.array([[0, 0, .126], [1.437, 0, -.999], [-1.437, 0, -.999]])
c2v = CharacterTable.point_group("Cv", 2)
reduction = c2v.coordinate_mode_reduction(water)
assert np.allclose(reduction, [2, 0, 1, 0])
print("3N representation by irrep:", reduction)
```

### Generate symmetry operations

```python
import numpy as np
from McUtils.Symmetry import point_group_data

elements, classes = point_group_data("Cv", 4, prop="classes")
flat_classes = np.concatenate(classes)
assert sorted(flat_classes.tolist()) == list(range(len(elements)))
print("number of operations:", len(elements))
print("class sizes:", [len(c) for c in classes])
```

### Decompose a custom representation

```python
import numpy as np
from McUtils.Symmetry import CharacterTable

table = CharacterTable.point_group("Cv", 2)
representation = np.array([6., 0., 2., 0.])
multiplicities = table.decompose_representation(representation)
print("irrep multiplicities:", np.rint(multiplicities).astype(int))
```

### Compare common molecular point groups

```python
from McUtils.Symmetry import CharacterTable

for family, order in [("Cv", 3), ("Dh", 4), ("S", 4)]:
    table = CharacterTable.point_group(family, order)
    print(family, order, "irreps:", table.irrep_names)
for fixed in ["Td", "Oh"]:
    print(fixed, CharacterTable.point_group(fixed).table.shape)
```

### Identify symmetry-related coordinate modes

```python
import numpy as np
from McUtils.Symmetry import CharacterTable

ammonia = np.array([[0, 0, .2], [1, 0, -.3],
                    [-.5, .866, -.3], [-.5, -.866, -.3]])
c3v = CharacterTable.point_group("Cv", 3)
reduction = c3v.coordinate_mode_reduction(ammonia)
print("Cartesian-mode reduction:", np.rint(reduction).astype(int))
```
