"""
This lists the types of readers and things available to the QChemLogReader.

It parallels `MOLPROLogComponents`/`OrcaLogComponents`: each entry in the
`Components` table maps a name onto a `(tag_start, tag_end, parser, mode)` spec that
the `ElectronicStructureLogReader` machinery uses to pull a block out of a Q-Chem
output file and turn it into usable (usually `NumPy`-backed) data.
"""
import io

import numpy as np

from ....Parsers import *
from collections import namedtuple, OrderedDict

#TODO: speed these parsers up, they're just whatever unoptimized code Claude came up with

########################################################################################################################
#
#                                           QChemLogComponents
#
# region QChemLogComponents
Components = OrderedDict()  # we'll register on this bit by bit
# each registration should look like:

# Components["Name"] = {
#     "description" : string, # used for documenting what we have
#     "tag_start"   : start_tag, # starting delimiter for a block
#     "tag_end"     : end_tag, # ending delimiter for a block; None means apply the parser upon tag_start
#     "parser"      : parser, # function that'll parse the returned list of blocks ("List") or block ("Single")
#     "mode"        : mode # "List" or "Single"
# }


def strip_recursive(at_list):
    """
    Recursively strip whitespace (and leading integer labels) from every string in a
    nested list.

    :param at_list: the (possibly nested) list of strings
    :type at_list: list
    :return: the cleaned list
    :rtype: list
    """
    return [
        Integer.remove(s.strip()) if isinstance(s, str) else strip_recursive(s)
        for s in at_list
    ]


########################################################################################################################
#
#                                           CartesianCoordinates
#
# region CartesianCoordinates

# Q-Chem prints geometries in a couple of nearly-identical layouts. Both start with a
# leading integer index, an atom label, and three Cartesian coordinates, e.g.
#
#              Standard Nuclear Orientation (Angstroms)
#     I     Atom           X                Y                Z
#  ----------------------------------------------------------------
#     1      C      -3.5692268380    -0.8935995770     0.1683542339
#     ...
#  ----------------------------------------------------------------
#
# so we can share a single row parser between them.

# A coordinate row is `<index> <atom-label> <x> <y> <z>`. Q-Chem prints these blocks with
# a variety of headers, footers, and trailing lines (basis info, multipole fields, ...),
# so rather than a start-anchored combinator we scan each block for the rows that match.
import re as _re

_coord_row_re = _re.compile(
    r"^\s*\d+\s+([A-Za-z]{1,3})\s+"
    r"(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$"
)

QChemCoords = namedtuple("QChemCoords", ["atoms", "coords"])


def _parse_one_geometry(block):
    """
    Parse a single Q-Chem geometry block into `(atoms, coords)`.

    :param block: the matched block text (one geometry)
    :type block: str
    :return: `(atoms, coords)` with `coords` shaped `(n_atoms, 3)`
    :rtype: tuple[list[str], np.ndarray]
    """
    atoms = []
    coords = []
    for line in block.split("\n"):
        m = _coord_row_re.match(line)
        if m is not None:
            atoms.append(m.group(1))
            coords.append([float(m.group(2)), float(m.group(3)), float(m.group(4))])
    return atoms, np.array(coords, dtype=float)


def _parse_cartesian_blocks(strs):
    """
    Shared helper: parse one-or-more Q-Chem coordinate blocks into `(atoms, coords)`.

    When every geometry has the same atom ordering (the common case) `coords` is returned
    as a single `(n_geometries, n_atoms, 3)` array and `atoms` as the shared atom list;
    otherwise both are returned as per-geometry lists.

    :param strs: the matched block string(s)
    :type strs: list[str]
    :return: the parsed `(atoms, coordinates)`
    :rtype: QChemCoords
    """
    if isinstance(strs, str):
        strs = [strs]

    all_atoms = []
    all_coords = []
    for block in strs:
        atoms, coords = _parse_one_geometry(block)
        if len(atoms) == 0:
            continue
        all_atoms.append(atoms)
        all_coords.append(coords)

    if len(all_coords) == 0:
        return QChemCoords([], np.zeros((0, 3)))

    shapes = {c.shape for c in all_coords}
    same_atoms = all(a == all_atoms[0] for a in all_atoms)
    if len(shapes) == 1 and same_atoms:
        return QChemCoords(all_atoms[0], np.array(all_coords))
    return QChemCoords(all_atoms, all_coords)


# --- Standard Nuclear Orientation (printed for every SCF that runs) --------------------
# We deliberately keep the tags simple: the title as the start delimiter and the blank
# line that follows the geometry (after the trailing `Nuclear Repulsion`/basis lines) as
# the end delimiter. The row parser only matches `<int> <atom> <x> <y> <z>` lines, so the
# `I Atom X Y Z` header and the trailing non-coordinate lines are ignored automatically.
# (Anchoring on the dashed separators is fragile because Q-Chem prints dashed lines of
# several different lengths throughout the file.)
cartesian_start_tag = FileStreamerTag("Standard Nuclear Orientation (Angstroms)")
cartesian_end_tag = "\n\n"


