"""
Readout for molecules held by external chemistry toolkits (`ExternalMolecule` wrappers:
`RDMolecule`, `OBMolecule`, `ASEMolecule`): identifiers, a 2D depiction (RDKit), a 3D view,
atoms (with masses and charges when the toolkit provides them) and bonds. Toolkit coordinates
are in Å.
"""

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutFields, ReadoutTable, ReadoutImage,
    FieldSet, Field, Column, TabularData, structure_scene, atoms_table,
)

__all__ = [
    "ExternalMoleculeReadout",
]


def _safe(f, default=None):
    try:
        v = f()
    except Exception:
        return default
    return default if v is None else v


class ExternalMoleculeReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for an `ExternalMolecule`. Every attribute is read defensively, since wrappers
    implement different subsets (`bonds`/`charges` raise `NotImplementedError` on the base class).
    """
    readout_id = "molecule"

    @property
    def mol(self):
        return self.obj

    def toolkit(self):
        return type(self.mol).__name__.replace("Molecule", "") or "external"

    def formula(self):
        counts = {}
        for a in self.mol.atoms:
            counts[a] = counts.get(a, 0) + 1
        order = (["C", "H"] if "C" in counts else []) + sorted(k for k in counts if not ("C" in counts and k in "CH"))
        return "".join(f"{k}{counts[k] if counts[k] > 1 else ''}" for k in order)

    def get_readout_title(self):
        smi = _safe(lambda: self.mol.to_smiles()) if hasattr(self.mol, "to_smiles") else None
        return f"{self.formula()}" + (f" ({smi})" if smi and len(smi) < 60 else "")

    def get_readout_subtitle(self):
        return f"{type(self.mol).__name__} wrapper"

    @readout_section("identifiers", title="Identifiers")
    def readout_identifiers(self, ctx):
        """Formula, size, charge and the toolkit's string identifiers."""
        m = self.mol
        f = [Field("toolkit", self.toolkit(), label="Toolkit"),
             Field("formula", self.formula(), label="Formula"),
             Field("num_atoms", len(m.atoms), label="Atoms", quantity="int")]
        bonds = _safe(lambda: m.bonds)
        if bonds is not None:
            f.append(Field("num_bonds", len(bonds), label="Bonds", quantity="int"))
        fc = _safe(lambda: m.formal_charges)
        if fc is not None:
            f.append(Field("formal_charge", int(np.sum(fc)), label="Formal charge", quantity="int"))
        masses = _safe(lambda: m.masses)
        if masses is not None:
            f.append(ctx.field("mass", float(np.sum(masses)), quantity="mass", unit="AtomicMassUnits", label="Mass"))
        for meth, key, lab in (("to_smiles", "smiles", "SMILES"), ("to_inchi", "inchi", "InChI"),
                               ("to_inchi_key", "inchi_key", "InChIKey")):
            if hasattr(m, meth):
                v = _safe(getattr(m, meth))
                if v:
                    f.append(Field(key, str(v), label=lab, quantity="identifier"))
        rings = _safe(lambda: m.rings)
        if rings is not None:
            f.append(Field("rings", len(rings), label="Rings", quantity="int"))
        meta = _safe(lambda: m.meta, {})
        for k, v in (meta or {}).items():
            if isinstance(v, (str, int, float, bool)):
                f.append(Field(f"meta_{k}", v, label=str(k)))
        return ReadoutFields(FieldSet(f, name="identifiers"))

    def _has_depiction(self):
        return hasattr(self.mol, "rdmol"), "2D depictions need RDKit"

    @readout_section("depiction", title="2D structure", available="_has_depiction")
    def readout_depiction(self, ctx, size=(420, 300), remove_hydrogens=True):
        """An RDKit 2D depiction (SVG in HTML, PNG fallback in PowerPoint)."""
        from rdkit import Chem
        from rdkit.Chem import rdDepictor
        from rdkit.Chem.Draw import rdMolDraw2D
        mol = Chem.Mol(self.mol.rdmol)
        if remove_hydrogens:
            mol = _safe(lambda: Chem.RemoveHs(mol), mol)
        rdDepictor.Compute2DCoords(mol)

        def draw(drawer):
            drawer.drawOptions().clearBackground = True
            drawer.DrawMolecule(mol)
            drawer.FinishDrawing()
            return drawer.GetDrawingText()

        svg = draw(rdMolDraw2D.MolDraw2DSVG(*size))
        png = _safe(lambda: draw(rdMolDraw2D.MolDraw2DCairo(size[0] * 2, size[1] * 2)))
        svg = svg[svg.find("<svg"):]
        return ReadoutImage(svg.encode(), content_type="image/svg+xml", fallback=png, id="image")

    @readout_section("structure", title="3D structure")
    def readout_structure(self, ctx):
        """3D view and coordinates (with masses and charges when available)."""
        m = self.mol
        coords = np.asarray(m.coords, dtype=float)
        bonds = _safe(lambda: m.bonds)
        extra = {}
        masses = _safe(lambda: m.masses)
        if masses is not None:
            extra["mass"] = ctx.column("mass", np.asarray(masses, dtype=float), quantity="mass",
                                       unit="AtomicMassUnits", label="Mass")
        fc = _safe(lambda: m.formal_charges)
        if fc is not None:
            extra["formal_charge"] = Column("formal_charge", np.asarray(fc, dtype=int), label="Formal charge")
        ch = _safe(lambda: m.charges)
        if ch is not None and len(ch) == len(m.atoms):
            extra["partial_charge"] = Column("partial_charge", np.asarray(ch, dtype=float), label="Partial charge",
                                             fmt="{:.4f}")
        return [structure_scene(list(m.atoms), coords, bonds=bonds, id="view"),
                atoms_table(ctx, list(m.atoms), coords, name="atoms", **extra)]

    def _has_bonds(self):
        return bool(_safe(lambda: self.mol.bonds)), "no bonds"

    @readout_section("bonds", title="Bonds", available="_has_bonds")
    def readout_bonds(self, ctx):
        """Bond list with orders and lengths."""
        m = self.mol
        b = np.asarray([[int(x[0]), int(x[1])] for x in m.bonds])
        order = np.asarray([float(x[2]) if len(x) > 2 else 1.0 for x in m.bonds])
        xyz = np.asarray(m.coords, dtype=float)
        lab = [f"{a}{i + 1}" for i, a in enumerate(m.atoms)]
        cols = [Column("atom_1", np.array([lab[i] for i in b[:, 0]]), label="Atom 1"),
                Column("atom_2", np.array([lab[i] for i in b[:, 1]]), label="Atom 2"),
                Column("order", order, label="Order", fmt="{:.1f}"),
                ctx.column("length", np.linalg.norm(xyz[b[:, 0]] - xyz[b[:, 1]], axis=1), quantity="length",
                           unit="Angstroms", label="Length")]
        return ReadoutTable(TabularData(cols, name="bonds"))
