import tempfile

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

    @validationTest
    def test_SMILESManip(self):
        from Psience.Molecools import Molecule
        from McUtils.Data import SMILESData
        from McUtils.ExternalPrograms import build_templated_smiles

        prod = build_templated_smiles(
            SMILESData.functional_group('carbamate'),
            {
                'functional_group':SMILESData.functional_group('imine'),
                'new_bonds':[
                    [0, 1],
                    [1, 0]
                ],
                'push_bonds':True
            }
        )
        print(prod)

        Molecule.from_string(prod).plot().show()

    @validationTest
    def test_SMILESScaffoldGenerator(self):
        from Psience.Molecools import Molecule

        prod = build_templated_smiles(
            'C1CCCC=1',
            {
                'functional_group':"[O:1]",
                'bond_order':2
            },
            {
                'functional_group':"[S:1]",
                'bond_order':2
            },
            active_sites={1:0, 2:2, 3:1},
            atom_replacements={2:'N'},
            remove_sites=True
        )

        print(prod)
        # Molecule.from_string(base_scaff).plot().show()
        Molecule.from_string(prod).plot().show()

    @validationTest
    def test_RandomSMILESManip(self):
        from Psience.Molecools import Molecule
        from McUtils.Data import SMILESData
        scaff = SMILESData.random_scaffold()
        fg = SMILESData.random_functional_group()

        smi = join_smiles_fragments(
            scaff,
            fg,
            # push_bonds='scaffold',
            # resanitize=False
        )
        print(scaff)
        print(fg)
        print(smi)
        Molecule.from_string(smi).plot(highlight_atoms=[0, 1]).show()
        return

    @validationTest
    def test_AromaticSMILESManip(self):
        from Psience.Molecools import Molecule
        diene = '[C:1]([C:5]2)[C:3]=[C:4][C:2]2'
        dienophile = 'O=C1NC(=O)[C:2]=[C:1]1'

        cache = {}
        dienophile = set_smiles_bond_order(dienophile, 0, 1, 1, cache=cache)
        template = join_smiles_fragments(diene, dienophile, [[0, 0], [1, 1]],
                                         cache=cache,
                                         add_implicit_hydrogens='full',
                                         push_bonds=True)
        map_data1 = parse_smiles_and_atom_map(diene, cache=cache, add_implicit_hydrogens='full')
        offset = len(map_data1['map'])
        template = renumber_smiles_atom_map(template, {offset: 2, offset + 1: 3},
                                            cache=cache,
                                            add_implicit_hydrogens='full')

        Molecule.from_string(template).plot(highlight_atoms=[0, 1, 2, 3]).show()

    @validationTest
    def test_SMILESBipy(self):
        from Psience.Molecools import Molecule
        from McUtils.Data import SMILESData
        from McUtils.ExternalPrograms import build_templated_smiles
        import McUtils.Plots as plt

        prod = build_templated_smiles(
            SMILESData.functional_group('ketone'),
            SMILESData.functional_group('imine'),
            {
                'functional_group': SMILESData.functional_group('carbamate'),
                'new_bonds': [
                    [1, 0],
                    [2, 1]
                ]
            },
            SMILESData.scaffold('m_phenylene'),
        )
        print(prod)

        def darken(id, cls, opts):
            if 'color' in opts:
                opts['color'] = plt.prep_color(opts['color'], lighten=-.1)
            return opts
        mol = Molecule.from_string(prod)
        fig = mol.plot(
            backend='svg3D',
            # atom_text={7:'asdasd'},
            # display_atom_numbers=True,
            highlight_atoms=[0, 9, 15, 4],
            draw_coords={
                (9, 0, 15):{},
                (4, 0, 9):{},
                (4, 0):{'line_color':"red"}
            },
            principle_axes=True,
            # reflectiveness=1,
            # roughness=.2,
            # metallic=.6
            theme='simple'
            # theme_function=darken
        )
        # iso = mol.get_surface().get_triangulation(method='isosurface',
        #                                           probe_radius=1,
        #                                           probe_type='ses',
        #                                           grid_samples=50)
        # fig = iso.plot(figure=fig, transparency=.8, line_color=None)
        fig.show()
        # fig.savefig('/Users/Mark/Desktop/whack.svg')
        # fig.savefig('/Users/Mark/Desktop/whack.glb')

    @validationTest
    def test_BindingSites(self):
        from Psience.Molecools import Molecule
        from McUtils.Data import SMILESData
        import McUtils.Plots as plt

        print(
            smiles_binding_sites(SMILESData.scaffold('m_phenylene'))
        )
        print(
            smiles_binding_sites("C=CC(O)(O)c1ccccc1")
        )

        # Molecule.from_string(
        #     "C=CC(O)(O)c1ccccc1"
        # ).plot().show()

    @validationTest
    def test_SmilesChiralities(self):
        print(
            build_templated_smiles(
                '[C:1]=[C:2]',
                '[C:1]C(C)(C)(C)',
                '[C:1]C(C)(C)(C)',
                stereos={(0, 1):'cis'}
            )
        )

        print(
            w := build_templated_smiles(
                '[C:1]=[C:2]',
                '[C:1]C(C)(C)(C)',
                '[C:1]C(C)(C)(C)',
                stereos={(0, 1): 'trans'}
            )
        )

        print(
            build_templated_smiles(
                w,
                stereos={(0, 1): 'cis'}
            )
        )

        print(
            build_templated_smiles(
                w,
                stereos={(0, 1): 'any'}
            )
        )

    @validationTest
    def test_SmilesTokens(self):
        from Psience.Molecools import Molecule
        import base64

        smi0, i0, b0 = build_templated_smiles(
            '[C:1]=[C:2]',
            '[C:1]C(C)(C)(C)',
            '[C:1]C(C)(C)(C)',
            stereos={(0, 1): 'cis'},
            return_fragment_indices=True,
            return_new_bonds=True
        )
        print(b0)
        # print(smi0)
        # print(i0)
        # return
        # smi = remove_smiles_binding_sites(smi)
        mol0 = Molecule.from_string(smi0)

        for encoding in [16, 32, 64, 85]:
            print("==="*10, encoding, "==="*10)
            RDMolecule.default_tag_byte_encoding = encoding
            smi2 = mol0.to_string('smi', remove_hydrogens=True, include_tag=True)
            smi, tag = smi2.split('_', 1)
            tokens = list(SMILESTokenizer().tokenize(smi))
            print()
            print("Atoms:", len(tokens))
            print("SMI:", len(smi))
            print(smi)
            print("Tag:", len(tag))
            print(tag)
            # print("Bytes:", len(base64.b64decode(tag.encode('utf-8'))))
            mol2 = Molecule.from_string(smi2, 'smi').get_embedded_molecule(ref=mol0, sel=list(range(4)))
            print(mol2.get_rmsd(mol0, sel=list(range(4))))
            # f1 = mol.plot(backend='x3d')
            # mol2.plot(backend='x3d', figure=f1, highlight_atoms=True)
            # mol2.plot(backend='x3d', display_atom_numbers=True).show()
            # f1.show()


    @validationTest
    def test_SMIToDB(self):
        samp = TestManager.test_data('a2bbb-substances.smi')
        vendor = SMILESSupplier(samp)
        with tempfile.NamedTemporaryFile() as db_file:
            db_file = db_file.name
            vendor.write_database_index(db_file, overwrite=True)
            vendor2 = SMILESSupplier.from_line_index_database(db_file)
            with vendor2:
                self.assertEqual(
                    vendor2.find_smi(88),
                    vendor.find_smi(88)
                )

    @validationTest
    def test_QChemJob(self):
        samp = TestManager.test_data('a2bbb-substances.smi')
        mol = RDMolecule.from_smiles(
            SMILESSupplier(samp).find_smi(68),
            add_implicit_hydrogens=True
        )

        huh = QChemJob(
                          "sp",
                          method="wb97x-d", basis_set="def2-svp",
                          atoms=mol.atoms, cartesians=mol.coords,
                          memory="8GB",
                          custom_basis="H     0\nS   3   1.00\n...\n****",  # raw $basis body
                          xc_functional="X wb97x_v 1.0\nC wb97x_v 1.0",  # raw $xc_functional body
                          plots="Some 3-D mesh spec...",
        )
        print(
            huh.format()
        )

    @validationTest
    def test_TemplatedSmilesIterator(self):
        BASE_DIENES = {
            'cyclopentadiene': '[C:1]([C:5]2)[C:3]=[C:4][C:2]2',
            'butadiene': '[C:1][C:5]=[C:6][C:2]',
            '1-N-butadiene': '[C:1][C:5]=[N:6][C:2]',
            '2-N-butadiene': '[C:1][C:5]=[C:6][N:2]',
            '2-O-butadiene': '[C:1][C:5]=[C:6][O:2]',
            'anthracene': '[c:1]3c1ccccc1[c:2]c2ccccc23',
            'anthracene-side': 'c12c(cc3ccccc3c1)[C:2]1[C:1]2C=C1',
            'naphthalene': 'c1ccc2[c:1]cc[c:2]c2c1'
        }

        BASE_DIENOPHILES = {
            'maleamide': 'O=C1NC(=O)[C:2]=[C:1]1',
            'ethene': '[C:1]=[C:2]',
            'CN': '[C:1]=[N:2]',
            'CO': '[C:1]=[O:2]',
        }

        BASE_TEMPLATES = {
            'cyclopentadiene': '[C:3]1[C:1]([C:7]2)[C:5]=[C:6][C:2]2[C:4]1',
            'butadiene': '[C:3]1[C:1][C:5]=[C:6][C:2][C:4]1',
            '1-N-butadiene': '[C:3]1[C:1][C:5]=[N:6][C:2][C:4]1',
            '2-N-butadiene': '[C:3]1[C:1][C:5]=[C:6][N:2][C:4]1',
            '2-O-butadiene': '[C:3]1[C:1][C:5]=[C:6][O:2][C:4]1',
            'butadiene-N': '[C:3]1[C:1][C:5]=[C:6][C:2][N:4]1',
            'butadiene-O': '[C:3]1[C:1][C:5]=[C:6][C:2][O:4]1',
            'anthracene': '[C:3]4[C:1]3c1ccccc1[C:2]([C:4]4)c2ccccc23',
            'anthracene-side': 'c12c(cc3ccccc3c1)[C:2]1[C:4][C:3][C:1]2C=C1',
            'dp-ibf': '[C:1]12(c3ccccc3)[C:3][C:4][C:2](c3ccccc3)(c3c1cccc3)O2',
            'dmfdc': '[C:1]12[C:3][C:4][C:2](C(C(OC)=O)=C1C(OC)=O)O2',
            'naphthalene': '[C:1]12[C:3][C:4][C:2](C=C1)c1c2cccc1'
        }

        BASE_FRAGMENTS = {
            'sulfonyl': '[S:1](=O)=O',
            'sulfonyl-phenyl': '[S:1](=O)(c1ccccc1)=O',
            'sulfonyl-chex': '[S:1](=O)(C1CCCCC1)=O',
            'pF-phenyl': '[c:1]1ccc(F)cc1',
            'OMe': '[O:1]C',
            'CN': '[C:1]N',
            'acetamide': '[C:1]C(=O)N',
            'methyl': '[C:1]',
            'carboxyl': '[C:1]C(=O)O',
            'tBu': '[C:1](C)(C)(C)',
            'MetBu': '[C:1]C(C)(C)(C)'
        }

        self.template = BASE_TEMPLATES['cyclopentadiene']
        self.frags = [BASE_FRAGMENTS['CN'], BASE_FRAGMENTS['sulfonyl-phenyl']]

        import rdkit.Chem.AllChem as Chem
        def _canon_set(smis):
            return {Chem.CanonSmiles(s) for s in smis}

        # the two substituent attachment points on every BASE_TEMPLATES scaffold
        ACTIVE_SITES = [2, 3]

        
        tests = []
        
        def register_test(test):
            tests.append(test)
            return test
        
        @register_test
        def test_basic_enumeration_count_and_validity(self):
            # 2 fragments chosen with repetition for 2 sites -> C(2+2-1, 2) = 3
            products = list(templated_smiles_iterator(self.template, self.frags, ACTIVE_SITES))
            self.assertEqual(len(products), 3)
            for smi in products:
                mol = Chem.MolFromSmiles(smi)
                self.assertIsNotNone(mol, f"invalid SMILES produced: {smi}")

        @register_test
        def test_products_are_all_distinct(self):
            products = list(templated_smiles_iterator(self.template, self.frags, ACTIVE_SITES))
            self.assertEqual(len(products), len(set(products)))
            self.assertEqual(len(_canon_set(products)), len(products))

        @register_test
        def test_chirality_expansion(self):
            # 3 fragment combos x (2 windings at site 2) x (1 winding at site 3) = 6
            products = list(templated_smiles_iterator(
                self.template, self.frags, ACTIVE_SITES,
                chiralities=[['CW', 'CCW'], ['CW']],
            ))
            self.assertEqual(len(products), 6)
            for smi in products:
                self.assertIsNotNone(Chem.MolFromSmiles(smi))
            # every stereo-labeled product should be distinct
            self.assertEqual(len(set(products)), 6)

        @register_test
        def test_single_winding_shorthand(self):
            # a bare string (not a list) for a site's chirality means "always this winding"
            fixed = list(templated_smiles_iterator(
                self.template, self.frags, ACTIVE_SITES, chiralities=['CW', 'CW'],
            ))
            expanded = list(templated_smiles_iterator(
                self.template, self.frags, ACTIVE_SITES, chiralities=[['CW'], ['CW']],
            ))
            self.assertEqual(fixed, expanded)
            self.assertEqual(len(fixed), 3)

        @register_test
        def test_substitution_filter(self):
            seen = []

            def no_double_sulfonyl(template, active_sites, frags):
                seen.append(frags)
                return frags.count(BASE_FRAGMENTS['sulfonyl-phenyl']) < 2

            products = list(templated_smiles_iterator(
                self.template, self.frags, ACTIVE_SITES, filter=no_double_sulfonyl,
            ))
            # of the 3 raw combos, exactly one (sulfonyl, sulfonyl) is excluded
            self.assertEqual(len(seen), 3)
            self.assertEqual(len(products), 2)

        @register_test
        def test_remove_sites_strips_all_atom_maps(self):
            products = list(templated_smiles_iterator(
                self.template, self.frags, ACTIVE_SITES, remove_sites=True,
            ))
            for smi in products:
                self.assertNotIn(':', smi)
                self.assertIsNotNone(Chem.MolFromSmiles(smi))

        @register_test
        def test_return_fragment_indices(self):
            products = list(templated_smiles_iterator(
                self.template, self.frags, ACTIVE_SITES, return_fragment_indices=True,
            ))
            for smi, fragments in products:
                self.assertIsNotNone(Chem.MolFromSmiles(smi))
                # one index group per replacement, plus the scaffold itself
                self.assertEqual(len(fragments), 1 + len(ACTIVE_SITES))

        @register_test
        def test_atom_replacements_pass_through(self):
            # swap the ring-fusion carbons' hydrogens for a heavier halogen via
            # `atom_replacements`, forwarded straight through to
            # `build_templated_smiles`
            products = list(templated_smiles_iterator(
                self.template, [BASE_FRAGMENTS['methyl']], ACTIVE_SITES,
                atom_replacements={0: 'F'},
            ))
            self.assertTrue(products)
            for smi in products:
                mol = Chem.MolFromSmiles(smi)
                self.assertIsNotNone(mol)
                self.assertTrue(any(a.GetSymbol() == 'F' for a in mol.GetAtoms()))

        @register_test
        def test_all_templates_and_fragments_never_crash_and_stay_valid(self):
            # Sanity-check the idiom data itself, across the whole
            # templates x fragments matrix. Not every (template, fragment) pair
            # is chemically valid -- e.g. the ring *oxygen* active site in
            # 'butadiene-O' can't accept a substituent at all -- so this
            # doesn't require a product every time (the AtomValenceException
            # is caught and simply yields nothing for that pair); it only
            # requires that the iterator never raises, and that whatever it
            # *does* produce is valid.
            for name, template in BASE_TEMPLATES.items():
                for frag_name, frag in BASE_FRAGMENTS.items():
                    with self.subTest(template=name, fragment=frag_name):
                        products = list(templated_smiles_iterator(
                            template, [frag], ACTIVE_SITES,
                            quiet=True
                        ))
                        self.assertIn(len(products), (0, 1))
                        for smi in products:
                            self.assertIsNotNone(Chem.MolFromSmiles(smi))

        @register_test
        def test_carbon_active_site_templates_accept_every_fragment(self):
            # restricted to templates whose two substituent sites really are
            # generic sp3 carbons (as opposed to e.g. 'butadiene-O's ring
            # oxygen), every fragment should attach cleanly at both sites
            carbon_site_templates = [
                'cyclopentadiene', 'butadiene', '1-N-butadiene',
                '2-N-butadiene', '2-O-butadiene', 'naphthalene',
            ]
            for name in carbon_site_templates:
                template = BASE_TEMPLATES[name]
                for frag_name, frag in BASE_FRAGMENTS.items():
                    with self.subTest(template=name, fragment=frag_name):
                        products = list(templated_smiles_iterator(
                            template, [frag], ACTIVE_SITES,
                        ))
                        self.assertEqual(len(products), 1)
                        self.assertIsNotNone(Chem.MolFromSmiles(products[0]))

        @register_test
        def test_base_dienes_and_dienophiles_are_parseable(self):
            # `BASE_DIENES`/`BASE_DIENOPHILES` aren't consumed by any function
            # currently in `cmcc_reactions` (the fusion step that would turn
            # them into a `BASE_TEMPLATES`-style scaffold isn't implemented
            # there), but they're still part of the idiom's data, so just
            # confirm they're valid, atom-mapped fragments in their own right.
            for name, smi in {**BASE_DIENES, **BASE_DIENOPHILES}.items():
                with self.subTest(fragment=name):
                    mol = Chem.MolFromSmiles(smi)
                    self.assertIsNotNone(mol, f"invalid SMILES for {name!r}: {smi}")
        
        for t in tests:
            print(t.__name__)
            t(self)

    @validationTest
    def test_ConformerEnsembles(self):
        import os
        os.environ["TORCH_COMPILE_DISABLE"] = "1"

        from Psience.Molecools import Molecule
        from McUtils.Scaffolding import NumpyTreeArchive

        samp = TestManager.test_data('a2bbb-substances.smi')
        conf_lib = {}
        for i in [33, 68, 77]:
            smi = SMILESSupplier(samp).find_smi(i)
            confs, engs = generate_conformer_ensemble(
                Molecule.from_string,
                smi
            )
            conf_lib[str(i)] = {
                'smi':smi,
                'energies':engs,
                'coord':[c.coords for c in confs]
            }

        import io
        buf = io.BytesIO()
        NumpyTreeArchive.from_tree(conf_lib).save(buf)
        print(len(buf.getvalue()))

        print(confs)


        confs, energies = generate_conformer_ensemble(
            Molecule.from_string,
            SMILESSupplier(samp).find_smi(68),
            target_num_structs=5,
            preopt_iterations=5,
            optimizer_settings={
                'max_iterations': 15
            },
            energy_evaluator='aimnet2'
        )

        print(confs)
        print(energies)

    @validationTest
    def test_ConformerLibraryFromTree(self):
        import io

        os.environ["TORCH_COMPILE_DISABLE"] = "1"

        from Psience.Molecools import Molecule

        samp = TestManager.test_data('a2bbb-substances.smi')
        conf_lib = {}
        raw_confs = {}
        for i in [33, 68, 77]:
            smi = SMILESSupplier(samp).find_smi(i)
            confs, engs = generate_conformer_ensemble(Molecule.from_string, smi, energy_evaluator='rdkit')
            raw_confs[str(i)] = confs
            conf_lib[str(i)] = {
                'smi': smi,
                'coord': [c.coords for c in confs],
                'energy':engs
            }

        lib = ConformerLibrary(conf_lib)
        self.assertEqual(len(lib), 3)
        self.assertEqual(set(lib.keys()), {'33', '68', '77'})

        rec = lib['68']
        print(rec)
        self.assertEqual(rec['smi'], conf_lib['68']['smi'])
        self.assertEqual(len(rec['coord']), len(raw_confs['68']))
        for a, c in zip(rec['coord'], raw_confs['68']):
            np.testing.assert_array_equal(np.asarray(a), c.coords)

        # round trip through `save`/`from_nparchive`, same as
        # `NumpyTreeArchive.from_tree(conf_lib).save(buf)` directly
        buf = io.BytesIO()
        lib.save(buf)
        self.assertGreater(len(buf.getvalue()), 0)

        buf.seek(0)
        reloaded = ConformerLibrary.from_nparchive(buf)
        self.assertEqual(len(reloaded), 3)
        self.assertEqual(reloaded.get_smiles('33'), conf_lib['33']['smi'])
        self.assertEqual(len(reloaded['77']['coord']), len(raw_confs['77']))

    @validationTest
    def test_CreateSmilesIteratorArchive(self):
        os.environ["TORCH_COMPILE_DISABLE"] = "1"

        from Psience.Molecools import Molecule

        samp = TestManager.test_data('a2bbb-substances.smi')
        supp = SMILESSupplier(samp)
        smis = [supp.find_smi(i) for i in [33, 68, 77]]

        with tempfile.TemporaryDirectory() as tmp_dir:
            target = os.path.join(tmp_dir, "conformers.npz")
            lib, _ = ConformerLibrary.create_smiles_iterator_archive(
                smis, target,
                loader=Molecule.from_string
            )

            # the in-memory library returned directly is already usable...
            self.assertEqual(len(lib), 3)
            self.assertEqual(lib.get_smiles('0'), smis[0])
            self.assertGreater(len(lib['1']['coord']), 0)

            # ...and so is a fresh read of what actually landed on disk
            reloaded = ConformerLibrary.from_nparchive(target)
            self.assertEqual(len(reloaded), 3)
            self.assertEqual(reloaded.get_smiles('2'), smis[2])

    # -- the "mostly SMILES" paradigm ----------------------------------------

    @debugTest
    def test_ConformerLibraryFromSMILESDatabase(self):
        from Psience.Molecools import Molecule

        samp = TestManager.test_data('a2bbb-substances.smi')

        with tempfile.TemporaryDirectory() as tmp_dir:
            db_file = os.path.join(tmp_dir, "substances.tar")
            with SMILESSupplier(samp) as (supp, _):
                supp.write_database_index(db_file)

            lib = ConformerLibrary.from_smidb(db_file, loader=lambda s:Molecule.from_string(s['smi'], 'smi'))
            direct = SMILESSupplier(samp)

            for i in [33, 68, 77]:
                self.assertEqual(lib.get_smiles(i), direct.find_smi(i))
                print(lib[i])
                # self.assertEqual(lib[i]['smi'], direct.find_smi(i))
                # self.assertIsNone(lib[i]['coord'])  # no metadata_arrays packaged

    # -- QM9 ------------------------------------------------------------------

    @inactiveTest
    def test_ConformerLibraryFromQM9(self):
        lib = ConformerLibrary.qm9('qm9.npz')
        lib.get_smiles(0)

    @inactiveTest
    def test_ConformerLibraryFromGEOM(self):
        lib = ConformerLibrary.geom('geom_path')
        lib.get_smiles(0)
        # self.assertEqual(len(lib), 2)
        # self.assertEqual(lib.get_smiles(0), 'C')
        #
        # rec = lib[1]
        # self.assertEqual(rec['smi'], 'CC')
        # np.testing.assert_array_equal(rec['coord'], coords1)