import numpy as np
import string
from .TableFormatters import TableFormatter
__all__ = ['format_tensor_element_table', 'format_symmetric_tensor_elements', 'format_mode_labels', 'format_zmatrix', 'format_state_vector_frequency_table', 'format_radix_value', 'format_elapsed_time']

def format_tensor_element_table(inds, vals, headers=('Indices', 'Value'), format='{:8.3f}', column_join='|', index_format='{:>5.0f}', **etc):
    """
    **LLM Docstring**

    Combine transposed index arrays with one or more value columns and format them under spanning headers.

    :param inds: index arrays identifying tensor elements
    :type inds: object
    :param vals: values paired with the index tuples
    :type vals: object
    :param headers: optional header rows
    :type headers: object
    :param format: numeric value formatter or formatter sequence
    :type format: object
    :param column_join: separator or separator sequence between columns
    :type column_join: object
    :param index_format: formatter applied to tensor index columns
    :type index_format: object
    :param etc: additional keyword options forwarded to the underlying formatter or operation
    :type etc: dict
    :return: formatted text
    :rtype: str
    """
    ...

def format_symmetric_tensor_elements(tensor, symmetries=None, cutoff=1e-06, headers=('Indices', 'Value'), allowed_indices=None, filter=None, format='{:12.3f}', **etc):
    """
    **LLM Docstring**

    Select entries above a cutoff, retain one ordered representative per declared symmetry, apply optional masks, and format them.

    :param tensor: tensor whose non-negligible symmetry-unique elements are formatted
    :type tensor: object
    :param symmetries: groups of tensor axes across which only nondecreasing index tuples are retained
    :type symmetries: object
    :param cutoff: absolute-value threshold for retaining tensor entries
    :type cutoff: object
    :param headers: optional header rows
    :type headers: object
    :param allowed_indices: per-axis allowed index collections
    :type allowed_indices: object
    :param filter: additional callable mask over retained index arrays
    :type filter: object
    :param format: numeric value formatter or formatter sequence
    :type format: object
    :param etc: additional keyword options forwarded to the underlying formatter or operation
    :type etc: dict
    :return: formatted text
    :rtype: str
    """
    ...

def format_mode_labels(labels, freqs=None, high_to_low=True, mode_index_format='{:.0f}', frequency_format='{:.0f}', headers=None, column_join=' | ', none_tag='mixed', **etc):
    """
    **LLM Docstring**

    Render one-based mode numbers with normalized label text and optional frequencies, optionally reversing high-to-low order.

    :param labels: mode-label objects
    :type labels: object
    :param freqs: optional frequencies paired with mode labels
    :type freqs: object
    :param high_to_low: whether modes and frequencies are reversed before numbering
    :type high_to_low: object
    :param mode_index_format: formatter for one-based mode indices
    :type mode_index_format: object
    :param frequency_format: formatter for frequencies
    :type frequency_format: object
    :param headers: optional header rows
    :type headers: object
    :param column_join: separator or separator sequence between columns
    :type column_join: object
    :param none_tag: text used when a mode label has no type
    :type none_tag: object
    :param etc: additional keyword options forwarded to the underlying formatter or operation
    :type etc: dict
    :return: formatted text
    :rtype: str
    """
    ...

def format_zmatrix(zm, preserve_embedding=True, preserve_indices=True, list_form=True):
    """
    **LLM Docstring**

    Format Z-matrix index rows with width chosen from the largest index and optionally remove embedding placeholders or atom indices.

    :param zm: Z-matrix index table
    :type zm: object
    :param preserve_embedding: whether placeholder embedding references in the first rows are retained
    :type preserve_embedding: object
    :param preserve_indices: whether the leading atom-index column and first row are retained
    :type preserve_indices: object
    :param list_form: whether output is formatted as a Python-style nested list
    :type list_form: object
    :return: formatted text
    :rtype: str
    """
    ...

def format_state_vector_frequency_table(state_list, freq_data, state_header='State', freq_header='Freq.', freq_fmt='{:.3f}', sep=' | ', join=' '):
    """
    **LLM Docstring**

    Join state-vector columns with one or more frequency columns under spanning headers.

    :param state_list: state vectors or state labels
    :type state_list: object
    :param freq_data: one or more frequency columns
    :type freq_data: object
    :param state_header: header for state-vector columns
    :type state_header: object
    :param freq_header: header or headers for frequency columns
    :type freq_header: object
    :param freq_fmt: frequency formatter or sequence of formatters
    :type freq_fmt: object
    :param sep: separator between state and frequency blocks
    :type sep: object
    :param join: separator between multiple frequency columns
    :type join: object
    :return: formatted text
    :rtype: str
    """
    ...

def format_radix_value(duration, target_format, variable_map, format_variables=None):
    """
    **LLM Docstring**

    Successively divide a duration by named unit sizes and interpolate quotient components plus the final remainder.

    :param duration: value to decompose into radix units
    :type duration: object
    :param target_format: format string naming the desired radix components
    :type target_format: object
    :param variable_map: mapping from component names to unit sizes
    :type variable_map: object
    :param format_variables: ordered names or mapping of components to unit sizes
    :type format_variables: object
    :return: formatted text
    :rtype: str
    """
    ...
duration_time_map = {'years': 31536000, 'days': 86400, 'hours': 3600, 'minutes': 60, 'seconds': 1}

def format_elapsed_time(duration, target_format='{hours:d}:{minutes:02d}:{seconds:02d}', format_variables=None):
    """
    **LLM Docstring**

    Convert a numeric or `timedelta` duration to seconds and format it through the configured year/day/hour/minute/second radix map.

    :param duration: value to decompose into radix units
    :type duration: object
    :param target_format: format string naming the desired radix components
    :type target_format: object
    :param format_variables: ordered names or mapping of components to unit sizes
    :type format_variables: object
    :return: formatted text
    :rtype: str
    """
    ...