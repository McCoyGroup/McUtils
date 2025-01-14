
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.ElectronicStructure import *

class ElectronicStructureTests(TestCase):

    @debugTest
    def test_GaussianJobs(self):
        basic_gjf = GaussianJob(
                title="woof",
                Mem="200gb",
                MP2=("aug-cc-pvtz", "Direct"),
                Opt="VeryTight",
                Freq="Anharmonic",

                atoms=["O", "H", "H"],
                # cartesians=[[0, 0, 0], [-1, 0, 0], [0, 1, 0]],
                zmatrix=[
                    [1, 1],
                    [1, 1, 2, 90]
                ],
            variables={'r1':35}
            ).format()
        print(basic_gjf)

    @debugTest
    def test_OrcaJobs(self):
        orca_def2 = OrcaJob(
                MP2=("def2-TZVP", "TightSCF"),
                opts=dict(mp2={"Density":"none"}),
                tddft=dict(
                    NROOTS=5,
                    IROOT=1
                ),
                atoms=["O", "H", "H"],
                # cartesians=[[0, 0, 0], [-1, 0, 0], [0, 1, 0]],
                zmatrix=[
                    [1, 1],
                    [1, 1, 2, 90]
                ]
            ).format()
        print(orca_def2)

        orca_r2scan = OrcaJob(
                level_of_theory='r2scan',

                atoms=["O", "H", "H"],
                # cartesians=[[0, 0, 0], [-1, 0, 0], [0, 1, 0]],
                zmatrix=[
                    [1, 1],
                    [1, 1, 2, 90]
                ]
            ).format()
        print(orca_r2scan)
