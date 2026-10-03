"""
Readouts for `McUtils.Data` records (`DataRecord`, e.g. ``AtomData['O']``).
"""

from ...Jupyter.Readouts import ReadoutAdapter, readout_section, record_nodes

__all__ = [
    "DataRecordReadout",
]


class DataRecordReadout(ReadoutAdapter):
    """
    **LLM Docstring**

    Readout for a `DataRecord` (a row of a `McUtils.Data` handler such as `AtomData`): scalar
    fields as a field list, nested values with the generic record view.
    """
    readout_id = "data_record"

    def get_readout_title(self):
        r = self.obj
        for k in ("Name", "name", "Symbol"):
            try:
                v = r[k]
            except Exception:
                continue
            if v:
                return str(v)
        return f"{getattr(r.handler, 'name', type(r.handler).__name__)} record"

    def get_readout_subtitle(self):
        h = getattr(self.obj, "handler", None)
        return f"{type(h).__name__} key {self.obj.key!r}" if h is not None else None

    @readout_section("fields", title="Fields")
    def readout_fields(self, ctx):
        """Every field of the record."""
        units = {"Mass": "AtomicMassUnits", "StandardAtomicWeights": "AtomicMassUnits",
                 "CovalentRadius": "Angstroms", "VanDerWaalsRadius": "Angstroms", "IconRadius": "Angstroms"}
        data = {k: self.obj[k] for k in self.obj.keys()}
        return record_nodes(data, "record", units=units)
