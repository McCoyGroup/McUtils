"""Implements calculation of Euler angles, Euler matrices, etc

"""
import numpy as np
__all__ = ['euler_angles', 'euler_matrix']

def zyz_mat(c, s):
    ...

def zyz_angles(basis):
    ...

def xyz_mat(c, s):
    ...

def xyz_angles(basis):
    ...

def xzy_mat(c, s):
    ...

def xzy_angles(basis):
    ...

def zyx_mat(c, s):
    ...

def zyx_angles(basis):
    ...
euler_mat_map = {'zyz': zyz_mat, 'xyz': xyz_mat, 'zyx': zyx_mat}

def euler_matrix(angles, ordering='xyz'):
    """Returns the Euler matrix for the specified angles

    :param angles:
    :type angles:
    :param ordering: the order in which the rotations should be performed
    :type ordering:
    """
    ...
euler_ang_map = {'zyz': zyz_angles, 'xyz': xyz_angles, 'zyx': zyx_angles}

def euler_angles(basis, ordering='xyz'):
    """Calculates the Euler angles for the basis

    :param basis: the basis to get the Euler angles for
    :type basis: np.ndarray
    """
    ...