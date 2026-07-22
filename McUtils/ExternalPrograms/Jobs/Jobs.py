import abc
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

    registry = {}
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
                valid, o = b.check_canon(o, v)
                if valid:
                    block_opts[i][o] = v
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