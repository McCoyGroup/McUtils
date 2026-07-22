# LLM Examples

These examples focus on the heavily reused vector, geometry, transformation, and sparse-array APIs.

## Build molecular coordinate frames

```python
import numpy as np
from McUtils.Numputils import vec_crosses, view_matrix

o, h1, h2 = np.array([[0, 0, 0], [.958, 0, 0], [-.240, .927, 0]])
frame = view_matrix(view_vector=h1 - o, up_vector=h2 - o)
local_coords = (np.stack([o, h1, h2]) - o) @ frame
assert np.allclose(frame @ frame.T, np.eye(3))
print(local_coords)
```

## Apply and invert a rigid transformation

```python
import numpy as np
from McUtils.Numputils import rotation_matrix, affine_matrix

coords = np.array([[0., 0., 0.], [1., 0., 0.], [0., 1., 0.]])
rotation = rotation_matrix([0, 0, 1], np.pi / 3)
translation = np.array([2., -1., .5])
transform = affine_matrix(rotation, translation)
homogeneous = np.pad(coords, ((0, 0), (0, 1)), constant_values=1)
moved = (transform @ homogeneous.T).T[:, :3]
restored = (np.linalg.inv(transform) @ np.pad(moved, ((0, 0), (0, 1)), constant_values=1).T).T[:, :3]
assert np.allclose(restored, coords)
```

## Store a block-sparse operator

```python
import numpy as np
from McUtils.Numputils import SparseArray

diagonal = np.arange(1., 7.)
operator = SparseArray.from_diag(diagonal)
vector = np.ones(6)
result = operator.asarray() @ vector
subblock = operator[:3, :3].asarray()
assert np.allclose(result, diagonal)
assert np.allclose(subblock, np.diag(diagonal[:3]))
print("sparse shape:", operator.shape)
```

## Measure batched molecular geometry

```python
import numpy as np
from McUtils.Numputils import pts_norms, pts_angles, pts_dihedrals

trajectory = np.random.default_rng(3).normal(size=(100, 4, 3))
bond = pts_norms(trajectory[:, 0], trajectory[:, 1])
angle = pts_angles(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2])
dihedral = pts_dihedrals(trajectory[:, 0], trajectory[:, 1],
                         trajectory[:, 2], trajectory[:, 3])
print(bond.mean(), np.degrees(angle).mean(), np.degrees(dihedral).std())
```

## Rotate vectors between directions

```python
import numpy as np
from McUtils.Numputils import vec_normalize, rotation_matrix

source = vec_normalize(np.array([1., 1., 0.]))
axis = np.array([0., 0., 1.])
rotation = rotation_matrix(axis, np.pi / 4)
target = source @ rotation
assert np.allclose(np.linalg.norm(target), 1)
print("rotated vector:", target)
# rotate directly from axis to target
rotation = rotation_matrix(source, target)
target2 = source @ rotation
assert np.allclose(target2, target)
```

## Deduplicate rows with vectorized set operations

```python
import numpy as np
from McUtils.Numputils import unique

states = np.array([[0, 1], [1, 0], [0, 1], [2, 0], [1, 0]])
distinct, sorting, first, inverse = unique(states, axis=0, return_index=True, return_inverse=True)
assert np.array_equal(distinct[inverse], states)
print("distinct states:", distinct)
print("first positions:", first)
```
