import numpy as np
import re
from ...Parsers import FileLineByLineReader
__all__ = ['CIFParser', 'CIFConverter']

class CIFSymmetriesArray:

    def __init__(self, key, symmetry_list):
        """
        **LLM Docstring**

        Hold the symmetry-operation strings for a CIF key, deferring construction of the
        matrix form.

        :param key: the CIF key these symmetries belong to
        :type key: str
        :param symmetry_list: the symmetry-function string(s)
        :type symmetry_list: str | list[str]
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a short representation noting how many symmetry operations are held.

        :return: the representation
        :rtype: str
        """
        ...

    def _parse_symmetry_function(self, arr, row, sf):
        """
        **LLM Docstring**

        Parse one CIF symmetry-function component (e.g. `x`, `-y`, `1/2+z`) into a row of
        an affine transformation matrix, filling in the coefficients and the translation.

        :param arr: the affine matrix being filled (modified in place)
        :type arr: np.ndarray
        :param row: the row (output coordinate) index
        :type row: int
        :param sf: the symmetry-function string for this coordinate
        :type sf: str
        """
        ...

    def _get_symmetries(self, key, symm_labels):
        """
        **LLM Docstring**

        Build the affine transformation matrix (or a stack of them) from CIF symmetry
        labels.

        :param key: the CIF key (for context)
        :type key: str
        :param symm_labels: a single `x,y,z`-style label or a list of them
        :type symm_labels: str | list[str]
        :return: the affine matrix or stack of matrices
        :rtype: np.ndarray
        """
        ...

    @property
    def transformation(self):
        """
        **LLM Docstring**

        The (cached) affine transformation matrices for the held symmetry operations.

        :return: the symmetry transformation matrices
        :rtype: np.ndarray
        """
        ...

class CIFParser(FileLineByLineReader):

    def __init__(self, file, fields=None, **kw):
        """
        **LLM Docstring**

        Open a CIF file for line-by-line reading.

        :param file: the CIF file
        :type file: str
        :param fields: the fields to restrict parsing to (all if omitted)
        :type fields: Iterable[str] | None
        :param kw: extra arguments for the line reader
        """
        ...

    def check_tag(self, line: str, depth: int=0, active_tag=None, label: str=None, history: list[str]=None):
        """
        **LLM Docstring**

        Classify a CIF line for the line-by-line reader: block starts (`data_`, `loop_`,
        `_key`), comments (`#`), block ends (`#END`), and loop boundaries.

        :param line: the current line
        :type line: str
        :param depth: the current nesting depth
        :type depth: int
        :param active_tag: the currently active block tag
        :param label: the current block label
        :type label: str | None
        :param history: the lines seen so far in the current block
        :type history: list[str] | None
        :return: the reader tag (and any label/data), or `None` to accumulate the line
        :rtype: object
        """
        ...
    custom_handlers = {}

    def get_block_handlers(self):
        """
        **LLM Docstring**

        Return the mapping of CIF field name to the handler that converts its raw text
        into a typed value (floats, ints, or symmetry arrays).

        :return: the field-to-handler mapping
        :rtype: dict
        """
        ...

    def _get_float(self, key, val):
        """
        **LLM Docstring**

        Convert a CIF value (scalar or list) to float(s).

        :param key: the field name (for context)
        :type key: str
        :param val: the raw value
        :type val: str | list
        :return: the float value(s)
        :rtype: float | np.ndarray
        """
        ...

    def _get_int(self, key, val):
        """
        **LLM Docstring**

        Convert a CIF value (scalar or list) to int(s).

        :param key: the field name (for context)
        :type key: str
        :param val: the raw value
        :type val: str | list
        :return: the int value(s)
        :rtype: float | np.ndarray
        """
        ...

    def resolve_handler(self, label: 'str|None'):
        """
        **LLM Docstring**

        Pick the handler for a field, falling back to the integer handler for fields
        whose names end in `_num`/`_number`.

        :param label: the field name
        :type label: str | None
        :return: the handler, or `None`
        :rtype: Callable | None
        """
        ...

    def handle_block(self, label: 'str|None', block_data, join=True, depth=0):
        """
        **LLM Docstring**

        Convert a parsed CIF block into typed data: apply a field handler when there is
        one, join text otherwise, and for unlabeled `loop_` blocks split the leading key
        lines from the value rows into per-key lists.

        :param label: the block label (or `None` for a loop block)
        :type label: str | None
        :param block_data: the accumulated block lines
        :type block_data: list | str
        :param join: join multi-line text values
        :type join: bool
        :param depth: the current nesting depth
        :type depth: int
        :return: the parsed block data
        :rtype: Any
        """
        ...

    def parse(self, target_fields=None):
        """
        **LLM Docstring**

        Parse the CIF file into a list of block dicts, optionally restricting to a set of
        target fields.

        :param target_fields: the fields to keep (all if omitted)
        :type target_fields: Iterable[str] | None
        :return: the parsed blocks
        :rtype: list
        """
        ...

