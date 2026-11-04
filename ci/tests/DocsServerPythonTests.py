"""Finding the Python that launched Jupyter, installing the extension with it, and the static fallback display."""

import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
import venv
from unittest import mock


def have_widgets():
    try:
        import ipywidgets, markdown  # noqa: F401
    except ImportError:
        return False
    return True


def widgets():
    from McUtils.Jupyter.JHTML.HTMLWidgets import HTMLWidgets
    return HTMLWidgets


class ServerDetectionTests(unittest.TestCase):
    def test_server_command_lines(self):
        W = widgets()
        yes = [
            ["/v/bin/python", "/v/bin/jupyter-lab", "--no-browser"],
            ["/v/bin/python3.11", "/v/bin/jupyter-notebook"],
            ["python", "-m", "jupyterlab"],
            ["python", "-m", "jupyter_server.serverapp"],
            ["C:\\Python\\python.exe", "C:\\Python\\Scripts\\jupyter-lab.exe"],
        ]
        no = [
            ["/v/bin/python", "-m", "ipykernel_launcher", "-f", "k.json"],
            ["/v/bin/python", "/x/ipykernel_launcher.py"],
            ["bash"],
            ["python", "my_script.py"],
        ]
        for argv in yes:
            self.assertTrue(W._is_jupyter_server(argv), argv)
        for argv in no:
            self.assertFalse(W._is_jupyter_server(argv), argv)

    def test_prose_in_a_shell_command_is_not_a_server(self):
        W = widgets()
        text = "echo run python -m jupyterlab then open /home/me/notes/jupyter-lab.txt later please"
        self.assertFalse(W._is_jupyter_server(["bash", "-c", text]))

    def test_the_interpreter_of_a_command_line(self):
        W = widgets()
        self.assertEqual(W._python_of(["/v/bin/python3.11", "/v/bin/jupyter-lab"]), "/v/bin/python3.11")
        with tempfile.TemporaryDirectory() as tmp:
            launcher = os.path.join(tmp, "jupyter-lab")
            open(launcher, "w").close()
            self.assertIsNone(W._python_of([launcher]))                 # no Python beside it
            python = os.path.join(tmp, "python")
            open(python, "w").close()
            self.assertEqual(W._python_of([launcher]), python)          # a native launcher: the one beside it

    def test_a_framework_python_relaunched_from_a_venv_resolves_to_the_venv(self):
        """macOS: the server process's argv[0] is the framework ``Python.app``; the environment is the launcher script's."""
        W = widgets()
        framework = "/Library/Frameworks/Python.framework/Versions/3.10/Resources/Python.app/Contents/MacOS/Python"
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "envs", "py", "bin"))
            script = os.path.join(tmp, "envs", "py", "bin", "jupyter-lab")
            python = os.path.join(tmp, "envs", "py", "bin", "python")
            open(script, "w").close(); open(python, "w").close()
            self.assertEqual(W._python_of([framework, script, "--no-browser"]), python)
            # `python -m jupyterlab`: no script, so the recorded launcher is what names the environment
            argv = W._Argv([framework, "-m", "jupyterlab"])
            argv.pid = 123
            with mock.patch.object(W, "_launcher_of", return_value=python) as launcher:
                self.assertEqual(W._python_of(argv), python)
            launcher.assert_called_once_with(123)
            with mock.patch.object(W, "_launcher_of", return_value=None):
                self.assertEqual(W._python_of(argv), framework)         # nothing better known

    def test_the_launcher_is_read_from_the_process_environment(self):
        W = widgets()
        with tempfile.TemporaryDirectory() as tmp:
            fake = os.path.join(tmp, "python")
            open(fake, "w").close()
            env = dict(os.environ, __PYVENV_LAUNCHER__=fake)
            child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"], env=env)
            try:
                self.assertEqual(W._launcher_of(child.pid), fake)
                self.assertIsNone(W._launcher_of(os.getpid()) if "__PYVENV_LAUNCHER__" not in os.environ else None)
            finally:
                child.kill(); child.wait()

    def test_jhtml_exposes_the_server_python_tools(self):
        try:
            from McUtils.Jupyter import JHTML
        except ImportError:
            self.skipTest("ipywidgets not installed")
        W = widgets()
        for name in ("server_environment", "jupyter_python", "install_command", "install_script",
                     "extension_locations", "extension_state", "extension_status", "check_extension"):
            self.assertEqual(getattr(JHTML, name).__func__, getattr(W, name).__func__, name)

    def test_prefix_from_a_python_path(self):
        W = widgets()
        self.assertEqual(W._prefix_of_python("/a/env/bin/python"), "/a/env")
        self.assertEqual(W._prefix_of_python("/a/env/python.exe"), "/a/env")


