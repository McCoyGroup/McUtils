"""
Readouts for conformer data: ensembles (CREST runs, `CRESTConformers`/`CRESTRotamers`, or any
set of coordinates with energies/weights), single `ConformerRecord`s, and bounded summaries of
`ConformerLibrary` contents (only the entries shown are loaded).
"""

import os

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutSection, ReadoutFields, ReadoutTable,
    ReadoutGallery, ReadoutArray, ReadoutCode, ReadoutText, FieldSet, Field, Column, TabularData, ArrayData,
    structure_scene, atoms_table, line_chart, bar_chart,
)

__all__ = [
    "ConformerEnsembleReadout",
    "CRESTReadout",
    "ConformerRecordReadout",
    "ConformerLibraryReadout",
]

KCAL_PER_HARTREE = 627.5094740631


def _kabsch(P, Q):
    """Rotate/translate ``P`` onto ``Q`` (both (n, 3)); returns the aligned copy of ``P``."""
    p0, q0 = P.mean(0), Q.mean(0)
    H = (P - p0).T @ (Q - q0)
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    return (P - p0) @ R.T + q0


class ConformerEnsembleReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for an ensemble ``(atoms, coords (n, natoms, 3), energies (n,), weights=None)`` with
    coordinates in Å and energies in Hartree. Shows the energy ranking, Boltzmann weights
    (given, or computed at ``temperature``), and the lowest conformers aligned onto the best one.
    """
    readout_id = "ensemble"

    def __init__(self, atoms, coords, energies=None, weights=None, name="Conformer ensemble", source=None,
                 temperature=298.15, meta=None):
        super().__init__(dict(atoms=list(atoms), coords=np.asarray(coords, dtype=float),
                              energies=None if energies is None else np.asarray(energies, dtype=float),
                              weights=None if weights is None else np.asarray(weights, dtype=float)))
        self.name = name
        self.source = source
        self.temperature = temperature
        self.extra_meta = dict(meta or {})

    @classmethod
    def from_crest(cls, crest_conformers, **opts):
        """From a `CRESTConformers` or `CRESTRotamers` record."""
        c = crest_conformers
        return cls(c.atoms, c.coords, getattr(c, "energies", None), getattr(c, "weights", None), **opts)

    @property
    def atoms(self):
        return self.obj["atoms"]

    @property
    def coords(self):
        return self.obj["coords"]

    def order(self):
        e = self.obj["energies"]
        return np.arange(len(self.coords)) if e is None else np.argsort(e, kind="stable")

    def relative(self):
        e = self.obj["energies"]
        return None if e is None else (e - e.min()) * KCAL_PER_HARTREE

    def weights(self):
        w = self.obj["weights"]
        if w is not None:
            return w
        rel = self.relative()
        if rel is None:
            return None
        kT = 0.0019872043 * self.temperature  # kcal/mol
        b = np.exp(-rel / kT)
        return b / b.sum()

    def get_readout_title(self):
        return self.name

    def get_readout_subtitle(self):
        return os.path.basename(str(self.source)) if self.source else None

    @readout_section("summary", title="Ensemble")
    def readout_summary(self, ctx):
        """Size, energy window and populations."""
        n = len(self.coords)
        f = [Field("conformers", n, label="Conformers", quantity="int"),
             Field("atoms", len(self.atoms), label="Atoms per conformer", quantity="int")]
        e = self.obj["energies"]
        if e is not None:
            f.append(ctx.field("lowest", float(e.min()), quantity="energy", unit="Hartrees", label="Lowest energy"))
            f.append(Field("window", float(self.relative().max()), label="Energy window (kcal/mol)", fmt="{:.2f}"))
        w = self.weights()
        if w is not None:
            ws = np.sort(w)[::-1]
            f.append(Field("top_weight", float(ws[0]), label="Population of best", fmt="{:.3f}"))
            f.append(Field("n90", int(np.searchsorted(np.cumsum(ws), .9) + 1), label="Conformers for 90% population",
                           quantity="int"))
            if self.obj["weights"] is None:
                f.append(Field("temperature", self.temperature, label="Boltzmann T (K)", fmt="{:.2f}"))
        for k, v in self.extra_meta.items():
            f.append(Field(k, v, label=k.replace("_", " ")))
        return ReadoutFields(FieldSet(f, name="summary"))

    def _has_energies(self):
        return self.obj["energies"] is not None, "no energies"

    @readout_section("energies", title="Energy ranking", available="_has_energies")
    def readout_energies(self, ctx, max_rows=25):
        """Relative energies and populations, lowest first (the table shows ``max_rows``; all are exported)."""
        o = self.order()
        rel = self.relative()[o]
        e = self.obj["energies"][o]
        w = self.weights()
        cols = [Column("rank", np.arange(1, len(o) + 1), label="Rank", quantity="index"),
                Column("conformer", o + 1, label="Conformer", quantity="index"),
                ctx.column("energy", e, quantity="energy", unit="Hartrees", label="Energy"),
                Column("relative", rel, label="ΔE (kcal/mol)", fmt="{:.3f}")]
        if w is not None:
            cols.append(Column("weight", w[o], label="Population", fmt="{:.4f}"))
        table = TabularData(cols, name="ranking")
        nodes = [line_chart(np.arange(1, len(o) + 1), rel, "Rank", "ΔE (kcal/mol)", markers=len(o) < 80,
                            x_name="rank", id="plot", caption="Relative energies, lowest first"),
                 ReadoutTable(table.take_rows(slice(0, max_rows)),
                              title=f"Lowest {min(max_rows, len(o))} of {len(o)}" if len(o) > max_rows else None)]
        if len(o) > max_rows:
            nodes.append(ReadoutArray(ArrayData("all_relative", rel, label="All ΔE", quantity=None), display=False))
        return nodes

    @readout_section("conformers", title="Lowest conformers")
    def readout_conformers(self, ctx, count=6, align=True, per_slide=3):
        """The ``count`` lowest conformers (aligned onto the best), each as a 3D view."""
        o = self.order()[:count]
        ref = self.coords[o[0]]
        rel = self.relative()
        w = self.weights()
        scenes = []
        for k, i in enumerate(o):
            x = _kabsch(self.coords[i], ref) if align and k > 0 else self.coords[i]
            cap = f"#{i + 1}"
            if rel is not None:
                cap += f": ΔE {rel[i]:.2f} kcal/mol"
            if w is not None:
                cap += f", {100 * w[i]:.1f}%"
            scenes.append(structure_scene(self.atoms, x, caption=cap, id=f"conformer_{i + 1}"))
        return ReadoutGallery(*scenes, id="gallery", per_slide=per_slide, shared_view=True)

    @readout_section("coordinates", title="Coordinates", default=False)
    def readout_coordinates(self, ctx):
        """Every conformer's coordinates (exported; not displayed)."""
        c, unit = ctx.convert(self.coords, "length", "Angstroms")
        return ReadoutArray(ArrayData("coordinates", c, axes=("conformer", "atom", "xyz"), unit=unit,
                                      quantity="length"), display=False)


