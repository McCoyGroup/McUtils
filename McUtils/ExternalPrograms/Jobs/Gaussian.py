import json
import os.path

from .Jobs import ExternalProgramJob, OptionsBlock, SystemBlock

__all__ = [
    "GaussianJob"
]

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
        return list(cls.load_json()[cls.opts_key].keys())

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
        if opt_dict is None:
            opt_list, opt_dict = cls.prep_opts(opt_list)

        base_opts = cls.load_json()
        if ignore_missing and key not in base_opts:
            return

        valid_opts = set(k.lower() for k in base_opts[key])
        bad_opts = []
        for o in opt_list:
            if o.lower() not in valid_opts:
                bad_opts.append(o)
        for o in opt_dict:
            if o.lower() not in valid_opts:
                bad_opts.append(o)
        if len(bad_opts) > 0:
            raise ValueError("got unknown options {} for property {} (known values are {})")

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
        if opt_dict is None:
            if isinstance(opt_list, str):
                return opt_list
            else:
                opt_list, opt_dict = cls.prep_opts(opt_list)

        opt_strings = [
            cls.format_opts(o)
            for o in opt_list
        ] + [
            "{}={}".format(k, cls.format_opts(o))
            for k, o in opt_dict.items()
        ]
        if wrap and len(opt_strings) > 0 or len(opt_strings) > 1:
            return "(" + ",".join(opt_strings) + ")"
        else:
            return "".join(opt_strings)

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
        base_params = []
        if opts is None:
            opts = self.opts
        for k,o in opts.items():
            if o is True:
                base_params.append(k)
            elif o is False:
                ...
            else:
                fmt = self.format_opts(o)
                if len(fmt) == 0:
                    base_params.append(k)
                else:
                    base_params.append(k+"="+fmt)
        return base_params

class GaussianLinkBlock(GaussianOptionsBlock):
    opts_key = "Link0"

    def get_params(self):
        """
        **LLM Docstring**

        Format the Link0 (`%`-prefixed) commands into the `link0` template parameter.

        :return: the `link0` parameter
        :rtype: dict
        """
        base = self.format_base_params()
        return {'link0':"\n".join("%"+b for b in base)}

class GaussianLOTBlock(GaussianOptionsBlock):
    opts_key = "LevelOfTheory"

    @classmethod
    def get_props(cls):
        """
        **LLM Docstring**

        Return the accepted level-of-theory options, adding `basis_set` and
        `level_of_theory` to the JSON-derived list.

        :return: the accepted property names
        :rtype: list
        """
        return ["basis_set", "level_of_theory"] + super().get_props()

    @classmethod
    def get_basis_set_map(cls):
        """
        **LLM Docstring**

        Return the lower-case-to-canonical mapping of the known basis-set names.

        :return: the basis-set name mapping
        :rtype: dict
        """
        return {
            k.lower():k
            for k in cls.load_json()["BasisSets"]
        }

    def get_params(self):
        """
        **LLM Docstring**

        Format the level-of-theory line (`#method(opts)/basis`), pulling the basis set
        from an explicit option or by recognizing a basis-set name among the method
        options.

        :return: the `level_of_theory` parameter (or an empty dict)
        :rtype: dict
        """
        lot = self.opts.get("level_of_theory", self.opts)
        if isinstance(lot, str):
            lot = {lot:[]}
        else:
            lot = lot.copy()

        lots = []
        for method, opts in lot.items():
            opt_list, opt_dict = self.prep_opts(opts)

            if 'basis_set' in opt_dict:
                basis_set = opt_dict['basis_set']
                del opt_dict[basis_set]
            elif 'basis_set' in self.opts:
                basis_set = self.opts['basis_set']
            else:
                bs_map = self.get_basis_set_map()
                for k in opt_list:
                    k = k.lower()
                    if k in bs_map:
                        basis_set = bs_map[k]
                        break
                else:
                    basis_set = ""
                opt_list = [k for k in opt_list if k.lower() not in bs_map]

            self.check_subopts(method, opt_list, opt_dict, ignore_missing=True)

            bs_string = ("/"+basis_set) if len(basis_set) > 0 else ""
            lots.append(
                method + self.format_opts(opt_list, opt_dict, wrap=True) + bs_string
            )

        if len(lots) == 0:
            return {}
        else:
            return {'level_of_theory':"#" + " ".join(lots)}

