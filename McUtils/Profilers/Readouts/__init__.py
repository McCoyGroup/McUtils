"""
Readouts for profiling and timing data: `Timer` measurements and `BlockProfiler` runs
(cProfile statistics as call tables and a cumulative-time chart; pyinstrument sessions as their
text report). Readouts only read what was recorded; they never run or re-time code.
"""

import os

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutFields, ReadoutTable, ReadoutCode,
    FieldSet, Field, Column, TabularData, bar_chart, line_chart,
)

__all__ = [
    "TimerReadout",
    "ProfileReadout",
]


class TimerReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for a `Timer`: the latest elapsed time and every recorded lap (``Timer.log`` /
    checkpoints), in seconds.
    """
    readout_id = "timer"

    def get_readout_title(self):
        return f"Timer: {self.obj.tag}" if self.obj.tag else "Timer"

    @readout_section("summary", title="Timing")
    def readout_summary(self, ctx):
        """Latest elapsed time, lap count and settings."""
        t = self.obj
        f = [Field("tag", str(t.tag), label="Tag"),
             Field("latest", np.nan if t.latest is None else float(t.latest), label="Latest (s)", fmt="{:.6f}"),
             Field("laps", len(t.laps), label="Laps", quantity="int")]
        if t.number is not None:
            f.append(Field("number", int(t.number), label="Repetitions", quantity="int"))
        if t.latest is not None and t.number:
            f.append(Field("per_call", float(t.latest) / t.number, label="Per call (s)", fmt="{:.6g}"))
        return ReadoutFields(FieldSet(f, name="summary"))

    def _has_laps(self):
        return len(self.obj.laps) > 0, "no laps recorded"

    @readout_section("laps", title="Laps", available="_has_laps")
    def readout_laps(self, ctx):
        """Each lap's split relative to its checkpoint and since the first lap."""
        laps = np.asarray(self.obj.laps, dtype=float).reshape(-1, 2)
        t0 = laps[0, 0]
        cols = [Column("lap", np.arange(1, len(laps) + 1), label="Lap", quantity="index"),
                Column("split", laps[:, 1] - laps[:, 0], label="Since checkpoint (s)", fmt="{:.6f}"),
                Column("elapsed", laps[:, 1] - t0, label="Since start (s)", fmt="{:.6f}")]
        nodes = [ReadoutTable(TabularData(cols, name="laps"))]
        if len(laps) > 1:
            nodes.append(line_chart(np.arange(1, len(laps) + 1), np.diff(np.concatenate([[t0], laps[:, 1]])), "Lap",
                                    "Lap time (s)", markers=True, x_name="lap", id="plot"))
        return nodes


class ProfileReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for a `BlockProfiler` after it ran. cProfile runs (`CProfileBlockProfiler`) give a
    table of the top functions by cumulative and internal time and a bar chart; the full statistics
    are exported. Pyinstrument runs give their text report.
    """
    readout_id = "profile"

    def stats(self):
        pr = getattr(self.obj, "pr", None)
        if pr is None:
            return None
        import pstats
        return pstats.Stats(pr)

    def get_readout_title(self):
        return f"Profile: {self.obj.name}"

    def rows(self):
        st = self.stats()
        out = []
        for (file, line, func), (cc, nc, tt, ct, callers) in st.stats.items():
            loc = f"{os.path.basename(file)}:{line}" if file != "~" else "built-in"
            out.append((f"{func} ({loc})", int(nc), int(cc), float(tt), float(ct), file))
        return out

    @readout_section("summary", title="Run")
    def readout_summary(self, ctx):
        """Totals."""
        st = self.stats()
        f = [Field("profiler", type(self.obj).__name__, label="Profiler"), Field("name", self.obj.name, label="Block")]
        if st is not None:
            f += [Field("total_time", float(st.total_tt), label="Total time (s)", fmt="{:.6f}"),
                  Field("total_calls", int(st.total_calls), label="Function calls", quantity="int"),
                  Field("primitive_calls", int(st.prim_calls), label="Primitive calls", quantity="int"),
                  Field("functions", len(st.stats), label="Functions", quantity="int")]
        return ReadoutFields(FieldSet(f, name="summary"))

    def _has_stats(self):
        return self.stats() is not None, "not a cProfile run"

    @readout_section("functions", title="Top functions", available="_has_stats")
    def readout_functions(self, ctx, top=20, sort_by="cumulative", strip=None):
        """The ``top`` functions by cumulative (or ``'tottime'``) time (``top=None`` shows and exports all)."""
        rows = self.rows()
        key = 4 if sort_by.startswith("cum") else 3
        rows.sort(key=lambda r: -r[key])
        cols = [Column("function", np.array([r[0] for r in rows]), label="Function"),
                Column("calls", np.array([r[1] for r in rows]), label="Calls"),
                Column("primitive_calls", np.array([r[2] for r in rows]), label="Primitive"),
                Column("tottime", np.array([r[3] for r in rows]), label="Own time (s)", fmt="{:.6f}"),
                Column("cumtime", np.array([r[4] for r in rows]), label="Cumulative (s)", fmt="{:.6f}"),
                Column("per_call", np.array([r[4] / max(r[1], 1) for r in rows]), label="Cum./call (s)", fmt="{:.3g}")]
        table = TabularData(cols, name="functions")
        top = len(rows) if top is None else top
        shown = rows[:min(top, 15)]
        return [bar_chart([r[0] for r in shown], [r[key] for r in shown],
                          y_label="Cumulative time" if key == 4 else "Own time", y_unit="Seconds",
                          id="chart", value_name="time"),
                ReadoutTable(table.take_rows(slice(0, top)), title=f"Top {min(top, len(rows))} of {len(rows)}")]

    @readout_section("report", title="Report", default=False)
    def readout_report(self, ctx, max_lines=80):
        """The profiler's own text report (`format_profile`)."""
        try:
            text = self.obj.format_profile()
        except Exception as e:
            raise ReadoutSectionUnavailable(f"no report: {e}")
        return ReadoutCode(text, id="text", max_lines=max_lines)
