"""
Input generation (and running) for NWChem.

`NWChemJob` builds the usual directive-style input from five blocks (preamble, geometry, basis, modules, tasks):

    NWChemJob('dft', 'optimize', xc='b3lyp', basis='cc-pvdz', nproc=4, memory='4 GB',
              atoms=['O', 'H', 'H'], cartesians=xyz, charge=0, multiplicity=1,
              dft={'convergence': {'energy': 1e-9}})

Settings for any module (``scf``, ``dft``, ``mp2``, ``ccsd``, ``tce``, ``driver``, ...) are given as dicts
(``{key: value}`` -> one ``key value`` line each; ``True`` is a bare keyword, a dict value is flattened into
``key sub val sub val``) or as literal text.
"""

import numbers
import os
import re

from .Jobs import ExternalProgramJob, OptionsBlock, SystemBlock

__all__ = [
    "NWChemJob"
]

_OPERATIONS = {
    'energy': 'energy', 'sp': 'energy',
    'gradient': 'gradient', 'grad': 'gradient',
    'optimize': 'optimize', 'opt': 'optimize', 'optimization': 'optimize',
    'saddle': 'saddle',
    'hessian': 'hessian', 'hess': 'hessian',
    'freq': 'freq', 'frequencies': 'freq', 'frequency': 'freq',
    'property': 'property', 'properties': 'property',
}

_THEORIES = {
    'scf', 'dft', 'sodft', 'mp2', 'direct_mp2', 'ccsd', 'ccsd(t)', 'ccsd+t(ccsd)', 'tce', 'mcscf', 'xtb', 'tddft',
}


def _fmt_value(v):
    if isinstance(v, bool):
        return None if not v else ""
    if isinstance(v, dict):
        return " ".join(f"{k} {_fmt_value(x)}" if _fmt_value(x) else f"{k}" for k, x in v.items())
    if isinstance(v, (list, tuple)):
        return " ".join(str(x) for x in v)
    if isinstance(v, float):
        return f"{v:.10g}"
    return str(v)


def _fmt_lines(opts, indent="  "):
    lines = []
    for k, v in opts.items():
        if v is None or v is False:
            continue
        val = _fmt_value(v)
        lines.append(f"{indent}{k}" + (f" {val}" if val else ""))
    return lines


def _fmt_memory(v):
    if isinstance(v, numbers.Number):
        v = int(v) if float(v).is_integer() else v
        return f"{v} mb"  # bare numbers are megabytes
    return str(v).lower()


class NWChemPreambleBlock(OptionsBlock):
    """
    ``start``, ``title``, ``echo``, ``memory`` and the scratch/permanent directories.
    """
    __props__ = ('start', 'title', 'echo', 'memory', 'scratch_dir', 'permanent_dir')

    def get_params(self):
        o = self.opts
        lines = []
        if o.get('echo'):
            lines.append("echo")
        if o.get('start') is not None:
            lines.append(f"start {o['start']}")
        if o.get('title') is not None:
            lines.append(f'title "{o["title"]}"')
        if o.get('scratch_dir') is not None:
            lines.append(f"scratch_dir {o['scratch_dir']}")
        if o.get('permanent_dir') is not None:
            lines.append(f"permanent_dir {o['permanent_dir']}")
        if o.get('memory') is not None:
            lines.append(f"memory total {_fmt_memory(o['memory'])}")  # per process
        return {"preamble": "\n".join(lines)} if len(lines) > 0 else {}


