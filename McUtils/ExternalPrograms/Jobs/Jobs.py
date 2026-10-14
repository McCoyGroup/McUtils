import abc
import os
import re
import tempfile
from ... import Devutils as dev
from ... import Coordinerds as coordops
from ...Formatters import OptionalTemplate
from ...Data import UnitsData

__all__ = [
    "OptionsBlock",
    "ExternalProgramJob"
]

class JobBlockBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_template(self):
        """
        **LLM Docstring**

        Abstract: return the template string this block fills in.

        :return: the block template
        :rtype: str
        """
        ...
    @abc.abstractmethod
    def get_params(self):
        """
        **LLM Docstring**

        Abstract: return the `{template_key: value}` mapping used to fill the template.

        :return: the template parameters
        :rtype: dict
        """
        ...
    def format(self):
        """
        **LLM Docstring**

        Render the block by filling its template with its parameters (recursively
        formatting any parameter that is itself formattable).

        :return: the formatted block text
        :rtype: str
        """
        params = {
            k:v.format() if hasattr(v, 'format') else v
            for k,v in self.get_params().items()
        }
        return OptionalTemplate(self.get_template(), **params).apply()

class JobBlock(JobBlockBase):
    template = None
    def __init__(self, **opts):
        """
        **LLM Docstring**

        Store the raw options for this block.

        :param opts: the block's options
        """
        self.opts = opts

    def get_template(self):
        """
        **LLM Docstring**

        Return the block's class-level template.

        :return: the template string
        :rtype: str
        """
        return self.template

    def get_params(self):
        """
        **LLM Docstring**

        Return the block options as template parameters, formatting any value that
        exposes a `format` method.

        :return: the template parameters
        :rtype: dict
        """
        return {k:v.format() if hasattr(v, 'format') else v for k,v in self.opts.items()}

