import json, numbers, os
from .Jobs import ExternalProgramJob, OptionsBlock, SystemBlock
__all__ = ['CRESTJob']

class CRESTOptionsBlock(OptionsBlock):
    opts_key = None
    job_params_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'crest_opts.json')
    _json = None

    @classmethod
    def load_json(cls):
        """
        **LLM Docstring**

        Load (and cache) the CREST options specification from the bundled JSON file.

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

class CRESTProcessBlock(CRESTOptionsBlock):
    opts_key = 'Process'

    def format_export(self):
        """
        **LLM Docstring**

        Format the process/environment options as shell `export` lines.

        :return: the formatted export commands, or `None` if there are none
        :rtype: str | None
        """
        ...

    def get_params(self):
        """
        **LLM Docstring**

        Return the `command_line` parameter carrying the `export` commands (or an empty
        dict).

        :return: the process template parameters
        :rtype: dict
        """
        ...

class CRESTCommandLineBlock(CRESTOptionsBlock):
    opts_key = 'CommandLine'
    __aliases__ = {'chrg': 'charge'}

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted command-line options, adding the `chrg` (charge) flag.

        :return: the accepted property names
        :rtype: list
        """
        ...
    argument_spacer = '\\ \n' + ' ' * 14

    def format_command_line(self):
        """
        **LLM Docstring**

        Format the CREST command-line flags (`--flag` / `--flag value`), inlining a few
        flags but line-wrapping longer argument lists.

        :return: the formatted command-line arguments, or `None` if there are none
        :rtype: str | None
        """
        ...

    def get_params(self):
        """
        **LLM Docstring**

        Return the `command_line` parameter carrying the formatted CREST flags (or an
        empty dict).

        :return: the command-line template parameters
        :rtype: dict
        """
        ...

class CRESTPathsBlock(OptionsBlock):
    __props__ = ('geom_file', 'crest_path', 'log_file')
    __aliases__ = {'geom_file': ['input_file'], 'crest_path': ['path']}

class CRESTSystemBlock(SystemBlock):
    __props__ = ('atoms', 'cartesians')
    fmt_key = ''

    def format_coordinate_block(self):
        """
        **LLM Docstring**

        Format the molecule as an XYZ block (atom count, blank comment line, then the
        Cartesian coordinates).

        :return: the formatted XYZ block
        :rtype: str
        """
        ...

    def get_params(self):
        """
        **LLM Docstring**

        Return the molecule-specification template parameters (the XYZ coordinate
        block).

        :return: the system template parameters
        :rtype: dict
        """
        ...

@ExternalProgramJob.register('crest')
class CRESTJob(ExternalProgramJob):
    job_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'crest_job.sh')
    blocks = [CRESTPathsBlock, CRESTProcessBlock, CRESTCommandLineBlock, CRESTSystemBlock]

    def __init__(self, *strs, path='crest', input_file='geom.xyz', log_file='confgen.log', **opts):
        """
        **LLM Docstring**

        Build a CREST job, treating bare string arguments as boolean command-line flags
        and wiring up the CREST executable, input geometry, and log-file paths.

        :param strs: bare command-line flags
        :param path: path to the CREST executable
        :type path: str
        :param input_file: the input geometry file name
        :type input_file: str
        :param log_file: the log file name
        :type log_file: str
        :param opts: the job options
        """
        ...

    @classmethod
    def get_block_types(cls):
        """
        **LLM Docstring**

        Return the ordered CREST block types.

        :return: the block types
        :rtype: list
        """
        ...

    @classmethod
    def load_template(cls):
        """
        **LLM Docstring**

        Return the path to the CREST job (shell-script) template.

        :return: the template path
        :rtype: str
        """
        ...