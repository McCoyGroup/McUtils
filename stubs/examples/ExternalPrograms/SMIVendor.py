"""Extracted from ExternalProgramsTest.test_SMIVendor via McUtils.Docs.ExamplesParser -- not the original file, and may reference test-only setup/state. Run with: python -m unittest ExternalProgramsTest.test_SMIVendor"""

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.ExternalPrograms import *
from McUtils.Data import UnitsData
from McUtils.Profilers import Timer
import sys, os, numpy as np, pprint

class ExternalProgramsTest(TestCase):

    class BoringEvaluators(EvaluationHandler):

        def add_vals(cls, coords, **kwargs):
            return np.sum(coords, axis=0)

        def get_evaluators(self) -> 'dict[str,method]':
            return {'add': self.add_vals}

    @staticmethod
    def _echo(arg):
        return arg

    @validationTest
    def test_SMIVendor(self):
        samp = TestManager.test_data('a2bbb-substances.smi')
        vendor = SMILESSupplier(samp)
        print()
        vendor = SMILESSupplier(TestManager.test_data('pubchem_partial_50000.smi'))
        print(vendor.find_smi(0))
        print(vendor.find_smi(1))
        vendor = SMILESSupplier(TestManager.test_data('pubchem_partial_50000.smi'))
        lix = vendor.create_line_index()
        vendor.save_line_index(TestManager.test_data('pubchem_partial_50000_idx.npy'), lix)
        print()
        vendor = SMILESSupplier(TestManager.test_data('pubchem_partial_50000.smi'), line_indices=TestManager.test_data('pubchem_partial_50000_idx.npy'))
        with Timer('serial'):
            sm1 = match_smiles_supplier(vendor, 'C=C')
        with Timer('parale'):
            sm2 = match_smiles_supplier(vendor, 'C=C', pool=4)
        print(sm1[:5])
        self.assertListEqual(sm1, sm2)
