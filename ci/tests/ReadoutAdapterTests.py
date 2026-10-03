"""Readout adapters in the per-module ``Readouts`` packages, reached through ``to_readout`` hooks."""
import io
import json
import os
import shutil
import tempfile
import unittest
import warnings
import zipfile

import numpy as np

from McUtils.Jupyter import Readout, ReadoutSection, ReadoutHTML, ReadoutText, to_readout, register_readout, \
    find_readout_adapter, mask_secrets, as_readout_node

warnings.filterwarnings("ignore")
TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "TestData")


def data(name):
    return os.path.join(TEST_DATA, name)


def section_ids(readout):
    return [c.id for c in readout.children]


def flat(readout, suffix):
    """The exported array whose flat key ends with ``suffix`` (exports are ``(arrays, metadata)``)."""
    arrays = readout.to_flat_data()[0]
    hits = [k for k in arrays if k.endswith(suffix)]
    if len(hits) != 1:
        raise KeyError(f"{suffix!r} matches {hits}")
    return arrays[hits[0]]


def problems(readout):
    return [(p, n.meta) for p, n in readout.walk() if n.meta.get("error")]


class _Exports:
    def assertExports(self, r):
        """Every renderer runs and the data export round-trips."""
        self.assertFalse(problems(r), problems(r))
        self.assertTrue(r.to_text())
        html = r.to_html()
        self.assertIn("<html", html.lower() if isinstance(html, str) else str(html).lower())
        buf = io.BytesIO()
        r.to_pptx(buf)
        with zipfile.ZipFile(io.BytesIO(buf.getvalue())) as z:
            self.assertTrue(any(n.startswith("ppt/slides/slide") for n in z.namelist()))
        json.loads(r.to_json())


class ElectronicStructureReadoutTests(unittest.TestCase, _Exports):
    def test_gaussian_log_hook(self):
        from McUtils.ExternalPrograms.Parsers import GaussianLogReader
        r = GaussianLogReader(data("water_freq.log")).to_readout()
        for s in ("summary", "structure", "vibrations"):
            self.assertIn(s, section_ids(r))
        np.testing.assert_allclose(flat(r, "vibrations/modes/frequency"), [1622.3029, 3803.3006, 3937.5256])
        self.assertExports(r)

    def test_fchk_and_qchem(self):
        from McUtils.ExternalPrograms.Parsers import GaussianFChkReader, QChemLogReader
        self.assertIn("hessian", section_ids(GaussianFChkReader(data("water_freq.fchk")).to_readout()))
        self.assertIn("energies", section_ids(QChemLogReader(data("qchem_samp.out")).to_readout()))

    def test_scan_log(self):
        from McUtils.ExternalPrograms.Parsers import GaussianLogReader
        r = GaussianLogReader(data("water_OH_scan.log")).to_readout()
        self.assertIn("scan", section_ids(r))
        self.assertFalse(problems(r))


class StructureReadoutTests(unittest.TestCase, _Exports):
    def test_cube(self):
        from McUtils.ExternalPrograms.Parsers import CubeFileParser
        r = CubeFileParser(data("samp.cube")).to_readout()
        self.assertEqual(section_ids(r)[:2], ["grid", "atoms"])
        self.assertExports(r)

    def test_cif(self):
        from McUtils.ExternalPrograms.Parsers import CIFParser
        r = CIFParser(data("samp.cif")).to_readout()
        self.assertIn("cell", section_ids(r))
        self.assertFalse(problems(r))

    def test_xyz_with_indented_counts(self):
        from McUtils.Parsers import XYZParser
        with XYZParser(data("crest_conformers.xyz")) as p:
            frames = p.parse()
        self.assertGreater(len(frames), 1)
        r = XYZParser(data("traj.xyz")).to_readout()
        self.assertIn("trajectory", section_ids(r))

    def test_registered_records(self):
        from McUtils.ExternalPrograms.Parsers import CRESTParser
        from McUtils.ExternalPrograms.Conformers import ConformerRecord
        conf = CRESTParser(TEST_DATA).parse_conformers()
        self.assertIsNotNone(find_readout_adapter(conf))
        r = to_readout(conf)
        self.assertIn("energies", section_ids(r))
        rec = ConformerRecord("O", ["O", "H", "H"], np.array([[0, 0, .22], [0, 1.43, -.9], [0, -1.43, -.9]]),
                              [[0, 1, 1], [0, 2, 1]], -76.2, "rdkit", {})
        self.assertIsNotNone(find_readout_adapter(rec))
        self.assertFalse(problems(to_readout(rec)))


