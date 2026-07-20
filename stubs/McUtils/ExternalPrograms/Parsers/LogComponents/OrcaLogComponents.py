"""
This lists the types of readers and things available to the GaussianLogReader
"""
import numpy as np
from ....Parsers import *
from collections import namedtuple, OrderedDict
Components = OrderedDict()
cartesian_start_tag = FileStreamerTag('CARTESIAN COORDINATES (ANGSTROEM)', follow_ups='---------------------------------')
cartesian_end_tag = '\n\n'

def strip_recursive(at_list):
    """
    **LLM Docstring**

    Recursively strip whitespace from every string in a nested list.

    :param at_list: the (possibly nested) list of strings
    :type at_list: list
    :return: the stripped list
    :rtype: list
    """
    ...
OrcaCoords = namedtuple('OrcaCoords', ['atoms', 'coords'])

def cartesian_coordinates_parser(strs):
    """
    **LLM Docstring**

    Parse an ORCA Cartesian-coordinates block into atom labels and coordinates.

    :param strs: the matched block string(s)
    :type strs: list[str]
    :return: the parsed `(atoms, coordinates)`
    :rtype: OrcaCoords
    """
    ...
cartesian_au_start_tag = FileStreamerTag('CARTESIAN COORDINATES (A.U.)', follow_ups='X           Y           Z')
cartesian_end_tag = '\n\n'
OrcaAUCoords = namedtuple('OrcaAUCoords', ['atoms', 'masses', 'coords'])

def cartesian_au_coordinates_parser(strs):
    """
    **LLM Docstring**

    Parse an ORCA atomic-units Cartesian-coordinates block into atom labels, masses,
    and coordinates.

    :param strs: the matched block string(s)
    :type strs: list[str]
    :return: the parsed `(atoms, mass, coordinates)`
    :rtype: OrcaAUCoords
    """
    ...
freqs_start_tag = FileStreamerTag('VIBRATIONAL FREQUENCIES', follow_ups='-----------------------')
freqs_end_tag = '\n\n\n'
FreqsParser = StringParser(Repeating((Named(Integer, 'Mode'), ':', Whitespace, Named(Number, 'Freqs')), suffix=Optional(Newline)))

def freqs_parser(freq_str):
    """
    **LLM Docstring**

    Parse an ORCA vibrational-frequencies block into a flat frequency array.

    :param freq_str: the frequencies block text
    :type freq_str: str
    :return: the frequencies
    :rtype: np.ndarray
    """
    ...
Components['VibrationalFrequencies'] = {'tag_start': freqs_start_tag, 'tag_end': freqs_end_tag, 'parser': freqs_parser, 'mode': 'Single'}

def parse_orca_matrix(orca_mat):
    """
    **LLM Docstring**

    Parse an ORCA column-blocked matrix printout into a dense array, dropping the
    row-index column of each block and concatenating the blocks.

    :param orca_mat: the matrix block text
    :type orca_mat: str
    :return: the parsed matrix
    :rtype: np.ndarray
    """
    ...
nms_start_tag = FileStreamerTag('NORMAL MODES', follow_ups='------------')
nms_end_tag = '\n\n\n'
Components['NormalModes'] = {'tag_start': nms_start_tag, 'tag_end': nms_end_tag, 'parser': parse_orca_matrix, 'mode': 'Single'}
Defaults = ()
glk = ()
list_type = {k: -1 for k in Components if Components[k]['mode'] == 'List'}
Ordering = {k: i for i, k in enumerate([k for k in glk if k not in list_type])}
__components__ = Components
__ordering__ = Ordering
__defaults__ = Defaults