"""
Readouts for parsed electronic-structure results: Gaussian logs and formatted checkpoints,
Q-Chem output, and a generic view for the other `ElectronicStructureLogReader` formats.

The adapters wrap the *parsed records* (dictionaries returned by the readers), not the readers,
so a readout can be built from data that was parsed earlier or loaded from an archive. Reader
classes expose ``to_readout()``, which parses a sensible key set and hands the result over.
Only sections whose data was actually parsed are built.
"""

import os

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutSection, ReadoutFields, ReadoutTable,
    ReadoutText, ReadoutGallery, ReadoutArray, ReadoutCode, FieldSet, Field, TabularData, Column, ArrayData,
    structure_scene, trajectory_scene, atoms_table, line_chart, stick_chart, matrix_chart, record_nodes,
)

__all__ = [
    "GaussianLogReadout",
    "GaussianFChkReadout",
    "QChemLogReadout",
    "ElectronicStructureLogReadout",
    "parse_log",
]


def _symbols(numbers):
    from ...Data import AtomData
    return [AtomData[int(z), "Symbol"] for z in numbers]


def _reader_path(reader):
    stream = getattr(reader, "stream", None)
    return getattr(stream, "_file", None)


def parse_log(reader_cls, file, keys, skip_failures=True):
    """
    Parse ``keys`` in one pass; if that fails, retry each key with a fresh reader (readers stream
    forward, so one malformed block shouldn't lose the rest). Missing/empty results are dropped.
    """
    out, failures = {}, {}
    keys = list(keys)
    try:
        with reader_cls(file) as r:
            res = r.parse(keys)
        items = list(res.items())
    except Exception:
        if not skip_failures:
            raise
        items = []
        for k in keys:
            try:
                with reader_cls(file) as r:
                    items.extend(r.parse([k]).items())
            except Exception as e:
                failures[k] = f"{type(e).__name__}: {e}"
    for k, v in items:
        if v is None or (isinstance(v, (list, tuple, dict)) and len(v) == 0) or k in out:
            continue
        out[k] = v
    return out, failures


def _last(v):
    return v[-1] if isinstance(v, (list, tuple)) and len(v) > 0 else v


def _rel(values):
    values = np.asarray(values, dtype=float)
    return values - np.nanmin(values)


class _ParsedLogReadout(ReadoutAdapter):
    """Shared plumbing: ``self.obj`` is the parsed-record dict, ``self.source`` the file."""
    default_keys = ()
    reader = None

    def __init__(self, data, source=None, failures=None):
        super().__init__(dict(data))
        self.source = source
        self.failures = dict(failures or {})

    @classmethod
    def from_file(cls, file, keys=None):
        reader = cls.get_reader()
        keys = cls.select_keys(reader, file, keys)
        data, failures = parse_log(reader, file, keys)
        return cls(data, source=file, failures=failures)

    @classmethod
    def from_reader(cls, reader, keys=None):
        return cls.from_file(_reader_path(reader), keys=keys)

    @classmethod
    def get_reader(cls):
        raise NotImplementedError

    @classmethod
    def select_keys(cls, reader, file, keys):
        return list(keys) if keys is not None else list(cls.default_keys)

    def has(self, *keys):
        return any(k in self.obj for k in keys)

    def get_readout_subtitle(self):
        return os.path.basename(self.source) if self.source else None

    def get_readout_meta(self):
        meta = {"source": str(self.source) if self.source else None, "parsed_keys": sorted(self.obj)}
        if self.failures:
            meta["parse_failures"] = self.failures
        return meta

    @readout_section("raw", title="Other parsed data", default=False)
    def readout_raw(self, ctx, keys=None, max_depth=2):
        """Generic views of parsed records not covered by the sections above (or of ``keys``)."""
        keys = keys or [k for k in self.obj if k not in self.covered_keys]
        nodes = []
        for k in keys:
            if k in self.obj:
                nodes.append(ReadoutSection(*record_nodes(self.obj[k], k, max_depth=max_depth), id=k, title=k))
        if not nodes:
            raise ReadoutSectionUnavailable("no other parsed data")
        return nodes

    covered_keys = ()