class OptionsBlock(JobBlock):
    __props__ = ()
    __aliases__ = {}
    def __init__(self, canonicalize_opts=True, **opts):
        """
        **LLM Docstring**

        Store the block options, canonicalizing their names against the block's known
        properties/aliases unless disabled.

        :param canonicalize_opts: canonicalize and validate the option names
        :type canonicalize_opts: bool
        :param opts: the block options
        """
        if canonicalize_opts:
            opts = self.check_opts(opts)
        super().__init__(**opts)
    _canon_opts = None

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the tuple of option names this block accepts.

        :return: the accepted property names
        :rtype: tuple
        """
        return cls.__props__
    @classmethod
    def get_aliases(cls):
        """
        **LLM Docstring**

        Return the mapping of canonical option names to their accepted aliases.

        :return: the alias mapping
        :rtype: dict
        """
        return cls.__aliases__
    @classmethod
    def get_canonical_opts_map(cls):
        """
        **LLM Docstring**

        Return (and cache) the lower-case-to-canonical mapping of the block's property
        names.

        :return: the canonicalization mapping
        :rtype: dict
        """
        if cls._canon_opts is None:
            cls._canon_opts = {
                k.lower():k for k in cls.get_props()
            }
        return cls._canon_opts
    _check_props = None
    @classmethod
    def get_props_set(cls):
        """
        **LLM Docstring**

        Return (and cache) the set of accepted property names, for fast membership
        checks.

        :return: the set of accepted properties
        :rtype: set
        """
        if cls._check_props is None:
            cls._check_props = set(cls.get_props())
        return cls._check_props
    _inv_alias_map = None
    @classmethod
    def get_inverse_alias_map(cls):
        """
        **LLM Docstring**

        Return (and cache) the lower-case-alias-to-canonical-name mapping.

        :return: the inverse alias mapping
        :rtype: dict
        """
        if cls._inv_alias_map is None:
            cls._inv_alias_map = {
                a.lower(): k
                for k, aliases in cls.get_aliases().items()
                for a in aliases
            }
        return cls._inv_alias_map

    require_value = None
    @classmethod
    def check_canon(cls, opt, val):
        """
        **LLM Docstring**

        Test whether an option belongs to this block, returning its canonical name.

        Honors `require_value`: options that require a value (or require none) are
        rejected when the supplied value doesn't match.

        :param opt: the option name
        :type opt: str
        :param val: the option value
        :return: `(belongs_to_block, canonical_name)`
        :rtype: tuple[bool, str]
        """

        if cls.require_value is not None:
            no_val = val is None or val is True
            if (
                    (no_val and cls.require_value)
                    or (not no_val and not cls.require_value)
            ):
                return False, opt

        opt = cls.canonicalize_opt_name(opt)
        return opt in cls.get_props_set(), opt


    @classmethod
    def canonicalize_opt_name(cls, opt):
        """
        **LLM Docstring**

        Resolve an option name to its canonical form via the alias and canonicalization
        maps.

        :param opt: the option name
        :type opt: str
        :return: the canonical option name
        :rtype: str
        """
        opt = cls.get_inverse_alias_map().get(opt.lower(), opt)
        opt = cls.get_canonical_opts_map().get(opt.lower(), opt)
        return opt
    def check_opts(self, opts):
        """
        **LLM Docstring**

        Canonicalize and validate a set of options, raising on unknown or duplicated
        names.

        :param opts: the raw options
        :type opts: dict
        :return: the canonicalized options
        :rtype: dict
        :raises ValueError: if any option is invalid or duplicated
        """
        new_opts = {}
        dupe_opts = set()
        bad_opts = set()
        check_props = self.get_props_set()
        for k,v in opts.items():
            k = self.canonicalize_opt_name(k)
            if k not in check_props:
                bad_opts.add(k)
            elif k in new_opts:
                dupe_opts.add(k)
            else:
                new_opts[k] = v

        if len(bad_opts) > 0:
            raise ValueError(f"options {bad_opts} invalid for {type(self).__name__} (valid set: {check_props})")
        if len(bad_opts) > 0:
            raise ValueError(f"got two values for option {dupe_opts} after canonicalization")

        return new_opts

    @classmethod
    def prep_opts(cls, opts):
        """
        **LLM Docstring**

        Normalize an option value into the canonical `[positional_list, keyword_dict]`
        form.

        Accepts `True` (no options), a bare string, a mapping, or an existing
        `[list, dict]` pair.

        :param opts: the option value to normalize
        :return: `[positional_options, keyword_options]`
        :rtype: list
        """
        if opts is True:
            opts = []
        if isinstance(opts, str):
            opts = [[opts], {}]
        elif hasattr(opts, 'items'):
            opts = [[], opts]
        elif not hasattr(opts, '__len__'):
            opts = [[str(opts)], {}]
        elif not (len(opts) == 2 and hasattr(opts[1], 'items') and not hasattr(opts[0], 'items')):
            opts = [opts, {}]
        return opts


class SystemBlock(OptionsBlock):
    __props__ = ("charge", "multiplicity", "atoms", "cartesians", "zmatrix", "ordering", "internals", "bonds")

    @classmethod
    def fmt_carts(cls, atoms, carts, float_fmt="{:11.8f}"):
        """
        **LLM Docstring**

        Format a set of atoms and Cartesian coordinates into aligned columns.

        :param atoms: the atom labels
        :type atoms: Sequence[str]
        :param carts: the Cartesian coordinates
        :type carts: Sequence
        :param float_fmt: format string for the coordinate values
        :type float_fmt: str
        :return: the formatted coordinate block
        :rtype: str
        """
        max_at_len = max(len(a) for a in atoms)
        carts = [
            [float_fmt.format(x) if not isinstance(x, str) else x for x in xyz]
            for xyz in carts
        ]
        col_lens = [
            max([len(xyz[i]) for xyz in carts])
            for i in range(3)
        ]
        fmt_string = f"{{a:<{max_at_len}}} {{xyz[0]:>{col_lens[0]}}} {{xyz[1]:>{col_lens[1]}}} {{xyz[2]:>{col_lens[2]}}}"
        return "\n".join(
            fmt_string.format(
                a=a,
                xyz=xyz
            )
            for a, xyz in zip(atoms, carts)
        )

    @classmethod
    def fmt_zmat(cls, atoms, zmat, ordering=None, float_fmt="{:11.8f}"):
        """
        **LLM Docstring**

        Format a Z-matrix (connectivity ordering plus internal-coordinate values) into
        aligned columns.

        When no `ordering` is supplied it is split out of a combined Z-matrix
        specification; the reference-atom and value columns are then padded and aligned.

        :param atoms: the atom labels
        :type atoms: Sequence[str]
        :param zmat: the Z-matrix values (or a combined ordering+value spec)
        :type zmat: Sequence
        :param ordering: the connectivity (reference-atom) ordering
        :type ordering: Sequence | None
        :param float_fmt: format string for the internal-coordinate values
        :type float_fmt: str
        :return: the formatted Z-matrix block
        :rtype: str
        """
        if ordering is None:
            if len(zmat) == len(atoms):
                zmat = zmat[1:]
            ordering = [
                [z[0], z[2], z[4]]
                if i > 1 else
                [z[0], z[2], -1]
                if i > 0 else
                [z[0], -1, -1]
                for i, z in enumerate(zmat)
            ]
            zmat = [
                [z[1], z[3], z[5]]
                if i > 1 else
                [z[1], z[3], -1]
                if i > 0 else
                [z[1], -1, -1]
                for i, z in enumerate(zmat)
            ]
        if len(ordering) < len(atoms):
            ordering = [[-1, -1, -1]] + list(ordering)
        if len(zmat) < len(atoms):
            zmat = [[-1, -1, -1]] + list(zmat)

        zmat = [
            ["", "", ""]
            if i == 0 else
            [z[0], "", ""]
            if i == 1 else
            [z[0], z[1], ""]
            if i == 2 else
            [z[0], z[1], z[2]]
            for i, z in enumerate(zmat)
        ]
        zmat = [
            [float_fmt.format(x) if not isinstance(x, str) else x for x in zz]
            for zz in zmat
        ]
        ordering = [
            ["", "", ""]
            if i == 0 else
            [z[0], "", ""]
            if i == 1 else
            [z[0], z[1], ""]
            if i == 2 else
            [z[0], z[1], z[2]]
            for i, z in enumerate(ordering)
        ]
        ordering = [
            ["{:.0f}".format(x) if not isinstance(x, str) else x for x in zz]
            for zz in ordering
        ]

        max_at_len = max(len(a) for a in atoms)

        nls = [
            max([len(xyz[i]) for xyz in ordering])
            for i in range(3)
        ]
        zls = [
            max([len(xyz[i]) for xyz in zmat])
            for i in range(3)
        ]
        fmt_string = f"{{a:<{max_at_len}}} {{n[0]:>{nls[0]}}} {{r[0]:>{zls[0]}}} {{n[1]:>{nls[1]}}} {{r[1]:>{zls[1]}}} {{n[2]:>{nls[2]}}} {{r[2]:>{zls[2]}}}"
        return "\n".join(
            fmt_string.format(
                a=a,
                n=n,
                r=r
            )
            for a, n, r in zip(atoms, ordering, zmat)
        )

    @classmethod
    def fmt_orca_zmat(cls, atoms, zmat, ordering=None, float_fmt="{:11.8f}"):
        """
        **LLM Docstring**

        Format a Z-matrix in ORCA's column order (all reference-atom indices, then all
        internal-coordinate values), with aligned columns.

        :param atoms: the atom labels
        :type atoms: Sequence[str]
        :param zmat: the Z-matrix values (or a combined ordering+value spec)
        :type zmat: Sequence
        :param ordering: the connectivity (reference-atom) ordering
        :type ordering: Sequence | None
        :param float_fmt: format string for the internal-coordinate values
        :type float_fmt: str
        :return: the formatted ORCA Z-matrix block
        :rtype: str
        """
        if ordering is None:
            if len(zmat) == len(atoms):
                zmat = zmat[1:]
            ordering = [
                [z[0], z[2], z[4]]
                if i > 1 else
                [z[0], z[2], -1]
                if i > 0 else
                [z[0], -1, -1]
                for i, z in enumerate(zmat)
            ]
            zmat = [
                [z[1], z[3], z[5]]
                if i > 1 else
                [z[1], z[3], -1]
                if i > 0 else
                [z[1], -1, -1]
                for i, z in enumerate(zmat)
            ]
        if len(ordering) < len(atoms):
            ordering = [[-1, -1, -1]] + list(ordering)
        if len(zmat) < len(atoms):
            zmat = [[-1, -1, -1]] + list(zmat)

        zmat = [
            ["0.0", "0.0", "0.0"]
                if i == 0 else
            [z[0], "0.0", "0.0"]
                if i == 1 else
            [z[0], z[1], "0.0"]
                if i == 2 else
            [z[0], z[1], z[2]]
            for i, z in enumerate(zmat)
        ]
        zmat = [
            [float_fmt.format(x) if not isinstance(x, str) else x for x in zz]
            for zz in zmat
        ]
        ordering = [
            [0, 0, 0]
                if i == 0 else
            [z[0], 0, 0]
                if i == 1 else
            [z[0], z[1], 0]
                if i == 2 else
            [z[0], z[1], z[2]]
            for i, z in enumerate(ordering)
        ]
        ordering = [
            ["{:.0f}".format(x) if not isinstance(x, str) else x for x in zz]
            for zz in ordering
        ]

        max_at_len = max(len(a) for a in atoms)

        nls = [
            max([len(xyz[i]) for xyz in ordering])
            for i in range(3)
        ]
        zls = [
            max([len(xyz[i]) for xyz in zmat])
            for i in range(3)
        ]
        fmt_string = f"{{a:<{max_at_len}}} {{n[0]:>{nls[0]}}} {{n[1]:>{nls[1]}}} {{n[2]:>{nls[2]}}} {{r[0]:>{zls[0]}}} {{r[1]:>{zls[1]}}} {{r[2]:>{zls[2]}}}"
        return "\n".join(
            fmt_string.format(a=a, n=n,r=r)
            for a, n, r in zip(atoms, ordering, zmat)
        )

    def format_bonds_block(self):
        """
        **LLM Docstring**

        Format the block's explicit bond list (pairs, optionally with a bond order) into
        one line per bond.

        :return: the formatted bonds block
        :rtype: str
        """
        bonds = self.opts.get('bonds')
        return "\n".join(
            ' {l} {r}{t}'.format(
                l='{:.0f}'.format(b[0]) if not isinstance(b[0], str) else b[0],
                r='{:.0f}'.format(b[1]) if not isinstance(b[1], str) else b[1],
                t=(
                    (" " + ('{:.0f}'.format(b[2]) if not isinstance(b[2], str) else b[2]))
                        if len(b) > 2 else
                    ""
                )
            )
            for b in bonds
        )

class ExternalProgramJob(metaclass=abc.ABCMeta):
    # blocks: 'tuple[OptionsBlock]' = []
    # base_template = None
    extension: str

    # how the program is run (used by `submit`)
    executable = None  # name of the binary on PATH
    output_extension = '.out'  # appended to the job name for the program's output file (`None` for no output file)
    stdout_output = False  # whether the program prints its output to stdout, which `submit` then redirects to the output file
    parallel_model = 'threads'  # 'threads' (shared memory; `--cpus-per-task`) or 'mpi' (`--ntasks`)

    registry = {}
    def to_readout(self, **opts):
        """
        **LLM Docstring**

        Build a `Readout` of the job specification (`ExternalProgramJobReadout`); nothing is submitted.

        :param opts: `ReadoutInterface.to_readout` options (``include``, ``exclude``, ``units``, ...)
        :return: the readout
        :rtype: McUtils.Jupyter.Readouts.Readout
        """
        from ..Readouts.Jobs import ExternalProgramJobReadout
        return ExternalProgramJobReadout(self).to_readout(**opts)

    @classmethod
    def register(cls, name, method=None):
        if method is None and hasattr(name, 'name'):
            method = name
            name = method.name
        if method is not None:
            cls.registry[name] = method
            return method
        else:
            def register(method, name=name):
                return cls.register(name, method)
            return register

    @classmethod
    def resolve(cls, job_class):
        if isinstance(job_class, str):
            job_class = {'method':job_class}
        if dev.is_dict_like(job_class):
            opts = job_class.copy()
            job_class = opts.pop('method')
        else:
            opts = {}
        if isinstance(job_class, str):
            job_class = cls.registry[job_class]
        return job_class, opts

    __common_aliases__ = {}

    # {common_name: canonical_prop_name | "block.subopt" | callable(value, opts)->(key, value)}

    @classmethod
    def get_common_aliases(cls):
        return cls.__common_aliases__

    _common_alias_priority = ('nproc', 'memory', 'checkpoint')
    @classmethod
    def translate_common_opts(cls, opts):
        """
        Rewrites universal option names (`memory`, `nproc`, `checkpoint`, ...) into
        whatever this backend's `__common_aliases__` maps them to, before block
        routing. A target can be a canonical prop name, a dotted "block.subopt"
        path (for options nested in a `%block ... end`-style spec), or a callable
        that gets first crack (useful when one common option depends on another,
        e.g. ORCA's per-core `MaxCore` depending on `nproc`).
        """
        aliases = cls.get_common_aliases()
        if not aliases:
            return opts
        opts = dict(opts)
        ordered = sorted(
            aliases,
            key=lambda k: cls._common_alias_priority.index(k)
            if k in cls._common_alias_priority else len(cls._common_alias_priority)
        )
        for common_name in ordered:
            if common_name not in opts:
                continue
            val = opts.pop(common_name)
            target = aliases[common_name]
            if target is None:
                raise ValueError(f"{cls.__name__} has no equivalent for common option {common_name!r}")
            elif callable(target):
                key, val = target(val, opts)
                opts[key] = val
            elif '.' in target:
                block_key, sub_key = target.split('.', 1)
                sub = opts.get(block_key, {})
                sub = dict(sub) if dev.is_dict_like(sub) else {}
                sub[sub_key] = val
                opts[block_key] = sub
            else:
                opts[target] = val
        return opts


    distance_units = 'Angstroms'
    @classmethod
    def get_mol_options(cls, mol, units=None, use_internals=False) -> dict:
        opts = {
            'atoms':mol.atoms,
            'bonds':mol.bonds
        }
        spin = mol.spin
        if spin is not None:
            opts['multiplicity'] = spin
        charge = mol.charge
        if charge is not None:
            opts['charge'] = charge
        if units is None:
            units = cls.distance_units
        if use_internals and mol.internals is not None:
            opts['zmatrix'] = mol.internals['zmatrix']
            opts['internals'] = coordops.zmatrix_unit_convert(
                mol.internal_coordinates,
                UnitsData.convert("BohrRadius", units)
            )
        else:
            opts['cartesians'] = mol.coords * UnitsData.convert("BohrRadius", units)
        return opts
    @classmethod
    def from_mol(cls, mol, *args, use_internals=False, **etc):
        return  cls(
            *args,
            **(cls.get_mol_options(mol, use_internals=use_internals) | etc)
        )

    def __init__(self, **opts):
        """
        **LLM Docstring**

        Set up the job: collect its block types and template, index which option names
        belong to which block, and sort the supplied options into per-block buckets.

        :param opts: the job options, distributed across the blocks
        """
        self.job_opts = dict(opts)  # as supplied, before common-option translation (used by `dependencies` and `submit`)
        opts = self.translate_common_opts(opts)
        self.blocks = self.get_block_types()
        self.base_template = self.load_template()
        self._block_keys = {
            k:b
            for b in self.get_block_types()
            for k in b.__props__
        }
        self.block_opts = self.populate_blocks(opts)
    @abc.abstractmethod
    def get_block_types(self):
        """
        **LLM Docstring**

        Abstract: return the ordered list of `OptionsBlock` types making up this job.

        :return: the block types
        :rtype: list
        """
        ...
    @abc.abstractmethod
    def load_template(self):
        """
        **LLM Docstring**

        Abstract: return the top-level job template.

        :return: the job template
        :rtype: str
        """
        ...

    def populate_blocks(self, opts):
        """
        **LLM Docstring**

        Route each supplied option into the first block that recognizes it, raising if
        any option matches no block.

        :param opts: the job options
        :type opts: dict
        :return: one option dict per block (in block order)
        :rtype: list[dict]
        :raises ValueError: if an option matches no block
        """
        block_opts = [
            {} for b in self.blocks
        ]
        bad_opts = set()
        for o,v in opts.items():
            for i,b in enumerate(self.blocks):
                valid, n = b.check_canon(o, v)
                if valid:
                    block_opts[i][n] = v
                    break
            else:
                bad_opts.add(o)
        if len(bad_opts) > 0:
            raise ValueError(f"can't find block type for opts {bad_opts} in {self.blocks}")

        return block_opts

    def get_params(self):
        """
        **LLM Docstring**

        Build every block's parameters and merge them into a single template-parameter
        mapping, raising on key collisions between blocks.

        :return: the merged template parameters
        :rtype: dict
        :raises ValueError: if two blocks produce the same key
        """
        block_opts = [
            b(**o).get_params()
            for b, o in zip(self.blocks, self.block_opts)
        ]
        all_opts = block_opts[0]
        for o in block_opts[1:]:
            double_keys = all_opts.keys() & o.keys()
            if len(double_keys) > 0:
                raise ValueError(f"got duplicate keys {double_keys}")
            all_opts = dict(all_opts, **o)
        return all_opts

    def format(self):
        """
        **LLM Docstring**

        Render the full job input file by filling the job template with the merged block
        parameters.

        :return: the formatted job text
        :rtype: str
        """
        all_opts = self.get_params()
        return OptionalTemplate(self.base_template).apply(**all_opts)

    def write(self, file, mode='w'):
        """
        **LLM Docstring**

        Write the formatted job to a file (path or open stream).

        :param file: an open stream or a file path
        :type file: str | IO
        :param mode: the file mode when a path is given
        :type mode: str
        :return: the file/stream that was written
        :rtype: str | IO
        """
        if hasattr(file, 'write'):
            file.write(self.format())
        else:
            with open(file, mode) as out:
                out.write(self.format())
        return file

    # ------------------------------------------------------------------
    # dependencies, running, and submission
    # ------------------------------------------------------------------
    @classmethod
    def get_dependencies(cls, **opts):
        """
        Hook for subclasses: the requirements of this program given (some of) the job options.
        The base implementation only requires `executable` to be on `PATH`. Subclasses should start from
        `super().get_dependencies(**opts)` and add what their options imply (extra programs, packages, ...).
        Unknown options must be ignored.

        :param opts: the job options (``method``, ``nproc``, ...), as they would be passed to the constructor
        :return: the requirements
        :rtype: JobDependencies
        """
        from .Dependencies import JobDependencies
        deps = JobDependencies()
        if cls.executable is not None:
            deps.add('executable', cls.executable)
        return deps

    @classmethod
    def discover_dependencies(cls, *, engine=None, **opts):
        """
        Work out what an environment needs in order to run this kind of job, without building or running it.
        Environments can render the result with `to_pixi_toml`, `to_pyproject_toml` or `module_load_commands`,
        or test it against the current environment with `check`.

        :param engine: the engine the job will be submitted through (a registered name or an engine); a SLURM engine
            adds ``sbatch``
        :param opts: the job options; any that influence what is needed (method, nproc, ...) are taken into account
        :return: the requirements
        :rtype: JobDependencies
        """
        deps = cls.get_dependencies(**opts)
        eng_name = engine if isinstance(engine, str) else getattr(engine, 'name', None)
        if eng_name == 'slurm':
            deps.add('executable', 'sbatch', reason='SLURM engine')
        return deps

    @property
    def dependencies(self):
        """
        The dependencies of *this* job (`discover_dependencies` with the options it was built from).
        """
        return type(self).discover_dependencies(**getattr(self, 'job_opts', {}))

    def get_run_command(self, input_file, output_file=None, *, nproc=None, executable=None, **run_opts):
        """
        The argument list that runs the program on `input_file`, from inside the work directory.
        Subclasses override this when the program needs more than ``<executable> <input>``.

        :param input_file: the input file name (relative to the work directory)
        :param output_file: the output file name (relative to the work directory), if the job has one
        :param nproc: the number of processes/threads the job was given
        :param executable: an explicit binary (path or name) replacing `executable`
        :param run_opts: program-specific command-line options
        :rtype: list[str]
        """
        exe = executable or self.executable
        if exe is None:
            raise ValueError(f"{type(self).__name__} does not know which program to run; pass `executable`")
        return [exe, input_file]

    @classmethod
    def parse_output(cls, text):
        """
        Pull what is cheaply available out of the program's output text. The base implementation finds nothing.

        :param text: the output file contents
        :return: parsed values (e.g. ``{'energy': ...}``)
        :rtype: dict
        """
        return {}

    @classmethod
    def collect_results(cls, submission):
        """
        Gather the results of a finished job: by default, `parse_output` of its output file.

        :param submission: the `JobSubmission` that was run
        :rtype: dict
        """
        path = submission.output_path
        if path is None or not os.path.isfile(path):
            return {}
        with open(path, errors='replace') as inp:
            return cls.parse_output(inp.read())

    def _resolve_nproc(self, nproc):
        job_nproc = self.job_opts.get('nproc') if hasattr(self, 'job_opts') else None
        if nproc is None:
            return job_nproc
        if job_nproc is not None and job_nproc != nproc:
            raise ValueError(
                f"{type(self).__name__} was built with nproc={job_nproc} but submit got nproc={nproc}; "
                "the input file fixes the core count, so rebuild the job instead"
            )
        return nproc

    def prepare_submission(self, work_dir=None, name=None, *,
                           nproc=None, executable=None, modules=(), setup_commands=(), environment=None,
                           run_options=None):
        """
        Describe how to run this job without writing or running anything.

        :param work_dir: the directory the job runs in (a new temporary directory by default)
        :param name: the base name of the input/output files (default: the program name)
        :param nproc: the number of processes/threads (default: the job's own ``nproc``)
        :param executable: an explicit binary replacing the class default
        :param modules: environment modules to ``module load`` before running
        :param setup_commands: extra shell lines to run before the program
        :param environment: environment variables to export before running
        :param run_options: program-specific options forwarded to `get_run_command`
        :return: the submission
        :rtype: JobSubmission
        """
        from .Submission import JobSubmission

        if work_dir is None:
            work_dir = tempfile.mkdtemp(prefix=type(self).__name__.lower() + "_")
        if name is None:
            name = type(self).__name__.replace("Job", "").lower() or "job"
        name = re.sub(r"[^A-Za-z0-9_.-]", "_", name)
        ext = getattr(self, 'extension', '.in')
        input_file = name + (ext if ext.startswith('.') else '.' + ext)
        output_file = None if self.output_extension is None else name + self.output_extension
        nproc = self._resolve_nproc(nproc)
        command = self.get_run_command(
            input_file, output_file,
            nproc=nproc, executable=executable, **(run_options or {})
        )
        return JobSubmission(
            self, work_dir, name, command,
            input_file=input_file,
            output_file=output_file,
            stdout_file=output_file if self.stdout_output else None,
            nproc=nproc,
            parallel_model=self.parallel_model,
            modules=modules,
            setup_commands=setup_commands,
            environment=environment
        )

    @staticmethod
    def _resolve_engine(engine):
        from ..ExecutionEngine import ExecutionEngine
        if engine is None:
            engine = 'subprocess'
        if isinstance(engine, str):
            engine = ExecutionEngine.resolve(engine)
        return engine

    def submit(self, engine=None, *,
               work_dir=None, name=None, nproc=None, executable=None,
               modules=(), setup_commands=(), environment=None, run_options=None,
               stage_only=False, check_dependencies=None,
               **engine_opts):
        """
        Write the job's input into `work_dir` and run it through an `ExecutionEngine`.

        :param engine: ``'subprocess'`` (default; a local child process), ``'slurm'``, any other registered engine
            name, or an `ExecutionEngine` instance
        :param work_dir: the directory the job runs in (a new temporary directory by default)
        :param name: the base name of the input/output files
        :param nproc: the number of processes/threads (default: the job's own ``nproc``)
        :param executable: an explicit binary replacing the class default
        :param modules: environment modules to load before running
        :param setup_commands: extra shell lines to run before the program
        :param environment: environment variables to export before running
        :param run_options: program-specific options forwarded to `get_run_command`
        :param stage_only: write the input file and run script, but don't run anything; returns the `JobSubmission`
            (useful for staging a job to another machine)
        :param check_dependencies: check required executables first and raise if they are missing.
            The default (`None`) does this for local engines only, since a scheduler's compute nodes
            may have programs the submitting machine does not.
        :param engine_opts: engine-specific options (for SLURM: ``partition``, ``account``, ``time``, ``mem``, ...)
        :return: a future whose `get_result` returns the output text and what was parsed from it
        :rtype: ExternalProgramFuture | JobSubmission
        """
        from .Submission import ExternalProgramFuture

        submission = self.prepare_submission(
            work_dir, name,
            nproc=nproc, executable=executable, modules=modules,
            setup_commands=setup_commands, environment=environment, run_options=run_options
        )
        if stage_only:
            return submission.write()

        engine = self._resolve_engine(engine)
        if check_dependencies is None:
            check_dependencies = getattr(engine, 'name', None) == 'subprocess'
        if check_dependencies:
            exe = submission.command[0]
            if exe != 'bash' and not (os.path.isabs(exe) and os.access(exe, os.X_OK)):
                import shutil
                if shutil.which(exe) is None and len(submission.modules) == 0 and len(submission.setup_commands) == 0:
                    raise FileNotFoundError(
                        f"can't find {exe!r} on PATH; pass `executable=`, load a module, or see "
                        f"{type(self).__name__}.discover_dependencies()"
                    )
        submission.write()
        future = engine.submit_command(submission, **engine_opts)
        return ExternalProgramFuture(future, submission)
