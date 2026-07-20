"""
This lists the types of readers and things available to the GaussianLogReader
"""
import io
import numpy as np
from ....Parsers import *
from collections import namedtuple, OrderedDict
Components = OrderedDict()
input_start_tag = FileStreamerTag(' Command line input:')
input_end_tag = '----------------'

def parse_command_line(inp_str):
    """
    **LLM Docstring**

    Pass the matched block through unchanged (the command-line / calculation-info
    text is stored as-is).

    :param inp_str: the block text
    :type inp_str: str
    :return: the block text unchanged
    :rtype: str
    """
    ...
Components['CommandLine'] = {'tag_start': input_start_tag, 'tag_end': input_end_tag, 'parser': parse_command_line, 'mode': 'Single'}
calc_start_tag = FileStreamerTag('Calculation info', follow_ups=('----------------',))
calc_end_tag = '----------------'

def parse_command_line(inp_str):
    """
    **LLM Docstring**

    Pass the matched block through unchanged (the command-line / calculation-info
    text is stored as-is).

    :param inp_str: the block text
    :type inp_str: str
    :return: the block text unchanged
    :rtype: str
    """
    ...
Components['CalculationInfo'] = {'tag_start': calc_start_tag, 'tag_end': calc_end_tag, 'parser': parse_command_line, 'mode': 'Single'}
cartesian_start_tag = FileStreamerTag('Input structure:')
cartesian_end_tag = '\n\n'
CRESTCoords = namedtuple('CRESTCoords', ['atoms', 'coords'])

def cartesian_coordinates_parser(cart):
    """
    **LLM Docstring**

    Parse a CREST Cartesian-coordinates block into atom labels and coordinates.

    :param cart: the coordinates block text
    :type cart: str
    :return: the parsed `(atoms, coords)`
    :rtype: CRESTCoords
    """
    ...
final_opt_info_start = 'Final Geometry Optimization'
final_opt_info_end = '--------------------------'

def parse_opt_info(opt_block):
    """
    **LLM Docstring**

    Pass the final-optimization-info block through unchanged.

    :param opt_block: the block text
    :type opt_block: str
    :return: the block text unchanged
    :rtype: str
    """
    ...
Components['FinalOptInfo'] = {'tag_start': final_opt_info_start, 'tag_end': final_opt_info_end, 'parser': parse_opt_info, 'mode': 'Single'}
final_ensemble_info = FileStreamerTag('Final Ensemble Information', follow_ups=('--------------------------',))
final_ensemble_info_end = '-------'
EnsembleInfo = namedtuple('EnsembleInfo', ['relative_energies', 'total_energies', 'weights', 'report'])

def parse_ensemble_info(opt_block: str):
    """
    **LLM Docstring**

    Parse the final ensemble-information block into the per-conformer energies
    (relative energy, weight, and degeneracy) plus the surrounding report text.

    :param opt_block: the ensemble-info block text
    :type opt_block: str
    :return: the parsed `EnsembleInfo`
    :rtype: EnsembleInfo
    """
    ...
Components['FinalEnsembleInfo'] = {'tag_start': final_ensemble_info, 'tag_end': final_opt_info_end, 'parser': parse_ensemble_info, 'mode': 'Single'}
Defaults = ()
glk = ()
list_type = {k: -1 for k in Components if Components[k]['mode'] == 'List'}
Ordering = {k: i for i, k in enumerate([k for k in glk if k not in list_type])}
__components__ = Components
__ordering__ = Ordering
__defaults__ = Defaults