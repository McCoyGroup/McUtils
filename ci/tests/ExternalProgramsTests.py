from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.ExternalPrograms import *
import sys, os, numpy as np

class ExternalProgramsTest(TestCase):

    # other format tests are covered in Psience.Molecools, don't really need here
    # api work is covered in Psience.PotentialRegistry
    @validationTest
    def test_CIFFiles(self):
        import pprint
        print()
        with CIFParser(TestManager.test_data('samp.cif'), ignore_comments=True) as cif:
            structs = cif.parse()
            struct = next(iter(structs[0].values()))
            res = CIFConverter(struct)#.find_all('cell_*', strict=False)
            pprint.pp(res.cell_properties)
            # print(cif.parse())

    # @validationTest
    # def test_GaussianJob(self):
    #     job = GaussianJob(
    #         system={
    #             'zmatrix':[],
    #             'variables':[]
    #         },
    #         Opt="ZMatrix",
    #         Freq="Anh"
    #     )
    #     print()
    #     print(job.format())

    @debugTest
    def test_ParseGaussianLogFile(self):
        with GaussianLogReader('methanol_vpt_scan.log') as parser:
            res = parser.parse(['SCFCoordinatesEnergies'])['SCFCoordinatesEnergies']