class FakeServerTests(unittest.TestCase):
    """Runs this machine's Python as a child of a stand-in ``jupyter-lab`` that uses a different (virtual) environment."""

    CODE = (
        "import json\n"
        "from McUtils.Jupyter.JHTML.HTMLWidgets import HTMLWidgets as W\n"
        "print(json.dumps({'python': W.jupyter_python(True), 'env': W.server_environment(True), "
        "'exec_prefix': W.get_exec_prefix(), 'command': W.install_command()}))\n"
    )

    def test_the_server_environment_is_found_through_the_process_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            env_dir = os.path.join(tmp, "serverenv")
            venv.create(env_dir, with_pip=False, symlinks=True)
            bindir = "Scripts" if os.name == "nt" else "bin"
            python = os.path.join(env_dir, bindir, "python")
            if not os.path.exists(python):
                self.skipTest("could not create a virtual environment")
            server = os.path.join(env_dir, bindir, "jupyter-lab")
            with open(server, "w") as f:
                f.write("#!{}\nimport subprocess, sys\nsys.exit(subprocess.call([{!r}, '-c', {!r}]))\n".format(
                    python, sys.executable, self.CODE))
            os.chmod(server, 0o755)
            env = dict(os.environ, PYTHONPATH=os.pathsep.join(p for p in sys.path if p))
            done = subprocess.run([server], capture_output=True, text=True, env=env, timeout=120)
            self.assertEqual(done.returncode, 0, done.stderr[-2000:])
            result = json.loads(done.stdout.strip().splitlines()[-1])
        self.assertEqual(result["python"]["path"], python)          # the venv's python, not its resolved target
        self.assertIn("server process", result["python"]["how"])
        self.assertEqual(os.path.realpath(result["env"]["prefix"]), os.path.realpath(env_dir))
        self.assertEqual(result["exec_prefix"], result["env"]["prefix"])
        self.assertTrue(result["command"].startswith("!"))
        self.assertIn(python, result["command"])
        self.assertIn("install_extension.py", result["command"])
        labs = result["env"]["labextension"]
        if labs is not None:                                        # jupyter_core was importable in that Python
            self.assertEqual(os.path.realpath(labs[0]), os.path.realpath(os.path.join(env_dir, "share", "jupyter", "labextensions")))


class SearchOrderTests(unittest.TestCase):
    def test_locations_follow_the_servers_search_order(self):
        W = widgets()
        with tempfile.TemporaryDirectory() as tmp:
            a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
            for d in (a, b):
                os.makedirs(os.path.join(d, W.extension_name))
            env = {"python": "p", "how": "t", "prefix": tmp, "labextension": [b, a, "/nowhere"], "nbextension": [a]}
            with mock.patch.object(W, "server_environment", classmethod(lambda cls, refresh=False: env)):
                found = W.extension_locations()
                self.assertEqual(W.get_exec_prefix(), tmp)
        self.assertEqual(found["labextension"], [b, a])
        self.assertEqual(found["nbextension"], [a])

    def test_without_jupyter_core_the_servers_prefix_is_searched(self):
        W = widgets()
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "share", "jupyter", "labextensions", W.extension_name))
            env = {"python": "p", "how": "t", "prefix": tmp, "labextension": None, "nbextension": None}
            with mock.patch.object(W, "server_environment", classmethod(lambda cls, refresh=False: env)):
                found = W.extension_locations()
        self.assertEqual(len(found["labextension"]), 1)
        self.assertEqual(found["nbextension"], [])


