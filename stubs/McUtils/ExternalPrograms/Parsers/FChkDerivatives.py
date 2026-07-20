"""
Lazy class for holding force constants and higher derivative tensors pulled from the Gaussian log file
"""
import numpy as np
from ...Numputils import SparseArray
__all__ = ['FchkForceConstants', 'FchkForceDerivatives', 'FchkDipoleDerivatives', 'FchkDipoleHigherDerivatives', 'FchkDipoleNumDerivatives']

class FchkForceConstants:
    """
    Holder class for force constants coming out of an fchk file.
    Allows us to construct the force constant matrix in lazy fashion if we want.
    """

    def __init__(self, fcs, num_atoms=None, reader=None):
        """
        **LLM Docstring**

        Hold the flattened force-constant (lower-triangle) data, optionally with the atom
        count (or a reader that can supply it).

        :param fcs: the flattened lower-triangle force constants
        :type fcs: np.ndarray
        :param num_atoms: the number of atoms (inferred lazily if omitted)
        :type num_atoms: int | None
        :param reader: a reader from which to pull the atom count
        :type reader: object | None
        """
        ...

    def __len__(self):
        """
        **LLM Docstring**

        The length of the raw flattened force-constant data.

        :return: the number of stored values
        :rtype: int
        """
        ...

    def _get_n(self):
        """
        :return:
        :rtype: int
        """
        ...

    @property
    def n(self):
        """
        **LLM Docstring**

        The number of atoms, inferred from the data length if not supplied.

        :return: the atom count
        :rtype: int
        """
        ...

    @property
    def shape(self):
        """
        **LLM Docstring**

        The shape of the full force-constant matrix, `(3n, 3n)`.

        :return: the matrix shape
        :rtype: tuple[int, int]
        """
        ...

    def _get_array(self):
        """Uses the computed n to make and symmetrize an appropriately formatted array from the lower-triangle data
        :return:
        :rtype: np.ndarray
        """
        ...

    @property
    def array(self):
        """
        **LLM Docstring**

        The full, symmetrized `(3n, 3n)` force-constant matrix reconstructed from the
        lower-triangle data.

        :return: the force-constant matrix
        :rtype: np.ndarray
        """
        ...

class FchkForceDerivatives:
    """Holder class for force constant derivatives coming out of an fchk file"""

    def __init__(self, derivs, num_atoms=None, num_modes=None, reader=None):
        """
        **LLM Docstring**

        Hold the flattened third/fourth force-constant derivative data, optionally with
        the atom and mode counts (or a reader supplying the atom count).

        :param derivs: the flattened derivative data
        :type derivs: np.ndarray
        :param num_atoms: the number of atoms (inferred lazily if omitted)
        :type num_atoms: int | None
        :param num_modes: the number of modes (inferred lazily if omitted)
        :type num_modes: int | None
        :param reader: a reader from which to pull the atom count
        :type reader: object | None
        """
        ...

    def __len__(self):
        """
        **LLM Docstring**

        The length of the raw flattened derivative data.

        :return: the number of stored values
        :rtype: int
        """
        ...

    def _get_n_m(self):
        """
        **LLM Docstring**

        Infer and cache the atom count `n` and mode count `m` from the data length,
        using the closed-form solutions of the sizing polynomials (with a Mathematica-
        derived cubic for the fully unknown case).

        :return: None
        :rtype: None
        """
        ...

    @property
    def n(self):
        """
        **LLM Docstring**

        The number of atoms, inferred from the data length if not supplied.

        :return: the atom count
        :rtype: int
        """
        ...

    @property
    def num_modes(self):
        """
        **LLM Docstring**

        The number of modes, inferred from the data length if not supplied.

        :return: the mode count
        :rtype: int
        """
        ...

    def _get_third_derivs(self):
        """
        **LLM Docstring**

        The first half of the raw data, holding the third derivatives.

        :return: the third-derivative data
        :rtype: np.ndarray
        """
        ...

    def _get_fourth_derivs(self):
        """
        **LLM Docstring**

        The second half of the raw data, holding the (diagonal) fourth derivatives.

        :return: the fourth-derivative data
        :rtype: np.ndarray
        """
        ...

    @property
    def third_derivs(self):
        """
        **LLM Docstring**

        The raw third-derivative data.

        :return: the third-derivative data
        :rtype: np.ndarray
        """
        ...

    @property
    def fourth_derivs(self):
        """
        **LLM Docstring**

        The raw fourth-derivative data.

        :return: the fourth-derivative data
        :rtype: np.ndarray
        """
        ...

    @staticmethod
    def _fill_3d_tensor(n, derivs, m=None):
        """Makes and fills a 3D tensor for our derivatives
        :param n:
        :type n:
        :param derivs:
        :type derivs:
        :return:
        :rtype: np.ndarray
        """
        ...

    def _get_third_deriv_array(self):
        """we make the appropriate 3D tensor from a bunch of 2D tensors
        :return:
        :rtype: np.ndarray
        """
        ...

    @property
    def third_deriv_array(self):
        """
        **LLM Docstring**

        The third derivatives as a full `(m, 3n, 3n)` tensor, symmetrized from the
        lower-triangle data.

        :return: the third-derivative tensor
        :rtype: np.ndarray
        """
        ...

    def _get_fourth_deriv_array(self):
        """We'll make our array of fourth derivs exactly the same as the third
        admittedly this should be a 4D tensor, but we only have the diagonal elements so it's just 3D
        I should make it a 4D sparse matrix honestly... Apparently we won't need many terms in the 4D tensor so it might
        make sense to handle that bloop doop bloop in the schmoop
        :return:
        :rtype: np.ndarray
        """
        ...

    @property
    def fourth_deriv_array(self):
        """
        **LLM Docstring**

        The fourth derivatives as a sparse tensor built from the diagonal elements
        Gaussian provides.

        :return: the fourth-derivative tensor
        :rtype: SparseArray
        """
        ...

