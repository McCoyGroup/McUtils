"""Imports and exports must work without the removed Jupyter readout shim."""

import os
import subprocess
import sys
import tempfile
import unittest


class ReadoutImportTests(unittest.TestCase):
    def test_html_runtime_uses_the_bundled_jupyter_resource(self):
        import inspect
        from pathlib import Path
        from McUtils.Jupyter import X3DHTML
        from McUtils.Readouts import HTMLReadoutRenderer

        expected = Path(inspect.getfile(X3DHTML)).parent / "resources" / "x3dom-full.js"
        self.assertTrue(expected.is_file())
        local = HTMLReadoutRenderer(x3dom_path="local").runtime_elements()[0]
        self.assertEqual(local.attrs["src"], expected.as_uri())
        inline = HTMLReadoutRenderer(x3dom_path="inline").runtime_elements()[0].tostring()
        self.assertIn("x3dom", inline)
        self.assertGreater(len(inline), 1000)

    def test_package_import_and_layout_export_without_jupyter_readouts(self):
        code = """
import importlib.abc
import sys

class RemovedReadouts(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if '.Jupyter.Readouts' in fullname:
            raise ModuleNotFoundError('Removed readout module: ' + fullname)

sys.meta_path.insert(0, RemovedReadouts())

import McUtils
from McUtils.Jupyter import Card, Grid, JHTML
from McUtils.Readouts import Readout, ReadoutFields, ReadoutGrid

readout = Readout(Grid([[Card(ReadoutFields({'answer': 42}), header='Result')]]))
assert isinstance(readout.children[0], ReadoutGrid)
assert '42' in readout.to_text()
assert 'Result' in readout.to_html()
assert '42' in readout.to_json()
assert not any('.Jupyter.Readouts' in name for name in sys.modules)
"""
        environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
                           PYTHONPATH=os.pathsep.join(os.path.abspath(p) for p in sys.path))
        with tempfile.TemporaryDirectory() as directory:
            process = subprocess.run([sys.executable, "-B", "-c", code], cwd=directory,
                                     env=environment, capture_output=True, text=True, timeout=60)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)


if __name__ == "__main__":
    unittest.main()