def cartesian_coordinates_parser(strs):
    """
    Parse Q-Chem "Standard Nuclear Orientation" blocks into atom labels and
    coordinates.

    :param strs: the matched block string(s)
    :type strs: list[str]
    :return: the parsed `(atoms, coordinates)`
    :rtype: QChemCoords
    """
    return _parse_cartesian_blocks(strs)


Components["CartesianCoordinates"] = {
    "description": "the `Standard Nuclear Orientation (Angstroms)` geometry blocks",
    "tag_start": cartesian_start_tag,
    "tag_end": cartesian_end_tag,
    "parser": cartesian_coordinates_parser,
    "mode": "List"
}

# --- Optimizer geometries (printed once per optimization cycle) ------------------------
opt_cartesian_start_tag = FileStreamerTag("Coordinates (Angstroms)")
opt_cartesian_end_tag = "Point Group"

Components["OptimizationCoordinates"] = {
    "description": "the per-cycle `Coordinates (Angstroms)` geometry blocks from the optimizer",
    "tag_start": opt_cartesian_start_tag,
    "tag_end": opt_cartesian_end_tag,
    "parser": cartesian_coordinates_parser,
    "mode": "List"
}
# endregion


########################################################################################################################
#
#                                           Energies
#
# region Energies

def _single_number_parser(block):
    """
    Pull the (last) floating point number out of a one-line-ish block.

    :param block: the matched block text
    :type block: str
    :return: the parsed number
    :rtype: float
    """
    if block is None:
        return None
    nums = Number.findall(block)
    if len(nums) == 0:
        return None
    return float(nums[-1])


def _number_list_parser(blocks):
    """
    Collapse a list of one-number blocks into a flat `np.ndarray`.

    :param blocks: the matched blocks
    :type blocks: list[str]
    :return: the parsed values
    :rtype: np.ndarray
    """
    return np.array([_single_number_parser(b) for b in blocks], dtype=float)


# `Total energy = -696.88973077` (one per converged SCF)
Components["SCFEnergies"] = {
    "description": "the converged `Total energy =` values (one per SCF)",
    "tag_start": FileStreamerTag("Total energy ="),
    "tag_end": "\n",
    "parser": _number_list_parser,
    "mode": "List"
}

# `SCF   energy = -696.88973077`
Components["SCFEnergiesRaw"] = {
    "description": "the `SCF   energy =` values (one per SCF)",
    "tag_start": FileStreamerTag("SCF   energy ="),
    "tag_end": "\n",
    "parser": _number_list_parser,
    "mode": "List"
}

# `Nuclear Repulsion Energy = 1023.29506433 hartrees`
Components["NuclearRepulsionEnergies"] = {
    "description": "the `Nuclear Repulsion Energy =` values",
    "tag_start": FileStreamerTag("Nuclear Repulsion Energy ="),
    "tag_end": "hartrees",
    "parser": _number_list_parser,
    "mode": "List"
}

# `Energy is   -696.827632946` (printed each optimizer step)
Components["OptimizationEnergies"] = {
    "description": "the per-step optimizer `Energy is` values",
    "tag_start": FileStreamerTag("Energy is"),
    "tag_end": "\n",
    "parser": _number_list_parser,
    "mode": "List"
}

# `Final energy is -696.785079267623`
Components["FinalEnergy"] = {
    "description": "the `Final energy is` value at the end of an optimization",
    "tag_start": FileStreamerTag("Final energy is"),
    "tag_end": "\n",
    "parser": _single_number_parser,
    "mode": "Single"
}
# endregion


########################################################################################################################
#
#                                           Gradients
#
# region Gradients

def gradient_parser(strs):
    """
    Parse Q-Chem `Gradient of SCF Energy` blocks.

    Q-Chem prints the gradient transposed and in column-blocks of (up to) six atoms:
    a header row of atom indices, then three rows (x, y, z). We stitch the column
    blocks back together and transpose to `(n_atoms, 3)`.

    :param strs: the matched block string(s)
    :type strs: list[str]
    :return: a list of `(n_atoms, 3)` gradient arrays (one per block)
    :rtype: list[np.ndarray]
    """
    if isinstance(strs, str):
        strs = [strs]
    grads = []
    for s in strs:
        col_blocks = []
        for chunk in s.strip().split("\n"):
            toks = chunk.split()
            if len(toks) == 0:
                continue
            # a data row starts with the component index 1/2/3 then floats;
            # a header row is all integers (atom indices)
            try:
                nums = [float(t) for t in toks]
            except ValueError:
                continue
            is_header = all(float(t).is_integer() for t in toks)
            if is_header:
                col_blocks.append([])
            else:
                if len(col_blocks) == 0:
                    col_blocks.append([])
                col_blocks[-1].append(nums[1:])  # drop the 1/2/3 row label
        # each col_block is 3 rows x k atoms -> stack cols across blocks -> (3, natoms)
        mat = np.concatenate([np.array(b) for b in col_blocks if len(b)], axis=1)
        grads.append(mat.T)  # -> (natoms, 3)
    return grads