class CIFConverter:

    def __init__(self, parsed_cif):
        """
        **LLM Docstring**

        Wrap parsed CIF data to provide higher-level property/coordinate extraction.

        :param parsed_cif: the parsed CIF blocks
        :type parsed_cif: list
        """
        ...

    @property
    def cell_properties(self):
        """
        **LLM Docstring**

        The unit-cell properties (all `cell_*` fields), merged into one dict.

        :return: the cell properties
        :rtype: dict
        """
        ...

    @property
    def atom_properties(self):
        """
        **LLM Docstring**

        The atom-site properties (all `atom_*` fields), merged into one dict.

        :return: the atom properties
        :rtype: dict
        """
        ...

    @property
    def symmetry_properties(self):
        """
        **LLM Docstring**

        The symmetry properties (all `symmetry_*` fields), merged into one dict.

        :return: the symmetry properties
        :rtype: dict
        """
        ...

    def prep_property_dict(self, res):
        """
        **LLM Docstring**

        Flatten a list of per-block property dicts into a single merged dict.

        :param res: the per-block property dicts
        :type res: list[dict]
        :return: the merged properties
        :rtype: dict
        """
        ...

    def find(self, item, strict=True, cache=False):
        """
        **LLM Docstring**

        Find the first value matching a field name (exact or, when `strict` is off, by
        regex), optionally caching the result.

        :param item: the field name or pattern
        :type item: str
        :param strict: match the name exactly
        :type strict: bool
        :param cache: cache the lookup
        :type cache: bool
        :return: the matched value (or matching `{key: value}`), or `None`
        :rtype: Any
        """
        ...

    def find_all(self, item, strict=True, cache=False):
        """
        **LLM Docstring**

        Find every value matching a field name (exact or, when `strict` is off, by
        regex), optionally caching the result.

        :param item: the field name or pattern
        :type item: str
        :param strict: match the name exactly
        :type strict: bool
        :param cache: cache the lookup
        :type cache: bool
        :return: the matched values
        :rtype: list
        """
        ...

    @property
    def atoms(self):
        """
        **LLM Docstring**

        The atom coordinates built from the atom and symmetry properties (applying the
        symmetry operations to the base coordinates).

        :return: the `{atoms, coords, charges}` structure
        :rtype: dict
        """
        ...

    def construct_base_atom_coords(self, property_dict):
        """
        **LLM Docstring**

        Build the base (asymmetric-unit) atom structure from a property dict: element
        symbols, charges, and fractional coordinates.

        :param property_dict: the merged atom properties
        :type property_dict: dict
        :return: the `{atoms, coords, charges}` structure
        :rtype: dict
        """
        ...

    def construct_atom_coords(self, atom_properties, symmetry_properties):
        """
        **LLM Docstring**

        Build the full atom structure by applying the crystallographic symmetry
        operations to the base coordinates (replicating atoms/charges accordingly).

        :param atom_properties: the merged atom properties
        :type atom_properties: dict
        :param symmetry_properties: the merged symmetry properties
        :type symmetry_properties: dict
        :return: the `{atoms, coords, charges}` structure
        :rtype: dict
        """
        ...