class NWChemGeometryBlock(SystemBlock):
    """
    ``charge`` and the ``geometry`` block. Cartesians are written in Angstroms with ``noautoz nocenter noautosym``
    and ``symmetry c1`` by default, so that gradients and Hessians come back in the frame that was supplied
    (``geometry_options`` replaces the default keywords). Z-matrices are only supported as literal text.
    """
    __props__ = SystemBlock.__props__ + ("geometry_options", "symmetry")

    default_geometry_options = ("units angstroms", "noautoz", "nocenter", "noautosym")

    def format_geometry_block(self):
        carts = self.opts.get("cartesians")
        zmat = self.opts.get("zmatrix")
        geom_opts = self.opts.get("geometry_options")
        if geom_opts is None:
            geom_opts = self.default_geometry_options
        elif isinstance(geom_opts, str):
            geom_opts = [geom_opts]
        lines = []
        symmetry = self.opts.get("symmetry", "c1")
        if symmetry is not None:
            lines.append(f"  symmetry {symmetry}")
        if carts is not None:
            body = carts if isinstance(carts, str) else self.fmt_carts(
                self.opts.get('atoms'), carts, float_fmt="{:16.10f}"
            )
            lines += ["  " + l for l in body.strip("\n").split("\n")]
        elif zmat is not None:
            if not isinstance(zmat, str):
                raise NotImplementedError("NWChemJob only supports Z-matrices supplied as text; pass Cartesians instead")
            lines += ["  zmatrix"] + ["    " + l for l in zmat.strip("\n").split("\n")] + ["  end"]
        else:
            raise ValueError("no coordinate spec supplied")
        return "\n".join(["geometry " + " ".join(geom_opts)] + lines + ["end"])

    def get_params(self):
        if len(self.opts) == 0:
            return {}
        charge = self.opts.get("charge")
        block = self.format_geometry_block()
        if charge:
            block = f"charge {charge}\n" + block
        return {"geometry": block}


class NWChemBasisBlock(OptionsBlock):
    """
    The ``basis`` (and optional ``ecp``) blocks. A string basis applies to every atom (``* library name``); a dict
    maps elements (or ``'*'``) to library names. ``basis_type`` is ``'spherical'`` or ``'cartesian'``; unless given,
    Dunning (``cc-p...``) and Karlsruhe (``def2-...``) sets are written as spherical, because NWChem otherwise falls
    back to Cartesian functions and gives energies that differ from other codes by ~1e-4 Eh (Pople sets keep NWChem's
    Cartesian default, matching Gaussian's 6D convention).
    """
    __props__ = ('basis', 'basis_type', 'ecp')
    __aliases__ = {'basis': ['basis_set']}

    _spherical_sets = re.compile(r"^(?:aug-|d-aug-|jun-|may-|apr-|heavy-aug-)*cc-p|^def2-", re.I)

    @classmethod
    def _default_basis_type(cls, basis):
        names = [basis] if isinstance(basis, str) else list(basis.values())
        if len(names) > 0 and all(isinstance(n, str) and cls._spherical_sets.match(n) for n in names):
            return 'spherical'
        return None

    @staticmethod
    def _library_lines(spec):
        if isinstance(spec, str):
            spec = {'*': spec}
        return [f"  {el} library {lib}" for el, lib in spec.items()]

    def get_params(self):
        o = self.opts
        blocks = []
        if o.get('basis') is not None:
            basis_type = o.get('basis_type') or self._default_basis_type(o['basis'])
            header = "basis" + ("" if basis_type is None else f" {basis_type}")
            blocks.append("\n".join([header] + self._library_lines(o['basis']) + ["end"]))
        if o.get('ecp') is not None:
            blocks.append("\n".join(["ecp"] + self._library_lines(o['ecp']) + ["end"]))
        return {"basis": "\n\n".join(blocks)} if len(blocks) > 0 else {}


