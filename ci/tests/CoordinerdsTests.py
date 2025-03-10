
from Peeves.TestUtils import *
from Peeves.Timer import Timer
from Peeves import BlockProfiler
from unittest import TestCase
from McUtils.Coordinerds import *
from McUtils.Plots import *
from McUtils.Numputils import *
import sys, numpy as np, os

class ConverterTest(TestCase):

    def setUp(self):
        super().setUp()
        self.initialize_data()
        self.load()

    @property
    def loaded(self):
        return hasattr(self, "cases")

    def load(self, n=10):
        if not self.loaded:
            self.cases = n
            self.transforms = DataGenerator.mats(n)
            self.shifts = DataGenerator.vecs(n)
            self.mats = affine_matrix(self.transforms, self.shifts)

    def initialize_data(self):
        self.n = 10
        self.test_zmats = CoordinateSet(DataGenerator.zmats(self.n, 15), system=ZMatrixCoordinates)
        self.test_carts = CoordinateSet(DataGenerator.multicoords(self.n, 10))
        self.test_structure = [
            [ 0.0,                    0.0,                   0.0                ],
            [ 0.5312106220949451,     0.0,                   0.0                ],
            [ 5.4908987527698905e-2,  0.5746865893353914,    0.0                ],
            [-6.188515885294378e-2,  -2.4189926062338385e-2, 0.4721688095375285 ],
            [ 1.53308938205413e-2,    0.3833690190410768,    0.23086294551212294],
            [ 0.1310095622893345,     0.30435650497612,      0.5316931774973834 ]
        ]
        self.dihed_test_structure = np.array([
            [0.0, 0.0, 0.0 ],
            [-0.8247121421923925, -0.629530611338456, 1.775332267901544 ],
            [0.1318851447521099, 2.088940054609643, 0.0],
            [1.786540362044548, -1.386051328559878, 0.0],
            [2.233806981137821, 0.3567096955165336, 0.0],
            [-0.8247121421923925, -0.629530611338456, -1.775332267901544]
        ])
        self.zm_conv_test_structure = np.array([
            [1.0, 0.0, 1.0],
            [-0.8247121421923925, -0.629530611338456, 1.775332267901544],
            [0.1318851447521099, 2.088940054609643, 0.0],
            [1.786540362044548, -1.386051328559878, 0.0],
            [2.233806981137821, 0.3567096955165336, 0.0],
            [-0.8247121421923925, -0.629530611338456, -1.775332267901544]
        ])

    @validationTest
    def test_GetDihedrals(self):
        from McUtils.Numputils import pts_dihedrals as calc_dihed

        orig = self.dihed_test_structure

        dihed = calc_dihed(orig[3:5], orig[2:4], orig[1:3], orig[0:2])
        self.assertEquals(round(dihed[0], 6), round(.591539, 6))
    @validationTest
    def test_CoordinateSet(self):
        import numpy as np
        coord_set = CoordinateSet(DataGenerator.coords(500))
        self.assertIsInstance(coord_set, np.ndarray)
    @validationTest
    def test_Loader(self):
        loaded = CoordinateSystemConverters.get_converter(CartesianCoordinates3D, ZMatrixCoordinates)
        self.assertIsInstance(loaded, CoordinateSystemConverter)
    @validationTest
    def test_CartesianToZMatrix(self):
        coord_set = CoordinateSet(DataGenerator.coords(10))
        coord_set = coord_set.convert(ZMatrixCoordinates, use_rad = False)
        self.assertEqual(coord_set.shape, (9, 3))
    @validationTest
    def test_CartesianToZMatrixMulti(self):
        coord_set = CoordinateSet(DataGenerator.multicoords(10, 10))
        coord_set = coord_set.convert(ZMatrixCoordinates, use_rad = False)
        self.assertEqual(coord_set.shape, (10, 9, 3))

    @validationTest
    def test_CartesianToZMatrixAndBack(self):
        cs1 = coord_set = CoordinateSet([self.zm_conv_test_structure]*4, CartesianCoordinates3D)
        coord_set = coord_set.convert(ZMatrixCoordinates)
        coord_set = coord_set.convert(CartesianCoordinates3D)
        cs2 = coord_set
        self.assertEqual(round(np.linalg.norm(cs2 - cs1), 8), 0.)

    @inactiveTest
    def test_PsiAnglesToZMatrixAndBack(self):
        carts_OCHH = CoordinateSet([
                                      [
                                          [  0.000000, 0.000000, 0.000000],
                                          [  0.000000, 0.000000, 1.220000],
                                          [  0.926647, 0.000000, 1.755000],
                                          [ -0.926647, 0.000000, 1.755000]
                                      ]
                                  ] * 2,
                                  system=CartesianCoordinates3D
                                  )
        O1 = 0
        C1 = 1
        H1 = 2
        H2 = 3
        _ = -1
        zm_ochh = [
            [O1, _, _, _],
            [C1, O1, _, _],
            [H1, O1, C1, _],
            [H2, O1, C1, H1]
        ]


        O1 = 1
        H1 = 0
        H2 = 2
        O2 = 3
        H3 = 4
        H4 = 5
        _ = -1
        zm_old = [  # water_dimer_freq_unopt Z-mat
            [H1, _, _, _],
            [O1, H1, _, _],
            [H2, O1, H1, _],
            [O2, O1, H2, H1],
            [H3, O2, H2, H1],
            [H4, O2, H2, H1]
        ]

        carts_old = CoordinateSet([
                                      [
                                          [  0.899890,  1.851024,  0.000000],
                                          [ -0.000214,  1.516013,  0.000000],
                                          [  0.099753,  0.552590,  0.000000],
                                          [ -0.000214, -1.390289, -0.000000],
                                          [ -0.498111, -1.704705,  0.761032],
                                          [ -0.498111, -1.704705, -0.761032]
                                      ]
                                  ] * 2,
                                  system=CartesianCoordinates3D
                              )
        carts_new = CoordinateSet([
                                      [
                                          [  0.000000,  0.000000,  0.000000],
                                          [  0.000000,  0.000000,  0.962259],
                                          [  0.931459,  0.000000, -0.241467],
                                          [ -1.297691, -2.406089, -0.989477],
                                          [ -2.033248, -2.168659, -1.559520],
                                          [ -0.925486, -1.557192, -0.708516]
                                      ]
                                  ] * 2,
                                  system=CartesianCoordinates3D
                                  )

        O1 = 1
        H1 = 0
        H2 = 2
        O2 = 3
        H3 = 4
        H4 = 5
        _ = -1
        zm_old = [ #water_dimer_freq_unopt Z-mat
            [H1, _, _, _],
            [O1, H1, _, _],
            [H2, O1, H1, _],
            [O2, O1, H2, H1],
            [H3, O2, H2, H1],
            [H4, O2, H2, H1]
        ]

        O1 = 0
        H1 = 1
        H2 = 2
        O2 = 3
        H3 = 4
        H4 = 5
        _ = -1
        zm_new = [
            [O1, _,   _,  _],
            [H1, O1,  _,  _],
            [H2, O1, H1,  _],
            [O2, O1, H1, H2],
            [H3, O2, O1, H2],
            [H4, O2, H3, O1]
        ]


        # test that we get same thing out for a given input
        carts = carts_new
        zm = zm_new

        # zmat_system = ZMatrixCoordinateSystem(
        #     ordering=zm
        # )
        # internals = carts.convert(zmat_system)
        # carts2 = internals.convert(CartesianCoordinates3D)
        # print(">>>", np.round(carts[0], 3))
        # print("==>", np.round(np.rad2deg(internals[0][:, 1:]), 0))
        # self.assertEqual(round(np.linalg.norm(carts - carts2), 8), 0.)

        zmat_system = ZMatrixCoordinateSystem(
            ordering=[x + [1] for x in zm]
        )
        internals2 = carts.convert(zmat_system)
        carts2 = internals2.convert(CartesianCoordinates3D)

        print("<<<", np.round(carts [0], 3))
        print("<<<", np.round(carts2[0], 3))
        print("<==", np.round(np.rad2deg(internals2[0][:, 1:]), 3))

        carts2 = CoordinateSet(carts2,
                      system=CartesianCoordinates3D
                      )
        zmat_system = ZMatrixCoordinateSystem(
            ordering=[x + [1] for x in zm]
        )
        internals3 = carts2.convert(zmat_system)
        print("<==", np.round(np.rad2deg(internals3[0][:, 1:]), 3))

        self.assertEqual(round(np.linalg.norm(carts - carts2), 8), 0.)

    @validationTest
    def test_ExpansionCoordinates(self):
        np.random.seed(0)
        coord_set = CoordinateSet([self.test_structure] * 2)
        expansion_1 = np.random.rand(len(self.test_structure)*3, len(self.test_structure)*3)
        expansion_1 = (expansion_1 / np.broadcast_to(np.linalg.norm(expansion_1, axis=0), expansion_1.shape))
        cs1 = CoordinateSystem("CartesianExpanded",
                               basis=CartesianCoordinates3D,
                               matrix=expansion_1
                               )
        expansion_2 = np.random.rand((len(self.test_structure) - 1) * 3, (len(self.test_structure) - 1) * 3)
        expansion_2 = (expansion_2 / np.broadcast_to(np.linalg.norm(expansion_2, axis=0), expansion_2.shape))
        cs2 = CoordinateSystem("ZMatrixExpanded",
                               basis=ZMatrixCoordinates,
                               matrix=expansion_2
                               )
        coord_set2 = coord_set.convert(cs1)
        coord_set2 = coord_set2.convert(cs2)
        coord_set2 = coord_set2.convert(CartesianCoordinates3D)
        self.assertEqual(round(np.linalg.norm(coord_set2 - coord_set), 8), 0.)
    @validationTest
    def test_ZMatrixToCartesian(self):
        # print(self.test_zmats.coords[0, 0], file=sys.stderr)
        coords = self.test_zmats.convert(CartesianCoordinates3D, use_rad = False)
        self.assertEqual(coords.shape, (self.n, 16, 3))
    @validationTest
    def test_NumpyLikeTest(self):
        # print(self.test_zmats.coords[0, 0], file=sys.stderr)
        coords = self.test_zmats.convert(CartesianCoordinates3D, use_rad = False)
        self.assertAlmostEqual(np.linalg.norm(coords - coords), 0.)
    # @timeitTest(number=2500)
    # def test_CartToZTiming(self):
    #     coord_set = self.test_carts
    #     coord_set = coord_set.convert(ZMatrixCoordinates, use_rad = False)
    #     self.assertEqual(coord_set.shape, (self.n, 9, 6))
    # @timeitTest(number=2500)
    # def test_ZMatrixToCartesianTiming(self):
    #     coords = self.test_zmats.convert(CartesianCoordinates3D, use_rad = False)
    #     self.assertEqual(coords.shape, (self.n, 16, 3))

    #region Jacobians
    @inactiveTest
    def test_CartesianToZMatrixJacobian(self):
        n = 10
        test_coords = DataGenerator.coords(n)
        # test_coords = np.array([[0, 0, 0], [1, 1, 0], [1, 2, 0], [0, 2, 1], [0, -2, -1]])
        coord_set = CoordinateSet(test_coords)
        # ordr = [
        #           [0, -1, -1, -1],
        #           [1,  0, -1, -1],
        #           [2,  0,  1, -1],
        #           [3,  1,  2,  0],
        #           [4,  0,  3,  2]
        #           ]

        icrds = coord_set.convert(ZMatrixCoordinates)#, ordering=ordr)
        # print(icrds)
        # wat = icrds.convert(CartesianCoordinates3D)

        internals = ZMatrixCoordinateSystem(**icrds.converter_options)
        ijacob = icrds.jacobian(CartesianCoordinates3D).reshape((n - 1) * 3, n * 3)
        nijacob = icrds.jacobian(CartesianCoordinates3D, all_numerical=True, stencil=3).reshape((n-1)*3, n*3)
        jacob = coord_set.jacobian(internals, stencil=3).reshape(n * 3, (n - 1) * 3)
        njacob = coord_set.jacobian(internals, all_numerical=True).reshape(n*3, (n-1)*3)

        # with Timer("Block Z2C"):
        #     wat = icrds.convert(CartesianCoordinates3D)
        # with Timer("Block Z2C Analytic"):
        #     ijacob = icrds.jacobian(CartesianCoordinates3D).reshape((n-1)*3, n*3)
        # with Timer("Block Z2C Numerical"):
        #     nijacob = icrds.jacobian(CartesianCoordinates3D, all_numerical=True, stencil=3).reshape((n-1)*3, n*3)
        # with Timer("Block C2Z"):
        #     icrds = coord_set.convert(ZMatrixCoordinates)#, ordering=ordr)
        # with Timer("Block C2Z Analytic"):
        #     jacob = coord_set.jacobian(internals, stencil=3).reshape(n * 3, (n - 1) * 3)
        # with Timer("Block C2Z Numerical"):
        #     njacob = coord_set.jacobian(internals, all_numerical=True).reshape(n*3, (n-1)*3)
        # raise Exception("wat")
        # ordcrd = coord_set[np.array(ordr, int)[:, 0]]
        # raise Exception(ordcrd-wat)

        vmax = np.max(np.abs(jacob))

        g = GraphicsGrid(ncols=2, nrows=2, image_size=(600, 600))
        ArrayPlot(jacob, figure=g[0, 0], vmin=-vmax, vmax=vmax)
        ArrayPlot(njacob, figure=g[0, 1], vmin=-vmax, vmax=vmax)
        ArrayPlot(np.round(njacob-jacob, 4), figure=g[1, 0], vmin=-vmax, vmax=vmax)
        ArrayPlot(np.round(njacob+jacob, 4), figure=g[1, 1], vmin=-vmax, vmax=vmax)
        g.padding=.05
        g.padding_top=.5
        # g.padding_bottom=0
        g.show()

        # g = GraphicsGrid(ncols=3, nrows=2, image_size=(900, 600))
        # ArrayPlot(jacob,          figure=g[0, 0])
        # ArrayPlot(njacob,         figure=g[1, 0])
        # ArrayPlot(jacob - njacob, figure=g[0, 1])
        # ArrayPlot(ijacob,         figure=g[1, 1])
        # ArrayPlot(nijacob@jacob,  figure=g[0, 2])
        # ArrayPlot(ijacob@jacob,   figure=g[1, 2])
        # g.show()

        self.assertTrue(np.allclose(jacob,  njacob), msg="{} too large".format(np.sum(np.abs(jacob-njacob))))
        self.assertTrue(np.allclose(ijacob,  nijacob))
        self.assertEquals(jacob.shape, (n*3, (n-1)*3)) # we always lose one atom
        self.assertAlmostEqual(np.sum((ijacob@jacob)), 3*n-6, 3)

    @validationTest
    def test_CartesianToZMatrixMultiJacobian(self):
        nstruct=20
        ndim=10
        coord_set = CoordinateSet(DataGenerator.multicoords(nstruct, ndim))
        all_numerical=True
        with BlockProfiler('jacobian_shit'):#, mode='deterministic'):
            jacob = coord_set.jacobian(ZMatrixCoordinates, stencil=5, all_numerical=all_numerical)
        # ArrayPlot(jacob[0], colorbar=True).show()
        if not all_numerical:
            self.assertEquals(jacob.shape, (nstruct, ndim, 3, 10 - 1, 3 )) # we always lose one atom
        else:
            self.assertEquals(jacob.shape, (3*ndim, nstruct, 10 - 1, 3 )) # we always lose one atom


    @validationTest
    def test_CH5ZMatJacobian(self):
        coord_set = CoordinateSet([
            [
                [ 0.000000000000000,    0.000000000000000,  0.000000000000000],
                [ 0.1318851447521099,   2.088940054609643,  0.000000000000000],
                [ 1.786540362044548,   -1.386051328559878,  0.000000000000000],
                [ 2.233806981137821,    0.3567096955165336, 0.000000000000000],
                [-0.8247121421923925, -0.6295306113384560, -1.775332267901544],
                [-0.8247121421923925, -0.6295306113384560,  1.775332267901544]
                ]
            ]*100,
            system=CartesianCoordinates3D
        )

        zmat_system = ZMatrixCoordinateSystem(
            ordering=[
                [0,  0, -1, -1],
                [1,  0,  1, -1],
                [2,  0,  1,  2],
                [3,  0,  1,  2],
                [4,  0,  1,  2],
                [5,  0,  1,  2]
            ]
        )
        # zmcs = coord_set.convert(ZMatrixCoordinates, ordering=zmat_ordering)

        jacob = coord_set.jacobian(
            zmat_system,
            stencil=5,
            prep=lambda coord, disps, zmcs: (disps, zmcs[..., :, 1]),
            all_numerical = True
        )
        self.assertEquals(jacob.shape, (np.product(coord_set.shape[1:]), 100, 5)) # I requested 5 bond lengths

        # the analytic derivs. track a slightly different shape
        jacob = coord_set.jacobian(
            zmat_system,
            stencil=5,
            prep=lambda coord, disps, zmcs: (disps, zmcs[..., :, 1])
        )
        self.assertEquals(jacob.shape, (100,) + coord_set.shape[1:] + (5, 3)) # I requested 5 bond lengths

    @inactiveTest
    def test_CartesianToZMatrixJacobian2(self):
        coord_set = CoordinateSet(DataGenerator.multicoords(10, 10)[0])
        njacob = coord_set.jacobian(ZMatrixCoordinates, 2, stencil=5, all_numerical=True)
        self.assertEquals(njacob.shape, (10 * 3, 10 * 3, 10 - 1, 3))  # we always lose one atom

        jacob = coord_set.jacobian(ZMatrixCoordinates, 2, stencil=5)  # semi-analytic
        self.assertEquals(jacob.shape, (10, 3, 10, 3, 10 - 1, 3))  # we always lose one atom

        # jacob = jacob.reshape((10, 3, 10, 3, 10 - 1, 3))

        # import McUtils.Plots as plt
        #
        # bleh_a = np.round(np.reshape(njacob, (900, 27)), 8)
        # bleh_b = np.round(np.reshape(jacob, (900, 27)), 8)
        # bleh_c = np.round(bleh_a - bleh_b, 10)
        # bleh_bleh = np.where(bleh_c != 0.)
        #
        # plt.ArrayPlot( ( bleh_a == 0. ).astype(int) )
        # plt.ArrayPlot( ( bleh_b == 0. ).astype(int) )
        # plt.ArrayPlot( ( np.round(bleh_c, 5) == 0. ).astype(int) ).show()

        njacob = njacob.reshape((10, 3, 10, 3, 10 - 1, 3))
        diffs = njacob - jacob
        bleh_bleh = np.where(np.round(diffs, 3) != 0.)
        # print(bleh_bleh)

        # print("???", np.round(jacob[0, :, 0, :, :, 0], 2), np.round(njacob[0, :, 0, :, :, 2], 2))
        self.assertTrue(
            np.allclose(diffs, 0., atol=1.0e-3),
            msg="wat: {}".format(np.max(np.abs(np.round(diffs, 3))))
        )

    @inactiveTest
    def test_CartesianToZMatrixJacobian2Planar(self):

        coord_set = CoordinateSet( # water
            np.array(
                [[-9.84847483e-18, -1.38777878e-17, 9.91295048e-02],
                 [-9.84847483e-18, -1.38777878e-17, 1.09912950e+00],
                 [ 1.00000000e+00, 9.71445147e-17, 9.91295048e-02],
                 [ 2.46519033e-32, -1.38777878e-17, 2.25076602e-01],
                 [-1.97215226e-31, 1.43714410e+00, -9.00306410e-01],
                 [-1.75999392e-16, -1.43714410e+00, -9.00306410e-01]]
            )
        )
        coord_set_2 = CoordinateSet( # HOD
            np.array([
                [-1.86403557e-17, -7.60465240e-02,  4.62443228e-02],
                [ 6.70904773e-17, -7.60465240e-02, -9.53755677e-01],
                [ 9.29682337e-01,  2.92315732e-01,  4.62443228e-02],
                [ 2.46519033e-32, -1.38777878e-17,  2.25076602e-01],
                [-1.97215226e-31,  1.43714410e+00, -9.00306410e-01],
                [-1.75999392e-16, -1.43714410e+00, -9.00306410e-01]
            ])
        )
        internal_ordering = [
            [0, -1, -1, -1],
            [1,  0, -1, -1],
            [2,  0,  1, -1],
            [3,  0,  2,  1],
            [4,  3,  1,  2],
            [5,  3,  4,  1]
        ]
        coord_set.converter_options = {'ordering': internal_ordering}
        njacob = coord_set.jacobian(ZMatrixCoordinates, 2, stencil=5, analytic_deriv_order=1) # only do analytic firsts
        self.assertEquals(njacob.shape, (6 * 3, 6, 3, 6 - 1, 3))  # we always lose one atom

        jacob = coord_set.jacobian(ZMatrixCoordinates, 2, stencil=5)  # totally-analytic
        self.assertEquals(jacob.shape, (6, 3, 6, 3, 6 - 1, 3))  # we always lose one atom

        njacob = njacob.reshape((6, 3, 6, 3, 6 - 1, 3))

        diffs = njacob - jacob
        ehhh = np.round(diffs, 3)
        # print(
        #     njacob[ np.abs(ehhh) > 0 ],
        #     jacob[np.abs(ehhh) > 0],
        # )

        print(
            np.array(np.where(np.abs(jacob) > 100)).T
        )
        print(np.max(np.abs(njacob)), np.max(np.abs(jacob)))
        self.assertTrue(
            np.allclose(diffs, 0., atol=1.0e-4),
            msg="wat: {}".format(np.max(np.abs(np.round(diffs, 6))))
        )

    @validationTest
    def test_CartesianToZMatrixMultiJacobian2(self):
        coord_set = CoordinateSet(DataGenerator.multicoords(10, 10))
        njacob = coord_set.jacobian(ZMatrixCoordinates, 2, stencil = 5, all_numerical=True)
        # TensorPlot(jacob[0],
        #            ticks_style = [
        #                dict(
        #                    bottom = False,
        #                    top = False,
        #                    labelbottom = False
        #                ),
        #                dict(
        #                    right = False,
        #                    left = False,
        #                    labelleft = False
        #                )
        #            ]
        #            ).show()
        self.assertEquals(njacob.shape, (10*3, 10*3, 10, 10 - 1, 3)) # we always lose one atom


        jacob = coord_set.jacobian(ZMatrixCoordinates, 2, stencil = 5) # semi-analytic
        self.assertEquals(jacob.shape, (10, 10, 3, 10, 3, 10 - 1, 3)) # we always lose one atom
        # self.assertEquals(jacob.shape, (10 * 3, 10, 10, 3, 10 - 1, 3)) # we always lose one atom

    @timeitTest(number=1)
    def test_CartesianToZMatrixMultiJacobian1(self):
        coord_set = CoordinateSet(DataGenerator.multicoords(1, 10))
        jacob = coord_set.jacobian(ZMatrixCoordinates, stencil = 5)
        # ArrayPlot(jacob[0], colorbar=True).show()
        self.assertEquals(jacob.shape, (1, 10*3, 10 * 3 - 3 )) # we always lose one atom
    @timeitTest(number=1)
    def test_CartesianToZMatrixMultiJacobian10(self):
        coord_set = CoordinateSet(DataGenerator.multicoords(10, 10))
        jacob = coord_set.jacobian(ZMatrixCoordinates, stencil = 5)
        # ArrayPlot(jacob[0], colorbar=True).show()
        self.assertEquals(jacob.shape, (10, 10*3, 10 * 3 - 3 )) # we always lose one atom
    @timeitTest(number=1)
    def test_CartesianToZMatrixMultiJacobian2Timing10(self):
        coord_set = CoordinateSet(DataGenerator.multicoords(10, 10))
        jacob = coord_set.jacobian(ZMatrixCoordinates, 2, stencil = 5)
        # ArrayPlot(jacob[0], colorbar=True).show()
        self.assertEquals(jacob.shape, (10, 10*3, 10*3, 10 * 3 - 3 )) # we always lose one atom
    @timeitTest(number=1)
    def test_CartesianToZMatrixMultiJacobian3Timing1(self):
        coord_set = CoordinateSet(DataGenerator.multicoords(1, 10))
        jacob = coord_set.jacobian(ZMatrixCoordinates, 3, stencil = 5)
        # ArrayPlot(jacob[0], colorbar=True).show()
        self.assertEquals(jacob.shape, (1, 10*3, 10*3, 10*3, 10 * 3 - 3 )) # we always lose one atom
    @timeitTest(number=1)
    def test_CartesianToZMatrixMultiJacobian3Timing10(self):
        coord_set = CoordinateSet(DataGenerator.multicoords(10, 10))
        jacob = coord_set.jacobian(ZMatrixCoordinates, 3, stencil = 5)
        # ArrayPlot(jacob[0], colorbar=True).show()
        self.assertEquals(jacob.shape, (10, 10*3, 10*3, 10*3, 10 * 3 - 3 )) # we always lose one atom

    @inactiveTest
    def test_CartesianToZMatrixMultiJacobian3(self):
        coord_set = CoordinateSet(DataGenerator.multicoords(10, 10))
        jacob = coord_set.jacobian(ZMatrixCoordinates, 3, stencil=5)
        # ArrayPlot(jacob[0], colorbar=True).show()
        self.assertEquals(jacob.shape, (10 * 3, 10 * 3, 10, 10, 3, 10 - 1, 3))  # we always lose one atom

    @validationTest
    def test_CartesianToZMatrixMultiJacobianTargeted(self):
        coord_set = CoordinateSet(DataGenerator.multicoords(10, 10))
        jacob = coord_set.jacobian(ZMatrixCoordinates, stencil=5, coordinates=[[1, 2, 3], None])
        # ArrayPlot(jacob[0], colorbar=True).show()
        self.assertEquals(jacob.shape, (10, 10, 3, 10 - 1, 3))  # we always lose one atom

    #endregion

    #region CoordinateSystemTests

    @validationTest
    def test_ZMatrixStep(self):
        self.assertEquals(ZMatrixCoordinates.displacement(.1), .1)

    @validationTest
    def test_CartStep(self):
        self.assertEquals(CartesianCoordinates3D.displacement(.1), .1)

    @validationTest
    def test_CartExpanded(self):
        expansion = (np.array(
            [
                [1 / np.sqrt(6), np.sqrt(2 / 3), 1 / np.sqrt(6)],
                [1 / np.sqrt(3), -(1 / np.sqrt(3)), 1 / np.sqrt(3)],
                [1 / np.sqrt(2), 0, -(1 / np.sqrt(2))]
            ]
        ))
        system = CoordinateSystem(
            basis=CartesianCoordinates3D,
            matrix=expansion
        )
        disp = system.displacement(.1)
        self.assertEquals(disp, .1)
        # self.assertEquals(disp.shape, (3,))

    @validationTest
    def test_SphericalCoords(self):

        coord_set = CoordinateSet(DataGenerator.multicoords(1, 10))
        crds = coord_set.convert(SphericalCoordinates, use_rad=False)
        old = crds.convert(coord_set.system, use_rad=False)
        newnew = old.convert(SphericalCoordinates, use_rad=False)

        self.assertAlmostEquals(np.sum(newnew - crds)[()], 0.)
        self.assertAlmostEquals(np.sum(coord_set - old)[()], 0.)

        # self.assertAlmostEquals(np.sum(coord_set.jacobian(new)[:, 0].reshape(30, 30) + np.eye(30, 30)), 0.)

    @validationTest
    def test_CustomConversion(self):

        def invert(coords, **opts):
            return -coords, opts

        new = CompositeCoordinateSystem.register(CartesianCoordinates3D, invert, pointwise=False, inverse_conversion=invert)
        coord_set = CoordinateSet(DataGenerator.multicoords(5, 10))
        crds = coord_set.convert(new)
        old = crds.convert(coord_set.system)

        self.assertEquals(np.sum(crds + coord_set), 0.)
        self.assertEquals(np.sum(coord_set - old), 0.)

        self.assertAlmostEquals(np.sum(coord_set.jacobian(new)[:, 0].reshape(30, 30) + np.eye(30, 30)), 0.)

    @validationTest
    def test_ChainCustomConversion(self):
        def invert(coords, **opts):
            return -coords, opts

        new = CompositeCoordinateSystem.register(SphericalCoordinates, invert, pointwise=False, inverse_conversion=invert)
        coord_set = CoordinateSet(DataGenerator.multicoords(5, 10))
        crds = coord_set.convert(new)
        old = crds.convert(coord_set.system)

        self.assertAlmostEqual(np.sum(coord_set - old)[()], 0.)

        # self.assertAlmostEquals(np.sum(coord_set.jacobian(new)[:, 0].reshape(30, 30) + np.eye(30, 30)), 0.)

    @debugTest
    def test_GenerateZMatrix(self):
        zmat = [
                    [0, -1, -1, -1],
                    [1,  0, -1, -1],
                    [2,  0,  1, -1],
                    [3,  1,  2,  0]
                ]
        coords = extract_zmatrix_internals(zmat)
        print(coords)
        for zm in enumerate_zmatrices(coords): print(zm)


    @validationTest
    def test_GenericInternals(self):
        import Psience as psi
        test_root = os.path.join(os.path.dirname(psi.__file__), "ci", "tests", "TestData")
        from Psience.Molecools import Molecule

        coords = Molecule.from_file(
            os.path.join(test_root, "nh3.fchk")
        ).coords

        new_coords = CoordinateSet(coords).convert(
            GenericInternalCoordinates,
            specs=[
                (0, 1),
                (0, 2),
                (0, 3),
                (1, 0, 2),
                (1, 0, 3),
                (2, 0, 3)
            ]
        )
        new_coords = new_coords + np.array([0, 0, 0, .2, 0, 0])

        raise Exception(
            coords - new_coords.convert(CartesianCoordinates3D)
        )
    #endregion
