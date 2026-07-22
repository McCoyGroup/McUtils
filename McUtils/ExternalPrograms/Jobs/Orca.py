import json, numbers, os

from .Jobs import ExternalProgramJob, OptionsBlock, SystemBlock

__all__ = [
    "OrcaJob"
]

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

class OrcaKeywordsBlock(OrcaOptionsBlock):
    opts_key = "Keywords"

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
        if keywords is not None:
            rest.update(keywords)
        super().__init__(**rest)

    _bs = None
    @classmethod
    def load_basis_sets(cls):
        """
        **LLM Docstring**

        Return (and cache) the lower-case-to-canonical mapping of known basis-set names.

        :return: the basis-set name mapping
        :rtype: dict
        """
        if cls._bs is None:
            cls._bs = {k.lower():k for k in cls.load_json()['BasisSets']}
        return cls._bs

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted keywords, combining `keywords`, the JSON-derived list, and
        the known basis-set names.

        :return: the accepted property names
        :rtype: list
        """
        return ['keywords'] + super().get_props() + list(cls.load_basis_sets().values())

    def canonicalize_basis_set(self, k):
        """
        **LLM Docstring**

        Resolve a basis-set name to its canonical spelling.

        :param k: the basis-set name
        :type k: str
        :return: the canonical name
        :rtype: str
        """
        bs = self.load_basis_sets()
        return bs.get(k.lower(), k)

    def get_params(self):
        """
        **LLM Docstring**

        Format the simple-keyword line (the `!`-prefixed keyword list).

        :return: the `keywords` parameter (or an empty dict)
        :rtype: dict
        """
        kws = []
        for k,v in self.opts.items():
            if v is True:
                kws.append(k)
            else:
                if isinstance(v, (str, int, float, )):
                    kws.append(f'{k} {v}')
                else:
                    kws.append(k+" "+" ".join(str(v) for v in v))
        if len(kws) > 0:
            return {"keywords":"!" + " ".join(g for g in kws)}
        else:
            return {}

class OrcaGlobalsBlock(OrcaKeywordsBlock):
    opts_key = "Globals"
    require_value = True

    @classmethod
    def load_basis_sets(cls):
        """
        **LLM Docstring**

        Return an empty basis-set mapping (basis sets are not globals).

        :return: an empty mapping
        :rtype: dict
        """
        return {}

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted globals option names (the keywords list without the leading
        `keywords` entry).

        :return: the accepted property names
        :rtype: list
        """
        return super().get_props()[1:]

    def get_params(self):
        """
        **LLM Docstring**

        Format the global (`%`-prefixed) settings block.

        :return: the `globals` parameter (or an empty dict)
        :rtype: dict
        """
        kws = []
        for k,v in self.opts.items():
            if v is True:
                kws.append(k)
            else:
                if isinstance(v, (str, numbers.Number)):
                    kws.append(f'{k} {v}')
                else:
                    kws.append(k+" "+" ".join(v))
        if len(kws) > 0:
            return {"globals":"\n".join("%"+g for g in kws)}
        else:
            return {}

class OrcaMethodsBlock(OrcaOptionsBlock):
    opts_key = "Blocks"

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
        if opts is not None:
            rest.update(opts)
        super().__init__(**rest)

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
        if opts is True:
            opts = {}
        if len(opts.items()) == 0:
            return ""
        else:
            padding = " " * len("%"+header)
            rows = "\n".join(padding + f"{k} {v}" for k,v in opts.items())
            return "\n".join(["%"+header, rows, padding+"end"])

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted method-block names, plus the catch-all `opts` key.

        :return: the accepted property names
        :rtype: list
        """
        return super().get_props() + ["opts"]

    def get_params(self):
        """
        **LLM Docstring**

        Format all of the requested `%...end` method blocks into the `methods`
        parameter.

        :return: the `methods` parameter (or an empty dict)
        :rtype: dict
        """
        kws = []
        for k,v in self.opts.items():
            method_block = self.format_options_block(k, v)
            if len(method_block) > 0:
                kws.append(method_block)
        if len(kws) > 0:
            return {"methods":"\n".join(kws)}
        else:
            return {}

class OrcaSystemBlock(SystemBlock):
    __props__ = SystemBlock.__props__ + ("variables", "constants")

    fmt_key = ""

    def format_coordinate_block(self):
        """
        **LLM Docstring**

        Format the ORCA coordinate block (`*xyz`/`*gzmt charge mult ... *`) from
        Cartesians or a Z-matrix.

        :return: the formatted coordinate block
        :rtype: str
        :raises ValueError: if neither Cartesians nor a Z-matrix is supplied
        """
        charge = self.opts.get("charge", 0)
        multiplicity = self.opts.get("multiplicity", 1)
        carts = self.opts.get("cartesians")
        zmat = self.opts.get("zmatrix")

        coord_type = ("xyz" if carts is not None else "gzmt")

        chunks = []
        chunks.append(f"*{coord_type} {charge} {multiplicity}")

        if carts is not None:
            if isinstance(carts, str):
                chunks.append(carts)
            else:
                chunks.append(self.fmt_carts(self.opts.get('atoms'), carts))
        elif zmat is not None:
            if isinstance(zmat, str):
                chunks.append(zmat)
            else:
                chunks.append(self.fmt_zmat(self.opts.get('atoms'), zmat, self.opts.get('ordering')))
        else:
            raise ValueError("no coordinate spec supplied")

        chunks.append("*")

        return "\n".join(chunks)

    def get_params(self):
        """
        **LLM Docstring**

        Return the molecule-specification template parameters (the coordinate block and,
        if present, a bonds block).

        :return: the system template parameters
        :rtype: dict
        """
        base_opts = {}
        if len(self.opts) > 0:
            base_opts[self.fmt_key + "system"] = self.format_coordinate_block()
            if len(self.opts.get('bonds', [])) > 0:
                base_opts[self.fmt_key + "bonds"] = self.format_bonds_block()
        return base_opts

@ExternalProgramJob.register("orca")
class OrcaJob(ExternalProgramJob):
    job_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'orca_job.inp')
    blocks = [
        OrcaKeywordsBlock,
        OrcaGlobalsBlock,
        OrcaMethodsBlock,
        OrcaSystemBlock
    ]

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
        if basis_set is not None:
            strs = (basis_set,) + strs
        if level_of_theory is not None:
            strs = (level_of_theory,) + strs
        # for o in strs:
        #     rt, o = OrcaKeywordsBlock.check_canon(o)
        #     if rt:
        #         opts[o] = True
        #     else:
        #         o[]
        opts = {o.lower():v for o,v in opts.items()}
        for o in strs:
            opts[o.lower()] = True
        super().__init__(**opts)

    # @classmethod
    # def get_extra_keys(cls):
    #     with open(cls.job_template) as r:
    #         t = r.read()
    #     return {s.strip("{").strip("}") for s in t.split()}

    @classmethod
    def get_block_types(cls):
        """
        **LLM Docstring**

        Return the ordered ORCA block types.

        :return: the block types
        :rtype: list
        """
        return cls.blocks

    @classmethod
    def load_template(cls):
        """
        **LLM Docstring**

        Return the path to the ORCA job template.

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