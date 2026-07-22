import json
import os.path
from .Jobs import ExternalProgramJob, OptionsBlock, SystemBlock
__all__ = ['GaussianJob']

class GaussianOptionsBlock(OptionsBlock):
    opts_key = None
    job_params_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'gaussian_opts.json')
    _json = None

    @classmethod
    def load_json(cls):
        """
        **LLM Docstring**

        Load (and cache) the Gaussian options specification from the bundled JSON file.

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

    @classmethod
    def check_subopts(cls, key, opt_list, opt_dict=None, ignore_missing=False):
        """
        **LLM Docstring**

        Validate the sub-options passed to a Gaussian keyword against the values allowed
        for it in the options JSON.

        :param key: the keyword whose sub-options are being checked
        :type key: str
        :param opt_list: positional sub-options
        :type opt_list: list
        :param opt_dict: keyword sub-options
        :type opt_dict: dict | None
        :param ignore_missing: skip validation when the keyword isn't in the JSON
        :type ignore_missing: bool
        :raises ValueError: if an unknown sub-option is supplied
        """
        ...

    @classmethod
    def format_opts(cls, opt_list, opt_dict=None, wrap=False):
        """
        **LLM Docstring**

        Format a keyword's sub-options into Gaussian's `opt` or `key=val` /
        `(a,b=c)` syntax, wrapping in parentheses when there is more than one.

        :param opt_list: positional sub-options (or a bare string)
        :type opt_list: list | str
        :param opt_dict: keyword sub-options
        :type opt_dict: dict | None
        :param wrap: force parenthesization
        :type wrap: bool
        :return: the formatted option string
        :rtype: str
        """
        ...

    def format_base_params(self, opts=None):
        """
        **LLM Docstring**

        Format this block's options into a list of `keyword` / `keyword=value` strings,
        dropping options set to `False`.

        :param opts: the options to format (defaults to the block's own)
        :type opts: dict | None
        :return: the formatted option strings
        :rtype: list[str]
        """
        ...

class GaussianLinkBlock(GaussianOptionsBlock):
    opts_key = 'Link0'

    def get_params(self):
        """
        **LLM Docstring**

        Format the Link0 (`%`-prefixed) commands into the `link0` template parameter.

        :return: the `link0` parameter
        :rtype: dict
        """
        ...

class GaussianLOTBlock(GaussianOptionsBlock):
    opts_key = 'LevelOfTheory'

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted level-of-theory options, adding `basis_set` and
        `level_of_theory` to the JSON-derived list.

        :return: the accepted property names
        :rtype: list
        """
        ...

    @classmethod
    def get_basis_set_map(cls):
        """
        **LLM Docstring**

        Return the lower-case-to-canonical mapping of the known basis-set names.

        :return: the basis-set name mapping
        :rtype: dict
        """
        ...

    def get_params(self):
        """
        **LLM Docstring**

        Format the level-of-theory line (`#method(opts)/basis`), pulling the basis set
        from an explicit option or by recognizing a basis-set name among the method
        options.

        :return: the `level_of_theory` parameter (or an empty dict)
        :rtype: dict
        """
        ...

class GaussianRouteBlock(GaussianOptionsBlock):
    opts_key = 'Route'

    @property
    def special_param_dispatch(self):
        """
        **LLM Docstring**

        Mapping from route keywords needing special handling to their handler methods.

        :return: the keyword-to-handler mapping
        :rtype: dict
        """
        ...

    def handle_freq(self, opts):
        """
        **LLM Docstring**

        Special-case the `freq` route keyword, splitting out the anharmonic/normal mode
        selection sub-options into their own template parameters.

        :param opts: the `freq` sub-options
        :return: `((positional, keyword), extra_template_params)`
        :rtype: tuple
        """
        ...
    linewidth = 80

    def get_params(self):
        """
        **LLM Docstring**

        Format the route section, applying any special-keyword handlers and wrapping the
        `#`-prefixed keyword list to the configured line width.

        :return: the `route` parameter plus any extra parameters
        :rtype: dict
        """
        ...

class GaussianSystemBlock(SystemBlock):
    __props__ = SystemBlock.__props__ + ('variables', 'constants')
    fmt_key = ''

    @classmethod
    def format_vars_block(cls, vars, float_fmt='{:11.8f}', joiner=None):
        """
        **LLM Docstring**

        Format a set of variables/constants into `name value` (or `name=value`) lines.

        :param vars: the variables (a mapping or an iterable of pairs)
        :type vars: dict | Iterable
        :param float_fmt: format string for numeric values
        :type float_fmt: str
        :param joiner: separator between name and value (inferred if omitted)
        :type joiner: str | None
        :return: the formatted block
        :rtype: str
        """
        ...

    def format_coordinate_block(self):
        """
        **LLM Docstring**

        Format the molecule specification: the charge/multiplicity line, the Cartesian
        or Z-matrix coordinates, and any constants/variables sections.

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

class GaussianRestBlock(GaussianOptionsBlock):
    opts_key = 'rest'
    job_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'gaussian_job.gjf')

    @classmethod
    def load_json(cls):
        """
        **LLM Docstring**

        Treat every remaining `{...}` placeholder in the job template as an accepted
        "rest" option, so leftover template keys can be filled directly.

        :return: the rest-options specification
        :rtype: dict
        """
        ...

@ExternalProgramJob.register('gaussian')
class GaussianJob(ExternalProgramJob):
    extension = 'gjf'
    job_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'gaussian_job.gjf')
    blocks = [GaussianLinkBlock, GaussianLOTBlock, GaussianRouteBlock, GaussianSystemBlock, GaussianRestBlock]

    def __init__(self, *strs, **opts):
        """
        **LLM Docstring**

        Build a Gaussian job, interpreting bare string arguments as either route
        keywords (if recognized) or the level of theory.

        :param strs: bare route keywords / level-of-theory strings
        :param opts: the job options
        """
        ...

    @classmethod
    def get_extra_keys(cls):
        """
        **LLM Docstring**

        Return the set of `{...}` placeholder names present in the job template.

        :return: the template placeholder names
        :rtype: set
        """
        ...

    @classmethod
    def get_block_types(cls):
        """
        **LLM Docstring**

        Return the ordered Gaussian block types.

        :return: the block types
        :rtype: list
        """
        ...

    @classmethod
    def load_template(cls):
        """
        **LLM Docstring**

        Return the path to the Gaussian job template.

        :return: the template path
        :rtype: str
        """
        ...
    non_blank_line_terminated = {'link0', 'level_of_theory'}

    def get_params(self):
        """
        **LLM Docstring**

        Assemble the job parameters, appending a trailing blank line to every section
        except the ones that must not be blank-line terminated.

        :return: the template parameters
        :rtype: dict
        """
        ...