class GaussianLogReadout(_ParsedLogReadout):
    """
    **LLM Docstring**

    Readout for a parsed Gaussian log: job summary, final structure, energies, optimization
    convergence and trajectory, scans, vibrations (table, IR sticks, mode animations), charges,
    dipoles, thermochemistry and AIMD trajectories. Geometries are in Å, AIMD coordinates in Bohr,
    energies in Hartree, frequencies in cm⁻¹ (as printed by Gaussian).
    """
    readout_id = "gaussian_log"
    default_keys = (
        "Header", "JobStatus", "ArchiveSummary", "Timing", "Geometries", "StandardCartesianCoordinates",
        "SCFEnergies", "ElectronicEnergies", "OptimizationConvergence", "ScanEnergies", "OptimizedScanEnergies",
        "VibrationalModes", "MullikenCharges", "DipoleMoments", "Thermochemistry", "RotationalConstants",
        "AIMDTrajectory", "ExcitedStates", "InputGeometry", "MoleculeInfo",
    )
    covered_keys = default_keys

    @classmethod
    def get_reader(cls):
        from ..Parsers import GaussianLogReader
        return GaussianLogReader

    @classmethod
    def select_keys(cls, reader, file, keys):
        if keys is not None:
            return list(keys)
        with reader(file) as r:
            avail = set(r.available_fields(True))
        return [k for k in cls.default_keys if k in avail or k in ("AIMDTrajectory", "ScanEnergies",
                                                                     "OptimizedScanEnergies")]

    # ---- helpers ------------------------------------------------------------------------- #
    def final_structure(self):
        """``(atoms, coords Å, label)`` of the last geometry printed, or None."""
        geoms = self.obj.get("Geometries")
        if geoms:
            pref = [g for g in geoms if g.get("orientation") == "Standard"] or geoms
            g = pref[-1]
            return _symbols(g["atomic_numbers"]), np.asarray(g["coordinates"]), f"{g.get('orientation', '')} orientation"
        sc = self.obj.get("StandardCartesianCoordinates")
        if sc is not None and len(sc) == 2 and len(sc[1]):
            info, coords = sc
            return _symbols(np.asarray(info[-1])[:, 1]), np.asarray(coords[-1]), "Standard orientation"
        ig = self.obj.get("InputGeometry")
        if ig:
            g = _last(ig)
            ats = g.get("atoms") or []
            if ats and all("coordinates" in a for a in ats):
                return ([a["atom"] for a in ats], np.array([a["coordinates"] for a in ats], dtype=float),
                        "Input geometry")
        return None

    def geometry_frames(self):
        sc = self.obj.get("StandardCartesianCoordinates")
        if sc is not None and len(sc) == 2 and len(sc[1]) > 1:
            info, coords = sc
            return _symbols(np.asarray(info[0])[:, 1]), np.asarray(coords)
        return None

    def get_readout_title(self):
        arch = self.obj.get("ArchiveSummary")
        if arch:
            a = _last(arch)
            return f"{a.get('formula', '')} {a.get('job', '')} — {a.get('level_of_theory', '')}/{a.get('basis', '')}".strip()
        return "Gaussian calculation"

    # ---- sections ------------------------------------------------------------------------ #
    @readout_section("summary", title="Calculation")
    def readout_summary(self, ctx):
        """Route, link-0 settings, job status, method/basis, final energies and timings."""
        f = []
        if self.source:
            f.append(ctx.field("file", os.path.abspath(self.source), label="File", quantity="path"))
        arch = self.obj.get("ArchiveSummary")
        if arch:
            a = _last(arch)
            for k, lab in (("job", "Job"), ("level_of_theory", "Method"), ("basis", "Basis"),
                           ("formula", "Formula"), ("date", "Date")):
                if a.get(k):
                    f.append(ctx.field(k, a[k], label=lab))
            routes = [x.get("route") for x in arch if x.get("route")]
            if routes:
                f.append(ctx.field("route", " | ".join(routes), label="Route"))
            props = a.get("properties", {})
            for k in ("State", "PG", "Version"):
                if k in props:
                    f.append(ctx.field(k.lower(), str(props[k]), label={"PG": "Point group"}.get(k, k)))
            for k in ("HF", "MP2", "MP3", "MP4", "CCSD", "CCSD(T)", "ZeroPoint"):
                if k in props:
                    v = np.asarray(props[k], dtype=float).reshape(-1)
                    lab = f"{k} energy" + (f" (last of {len(v)})" if len(v) > 1 else "")
                    f.append(ctx.field(k.lower().replace("(", "_").replace(")", ""), float(v[-1]),
                                       quantity="energy", unit="Hartrees", label=lab))
        hd = self.obj.get("Header")
        if hd is not None:
            cfg = getattr(hd, "config", {}) or {}
            for k, v in cfg.items():
                f.append(ctx.field("link0_" + k.lower(), str(v), label=f"%{k}"))
            if not arch:
                f.append(ctx.field("route", " ".join(f"{k}" + (f"({','.join(v)})" if v else "")
                                                   for k, v in (getattr(hd, "job", {}) or {}).items()),
                                   label="Route"))
        mi = self.obj.get("MoleculeInfo")
        if mi:
            for d in mi:
                if "charge" in d:
                    f.append(ctx.field("charge", int(d["charge"]), label="Charge", quantity="int"))
                    f.append(ctx.field("multiplicity", int(d.get("multiplicity", 1)), label="Multiplicity",
                                       quantity="int"))
                    break
        st = self.obj.get("JobStatus")
        if st:
            f.append(ctx.field("status", st.get("status"), label="Status"))
            if st.get("warnings"):
                f.append(ctx.field("warnings", len(st["warnings"]), label="Warnings", quantity="int"))
        tm = self.obj.get("Timing")
        if tm:
            f.append(ctx.field("cpu_time", float(sum(t.get("seconds", 0) for t in tm)), label="CPU time (s)"))
        nodes = [ReadoutFields(FieldSet(f, name="summary"))]
        if st and st.get("warnings"):
            nodes.append(ReadoutCode("\n".join(st["warnings"]), title="Warnings", id="warnings"))
        return nodes

    def _has_structure(self):
        return self.final_structure() is not None, "no geometry was parsed"

    @readout_section("structure", title="Final structure", available="_has_structure")
    def readout_structure(self, ctx):
        """The last printed geometry (3D view and coordinates)."""
        atoms, coords, label = self.final_structure()
        return [structure_scene(atoms, coords, caption=label, id="view"),
                atoms_table(ctx, atoms, coords, units="Angstroms", name="coordinates")]

    def _has_energies(self):
        e = self.obj.get("SCFEnergies")
        return e is not None and len(np.atleast_1d(e)) > 1, "fewer than two SCF energies"

    @readout_section("energies", title="SCF energies", available="_has_energies")
    def readout_energies(self, ctx):
        """SCF energy at every SCF solution in the log (optimization steps, scan points, ...)."""
        e, unit = ctx.convert(np.asarray(self.obj["SCFEnergies"], dtype=float), "energy", "Hartrees")
        step = np.arange(1, len(e) + 1)
        return [line_chart(step, e, "SCF step", "Energy", y_unit=unit, markers=len(e) < 60, x_name="step",
                           y_quantity="energy", id="plot",
                           caption=f"{len(e)} SCF energies; final {e[-1]:.8f}")]

    def _has_opt(self):
        return self.has("OptimizationConvergence"), "not an optimization"

    @readout_section("optimization", title="Optimization", available="_has_opt")
    def readout_optimization(self, ctx, animate=True):
        """Final convergence criteria, number of steps and (optionally) the geometry trajectory."""
        conv = self.obj["OptimizationConvergence"]
        last = _last(conv)
        crit = [k for k in last]
        cols = [Column("criterion", np.array(crit), label="Criterion"),
                Column("value", np.array([float(last[k]["value"]) for k in crit]), label="Value", fmt="{:.3e}"),
                Column("threshold", np.array([float(last[k]["threshold"]) for k in crit]), label="Threshold", fmt="{:.3e}"),
                Column("converged", np.array(["yes" if last[k]["converged"] else "no" for k in crit]), label="Converged")]
        nodes = [ReadoutFields(FieldSet([Field("steps", len(conv), label="Optimization steps", quantity="int")],
                                        name="steps")),
                 ReadoutTable(TabularData(cols, name="convergence"), title="Final step")]
        hist = []
        for k in crit:
            vals = [float(c[k]["value"]) for c in conv if k in c]
            if len(vals) == len(conv):
                hist.append((k, np.asarray(vals)))
        if len(conv) > 1 and hist:
            step = np.arange(1, len(conv) + 1)
            nodes.append(line_chart(step, [np.log10(np.abs(v) + 1e-16) for _, v in hist], "Optimization step",
                                    "log10 |value|", names=[k for k, _ in hist], markers=True, x_name="step",
                                    id="convergence_plot", caption="Convergence criteria per step"))
        frames = self.geometry_frames()
        if animate and frames is not None:
            atoms, coords = frames
            nodes.append(trajectory_scene(atoms, coords, caption=f"{len(coords)} geometries", id="trajectory"))
        return nodes

    def _has_scan(self):
        return self.has("ScanEnergies", "OptimizedScanEnergies"), "not a scan"

    @readout_section("scan", title="Scan", available="_has_scan")
    def readout_scan(self, ctx):
        """Scan energies: rigid scans (``ScanEnergies``) and relaxed scans (``OptimizedScanEnergies``)."""
        nodes = []
        se = self.obj.get("ScanEnergies")
        if se is not None:
            names = [str(c) for c in np.asarray(se.coords)]
            vals = np.asarray(se.energies, dtype=float)
            ecols = [i for i in range(2, vals.shape[1])]
            coord = vals[:, 1]
            es = [ctx.convert(vals[:, i] - np.nanmin(vals[:, i]), "energy", "Hartrees")[0] for i in ecols]
            unit = ctx.convert(1.0, "energy", "Hartrees")[1]
            nodes.append(line_chart(coord, es, f"{names[1]}", "Relative energy", y_unit=unit,
                                    names=[names[i] for i in ecols], x_name=names[1], id="plot",
                                    caption=f"{len(coord)} scan points (relative to each minimum)"))
            cols = [Column("step", vals[:, 0].astype(int), label="Step", quantity="index"),
                    Column(names[1].lower(), coord, label=names[1])]
            cols += [ctx.column(names[i].lower(), vals[:, i], quantity="energy", unit="Hartrees", label=names[i])
                     for i in ecols]
            nodes.append(ReadoutTable(TabularData(cols, name="points"), title="Scan points"))
        ose = self.obj.get("OptimizedScanEnergies")
        if ose is not None:
            e = np.asarray(ose.energies, dtype=float)
            coords = {k: np.asarray(v) for k, v in dict(ose.coords).items()}
            varying = [k for k, v in coords.items() if np.ptp(v) > 1e-6] or list(coords)[:1]
            x = coords[varying[0]] if varying else np.arange(len(e))
            rel, unit = ctx.convert(e - np.nanmin(e), "energy", "Hartrees")
            nodes.append(line_chart(x, rel, varying[0] if varying else "point", "Relative energy", y_unit=unit,
                                    markers=True, x_name="coordinate", id="relaxed_plot",
                                    caption=f"Relaxed scan along {', '.join(varying)}"))
            cols = [Column("point", np.arange(1, len(e) + 1), label="#", quantity="index")]
            cols += [Column(k, coords[k], label=k) for k in varying]
            cols.append(ctx.column("energy", e, quantity="energy", unit="Hartrees", label="Energy"))
            nodes.append(ReadoutTable(TabularData(cols, name="relaxed_points"), title="Optimized scan points"))
        return nodes

    def _has_vib(self):
        return self.has("VibrationalModes"), "no frequencies"

    @readout_section("vibrations", title="Vibrations", available="_has_vib")
    def readout_vibrations(self, ctx, animate=True, max_modes=6, amplitude=.35, frames=12, duration=2.0):
        """Harmonic frequencies, IR intensities and (optionally) animations of the first modes."""
        vm = _last(self.obj["VibrationalModes"])
        freqs = np.asarray(vm["frequencies"], dtype=float)
        n = len(freqs)
        cols = [Column("mode", np.arange(1, n + 1), label="Mode", quantity="index")]
        if vm.get("symmetries"):
            cols.append(Column("symmetry", np.array([str(s) for s in vm["symmetries"]]), label="Sym."))
        cols.append(ctx.column("frequency", freqs, quantity="frequency", unit="Wavenumbers", label="Frequency"))
        for k, lab, unit in (("reduced_masses", "Red. mass", "AtomicMassUnits"),
                             ("force_constants", "Force const. (mDyne/Å)", None),
                             ("ir_intensities", "IR intensity", "KilometersPerMole")):
            if vm.get(k) is not None:
                q = "mass" if unit == "AtomicMassUnits" else ("intensity" if unit else None)
                cols.append(ctx.column(k, np.asarray(vm[k], dtype=float), quantity=q, unit=unit, label=lab))
        nodes = [ReadoutTable(TabularData(cols, name="modes"))]
        fdisp, funit = ctx.convert(freqs, "frequency", "Wavenumbers")
        if vm.get("ir_intensities") is not None:
            nodes.append(stick_chart(fdisp, np.asarray(vm["ir_intensities"], dtype=float), "Frequency", "IR intensity",
                                     x_unit=funit, y_unit="KilometersPerMole", x_name="frequency",
                                     y_name="intensity", id="ir_spectrum", caption="Harmonic IR stick spectrum"))
        st = self.final_structure()
        disp = vm.get("displacements")
        if animate and st is not None and disp is not None:
            atoms, eq, _ = st
            disp = np.asarray(disp, dtype=float)
            if disp.shape[1] == len(atoms):
                phases = np.sin(np.linspace(0, 2 * np.pi, frames, endpoint=False))
                scenes = []
                for i in range(min(n, max_modes)):
                    d = disp[i] / max(np.max(np.linalg.norm(disp[i], axis=1)), 1e-12)
                    traj = eq[None] + amplitude * phases[:, None, None] * d[None]
                    cap = ctx.field("frequency", float(freqs[i]), quantity="frequency", unit="Wavenumbers",
                                    label=f"Mode {i + 1}")
                    sc = trajectory_scene(atoms, traj, caption=cap, id=f"mode_{i + 1}", duration=duration)
                    scenes.append(sc)
                nodes.append(ReadoutGallery(*scenes, id="animations", title="Mode animations", shared_view=True,
                                            per_slide=3))
        return nodes

    def _has_charges(self):
        return self.has("MullikenCharges"), "no Mulliken charges"

    @readout_section("charges", title="Mulliken charges", available="_has_charges")
    def readout_charges(self, ctx):
        """The last Mulliken population analysis."""
        mc = _last(self.obj["MullikenCharges"])
        cols = [Column("center", np.asarray(mc["centers"]), label="#", quantity="index"),
                Column("atom", np.array([str(s) for s in mc["symbols"]]), label="Atom"),
                Column("charge", np.asarray(mc["charges"], dtype=float), label="Charge (e)", fmt="{:.4f}")]
        return [ReadoutTable(TabularData(cols, name="charges"))]

    def _has_dipole(self):
        return self.has("DipoleMoments"), "no dipole moments"

    @readout_section("dipole", title="Dipole moment", available="_has_dipole")
    def readout_dipole(self, ctx):
        """The last printed dipole moment (Debye, Gaussian's standard orientation)."""
        d = np.asarray(self.obj["DipoleMoments"], dtype=float).reshape(-1, 3)
        last = d[-1]
        f = [Field(k, float(v), label=f"μ{k}", unit="Debye", quantity="dipole") for k, v in zip("xyz", last)]
        f.append(Field("total", float(np.linalg.norm(last)), label="|μ|", unit="Debye", quantity="dipole"))
        nodes = [ReadoutFields(FieldSet(f, name="dipole"))]
        if len(d) > 1:
            nodes.append(line_chart(np.arange(1, len(d) + 1), np.linalg.norm(d, axis=1), "Step", "|μ|",
                                    y_unit="Debye", x_name="step", id="history", caption="Dipole magnitude per step"))
        return nodes

    def _has_thermo(self):
        return self.has("Thermochemistry"), "no thermochemistry"

    @readout_section("thermochemistry", title="Thermochemistry", available="_has_thermo")
    def readout_thermochemistry(self, ctx):
        """Thermal corrections and energies (Hartree)."""
        th = _last(self.obj["Thermochemistry"])
        f = []
        for group in ("corrections", "energies"):
            for k, v in (th.get(group) or {}).items():
                try:
                    v = float(v)
                except (TypeError, ValueError):
                    continue
                f.append(ctx.field(f"{group}_{k}"[:60].replace(" ", "_").lower(), v, quantity="energy",
                                   unit="Hartrees", label=k))
        if not f:
            raise ReadoutSectionUnavailable("no numeric thermochemistry values")
        return ReadoutFields(FieldSet(f, name="thermochemistry"))

    def _has_aimd(self):
        return self.has("AIMDTrajectory"), "not a dynamics run"

    @readout_section("aimd", title="AIMD trajectory", available="_has_aimd")
    def readout_aimd(self, ctx, animate=True, max_frames=60):
        """Energies along the trajectory and an animation of the geometries (Bohr in the log)."""
        traj = self.obj["AIMDTrajectory"]
        coords = np.asarray(traj.coords, dtype=float)
        e = np.asarray(traj.vals.energies, dtype=float)
        rel, unit = ctx.convert(e - e[0], "energy", "Hartrees")
        nodes = [ReadoutFields(FieldSet([Field("frames", len(coords), label="Frames", quantity="int"),
                                         ctx.field("e0", float(e[0]), quantity="energy", unit="Hartrees",
                                                   label="Initial energy")], name="summary")),
                 line_chart(np.arange(len(e)), rel, "Step", "Energy − E₀", y_unit=unit, x_name="step", id="energy",
                            caption="Potential energy along the trajectory")]
        st = self.final_structure()
        if animate:
            nat = coords.shape[1]
            atoms = st[0] if st is not None and len(st[0]) == nat else None
            if atoms is None and self.has("Header"):
                atoms = None
            if atoms is not None:
                nodes.append(trajectory_scene(atoms, coords, units="BohrRadius", max_frames=max_frames,
                                              caption=f"{len(coords)} frames", id="animation"))
        return nodes


