# import itertools
#
# import scipy.linalg
#
# import McUtils.Zachary
from Peeves.TestUtils import *
from unittest import TestCase

# from McUtils.Data import UnitsData, PotentialData
# from McUtils.Zachary import Interpolator, Symbols
# import McUtils.Plots as plt
# from McUtils.GaussianInterface import GaussianLogReader

from McUtils.Symmetry import *
# from Psience.Molecools import Molecule
import numpy as np
import McUtils.Numputils as nput

class SymmetryTests(TestCase):


    @validationTest
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

        # s7 = symmetric_group_character_table(7)
        # print(np.linalg.svd(s7))

    @validationTest
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

    @validationTest
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
        # self.assertAlmostEqual(np.sum(character_coeffs[0, 0]), 0)

        # raise Exception(coords)
        # p.symmetry_permutations(coords)
        # perms = [nput.symmetry_permutation(coords, m) for m in p.matrices]
        # print(perms)

    @validationTest
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

    @validationTest
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

    @validationTest
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

    @validationTest
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


    @validationTest
    def test_PointGroupAlignments(self):
        pg = PointGroup.from_name("Ch", 6)
        print(pg.axes @ pg.axes.T)
        new_pg = pg.align(np.eye(3))
        print(new_pg.get_axes())

    @validationTest
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


    @debugTest
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

        symm_modes = symmetrized_coordinate_coefficients(p, coords)#, as_characters=True, normalize=False)
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

        coeffs, full_internals, expansions, base = symmetrize_internals(p, internals, coords,
                                                                        return_expansions=True,
                                                                        return_base_expansion=True)
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


        coeffs, full_internals, expansions, base = symmetrize_internals(p, internals, coords,
                                                                        return_expansions=True,
                                                                        return_base_expansion=True,
                                                                        atom_selection=[1, 2, 3]
                                                                        )
        # print("-"*100)
        # print(coeffs[0])

