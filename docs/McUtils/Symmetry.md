# <a id="McUtils.Symmetry">McUtils.Symmetry</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/__init__.py#L1?message=Update%20Docs)]
</div>
    
Provides basic support for point group identification and symmetry handling

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[CharacterTable](Symmetry/Characters/CharacterTable.md)   
</div>
   <div class="col" markdown="1">
[symmetric_group_class_sizes](Symmetry/Characters/symmetric_group_class_sizes.md)   
</div>
   <div class="col" markdown="1">
[symmetric_group_character_table](Symmetry/Characters/symmetric_group_character_table.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[point_group_data](Symmetry/Characters/point_group_data.md)   
</div>
   <div class="col" markdown="1">
[IdentityElement](Symmetry/Elements/IdentityElement.md)   
</div>
   <div class="col" markdown="1">
[SymmetryElement](Symmetry/Elements/SymmetryElement.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[InversionElement](Symmetry/Elements/InversionElement.md)   
</div>
   <div class="col" markdown="1">
[RotationElement](Symmetry/Elements/RotationElement.md)   
</div>
   <div class="col" markdown="1">
[ReflectionElement](Symmetry/Elements/ReflectionElement.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ImproperRotationElement](Symmetry/Elements/ImproperRotationElement.md)   
</div>
   <div class="col" markdown="1">
[RotorTypes](Symmetry/Rotors/RotorTypes.md)   
</div>
   <div class="col" markdown="1">
[identify_rotor_type](Symmetry/Rotors/identify_rotor_type.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[NamedPointGroups](Symmetry/PointGroups/NamedPointGroups.md)   
</div>
   <div class="col" markdown="1">
[ParametrizedPointGroups](Symmetry/PointGroups/ParametrizedPointGroups.md)   
</div>
   <div class="col" markdown="1">
[PointGroup](Symmetry/PointGroups/PointGroup.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[PointGroupIdentifier](Symmetry/SymmetryIdentifier/PointGroupIdentifier.md)   
</div>
   <div class="col" markdown="1">
[identify_symmetry_equivalent_atoms](Symmetry/SymmetryIdentifier/identify_symmetry_equivalent_atoms.md)   
</div>
   <div class="col" markdown="1">
[identify_point_group](Symmetry/SymmetryIdentifier/identify_point_group.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[symmetrize_structure](Symmetry/Symmetrizer/symmetrize_structure.md)   
</div>
   <div class="col" markdown="1">
[symmetrized_coordinate_coefficients](Symmetry/Symmetrizer/symmetrized_coordinate_coefficients.md)   
</div>
   <div class="col" markdown="1">
[get_internal_permutation_symmetry_matrices](Symmetry/Symmetrizer/get_internal_permutation_symmetry_matrices.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[symmetrize_internals](Symmetry/Symmetrizer/symmetrize_internals.md)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>





## Examples
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













<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#Tests-96fa91" markdown="1"> Tests</a> <a class="float-right" data-toggle="collapse" href="#Tests-96fa91"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Tests-96fa91" markdown="1">
 - [Characters](#Characters)
- [CharacterDecomposition](#CharacterDecomposition)
- [CharacterSymmetries](#CharacterSymmetries)
- [SymmetryElements](#SymmetryElements)
- [Transformations](#Transformations)
- [Composition](#Composition)
- [PointGroupElements](#PointGroupElements)
- [PointGroupAlignments](#PointGroupAlignments)
- [Visualization](#Visualization)
- [InternalSymmetries](#InternalSymmetries)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#Setup-2eb66a" markdown="1"> Setup</a> <a class="float-right" data-toggle="collapse" href="#Setup-2eb66a"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Setup-2eb66a" markdown="1">
 
Before we can run our examples we should get a bit of setup out of the way.
Since these examples were harvested from the unit tests not all pieces
will be necessary for all situations.

All tests are wrapped in a test class
```python
class SymmetryTests(TestCase):
```

 </div>
</div>

#### <a name="Characters">Characters</a>
```python
    def test_Characters(self):
        print()

        ct = CharacterTable.point_group("Dh", 4)
        print(ct.format())
        ct = CharacterTable.point_group("Oh")
        print(ct.format())
        ct = CharacterTable.point_group("Cv", 2)
        print(ct.format())
        ct = CharacterTable.point_group("Td")
        print(ct.format())
        ct = CharacterTable.point_group("S", 4)
        print(ct.format())
        ct = CharacterTable.point_group("C", 3)
        print(ct.format())

        elements, classes = point_group_data("Cv", 5, prop="classes")
        self.assertEquals(
            np.sort(np.concatenate(classes)).tolist(),
            np.arange(sum(len(l) for l in classes)).tolist()
        )
        self.assertEquals(len(elements), sum(len(l) for l in classes))

        # ct = CharacterTable.point_group("Cv", 7)
        # # ct = CharacterTable.fixed_size_point_group("T")
        # with np.printoptions(linewidth=1e8, threshold=1e8):
        #     print(ct.format())
        #     print(np.round(np.real(ct.table.T @ np.conj(ct.table)), 8))

        return

        print(mfmt.TableFormatter("").format(symmetric_group_character_table(3)))
        print("="*50)
        print(mfmt.TableFormatter("").format(symmetric_group_character_table(4)))
        # print("="*50)
        # print(mfmt.TableFormatter("").format(symmetric_group_character_table(5)))
        # print("="*50)
        # print(mfmt.TableFormatter("").format(symmetric_group_character_table(6)))
        # print("="*50)
        # print(mfmt.TableFormatter("").format(symmetric_group_character_table(7)))
        # checked against Mathematica, good up through order 7

        weights, ct = symmetric_group_character_table(4, return_weights=True)
        weights = weights #/ np.sum(weights)
        w_vec = np.sqrt(weights[np.newaxis, :] / np.sum(weights))
        wct = w_vec * ct
        # print(weights)
        # print(ct)
        print(mfmt.TableFormatter("").format(wct))
        print(np.round(wct @ wct.T, 6))

        sel = (0, 2, 3, 4)
        b2 = wct[:, sel]
        w2 = np.sqrt(weights[np.newaxis, sel] / np.sum(weights[sel,]))
        q, r = np.linalg.qr(b2.T)
        print(q.T / w2)
```

#### <a name="CharacterDecomposition">CharacterDecomposition</a>
```python
    def test_CharacterDecomposition(self):
        # print()

        pg = CharacterTable.point_group("Cv", 2)
        coords = np.array([[ 0.00000, 0.,  0.12595],
                           [ 1.43714, 0., -0.99944],
                           [-1.43714, 0., -0.99944]])
        self.assertEquals(
            [2, 0, 1, 0],
            np.round(pg.coordinate_mode_reduction(coords), 8).tolist()
        )
        # return

        pg = CharacterTable.point_group("Cv", 3)
        rep = pg.axis_representation()
        decomp = pg.decompose_representation(rep).T
        self.assertEquals(
            [
                np.round(decomp[0] + decomp[1], 8).tolist(),
                np.round(decomp[2], 8).tolist()
            ],
            [
                [0, 0, 1], # 3rd irrep is x-y
                [1, 0, 0] # 1st irrep is z
            ]
        )
        self.assertEquals(
            [
                np.round(decomp[3] + decomp[4], 8).tolist(),
                np.round(decomp[5], 8).tolist()
            ],
            [
                [0, 0, 1], # 3rd irrep is x-y rotation
                [0, 1, 0] # 2nd irrep is z rotation
            ]
        )


        pg = CharacterTable.point_group("Td")

        # print(pg.format())
        rep = pg.axis_representation()
        # print(np.round(rep, 8))

        decomp = pg.decompose_representation(rep).T

        self.assertEquals(
            [
                np.round(np.sum(decomp[:3], axis=0), 8).tolist(),
                np.round(np.sum(decomp[3:], axis=0), 8).tolist()
            ],
            [
                [0, 0, 0, 0, 1], # triply degenerate irreps
                [0, 0, 0, 1, 0] # triply degenerate irreps
            ]
        )
        print(np.round(np.sum(decomp[:3], axis=0), 8))
        print(np.round(np.sum(decomp[3:], axis=0), 8))
```

#### <a name="CharacterSymmetries">CharacterSymmetries</a>
```python
    def test_CharacterSymmetries(self):
        # print(
        #     nput.enumerate_permutations([
        #         [0, 1, 2, 3],
        #         [0, 3, 1, 2],
        #         [0, 1, 3, 2]
        #     ])
        # )
        # return
        # mats = point_group_data("Cv", 3, prop="matrices")
        # uhh = nput.vec_tensordiag(np.eye(3))
        # print()
        # print(CharacterTable.point_group('Cv', 3).format())
        # print(CharacterTable.point_group('Cv', 3).axis_representation(include_rotations=False))
        # woof = np.tensordot(mats, nput.vec_tensordiag(np.eye(3)), axes=[-1, -1])
        # print(np.trace(woof, axis1=1, axis2=-1))
        #
        #
        #
        # return
        p = CharacterTable.point_group('Cv', 3)
        coords = np.concatenate(
            [
                [[0, 0, 1]],
                nput.apply_symmetries([1, 0, 0], p.matrices)
            ],
            axis=0
        )
        # character_coeffs = p.symmetrized_coordinate_coefficients(coords, normalize=True)
        # self.assertAlmostEqual(np.sum(character_coeffs[0, 0]), 0)
        # self.assertAlmostEqual(np.sum(character_coeffs[0, 1]), 0)
        # self.assertAlmostEqual(np.sum(character_coeffs[0, 2]), 1) # nitrogen z coordinate

        character_coeffs2 = p.symmetrized_coordinate_coefficients(coords, as_characters=False)
        # return

        print(
            np.round(np.sum(character_coeffs2[:6, 3], axis=0).reshape(4, 3), 8)
        )
        print(
            np.round(np.sum(character_coeffs2[:6, 6], axis=0).reshape(4, 3), 8)
        )
        print(
            np.round(np.sum(character_coeffs2[:6, 9], axis=0).reshape(4, 3), 8)
        )
```

#### <a name="SymmetryElements">SymmetryElements</a>
```python
    def test_SymmetryElements(self):

        for s in [
            InversionElement(),
            RotationElement(5, [0, 1, 1], 2),
            ImproperRotationElement(11, [1, 0, 0]),
            ReflectionElement([1, 0, 1])
        ]:
            self.assertEquals(
                SymmetryElement.from_transformation_matrix(
                    s.get_transformation()
                ),
                s
            )
```

#### <a name="Transformations">Transformations</a>
```python
    def test_Transformations(self):

        np.random.seed(12223)
        tf = nput.view_matrix(np.random.rand(3))
        ax = np.random.rand(3)
        for a in [
            InversionElement(),
            RotationElement(2, ax),
            RotationElement(5, ax),
            RotationElement(7, ax, 2),
            RotationElement(22, ax, 11),
            ReflectionElement(ax),
            ImproperRotationElement(3, ax),
            ImproperRotationElement(6, ax, 5),
            ImproperRotationElement(7, ax, 5),
        ]:
            s = a.transform(tf)

            x1 = s.get_transformation()
            x2 = tf @ a.get_transformation() @ tf.T
            # print(x1)
            # print(x2)

            self.assertTrue(
                np.allclose(x1, x2)
            )
```

#### <a name="Composition">Composition</a>
```python
    def test_Composition(self):
        np.random.seed(123)
        ax = np.random.rand(3)
        ax2 = np.cross(ax, [0, 1, 0])
        ax3 = RotationElement(6, ax).get_transformation() @ ax
        for a,b in [
            [InversionElement(), RotationElement(7, ax2, root=5)],
            [RotationElement(2, ax), RotationElement(7, ax2, root=5)],
            [RotationElement(2, ax), ImproperRotationElement(7, ax2, root=5)],
            [RotationElement(3, ax), RotationElement(7, ax, root=5)],
            [RotationElement(6, ax), RotationElement(11, ax3)],
            [RotationElement(6, ax), ImproperRotationElement(12, ax3)],
        ]:
            s1 = a @ b
            s2 = SymmetryElement.compose(a, b)
            print(a, "@", b, "=>", s1)

            if hasattr(s1, 'bits'):
                print(":", SymmetryElement.from_transformation_matrix(s1.get_transformation()))


            self.assertTrue(
                np.allclose(
                    s1.get_transformation(),
                    s2.get_transformation()
                )
            )
```

#### <a name="PointGroupElements">PointGroupElements</a>
```python
    def test_PointGroupElements(self):
        for name in [
            # ("Cv", 2),
            # ("S", 4),
            # ("Ch", 4),
            # ("Ch", 6),
            # ("Dh", 4),
            # ("Dh", 6),
            # ("Dd", 7),
            # ("D", 7),
            ("T",),
            ("Td",),
            ("Th",),
            ("O",),
            ("Oh",),
            ("I",),
            ("Ih",),
        ]:
            pg = PointGroup.from_name(*name)
            ct = pg.character_table
            elements = ct.permutations
            classes = ct.classes
            print(pg, pg.elements)
            self.assertIsNot(classes, None)
            self.assertEquals(
                np.sort(np.concatenate(classes)).tolist(),
                np.arange(sum(len(l) for l in classes)).tolist()
            )
            self.assertEquals(len(elements), sum(len(l) for l in classes))
```

#### <a name="PointGroupAlignments">PointGroupAlignments</a>
```python
    def test_PointGroupAlignments(self):
        pg = PointGroup.from_name("Ch", 6)
        print(pg.axes @ pg.axes.T)
        new_pg = pg.align(np.eye(3))
        print(new_pg.get_axes())
```

#### <a name="Visualization">Visualization</a>
```python
    def test_Visualization(self):
        pg = PointGroup.from_name("Dd", 3)
        # base = pg.plot() #.show()
        print(pg.axes)
        new_pg = pg.align(np.eye(3))
        print(new_pg.axes)
        new_pg.plot().show()
        for e in pg.elements:
            if hasattr(e, 'axis'):
                print(e, e.axis)
```

#### <a name="InternalSymmetries">InternalSymmetries</a>
```python
    def test_InternalSymmetries(self):
        import McUtils.Coordinerds as coordops
        import McUtils.Numputils as nput

        # mats, ints = get_internal_permutation_symmetry_matrices(
        #     coords,
        #     [
        #         [0, 2, 1, 4, 3]
        #     ]
        # )
        # self.assertEquals(mats.shape, (len(ints), len(ints), 1))


        p = CharacterTable.point_group('Cv', 3)

        coords = np.concatenate(
            [
                [[0, 0, 1]],
                nput.apply_symmetries([1, 0, 0], p.matrices)
            ],
            axis=0
        )
        # print(p.matrices)
        # print(coords)


        symm_modes = symmetrized_coordinate_coefficients(p, coords, drop_empty_modes=False)#, as_characters=True, normalize=False)
        # print(np.round(symm_modes[2], 8))
        self.assertEquals(
            [s.shape for s in symm_modes],
            [(12, 4), (12, 4), (12, 7)] # z-component of nitrogen has no symmetry equivalents
        )

        internals = coordops.extract_zmatrix_internals([
            [0, -1, -1, -1],
            [1,  0, -1, -1],
            [2,  0,  1, -1],
            [3,  0,  2,  1]
        ], canonicalize=True)

        # internals = [(0, 1)]

        coeffs, full_internals, red_exps, expansions, base = symmetrize_internals(p, internals, coords,
                                                                                 return_expansions=True,
                                                                                 return_base_expansion=True,
                                                                                 reduce_redundant_coordinates=True)
        self.assertEquals(len(full_internals), 9)
        self.assertEquals(
            [s.shape for s in coeffs],
            [(9, 3), (9, 3), (9, 6)]
        )
        a1_coeffs, a1_inv = expansions[0]
        int_vals, _ = base
        self.assertAlmostEquals(a1_coeffs[0][0], int_vals[0][0] * np.sqrt(3))
        # print(a1_coeffs[0])
        # print(int_vals[0])
        # print(a1_coeffs[1].shape)
        print(red_exps[1].shape)


        coeffs, full_internals, expansions, base = symmetrize_internals(p, internals, coords,
                                                                        return_expansions=True,
                                                                        return_base_expansion=True,
                                                                        atom_selection=[1, 2, 3]
                                                                        )
```

 </div>
</div>






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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/__init__.py#L1?message=Update%20Docs)   
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