class NWChemModulesBlock(OptionsBlock):
    """
    ``module ... end`` settings blocks. ``xc`` is shorthand for ``dft={'xc': ...}``. The multiplicity and the
    theory the job runs at are supplied by the job, which sets ``mult``/``odft`` (DFT) or ``uhf``/``nopen``
    (everything else, through ``scf``) unless the module settings already say otherwise.
    """
    __props__ = ('xc', 'scf', 'dft', 'mp2', 'ccsd', 'tce', 'driver', 'property', 'vib', 'hessian', 'cosmo', 'esp',
                 'xtb', 'tddft', 'set')

    def __init__(self, multiplicity=None, theory=None, **opts):
        super().__init__(**opts)
        self.multiplicity = multiplicity
        self.theory = theory

    def _settings(self):
        mods = {k: v for k, v in self.opts.items() if k not in ('xc', 'set')}
        xc = self.opts.get('xc')
        mult = self.multiplicity or 1
        theory = (self.theory or '').lower()
        if xc is not None:
            d = dict(mods.get('dft') or {}) if isinstance(mods.get('dft'), dict) else None
            if d is None and mods.get('dft') is not None:
                raise ValueError("`xc` can't be combined with literal-text `dft` settings; put the xc line in the text")
            d = {'xc': xc, **(d or {})}
            mods['dft'] = d
        if mult > 1:
            if theory in ('dft', 'tddft', 'sodft'):
                d = mods.get('dft')
                if d is None:
                    d = mods['dft'] = {}
                if isinstance(d, dict):
                    d.setdefault('odft', True)
                    d.setdefault('mult', mult)
            else:
                d = mods.get('scf')
                if d is None:
                    d = mods['scf'] = {}
                if isinstance(d, dict) and not ({'uhf', 'rohf', 'rhf'} & set(d)):
                    d['uhf'] = True
                    d.setdefault('nopen', mult - 1)
        return mods

    def get_params(self):
        blocks = []
        for name, body in self._settings().items():
            if body is None:
                continue
            if isinstance(body, dict):
                lines = _fmt_lines(body)
            elif isinstance(body, str):
                lines = ["  " + l.strip() for l in body.strip("\n").split("\n")]
            else:
                lines = ["  " + str(l) for l in body]
            blocks.append("\n".join([name] + lines + ["end"]))
        for k, v in (self.opts.get('set') or {}).items():
            blocks.append(f"set {k} {_fmt_value(v)}")
        return {"modules": "\n\n".join(blocks)} if len(blocks) > 0 else {}


class NWChemTaskBlock(OptionsBlock):
    """
    The ``task <theory> <operation>`` line(s). Several steps can be chained with ``tasks=[('dft', 'optimize'), ...]``.
    """
    __props__ = ('theory', 'operation', 'tasks')

    def get_params(self):
        tasks = self.opts.get('tasks')
        if tasks is None:
            theory = self.opts.get('theory')
            if theory is None:
                raise ValueError("NWChemJob needs a `theory` (e.g. 'dft', 'scf', 'mp2')")
            tasks = [(theory, self.opts.get('operation') or 'energy')]
        lines = []
        for theory, op in tasks:
            lines.append(f"task {theory} {_OPERATIONS[str(op).lower()]}")
        return {"tasks": "\n".join(lines)}