class CRESTReadout(ConformerEnsembleReadout):
    """
    **LLM Docstring**

    Readout for a CREST run directory (via `CRESTParser`): the final ensemble from
    ``crest_conformers.xyz`` with the populations and run information from ``confgen.log``,
    plus the command line and run settings.
    """
    readout_id = "crest"

    def __init__(self, parser, **opts):
        self.parser = parser
        conf = parser.parse_conformers()
        try:
            log = parser.parse_log()
        except Exception:
            log = {}
        self.log = log or {}
        info = self.log.get("FinalEnsembleInfo")
        weights = None
        if info is not None and len(np.atleast_1d(info.weights)) == len(conf.energies):
            weights = np.asarray(info.weights, dtype=float)
        super().__init__(conf.atoms, conf.coords, conf.energies, weights, name="CREST conformer ensemble",
                         source=getattr(parser, "dir", None) or getattr(parser, "path", None), **opts)

    @classmethod
    def from_directory(cls, directory, **opts):
        from ..Parsers import CRESTParser
        return cls(CRESTParser(directory), **opts)

    def _has_log(self):
        return bool(self.log), "no confgen.log"

    @readout_section("run", title="CREST run", available="_has_log")
    def readout_run(self, ctx):
        """Command line, calculation settings and the final-ensemble report."""
        nodes = []
        if self.log.get("CommandLine"):
            nodes.append(ReadoutCode(self.log["CommandLine"].strip(), title="Command line", id="command"))
        if self.log.get("CalculationInfo"):
            nodes.append(ReadoutCode(self.log["CalculationInfo"].strip(), title="Settings", id="settings",
                                     max_lines=40))
        info = self.log.get("FinalEnsembleInfo")
        if info is not None and getattr(info, "report", None):
            nodes.append(ReadoutCode(str(info.report).strip(), title="Ensemble report", id="report", max_lines=30))
        return nodes


class ConformerRecordReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for a `ConformerRecord` (SMILES, atoms, coordinates, bonds, energy and the evaluator
    and optimization settings that produced it). Coordinates are taken as ``units`` (Bohr for records
    generated through Psience molecules).
    """
    readout_id = "conformer"

    def __init__(self, record, units="BohrRadius"):
        super().__init__(record)
        self.units = units

    def get_readout_title(self):
        return self.obj.smiles or "Conformer"

    @readout_section("summary", title="Conformer")
    def readout_summary(self, ctx):
        """SMILES, size, energy and provenance."""
        r = self.obj
        f = [Field("smiles", r.smiles, label="SMILES", quantity="identifier"),
             Field("atoms", len(r.atoms), label="Atoms", quantity="int")]
        if r.energy is not None:
            f.append(ctx.field("energy", float(r.energy), quantity="energy", unit="Hartrees", label="Energy"))
        if r.energy_evaluator is not None:
            f.append(Field("energy_evaluator", str(r.energy_evaluator), label="Energy evaluator"))
        if r.optimization_settings:
            for k, v in dict(r.optimization_settings).items():
                f.append(Field(f"opt_{k}", str(v), label=f"opt: {k}"))
        return ReadoutFields(FieldSet(f, name="summary"))

    @readout_section("structure", title="Structure")
    def readout_structure(self, ctx):
        """3D view and coordinates."""
        r = self.obj
        return [structure_scene(r.atoms, r.coords, units=self.units, bonds=r.bonds, id="view"),
                atoms_table(ctx, r.atoms, r.coords, units=self.units, name="coordinates")]


class ConformerLibraryReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Bounded readout for a `ConformerLibrary`: size, backend and the first ``max_entries`` entries
    (SMILES, conformer counts, energy ranges) plus a structure for the first entry. Nothing beyond the
    entries shown is loaded.
    """
    readout_id = "conformer_library"

    def __init__(self, library, units="Angstroms"):
        super().__init__(library)
        self.units = units

    def get_readout_title(self):
        return "Conformer library"

    def _entries(self, n):
        lib = self.obj
        keys = []
        for i, k in enumerate(lib.keys()):
            if i >= n:
                break
            keys.append(k)
        return keys

    @readout_section("summary", title="Library")
    def readout_summary(self, ctx):
        """Size and backend."""
        lib = self.obj
        backend = getattr(lib, "backend", None)
        f = [Field("entries", len(lib), label="Entries", quantity="int"),
             Field("backend", type(backend).__name__ if backend is not None else type(lib).__name__, label="Backend")]
        return ReadoutFields(FieldSet(f, name="summary"))

    @readout_section("entries", title="Entries")
    def readout_entries(self, ctx, max_entries=20):
        """The first ``max_entries`` entries."""
        lib = self.obj
        keys = self._entries(max_entries)
        rows = []
        for k in keys:
            e = lib[k]
            smi = e.get("smi") if isinstance(e, dict) else None
            coords = np.asarray(e.get("coord")) if isinstance(e, dict) and e.get("coord") is not None else None
            en = np.asarray(e.get("energy"), dtype=float) if isinstance(e, dict) and e.get("energy") is not None else None
            rows.append((str(k), smi or "", 0 if coords is None else (len(coords) if coords.ndim == 3 else 1),
                         np.nan if en is None or not en.size else float(en.min()),
                         np.nan if en is None or not en.size else float((en.max() - en.min()) * KCAL_PER_HARTREE)))
        cols = [Column("key", np.array([r[0] for r in rows]), label="Key"),
                Column("smiles", np.array([r[1] for r in rows]), label="SMILES"),
                Column("conformers", np.array([r[2] for r in rows]), label="Conformers"),
                Column("lowest_energy", np.array([r[3] for r in rows]), label="Lowest E (Eₕ)", fmt="{:.6f}"),
                Column("window", np.array([r[4] for r in rows]), label="Window (kcal/mol)", fmt="{:.2f}")]
        nodes = [ReadoutTable(TabularData(cols, name="entries"))]
        if len(lib) > len(keys):
            nodes.append(ReadoutText(f"{len(lib) - len(keys)} more entries not loaded", role="note"))
        return nodes
