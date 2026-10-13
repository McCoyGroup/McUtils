"""
Lightweight descriptions of what an external-program job (or a python model) needs
in order to run, so that an environment can be assembled *before* anything is submitted.

`ExternalProgramJob.discover_dependencies` returns a `JobDependencies`, which can be rendered
as a pixi/uv manifest, a list of ``module load`` commands, or checked against the
current environment.
"""

import importlib.util
import os
import re
import shutil
import subprocess

__all__ = [
    "Requirement",
    "RequirementStatus",
    "DependencyReport",
    "JobDependencies"
]


class Requirement:
    """
    A single dependency.

    ``kind`` is one of

    * ``'executable'`` -- a program that has to be on ``PATH`` (checked with `shutil.which`)
    * ``'module'`` -- an environment module (``module load name/spec``); cluster-specific, never checked
    * ``'conda'`` -- a conda-forge package (what pixi installs)
    * ``'pip'`` -- a PyPI package (what uv installs); ``import_name`` is used to check it
    """
    kinds = ('executable', 'module', 'conda', 'pip')

    def __init__(self, kind, name, spec=None, *, optional=False, reason=None, import_name=None):
        if kind not in self.kinds:
            raise ValueError(f"requirement kind {kind!r} not in {self.kinds}")
        self.kind = kind
        self.name = name
        self.spec = spec
        self.optional = optional
        self.reason = reason
        self.import_name = import_name

    def format(self):
        """
        The requirement as it would appear in a manifest (``name``, ``name>=1.2``, or ``name/1.2`` for modules).
        """
        if self.spec is None:
            return self.name
        spec = str(self.spec)
        if self.kind == 'module':
            return f"{self.name}/{spec}"
        elif spec[:1] in "<>=!~":
            return f"{self.name}{spec}"
        else:
            return f"{self.name}=={spec}" if self.kind == 'pip' else f"{self.name} {spec}"

    def to_dict(self):
        return {
            k: v for k, v in dict(
                kind=self.kind, name=self.name, spec=self.spec, optional=self.optional,
                reason=self.reason, import_name=self.import_name
            ).items() if v not in (None, False)
        }

    @classmethod
    def from_dict(cls, d):
        d = dict(d)
        return cls(d.pop('kind'), d.pop('name'), **d)

    def key(self):
        return (self.kind, self.name)

    def check(self):
        """
        Test whether this requirement is satisfied in the *current* process/environment.

        :rtype: RequirementStatus
        """
        if self.kind == 'executable':
            path = shutil.which(self.name)
            return RequirementStatus(self, path is not None, path)
        elif self.kind in ('pip', 'conda'):
            mod = self.import_name
            if mod is None:
                return RequirementStatus(self, None, None, "no import name; cannot check")
            try:
                spec = importlib.util.find_spec(mod)
            except (ImportError, ValueError):
                spec = None
            return RequirementStatus(self, spec is not None, None if spec is None else spec.origin)
        else:
            return RequirementStatus(self, None, None, "environment modules are not checked")

    def __repr__(self):
        return f"{type(self).__name__}({self.kind}:{self.format()}{' optional' if self.optional else ''})"


class RequirementStatus:
    def __init__(self, requirement, found, location=None, note=None):
        self.requirement = requirement
        self.found = found  # True / False / None (unknown)
        self.location = location
        self.note = note

    def __repr__(self):
        return f"RequirementStatus({self.requirement!r}, found={self.found}, location={self.location})"


class DependencyReport:
    """
    The result of `JobDependencies.check`.
    """
    def __init__(self, statuses):
        self.statuses = list(statuses)

    @property
    def missing(self):
        return [s.requirement for s in self.statuses if s.found is False and not s.requirement.optional]

    @property
    def missing_optional(self):
        return [s.requirement for s in self.statuses if s.found is False and s.requirement.optional]

    @property
    def unknown(self):
        return [s.requirement for s in self.statuses if s.found is None]

    @property
    def ok(self):
        return len(self.missing) == 0

    def raise_if_missing(self):
        if not self.ok:
            raise ImportError(
                "missing dependencies: " + ", ".join(f"{r.kind}:{r.format()}" for r in self.missing)
            )
        return self

    def __repr__(self):
        return f"DependencyReport(ok={self.ok}, missing={self.missing}, unknown={len(self.unknown)})"


