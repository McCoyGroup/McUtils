"""
Optimization results as readouts.

`OptimizationRun` normalizes the tuples returned by `iterative_step_minimize`, `scipy_minimize`,
`iterative_chain_minimize`/`string_method_minimize` and the `polyfit_*` helpers into one record:
final points, convergence flags, errors, iteration counts, the optional trajectory, and (when a
``function`` is supplied) function values along the way. Nothing is re-run; the function is only
evaluated on points already in the result.
"""

import dataclasses

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutFields, ReadoutTable, ReadoutArray,
    ReadoutText, ReadoutPlot, FieldSet, Field, Column, TabularData, ArrayData, line_chart,
)

__all__ = [
    "OptimizationRun",
    "OptimizationReadout",
]


@dataclasses.dataclass
class OptimizationRun:
    """
    A normalized optimization result.

    :param kind: ``'minimize'``, ``'scipy'``, ``'chain'`` or ``'critical_points'``
    :param points: final points ``(members, n)`` (chains: final images ``(images, n)``)
    :param converged: per-member flags
    :param errors: per-member final errors
    :param iterations: per-member iteration counts
    :param paths: per-member arrays ``(steps, n)`` (starting point first when known), or chain
        snapshots ``(iterations, images, n)``
    """
    kind: str
    points: np.ndarray
    converged: np.ndarray
    errors: np.ndarray = None
    iterations: np.ndarray = None
    paths: list = None
    function: object = None
    method: str = None
    message: str = None
    settings: dict = None
    values: np.ndarray = None

    # ---- constructors ---------------------------------------------------------------------- #
    @classmethod
    def from_step_result(cls, result, trajectory=None, guess=None, function=None, method=None, settings=None):
        """
        From ``iterative_step_minimize``: ``result = (points, converged, (errors, iterations))``,
        ``trajectory`` the list returned with ``return_trajectory=True``.
        """
        if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], tuple) and trajectory is None:
            result, trajectory = result
        pts, conv, (errs, its) = result
        if isinstance(pts, tuple):  # unitary runs return (points, rotations)
            pts = pts[0]
        pts = np.asarray(pts, dtype=float)
        squeeze = pts.ndim == 1
        pts = pts.reshape(-1, pts.shape[-1])
        nm = len(pts)
        errs = np.atleast_1d(np.asarray(errs, dtype=float)).reshape(-1)
        its = np.atleast_1d(np.asarray(its)).reshape(-1)
        conv = np.atleast_1d(np.asarray(conv, dtype=bool))
        if conv.size == 1 and nm > 1:
            conv = np.repeat(conv, nm) & (errs <= np.nanmax(errs))
        paths = None
        if trajectory is not None:
            start = None if guess is None else np.asarray(guess, dtype=float).reshape(-1, pts.shape[-1])
            paths = [[start[i]] if start is not None else [] for i in range(nm)]
            for idx, positions in trajectory:
                idx = np.atleast_1d(np.asarray(idx, dtype=int))
                positions = np.asarray(positions, dtype=float).reshape(len(idx), -1)
                for k, i in enumerate(idx):
                    paths[i].append(positions[k])
            paths = [np.asarray(p) for p in paths]
        return cls("minimize", pts, conv, errs, its, paths, function, method or "iterative_step_minimize",
                   settings=settings)

    @classmethod
    def from_scipy_result(cls, result, function=None, method=None, settings=None):
        """From ``scipy_minimize``: ``(success, x | (x, trajectory), OptimizeResult)``."""
        success, x, res = result
        path = None
        if isinstance(x, tuple):
            x, path = x
            path = np.asarray([np.asarray(p, dtype=float).reshape(-1) for p in path])
        x = np.asarray(x, dtype=float).reshape(1, -1)
        its = np.array([getattr(res, "nit", len(path) if path is not None else 0)])
        jac = getattr(res, "jac", None)
        err = np.array([np.max(np.abs(jac)) if jac is not None else np.nan])
        return cls("scipy", x, np.array([bool(success)]), err, its, [path] if path is not None else None, function,
                   method or f"scipy ({getattr(res, 'method', '') or 'minimize'})",
                   message=str(getattr(res, "message", "")), settings=settings)

    @classmethod
    def from_chain_result(cls, result, function=None, method=None, settings=None):
        """From ``iterative_chain_minimize`` / ``string_method_minimize``."""
        (images, numbers), conv, (errs, its) = result
        snaps = None
        if isinstance(images, tuple):
            images, snaps = images
        images = np.asarray(images, dtype=float)
        if images.ndim == 3:  # batched chains: report the first
            images = images[0]
        paths = [np.asarray(snaps, dtype=float)] if snaps else None
        return cls("chain", images, np.atleast_1d(np.asarray(conv, dtype=bool))[:1],
                   np.atleast_1d(np.asarray(errs, dtype=float)).reshape(-1)[:1],
                   np.atleast_1d(np.asarray(its)).reshape(-1)[:1], paths, function, method or "chain minimization",
                   settings=settings)

    @classmethod
    def from_critical_points(cls, result, x=None, y=None, kind="minima", settings=None):
        """From ``polyfit_minima`` / ``polyfit_maxima`` / ``polyfit_critical_points``."""
        roots, values = result[0], result[1]
        curv = result[2] if len(result) > 2 else None
        run = cls("critical_points", np.asarray(roots, dtype=float).reshape(-1, 1),
                  np.ones(len(np.atleast_1d(roots)), dtype=bool), method=f"polyfit ({kind})", settings=settings,
                  values=np.asarray(values, dtype=float))
        run.curvature = None if curv is None else np.asarray(curv, dtype=float)
        run.samples = None if x is None else (np.asarray(x, dtype=float), np.asarray(y, dtype=float))
        return run

    def evaluate(self, points):
        if self.function is None:
            return None
        pts = np.asarray(points, dtype=float)
        try:
            return np.asarray(self.function(pts), dtype=float)
        except TypeError:
            return np.asarray(self.function(pts, None), dtype=float)

    def to_readout(self, **opts):
        return OptimizationReadout(self).to_readout(**opts)


class OptimizationReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for an `OptimizationRun`: convergence summary, final points, convergence traces
    (function value, step size), 2D paths over the function's contours, chain energy profiles and
    fitted critical points. Values are in whatever units the optimized function uses.
    """
    readout_id = "optimization"

    @property
    def run(self):
        return self.obj

    def get_readout_title(self):
        return {"minimize": "Minimization", "scipy": "Minimization (SciPy)", "chain": "Chain-of-states optimization",
                "critical_points": "Fitted critical points"}.get(self.run.kind, "Optimization")

    def get_readout_subtitle(self):
        return self.run.method

    @readout_section("summary", title="Summary")
    def readout_summary(self, ctx):
        """Convergence, iteration counts and final errors / function values."""
        r = self.run
        f = [Field("method", r.method, label="Method")]
        if r.kind != "critical_points":
            f += [Field("members", len(r.points) if r.kind != "chain" else 1, label="Runs" if r.kind != "chain" else "Chains",
                        quantity="int"),
                  Field("dimension", int(r.points.shape[-1]), label="Dimension", quantity="int"),
                  Field("converged", f"{int(np.sum(r.converged))} of {len(r.converged)}", label="Converged")]
            if r.iterations is not None:
                f.append(Field("iterations", ", ".join(str(int(i)) for i in r.iterations[:10]), label="Iterations"))
            if r.errors is not None:
                f.append(Field("max_error", float(np.nanmax(r.errors)), label="Max final error", fmt="{:.3e}"))
            if r.function is not None and r.kind != "chain":
                fv = r.evaluate(r.points)
                f.append(Field("best_value", float(np.nanmin(fv)), label="Best function value", fmt="{:.8g}"))
        else:
            f.append(Field("count", len(r.points), label="Critical points", quantity="int"))
        if r.message:
            f.append(Field("message", r.message, label="Message"))
        for k, v in (r.settings or {}).items():
            f.append(Field(f"setting_{k}", str(v), label=k))
        return ReadoutFields(FieldSet(f, name="summary"))

    @readout_section("result", title="Final points")
    def readout_result(self, ctx, max_dims=8):
        """Final coordinates per run (chain: per image), with errors and function values."""
        r = self.run
        pts = r.points
        n = pts.shape[-1]
        label = "image" if r.kind == "chain" else ("root" if r.kind == "critical_points" else "run")
        cols = [Column(label, np.arange(1, len(pts) + 1), label=label.capitalize(), quantity="index")]
        cols += [Column(f"x{i}", pts[:, i], label=f"x{i}", fmt="{:.6g}") for i in range(min(n, max_dims))]
        if r.kind == "critical_points":
            cols.append(Column("value", np.asarray(r.values).reshape(-1), label="Value", fmt="{:.6g}"))
            if getattr(r, "curvature", None) is not None:
                cols.append(Column("curvature", np.asarray(r.curvature).reshape(-1), label="Curvature", fmt="{:.4g}"))
        else:
            fv = r.evaluate(pts)
            if fv is not None:
                cols.append(Column("value", fv, label="f", fmt="{:.8g}"))
            if r.kind != "chain":
                cols.append(Column("converged", np.array(["yes" if c else "no" for c in r.converged]), label="Converged"))
                if r.errors is not None:
                    cols.append(Column("error", r.errors, label="Error", fmt="{:.3e}"))
                if r.iterations is not None:
                    cols.append(Column("iterations", r.iterations.astype(int), label="Iterations"))
        nodes = [ReadoutTable(TabularData(cols, name="points"))]
        if n > max_dims:
            nodes.append(ReadoutArray(ArrayData("points", pts, axes=(label, "coordinate")), display=False))
        return nodes

    def _has_trace(self):
        return self.run.kind in ("minimize", "scipy") and self.run.paths is not None, "no trajectory recorded"

    @readout_section("convergence", title="Convergence", available="_has_trace")
    def readout_convergence(self, ctx):
        """Function value (if a function was given) and step length per iteration, for every run."""
        r = self.run
        nodes = []
        paths = [p for p in r.paths if p is not None and len(p) > 1]
        if not paths:
            raise ReadoutSectionUnavailable("trajectories are too short")
        L = max(len(p) for p in paths)
        steps = np.arange(L)
        if r.function is not None:
            vals = [np.pad(r.evaluate(p), (0, L - len(p)), constant_values=np.nan) for p in paths]
            nodes.append(line_chart(steps, vals, "Iteration", "f", names=[f"run {i + 1}" for i in range(len(vals))],
                                    markers=L < 60, x_name="iteration", id="values", caption="Function value per iteration"))
        sizes = [np.pad(np.log10(np.linalg.norm(np.diff(p, axis=0), axis=1) + 1e-16), (0, L - len(p)),
                        constant_values=np.nan) for p in paths]
        nodes.append(line_chart(steps[1:], [s[:L - 1] for s in sizes], "Iteration", "log10 |step|",
                                names=[f"run {i + 1}" for i in range(len(sizes))], markers=L < 60, x_name="iteration",
                                id="steps", caption="Step length per iteration"))
        for i, p in enumerate(paths):
            nodes.append(ReadoutArray(ArrayData(f"path_{i + 1}", p, axes=("iteration", "coordinate")), display=False))
        return nodes

    def _has_2d(self):
        r = self.run
        ok = r.function is not None and r.points.shape[-1] == 2 and (r.paths is not None or r.kind == "chain")
        return ok, "paths are drawn for 2D problems with a function"

    @readout_section("paths", title="Paths", available="_has_2d")
    def readout_paths(self, ctx, padding=.25, resolution=120, levels=25):
        """Optimization paths (or the chain) over contours of the function."""
        r = self.run
        if r.kind == "chain":
            lines = [r.points] + ([r.paths[0][0]] if r.paths else [])
            labels = ["final chain"] + (["initial chain"] if r.paths else [])
        else:
            lines = [p for p in r.paths if p is not None and len(p)]
            labels = [f"run {i + 1}" for i in range(len(lines))]
        allp = np.concatenate(lines)
        lo, hi = allp.min(0), allp.max(0)
        span = np.maximum(hi - lo, 1e-6)
        lo, hi = lo - padding * span, hi + padding * span
        X, Y = np.meshgrid(np.linspace(lo[0], hi[0], resolution), np.linspace(lo[1], hi[1], resolution))
        Z = r.evaluate(np.stack([X, Y], -1).reshape(-1, 2)).reshape(X.shape)

        def build():
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            fig = Figure(figsize=(5.2, 4.0), dpi=100)
            FigureCanvasAgg(fig)
            ax = fig.add_subplot(111)
            zz = np.log10(Z - np.nanmin(Z) + 1e-3) if np.nanmax(Z) - np.nanmin(Z) > 50 else Z
            ax.contourf(X, Y, zz, levels=levels, cmap="Greys_r", alpha=.55)
            ax.contour(X, Y, zz, levels=levels, colors="white", linewidths=.3, alpha=.6)
            palette = ["#1F4E79", "#C55A11", "#2E7D32", "#6A1B9A", "#00838F"]  # same order as line_chart
            for k, (p, lab) in enumerate(zip(lines, labels)):
                c = palette[k % len(palette)]
                ax.plot(p[:, 0], p[:, 1], "-o", color=c, ms=3, lw=1.2, label=lab)
                ax.plot(p[-1:, 0], p[-1:, 1], "*", color=c, ms=11, mec="white", mew=.6)
            ax.set_xlabel("x0")
            ax.set_ylabel("x1")
            ax.legend(fontsize=8, loc="best")
            fig.tight_layout()
            return fig

        return ReadoutPlot(build, caption="Paths over the function (log scale when the range is large)", id="plot",
                           data=ArrayData("paths", np.concatenate(lines), axes=("point", "coordinate")))

    def _has_chain(self):
        return self.run.kind == "chain" and self.run.function is not None, "not a chain with a function"

    @readout_section("profile", title="Energy profile", available="_has_chain")
    def readout_profile(self, ctx):
        """Function value along the final chain (and the initial one, when recorded)."""
        r = self.run
        e = r.evaluate(r.points)
        ys, names = [e - e.min()], ["final"]
        if r.paths:
            e0 = r.evaluate(r.paths[0][0])
            ys.append(e0 - e.min())
            names.append("initial")
        i_max = int(np.argmax(e))
        return [line_chart(np.arange(1, len(e) + 1), ys, "Image", "f − min f", names=names, markers=True,
                           x_name="image", id="plot",
                           caption=f"Barrier {e[i_max] - e[0]:.6g} at image {i_max + 1} (relative to image 1)"),
                ReadoutFields(FieldSet([Field("barrier_forward", float(e[i_max] - e[0]), label="Forward barrier",
                                              fmt="{:.6g}"),
                                        Field("barrier_reverse", float(e[i_max] - e[-1]), label="Reverse barrier",
                                              fmt="{:.6g}"),
                                        Field("highest_image", i_max + 1, label="Highest image", quantity="int")],
                                       name="barriers"))]

    def _has_samples(self):
        r = self.run
        return r.kind == "critical_points" and getattr(r, "samples", None) is not None, "no fitted samples"

    @readout_section("fit", title="Fit", available="_has_samples")
    def readout_fit(self, ctx):
        """The sampled values with the fitted critical points marked."""
        r = self.run
        x, y = r.samples

        def build():
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            fig = Figure(figsize=(4.6, 3.2), dpi=100)
            FigureCanvasAgg(fig)
            ax = fig.add_subplot(111)
            ax.plot(x, y, "o", color="#1F4E79", ms=4, label="samples")
            ax.plot(r.points[:, 0], np.asarray(r.values).reshape(-1), "*", color="#C55A11", ms=12, label="fit")
            ax.legend(fontsize=8)
            fig.tight_layout()
            return fig

        return ReadoutPlot(build, id="plot", data=TabularData([Column("x", x), Column("y", y)], name="samples"))
