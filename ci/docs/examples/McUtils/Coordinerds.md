**LLM Examples**

### Convert Cartesian coordinates to a Z-matrix and back

```python
import numpy as np
from McUtils.Coordinerds import CoordinateSet, CartesianCoordinates3D, ZMatrixCoordinates

water = CoordinateSet([[0, 0, 0], [.958, 0, 0], [-.240, .927, 0]],
                      system=CartesianCoordinates3D)
ordering = [[0, -1, -1, -1], [1, 0, -1, -1], [2, 0, 1, -1]]
internals = water.convert(ZMatrixCoordinates, ordering=ordering)
rebuilt = internals.convert(CartesianCoordinates3D)
print("bond lengths and angle:", internals)
assert np.allclose(rebuilt, water)
```

### Convert a batch of geometries

```python
import numpy as np
from McUtils.Coordinerds import CoordinateSet, CartesianCoordinates3D, ZMatrixCoordinates

base = np.array([[0, 0, 0], [.958, 0, 0], [-.240, .927, 0]])
trajectory = np.stack([base, base * 1.01, base * .99])
coords = CoordinateSet(trajectory, system=CartesianCoordinates3D)
ordering = [[0, -1, -1, -1], [1, 0, -1, -1], [2, 0, 1, -1]]
internal_trajectory = coords.convert(ZMatrixCoordinates, ordering=ordering)
print("trajectory shape:", internal_trajectory.shape)
print("O-H distances:", internal_trajectory[:, 0, 0])
```

### Use the convenience conversion interface

```python
import numpy as np
from McUtils.Coordinerds import cartesian_to_zmatrix, zmatrix_to_cartesian

coords = np.array([[0, 0, 0], [1.2, 0, 0], [0.1, 1.0, 0], [0.2, .3, 1.1]])
zmatrix = cartesian_to_zmatrix(coords)
restored = zmatrix_to_cartesian(zmatrix.coords,
                                origins=zmatrix.origins, axes=zmatrix.axes)
pair_dists = np.linalg.norm(coords[:, None] - coords[None, :], axis=-1)
restored_dists = np.linalg.norm(restored[:, None] - restored[None, :], axis=-1)
assert np.allclose(pair_dists, restored_dists)
assert np.allclose(restored, coords)
```

### Canonicalize internal-coordinate specifications

```python
from McUtils.Coordinerds import canonicalize_internal

specs = [(0, 1), (2, 1, 0), (3, 2, 1, 0)]
canonical = [canonicalize_internal(spec) for spec in specs]
for original, normalized in zip(specs, canonical):
    print(original, "->", normalized)
```

### Generate primitive coordinates from a bond graph

```python
from McUtils.Coordinerds import PrimitiveCoordinatePicker

atoms = ["C", "C", "O", "H", "H", "H", "H", "H", "H"]
bonds = [(0, 1), (1, 2), (0, 3), (0, 4), (0, 5),
         (1, 6), (1, 7), (2, 8)]
picker = PrimitiveCoordinatePicker(atoms, bonds)
coordinates = picker.coords
print("primitive coordinates:", len(coordinates))
print(coordinates[:10])
```

### Reindex a Z-matrix ordering

```python
import numpy as np
from McUtils.Coordinerds import reindex_zmatrix

ordering = np.array([[0, -1, -1, -1], [1, 0, -1, -1],
                     [2, 0, 1, -1], [3, 2, 0, 1]])
permutation = np.array([0, 2, 1, 3])
reindexed = reindex_zmatrix(ordering, permutation)
print(reindexed)
```
