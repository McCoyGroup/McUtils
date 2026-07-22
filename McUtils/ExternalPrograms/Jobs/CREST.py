import json, numbers, os

from .Jobs import ExternalProgramJob, OptionsBlock, SystemBlock

__all__ = [
    "CRESTJob"
]

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
        if cls._json is None:
            with open(cls.job_params_json) as opts_json:
                cls._json = json.load(opts_json)
        return cls._json

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted option names for this block, read from its section of the
        options JSON.

        :return: the accepted property names
        :rtype: list
        """
        return list(cls.load_json()[cls.opts_key])

class CRESTProcessBlock(CRESTOptionsBlock):
    opts_key = "Process"

    def format_export(self):
        """
        **LLM Docstring**

        Format the process/environment options as shell `export` lines.

        :return: the formatted export commands, or `None` if there are none
        :rtype: str | None
        """
        if len(self.opts) == 0:
            return None

        return "\n".join(
            f'export {k} {v}'
            for k, v in self.opts.items()
            if v is not None
        )

    def get_params(self):
        """
        **LLM Docstring**

        Return the `command_line` parameter carrying the `export` commands (or an empty
        dict).

        :return: the process template parameters
        :rtype: dict
        """
        cmd = self.format_export()
        if cmd is None:
            return {}
        else:
            return {
                'command_line': cmd
            }

class CRESTCommandLineBlock(CRESTOptionsBlock):
    opts_key = "CommandLine"

    __aliases__ = {'chrg':'charge'}
    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted command-line options, adding the `chrg` (charge) flag.

        :return: the accepted property names
        :rtype: list
        """
        return ["chrg"] + super().get_props()

    argument_spacer = "\\ \n" + " " * 14
    def format_command_line(self):
        """
        **LLM Docstring**

        Format the CREST command-line flags (`--flag` / `--flag value`), inlining a few
        flags but line-wrapping longer argument lists.

        :return: the formatted command-line arguments, or `None` if there are none
        :rtype: str | None
        """
        if len(self.opts) == 0:
            return None
        elif len(self.opts) < 3:
            return "  ".join(
                f"--{k}" if v is True else f'--{k} {v}'
                for k, v in self.opts.items()
                if v is not None
            )
        else:
            return self.argument_spacer + self.argument_spacer.join(
                f"--{k}  " if v is True else f'--{k} {v}  '
                for k,v in self.opts.items()
                if v is not None
            )

    def get_params(self):
        """
        **LLM Docstring**

        Return the `command_line` parameter carrying the formatted CREST flags (or an
        empty dict).

        :return: the command-line template parameters
        :rtype: dict
        """
        cmd = self.format_command_line()
        if cmd is None:
            return {}
        else:
            return {
                'command_line': cmd
            }

class CRESTPathsBlock(OptionsBlock):
    __props__ = ('geom_file', 'crest_path', "log_file")
    __aliases__ = {'geom_file':['input_file'], 'crest_path':['path']}


class CRESTSystemBlock(SystemBlock):
    __props__ = ("atoms", "cartesians")

    fmt_key = ""

    def format_coordinate_block(self):
        """
        **LLM Docstring**

        Format the molecule as an XYZ block (atom count, blank comment line, then the
        Cartesian coordinates).

        :return: the formatted XYZ block
        :rtype: str
        """
        atoms = self.opts.get("atoms")
        carts = self.opts.get("cartesians")
        return f"{len(atoms)}\n\n" + self.fmt_carts(atoms, carts)

    def get_params(self):
        """
        **LLM Docstring**

        Return the molecule-specification template parameters (the XYZ coordinate
        block).

        :return: the system template parameters
        :rtype: dict
        """
        base_opts = {}
        if len(self.opts) > 0:
            base_opts[self.fmt_key + "system"] = self.format_coordinate_block()
        return base_opts

@ExternalProgramJob.register("crest")
class CRESTJob(ExternalProgramJob):
    job_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'crest_job.sh')
    blocks = [
        CRESTPathsBlock,
        CRESTProcessBlock,
        CRESTCommandLineBlock,
        CRESTSystemBlock
    ]

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
        # for o in strs:
        #     rt, o = OrcaKeywordsBlock.check_canon(o)
        #     if rt:
        #         opts[o] = True
        #     else:
        #         o[]
        opts = {o.lower():v for o,v in opts.items()}
        for o in strs:
            opts[o.lower()] = True
        super().__init__(path=path, input_file=input_file, log_file=log_file, **opts)

    # @classmethod
    # def get_extra_keys(cls):
    #     with open(cls.job_template) as r:
    #         t = r.read()
    #     return {s.strip("{").strip("}") for s in t.split()}

    @classmethod
    def get_block_types(cls):
        """
        **LLM Docstring**

        Return the ordered CREST block types.

        :return: the block types
        :rtype: list
        """
        return cls.blocks

    @classmethod
    def load_template(cls):
        """
        **LLM Docstring**

        Return the path to the CREST job (shell-script) template.

        :return: the template path
        :rtype: str
        """
        return cls.job_template

    # non_blank_line_terminated = {'link0', 'level_of_theory'}
    # def get_params(self):
    #     base_params = super().get_params()
    #     for k,b in base_params.items():
    #         if k not in self.non_blank_line_terminated:
    #             base_params[k] = b + "\n"
    #
    #     return base_params