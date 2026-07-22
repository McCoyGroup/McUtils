"""Extracted from ExtensionsTests.test_SharedLibrary via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExtensionsTests.test_SharedLibrary"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Extensions import *
from McUtils.Data import *
import sys, os, numpy as np

class ExtensionsTests(TestCase):

    @validationTest
    def test_SharedLibrary(self):
        lib_file = TestManager.test_data('libmbpol.so')
        mbpol = SharedLibrary(lib_file, get_pot=dict(name='calcpot_', nwaters=(int,), energy=(float,), coords=[float], return_type=None, defaults={'energy': 0}, return_handler=lambda r, kw: SharedLibraryFunction.uncast(kw['energy']) / 627.5094740631), get_pot_grad=dict(name='calcpotg_', nwaters=(int,), energy=(float,), coords=[float], grad=[float], return_type=None, prep_args=lambda kw: [kw.__setitem__('grad', np.zeros(kw['nwaters'] * 9)), kw][1], defaults={'grad': None, 'energy': 0}, return_handler=lambda r, kw: {'grad': kw['grad'].reshape(-1, 3) / 627.5094740631, 'energy': SharedLibraryFunction.uncast(kw['energy']) / 627.5094740631}))
        water = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
        self.assertGreater(mbpol.get_pot_grad(nwaters=1, coords=water)['energy'], 0.005)
        self.assertEquals(mbpol.get_pot_grad(nwaters=1, coords=water)['grad'].shape, (3, 3))
        water = np.array([[-0.063259, -0.25268, 0.2621], [0.74277, 0.26059, 0.17009], [-0.67951, -0.0079118, -0.43219]])
        self.assertGreater(mbpol.get_pot_grad(nwaters=1, coords=water)['energy'], 0.0006)
        self.assertEquals(mbpol.get_pot_grad(nwaters=1, coords=water)['grad'].shape, (3, 3))
        water = np.array([[-0.0044590985, -0.0513425796, 1.58138e-05], [0.9861302114, -0.0745730984, 5.4324e-06], [-0.1597470923, 0.8967180895, -1.64932e-05]])
        self.assertGreater(mbpol.get_pot_grad(nwaters=1, coords=water)['energy'], 0.001)
        self.assertEquals(mbpol.get_pot_grad(nwaters=1, coords=water)['grad'].shape, (3, 3))