class GaussianFChkReadout(_ParsedLogReadout):
    """
    **LLM Docstring**

    Readout for a Gaussian formatted checkpoint: method/energy summary, structure (Bohr in the
    file), Mulliken charges, dipole, the Cartesian Hessian (heatmap; full matrix exported) and
    vibrational data when present.
    """
    readout_id = "gaussian_fchk"
    default_keys = ("AtomicNumbers", "Coordinates", "Total Energy", "SCF Energy", "Charge",
                    "Multiplicity", "AtomicMasses", "Mulliken Charges", "DipoleMoment", "ForceConstants",
                    "VibrationalData", "Gradient")
    covered_keys = default_keys

    @classmethod
    def get_reader(cls):
        from ..Parsers import GaussianFChkReader
        return GaussianFChkReader

    def atoms(self):
        z = self.obj.get("AtomicNumbers")
        return None if z is None else _symbols(np.asarray(z))

    def header(self):
        """``{'title', 'job', 'method', 'basis'}`` from the two fchk header lines."""
        hd = self.obj.get("Header")
        if not isinstance(hd, str):
            return {}
        lines = [l for l in hd.splitlines() if l.strip()]
        out = {"title": lines[0].strip()} if lines else {}
        if len(lines) > 1:
            parts = lines[1].split()
            out.update(dict(zip(("job", "method", "basis"), parts)))
        return out

    def get_readout_title(self):
        h = self.header()
        if h.get("title"):
            extra = "/".join(h[k] for k in ("method", "basis") if k in h)
            return h["title"] + (f" — {extra}" if extra else "")
        return "Gaussian checkpoint"

    @readout_section("summary", title="Calculation")
    def readout_summary(self, ctx):
        """Header, charge/multiplicity and energies."""
        f = []
        if self.source:
            f.append(ctx.field("file", os.path.abspath(self.source), label="File", quantity="path"))
        for k, v in self.header().items():
            f.append(ctx.field(k, v, label=k.capitalize()))
        atoms = self.atoms()
        if atoms:
            counts = {}
            for a in atoms:
                counts[a] = counts.get(a, 0) + 1
            f.append(ctx.field("formula", "".join(f"{k}{v if v > 1 else ''}" for k, v in counts.items()),
                               label="Composition"))
        for k, lab in (("Charge", "Charge"), ("Multiplicity", "Multiplicity")):
            if k in self.obj:
                f.append(ctx.field(k.lower(), int(self.obj[k]), label=lab, quantity="int"))
        for k in ("Total Energy", "SCF Energy"):
            if k in self.obj:
                f.append(ctx.field(k.lower().replace(" ", "_"), float(self.obj[k]), quantity="energy",
                                   unit="Hartrees", label=k))
        if "Gradient" in self.obj:
            g = np.asarray(self.obj["Gradient"], dtype=float)
            f.append(ctx.field("max_gradient", float(np.max(np.abs(g))), label="Max |gradient| (Eₕ/a₀)"))
        return ReadoutFields(FieldSet(f, name="summary"))

    def _has_structure(self):
        return self.has("Coordinates") and self.atoms() is not None, "no coordinates"

    @readout_section("structure", title="Structure", available="_has_structure")
    def readout_structure(self, ctx):
        """Current Cartesian coordinates (Bohr in the file)."""
        atoms = self.atoms()
        xyz = np.asarray(self.obj["Coordinates"], dtype=float).reshape(-1, 3)
        extra = {}
        if "AtomicMasses" in self.obj:
            extra["mass"] = ctx.column("mass", np.asarray(self.obj["AtomicMasses"], dtype=float), quantity="mass",
                                       unit="AtomicMassUnits", label="Mass")
        if "Mulliken Charges" in self.obj:
            extra["mulliken"] = Column("mulliken", np.asarray(self.obj["Mulliken Charges"], dtype=float),
                                       label="Mulliken (e)", fmt="{:.4f}")
        return [structure_scene(atoms, xyz, units="BohrRadius", id="view"),
                atoms_table(ctx, atoms, xyz, units="BohrRadius", name="coordinates", **extra)]

    def _has_dipole(self):
        return self.has("DipoleMoment"), "no dipole"

    @readout_section("dipole", title="Dipole moment", available="_has_dipole")
    def readout_dipole(self, ctx):
        """Dipole moment (atomic units, as stored in the checkpoint)."""
        d = np.asarray(self.obj["DipoleMoment"], dtype=float)
        f = [Field(k, float(v), label=f"μ{k}", unit="a.u.", quantity="dipole") for k, v in zip("xyz", d)]
        f.append(Field("total", float(np.linalg.norm(d)), label="|μ|", unit="a.u.", quantity="dipole"))
        return ReadoutFields(FieldSet(f, name="dipole"))

    def _has_hessian(self):
        return self.has("ForceConstants"), "no force constants"

    @readout_section("hessian", title="Cartesian Hessian", available="_has_hessian")
    def readout_hessian(self, ctx):
        """The Cartesian force-constant matrix (Eₕ/a₀²); shown as a heatmap, exported in full."""
        fc = self.obj["ForceConstants"]
        h = np.asarray(fc.array if hasattr(fc, "array") else fc, dtype=float)
        evals = np.linalg.eigvalsh(h)
        return [matrix_chart(h, caption=f"{h.shape[0]}×{h.shape[1]}; eigenvalues {evals.min():.3g} … {evals.max():.3g}",
                             label="Force constant", unit="Eₕ/a₀²", id="matrix", name="hessian")]

    def _has_vib(self):
        return self.has("VibrationalData"), "no vibrational data"

    @readout_section("vibrations", title="Vibrations", available="_has_vib")
    def readout_vibrations(self, ctx):
        """Frequencies, reduced masses, force constants and intensities stored in the checkpoint."""
        vd = self.obj["VibrationalData"]
        freqs = np.asarray(vd["Frequencies"], dtype=float)
        cols = [Column("mode", np.arange(1, len(freqs) + 1), label="Mode", quantity="index"),
                ctx.column("frequency", freqs, quantity="frequency", unit="Wavenumbers", label="Frequency")]
        for k, lab, unit, q in (("ReducedMasses", "Red. mass", "AtomicMassUnits", "mass"),
                                ("ForceConstants", "Force const. (mDyne/Å)", None, None),
                                ("Intensities", "IR intensity", "KilometersPerMole", "intensity")):
            if vd.get(k) is not None:
                cols.append(ctx.column(k.lower(), np.asarray(vd[k], dtype=float), quantity=q, unit=unit, label=lab))
        nodes = [ReadoutTable(TabularData(cols, name="modes"))]
        if vd.get("Intensities") is not None:
            f, fu = ctx.convert(freqs, "frequency", "Wavenumbers")
            nodes.append(stick_chart(f, np.asarray(vd["Intensities"], dtype=float), "Frequency", "IR intensity",
                                     x_unit=fu, y_unit="KilometersPerMole", id="ir_spectrum",
                                     x_name="frequency", y_name="intensity"))
        return nodes


