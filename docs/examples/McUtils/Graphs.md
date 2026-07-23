**LLM Examples**

### Analyze a molecular graph

```python
from McUtils.Graphs import EdgeGraph

labels = ["C", "C", "O", "H", "H", "H", "H", "H", "H"]
edges = [(0, 1), (1, 2), (0, 3), (0, 4), (0, 5),
         (1, 6), (1, 7), (2, 8)]
ethanol = EdgeGraph(labels, edges)
print("C-to-O path:", ethanol.get_path(0, 2))
print("fragments:", ethanol.get_fragments(return_labels=True))
print("three-bond neighborhood:", list(ethanol.neighbor_iterator(0, num=3)))
```

### Detect rings and break a bond

```python
from McUtils.Graphs import EdgeGraph

benzene = EdgeGraph(["C"] * 6, [(i, (i + 1) % 6) for i in range(6)])
rings = benzene.get_rings()
opened = benzene.break_bonds([(0, 1)], return_single_graph=True)
assert len(rings) == 1
assert opened.get_path(0, 1) == (0, 5, 4, 3, 2, 1)
print("ring:", rings[0])
print("opened-chain distances:", opened.get_distances(0))
```

### Traverse nested scientific data

```python
from McUtils.Graphs import tree_iter
from McUtils.Iterators import riffle

workflow = {
    "optimize": {"geometry": {}, "energy": {}},
    "frequency": {"modes": {}, "intensities": {}}
}
for path, is_term in tree_iter(workflow, yield_paths='terminal', traversal_ordering="dfs"):
    print(*riffle(path, [" / "] * len(path)))
```

### Compare two labeled graphs

```python
from McUtils.Graphs import EdgeGraph

first = EdgeGraph(["O", "H", "H"], [(0, 1), (0, 2)])
second = EdgeGraph(["H", "O", "H"], [(1, 0), (1, 2)])
permutation = first.get_reindexing(second)
aligned = second.take(permutation)
print("alignment:", permutation, aligned.labels)
```

### Compute a graph layout and plot it

```python
from McUtils.Graphs import EdgeGraph

graph = EdgeGraph(list("ABCDEF"), [(0, 1), (1, 2), (2, 3),
                                    (3, 4), (4, 5), (5, 0), (0, 3)])
positions = graph.layout(method="kamada_kawai")
print("node positions:", positions)
figure = graph.plot(method="kamada_kawai")
figure.show()
```

### Test generic rigidity

```python
import numpy as np
from McUtils.Graphs import statistically_rigid

points = np.array([[0., 0.], [1., 0.], [0., 1.]])
edges = [(0, 1), (1, 2), (2, 0)]
rigid, (matrix, rank) = statistically_rigid(edges, ndim=2, points=points, return_rigidity_matrix=True)
print("rigidity-matrix rank:", rank, "rigid:", rigid)
```

### Molecular graphs

```python
import numpy as np
from McUtils.ExternalPrograms import RDMolecule
from McUtils.Coordinerds import CoordinateSet, CartesianCoordinates3D, ZMatrixCoordinates

mol = RDMolecule.from_smiles(
    "CC(O)C(=O)O", add_implicit_hydrogens=True,
    num_confs=20, optimize=True, take_min=True
)
graph = mol.get_edge_graph()
carts = CoordinateSet(mol.coords, system=CartesianCoordinates3D)
zmat = carts.convert(ZMatrixCoordinates)
round_trip = zmat.convert(CartesianCoordinates3D)

print("atoms:", mol.atoms)
print("rings:", graph.get_rings())
print("coordinate round-trip error:", np.linalg.norm(round_trip - carts))
mol.plot(image_size=(650, 450)).show()
```