Components["Gradients"] = {
    "description": "the `Gradient of SCF Energy` blocks, reshaped to `(n_atoms, 3)`",
    "tag_start": FileStreamerTag("Gradient of SCF Energy"),
    "tag_end": "Max gradient component",
    "parser": gradient_parser,
    "mode": "List"
}
# endregion


########################################################################################################################
#
#                                           DipoleMoments
#
# region DipoleMoments

QChemDipole = namedtuple("QChemDipole", ["xyz", "total"])


def dipole_parser(strs):
    """
    Parse Q-Chem `Dipole Moment (Debye)` blocks.

    The block looks like::

            Dipole Moment (Debye)
                 X      -2.7868      Y       0.7232      Z       0.7829
               Tot       2.9837

    :param strs: the matched block string(s)
    :type strs: list[str]
    :return: a list of `(xyz, total)` dipole records (one per block)
    :rtype: list[QChemDipole]
    """
    if isinstance(strs, str):
        strs = [strs]
    dips = []
    for s in strs:
        nums = np.array(Number.findall(s)).astype(float)
        # first three are X, Y, Z; fourth is Tot
        dips.append(QChemDipole(nums[:3], float(nums[3])))
    return dips


Components["DipoleMoments"] = {
    "description": "the `Dipole Moment (Debye)` blocks",
    "tag_start": FileStreamerTag("Dipole Moment (Debye)"),
    "tag_end": "Quadrupole Moments",
    "parser": dipole_parser,
    "mode": "List"
}
# endregion


########################################################################################################################
#
#                                           MullikenCharges
#
# region MullikenCharges

QChemMulliken = namedtuple("QChemMulliken", ["atoms", "charges"])


def mulliken_parser(strs):
    """
    Parse Q-Chem `Ground-State Mulliken Net Atomic Charges` blocks into atom labels
    and charges.

    :param strs: the matched block string(s)
    :type strs: list[str]
    :return: a list of `(atoms, charges)` records (one per block)
    :rtype: list[QChemMulliken]
    """
    if isinstance(strs, str):
        strs = [strs]
    out = []
    for s in strs:
        atoms = []
        charges = []
        for line in s.split("\n"):
            toks = line.split()
            # data rows look like: `1 C  -0.120508`
            if len(toks) == 3 and toks[0].lstrip("-").isdigit():
                try:
                    charges.append(float(toks[2]))
                except ValueError:
                    continue
                atoms.append(toks[1])
        out.append(QChemMulliken(atoms, np.array(charges, dtype=float)))
    return out


Components["MullikenCharges"] = {
    "description": "the `Ground-State Mulliken Net Atomic Charges` blocks",
    "tag_start": FileStreamerTag("Ground-State Mulliken Net Atomic Charges"),
    "tag_end": "Sum of atomic charges",
    "parser": mulliken_parser,
    "mode": "List"
}
# endregion


########################################################################################################################
#
#                                           Header / job info
#
# region Header

QChemHeader = namedtuple("QChemHeader", ["version", "method", "basis", "input"])


def header_parser(block):
    """
    Parse the leading portion of a Q-Chem run for the version, the user `$rem`/method
    and basis settings, and the raw echoed input.

    :param block: the matched block text (from the start of the file)
    :type block: str
    :return: the parsed header record
    :rtype: QChemHeader
    """
    if block is None:
        return None

    version = None
    for line in block.split("\n"):
        low = line.lower()
        if "q-chem version" in low:
            version = line.split(":")[-1].strip()
            break

    method = None
    basis = None
    for line in block.split("\n"):
        toks = line.split()
        if len(toks) >= 2:
            key = toks[0].upper()
            if key == "METHOD":
                method = toks[1]
            elif key == "BASIS":
                basis = toks[1]
    if basis is None:
        # fall back to the `Requested basis set is def2-SVP` line
        for line in block.split("\n"):
            if "Requested basis set is" in line:
                basis = line.split("is")[-1].strip()
                break

    return QChemHeader(version, method, basis, block)


Components["Header"] = {
    "description": "the version / method / basis / echoed-input header block",
    "tag_start": None,
    "tag_end": "Standard Nuclear Orientation",
    "parser": header_parser,
    "mode": "Single"
}


def input_parser(block):
    """
    Return the echoed `User input:` section (the `$molecule`/`$rem`/... blocks) as
    text.

    :param block: the matched block text
    :type block: str
    :return: the input text
    :rtype: str
    """
    return None if block is None else block.strip()


