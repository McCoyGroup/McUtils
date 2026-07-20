import os.path
import numpy as np
from collections import namedtuple
from ..Parsers import ElectronicStructureLogReader
from ...Parsers import FileStreamReader, XYZParser, Word, Number
__all__ = ['CRESTParser']

class CRESTOptLogParser(FileStreamReader):

    def __init__(self, file, **kwargs):
        """
        **LLM Docstring**

        Open a CREST optimization log (`crestopt.log`) for stream reading.

        :param file: the log file
        :type file: str
        :param kwargs: extra arguments for the stream reader
        """
        ...
    CRESTCoords = namedtuple('CRESTCoords', ['energy', 'atoms', 'coords'])

    @classmethod
    def parse_struct(cls, data):
        """
        **LLM Docstring**

        Parse one optimization-step block into its energy, atom labels, and coordinates.

        :param data: the block text
        :type data: str
        :return: the parsed `(energy, atoms, coords)`
        :rtype: CRESTOptLogParser.CRESTCoords
        """
        ...

    def get_next_block(self):
        """
        **LLM Docstring**

        Read the next optimization-step block (delimited by `=` and `Etot`), or `None` at
        end of file.

        :return: the block text, or `None`
        :rtype: str | None
        """
        ...

    def parse(self):
        """
        **LLM Docstring**

        Parse every optimization step in the log into a list of coordinate records.

        :return: the parsed steps
        :rtype: list
        """
        ...

class CRESTConfgenLogParser(ElectronicStructureLogReader):
    components_name = 'CRESTLogComponents'

    def parse(self, keys=None, num=None, reset=False):
        """
        **LLM Docstring**

        Parse the conformer-generation log for the requested component keys (defaulting
        to the command line, calculation info, input structure, and final opt/ensemble
        info).

        :param keys: the component keys to parse (defaults chosen if omitted)
        :type keys: list[str] | None
        :param num: number of entries to pull for list-mode components
        :type num: int | None
        :param reset: rewind the stream before parsing
        :type reset: bool
        :return: the parsed data keyed by component
        :rtype: dict
        """
        ...

class CRESTParser:
    """Real access pattern: CRESTParser.<AttrName> (7 class attributes, e.g. CRESTParser.opt_log_file == 'crestopt.log'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"""
    _MEMBERS = {'opt_log_file': 'crestopt.log', 'confgen_log_file': 'confgen.log', 'ensemble_energies_file': 'ensemble_energies.log', 'ensembe_file': 'ensemble_energies.log', 'conformers_best_file': 'crest_best.xyz', 'conformers_file': 'crest_conformers.xyz', 'rotamers_file': 'crest_rotamers.xyz'}

    def __init__(self, parse_dir, opt_log_file=None, confgen_log_file=None, ensemble_energies_file=None, conformers_file=None, conformers_best_file=None, rotamers_file=None):
        """
        **LLM Docstring**

        Set up a parser over a CREST output directory, locating each of the standard
        output files (optimization log, confgen log, ensemble energies, conformers,
        best conformers, rotamers).

        :param parse_dir: the CREST output directory
        :type parse_dir: str
        :param opt_log_file: override for the optimization-log file name
        :type opt_log_file: str | None
        :param confgen_log_file: override for the confgen-log file name
        :type confgen_log_file: str | None
        :param ensemble_energies_file: override for the ensemble-energies file name
        :type ensemble_energies_file: str | None
        :param conformers_file: override for the conformers file name
        :type conformers_file: str | None
        :param conformers_best_file: override for the best-conformers file name
        :type conformers_best_file: str | None
        :param rotamers_file: override for the rotamers file name
        :type rotamers_file: str | None
        """
        ...

    def parse_optimized_structures(self):
        """
        **LLM Docstring**

        Parse the optimization-log file into its sequence of structures.

        :return: the optimization structures
        :rtype: list
        """
        ...

    def parse_ensemble_enegies(self):
        """
        **LLM Docstring**

        Load the ensemble-energies file as a numeric array.

        :return: the ensemble energies
        :rtype: np.ndarray
        """
        ...
    CRESTConformers = namedtuple('CRESTConformers', ['atoms', 'energies', 'coords'])

    def parse_conformers(self, conformers_file=None):
        """
        **LLM Docstring**

        Parse a conformers XYZ file into atoms, per-conformer energies, and coordinates.

        :param conformers_file: the conformers file (defaults to the located one)
        :type conformers_file: str | None
        :return: the parsed `(atoms, energies, coords)`
        :rtype: CRESTParser.CRESTConformers
        """
        ...

    def parse_best_conformers(self):
        """
        **LLM Docstring**

        Parse the best-conformers XYZ file.

        :return: the parsed `(atoms, energies, coords)`
        :rtype: CRESTParser.CRESTConformers
        """
        ...
    CRESTRotamers = namedtuple('CRESTRotamers', ['atoms', 'energies', 'weights', 'coords'])

    def parse_rotamers(self, rotamers_file=None):
        """
        **LLM Docstring**

        Parse a rotamers XYZ file into atoms, energies, weights, and coordinates.

        :param rotamers_file: the rotamers file (defaults to the located one)
        :type rotamers_file: str | None
        :return: the parsed `(atoms, energies, weights, coords)`
        :rtype: CRESTParser.CRESTRotamers
        """
        ...

    def parse_log(self):
        """
        **LLM Docstring**

        Parse the conformer-generation log file.

        :return: the parsed log data
        :rtype: dict
        """
        ...

    def _locate_file(self, base_file, default_file):
        """
        **LLM Docstring**

        Resolve an output file name to a path within the parse directory, falling back
        to the bare name if it isn't found there.

        :param base_file: the requested file name (or `None` to use the default)
        :type base_file: str | None
        :param default_file: the default file name
        :type default_file: str
        :return: the located path
        :rtype: str
        """
        ...