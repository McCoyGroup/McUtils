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
            f'export {k}={v}'
            for k, v in self.opts.items()
            if v is not None
        )

    def get_params(self):
        """
        **LLM Docstring**

        Return the `process_setup` parameter carrying the `export` commands (or an empty
        dict).

        :return: the process template parameters
        :rtype: dict
        """
        cmd = self.format_export()
        if cmd is None:
            return {}
        else:
            return {
                'process_setup': cmd
            }

class CRESTCommandLineBlock(CRESTOptionsBlock):
    opts_key = "CommandLine"

    __aliases__ = {'chrg':['charge']}
    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted command-line options, adding the `chrg` (charge) flag.

        :return: the accepted property names
        :rtype: list
        """
        return ["chrg", "multiplicity"] + super().get_props()

    argument_spacer = " \\\n" + " " * 14
    def format_command_line(self):
        """
        **LLM Docstring**

        Format the CREST command-line flags (`--flag` / `--flag value`), inlining a few
        flags but line-wrapping longer argument lists.

        :return: the formatted command-line arguments, or `None` if there are none
        :rtype: str | None
        """
        opts = dict(self.opts)
        mult = opts.pop('multiplicity', None)  # CREST counts unpaired electrons rather than spin multiplicity
        if mult is not None and mult > 1:
            opts.setdefault('uhf', mult - 1)
        if len(opts) == 0:
            return None
        elif len(opts) < 3:
            return "  ".join(
                f"--{k}" if v is True else f'--{k} {v}'
                for k, v in opts.items()
                if v is not None
            )
        else:
            return self.argument_spacer + self.argument_spacer.join(
                f"--{k}" if v is True else f'--{k} {v}'
                for k,v in opts.items()
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
    __props__ = ("atoms", "cartesians", "bonds")  # `bonds` is accepted (`from_mol` supplies it) but CREST's xyz input has none

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
    __common_aliases__ = {'nproc': 'T'}  # the `--T` command-line flag
    extension = '.sh'
    output_extension = None  # the generated script names its own log file
    executable = 'crest'

    @classmethod
    def get_dependencies(cls, **opts):
        """
        CREST drives xtb, and both are on conda-forge.
        """
        deps = super().get_dependencies(**opts)
        deps.add('conda', 'crest')
        deps.add('conda', 'xtb')
        deps.add('executable', 'xtb')
        return deps

    def get_run_command(self, input_file, output_file=None, *, nproc=None, executable=None, **run_opts):
        """
        The input *is* a shell script that calls `crest`.
        """
        return ['bash', input_file]

    @classmethod
    def parse_output(cls, text):
        """
        :return: ``terminated_normally`` from the CREST log
        """
        return {'terminated_normally': "CREST terminated normally" in text}

    @classmethod
    def collect_results(cls, submission):
        """
        The log's `parse_output` plus the conformer ensemble CREST wrote (``atoms``, ``energies`` in Hartree,
        ``coords`` in Angstrom) read with `CRESTParser`.
        """
        import numpy as np
        from ..Parsers.Crest import CRESTParser

        log = os.path.join(submission.work_dir, submission.job.job_opts.get('log_file', 'confgen.log'))
        res = {}
        if os.path.isfile(log):
            with open(log, errors='replace') as inp:
                res.update(cls.parse_output(inp.read()))
        parser = CRESTParser(submission.work_dir)
        if os.path.isfile(parser.conformers_file):
            confs = parser.parse_conformers()
            res.update(atoms=list(confs.atoms), energies=np.asarray(confs.energies), coords=np.asarray(confs.coords))
        return res
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