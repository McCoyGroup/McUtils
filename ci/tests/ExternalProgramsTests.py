from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.ExternalPrograms import *
from McUtils.Data import UnitsData
import sys, os, numpy as np, pprint

class ExternalProgramsTest(TestCase):

    # other format tests are covered in Psience.Molecools, don't really need here
    # api work is covered in Psience.PotentialRegistry
    @debugTest
    def test_CIFFiles(self):
        print()
        with CIFParser(TestManager.test_data('samp.cif'), ignore_comments=True) as cif:
            structs = cif.parse()
            struct = next(iter(structs[0].values()))
            res = CIFConverter(struct)#.find_all('cell_*', strict=False)
            pprint.pp(res.atom_properties)
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

    @validationTest
    def test_ParseGaussianLogFile(self):
        with GaussianLogReader(TestManager.test_data('methanol_vpt_scan.log')) as parser:
            res = parser.parse(['SCFCoordinatesEnergies'])['SCFCoordinatesEnergies']

    @validationTest
    def test_ParseReports(self):
        with GaussianLogReader(TestManager.test_data('molec1_tdcis_b3lyp.log')) as parser:
            parse = parser.parse(['Reports', 'ExcitedStates'])
            res = parse['Reports']

        pprint.pprint(res)
        pprint.pprint(parse['ExcitedStates'])


        with GaussianLogReader(TestManager.test_data('water_freq.log')) as parser:
            parse = parser.parse(['Reports'])
            res = parse['Reports']

        pprint.pprint(res)

        with GaussianLogReader(TestManager.test_data('tbhp_030.log')) as parser:
            parse = parser.parse(['Reports'])
            res = parse['Reports']

        pprint.pprint(res)


        with GaussianLogReader(TestManager.test_data('water_OH_scan.log')) as parser:
            parse = parser.parse(['Reports'])
            res = parse['Reports']

        pprint.pprint(res)

    @validationTest
    def test_CRESTParse(self):

        parser = CRESTParser(TestManager.test_data_dir)

        structs = parser.parse_optimized_structures()
        print(len(structs))
        print(structs[-1].energy)
        print(len(structs[-1].atoms))
        print(len(structs[-1].coords))

        log_info = parser.parse_log()
        # import pprint
        # pprint.pprint(log_info)

        print(log_info['FinalEnsembleInfo'].weights.shape)

        print(parser.parse_conformers().coords[0].shape)
        rotamers = parser.parse_rotamers()
        print(np.sum(rotamers.weights))


    @validationTest
    def test_CRESTJob(self):
        from Psience.Molecools import Molecule


        mol = Molecule.from_file(TestManager.test_data('tbhp_180.fchk'))

        print(
            CRESTJob(
                "gfn2",
                "nci",
                ewin=10,
                # "nco",
                atoms=mol.atoms,
                cartesians=mol.coords * UnitsData.convert("BohrRadius", "Angstroms")
            ).format()
        )