class RunReadoutTests(unittest.TestCase, _Exports):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_log_series(self):
        from McUtils.Scaffolding import Logger, LogParser
        lf = os.path.join(self.dir, "run.log")
        log = Logger(lf)
        for i in range(5):
            with log.block(tag=f"Iteration {i}"):
                log.log_print(f"Energy: {-1. - i:.3f}")
        r = LogParser(lf).to_readout()
        self.assertIn("values", section_ids(r))
        self.assertEqual(len(flat(r, "blocks/tag")), 5)
        np.testing.assert_allclose(flat(r, "values/energy"), -1. - np.arange(5))
        self.assertExports(r)

    def test_checkpoint_is_indexed_without_loading(self):
        from McUtils.Scaffolding import NumPyCheckpointer
        from McUtils.Scaffolding.Readouts import npz_index
        f = os.path.join(self.dir, "chk.npz")
        c = NumPyCheckpointer(f)
        with c:
            c["coords"] = np.zeros((4, 3))
            c["meta"] = {"n": 3}
        keys = {k.replace("::>|<::", "/") for k, *_ in npz_index(f)}
        self.assertEqual(keys, {"coords", "meta/n"})
        r = c.to_readout(include=["summary", "contents", "selected"], selected={"show": ["coords"]})
        self.assertExports(r)

    def test_job_masks_secrets(self):
        from McUtils.Scaffolding import Job
        j = Job(self.dir, job_parameters={"basis": "sto-3g", "api_token": "abc123"})
        with j:
            pass
        text = j.to_readout().to_text()
        self.assertIn("sto-3g", text)
        self.assertEqual(mask_secrets({"api_token": "abc123"})["api_token"], "••••")

    def test_options_routing(self):
        from McUtils.Devutils import OptionsSet

        def f(x, tol=1e-8): pass

        r = OptionsSet(tol=1e-6, colour="red", password="x").to_readout(targets=[f])
        self.assertIn("routing", section_ids(r))
        self.assertNotIn("password=x", r.to_text())


class OptimizationReadoutTests(unittest.TestCase, _Exports):
    def test_minimize_and_polyfit(self):
        from McUtils.Numputils.Optimization import iterative_step_minimize, NewtonStepFinder, polyfit_minima
        from McUtils.Numputils.Readouts import OptimizationRun
        f = lambda x, mask=None: np.sum((np.asarray(x) - 1) ** 2, axis=-1)
        g = lambda x, mask=None: 2 * (np.asarray(x) - 1)
        h = lambda x, mask=None: np.broadcast_to(2 * np.eye(2), np.asarray(x).shape[:-1] + (2, 2))
        guess = np.array([[0., 0.], [2., 3.]])
        res = iterative_step_minimize(guess, NewtonStepFinder(f, g, h, line_search=False), return_trajectory=True,
                                      max_iterations=20, tol=1e-8, logger=False)
        run = OptimizationRun.from_step_result(res, guess=guess, function=f)
        self.assertTrue(np.all(run.converged))
        r = run.to_readout()
        self.assertIn("paths", section_ids(r))
        self.assertExports(r)
        x = np.linspace(-1, 1, 9)
        r2 = OptimizationRun.from_critical_points(polyfit_minima(x, (x - .3) ** 2), x, (x - .3) ** 2).to_readout()
        self.assertAlmostEqual(float(flat(r2, "result/x0")[0]), .3, places=6)


class ProfilerReadoutTests(unittest.TestCase):
    def test_profile_and_timer(self):
        from McUtils.Profilers import BlockProfiler, Timer
        p = BlockProfiler.profiler(name="block", mode="deterministic", print_res=False)
        with p:
            sum(np.arange(1000) ** 2)
        r = p.to_readout(functions={"top": 5})
        self.assertIn("functions", section_ids(r))
        t = Timer(print_times=0, file=io.StringIO())
        with t:
            t.log()
            t.log()
        self.assertIn("laps", section_ids(t.to_readout()))


class ViewReadoutTests(unittest.TestCase):
    def test_graphics_and_composition(self):
        import McUtils.Plots as plt
        from McUtils.Jupyter import JHTML
        p = plt.Plot([0, 1, 2], [0, 1, 4])
        r = p.to_readout(include=["view", "details"])
        self.assertEqual(section_ids(r), ["view", "details"])
        sec = ReadoutSection.compose(p.to_readout(), JHTML.HTML.Div(JHTML.HTML.B("hi")))
        self.assertEqual(sec.children[0].children[0].kind, "plot")  # one-section readouts flatten
        html_node = as_readout_node(JHTML.HTML.Div(JHTML.HTML.B("visible text")))
        self.assertIsInstance(html_node, ReadoutHTML)
        self.assertEqual(html_node.text_content(), "visible text")
        self.assertIn("visible text", Readout(ReadoutSection(html_node, id="s")).to_text())


if __name__ == "__main__":
    unittest.main()
