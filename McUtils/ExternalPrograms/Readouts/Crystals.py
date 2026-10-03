"""
Readout for crystallographic (CIF) records: publication/composition metadata, cell geometry,
symmetry operations, asymmetric-unit sites and a unit-cell scene. Symmetry-expanded positions
are wrapped into the cell and de-duplicated here (`CIFConverter.atoms` applies every operation
without either step).
"""

import os
import re

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutFields, ReadoutTable, ReadoutArray,
    FieldSet, Field, ArrayData, Column, TabularData, structure_scene, cell_matrix, element_symbol,
)

__all__ = [
    "CIFReadout",
    "expand_cif_sites",
]


def _f(v):
    """CIF numbers may carry uncertainties: '3.97(2)' -> 3.97."""
    if isinstance(v, (int, float, np.number)):
        return float(v)
    m = re.match(r"\s*([-+0-9.eE]+)", str(v))
    return float(m.group(1)) if m else np.nan


def expand_cif_sites(symbols, fractional, transformations, tol=1e-3):
    """
    Apply each 4×4 fractional-space symmetry operation to every site, wrap into [0, 1) and drop
    duplicates. Returns ``(symbols, fractional (n, 3), site_index (n,))``.
    """
    fractional = np.asarray(fractional, dtype=float)
    out_s, out_f, out_i = [], [], []
    for i, (s, f) in enumerate(zip(symbols, fractional)):
        h = np.append(f, 1.0)
        imgs = np.einsum("nij,j->ni", np.asarray(transformations, dtype=float), h)[:, :3]
        imgs = imgs - np.floor(imgs + tol / 10)
        kept = []
        for p in imgs:
            if all(np.linalg.norm((p - q) - np.round(p - q)) > tol for q in kept):
                kept.append(p)
        for p in kept:
            out_s.append(s)
            out_f.append(p)
            out_i.append(i)
    return out_s, np.array(out_f), np.array(out_i)


class CIFReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for a CIF data block (a `CIFConverter`, the list of blocks from `CIFParser.parse`,
    or one block dict). Lengths are Å, angles degrees; fractional coordinates are dimensionless.
    """
    readout_id = "cif"

    def __init__(self, data, source=None, block=0):
        from ..Parsers import CIFConverter
        if not isinstance(data, CIFConverter):
            blocks = data if isinstance(data, list) else [data]
            data = CIFConverter(blocks[block:block + 1] if len(blocks) > 1 else blocks)
        super().__init__(data)
        self.source = source

    @classmethod
    def from_file(cls, file, block=0):
        from ..Parsers import CIFParser
        with CIFParser(file, ignore_comments=True) as p:
            blocks = p.parse()
        return cls(blocks, source=file, block=block)

    @property
    def conv(self):
        return self.obj

    def block(self):
        c = self.conv
        for a in ("cif_data", "data", "blocks", "struct"):
            v = getattr(c, a, None)
            if isinstance(v, list) and v and isinstance(v[0], dict):
                return v[0]
            if isinstance(v, dict):
                return v
        return {}

    def find(self, name, default=None):
        try:
            v = self.conv.find(name)
        except Exception:
            v = None
        return default if v is None else v

    def cell(self):
        cp = self.conv.cell_properties
        return {k: _f(cp[k]) for k in ("cell_length_a", "cell_length_b", "cell_length_c",
                                         "cell_angle_alpha", "cell_angle_beta", "cell_angle_gamma") if k in cp}

    def lattice(self):
        c = self.cell()
        return cell_matrix(c["cell_length_a"], c["cell_length_b"], c["cell_length_c"],
                           c["cell_angle_alpha"], c["cell_angle_beta"], c["cell_angle_gamma"])

    def sites(self):
        ap = self.conv.atom_properties
        labels = list(ap.get("atom_site_label", []))
        types = list(ap.get("atom_site_type_symbol", labels))
        frac = np.column_stack([np.asarray([_f(x) for x in np.atleast_1d(ap[f"atom_site_fract_{k}"])])
                                for k in "xyz"])
        occ = np.asarray([_f(x) for x in np.atleast_1d(ap.get("atom_site_occupancy", np.ones(len(labels))))])
        return labels, [element_symbol(t) for t in types], frac, occ

    def operations(self):
        sp = self.conv.symmetry_properties
        ops = sp.get("symmetry_equiv_pos_as_xyz")
        if ops is None:
            return [], np.eye(4)[None]
        symms = list(getattr(ops, "symms", []))
        return [str(s) for s in symms], np.asarray(ops.transformation, dtype=float)

    def get_readout_title(self):
        name = self.find("chemical_name_systematic") or self.find("chemical_formula_sum") or "Crystal structure"
        return str(name).strip().strip("'")

    def get_readout_subtitle(self):
        return os.path.basename(self.source) if self.source else None

    # ---- sections ---------------------------------------------------------------------- #
    @readout_section("summary", title="Record")
    def readout_summary(self, ctx):
        """Composition, space group and publication metadata."""
        f = []
        if self.source:
            f.append(ctx.field("file", os.path.abspath(self.source), label="File", quantity="path"))
        sp = self.conv.symmetry_properties
        for k, lab in (("chemical_formula_sum", "Formula"), ("chemical_formula_structural", "Structural formula"),
                       ("chemical_name_systematic", "Name")):
            v = self.find(k)
            if v is not None:
                f.append(ctx.field(k, str(v).strip("'"), label=lab))
        for k, lab in (("symmetry_space_group_name_H-M", "Space group (H-M)"),
                       ("symmetry_Int_Tables_number", "IT number"), ("symmetry_cell_setting", "Cell setting")):
            if sp.get(k) is not None:
                f.append(ctx.field(k.replace("-", "_").lower(), str(sp[k]).strip("'"), label=lab))
        for k, lab in (("publ_section_title", "Title"), ("journal_name_full", "Journal"), ("journal_year", "Year"),
                       ("journal_volume", "Volume"), ("cod_database_code", "COD code")):
            v = self.find(k)
            if v is not None:
                if isinstance(v, float) and v.is_integer():
                    v = int(v)
                f.append(ctx.field(k, " ".join(str(v).split()).strip("'"), label=lab))
        return ReadoutFields(FieldSet(f, name="summary"))

    @readout_section("cell", title="Unit cell")
    def readout_cell(self, ctx):
        """Cell lengths and angles, volume, Z and the lattice vectors."""
        c = self.cell()
        f = [ctx.field(k.replace("cell_length_", ""), v, quantity="length", unit="Angstroms",
                       label=k.replace("cell_length_", "")) for k, v in c.items() if "length" in k]
        f += [Field(k.replace("cell_angle_", ""), v, label=k.replace("cell_angle_", "").replace("alpha", "α")
                    .replace("beta", "β").replace("gamma", "γ"), unit="Degrees", quantity="angle")
              for k, v in c.items() if "angle" in k]
        cp = self.conv.cell_properties
        L = self.lattice()
        f.append(ctx.field("volume", float(abs(np.linalg.det(L))), label="Volume (Å³)"))
        if cp.get("cell_formula_units_Z") is not None:
            f.append(Field("z", int(_f(cp["cell_formula_units_Z"])), label="Z", quantity="int"))
        Ld, unit = ctx.convert(L, "length", "Angstroms")
        cols = [Column("vector", np.array(["a", "b", "c"]), label="Vector")] + \
               [Column(k, Ld[:, i], label=k, unit=unit, quantity="length") for i, k in enumerate("xyz")]
        return [ReadoutFields(FieldSet(f, name="cell")), ReadoutTable(TabularData(cols, name="lattice"),
                                                                       title="Lattice vectors")]

    @readout_section("sites", title="Asymmetric unit")
    def readout_sites(self, ctx):
        """Site labels, element, fractional coordinates, occupancy and Wyckoff data."""
        labels, syms, frac, occ = self.sites()
        ap = self.conv.atom_properties
        cols = [Column("label", np.array(labels), label="Label"), Column("element", np.array(syms), label="Element")]
        cols += [Column(f"frac_{k}", frac[:, i], label=f"{k} (frac)", fmt="{:.5f}") for i, k in enumerate("xyz")]
        cols.append(Column("occupancy", occ, label="Occupancy", fmt="{:.3f}"))
        for k, lab in (("atom_site_symmetry_multiplicity", "Mult."), ("atom_site_Wyckoff_symbol", "Wyckoff")):
            if k in ap:
                cols.append(Column(k.split("_")[-1].lower(), np.array([str(x) for x in np.atleast_1d(ap[k])]), label=lab))
        return ReadoutTable(TabularData(cols, name="sites"))

    @readout_section("symmetry", title="Symmetry operations")
    def readout_symmetry(self, ctx):
        """Equivalent positions (as written and as 4×4 fractional-space matrices)."""
        symms, T = self.operations()
        if not symms:
            raise ReadoutSectionUnavailable("no symmetry operations")
        cols = [Column("op", np.arange(1, len(symms) + 1), label="#", quantity="index"),
                Column("xyz", np.array(symms), label="Equivalent position")]
        return [ReadoutTable(TabularData(cols, name="operations")),
                ReadoutArray(ArrayData("matrices", T, axes=("operation", "row", "column"),
                                       label="Affine matrices (fractional)"), display=False)]

    @readout_section("structure", title="Unit cell contents")
    def readout_structure(self, ctx, bonds=False):
        """All symmetry-equivalent sites wrapped into one cell (Cartesian, Å) with the cell edges."""
        labels, syms, frac, occ = self.sites()
        _, T = self.operations()
        s, F, idx = expand_cif_sites(syms, frac, T)
        L = self.lattice()
        xyz = F @ L
        counts = {}
        for x in s:
            counts[x] = counts.get(x, 0) + 1
        comp = " ".join(f"{k}{v}" for k, v in counts.items())
        from ...Jupyter.Readouts import guess_bonds
        bl = guess_bonds(s, xyz) if bonds else None
        cols = [Column("site", np.array([labels[i] for i in idx]), label="Site"),
                Column("element", np.array(s), label="Element")]
        cols += [Column(f"frac_{k}", F[:, i], label=f"{k} (frac)", fmt="{:.5f}") for i, k in enumerate("xyz")]
        Xd, unit = ctx.convert(xyz, "length", "Angstroms")
        cols += [Column(k, Xd[:, i], label=k, unit=unit, quantity="length") for i, k in enumerate("xyz")]
        return [structure_scene(s, xyz, cell=L, bonds=bl if bonds else [], caption=f"{len(s)} atoms per cell ({comp})",
                                id="view", radius_scale=.18),
                ReadoutTable(TabularData(cols, name="cell_atoms"), title="Atoms in the cell")]
