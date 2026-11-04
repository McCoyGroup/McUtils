"""`DocBuilder.create_layout` copies the template files (404.html, Contributing.md, Gemfile) next to the pages."""

import contextlib
import importlib.util
import io
import os
import unittest

from McUtils.Docs import DocBuilder

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_sibling(name):
    spec = importlib.util.spec_from_file_location(name + "_for_layout", os.path.join(HERE, name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PipelineTestBase = _load_sibling("DocsReadoutEmbedTests").PipelineTestBase


class CreateLayoutTests(PipelineTestBase):
    names = ("404.html", "Contributing.md", "Gemfile")

    def builder(self, target):
        return DocBuilder(**self.config(target))

    def test_template_files_are_copied_whatever_the_working_directory(self):
        target = self.new_dir()
        elsewhere = self.new_dir()
        old = os.getcwd()
        os.chdir(elsewhere)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                self.builder(target).create_layout()
        finally:
            os.chdir(old)
        for name in self.names:
            self.assertTrue(os.path.isfile(os.path.join(target, name)), name)
        self.assertTrue(os.path.isfile(os.path.join(target, "_config.yml")))

    def test_existing_files_are_left_alone(self):
        target = self.new_dir()
        with open(os.path.join(target, "Gemfile"), "w") as f:
            f.write("# mine\n")
        with contextlib.redirect_stdout(io.StringIO()):
            self.builder(target).create_layout()
        with open(os.path.join(target, "Gemfile")) as f:
            self.assertEqual(f.read(), "# mine\n")
        self.assertTrue(os.path.isfile(os.path.join(target, "404.html")))

    def test_the_message_names_the_destination(self):
        target = self.new_dir()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.builder(target).create_layout()
        self.assertIn("writing Gemfile file to " + os.path.join(target, "Gemfile"), out.getvalue())


if __name__ == "__main__":
    unittest.main()