class QChemLogReadout(_ParsedLogReadout):
    """
    **LLM Docstring**

    Readout for Q-Chem output: version/method/basis, final structure (Å), energies along the
    run, the last dipole, Mulliken charges and job times.
    """
    readout_id = "qchem_log"
    default_keys = ("Header", "CartesianCoordinates", "SCFEnergies", "OptimizationEnergies", "FinalEnergy",
                    "DipoleMoments", "MullikenCharges", "JobTimes", "VibrationalFrequencies", "InputSection")
    covered_keys = default_keys

    @classmethod
    def get_reader(cls):
        from ..Parsers import QChemLogReader
        return QChemLogReader

    def get_readout_title(self):
        hd = self.obj.get("Header")
        if hd is not None:
            return f"Q-Chem {getattr(hd, 'method', '')}/{getattr(hd, 'basis', '')}"
        return "Q-Chem calculation"

    @readout_section("summary", title="Calculation")
    def readout_summary(self, ctx):
        """Version, method, basis, final energy and job times."""
        f = []
        if self.source:
            f.append(ctx.field("file", os.path.abspath(self.source), label="File", quantity="path"))
        hd = self.obj.get("Header")
        if hd is not None:
            for k in ("version", "method", "basis"):
                if getattr(hd, k, None):
                    f.append(ctx.field(k, str(getattr(hd, k)), label=k.capitalize()))
        if "FinalEnergy" in self.obj:
            f.append(ctx.field("final_energy", float(self.obj["FinalEnergy"]), quantity="energy", unit="Hartrees",
                               label="Final energy"))
        if "JobTimes" in self.obj:
            jt = np.asarray(self.obj["JobTimes"], dtype=float).reshape(-1)
            f.append(ctx.field("job_times", ", ".join(f"{t:.1f}" for t in jt), label="Job times (s)"))
        nodes = [ReadoutFields(FieldSet(f, name="summary"))]
        if "InputSection" in self.obj:
            nodes.append(ReadoutCode(self.obj["InputSection"], title="Input", id="input", max_lines=60))
        return nodes

    def _has_structure(self):
        return self.has("CartesianCoordinates"), "no coordinates"

    @readout_section("structure", title="Final structure", available="_has_structure")
    def readout_structure(self, ctx, animate=True):
        """Last printed geometry, plus the optimization trajectory when there are several."""
        cc = self.obj["CartesianCoordinates"]
        atoms, coords = list(cc.atoms), np.asarray(cc.coords, dtype=float)
        nodes = [structure_scene(atoms, coords[-1], id="view"),
                 atoms_table(ctx, atoms, coords[-1], name="coordinates")]
        if animate and len(coords) > 1:
            nodes.append(trajectory_scene(atoms, coords, caption=f"{len(coords)} geometries", id="trajectory"))
        return nodes

    def _has_energies(self):
        return self.has("SCFEnergies", "OptimizationEnergies"), "no energies"

    @readout_section("energies", title="Energies", available="_has_energies")
    def readout_energies(self, ctx):
        """SCF energies and optimization energies per step."""
        nodes = []
        for k, lab in (("OptimizationEnergies", "Optimization step"), ("SCFEnergies", "SCF solution")):
            if k in self.obj:
                e, unit = ctx.convert(np.asarray(self.obj[k], dtype=float), "energy", "Hartrees")
                nodes.append(line_chart(np.arange(1, len(e) + 1), e, lab, "Energy", y_unit=unit, x_name="step",
                                        id=k.lower(), caption=f"{k}: {len(e)} values, final {e[-1]:.8f}"))
        return nodes

    def _has_dipole(self):
        return self.has("DipoleMoments"), "no dipoles"

    @readout_section("dipole", title="Dipole moment", available="_has_dipole")
    def readout_dipole(self, ctx):
        """The last dipole moment (Debye)."""
        d = _last(self.obj["DipoleMoments"])
        xyz = np.asarray(d.xyz, dtype=float)
        f = [Field(k, float(v), label=f"μ{k}", unit="Debye", quantity="dipole") for k, v in zip("xyz", xyz)]
        f.append(Field("total", float(d.total), label="|μ|", unit="Debye", quantity="dipole"))
        return ReadoutFields(FieldSet(f, name="dipole"))

    def _has_charges(self):
        return self.has("MullikenCharges"), "no charges"

    @readout_section("charges", title="Mulliken charges", available="_has_charges")
    def readout_charges(self, ctx):
        """The last Mulliken analysis."""
        m = _last(self.obj["MullikenCharges"])
        atoms = list(m.atoms)
        cols = [Column("index", np.arange(1, len(atoms) + 1), label="#", quantity="index"),
                Column("atom", np.array(atoms), label="Atom"),
                Column("charge", np.asarray(m.charges, dtype=float), label="Charge (e)", fmt="{:.4f}")]
        return ReadoutTable(TabularData(cols, name="charges"))