@ExternalProgramJob.register("nwchem")
class NWChemJob(ExternalProgramJob):
    """
    An NWChem calculation. Positional strings name the theory (``'dft'``, ``'scf'``, ``'mp2'``, ...) and/or the
    operation (``'optimize'``, ``'freq'``, ...).
    """
    extension = ".nw"
    job_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'nwchem_job.nw')
    blocks = [
        NWChemPreambleBlock,
        NWChemGeometryBlock,
        NWChemBasisBlock,
        NWChemModulesBlock,
        NWChemTaskBlock
    ]
    executable = 'nwchem'
    stdout_output = True
    parallel_model = 'mpi'
    distance_units = 'Angstroms'

    def __init__(self, *strs, theory=None, operation=None, task=None, **opts):
        operation = task if operation is None else operation
        for s in strs:
            key = s.lower()
            if key in _OPERATIONS:
                operation = _OPERATIONS[key]
            elif key in _THEORIES:
                theory = key
            else:
                raise ValueError(f"can't interpret positional option {s!r}; expected a theory {sorted(_THEORIES)} "
                                 f"or an operation {sorted(set(_OPERATIONS.values()))}")
        if theory is not None:
            opts['theory'] = theory.lower()
        if operation is not None:
            opts['operation'] = operation
        # `nproc` is an MPI launch option, not an input one: it is kept in `job_opts` for `submit`/`dependencies`
        nproc = opts.pop('nproc', None)
        super().__init__(**opts)
        if nproc is not None:
            self.job_opts['nproc'] = nproc

    @classmethod
    def get_block_types(cls):
        return cls.blocks

    @classmethod
    def load_template(cls):
        return cls.job_template

    def populate_blocks(self, opts):
        block_opts = super().populate_blocks(opts)
        i_task = self.blocks.index(NWChemTaskBlock)
        i_mod = self.blocks.index(NWChemModulesBlock)
        i_sys = self.blocks.index(NWChemGeometryBlock)
        task_opts = block_opts[i_task]
        mod_opts = block_opts[i_mod]
        if 'theory' not in task_opts and 'tasks' not in task_opts:
            task_opts['theory'] = 'dft' if ('xc' in mod_opts or 'dft' in mod_opts) else 'scf'
        mod_opts['theory'] = task_opts.get('theory') or (task_opts['tasks'][0][0] if task_opts.get('tasks') else None)
        mod_opts['multiplicity'] = block_opts[i_sys].get('multiplicity')
        return block_opts

    @classmethod
    def optimization(cls, *strs, **opts):
        return cls(*strs, operation='optimize', **opts)

    @classmethod
    def gradient(cls, *strs, **opts):
        return cls(*strs, operation='gradient', **opts)

    @classmethod
    def frequencies(cls, *strs, **opts):
        return cls(*strs, operation='freq', **opts)

    @classmethod
    def get_dependencies(cls, **opts):
        """
        NWChem from conda-forge (which brings its own MPI); a launcher is only listed when ``nproc > 1``.
        """
        deps = super().get_dependencies(**opts)
        deps.add('conda', 'nwchem', reason='conda-forge is the simplest way to install NWChem')
        if (opts.get('nproc') or 1) > 1:
            deps.add('executable', 'mpirun', reason='nproc > 1')
        return deps

    def get_run_command(self, input_file, output_file=None, *, nproc=None, executable=None, **run_opts):
        """
        ``[mpirun -np N [mpi_args]] nwchem input`` (NWChem prints to stdout, which `submit` redirects to the output file)
        """
        cmd = [executable or self.executable, input_file]
        if nproc is not None and nproc > 1:
            # `mpi_args` e.g. ['--oversubscribe'] for an OpenMPI that sees fewer scheduler slots than `nproc`
            cmd = [run_opts.get('mpirun', 'mpirun'), '-np', str(nproc)] + list(run_opts.get('mpi_args') or []) + cmd
        return cmd

    _grad_row = re.compile(
        r"^\s+(\d+)\s+([A-Za-z]{1,2})((?:\s+-?\d+\.\d+){6})\s*$", re.M
    )

    @classmethod
    def parse_output(cls, text):
        """
        :return: ``terminated_normally``; the last total ``energy`` (Hartree); and, if a gradient was printed,
            ``gradient`` (Hartree/Bohr, shape ``(natoms, 3)``) and the ``geometry_bohr`` it belongs to
        """
        res = {'terminated_normally': "Total times  cpu:" in text}
        energies = [float(e) for e in re.findall(
            r"Total (?:DFT|SCF|MP2|CCSD(?:\(T\))?|TDDFT|SODFT) energy\s*=\s*(-?\d+\.\d+)", text)]
        if len(energies) > 0:
            res['energy'] = energies[-1]
            res['energies'] = energies
        idx = text.rfind("ENERGY GRADIENTS")
        if idx >= 0:
            rows = cls._grad_row.findall(text[idx:])
            if len(rows) > 0:
                vals = [[float(x) for x in r[2].split()] for r in rows]
                res['geometry_bohr'] = [v[:3] for v in vals]
                res['gradient'] = [v[3:] for v in vals]
        return res
