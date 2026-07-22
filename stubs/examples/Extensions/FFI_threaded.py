"""Extracted from ExtensionsTests.test_FFI_threaded via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExtensionsTests.test_FFI_threaded"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Extensions import *
from McUtils.Data import *
import sys, os, numpy as np

class ExtensionsTests(TestCase):

    @debugTest
    def test_FFI_threaded(self):
        lib_dir = TestManager.test_data('LegacyMBPol')
        mbpol = FFIModule.from_lib(lib_dir, extra_link_args=['-mmacosx-version-min=12.0'])
        from Peeves.Timer import Timer
        waters = np.array([[[0, 0, 0], [1, 0, 0], [0, 1, 0]], [[-0.063259, -0.25268, 0.2621], [0.74277, 0.26059, 0.17009], [-0.67951, -0.0079118, -0.43219]], [[-0.0044590985, -0.0513425796, 1.58138e-05], [0.9861302114, -0.0745730984, 5.4324e-06], [-0.1597470923, 0.8967180895, -1.64932e-05]]] * 2500)
        with Timer(tag='Threaded'):
            res = mbpol.get_pot(nwaters=1, coords=waters, threading_var='coords')
            print(np.mean(res))
        with Timer(tag='Unthreaded'):
            res = np.array([mbpol.get_pot(nwaters=1, coords=w) for w in waters])
            print(np.mean(res))