class InstallScriptTests(unittest.TestCase):
    def run_script(self, *args):
        W = widgets()
        return subprocess.run([sys.executable, W.install_script(), *args], capture_output=True, text=True, timeout=60)

    def test_it_installs_replaces_and_reports(self):
        W = widgets()
        with tempfile.TemporaryDirectory() as tmp:
            done = self.run_script("--prefix", tmp, "--dry-run")
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("would install", done.stdout)
            self.assertFalse(os.path.exists(os.path.join(tmp, "share")))
            done = self.run_script("--prefix", tmp)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("installed", done.stdout)
            self.assertIn("Hard-reload", done.stdout)
            lab = os.path.join(tmp, "share", "jupyter", "labextensions", W.extension_name)
            nb = os.path.join(tmp, "share", "jupyter", "nbextensions", W.extension_name)
            for kind, target in (("labextension", lab), ("nbextension", nb)):
                self.assertEqual(W.extension_fingerprint(target, kind), W.extension_fingerprint(W.extension_source(kind), kind))
            with open(os.path.join(lab, "package.json"), "w") as f:      # make the install outdated
                json.dump({"name": W.extension_name, "version": "0.1.0"}, f)
            self.assertFalse(W.extension_copy_status(lab, "labextension")["current"])
            done = self.run_script("--prefix", tmp)
            self.assertIn("replaced", done.stdout)
            self.assertTrue(W.extension_copy_status(lab, "labextension")["current"])
            self.assertEqual([n for n in os.listdir(os.path.dirname(lab)) if n.startswith(".activehtml-")], [])

    def test_a_missing_source_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            done = self.run_script("--prefix", tmp, "--source", tmp)
            self.assertEqual(done.returncode, 1)
            self.assertIn("nothing installed", done.stdout)

    def test_the_command_quotes_paths_with_spaces(self):
        W = widgets()
        env = {"python": "/my env/bin/python", "how": "t", "prefix": "/my env", "labextension": None, "nbextension": None}
        with mock.patch.object(W, "server_environment", classmethod(lambda cls, refresh=False: env)):
            command = W.install_command()
        if os.name != "nt":
            self.assertTrue(command.startswith("!'/my env/bin/python' "), command)


@unittest.skipUnless(have_widgets(), "ipywidgets/markdown not installed")
class StaticFallbackTests(unittest.TestCase):
    def setUp(self):
        W = widgets()
        self.W = W
        for name in ("_extension_checked", "_extension_state", "static_fallback"):
            self.addCleanup(setattr, W, name, getattr(W, name))
        W._extension_checked = True               # the check itself is covered elsewhere
        self.shown = []
        from McUtils.Jupyter.JHTML.WidgetTools import JupyterAPIs
        fake = types.SimpleNamespace(display=lambda *a, **k: self.shown.extend(a), HTML=lambda s: s)
        patcher = mock.patch.object(JupyterAPIs, "get_display_api", classmethod(lambda cls: fake))
        patcher.start()
        self.addCleanup(patcher.stop)

    def widget(self):
        from McUtils.Jupyter import JHTML
        return JHTML.Div(JHTML.Button("Run", event_handlers={"click": lambda *a: None}), "some text")

    def test_an_outdated_extension_shows_a_static_view_not_the_widget(self):
        self.W._extension_state = "outdated"
        self.widget().display()
        (shown,) = self.shown
        text = shown.tostring()
        self.assertIn("Static view", text)
        self.assertIn("outdated", text)
        self.assertIn("some text", text)
        self.assertIn("<button", text)

    def test_a_current_extension_shows_the_widget(self):
        self.W._extension_state = "current"
        self.widget().display()
        (shown,) = self.shown
        self.assertFalse(hasattr(shown, "tostring"))     # the ipywidget itself

    def test_the_fallback_can_be_turned_off(self):
        self.W._extension_state = "missing"
        self.W.static_fallback = False
        self.widget().display()
        self.assertFalse(hasattr(self.shown[0], "tostring"))

    def test_an_apps_interface_without_a_static_form_says_so_instead_of_failing(self):
        from McUtils.Jupyter import Button
        self.W._extension_state = "missing"
        with mock.patch.object(Button, "to_static_html", side_effect=ValueError("needs a live kernel")):
            Button("x")._ipython_display_()
        (shown,) = self.shown
        self.assertIn("no static view", shown.tostring())

    def test_jdoc_returns_the_static_page_when_the_extension_is_unusable(self):
        import McUtils.Docs.HTMLDocs as hd
        from McUtils.Docs import jdoc
        for kind, names in (("css", hd._FINX_CSS_FILES), ("js", hd._FINX_JS_FILES)):
            for name in names:
                hd._FINX_ASSET_CACHE.setdefault((kind, name), "")
        mod = types.ModuleType("server_python_demo")
        exec('def area(r):\n    """\n    Area.\n\n    :param r: radius\n    :type r: float\n    """\n    return r', mod.__dict__)
        mod.area.__module__ = "server_python_demo"
        sys.modules["server_python_demo"] = mod
        self.addCleanup(sys.modules.pop, "server_python_demo", None)
        self.W._extension_state = "outdated"
        page = jdoc(mod.area)
        text = page.tostring()
        self.assertIn("Static view", text)
        self.assertIn("iframe", text)
        self.W._extension_state = "current"
        self.assertNotIn("iframe", getattr(jdoc(mod.area), "tostring", lambda: "")())


if __name__ == "__main__":
    unittest.main()