class JobDependencies:
    """
    A set of `Requirement`s with helpers for turning them into something an environment can act on.
    """
    def __init__(self, requirements=(), *, notes=(), env_vars=None):
        self.requirements = []
        self.notes = list(notes)
        self.env_vars = dict(env_vars or {})
        for r in requirements:
            self.add(r)

    def add(self, kind, name=None, spec=None, **opts):
        """
        Add a requirement (a `Requirement`, or ``kind, name, spec, **opts``); an existing requirement of the same
        kind and name is merged (a non-optional request wins over an optional one).
        """
        req = kind if isinstance(kind, Requirement) else Requirement(kind, name, spec, **opts)
        for i, old in enumerate(self.requirements):
            if old.key() == req.key():
                if old.optional and not req.optional:
                    self.requirements[i] = req
                elif old.spec is None and req.spec is not None:
                    old.spec = req.spec
                return self
        self.requirements.append(req)
        return self

    def merge(self, other):
        """
        :return: a new `JobDependencies` with the requirements of both
        """
        new = type(self)(self.requirements, notes=self.notes, env_vars=self.env_vars)
        for r in other.requirements:
            new.add(Requirement.from_dict(r.to_dict()))
        new.notes.extend(n for n in other.notes if n not in new.notes)
        new.env_vars.update(other.env_vars)
        return new

    __add__ = merge

    def _of_kind(self, kind, include_optional=True):
        return [r for r in self.requirements if r.kind == kind and (include_optional or not r.optional)]

    @property
    def executables(self):
        return self._of_kind('executable')

    @property
    def modules(self):
        return self._of_kind('module')

    @property
    def conda_packages(self):
        return self._of_kind('conda')

    @property
    def pip_packages(self):
        return self._of_kind('pip')

    def to_dict(self):
        return {
            'requirements': [r.to_dict() for r in self.requirements],
            'notes': list(self.notes),
            'env_vars': dict(self.env_vars)
        }

    @classmethod
    def from_dict(cls, d):
        return cls([Requirement.from_dict(r) for r in d.get('requirements', [])],
                   notes=d.get('notes', ()), env_vars=d.get('env_vars'))

    def check(self):
        """
        Check the requirements that can be checked against the current environment.

        :rtype: DependencyReport
        """
        return DependencyReport(r.check() for r in self.requirements)

    def module_load_commands(self, include_optional=False):
        """
        :return: ``module load ...`` lines for the environment-module requirements
        """
        return [f"module load {r.format()}" for r in self._of_kind('module', include_optional)]

    @staticmethod
    def _toml_str(s):
        return '"' + str(s).replace('\\', '\\\\').replace('"', '\\"') + '"'

    @staticmethod
    def _split_spec(r):
        spec = '*' if r.spec is None else str(r.spec)
        if spec[:1].isdigit():
            spec = "==" + spec if '*' not in spec else spec
        return spec

    def to_pixi_toml(self, name="job-env", *, python="3.11.*", platforms=("linux-64",),
                     channels=("conda-forge",), include_optional=False, extra_conda=None, extra_pip=None):
        """
        Render a ``pixi.toml``: conda requirements under ``[dependencies]`` and pip requirements under
        ``[pypi-dependencies]`` (a package listed for both is taken from conda). Executables/modules that no
        conda or pip package provides are listed in comments.

        :param name: the project name
        :param python: the python constraint
        :param platforms: pixi platforms
        :param channels: conda channels
        :param include_optional: whether to include optional requirements
        :param extra_conda: additional ``{name: spec}`` conda requirements
        :param extra_pip: additional ``{name: spec}`` pip requirements
        :rtype: str
        """
        lines = [
            "[workspace]",
            f"name = {self._toml_str(name)}",
            f"channels = [{', '.join(self._toml_str(c) for c in channels)}]",
            f"platforms = [{', '.join(self._toml_str(p) for p in platforms)}]",
            "",
            "[dependencies]",
            f"python = {self._toml_str(python)}",
        ]
        conda = {r.name: self._split_spec(r) for r in self._of_kind('conda', include_optional)}
        conda.update(extra_conda or {})
        conda.pop('python', None)
        for k, v in conda.items():
            lines.append(f"{k} = {self._toml_str(v)}")
        # where a package is available from both, conda wins (installing it twice would conflict)
        pip = {r.name: self._split_spec(r) for r in self._of_kind('pip', include_optional) if r.name not in conda}
        pip.update(extra_pip or {})
        if len(pip) > 0:
            lines += ["", "[pypi-dependencies]"]
            for k, v in pip.items():
                lines.append(f"{k} = {self._toml_str(v)}")
        provided = set(conda) | set(pip)
        unmet = [r for r in self.requirements
                 if r.kind in ('executable', 'module') and (include_optional or not r.optional)
                 and r.name not in provided]
        if len(unmet) > 0:
            lines += [""] + [f"# not installable here: {r.kind} {r.format()}"
                             + (f" ({r.reason})" if r.reason else "") for r in unmet]
        return "\n".join(lines) + "\n"

    def to_pyproject_toml(self, name="job-env", *, python=">=3.10", include_optional=False, extra_pip=None):
        """
        Render a uv ``pyproject.toml`` from the pip requirements (conda-only requirements are listed in comments).

        :rtype: str
        """
        pip = [r.format() for r in self._of_kind('pip', include_optional)]
        pip += [f"{k}{'' if v in (None, '*') else v}" for k, v in (extra_pip or {}).items()]
        lines = [
            "[project]",
            f"name = {self._toml_str(name)}",
            'version = "0.1.0"',
            f"requires-python = {self._toml_str(python)}",
            "dependencies = [" + ", ".join(self._toml_str(p) for p in pip) + "]",
            "",
            "[tool.uv]",
            "package = false",
        ]
        conda_only = [r for r in self._of_kind('conda', include_optional)
                      if r.name not in {p.name for p in self._of_kind('pip', include_optional)}]
        if len(conda_only) > 0:
            lines += [""] + [f"# conda-only (use pixi): {r.format()}" for r in conda_only]
        return "\n".join(lines) + "\n"

    def __repr__(self):
        return f"{type(self).__name__}({self.requirements})"