Components["InputSection"] = {
    "description": "the echoed `User input:` section",
    "tag_start": FileStreamerTag("User input:"),
    "tag_end": "Standard Nuclear Orientation",
    "parser": input_parser,
    "mode": "Single"
}


def job_time_parser(blocks):
    """
    Parse the wall/CPU seconds out of each `Total job time:` line.

    :param blocks: the matched blocks
    :type blocks: list[str]
    :return: a `(n_jobs, 2)` array of `(wall, cpu)` seconds
    :rtype: np.ndarray
    """
    out = []
    for b in blocks:
        nums = np.array(Number.findall(b)).astype(float)
        out.append(nums[:2])  # wall, cpu
    return np.array(out, dtype=float)


Components["JobTimes"] = {
    "description": "the `Total job time:` wall/cpu seconds",
    "tag_start": FileStreamerTag("Total job time:"),
    "tag_end": "\n",
    "parser": job_time_parser,
    "mode": "List"
}
# endregion


########################################################################################################################
#
#                                           VibrationalFrequencies
#
# region VibrationalFrequencies
# NOTE: the attached file is an FSM + TS-optimization job and contains no
# `VIBRATIONAL ANALYSIS` section, so this component is written to Q-Chem's standard
# frequency-printout layout but is *not* exercised by that particular file.

QChemFrequencies = namedtuple("QChemFrequencies", ["freqs", "ir_intensities", "modes"])


def frequency_parser(block):
    """
    Parse a Q-Chem `VIBRATIONAL ANALYSIS` section.

    Q-Chem prints frequencies in column-blocks of three modes with a `Frequency:` row,
    an `IR Inten:` row, and then per-atom `X Y Z` displacement rows headed by
    `X      Y      Z`. This collects the frequencies, IR intensities, and (when
    present) the displacement vectors.

    :param block: the matched section text
    :type block: str
    :return: the parsed `(freqs, ir_intensities, modes)`
    :rtype: QChemFrequencies
    """
    if block is None:
        return None

    freqs = []
    ir = []
    mode_cols = []  # list of (3 x k) displacement arrays, k modes per block

    current_disp = None  # rows of [x1 y1 z1 x2 y2 z2 ...]
    for line in block.split("\n"):
        stripped = line.strip()
        if stripped.startswith("Frequency:"):
            freqs.extend(float(x) for x in Number.findall(stripped))
            if current_disp is not None and len(current_disp):
                mode_cols.append(np.array(current_disp))
            current_disp = []
        elif stripped.startswith("IR Inten:"):
            ir.extend(float(x) for x in Number.findall(stripped))
        else:
            toks = stripped.split()
            # displacement rows: atom-label followed by 3*k floats
            if len(toks) >= 4 and current_disp is not None:
                try:
                    vals = [float(t) for t in toks[1:]]
                except ValueError:
                    continue
                if len(vals) % 3 == 0 and len(vals) > 0:
                    current_disp.append(vals)
    if current_disp is not None and len(current_disp):
        mode_cols.append(np.array(current_disp))

    modes = None
    if len(mode_cols):
        # each block: (n_atoms, 3*k) -> split into k modes of (n_atoms, 3)
        all_modes = []
        for block_arr in mode_cols:
            k = block_arr.shape[1] // 3
            for m in range(k):
                all_modes.append(block_arr[:, 3 * m:3 * (m + 1)])
        modes = np.array(all_modes)  # (n_modes, n_atoms, 3)

    return QChemFrequencies(
        np.array(freqs, dtype=float),
        np.array(ir, dtype=float),
        modes
    )


Components["VibrationalFrequencies"] = {
    "description": "the `VIBRATIONAL ANALYSIS` frequencies / IR intensities / normal modes",
    "tag_start": FileStreamerTag("VIBRATIONAL ANALYSIS"),
    "tag_end": "STANDARD THERMODYNAMIC QUANTITIES",
    "parser": frequency_parser,
    "mode": "Single"
}
# endregion


########################################################################################################################
#
#                                           Defaults
#
# region Defaults
Defaults = (
    "Header",
    "CartesianCoordinates",
    "SCFEnergies"
)
# endregion


########################################################################################################################
#
#                                           Ordering
#
# region Ordering
# defines the ordering in the log file
glk = (  # this must be sorted by what appears when
    "Header",
    "InputSection",
    "FinalEnergy",
    "VibrationalFrequencies"
)
list_type = {k: -1 for k in Components if Components[k]["mode"] == "List"}
Ordering = {k: i for i, k in enumerate([k for k in glk if k not in list_type])}
Ordering.update(list_type)
del glk
del list_type
# endregion

__components__ = Components
__ordering__ = Ordering
__defaults__ = Defaults
