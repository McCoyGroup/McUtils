import abc
from ...Formatters import OptionalTemplate
__all__ = ['OptionsBlock', 'ExternalProgramJob']

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
        ...

class JobBlock(JobBlockBase):
    template = None

    def __init__(self, **opts):
        """
        **LLM Docstring**

        Store the raw options for this block.

        :param opts: the block's options
        """
        ...

    def get_template(self):
        """
        **LLM Docstring**

        Return the block's class-level template.

        :return: the template string
        :rtype: str
        """
        ...

    def get_params(self):
        """
        **LLM Docstring**

        Return the block options as template parameters, formatting any value that
        exposes a `format` method.

        :return: the template parameters
        :rtype: dict
        """
        ...

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
        ...
    _canon_opts = None

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the tuple of option names this block accepts.

        :return: the accepted property names
        :rtype: tuple
        """
        ...

    @classmethod
    def get_aliases(cls):
        """
        **LLM Docstring**

        Return the mapping of canonical option names to their accepted aliases.

        :return: the alias mapping
        :rtype: dict
        """
        ...

    @classmethod
    def get_canonical_opts_map(cls):
        """
        **LLM Docstring**

        Return (and cache) the lower-case-to-canonical mapping of the block's property
        names.

        :return: the canonicalization mapping
        :rtype: dict
        """
        ...
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
        ...
    _inv_alias_map = None

    @classmethod
    def get_inverse_alias_map(cls):
        """
        **LLM Docstring**

        Return (and cache) the lower-case-alias-to-canonical-name mapping.

        :return: the inverse alias mapping
        :rtype: dict
        """
        ...
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
        ...

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
        ...

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
        ...

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
        ...

class SystemBlock(OptionsBlock):
    __props__ = ('charge', 'multiplicity', 'atoms', 'cartesians', 'zmatrix', 'ordering', 'internals', 'bonds')

    @classmethod
    def fmt_carts(cls, atoms, carts, float_fmt='{:11.8f}'):
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
        ...

    @classmethod
    def fmt_zmat(cls, atoms, zmat, ordering=None, float_fmt='{:11.8f}'):
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
        ...

    @classmethod
    def fmt_orca_zmat(cls, atoms, zmat, ordering=None, float_fmt='{:11.8f}'):
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
        ...

    def format_bonds_block(self):
        """
        **LLM Docstring**

        Format the block's explicit bond list (pairs, optionally with a bond order) into
        one line per bond.

        :return: the formatted bonds block
        :rtype: str
        """
        ...

class ExternalProgramJob(metaclass=abc.ABCMeta):

    def __init__(self, **opts):
        """
        **LLM Docstring**

        Set up the job: collect its block types and template, index which option names
        belong to which block, and sort the supplied options into per-block buckets.

        :param opts: the job options, distributed across the blocks
        """
        ...

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
        ...

    def get_params(self):
        """
        **LLM Docstring**

        Build every block's parameters and merge them into a single template-parameter
        mapping, raising on key collisions between blocks.

        :return: the merged template parameters
        :rtype: dict
        :raises ValueError: if two blocks produce the same key
        """
        ...

    def format(self):
        """
        **LLM Docstring**

        Render the full job input file by filling the job template with the merged block
        parameters.

        :return: the formatted job text
        :rtype: str
        """
        ...

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
        ...