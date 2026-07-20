import json, numbers, os
from .Jobs import ExternalProgramJob, OptionsBlock, SystemBlock
__all__ = ['OrcaJob']

class OrcaOptionsBlock(OptionsBlock):
    opts_key = None
    job_params_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'orca_opts.json')
    _json = None

    @classmethod
    def load_json(cls):
        """
        **LLM Docstring**

        Load (and cache) the ORCA options specification from the bundled JSON file.

        :return: the options specification
        :rtype: dict
        """
        ...

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted option names for this block, read from its section of the
        options JSON.

        :return: the accepted property names
        :rtype: list
        """
        ...

class OrcaKeywordsBlock(OrcaOptionsBlock):
    opts_key = 'Keywords'
    require_value = False

    def __init__(self, keywords=None, **rest):
        """
        **LLM Docstring**

        Initialize the ORCA simple-keywords block, folding any `keywords` mapping into
        the options.

        :param keywords: an optional mapping of extra keywords
        :type keywords: dict | None
        :param rest: the remaining block options
        """
        ...
    _bs = None

    @classmethod
    def load_basis_sets(cls):
        """
        **LLM Docstring**

        Return (and cache) the lower-case-to-canonical mapping of known basis-set names.

        :return: the basis-set name mapping
        :rtype: dict
        """
        ...

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted keywords, combining `keywords`, the JSON-derived list, and
        the known basis-set names.

        :return: the accepted property names
        :rtype: list
        """
        ...

    def canonicalize_basis_set(self, k):
        """
        **LLM Docstring**

        Resolve a basis-set name to its canonical spelling.

        :param k: the basis-set name
        :type k: str
        :return: the canonical name
        :rtype: str
        """
        ...

    def get_params(self):
        """
        **LLM Docstring**

        Format the simple-keyword line (the `!`-prefixed keyword list).

        :return: the `keywords` parameter (or an empty dict)
        :rtype: dict
        """
        ...

class OrcaGlobalsBlock(OrcaKeywordsBlock):
    opts_key = 'Globals'
    require_value = True

    @classmethod
    def load_basis_sets(cls):
        """
        **LLM Docstring**

        Return an empty basis-set mapping (basis sets are not globals).

        :return: an empty mapping
        :rtype: dict
        """
        ...

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted globals option names (the keywords list without the leading
        `keywords` entry).

        :return: the accepted property names
        :rtype: list
        """
        ...

    def get_params(self):
        """
        **LLM Docstring**

        Format the global (`%`-prefixed) settings block.

        :return: the `globals` parameter (or an empty dict)
        :rtype: dict
        """
        ...

class OrcaMethodsBlock(OrcaOptionsBlock):
    opts_key = 'Blocks'
    require_value = True

    def __init__(self, opts=None, **rest):
        """
        **LLM Docstring**

        Initialize the ORCA method-blocks section, folding an `opts` mapping into the
        options.

        :param opts: an optional mapping of method blocks
        :type opts: dict | None
        :param rest: the remaining block options
        """
        ...

    def format_options_block(self, header, opts):
        """
        **LLM Docstring**

        Format a single `%header ... end` ORCA input block from its option mapping.

        :param header: the block header (e.g. `scf`, `geom`)
        :type header: str
        :param opts: the block's options (or `True` for an empty block)
        :type opts: dict | bool
        :return: the formatted block (empty string if there are no options)
        :rtype: str
        """
        ...

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted method-block names, plus the catch-all `opts` key.

        :return: the accepted property names
        :rtype: list
        """
        ...

    def get_params(self):
        """
        **LLM Docstring**

        Format all of the requested `%...end` method blocks into the `methods`
        parameter.

        :return: the `methods` parameter (or an empty dict)
        :rtype: dict
        """
        ...

class OrcaSystemBlock(SystemBlock):
    __props__ = SystemBlock.__props__ + ('variables', 'constants')
    fmt_key = ''

    def format_coordinate_block(self):
        """
        **LLM Docstring**

        Format the ORCA coordinate block (`*xyz`/`*gzmt charge mult ... *`) from
        Cartesians or a Z-matrix.

        :return: the formatted coordinate block
        :rtype: str
        :raises ValueError: if neither Cartesians nor a Z-matrix is supplied
        """
        ...

    def get_params(self):
        """
        **LLM Docstring**

        Return the molecule-specification template parameters (the coordinate block and,
        if present, a bonds block).

        :return: the system template parameters
        :rtype: dict
        """
        ...

class OrcaJob(ExternalProgramJob):
    job_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'orca_job.inp')
    blocks = [OrcaKeywordsBlock, OrcaGlobalsBlock, OrcaMethodsBlock, OrcaSystemBlock]

    def __init__(self, *strs, basis_set=None, level_of_theory=None, **opts):
        """
        **LLM Docstring**

        Build an ORCA job, treating the basis set, level of theory, and any bare string
        arguments as simple keywords.

        :param strs: bare simple keywords
        :param basis_set: the basis set keyword
        :type basis_set: str | None
        :param level_of_theory: the method keyword
        :type level_of_theory: str | None
        :param opts: the job options
        """
        ...

    @classmethod
    def get_block_types(cls):
        """
        **LLM Docstring**

        Return the ordered ORCA block types.

        :return: the block types
        :rtype: list
        """
        ...

    @classmethod
    def load_template(cls):
        """
        **LLM Docstring**

        Return the path to the ORCA job template.

        :return: the template path
        :rtype: str
        """
        ...