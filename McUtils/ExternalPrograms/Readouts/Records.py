"""
Readouts for chemical records: SMILES strings (tokenized into atoms and bonds by `SMILESTokenizer`; no
toolkit needed), and resource-API compound records (`PubChemAPI.Compound` and other records that
were already fetched; nothing is fetched here). Element and other reference-data records are in
`McUtils.Data.Readouts`.
"""

import numbers

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutFields, ReadoutTable, ReadoutImage,
    FieldSet, Field, Column, TabularData, record_nodes,
)

__all__ = [
    "SMILESReadout",
    "CompoundRecordReadout",
]


class SMILESReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for a SMILES string: the tokenized atom sequence (element, bonding to the previous atom,
    stereo marks), element counts, and an RDKit depiction when RDKit is installed.
    """
    readout_id = "smiles"

    def __init__(self, smiles):
        super().__init__(str(smiles))

    def get_readout_title(self):
        return self.obj

    def tokens(self):
        from ..SMILES import SMILESTokenizer
        return list(SMILESTokenizer().tokenize(self.obj))

    @readout_section("summary", title="SMILES")
    def readout_summary(self, ctx):
        """String, atom count and element composition (explicit atoms only)."""
        toks = self.tokens()
        counts = {}
        for t in toks:
            s = t.symbol.capitalize() if t.symbol.islower() else t.symbol
            counts[s] = counts.get(s, 0) + 1
        aromatic = sum(1 for t in toks if t.symbol.islower())
        f = [Field("smiles", self.obj, label="SMILES", quantity="identifier"),
             Field("atoms", len(toks), label="Explicit atoms", quantity="int"),
             Field("composition", " ".join(f"{k}{v}" for k, v in sorted(counts.items())), label="Composition"),
             Field("aromatic", aromatic, label="Aromatic atoms", quantity="int"),
             Field("stereocenters", sum(1 for t in toks if t.stereochemistry), label="Stereo-marked atoms",
                   quantity="int")]
        return ReadoutFields(FieldSet(f, name="summary"))

    @readout_section("atoms", title="Tokenized atoms")
    def readout_atoms(self, ctx):
        """One row per atom token: index, symbol, previous atom, bond order, stereochemistry."""
        toks = self.tokens()
        cols = [Column("index", np.array([t.index for t in toks]), label="#", quantity="index"),
                Column("symbol", np.array([t.symbol for t in toks]), label="Symbol"),
                Column("previous", np.array([-1 if t.previous is None else t.previous for t in toks]), label="Bonded to"),
                Column("bond_order", np.array([np.nan if t.bond_order is None else float(t.bond_order) for t in toks]),
                       label="Bond order", fmt="{:.1f}"),
                Column("stereo", np.array([str(t.stereochemistry or "") for t in toks]), label="Stereo"),
                Column("bond_stereo", np.array([str(t.bond_stereochemistry or "") for t in toks]), label="Bond stereo")]
        return ReadoutTable(TabularData(cols, name="tokens"))

    def _has_rdkit(self):
        import importlib.util
        return importlib.util.find_spec("rdkit") is not None, "RDKit is not installed"

    @readout_section("depiction", title="2D structure", available="_has_rdkit")
    def readout_depiction(self, ctx, size=(420, 300)):
        """RDKit depiction (SVG with a PNG fallback for PowerPoint)."""
        from rdkit import Chem
        from rdkit.Chem.Draw import rdMolDraw2D
        mol = Chem.MolFromSmiles(self.obj)
        if mol is None:
            raise ReadoutSectionUnavailable("RDKit could not parse the SMILES")

        def draw(d):
            d.drawOptions().clearBackground = True
            d.DrawMolecule(mol)
            d.FinishDrawing()
            return d.GetDrawingText()

        svg = draw(rdMolDraw2D.MolDraw2DSVG(*size))
        png = draw(rdMolDraw2D.MolDraw2DCairo(size[0] * 2, size[1] * 2))
        return ReadoutImage(svg[svg.find("<svg"):].encode(), content_type="image/svg+xml", fallback=png, id="image")


class CompoundRecordReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for an already-fetched compound record (e.g. `PubChemAPI.Compound`) or any mapping of
    compound properties. Identifier-like properties go first; nothing is requested over the network.
    """
    readout_id = "compound"
    identifier_keys = ("CID", "IUPACName", "Title", "MolecularFormula", "CanonicalSMILES", "IsomericSMILES",
                       "SMILES", "InChI", "InChIKey")

    def props(self):
        r = self.obj
        for attr in ("props", "properties", "data"):
            v = getattr(r, attr, None)
            if isinstance(v, dict):
                out = dict(v)
                if getattr(r, "cid", None) is not None:
                    out.setdefault("CID", r.cid)
                return out
        if isinstance(r, dict):
            return dict(r)
        return {k: v for k, v in vars(r).items() if not k.startswith("_")}

    def get_readout_title(self):
        p = self.props()
        return str(p.get("IUPACName") or p.get("Title") or p.get("MolecularFormula") or "Compound")

    @readout_section("identifiers", title="Identifiers")
    def readout_identifiers(self, ctx):
        """Identifier fields."""
        p = self.props()
        f = [Field(k.lower(), p[k], label=k, quantity="identifier" if "SMILES" in k or "InChI" in k else None)
             for k in self.identifier_keys if k in p and p[k] is not None]
        if not f:
            raise ReadoutSectionUnavailable("no identifiers")
        return ReadoutFields(FieldSet(f, name="identifiers"))

    @readout_section("properties", title="Properties")
    def readout_properties(self, ctx):
        """Every other property."""
        p = {k: v for k, v in self.props().items() if k not in self.identifier_keys}
        if not p:
            raise ReadoutSectionUnavailable("no other properties")
        return record_nodes(p, "properties")
