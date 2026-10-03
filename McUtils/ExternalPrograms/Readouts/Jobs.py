"""
Readouts for external-program job specifications (`ExternalProgramJob`: `GaussianJob`,
`OrcaJob`, `QChemJob`, `CRESTJob`, ...) and execution status snapshots (`ExecutionFuture`,
`ExecutionQueue`). Job readouts are snapshots of the specification: nothing is submitted.
Futures report the status they already hold; ``refresh=True`` asks the backend once, never waits.
"""

import numbers

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutSection, ReadoutFields, ReadoutTable,
    ReadoutCode, FieldSet, Field, Column, TabularData, structure_scene, atoms_table, record_nodes, is_secret_key,
)

__all__ = [
    "ExternalProgramJobReadout",
    "ExecutionReadout",
]

_is_secret = is_secret_key


def _fmt(v):
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, (list, tuple)) and all(isinstance(x, (str, numbers.Number)) for x in v):
        return ", ".join(str(x) for x in v)
    return str(v)


class ExternalProgramJobReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for an `ExternalProgramJob`: one settings table per input block (link-0/resources,
    method, route, ...), the geometry when the job carries ``atoms``/``cartesians`` (Å), and the
    formatted input. Option names that look like credentials are masked.
    """
    readout_id = "job"

    def blocks(self):
        job = self.obj
        return [(b.__name__, opts or {}) for b, opts in zip(job.blocks, job.block_opts)]

    def geometry(self):
        for _, opts in self.blocks():
            if "atoms" in opts and "cartesians" in opts and opts["cartesians"] is not None:
                return list(opts["atoms"]), np.asarray(opts["cartesians"], dtype=float), opts
        return None

    def get_readout_title(self):
        return f"{type(self.obj).__name__.replace('Job', '')} job"

    def get_readout_subtitle(self):
        for _, o in self.blocks():
            if o.get("title"):
                return str(o["title"])
        return None

    @readout_section("settings", title="Settings")
    def readout_settings(self, ctx):
        """Options of every input block (geometry excluded)."""
        nodes = []
        for name, opts in self.blocks():
            items = [(k, v) for k, v in opts.items() if k not in ("atoms", "cartesians", "zmatrix", "internals",
                                                                  "variables", "bonds")]
            if not items:
                continue
            fields = [Field(str(k).lower().replace(" ", "_"), "••••" if _is_secret(k) else _fmt(v), label=str(k))
                      for k, v in items]
            title = name.replace(type(self.obj).__name__.replace("Job", ""), "").replace("Block", "") or name
            nodes.append(ReadoutFields(FieldSet(fields, name=name.lower()), title=title))
        if not nodes:
            raise ReadoutSectionUnavailable("no options set")
        return nodes

    def _has_geometry(self):
        return self.geometry() is not None, "no Cartesian geometry in the job"

    @readout_section("geometry", title="Geometry", available="_has_geometry")
    def readout_geometry(self, ctx):
        """The input geometry (Å)."""
        atoms, xyz, opts = self.geometry()
        f = []
        for k in ("charge", "multiplicity"):
            if opts.get(k) is not None:
                f.append(Field(k, opts[k], label=k.capitalize(), quantity="int"))
        nodes = [ReadoutFields(FieldSet(f, name="state"))] if f else []
        return nodes + [structure_scene(atoms, xyz, id="view"), atoms_table(ctx, atoms, xyz, name="coordinates")]

    @readout_section("input", title="Input")
    def readout_input(self, ctx, max_lines=200):
        """The formatted input file / script."""
        try:
            text = self.obj.format()
        except Exception as e:
            raise ReadoutSectionUnavailable(f"couldn't format the input: {e}")
        return ReadoutCode(text, title=None, id="text", max_lines=max_lines)


class ExecutionReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Status snapshot of an `ExecutionFuture` or an `ExecutionQueue` (one row per future). Results are
    shown only for futures that already completed; ``refresh=True`` calls ``get_status()`` once.
    """
    readout_id = "execution"

    def futures(self):
        return list(getattr(self.obj, "futures", [self.obj]))

    def get_readout_title(self):
        return "Execution queue" if hasattr(self.obj, "futures") else "Execution status"

    @staticmethod
    def _row(fut, refresh):
        status = fut.status
        if refresh:
            try:
                status = fut.get_status()
            except Exception as e:
                status = f"error: {e}"
        status = getattr(status, "value", status)
        info = {"type": type(fut).__name__, "status": str(status)}
        for k in ("job_id", "watch_dir", "poll_time"):
            v = getattr(fut, k, None)
            if v is not None:
                info[k] = str(v)
        return info

    @readout_section("status", title="Status")
    def readout_status(self, ctx, refresh=False):
        """Current (stored) status of each future."""
        rows = [self._row(f, refresh) for f in self.futures()]
        keys = []
        for r in rows:
            keys += [k for k in r if k not in keys]
        cols = [Column("index", np.arange(1, len(rows) + 1), label="#", quantity="index")]
        cols += [Column(k, np.array([r.get(k, "") for r in rows]), label=k.replace("_", " ")) for k in keys]
        counts = {}
        for r in rows:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        return [ReadoutFields(FieldSet([Field(f"n_{k}", v, label=k, quantity="int") for k, v in counts.items()],
                                       name="counts")),
                ReadoutTable(TabularData(cols, name="futures"))]

    @readout_section("results", title="Completed results")
    def readout_results(self, ctx, max_items=10):
        """Results already held by completed futures (no waiting)."""
        nodes = []
        for i, f in enumerate(self.futures()):
            if getattr(f, "_is_complete", False) and getattr(f, "_result", None) is not None:
                res = f._result
                nodes.append(ReadoutSection(*record_nodes(res if isinstance(res, dict) else {"result": res},
                                                          f"result_{i + 1}"),
                                            id=f"result_{i + 1}", title=f"Future {i + 1}"))
            if len(nodes) >= max_items:
                break
        if not nodes:
            raise ReadoutSectionUnavailable("no completed results held")
        return nodes
