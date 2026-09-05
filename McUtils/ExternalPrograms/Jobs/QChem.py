import json, os

from .Jobs import ExternalProgramJob, OptionsBlock, SystemBlock

__all__ = [
    "QChemJob"
]

class QChemOptionsBlock(OptionsBlock):
    opts_key = None

    job_params_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'qchem_opts.json')
    _json = None
    @classmethod
    def load_json(cls):
        """
        Load (and cache) the Q-Chem options specification from the bundled JSON file.
        """
        if cls._json is None:
            with open(cls.job_params_json) as opts_json:
                cls._json = json.load(opts_json)
        return cls._json

    @classmethod
    def get_props(cls):
        """
        Return the accepted option names for this block, read from its section of
        the options JSON.
        """
        return list(cls.load_json()[cls.opts_key])


class QChemRemBlock(QChemOptionsBlock):
    """
    The `$rem ... $end` block: Q-Chem's flat `KEY value` option set (method, basis,
    jobtype, memory, convergence controls, ...). Accepted keys come from
    `qchem_opts.json["REM"]` -- extend that file as you go.
    """
    opts_key = "REM"

    __aliases__ = {
        'basis':['basis_set']
    }

    def format_rem_block(self):
        """
        Format the `$rem` body as one `KEY value` line per option.
        """
        lines = "\n".join(f"{k.upper()}  {v}" for k, v in self.opts.items() if v is not None)
        return "\n".join(["$rem", lines, "$end"]) if len(self.opts) > 0 else ""

    def get_params(self):
        block = self.format_rem_block()
        return {"rem": block} if len(block) > 0 else {}


class QChemMoleculeBlock(SystemBlock):
    """
    The `$molecule ... $end` block. Falls back to `read` (reuse the geometry from a
    prior job in the same input) when no Cartesians are supplied.

    NOTE: only Cartesians are wired up here -- `zmatrix`/`internals` support (which
    `SystemBlock` already declares props for) still needs Q-Chem's Z-matrix format.
    """
    fmt_key = ""

    def format_molecule_block(self):
        charge = self.opts.get("charge", 0)
        multiplicity = self.opts.get("multiplicity", 1)
        carts = self.opts.get("cartesians")
        atoms = self.opts.get("atoms")

        chunks = ["$molecule", f"{charge} {multiplicity}"]
        if carts is not None:
            chunks.append(carts if isinstance(carts, str) else self.fmt_carts(atoms, carts))
        else:
            chunks.append("read")
        chunks.append("$end")
        return "\n".join(chunks)

    def get_params(self):
        base_opts = {}
        if len(self.opts) > 0:
            base_opts["molecule"] = self.format_molecule_block()
        return base_opts


class QChemSectionsBlock(QChemOptionsBlock):
    """
    Generic pass-through for any other Q-Chem `$section ... $end` block (`$basis`,
    `$ecp`, `$comment`, `$external_charges`, `$pcm`, `$plots`, `$xc_functional`,
    ...; see https://manual.q-chem.com/6.4/A2.S1.SS2.html for the documented set).
    Each option's value is the section's literal body text, supplied as-is by the
    caller -- no per-section formatting happens here, since the syntax differs
    enough across sections (and changes across Q-Chem versions) that a raw string
    is the more durable contract than a bespoke formatter per section.
    """
    opts_key = "Sections"

    __aliases__ = {
        'basis': ['custom_basis']
    }

    def format_sections(self):
        chunks = []
        for name, body in self.opts.items():
            if body is None:
                continue
            body = body if isinstance(body, str) else str(body)
            chunks.append(f"${name}\n{body.strip()}\n$end")
        return "\n\n".join(chunks)

    def get_params(self):
        block = self.format_sections()
        return {"extra_sections": block} if len(block) > 0 else {}


@ExternalProgramJob.register("qchem")
class QChemJob(ExternalProgramJob):
    extension = ".in"
    job_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Templates', 'qchem_job.in')
    blocks = [
        QChemMoleculeBlock,
        QChemRemBlock,
        QChemSectionsBlock
    ]

    __common_aliases__ = {
        'memory': 'MEM_TOTAL',
        'checkpoint': None
    }

    def __init__(self, *strs, **opts):
        for o in strs:
            opts.setdefault('jobtype', o)
        super().__init__(**opts)

    @classmethod
    def get_block_types(cls):
        return cls.blocks

    @classmethod
    def load_template(cls):
        return cls.job_template