class FchkDipoleDerivatives:
    """Holder class for dipole derivatives coming out of an fchk file"""

    def __init__(self, derivs, num_atoms=None, reader=None):
        """
        **LLM Docstring**

        Hold the flattened dipole-derivative data, optionally with the atom count (or a
        reader supplying it).

        :param derivs: the flattened dipole derivatives
        :type derivs: np.ndarray
        :param num_atoms: the number of atoms (inferred lazily if omitted)
        :type num_atoms: int | None
        :param reader: a reader from which to pull the atom count
        :type reader: object | None
        """
        ...

    def _get_n(self):
        """
        :return:
        :rtype: int
        """
        ...

    @property
    def n(self):
        """
        **LLM Docstring**

        The number of atoms, inferred from the data length (`3 * 3n` values) if not
        supplied.

        :return: the atom count
        :rtype: int
        """
        ...

    @property
    def shape(self):
        """
        **LLM Docstring**

        The shape of the dipole-derivative array, `(3n, 3)`.

        :return: the array shape
        :rtype: tuple[int, int]
        """
        ...

    @property
    def array(self):
        """
        **LLM Docstring**

        The dipole derivatives reshaped to `(3n, 3)`.

        :return: the dipole-derivative array
        :rtype: np.ndarray
        """
        ...

class FchkDipoleHigherDerivatives:
    """Holder class for dipole derivatives coming out of an fchk file"""

    def __init__(self, derivs, num_atoms=None, num_modes=None, reader=None):
        """
        **LLM Docstring**

        Hold the flattened higher dipole-derivative data (numerical derivatives w.r.t.
        the modes of the Cartesian dipole derivatives), optionally with atom/mode counts.

        :param derivs: the flattened higher dipole derivatives
        :type derivs: np.ndarray
        :param num_atoms: the number of atoms (inferred lazily if omitted)
        :type num_atoms: int | None
        :param num_modes: the number of modes (inferred lazily if omitted)
        :type num_modes: int | None
        :param reader: a reader from which to pull the atom count
        :type reader: object | None
        """
        ...

    def _get_n_m(self):
        """
        :return:
        :rtype: int
        """
        ...

    @property
    def num_modes(self):
        """
        **LLM Docstring**

        The number of modes, inferred from the data length if not supplied.

        :return: the mode count
        :rtype: int
        """
        ...

    @property
    def n(self):
        """
        **LLM Docstring**

        The number of atoms, inferred from the data length if not supplied.

        :return: the atom count
        :rtype: int
        """
        ...

    @property
    def shape(self):
        """
        **LLM Docstring**

        The shape of one derivative block, `(m, 3n, 3)`.

        :return: the block shape
        :rtype: tuple[int, int, int]
        """
        ...

    @property
    def second_deriv_array(self):
        """
        **LLM Docstring**

        The second dipole derivatives (`d^2 mu / dQ dx`) reshaped to `(m, 3n, 3)`.

        :return: the second-derivative array
        :rtype: np.ndarray
        """
        ...

    @property
    def third_deriv_array(self):
        """
        **LLM Docstring**

        The third dipole derivatives (`d^3 mu / dQ^2 dx`) as a `(m, m, 3n, 3)` tensor,
        built from the diagonal blocks Gaussian provides.

        :return: the third-derivative tensor
        :rtype: np.ndarray
        """
        ...

class FchkDipoleNumDerivatives:
    """
    Holder class for numerical derivatives coming out of an fchk file.
    Gaussian returns first and second derivatives
    """

    def __init__(self, derivs, num_atoms=None, num_modes=None, reader=None):
        """
        **LLM Docstring**

        Hold the flattened numerical dipole derivatives (first and second) with respect
        to the modes, optionally with the mode count.

        :param derivs: the flattened numerical derivatives
        :type derivs: np.ndarray
        :param num_atoms: unused (kept for signature parity)
        :type num_atoms: int | None
        :param num_modes: the number of modes (inferred lazily if omitted)
        :type num_modes: int | None
        :param reader: unused (kept for signature parity)
        :type reader: object | None
        """
        ...

    def _get_m(self):
        """
        Returns the number of _modes_ in the system
        :return:
        :rtype: int
        """
        ...

    @property
    def num_modes(self):
        """
        **LLM Docstring**

        The number of modes, inferred from the data length if not supplied.

        :return: the mode count
        :rtype: int
        """
        ...

    @property
    def shape(self):
        """
        **LLM Docstring**

        The shape of one derivative block, `(m, 3)`.

        :return: the block shape
        :rtype: tuple[int, int]
        """
        ...

    @property
    def first_derivatives(self):
        """
        **LLM Docstring**

        The first numerical dipole derivatives, reshaped to `(m, 3)`.

        :return: the first-derivative array
        :rtype: np.ndarray
        """
        ...

    @property
    def second_derivatives(self):
        """
        **LLM Docstring**

        The second numerical dipole derivatives, reshaped to `(m, 3)`.

        :return: the second-derivative array
        :rtype: np.ndarray
        """
        ...