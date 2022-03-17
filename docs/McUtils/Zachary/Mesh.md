# <a id="McUtils.Zachary.Mesh">McUtils.Zachary.Mesh</a>
    
Represents an n-dimensional grid, used by Interpolator and (eventually) FiniteDifferenceFunction to automatically
know what kind of data is fed in

### Members

<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[Mesh](Mesh/Mesh.md)   
</div>
   <div class="col" markdown="1">
[MeshType](Mesh/MeshType.md)   
</div>
</div>
</div>

### Examples

## Examples


### Unit Tests


<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#tests">Tests</a> <a class="float-right" data-toggle="collapse" href="#tests"><i class="fa fa-chevron-down"></i></a>
 </div>
<div class="collapsible-section collapsible-section-body collapse show" id="tests" markdown="1">

- [LinSpaceMesh](#LinSpaceMesh)
- [MeshGridMesh](#MeshGridMesh)
- [StructuredMesh](#StructuredMesh)
- [UnstructuredMesh](#UnstructuredMesh)
- [RegularMesh](#RegularMesh)
- [RegMeshSubgrids](#RegMeshSubgrids)
- [SemiStructuredMesh](#SemiStructuredMesh)
- [MeshFromList](#MeshFromList)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
#### <a class="collapse-link" data-toggle="collapse" href="#test-setup">Setup</a> <a class="float-right" data-toggle="collapse" href="#test-setup"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse" id="test-setup" markdown="1">

Before we can run our examples we should get a bit of setup out of the way.
Since these examples were harvested from the unit tests not all pieces
will be necessary for all situations.
```python
try:
    from Peeves.TestUtils import *
    from Peeves import BlockProfiler
except:
    pass
from unittest import TestCase
from McUtils.Zachary import *
from McUtils.Zachary.Taylor.ZachLib import *
from McUtils.Plots import *
from McUtils.Data import *
import McUtils.Numputils as nput
from McUtils.Parallelizers import *
from McUtils.Scaffolding import Logger
import sys, h5py, math, numpy as np, itertools
```

All tests are wrapped in a test class
```python
class ZacharyTests(TestCase):
    def setUp(self):
        self.save_data = TestManager.data_gen_tests
    def __getstate__(self):
        return {}
    def __setstate__(self, state):
        pass
    def get_error(self, ref_vals, vals):
        err = np.abs(vals - ref_vals)
        cum_err = np.linalg.norm(err.flatten())
        max_err = np.max(err.flatten())
        mean_err = np.average(err.flatten())
        return err, cum_err, max_err, mean_err
    def plot_err(self, grid, ref_vals, vals, errs):
        if grid.ndim == 1:
            Plot(grid, ref_vals, figure=Plot(grid, vals))
            Plot(grid, errs[0]).show()
        elif grid.ndim == 3:
            g = (grid[:, :, 0], grid[:, :, 1])
            gg = GraphicsGrid(nrows=2, ncols=2)
            gg[0, 0] = ContourPlot(*g, ref_vals, figure=gg[0, 0])
            gg[1, 0] = ContourPlot(*g, vals, figure=gg[1, 0])
            gg[1, 1] = ContourPlot(*g, errs[0], figure=gg[1, 1])
            gg[0, 0].tight_layout()
            gg.show()
    def print_error(self, n, order, errs):
        print(
            "Order: {}.{}\nCumulative Error: {}\nMax Error: {}\nMean Error: {}".format(n, order, *errs[1:])
        )
    class harmonically_coupled_morse:
        # mass_weights = masses[:2] / np.sum(masses[:2])
        def __init__(self,
                     De_1, a_1, re_1,
                     De_2, a_2, re_2,
                     kb, b_e
                     ):
            self.De_1 = De_1
            self.a_1 = a_1
            self.re_1 = re_1
            self.De_2 = De_2
            self.a_2 = a_2
            self.re_2 = re_2
            self.kb = kb
            self.b_e = b_e

        def __call__(self, carts):
            v1 = carts[..., 1, :] - carts[..., 0, :]
            v2 = carts[..., 2, :] - carts[..., 0, :]
            r1 = nput.vec_norms(v1) - self.re_1
            r2 = nput.vec_norms(v2) - self.re_2
            bend, _ = nput.vec_angles(v1, v2)
            bend = bend - self.b_e

            return (
                    self.De_1 * (1 - np.exp(-self.a_1 * r1)) ** 2
                    + self.De_2 * (1 - np.exp(-self.a_2 * r2)) ** 2
                    + self.kb * bend**2
            )
```

 </div>
</div>

#### <a name="LinSpaceMesh">LinSpaceMesh</a>
```python
    def test_LinSpaceMesh(self):
        mg = Mesh(np.linspace(-1, 1, 3))
        self.assertIs(mg.mesh_type, MeshType.Structured)
        self.assertEquals(mg.shape, (3,))
```
#### <a name="MeshGridMesh">MeshGridMesh</a>
```python
    def test_MeshGridMesh(self):
        mg = np.array(np.meshgrid(np.array([-1, 0, 1]), np.array([-1, 0, 1]), indexing='ij'))
        regmesh = Mesh(mg)
        self.assertIs(regmesh.mesh_type, MeshType.Regular)
        self.assertEquals(regmesh.shape, (3, 3, 2))
```
#### <a name="StructuredMesh">StructuredMesh</a>
```python
    def test_StructuredMesh(self):
        mg = np.array(np.meshgrid(np.array([-1, -.5, 0, 1]), np.array([-1, 0, 1]), indexing='ij'))
        regmesh = Mesh(mg)
        self.assertIs(regmesh.mesh_type, MeshType.Structured)
        self.assertEquals(regmesh.shape, (4, 3, 2))
```
#### <a name="UnstructuredMesh">UnstructuredMesh</a>
```python
    def test_UnstructuredMesh(self):
        mg = np.random.rand(100, 10, 2)
        regmesh = Mesh(mg)
        self.assertIs(regmesh.mesh_type, MeshType.Unstructured)
```
#### <a name="RegularMesh">RegularMesh</a>
```python
    def test_RegularMesh(self):
        regmesh = Mesh.RegularMesh([-1, 1, 3], [-1, 1, 3])
        self.assertIs(regmesh.mesh_type, MeshType.Regular)
        self.assertEquals(regmesh.shape, (3, 3, 2))
```
#### <a name="RegMeshSubgrids">RegMeshSubgrids</a>
```python
    def test_RegMeshSubgrids(self):
        regmesh = Mesh.RegularMesh([-1, 1, 3], [-1, 1, 3])
        m = [Mesh(g) for g in regmesh.subgrids]
        self.assertTrue(all(g.mesh_type is MeshType.Regular for g in m))
```
#### <a name="SemiStructuredMesh">SemiStructuredMesh</a>
```python
    def test_SemiStructuredMesh(self):
        semi_mesh = Mesh([[np.arange(i)] for i in range(10, 25)])
        self.assertIs(semi_mesh.mesh_type, MeshType.SemiStructured)
```
#### <a name="MeshFromList">MeshFromList</a>
```python
    def test_MeshFromList(self):
        try:
            wat = np.asarray([[-1, 0, 1], [-1, 0, 1]])
            bad = Mesh(wat)
        except Mesh.MeshError:
            pass
        else:
            # just to make it accessible through Mesh
            self.assertIs(bad.mesh_type, MeshType.Indeterminate)
```

 </div>
</div>

___

[Edit Examples](https://github.com/McCoyGroup/McUtils/edit/edit/ci/examples/McUtils/Zachary/Mesh.md) or 
[Create New Examples](https://github.com/McCoyGroup/McUtils/new/edit/?filename=ci/examples/McUtils/Zachary/Mesh.md) <br/>
[Edit Template](https://github.com/McCoyGroup/McUtils/edit/edit/ci/docs/McUtils/Zachary/Mesh.md) or 
[Create New Template](https://github.com/McCoyGroup/McUtils/new/edit/?filename=ci/docs/templates/McUtils/Zachary/Mesh.md) <br/>
[Edit Docstrings](https://github.com/McCoyGroup/McUtils/edit/edit/McUtils/Zachary/Mesh/__init__.py?message=Update%20Docs)