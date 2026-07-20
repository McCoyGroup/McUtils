"""
This lists the types of readers and things available to the GaussianLogReader
"""
import io
import numpy as np
from ....Parsers import *
from collections import namedtuple, OrderedDict
Components = OrderedDict()
cartesian_start_tag = FileStreamerTag('Atomic Coordinates', follow_ups=('Nr  Atom  Charge', '\n\n'))
cartesian_end_tag = '\n\n'

def strip_recursive(at_list):
    """
    **LLM Docstring**

    Recursively strip whitespace (and leading integer labels) from every string in a
    nested list.

    :param at_list: the (possibly nested) list of strings
    :type at_list: list
    :return: the cleaned list
    :rtype: list
    """
    ...
MOLPROCoords = namedtuple('MOLPROCoords', ['atoms', 'coords'])

def cartesian_coordinates_parser(strs):
    """
    **LLM Docstring**

    Parse a MOLPRO Cartesian-coordinates block into atom labels and coordinates.

    :param strs: the matched block string(s)
    :type strs: list[str]
    :return: the parsed `(atoms, coordinates)`
    :rtype: MOLPROCoords
    """
    ...
normal_modes_start_tag = FileStreamerTag('Normal Modes')
normal_modes_end_tag = 'Frequencies dumped'
MOLPRONormalModes = namedtuple('MOLPRONormalModes', ['freqs', 'modes'])

def normal_modes_parser(strs):
    """
    **LLM Docstring**

    Parse a MOLPRO normal-modes block into per-structure frequencies and mode
    displacement matrices, concatenating the column sub-blocks.

    :param strs: the matched block string(s)
    :type strs: list[str]
    :return: the parsed `(frequencies, modes)`
    :rtype: MOLPRONormalModes
    """
    ...
Components['NormalModes'] = {'tag_start': normal_modes_start_tag, 'tag_end': normal_modes_end_tag, 'parser': normal_modes_parser, 'mode': 'List'}
quadratic_terms_start_tag = FileStreamerTag('Quadratic force constants:', follow_ups=['f_ij', '\n\n'])
quadratic_terms_end_tag = '\n\n'

def quadratic_terms_parser(qts):
    """
    **LLM Docstring**

    Parse the MOLPRO quadratic force-constant terms into their mode index and value
    arrays.

    :param qts: the quadratic-terms block text
    :type qts: str
    :return: `[indices, values]`
    :rtype: list[np.ndarray]
    """
    ...
cubic_terms_start_tag = FileStreamerTag('Cubic force constants:', follow_ups=['f_ijk', '\n\n'])
cubic_terms_end_tag = '\n\n'

def cubic_terms_parser(qts):
    """
    **LLM Docstring**

    Parse the MOLPRO cubic force-constant terms into their mode-index triples and
    value arrays.

    :param qts: the cubic-terms block text
    :type qts: str
    :return: `[index_triples, values]`
    :rtype: list[np.ndarray]
    """
    ...
Components['CubicTerms'] = {'tag_start': cubic_terms_start_tag, 'tag_end': cubic_terms_end_tag, 'parser': cubic_terms_parser, 'mode': 'Single'}
quartic_terms_start_tag = FileStreamerTag('Quartic force constants:', follow_ups=['f_ijkl', '\n\n'])
quartic_terms_end_tag = '\n\n'

def quartic_terms_parser(qts):
    """
    **LLM Docstring**

    Parse the MOLPRO quartic force-constant terms into their mode-index quadruples
    and value arrays.

    :param qts: the quartic-terms block text
    :type qts: str
    :return: `[index_quadruples, values]`
    :rtype: list[np.ndarray]
    """
    ...
Defaults = ()
glk = ()
list_type = {k: -1 for k in Components if Components[k]['mode'] == 'List'}
Ordering = {k: i for i, k in enumerate([k for k in glk if k not in list_type])}
__components__ = Components
__ordering__ = Ordering
__defaults__ = Defaults