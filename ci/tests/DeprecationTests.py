from McUtils.ExternalPrograms import *

from Peeves.TestUtils import *
from unittest import TestCase
import os, subprocess, sys, warnings, importlib


class DeprecationTests(TestCase):

    def _run(self, code, mode=None):
        env = dict(os.environ)
        env.pop("MCUTILS_DEPRECATIONS", None)
        if mode is not None:
            env["MCUTILS_DEPRECATIONS"] = mode
        return subprocess.run([sys.executable, "-W", "default", "-c", code], capture_output=True, text=True, env=env)

    @debugTest
    def test_GaussianInterfaceWarnsOnUse(self):
        res = self._run(
            "from McUtils.GaussianInterface import GaussianLogReader\n"
            "from McUtils.GaussianInterface import GaussianFChkReader\n"  # second access shouldn't warn again
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(res.stderr.count("McUtilsDeprecationWarning"), 1, res.stderr)
        self.assertIn("McUtils.ExternalPrograms.Parsers", res.stderr)

    @debugTest
    def test_BareImportDoesNotWarn(self):
        res = self._run("import McUtils.GaussianInterface")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertNotIn("Deprecat", res.stderr)

    @debugTest
    def test_ErrorMode(self):
        res = self._run("from McUtils.GaussianInterface import GaussianLogReader", mode="error")
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("McUtilsDeprecationError", res.stderr)

    @debugTest
    def test_IgnoreMode(self):
        res = self._run("from McUtils.GaussianInterface import GaussianLogReader", mode="ignore")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertNotIn("Deprecat", res.stderr)

    @debugTest
    def test_SameObjects(self):
        import McUtils.GaussianInterface as old
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.assertIs(old.GaussianLogReader, GaussianLogReader)
            self.assertIs(old.GaussianFChkReader, GaussianFChkReader)
            self.assertTrue(set(old.__all__) >= {"GaussianLogReader", "GaussianFChkReader", "FchkForceConstants"})

    @debugTest
    def test_RegistryHasSchedule(self):
        from McUtils.Devutils import list_deprecations
        import McUtils.GaussianInterface as old
        old.GaussianLogReader  # register
        entry = list_deprecations()["McUtils.GaussianInterface"]
        self.assertTrue(entry["since"] and entry["remove_in"] and entry["new"])