class ElectronicStructureLogReadout(_ParsedLogReadout):
    """
    **LLM Docstring**

    Generic readout for any `ElectronicStructureLogReader` (ORCA, MOLPRO, ...): parses every
    component the reader defines and shows each record with the generic record view. A structure
    is shown when a ``CartesianCoordinates`` record with atoms and coordinates is present.
    """
    readout_id = "electronic_structure_log"
    reader_class = None

    def __init__(self, data, source=None, failures=None, reader_class=None):
        super().__init__(data, source=source, failures=failures)
        self.reader_class = reader_class

    @classmethod
    def from_reader(cls, reader, keys=None):
        rc = type(reader)
        if keys is None:
            keys = list(rc.load_components().__components__.keys()) if hasattr(rc, "load_components") else []
        data, failures = parse_log(rc, _reader_path(reader), keys)
        return cls(data, source=_reader_path(reader), failures=failures, reader_class=rc)

    def get_readout_title(self):
        return (self.reader_class.__name__.replace("LogReader", "") if self.reader_class else "Calculation") + " output"

    def _structure(self):
        cc = self.obj.get("CartesianCoordinates")
        if cc is None:
            return None
        atoms = getattr(cc, "atoms", None)
        coords = getattr(cc, "coords", None)
        if atoms is None and isinstance(cc, tuple) and len(cc) == 2:
            atoms, coords = cc
        if atoms is None or coords is None:
            return None
        coords = np.asarray(coords, dtype=float)
        if coords.ndim == 3:
            coords = coords[-1]
        return list(atoms), coords

    def _has_structure(self):
        return self._structure() is not None, "no Cartesian coordinates"

    @readout_section("structure", title="Structure", available="_has_structure")
    def readout_structure(self, ctx):
        """Last Cartesian coordinates (assumed Å)."""
        atoms, coords = self._structure()
        return [structure_scene(atoms, coords, id="view"), atoms_table(ctx, atoms, coords, name="coordinates")]

    @readout_section("records", title="Parsed records")
    def readout_records(self, ctx, max_depth=2):
        """Every parsed component, with the generic record view."""
        nodes = [ReadoutSection(*record_nodes(v, k, max_depth=max_depth), id=k, title=k) for k, v in self.obj.items()]
        if not nodes:
            raise ReadoutSectionUnavailable("nothing was parsed")
        return nodes
