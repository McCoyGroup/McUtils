"""
Input generation (and running) for Psi4.

Psi4 inputs are python-flavoured scripts: a ``molecule`` block, ``set`` blocks for options, and driver calls.
`Psi4Job` builds them from four blocks (resources, molecule, options, commands), e.g.

    Psi4Job(method='b3lyp-d3bj', basis='cc-pvdz', task='optimize', nproc=4, memory='8 GB',
            atoms=['O', 'H', 'H'], cartesians=xyz, charge=0, multiplicity=1)

Options without a dedicated keyword go in ``options={...}`` (global ``set``) or ``module_options={'scf': {...}}``
(``set scf ...``).
"""

import json
import numbers
import os
import re

from .Jobs import ExternalProgramJob, OptionsBlock, SystemBlock

__all__ = [
    "Psi4Job"
]

_TASKS = {
    'energy': 'energy', 'sp': 'energy',
    'gradient': 'gradient', 'grad': 'gradient',
    'hessian': 'hessian', 'hess': 'hessian',
    'optimize': 'optimize', 'opt': 'optimize', 'optimization': 'optimize',
    'frequencies': 'frequencies', 'frequency': 'frequencies', 'freq': 'frequencies',
    'properties': 'properties', 'prop': 'properties',
}

RESULTS_FILE = 'psi4_results.json'


