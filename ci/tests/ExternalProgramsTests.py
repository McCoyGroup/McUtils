
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.ExternalPrograms import *
from McUtils.Data import UnitsData
from McUtils.Profilers import Timer
import sys, os, numpy as np, pprint

class ExternalProgramsTest(TestCase):

    # other format tests are covered in Psience.Molecools, don't really need here
    # api work is covered in Psience.PotentialRegistry
    @validationTest
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

    class BoringEvaluators(EvaluationHandler):
        def add_vals(cls, coords, **kwargs):
            return np.sum(coords, axis=0)
        def get_evaluators(self) -> 'dict[str,method]':
            return {
                "add":self.add_vals
            }


    @validationTest
    def test_EvaluationServer(self):
        connection = ('localhost', 12345)
        with GitHandler.start_multiprocessing_server(connection=connection, timeout=2):
            client = NodeCommClient(connection)
            res = client.call('pwd')
            client.print_response(res)
            res = client.call('git', 'status')
            client.print_response(res)

        with self.BoringEvaluators.start_multiprocessing_server(connection=connection, timeout=2):
            client = EvaluationClient(connection)
            res = client.call('add', np.array([[1, 2], [3, 4]]))
            if isinstance(res, dict):
               client.print_response(res)
            else:
                pprint.pprint(res)

    @staticmethod
    def _echo(arg): return arg
    @debugTest
    def test_SMIVendor(self):
        samp = TestManager.test_data('a2bbb-substances.smi')
        vendor = SMILESSupplier(samp)

        # print(vendor.find_smi(5))
        # with open(samp) as smi:
        #     for i in range(6):
        #         test = smi.readline()
        #     print(test)
        #
        # print(vendor.line_indices[:5])


        # with Timer():
        #     print(vendor.find_smi(90))
        #
        # with Timer():
        #     print(vendor.find_smi(90))
        #
        # vendor = SMILESSupplier(samp)
        # vendor.create_line_index()
        #
        # with Timer():
        #     print(vendor.find_smi(90))
        #
        # smi_list = consume_smiles_supplier(vendor, self._echo, upto=83)
        # smi_list2 = consume_smiles_supplier(vendor, self._echo, 3, upto=83)
        # self.assertListEqual(smi_list, smi_list2)

        # pubhchem = SMILESSupplier("/Users/Mark/Downloads/pubchem_cid_smi_2026_01.smi", split_idx=1)
        # subsmi = consume_smiles_supplier(pubhchem, self._echo, upto=int(5e4))
        # import McUtils.Devutils as dev
        # dev.write_file("/Users/Mark/Desktop/pubchem_partial_50000.smi", "\n".join(subsmi))
        # return

        vendor = SMILESSupplier(TestManager.test_data('pubchem_partial_50000.smi'))
        lix = vendor.create_line_index()
        vendor.save_line_index(TestManager.test_data('pubchem_partial_50000_idx.npy'), lix)

        print()
        vendor = SMILESSupplier(TestManager.test_data('pubchem_partial_50000.smi'),
                                line_indices=TestManager.test_data('pubchem_partial_50000_idx.npy'))
        with Timer("serial"):
            sm1 = match_smiles_supplier(vendor, "C=C")

        with Timer("parale"):
            sm2 = match_smiles_supplier(vendor, "C=C", pool=4)

        self.assertListEqual(sm1, sm2)