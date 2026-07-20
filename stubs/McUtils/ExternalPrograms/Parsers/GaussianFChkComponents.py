"""Defines components of an .fchk file that are already known and parseable"""
from .FChkDerivatives import *
import numpy as np
FormattedCheckpointComponents = {}

def get_names(atom_ints, reader=None):
    ...
FormattedCheckpointComponents['Int Atom Types'] = get_names

def reformat(coords, reader=None):
    ...
FormattedCheckpointComponents['Current cartesian coordinates'] = reformat
FormattedCheckpointComponents['Cartesian Force Constants'] = FchkForceConstants
FormattedCheckpointComponents['Cartesian 3rd/4th derivatives'] = FchkForceDerivatives
FormattedCheckpointComponents['Dipole Derivatives'] = FchkDipoleDerivatives
FormattedCheckpointComponents['Dipole Moment num derivs'] = FchkDipoleNumDerivatives
FormattedCheckpointComponents['Dipole Derivatives num derivs'] = FchkDipoleHigherDerivatives

def parse_pol(pol_array, tril=np.tril_indices(3), reader=None):
    ...
FormattedCheckpointComponents['Polarizability'] = parse_pol

def parse_hyper_pol(pol_array, tril=np.tril_indices(3), reader=None):
    ...
FormattedCheckpointComponents['HyperPolarizability'] = parse_pol

def parse_pol_derivs(pol_array, tril=np.tril_indices(3), reader=None):
    ...
FormattedCheckpointComponents['Polarizability Derivatives'] = parse_pol_derivs

def parse_pol_num_derivs(pol_array, tril=np.tril_indices(3), reader=None):
    ...
FormattedCheckpointComponents['Polarizability num derivs'] = parse_pol_num_derivs

def split_vib_modes(mcoeffs, reader=None):
    """Pulls the mode vectors from the coeffs
    There should be 3N-6 modes where each vector is 3N long so N = (1 + sqrt(1 + l/9))

    :param mcoeffs:
    :type mcoeffs:
    :return:
    :rtype:
    """
    ...
FormattedCheckpointComponents['Vib-Modes'] = split_vib_modes

def split_vib_e2(e2, reader=None):
    """Pulls the vibrational data out of the file

    :param e2:
    :type e2:
    :return:
    :rtype:
    """
    ...
FormattedCheckpointComponents['Vib-E2'] = split_vib_e2
"FormattedCheckpointCommonNames data omitted from this build (13 keys: ['Atomic numbers', 'Current cartesian coordinates', 'Cartesian Gradient', 'Cartesian Force Constants', 'Cartesian 3rd/4th derivatives', 'Dipole Moment', 'Dipole Derivatives', 'Dipole Moment num derivs', 'Dipole Derivatives num derivs', 'Vib-E2', 'Vib-Modes', 'Vib-AtMass', 'Real atomic weights'])"