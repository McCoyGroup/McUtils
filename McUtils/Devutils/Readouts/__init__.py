"""
Readouts for development utilities: `OptionsSet` (the options, with credential-like values masked,
and optionally how they route to target callables). `Logger` readouts are log-file readouts
(`McUtils.Scaffolding.Readouts.LogReadout`).
"""

import numpy as np

from ...Jupyter.Readouts import (
    ReadoutAdapter, readout_section, ReadoutSectionUnavailable, ReadoutTable, Column, TabularData,
    record_nodes, mask_secrets,
)

__all__ = [
    "OptionsSetReadout",
]


class OptionsSetReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for an `OptionsSet` (or a plain options dict). With ``targets`` (callables or classes
    the options are split across), a routing table shows which target accepts each option.
    """
    readout_id = "options"

    def __init__(self, options, targets=()):
        super().__init__(options)
        self.targets = list(targets) if isinstance(targets, (list, tuple)) else [targets]

    def ops(self):
        o = self.obj
        return dict(o.__dict__["ops"]) if "ops" in getattr(o, "__dict__", {}) else dict(o)

    def get_readout_title(self):
        return "Options"

    @readout_section("options", title="Options")
    def readout_options(self, ctx):
        """Option values (credential-like values masked)."""
        ops = self.ops()
        if not ops:
            raise ReadoutSectionUnavailable("no options")
        return record_nodes(mask_secrets(ops), "options")

    def _has_targets(self):
        return bool(self.targets), "no targets given"

    @readout_section("routing", title="Routing", available="_has_targets")
    def readout_routing(self, ctx):
        """Which target accepts each option (options no target accepts are flagged)."""
        from ..Options import OptionsSet
        ops = self.ops()
        helper = OptionsSet(dict(ops))
        names = sorted(ops)
        cols = [Column("option", np.array(names), label="Option")]
        accepted = np.zeros(len(names), dtype=bool)
        for t in self.targets:
            try:
                props = set(helper.get_props(t))
            except Exception:
                props = set()
            hit = np.array([n in props for n in names])
            accepted |= hit
            cols.append(Column(getattr(t, "__name__", str(t)), np.where(hit, "✓", ""),
                               label=getattr(t, "__qualname__", getattr(t, "__name__", str(t)))))
        cols.append(Column("unused", np.where(accepted, "", "unused"), label="Unused"))
        return ReadoutTable(TabularData(cols, name="routing"))
