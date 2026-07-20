"""
This lists the types of readers and things available to the GaussianLogReader
"""
import io
import numpy as np
from ...Parsers import *
from collections import namedtuple, OrderedDict
GaussianLogComponents = OrderedDict()
tag_start = '******************************************'
tag_end = FileStreamerTag(' --------', follow_ups=(' -----',))
HeaderHashBlockLineParser = StringParser(HeaderHashBlockLine)

def header_parser(header):
    ...
mode = 'Single'
GaussianLogComponents['Header'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': header_parser, 'mode': mode}
tag_start = 'Z-matrix:'
tag_end = ' \n'

def parser(zmat):
    ...
mode = 'Single'
GaussianLogComponents['InputZMatrix'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parser, 'mode': mode}
cart_delim = ' --------------------------------------------------------------'
cartesian_start_tag = FileStreamerTag('Center     Atomic      Atomic             Coordinates (Angstroms)', follow_ups=cart_delim)
cartesian_end_tag = cart_delim
label_pattern = RegexPattern([' ', Integer, ' '])

def cartesian_coordinates_parser(strs, label_pattern=label_pattern):
    ...

def header_cartesian_parser(carts):
    ...
GaussianLogComponents['HeaderCartesianCoordinates'] = {'tag_start': 'Symbolic Z-matrix:', 'tag_end': '\n\n', 'parser': header_cartesian_parser, 'mode': 'Single'}
tag_end = ' ---------------------------------------------------------------------'

def parser(strs):
    ...
mode = 'List'
GaussianLogComponents['ZMatrices'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parser, 'mode': mode}
tag_start = 'Optimization '
tag_end = '                        !\n ------------------------------------------------------------------------\n'

def parser(pars):
    """Parses a optimizatioon parameters block"""
    ...
mode = 'List'
GaussianLogComponents['OptimizationParameters'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parser, 'mode': mode}
tag_start = 'Mulliken charges:'
tag_end = 'Sum of Mulliken charges'

def parser(charges):
    """Parses a Mulliken charges block"""
    ...
mode = 'List'
GaussianLogComponents['MullikenCharges'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parser, 'mode': mode}
tag_start = 'Dipole moment ('
tag_end = ' N-N='

def parser(moms):
    """Parses a multipole moments block"""
    ...
mode = 'List'
GaussianLogComponents['MultipoleMoments'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parser, 'mode': mode}
tag_start = 'Dipole moment ('
tag_end = 'Quadrupole moment ('

def parser(moms):
    """Parses a multipole moments block"""
    ...
mode = 'List'
GaussianLogComponents['DipoleMoments'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parser, 'mode': mode}
tag_start = ' Dipole        ='
tag_end = ' Optimization'

def convert_D_number(a, **kw):
    ...
DNumberPattern = RegexPattern((Number, 'D', Integer), dtype=float)

def parser(mom):
    """Parses dipole block, but only saves the dipole of the optimized structure"""
    ...
mode = 'List'
parse_mode = 'Single'
GaussianLogComponents['OptimizedDipoleMoments'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parser, 'mode': mode, 'parse_mode': parse_mode}
tag_start = ' Summary of the potential surface scan:'
tag_end = 'Normal termination of'

def parser(block):
    """Parses the scan summary block"""
    ...
mode = 'Single'
GaussianLogComponents['ScanEnergies'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parser, 'mode': mode}
tag_start = ' Summary of Optimized Potential Surface Scan'
tag_end = FileStreamerTag(tag_alternatives=(' Largest change from initial coordinates is atom ', '-' * 25))
eigsPattern = RegexPattern(('Eigenvalues --', Repeating(Capturing(Number), suffix=Optional(Whitespace))), joiner=Whitespace)
eigsShift = RegexPattern(('add', Whitespace, Named(Number, 'Shift')), joiner=Whitespace)
EigsShiftPat = StringParser(eigsShift)

def parser(pars):
    """Parses the scan summary block and returns only the energies"""
    ...
mode = 'Single'
GaussianLogComponents['OptimizedScanEnergies'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parser, 'mode': mode}

def parse_scf_energies(energy_blocks):
    ...
GaussianLogComponents['SCFEnergies'] = {'tag_start': 'SCF Done:  E(', 'tag_end': ' A.U. ', 'parser': parse_scf_energies, 'mode': 'List'}
tag_start = FileStreamerTag('/l202.exe', follow_ups=('Standard orientation: ',))
tag_end = FileStreamerTag('SCF Done:  E(', follow_ups=(' A.U. ',))
SCFEnergyPattern = StringParser(RegexPattern(('SCF Done:  E\\(', Repeating(Any), '\\) =', Whitespace, Named(Number, 'energy'))))

def parse_scf_block_coordinate_energies(energy_blocks):
    ...
GaussianLogComponents['SCFCoordinatesEnergies'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parse_scf_block_coordinate_energies, 'mode': 'List'}
tag_start = FileStreamerTag('Total Anharmonic X Matrix (in cm^-1)', follow_ups=('-' * 25,))
tag_end = FileStreamerTag(tag_alternatives=(' ================================================== ', '-' * 25))

def parser(pars):
    """Parses the X matrix block and returns stuff --> huge pain in the ass function"""
    ...
mode = 'Single'
GaussianLogComponents['XMatrix'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parser, 'mode': mode}
tag_start = 'Job cpu time'
tag_end = 'Normal termination'

def parser(block, start=tag_start):
    ...
mode = 'Single'
GaussianLogComponents['Footer'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parser, 'mode': mode}
tag_start = 'FrcOut:'
tag_end = 'MW cartesian velocity:'
CartesianBlockTags = ['Cartesian coordinates: (bohr)', 'MW cartesian']

def parse_aimd_coords(blocks):
    ...
ValueBlockTags = ['FrcOut', FileStreamerTag('Final forces over variables', follow_ups=('Leave Link',))]

def convert_D_number(a, **kw):
    ...
DNumberPattern = RegexPattern((Number, 'D', Integer), dtype=float)
EnergyBlockPattern = StringParser(RegexPattern(('Energy=', Named(DNumberPattern, 'E', handler=convert_D_number))))
ForceBlockTags = ['force vector number 2', 'After rot']

def parse_grad(block):
    ...

def parse_weird_mat(pars):
    """Parses the Hessian matrix block and returns stuff --> huge pain in the ass function"""
    ...
HessianBlockTags = ['Force constants in Cartesian coordinates:', 'Final forces']

def convert_D_number_block(a, **kw):
    ...
DNumberPattern = RegexPattern((Number, 'D', Integer), dtype=float)

def parse_aimd_values_blocks(blocks):
    ...

def parser(blocks):
    ...
mode = 'List'
GaussianLogComponents['AIMDTrajectory'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parser, 'mode': mode}
force_block_tags = ('Forces (Hartrees/Bohr)', 'Cartesian Forces:')

def parse_force_list(strs):
    ...
mode = 'List'
GaussianLogComponents['Gradients'] = {'tag_start': force_block_tags[0], 'tag_end': force_block_tags[1], 'parser': parse_force_list, 'mode': mode}

def parse_hessian_list(hessias):
    ...
mode = 'List'
GaussianLogComponents['Hessians'] = {'tag_start': HessianBlockTags[0], 'tag_end': HessianBlockTags[1], 'parser': parse_hessian_list, 'mode': mode}
cubic_block_tags = ('Final third derivatives:', 'Diagonal')
label_pattern = RegexPattern([' ', PositiveInteger, ' '])

def parse_cubic_mat(pars, label_pattern=label_pattern):
    """Parses the Hessian matrix block and returns stuff --> huge pain in the ass function"""
    ...

def parse_cubics_list(hessias):
    ...
mode = 'List'
GaussianLogComponents['CubicDerivs'] = {'tag_start': cubic_block_tags[0], 'tag_end': cubic_block_tags[1], 'parser': parse_cubics_list, 'mode': mode}
quartic_block_tags = ('nuclear 4th derivatives', 'Numerical')

def parse_quartics_list(hessias):
    ...
mode = 'List'
GaussianLogComponents['QuarticDerivs'] = {'tag_start': quartic_block_tags[0], 'tag_end': quartic_block_tags[1], 'parser': parse_quartics_list, 'mode': mode}
tag_start = 'Harmonic frequencies (cm**-1)'
tag_end = '\n\n'

def parse_nms_modes(label, symmetries, freqs, masses, fcs, ir_ints, _, disps):
    ...

def parse_nms_block(block):
    ...

def parse(blocks):
    ...
mode = 'List'
GaussianLogComponents['NormalModes'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parse, 'mode': mode}
tag_start = 'Excitation energies and oscillator strengths:'
tag_end = 'SavETr:'

def parse_excited_states(blocks: str):
    ...
mode = 'Single'
GaussianLogComponents['ExcitedStates'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parse_excited_states, 'mode': mode}
tag_start = 'Zeta(I,J)'
tag_end = 'Num. of Coriolis'

def parse_coriolis(blocks):
    ...
mode = 'Single'
GaussianLogComponents['CoriolisTerms'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parse_coriolis, 'mode': mode}
tag_start = 'K(I,J)'
tag_end = 'Num. of 2nd derivatives'

def parse_quadratics(blocks):
    ...
mode = 'Single'
GaussianLogComponents['QuadraticTerms'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parse_quadratics, 'mode': mode}
tag_start = 'K(I,J,K)'
tag_end = 'Num. of 3rd derivatives'

def parse_cubics(blocks):
    ...
mode = 'Single'
GaussianLogComponents['CubicTerms'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parse_cubics, 'mode': mode}
tag_start = 'K(I,J,K,L)'
tag_end = 'Num. of 4th derivatives'

def parse_quartics(blocks):
    ...
mode = 'Single'
GaussianLogComponents['QuarticTerms'] = {'tag_start': tag_start, 'tag_end': tag_end, 'parser': parse_quartics, 'mode': mode}
tag_start = '1\\'
tag_end = FileStreamerTag(('\\\\@', '\\\n \\@', '\\\\\n @'))

def skip_report_header(stuff):
    ...
num_pattern = Alternatives([Integer, Number, IntBaseNumber, (Number, 'e', Integer)])
scan_spec = namedtuple('scan_spec', ['value', 'steps', 'amount'])

def parse_reports(blocks, endline_pattern=RegexPattern([Newline, Whitespace]), num_pattern=num_pattern, numblock_pattern=Repeating(num_pattern, suffix=Optional(','))):
    ...

def tag_validator(block):
    ...
mode = 'List'
GaussianLogComponents['Reports'] = {'tag_start': tag_start, 'tag_end': tag_end, 'validator': tag_validator, 'parser': parse_reports, 'mode': mode}
GaussianLogDefaults = ('StartDateTime', 'InputZMatrix', 'ScanTable', 'Blurb', 'ComputerTimeElapsed', 'EndDateTime')
"glk data omitted from this build (22 items: ['Header', 'StartDateTime', 'CartesianCoordinates', 'ZMatCartesianCoordinates', 'StandardCartesianCoordinates', 'CartesianCoordinateVectors', 'MullikenCharges', 'MultipoleMoments', 'DipoleMoments', 'OptimizedDipoleMoments', 'QuadrupoleMoments', 'OctapoleMoments', 'HexadecapoleMoments', 'IntermediateEnergies', 'InputZMatrix', 'InputZMatrixVariables', 'ZMatrices', 'ScanEnergies', 'OptimizedScanEnergies', 'OptimizationScan', 'Blurb', 'Footer'])"
list_type = {k: -1 for k in GaussianLogComponents if GaussianLogComponents[k]['mode'] == 'List'}
GaussianLogOrdering = {k: i for i, k in enumerate([k for k in glk if k not in list_type])}