def _fmt_value(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(_fmt_value(x) for x in v) + "]"
    if isinstance(v, float):
        return repr(v)
    return str(v)


def _fmt_memory(v):
    if isinstance(v, numbers.Number):
        v = int(v) if float(v).is_integer() else v
        return f"{v} mb"  # bare numbers are megabytes, as for ORCA's MaxCore
    return str(v)


def _fmt_set_block(header, opts):
    rows = "\n".join(f"  {k} {_fmt_value(v)}" for k, v in opts.items() if v is not None)
    if len(rows) == 0:
        return ""
    return ("set " + header + " {" if header else "set {") + f"\n{rows}\n}}"


class Psi4ResourcesBlock(OptionsBlock):
    """
    ``memory`` and thread count.
    """
    __props__ = ('memory', 'threads')
    __aliases__ = {'threads': ['nthreads', 'num_threads']}

    def get_params(self):
        lines = []
        if self.opts.get('memory') is not None:
            lines.append(f"memory {_fmt_memory(self.opts['memory'])}")
        if self.opts.get('threads') is not None:
            lines.append(f"set_num_threads({int(self.opts['threads'])})")
        return {"resources": "\n".join(lines)} if len(lines) > 0 else {}


class Psi4MoleculeBlock(SystemBlock):
    """
    The ``molecule { ... }`` block. Cartesians are written in Angstroms with ``no_reorient``/``no_com`` and
    ``symmetry c1`` by default, so that gradients and Hessians come back in the frame that was supplied.
    Z-matrices are only supported as literal text.
    """
    __props__ = SystemBlock.__props__ + ("name", "symmetry", "reorient", "recenter")

    def format_molecule_block(self):
        charge = self.opts.get("charge") or 0
        multiplicity = self.opts.get("multiplicity") or 1
        carts = self.opts.get("cartesians")
        zmat = self.opts.get("zmatrix")
        if carts is not None:
            body = carts if isinstance(carts, str) else self.fmt_carts(
                self.opts.get('atoms'), carts, float_fmt="{:16.10f}"
            )
        elif zmat is not None:
            if not isinstance(zmat, str):
                raise NotImplementedError("Psi4Job only supports Z-matrices supplied as text; pass Cartesians instead")
            body = zmat
        else:
            raise ValueError("no coordinate spec supplied")
        lines = [f"{charge} {multiplicity}"] + body.strip("\n").split("\n") + ["units angstrom"]
        symmetry = self.opts.get("symmetry", "c1")
        if symmetry is not None:
            lines.append(f"symmetry {symmetry}")
        if not self.opts.get("reorient", False):
            lines.append("no_reorient")
        if not self.opts.get("recenter", False):
            lines.append("no_com")
        name = self.opts.get("name")
        header = "molecule" + ("" if name is None else f" {name}") + " {"
        return "\n".join([header] + ["  " + l for l in lines] + ["}"])

    def get_params(self):
        return {"molecule": self.format_molecule_block()} if len(self.opts) > 0 else {}


class Psi4OptionsBlock(OptionsBlock):
    """
    ``set { ... }`` blocks: a curated set of common global options as keywords, plus ``options`` (any global
    option) and ``module_options`` (``{module: {option: value}}`` -> ``set module { ... }``).
    """
    __props__ = (
        'basis', 'reference', 'scf_type', 'e_convergence', 'd_convergence', 'maxiter', 'guess', 'freeze_core',
        'puream', 'df_basis_scf', 'df_basis_mp2', 'df_basis_cc', 'basis_guess',
        'dft_radial_points', 'dft_spherical_points', 'dft_pruning_scheme',
        'mp2_type', 'mp_type', 'cc_type', 'ci_type',
        'g_convergence', 'geom_maxiter', 'opt_type', 'full_hess_every', 'step_type',
        'soscf', 'damping_percentage', 'fail_on_maxiter', 'num_roots', 'tdscf_states', 'print',
        'options', 'module_options'
    )
    __aliases__ = {'basis': ['basis_set']}

    def get_params(self):
        opts = dict(self.opts)
        extra = opts.pop('options', None) or {}
        modules = opts.pop('module_options', None) or {}
        blocks = [_fmt_set_block("", dict(opts, **extra))]
        blocks += [_fmt_set_block(m, o) for m, o in modules.items()]
        blocks = [b for b in blocks if len(b) > 0]
        return {"options": "\n".join(blocks)} if len(blocks) > 0 else {}


class Psi4CommandsBlock(OptionsBlock):
    """
    The driver call (``energy``/``gradient``/``hessian``/``optimize``/``frequencies``/``properties``) and the
    code that records its results in ``psi4_results.json`` so they don't have to be scraped from the output.
    """
    __props__ = ('method', 'task', 'driver_options', 'properties', 'save_results',
                 'molden', 'fchk', 'pre_commands', 'post_commands')

    def format_commands(self):
        method = self.opts.get('method')
        if method is None:
            raise ValueError("Psi4Job needs a `method` (e.g. 'scf', 'b3lyp-d3bj', 'mp2')")
        task = _TASKS[str(self.opts.get('task') or 'energy').lower()]
        kw = dict(self.opts.get('driver_options') or {})
        if self.opts.get('properties') is not None:
            kw['properties'] = list(self.opts['properties'])
            if task == 'energy':
                task = 'properties'
        kw['return_wfn'] = True
        call_args = ", ".join([repr(method)] + [f"{k}={v!r}" for k, v in kw.items()])
        lines = list(self.opts.get('pre_commands') or [])
        lines.append(f"_result, wfn = {task}({call_args})")
        if self.opts.get('save_results', True):
            lines += [
                "import json as _json",
                f"_out = {{'task': {task!r}, 'method': {method!r}, 'energy': float(variable('CURRENT ENERGY')),",
                "         'geometry_bohr': wfn.molecule().geometry().np.tolist()}",
            ]
            if task == 'gradient':
                lines.append("_out['gradient'] = wfn.gradient().np.tolist()")
            if task in ('hessian', 'frequencies'):
                lines.append("_out['hessian'] = wfn.hessian().np.tolist()")
            if task == 'frequencies':
                lines.append("_out['frequencies'] = wfn.frequencies().np.tolist()")
            lines += [
                f"with open({RESULTS_FILE!r}, 'w') as _f:",
                "    _json.dump(_out, _f)",
            ]
        if self.opts.get('molden'):
            lines.append("molden(wfn, 'psi4.molden')")
        if self.opts.get('fchk'):
            lines.append("fchk(wfn, 'psi4.fchk')")
        lines += list(self.opts.get('post_commands') or [])
        return "\n".join(lines)

    def get_params(self):
        return {"commands": self.format_commands()}


@ExternalProgramJob.register("psi4")
class Psi4Job(ExternalProgramJob):
    """
    A Psi4 calculation. The first positional strings may name the task (``'optimize'``, ``'freq'``, ...) or the method.
    """
    extension = ".dat"
    job_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'psi4_job.dat')
    blocks = [
        Psi4ResourcesBlock,
        Psi4MoleculeBlock,
        Psi4OptionsBlock,
        Psi4CommandsBlock
    ]
    executable = 'psi4'
    stdout_output = False  # `psi4 -o` names the output file
    parallel_model = 'threads'
    distance_units = 'Angstroms'

    __common_aliases__ = {
        'nproc': 'threads',
    }

    def __init__(self, *strs, method=None, task=None, **opts):
        for s in strs:
            key = s.lower()
            if key in _TASKS:
                task = _TASKS[key]
            elif method is None:
                method = s
            else:
                raise ValueError(f"can't interpret positional option {s!r} (method is already {method!r})")
        if method is not None:
            opts['method'] = method
        if task is not None:
            opts['task'] = task
        super().__init__(**opts)

    @classmethod
    def get_block_types(cls):
        return cls.blocks

    @classmethod
    def load_template(cls):
        return cls.job_template

    def populate_blocks(self, opts):
        block_opts = super().populate_blocks(opts)
        mol = block_opts[self.blocks.index(Psi4MoleculeBlock)]
        set_opts = block_opts[self.blocks.index(Psi4OptionsBlock)]
        extra = set_opts.get('options') or {}
        if (mol.get('multiplicity') or 1) > 1 and 'reference' not in set_opts and 'reference' not in extra:
            set_opts['reference'] = 'uhf'  # psi4 needs an unrestricted/ROHF reference for open shells; `uhf` runs UKS for DFT
        return block_opts

    @classmethod
    def energy(cls, *strs, **opts):
        return cls(*strs, task='energy', **opts)

    @classmethod
    def gradient(cls, *strs, **opts):
        return cls(*strs, task='gradient', **opts)

    @classmethod
    def hessian(cls, *strs, **opts):
        return cls(*strs, task='hessian', **opts)

    @classmethod
    def optimization(cls, *strs, **opts):
        return cls(*strs, task='optimize', **opts)

    @classmethod
    def frequencies(cls, *strs, **opts):
        return cls(*strs, task='frequencies', **opts)

    @classmethod
    def get_dependencies(cls, **opts):
        """
        Psi4 (the program and its python module) from conda-forge.
        """
        deps = super().get_dependencies(**opts)
        deps.add('conda', 'psi4', import_name='psi4', reason='conda-forge is the supported way to install Psi4')
        method = str(opts.get('method') or '').lower()
        if re.search(r'-d[234]', method) or opts.get('dispersion') is not None:
            # psi4 hands -D3 corrections to the `s-dftd3` program through QCEngine
            deps.add('conda', 'simple-dftd3', reason='-D3 dispersion corrections (psi4 calls s-dftd3 via QCEngine)')
            deps.add('conda', 'dftd3-python', import_name='dftd3', reason='-D3 dispersion corrections')
        return deps

    def get_run_command(self, input_file, output_file=None, *, nproc=None, executable=None, **run_opts):
        """
        ``psi4 -i input -o output [-n nproc]``
        """
        cmd = [executable or self.executable, '-i', input_file]
        if output_file is not None:
            cmd += ['-o', output_file]
        if nproc is not None:
            cmd += ['-n', str(nproc)]
        return cmd

    @classmethod
    def parse_output(cls, text):
        """
        :return: ``terminated_normally`` and the last printed ``energy`` (Hartree) if there is one
        """
        res = {'terminated_normally': "Psi4 exiting successfully" in text}
        energies = [float(e) for e in re.findall(r"^\s*Total Energy\s*=\s+(-?\d+\.\d+)", text, re.M)]
        energies += [float(e) for e in re.findall(r"Final energy is\s+(-?\d+\.\d+)", text)]
        if len(energies) > 0:
            res['energy'] = energies[-1]
        return res

    @classmethod
    def collect_results(cls, submission):
        """
        The contents of ``psi4_results.json`` (energy, gradient/hessian/frequencies, final geometry in Bohr)
        merged over what `parse_output` finds in the output file.
        """
        res = super().collect_results(submission)
        path = os.path.join(submission.work_dir, RESULTS_FILE)
        if os.path.isfile(path):
            with open(path) as inp:
                res.update(json.load(inp))
        return res
