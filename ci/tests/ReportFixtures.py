"""Shared toy source for the report tests: a registered adapter with a few sections (McUtils tests can't import Psience)."""

import numpy as np

from McUtils.Readouts import (Field, FieldSet, ReadoutFields, ReadoutTable, ReadoutAdapter, readout_section,
                              register_readout, Column, TabularData, ReadoutImage)


_TINY_PNG = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d49444154789c6360f8cfc0f01f0005000201"
    "a2b1c0e50000000049454e44ae426082")


class ToyResult:
    """An object with an energy, three frequencies and labels."""

    def __init__(self, name="toy", energy=-76.02665, freqs=(1648.23, 3832.71, 3943.88)):
        self.name = name
        self.energy = float(energy)
        self.freqs = np.array(freqs, dtype=float)
        self.labels = ["bend", "sym stretch", "asym stretch"][:len(self.freqs)]


@register_readout(ToyResult)
class ToyReadout(ReadoutAdapter):
    readout_id = "toy"

    def get_readout_title(self):
        return f"Toy {self.obj.name}"

    @readout_section(description="Energy and size of the system.")
    def readout_summary(self, ctx):
        return ReadoutFields(FieldSet([Field("energy", self.obj.energy, label="Energy", unit="Hartree"),
                                       Field("n_modes", len(self.obj.freqs), label="Modes")], title="Summary"))

    @readout_section(description="Vibrational frequencies in cm-1.")
    def readout_frequencies(self, ctx):
        return ReadoutTable(TabularData([Column("mode", self.obj.labels),
                                         Column("frequency", self.obj.freqs, unit="cm^-1")],
                                        title="Frequencies"))

    @readout_section(default=False, description="A picture of the system (no numbers).")
    def readout_picture(self, ctx):
        return ReadoutImage(_TINY_PNG, content_type="image/png", id="picture", title="Picture")

    @readout_section(default=False, available=lambda i: False, description="Never available.")
    def readout_missing(self, ctx):
        return None


def toy_catalog(**sources):
    """A `SourceCatalog` with the given ``handle=ToyResult`` entries (default: one called ``water``)."""
    from McUtils.Readouts.Reports import SourceCatalog
    cat = SourceCatalog()
    for handle, obj in (sources or {"water": ToyResult("water")}).items():
        cat.add(handle, obj, title=f"Source {handle}")
    return cat


class ReasonQuirkResult(ToyResult):
    """Its sections report ``(True, "reason text")``, the way some real availability checks do."""


@register_readout(ReasonQuirkResult)
class ReasonQuirkReadout(ToyReadout):
    @readout_section(available=lambda i: (True, "informational note, not a problem"), description="Fine.")
    def readout_noted(self, ctx):
        return ReadoutFields(FieldSet([Field("x", 1.0, label="X")], title="Noted"))
