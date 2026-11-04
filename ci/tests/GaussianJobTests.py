
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.ExternalPrograms.Parsers import *
import sys, os, numpy as np

class GaussianJobTests(TestCase):

    def setUp(self):
        self.test_log_water = TestManager.test_data("water_OH_scan.log")
        self.test_log_freq = TestManager.test_data("water_freq.log")
        self.test_log_opt = TestManager.test_data("water_dimer_test.log")
        self.test_fchk = TestManager.test_data("water_freq.fchk")
        self.test_log_h2 = TestManager.test_data("outer_H2_scan_new.log")
        self.test_scan = TestManager.test_data("water_OH_scan.log")
        self.test_rel_scan = TestManager.test_data("tbhp_030.log")

    @validationTest
    def test_GaussianJobWriter(self):
        job = GaussianJob(
            "water scan",
            description="Simple water scan",
            config= GaussianJob.Config(
                NProc = 4,
                Mem = '1000MB'
            ),
            job= GaussianJob.Job(
                'Scan'
            ),
            system = GaussianJob.System(
                charge=0,
                molecule=[
                    ["O", "H", "H"],
                    [
                        [0, 0, 0],
                        [.987, 0, 0],
                        [0, .987, 0]
                    ]
                ],
                vars=[
                    GaussianJob.System.Variable("y1", 0., 10., .1),
                    GaussianJob.System.Constant("x1", 10)
                ]
            ),

            footer="""
                C,O,H, 0
                6-31G(d,p)

                Rh 0
                lanl2dz
                """
        )
        # print(job.format())
        self.assertIsInstance(job.format(), str)

    @validationTest
    def test_LinkedModeScan(self):
        """
        Set up a Linked array of Gaussian jobs
        """
        import itertools as ip

        struct = np.array([
            [0,    0,    0],
            [.987, 0,    0],
            [0,    .987, 0]
        ])
        oh_modes = np.array([
            [
                [0, 0, 0],
                [1, 0, 0],
                [0, 0, 0]
            ],
            [
                [0, 0, 0],
                [0, 0, 0],
                [0, 1, 0]
            ],
        ])
        displacements = ip.product(
            [-.05, 0, .05],
            [-.05, 0, .05]
        )

        job = GaussianJobArray(
            GaussianJob(
                "normal mode scan",
                description="Simple normal mode scan",
                config=GaussianJob.Config(
                    NProc=4,
                    Mem='1000MB',
                    Chk="displacement_{}.chk".format(i)
                ),
                job=GaussianJob.Job(
                    'SinglePoint'
                ),
                system=GaussianJob.System(
                    charge=0,
                    molecule=[
                        ["O", "H", "H"],
                        struct + np.tensordot(d, oh_modes, axes=[0, 0])
                    ]
                ),
                footer="""
                        C,O,H, 0
                        6-31G(d,p)
                        
                        Rh 0
                        lanl2dz
                        """
            )
            for i, d in enumerate(displacements)
        )
        job_str = job.format()
        self.assertIsInstance(job_str, str)
        self.assertIn("--Link1--", job_str)
