import enum
import numpy as np
__all__ = ['RotorTypes', 'identify_rotor_type']

class RotorTypes(enum.Enum):
    """Real access pattern: RotorTypes.<MemberName> (this is an enum with 7 members, e.g. RotorTypes.Atom == 'atom'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:"""
    _MEMBERS = {'Atom': 'atom', 'Linear': 'linear', 'Planar': 'planar', 'Oblate': 'oblate', 'Prolate': 'prolate', 'Spherical': 'spherical', 'Asymmetric': 'asymmetric'}

def identify_rotor_type(moms: np.ndarray, tol=1e-08, zero_tol=1e-06):
    """
    **LLM Docstring**

    Classify principal moments as atomic, linear, spherical, oblate, prolate, or asymmetric and independently test the planar moment relation.

    :param moms: Value used as `moms` by the implementation.
    :type moms: np.ndarray
    :param tol: Numerical tolerance used for geometric or equality tests. Defaults to `1e-08`.
    :type tol: object
    :param zero_tol: Value used as `zero_tol` by the implementation. Defaults to `1e-06`.
    :type zero_tol: object
    :return: A pair of rotor type and planar flag.
    :rtype: tuple[RotorTypes, bool]
    """
    ...