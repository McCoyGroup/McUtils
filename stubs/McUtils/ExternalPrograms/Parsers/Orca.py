import numpy as np
from collections import namedtuple
from .Parsers import ElectronicStructureLogReader
from ...Parsers import FileStreamReader, Number, RegexPattern, Integer, Word
__all__ = ['OrcaLogReader', 'OrcaHessReader']

class OrcaLogReader(ElectronicStructureLogReader):
    components_name = 'OrcaLogComponents'

class OrcaHessReader(FileStreamReader):

    def __init__(self, file, **kwargs):
        """
        **LLM Docstring**

        Open an ORCA `.hess` file for stream reading.

        :param file: the `.hess` file
        :type file: str
        :param kwargs: extra arguments for the stream reader
        """
        ...
    ENumber = RegexPattern((Number, 'E', Integer), 'ENumber', dtype=float)
    matrix_types = {'normal_modes': ENumber}
    array_types = {'vibrational_frequencies': Number, 'dipole_derivatives': ENumber, 'ir_spectrum': Number}

    @classmethod
    def get_special_handlers(cls):
        """
        **LLM Docstring**

        Return the mapping of block tags that need a dedicated parser to that parser.

        :return: the tag-to-handler mapping
        :rtype: dict
        """
        ...

    @classmethod
    def handle_orca_block(cls, tag, data: str):
        """
        **LLM Docstring**

        Dispatch a `.hess` block to the appropriate parser, choosing by tag: a special
        handler, a typed matrix/array parser, or a size-based guess between a scalar,
        array, and matrix.

        :param tag: the block tag
        :type tag: str
        :param data: the block text
        :type data: str
        :return: the parsed block
        :rtype: Any
        """
        ...

    @classmethod
    def parse_matrix(cls, data, col_blocks=5, data_pattern=None):
        """
        **LLM Docstring**

        Parse an ORCA block-formatted matrix (a header giving the dimensions followed by
        column-blocked numeric data) into a dense array.

        :param data: the block text
        :type data: str
        :param col_blocks: number of columns per printed block
        :type col_blocks: int
        :param data_pattern: the numeric pattern to match (defaults to ORCA's `E`-number)
        :type data_pattern: object | None
        :return: the parsed matrix
        :rtype: np.ndarray
        :raises ValueError: if the element count doesn't match the declared size
        """
        ...

    @classmethod
    def parse_array(cls, data, data_pattern=None):
        """
        **LLM Docstring**

        Parse an ORCA block whose header gives a length followed by that many numeric
        rows, flattening single-column results.

        :param data: the block text
        :type data: str
        :param data_pattern: the numeric pattern to match (defaults to ORCA's `E`-number)
        :type data_pattern: object | None
        :return: the parsed array
        :rtype: np.ndarray
        """
        ...
    OrcaCoords = namedtuple('OrcaCoords', ['atoms', 'mass', 'coords'])

    @classmethod
    def parse_atoms(cls, data):
        """
        **LLM Docstring**

        Parse the atoms block into element labels, masses, and coordinates.

        :param data: the block text
        :type data: str
        :return: the parsed `(atoms, mass, coords)`
        :rtype: OrcaHessReader.OrcaCoords
        """
        ...

    def get_next_block(self):
        """
        **LLM Docstring**

        Read the next `$tag ... ` block from the file, returning its tag and body (or
        `None` at end of file).

        :return: `(tag, body)` or `None`
        :rtype: tuple | None
        """
        ...

    def parse(self, tags=None, excludes=None):
        """
        **LLM Docstring**

        Parse the `.hess` file into a dict of tag to parsed block, optionally restricting
        to (or excluding) specific tags.

        :param tags: tags to include (all if omitted)
        :type tags: Iterable[str] | None
        :param excludes: tags to exclude
        :type excludes: Iterable[str] | None
        :return: the parsed blocks keyed by tag
        :rtype: dict
        """
        ...