class GaussianRouteBlock(GaussianOptionsBlock):
    opts_key = "Route"

    @property
    def special_param_dispatch(self):
        """
        **LLM Docstring**

        Mapping from route keywords needing special handling to their handler methods.

        :return: the keyword-to-handler mapping
        :rtype: dict
        """
        return {
            "freq":self.handle_freq
        }

    def handle_freq(self, opts):
        """
        **LLM Docstring**

        Special-case the `freq` route keyword, splitting out the anharmonic/normal mode
        selection sub-options into their own template parameters.

        :param opts: the `freq` sub-options
        :return: `((positional, keyword), extra_template_params)`
        :rtype: tuple
        """
        opt_list, opt_dict = self.prep_opts(opts)
        base = {}
        extra = {}
        for k, o in opt_dict.items():
            if k.lower() in {"selanharmonicmodes"}:
                opt_list.append(k)
                extra["select_anharmonic_modes"] = " ".join(str(i) for i in o)
            elif k.lower() in {"selnormalmodes"}:
                opt_list.append(k)
                extra["select_normal_modes"] = " ".join(str(i) for i in o)
            else:
                base[k] = o

        return (opt_list, base), extra

    linewidth = 80
    def get_params(self):
        """
        **LLM Docstring**

        Format the route section, applying any special-keyword handlers and wrapping the
        `#`-prefixed keyword list to the configured line width.

        :return: the `route` parameter plus any extra parameters
        :rtype: dict
        """
        base_params = {}
        extra_params = {}
        disp = self.special_param_dispatch
        for k,o in self.opts.items():
            d = disp.get(k.lower())
            if d is None:
                base_params[k] = o
            else:
                o1, o2 = d(o)
                base_params[k] = o1
                extra_params.update(o2)
        gp_params = self.format_base_params(base_params)
        blocks = [ [] ]
        bl = 1
        for g in gp_params:
            pad = len(g) + 1
            bl = bl + pad
            if bl > self.linewidth:
                blocks.append([])
                bl = 1 + pad
            blocks[-1].append(g)

        params = {}
        route_str = "\n".join("#" + " ".join(b) for b in blocks if len(b) > 0)
        if len(route_str) > 0:
            params['route'] = route_str
        params.update(extra_params)

        return params

class GaussianSystemBlock(SystemBlock):
    __props__ = SystemBlock.__props__ + ("variables", "constants")

    fmt_key = ""


    @classmethod
    def format_vars_block(cls, vars, float_fmt="{:11.8f}", joiner=None):
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
        if isinstance(vars, dict):
            if joiner is None:
                joiner = "="
            vars = vars.items()
        if joiner is None:
            joiner = " "
        return "\n".join(
            " {k}{joiner}{v}".format(
                k=k,
                joiner=joiner,
                v=v if isinstance(v, str) else float_fmt.format(v)
            )
            for k, v in vars
        )

    def format_coordinate_block(self):
        """
        **LLM Docstring**

        Format the molecule specification: the charge/multiplicity line, the Cartesian
        or Z-matrix coordinates, and any constants/variables sections.

        :return: the formatted coordinate block
        :rtype: str
        :raises ValueError: if neither Cartesians nor a Z-matrix is supplied
        """
        charge = self.opts.get("charge", 0)
        multiplicity = self.opts.get("multiplicity", 1)
        carts = self.opts.get("cartesians")
        zmat = self.opts.get("zmatrix")

        chunks = []
        chunks.append(f"{charge} {multiplicity}")

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

        consts = self.opts.get("constants")
        if consts is None: consts = []
        if len(consts) > 0:
            chunks.append("Constants:")
            chunks.append(self.format_vars_block(consts))
        vars = self.opts.get("variables")
        if vars is None: vars = []
        if len(vars) > 0:
            chunks.append("Variables:")
            chunks.append(self.format_vars_block(vars))

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

class GaussianRestBlock(GaussianOptionsBlock):
    opts_key = "rest"
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
        if cls._json is None:
            with open(cls.job_template) as r:
                t = r.read()
            return {"rest":{s.strip("{").strip("}"):[] for s in t.split()}}
        return cls._json

class GaussianJob(ExternalProgramJob):
    job_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'gaussian_job.gjf')
    blocks = [
        GaussianLinkBlock,
        GaussianLOTBlock,
        GaussianRouteBlock,
        GaussianSystemBlock,
        GaussianRestBlock
    ]

    def __init__(self, *strs, **opts):
        """
        **LLM Docstring**

        Build a Gaussian job, interpreting bare string arguments as either route
        keywords (if recognized) or the level of theory.

        :param strs: bare route keywords / level-of-theory strings
        :param opts: the job options
        """
        for o in strs:
            rt, o = GaussianRouteBlock.check_canon(o)
            if rt:
                opts[o] = True
            else:
                opts['level_of_theory'] = o
        super().__init__(**opts)

    @classmethod
    def get_extra_keys(cls):
        """
        **LLM Docstring**

        Return the set of `{...}` placeholder names present in the job template.

        :return: the template placeholder names
        :rtype: set
        """
        with open(cls.job_template) as r:
            t = r.read()
        return {s.strip("{").strip("}") for s in t.split()}

    @classmethod
    def get_block_types(cls):
        """
        **LLM Docstring**

        Return the ordered Gaussian block types.

        :return: the block types
        :rtype: list
        """
        return cls.blocks

    @classmethod
    def load_template(cls):
        """
        **LLM Docstring**

        Return the path to the Gaussian job template.

        :return: the template path
        :rtype: str
        """
        return cls.job_template

    non_blank_line_terminated = {'link0', 'level_of_theory'}
    def get_params(self):
        """
        **LLM Docstring**

        Assemble the job parameters, appending a trailing blank line to every section
        except the ones that must not be blank-line terminated.

        :return: the template parameters
        :rtype: dict
        """
        base_params = super().get_params()
        for k,b in base_params.items():
            if k not in self.non_blank_line_terminated:
                base_params[k] = b + "\n"

        return base_params