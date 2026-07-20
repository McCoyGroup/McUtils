"""
Implements an importer for Gaussian output formats
"""
import numpy as np, re, math, io
from .GaussianLogComponents import GaussianLogComponents, GaussianLogDefaults, GaussianLogOrdering
from . import GaussianLogComponents as GaussianLogParsers
from .GaussianFChkComponents import FormattedCheckpointComponents, FormattedCheckpointCommonNames
from ...Parsers import FileStreamReader, FileStreamCheckPoint, FileStreamReaderException
__all__ = ['GaussianFChkReader', 'GaussianLogReader', 'GaussianLogReaderException', 'GaussianFChkReaderException']
__reload_hook__ = ['.GaussianFChkComponents', '.GaussianLogComponents']

class GaussianLogReaderException(FileStreamReaderException):
    """
    A class for holding exceptions that occur in the course of reading from a log file
    """

class GaussianLogReader(FileStreamReader):
    """
    Implements a stream based reader for a Gaussian .log file.
    This is inherits from the `FileStreamReader` base, and takes a two pronged approach to getting data.
    First, a block is found in a log file based on a pair of tags.
    Next, a function (usually based on a `StringParser`) is applied to this data to convert it into a usable data format.
    The goal is to move toward wrapping all returned data in a `QuantityArray` so as to include data type information, too.

    You can see the full list of available keys in the `GaussianLogComponents` module, but currently they are:
    * `"Header"`: the header for the Gaussian job
    * `"InputZMatrix"`: the string of the input Z-matrix
    * `"CartesianCoordinates"`: all the Cartesian coordinates in the file
    * `"ZMatCartesianCoordinates"`: all of the Cartesian coordinate in Z-matrix orientation
    * `"StandardCartesianCoordinates"`: all of the Cartesian coordinates in 'standard' orientation
    * `"InputCartesianCoordinates"`: all of the Cartesian coordinates in 'input' orientation
    * `"ZMatrices"`: all of the Z-matrices
    * `"OptimizationParameters"`: all of the optimization parameters
    * `"MullikenCharges"`: all of the Mulliken charges
    * `"MultipoleMoments"`: all of the multipole moments
    * `"DipoleMoments"`: all of the dipole moments
    * `"OptimizedDipoleMoments"`: all of the dipole moments from an optimized scan
    * `"ScanEnergies"`: the potential surface information from a scan
    * `"OptimizedScanEnergies"`: the PES from an optimized scan
    * `"XMatrix"`: the anharmonic X-matrix from Gaussian's style of perturbation theory
    * `"Footer"`: the footer from a calculation

    You can add your own types, too.
    If you need something we don't have, give `GaussianLogComponents` a look to see how to add it in.

    """
    registered_components = GaussianLogComponents
    default_keys = GaussianLogDefaults
    default_ordering = GaussianLogOrdering
    parsers = GaussianLogParsers

    def parse(self, keys=None, num=None, reset=False):
        """The main function we'll actually use. Parses bits out of a .log file.

        :param keys: the keys we'd like to read from the log file
        :type keys: str or list(str)
        :param num: for keys with multiple entries, the number of entries to pull
        :type num: int or None
        :return: the data pulled from the log file, strung together as a `dict` and keyed by the _keys_
        :rtype: dict
        """
        ...

    def get_default_keys(self):
        """
        Tries to get the default keys one might be expected to want depending on the type of job as determined from the Header
        Currently only supports 'opt', 'scan', and 'popt' as job types.

        :return: key listing
        :rtype: tuple(str)
        """
        ...

    @classmethod
    def read_props(cls, file, keys):
        """
        **LLM Docstring**

        Convenience classmethod: open `file`, parse the requested keys, and return the
        result (unwrapped to the single value when one key is given).

        :param file: the Gaussian `.log` file
        :type file: str
        :param keys: the component key(s) to read
        :type keys: str | list[str]
        :return: the parsed data
        :rtype: dict | Any
        """
        ...

class GaussianFChkReaderException(FileStreamReaderException):
    ...

class GaussianFChkReader(FileStreamReader):
    """Implements a stream based reader for a Gaussian .fchk file. Pretty generall I think. Should be robust-ish.
    One place to change things up is convenient parsers for specific commonly pulled parts of the fchk

    """
    GaussianFChkReaderException = GaussianFChkReaderException
    registered_components = FormattedCheckpointComponents
    common_names = {to_: from_ for from_, to_ in FormattedCheckpointCommonNames.items()}
    to_common_name = FormattedCheckpointCommonNames

    def __init__(self, file, **kwargs):
        """
        **LLM Docstring**

        Open a Gaussian `.fchk` file for stream reading.

        :param file: the `.fchk` file
        :type file: str
        :param kwargs: extra arguments for the stream reader
        """
        ...

    def read_header(self):
        """Reads the header and skips the stream to where we want to be

        :return: the header
        :rtype: str
        """
        ...
    fchk_re_pattern = '^(.+?)\\s+(I|R|C|H)\\s+(N=)?\\s+(.+)\\s+'
    fchk_re = re.compile(fchk_re_pattern)

    def get_next_block_params(self):
        """Pulls the tag of the next block, the type, the number of bytes it'll be,
        and if it's a single-line block it'll also spit back the block itself

        :return:
        :rtype: dict
        """
        ...

    def get_block(self, name=None, dtype=None, byte_count=None, value=None):
        """Pulls the next block by first pulling the block tag

        :return:
        :rtype:
        """
        ...

    def skip_block(self, name=None, dtype=None, byte_count=None, value=None):
        """Skips the next block

        :return:
        :rtype:
        """
        ...

    @property
    def num_atoms(self):
        """
        **LLM Docstring**

        The number of atoms in the file, parsed (and cached) from the `Number of atoms`
        block on first access.

        :return: the atom count
        :rtype: int
        """
        ...

    def parse(self, keys=None, default='raise'):
        """
        **LLM Docstring**

        Parse the requested blocks out of the `.fchk` file (or every block when no keys
        are given), resolving common-name aliases and skipping unrequested blocks.

        Malformed blocks are skipped where possible; when a requested key can't be found,
        either raises or fills in `default` depending on the `default` argument.

        :param keys: the block key(s) to read (all if omitted)
        :type keys: str | Iterable[str] | None
        :param default: value to use for missing keys, or `'raise'` to error
        :type default: Any
        :return: the parsed blocks keyed by name
        :rtype: dict
        """
        ...

    @classmethod
    def read_props(cls, file, keys):
        """
        **LLM Docstring**

        Convenience classmethod: open `file`, parse the requested keys, and return the
        result (unwrapped to the single value when one key is given).

        :param file: the `.fchk` file
        :type file: str
        :param keys: the block key(s) to read
        :type keys: str | list[str]
        :return: the parsed data
        :rtype: dict | Any
        """
        ...