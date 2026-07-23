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

### Complete symmetry breaking decomposition workflow

```python
from Psience.Molecools import Molecule
from McUtils.Plots import Sphere
import numpy as np
import McUtils.Numputils as nput
from McUtils.Data import AtomData, UnitsData
from McUtils.Symmetry import identify_point_group, symmetrized_coordinate_coefficients
from McUtils.Plots import Plot

atoms = ["O", "H", "H"]
eq = np.array([[0., 0., 0.], [0.758, 0., 0.504], [-0.758, 0., 0.504]])
masses = np.array([AtomData[a, "Mass"] for a in atoms])
displacements = np.linspace(0, 0.25, 31)

groups, asymmetry = [], []
pg0 = identify_point_group(eq, masses=masses, tol=1e-3)

# optional, show the point group elements in context
fig = pg0[1].plot()
for coord, col in zip(
    eq, [AtomData[a, "IconColor"] for a in atoms]
):
    Sphere(coord, .5, color=col).plot(fig)
fig.show()


# get symmetrized coordinates
symms = symmetrized_coordinate_coefficients(pg0[1], eq,
                                            merge_equivalents=True,
                                            as_characters=True,
                                            normalize=True,
                                            realign=False)
projector = nput.translation_rotation_projector(
    eq, masses, direction='reverse')
coords = projector @ np.concatenate(symms, axis=-1).T
coords = nput.find_basis(coords)

# optional, animate the symmetrized coordinates
mol = Molecule(
    atoms,
    eq * UnitsData.convert("Angstroms", "BohrRadius")
)
anim = mol.animate_coordinate(2,
                              coordinate_expansion=[coords.T],
                              view_settings={
                                  'right_vector': [1, 0, 0],
                                  'up_vector': [0, 0, -1],
                                  'view_distance': 3
                              })
anim.show()

# project a displacement onto the symmetry coordinate basis
groups, asymmetries = [], []
for dx in displacements:
    geom = eq.copy()
    geom[1, 0] += dx
    pg = identify_point_group(geom, masses=masses, tol=1e-3)
    groups.append(str(pg))
    asymmetry.append(np.dot((geom - eq).flatten(), coords))

print(list(zip(displacements[::10], groups[::10])))
asymmetries = np.moveaxis(asymmetry, -1, 0)
figure = None
for a in asymmetries:
    figure = Plot(displacements, a,
                 plot_label="symmetry-breaking",
                 axes_labels=["H displacement (Å)", "asymmetry (Å)"], figure=figure)
figure.show()
```