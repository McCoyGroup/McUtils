
from Peeves.TestUtils import *
from unittest import TestCase
import ast, os, warnings


class ReadoutLayeringTests(TestCase):
    """The readout framework must not pull in Jupyter/Plots (or any heavier McUtils package) at import time."""

    heavy = {"Jupyter", "Plots", "ExternalPrograms", "Zachary", "Docs"}

    def _package_dir(self):
        import McUtils.Readouts as R
        return os.path.dirname(R.__file__)

    def _module_level_imports(self, path, pkg_parts):
        tree = ast.parse(open(path, encoding="utf8").read())
        # only statements that execute at import: the module body, plus `if`/`try` blocks but not function/class bodies
        stack = list(tree.body)
        while stack:
            node = stack.pop()
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                continue
            if isinstance(node, ast.ImportFrom):
                if node.level:
                    base = pkg_parts[:len(pkg_parts) - (node.level - 1)] if node.level > 1 else pkg_parts
                    yield base + (node.module.split(".") if node.module else []), node
                else:
                    yield (node.module or "").split("."), node
            elif isinstance(node, ast.Import):
                for a in node.names:
                    yield a.name.split("."), node
            else:
                for field in ("body", "orelse", "finalbody", "handlers"):
                    stack.extend(getattr(node, field, []) or [])

    @validationTest
    def test_NoHeavyImportsAtModuleLevel(self):
        root = self._package_dir()
        offenders = []
        for dp, dn, fn in os.walk(root):
            dn[:] = [d for d in dn if d != "__pycache__"]
            rel = os.path.relpath(dp, os.path.dirname(root)).split(os.sep)  # ['Readouts', ...]
            for f in fn:
                if not f.endswith(".py"): continue
                pkg_parts = ["McUtils"] + rel
                for target, node in self._module_level_imports(os.path.join(dp, f), pkg_parts):
                    if "McUtils" in target[:1] and len(target) > 1 and target[1] in self.heavy:
                        offenders.append((os.path.join(dp, f), node.lineno, ".".join(target)))
        self.assertEqual(offenders, [])

    @validationTest
    def test_CanonicalExportsAreSameObjects(self):
        import McUtils.Readouts as R
        from McUtils.Readouts import Nodes, Interface, Views
        for module, names in (
            (Nodes, ("Readout", "ReadoutSection")),
            (Interface, ("ReadoutAdapter", "to_readout", "register_readout")),
            (Views, ("ReadoutHTML", "ReadoutWidget")),
        ):
            for name in names:
                self.assertIs(getattr(R, name), getattr(module, name))
