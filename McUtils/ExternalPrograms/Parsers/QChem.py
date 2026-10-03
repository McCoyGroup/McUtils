
import numpy as np
from collections import namedtuple
from .Parsers import ElectronicStructureLogReader
from ...Parsers import FileStreamReader, Number, RegexPattern, Integer, Word

__all__ = [
    "QChemLogReader"
]


class QChemLogReader(ElectronicStructureLogReader):
    """
    Implements a stream-based reader for a Q-Chem output (`.out`/`.log`) file.

    Parallels `MOLPROLogReader`/`OrcaLogReader`: the block tag/parser table lives in
    the companion `QChemLogComponents` module and is resolved lazily by the
    `ElectronicStructureLogReader` base. Read data with `parse`, or the convenience
    classmethod `read_props`::

        from McUtils.ExternalPrograms.Parsers import QChemLogReader

        data = QChemLogReader.read_props(
            "job.out",
            ["Header", "CartesianCoordinates", "SCFEnergies", "FinalEnergy"]
        )
    """
    components_name = "QChemLogComponents"

    def to_readout(self, keys=None, **opts):
        """
        **LLM Docstring**

        Build a `Readout` of parsed results (`QChemLogReadout`).

        :param opts: `ReadoutInterface.to_readout` options (``include``, ``exclude``, ``units``, ...)
        :return: the readout
        :rtype: McUtils.Jupyter.Readouts.Readout
        """
        from ..Readouts.ElectronicStructure import QChemLogReadout
        return QChemLogReadout.from_reader(self, keys=keys).to_readout(**opts)
