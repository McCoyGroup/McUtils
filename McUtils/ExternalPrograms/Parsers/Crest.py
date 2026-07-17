import os.path

import numpy as np
from collections import namedtuple
from ..Parsers import ElectronicStructureLogReader
from ...Parsers import FileStreamReader, XYZParser, Word, Number


__all__ = [
    "CRESTParser"
]

class CRESTOptLogParser(FileStreamReader):

    def __init__(self, file, **kwargs):
        """
        **LLM Docstring**

        Open a CREST optimization log (`crestopt.log`) for stream reading.

        :param file: the log file
        :type file: str
        :param kwargs: extra arguments for the stream reader
        """
        super().__init__(file, **kwargs)

    CRESTCoords = namedtuple("CRESTCoords", ["energy", "atoms", "coords"])
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
        coords = np.array(Number.findall(data)).astype(float)
        e, coords = coords[0], coords[1:].reshape(-1, 3)
        atoms = Word.findall(data)
        return cls.CRESTCoords(
            e,
            atoms,
            coords
        )

    def get_next_block(self):
        """
        **LLM Docstring**

        Read the next optimization-step block (delimited by `=` and `Etot`), or `None` at
        end of file.

        :return: the block text, or `None`
        :rtype: str | None
        """
        block = self.get_tagged_block("=", "Etot")
        if block is None:
            return None
        else:
            return block.rsplit("\n", 1)[0]

    def parse(self):
        """
        **LLM Docstring**

        Parse every optimization step in the log into a list of coordinate records.

        :return: the parsed steps
        :rtype: list
        """
        res = []
        block = self.get_next_block()
        while block is not None:
            res.append(self.parse_struct(block))
            block = self.get_next_block()

        return res

class CRESTConfgenLogParser(ElectronicStructureLogReader):
    components_name = "CRESTLogComponents"

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
        if keys is None:
            keys = [
                "CommandLine",
                "CalculationInfo",
                "InputStructure",
                "FinalOptInfo",
                "FinalEnsembleInfo"
            ]
        return super().parse(keys, num=num, reset=reset)

class CRESTParser:

    opt_log_file = 'crestopt.log'
    confgen_log_file = 'confgen.log'
    ensemble_energies_file = 'ensemble_energies.log'
    ensembe_file = 'ensemble_energies.log'
    conformers_best_file = 'crest_best.xyz'
    conformers_file = 'crest_conformers.xyz'
    rotamers_file = 'crest_rotamers.xyz'
    def __init__(self, parse_dir,
                 opt_log_file=None,
                 confgen_log_file=None,
                 ensemble_energies_file=None,
                 conformers_file=None,
                 conformers_best_file=None,
                 rotamers_file=None
                 ):
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
        self.dir = parse_dir
        self.opt_log_file = self._locate_file(opt_log_file, self.opt_log_file)
        self.confgen_log_file = self._locate_file(confgen_log_file, self.confgen_log_file)
        self.ensemble_energies_file = self._locate_file(ensemble_energies_file, self.ensemble_energies_file)
        self.conformers_file = self._locate_file(conformers_file, self.conformers_file)
        self.conformers_best_file = self._locate_file(conformers_best_file, self.conformers_best_file)
        self.rotamers_file = self._locate_file(rotamers_file, self.rotamers_file)
    def parse_optimized_structures(self):
        """
        **LLM Docstring**

        Parse the optimization-log file into its sequence of structures.

        :return: the optimization structures
        :rtype: list
        """
        with CRESTOptLogParser(self.opt_log_file) as parser:
            structs = parser.parse()
        return structs

    def parse_ensemble_enegies(self):
        """
        **LLM Docstring**

        Load the ensemble-energies file as a numeric array.

        :return: the ensemble energies
        :rtype: np.ndarray
        """
        return np.loadtxt(self.ensemble_energies_file)

    CRESTConformers = namedtuple("CRESTConformers", ['atoms', 'energies', 'coords'])
    def parse_conformers(self, conformers_file=None):
        """
        **LLM Docstring**

        Parse a conformers XYZ file into atoms, per-conformer energies, and coordinates.

        :param conformers_file: the conformers file (defaults to the located one)
        :type conformers_file: str | None
        :return: the parsed `(atoms, energies, coords)`
        :rtype: CRESTParser.CRESTConformers
        """
        if conformers_file is None:
            conformers_file = self.conformers_file
        with XYZParser(conformers_file) as parser:
            structs = parser.parse()
        atoms = structs[0][1]
        coords = np.array([s for c,a,s in structs])
        energies = np.array([c.strip() for c,a,s in structs]).astype(float)
        return self.CRESTConformers(atoms, energies, coords)

    def parse_best_conformers(self):
        """
        **LLM Docstring**

        Parse the best-conformers XYZ file.

        :return: the parsed `(atoms, energies, coords)`
        :rtype: CRESTParser.CRESTConformers
        """
        return self.parse_conformers(self.conformers_best_file)

    CRESTRotamers = namedtuple("CRESTRotamers", ['atoms', 'energies', 'weights', 'coords'])
    def parse_rotamers(self, rotamers_file=None):
        """
        **LLM Docstring**

        Parse a rotamers XYZ file into atoms, energies, weights, and coordinates.

        :param rotamers_file: the rotamers file (defaults to the located one)
        :type rotamers_file: str | None
        :return: the parsed `(atoms, energies, weights, coords)`
        :rtype: CRESTParser.CRESTRotamers
        """
        if rotamers_file is None:
            rotamers_file = self.rotamers_file
        with XYZParser(rotamers_file) as parser:
            structs = parser.parse()
        atoms = structs[0][1]
        coords = np.array([s for c,a,s in structs])
        eng_rel = np.array([c.split()[:2] for c,a,s in structs]).astype(float)
        return self.CRESTRotamers(atoms, eng_rel[:, 0], eng_rel[:, 1], coords)

    def parse_log(self):
        """
        **LLM Docstring**

        Parse the conformer-generation log file.

        :return: the parsed log data
        :rtype: dict
        """
        with CRESTConfgenLogParser(self.confgen_log_file) as parser:
            structs = parser.parse()
        return structs

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
        if base_file is None:
            base_file = default_file
        test = os.path.join(self.dir, base_file)
        if os.path.exists(test):
            return test
        else:
            return base_file