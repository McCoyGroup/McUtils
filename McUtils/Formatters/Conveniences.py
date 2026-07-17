
import numpy as np
import string
from .TableFormatters import TableFormatter

__all__ = [
    "format_tensor_element_table",
    "format_symmetric_tensor_elements",
    "format_mode_labels",
    "format_zmatrix",
    "format_state_vector_frequency_table",
    "format_radix_value",
    "format_elapsed_time"
]

def format_tensor_element_table(inds, vals,
                                headers=("Indices", "Value"),
                                format="{:8.3f}",
                                column_join="|",
                                index_format="{:>5.0f}",
                                **etc
                                ):
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
    if isinstance(column_join, str):
        column_join = (" ", column_join)
    vals = np.asanyarray(vals)
    if vals.ndim == 1:
        vals = vals[:, np.newaxis]
    spans = [len(inds), vals.shape[-1]]
    return TableFormatter(
        column_formats=[index_format] * spans[0] + (
            [format] * spans[1]
                if isinstance(format, str) else
            format
        ),
        headers=headers,
        header_spans=spans,
        column_join=(
            [column_join[0]] * (spans[0]-1)
            + [column_join[1]]
            + [column_join[0]] * (vals.shape[-1]-1)
        ),
        **etc
    ).format(np.concatenate([np.array(inds).T, vals], axis=1))

def format_symmetric_tensor_elements(
        tensor,
        symmetries=None,
        cutoff=1e-6,
        headers=("Indices", "Value"),
        allowed_indices=None,
        filter=None,
        format="{:12.3f}",
        **etc
):
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
    tensor = np.asanyarray(tensor)
    if symmetries is None:
        symmetries = [np.arange(tensor.ndim)]

    symmetries = [np.sort(s) for s in symmetries]

    inds = np.where(np.abs(tensor) >= cutoff)
    if len(symmetries) > 0:
        inds_tests = [
            np.all(np.diff([inds[i] for i in symm], axis=0) >= 0, axis=0)
            for symm in symmetries
        ]
        inds_mask = np.all(inds_tests, axis=0)
        inds = tuple(x[inds_mask] for x in inds)

    if allowed_indices is not None:
        mask = np.full(len(inds[0]), True)
        for a,x in zip(allowed_indices, inds):
            if a is None: continue
            mask = mask & np.in1d(x, a)
        inds = tuple(x[mask] for x in inds)

    if filter is not None:
        mask = filter(inds)
        inds = tuple(x[mask] for x in inds)

    vals = tensor[inds]

    return format_tensor_element_table(inds, vals, headers=headers, format=format, **etc)

def format_mode_labels(labels,
                       freqs=None,
                       high_to_low=True,
                       mode_index_format="{:.0f}",
                       frequency_format="{:.0f}",
                       headers=None,
                       column_join=" | ",
                       none_tag="mixed",
                       **etc
                       ):
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
    labels = [
        none_tag
            if lab.type is None else
        " ".join(t for t in lab.type if t is not None)
        for lab in labels
    ]

    if freqs is not None:
        return TableFormatter(
            [mode_index_format, frequency_format, "{}"],
            headers=("Mode", "Frequency", "Label") if headers is None else headers,
            column_join=column_join,
            **etc
        ).format([
            [i+1, f, lab]
            for i,(f,lab) in enumerate(zip(
                reversed(freqs) if high_to_low else freqs,
                reversed(labels) if high_to_low else labels
            ))
        ])
    else:
        return TableFormatter(
            [mode_index_format, "{}"],
            headers=("Mode", "Label") if headers is None else headers,
            column_join=column_join,
            **etc
        ).format([
            [i + 1, lab]
            for i, lab in enumerate(
                reversed(labels) if high_to_low else labels
            )
        ])

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
    max_ind = int(np.log10(max([max(z) for z in zm]))) + 2
    formatter = TableFormatter(
        f"{{:>{max_ind}.0f}}",
        column_join=", " if list_form else " ",
        row_padding=" [" if list_form else "",
        row_join="],\n" if list_form else "\n"
    )
    if not preserve_embedding:
        if isinstance(zm, np.ndarray):
            zm = zm.tolist()
        else:
            zm = [list(z) for z in zm]
        if len(zm[0]) == 4:
            zm[0][1] = ""
            zm[0][2] = ""
            zm[0][3] = ""

            zm[1][2] = ""
            zm[1][3] = ""

            zm[2][3] = ""
        else:
            zm[0][1] = ""
            zm[0][2] = ""

            zm[1][2] = ""

    if not preserve_indices:
        if len(zm[0]) == 4:
            zm = [z[1:] for z in zm[1:]]

    base = formatter.format(zm)
    if list_form:
        base = "[" + base[1:] + "]]"

    return base

def format_state_vector_frequency_table(state_list, freq_data,
                                        state_header="State",
                                        freq_header="Freq.",
                                        freq_fmt='{:.3f}',
                                        sep=" | ",
                                        join=" ",
                                        ):
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
    state_cols = (
            len(state_list[0])
                if not isinstance(state_list[0], str) else
            1
    )
    freq_data = np.asanyarray(freq_data)
    if freq_data.ndim == 1:
        freq_data = freq_data[:, np.newaxis]
    freq_cols = freq_data.shape[-1]
    if isinstance(freq_fmt, str):
        freq_fmt = [freq_fmt] * freq_cols
    else:
        freq_fmt = list(freq_fmt) * freq_cols
        freq_fmt = freq_fmt[:freq_cols]

    if isinstance(freq_header, str):
        freq_header = [freq_header] * freq_cols
    else:
        freq_header = list(freq_header) * freq_cols
        freq_header = freq_header[:freq_cols]

    formatter = TableFormatter(
        [""] * state_cols + freq_fmt,
        headers=[state_header] + freq_header,
        header_spans=[state_cols] + [1] * freq_cols,
        column_join=[" "] * (state_cols - 1) + [sep] + [join] * (freq_cols - 1)
    )
    return formatter.format(
        [list(x) + v for x, v in zip(state_list, freq_data.tolist())]
            if not isinstance(state_list[0], str) else
        [[x] + v for x, v in zip(state_list, freq_data.tolist())]
    )

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
    if format_variables is None:
        format_variables = [field
                for _, field, _, _ in string.Formatter().parse(target_format)
                if field is not None]
    if not isinstance(format_variables, dict):
        format_variables = {
            k:variable_map[k]
            for k in format_variables
        }

    opts = {}
    for k,v in format_variables.items():
        opts[k] = duration//v
        duration = duration%v
    opts['remainder'] = duration

    return target_format.format(**opts)

duration_time_map = {'years':31536000, 'days':86400, 'hours':3600, 'minutes':60, 'seconds':1}
def format_elapsed_time(duration,
                        target_format="{hours:d}:{minutes:02d}:{seconds:02d}",
                        format_variables=None):
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
    if hasattr(duration, 'total_seconds'):
        duration = duration.total_seconds()
    return format_radix_value(duration, target_format, duration_time_map, format_variables=format_variables)