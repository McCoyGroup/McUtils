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
    @validationTest
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

        print()
        vendor = SMILESSupplier(TestManager.test_data('pubchem_partial_50000.smi'))
        print(vendor.find_smi(0))
        print(vendor.find_smi(1))

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

        print(sm1[:5])
        self.assertListEqual(sm1, sm2)

    @validationTest
    def test_QM9(self):
        supplier = QM9(os.path.expanduser("~/Documents/Postdoc/datasets/qm9.npz"))
        print(
            supplier.load_data(0)
        )

    @validationTest
    def test_SBatchFromPython(self):
        import os
        os.chdir("/Users/Mark/Desktop")
        woof, script_file = sbatch_python_job(print, 1, 2, 3)

        print(woof.format())
        print(script_file.resolve_buffer())

    @validationTest
    def test_PubChemAPI(self):
        api = PubChemAPI()
        print(
            api.get_compounds_by_name('melatonin')
        )

    @validationTest
    def test_SingularityRun(self):
        import shlex

        sing = SingularityLauncher(
            "/scratch/images/myapp.sif",  # image
            "python", "-m", "myapp",  # command + args
            mode='exec',
            env={
                "PYTHONPATH": "/work/src:/work/libs",
                "PYTHONUNBUFFERED": "1",
            },
            bind={
                "/home/me/project/src": "/work/src",
                "/home/me/project/libs": "/work/libs",
                "/home/me/project/out": "/work/out",
            },
            bind_sources=['Psience'],
            pwd="/work",
            cleanenv=True,  # start from a clean container env
        )
        print(shlex.join(sing.get_launch_command()))

    @validationTest
    def test_DockerRun(self):
        import shlex

        docker = DockerLauncher(
            "python:3.12-slim",  # image
            "python", "-m", "myapp",  # entrypoint command + args
            rm=True,
            env={
                "PYTHONPATH": "/work/src:/work/libs",
                "PYTHONUNBUFFERED": "1",
            },
            volume={
                "/home/me/project/src":"/work/src:ro",  # local src, read-only
                "/home/me/project/libs":"/work/libs:ro",  # local libs, read-only
                "/home/me/project/out":"/work/out",  # writable output dir
            },
            workdir="/work",
        )
        print(shlex.join(docker.get_launch_command()))

    @validationTest
    def test_ServerPackage(self):
        SLURMClient.create_server_package("/Users/Mark/Desktop", overwrite=True)

    @validationTest
    def test_CubeParser(self):
        from Psience.Molecools import Molecule
        # with CubeFileParser(TestManager.test_data('samp.cube')) as parser:
        #     pprint.pprint(parser.parse())

        eval = CubePropEvaluator.from_file(TestManager.test_data('samp.cube'))
        surf = eval.get_isosurface(0.2)
        surf2 = eval.get_isosurface(-0.2)
        mol = Molecule(eval.base_data.atoms.numbers,
                       eval.base_data.atoms.positions)

        fig = mol.plot(backend='x3d')
        surf.plot(figure=fig, transparency=.4, line_color=None)
        surf2.plot(figure=fig, color='yellow', transparency=.4, line_color=None)
        fig.show()
        return

        eval = CubePropEvaluator.from_file('/Users/Mark/Downloads/h2o.mol2.cube')
        mol = Molecule(eval.base_data.atoms.numbers,
                       eval.base_data.atoms.positions)

        fig = mol.plot(backend='x3d')
        surf = mol.get_surface(samples=200)
        tri = surf.get_triangulation()
        tri.plot(solid=False, figure=fig,
                 vertex_values=eval.evaluate(tri.verts),
                 transparency=.5)
        fig.show()

    @validationTest
    def test_OBGen3D(self):
        from Psience.Molecools import Molecule

        mol = OBMolecule.from_string("CO[C]12C[C@@](C=C1)(c1ccc(F)cc1)CC2", "smi")#, conformer_generator='gen3d')
        # print(mol.coords)
        # Molecule.from_openbabel(mol).plot().show()
        mol.draw(use_coords=True).show()

    @debugTest
    def test_SMILESManip(self):
        from Psience.Molecools import Molecule
        from McUtils.Data import SMILESData

        print(
            SMILESData.scaffold('coumarin_3_7_diyl')
        )
        print(
            SMILESData.functional_group('phenyl')
        )


        smi = join_smiles_fragments(
            SMILESData.scaffold('coumarin_3_7_diyl'),
            SMILESData.functional_group('phenyl'),
            break_aromaticity='scaffold'
        )
        print(smi)
        Molecule.from_string(smi).plot(highlight_atoms=[0, 1]).show()
        return

        diene = '[C:1]([C:5]2)[C:3]=[C:4][C:2]2'
        dienophile = 'O=C1NC(=O)[C:2]=[C:1]1'

        cache = {}
        dienophile = set_smiles_bond_order(dienophile, 0, 1, 1, cache=cache)
        template = join_smiles_fragments(diene, dienophile, [[0, 0], [1, 1]],
                                         cache=cache,
                                         add_implicit_hydrogens='full',
                                         break_aromaticity=True)
        map_data1 = parse_smiles_and_atom_map(diene, cache=cache, add_implicit_hydrogens='full')
        offset = len(map_data1['map'])
        template = renumber_smiles_atom_map(template, {offset: 2, offset + 1: 3},
                                 cache=cache,
                                 add_implicit_hydrogens='full')

        Molecule.from_string(template).plot(highlight_atoms=[0, 1, 2, 3]).show()