"""
Lazy class for holding force constants and higher derivative tensors pulled from the Gaussian log file
"""
import numpy as np
from ...Numputils import SparseArray

__all__ = [
    "FchkForceConstants",
    "FchkForceDerivatives",
    "FchkDipoleDerivatives",
    "FchkDipoleHigherDerivatives",
    "FchkDipoleNumDerivatives"
]

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
        self.fcs = fcs
        self._n = (
            num_atoms
                if num_atoms is not None else
            reader.num_atoms
                if reader is not None else
            None
        )

    def __len__(self):
        """
        **LLM Docstring**

        The length of the raw flattened force-constant data.

        :return: the number of stored values
        :rtype: int
        """
        return len(self.fcs)

    def _get_n(self):
        """
        :return:
        :rtype: int
        """
        if self._n is None:
            self._n = int((-1 + np.sqrt(1 + 8*len(self)))/6) # solving 3n*3n == 2*l - 3n
        return self._n

    @property
    def n(self):
        """
        **LLM Docstring**

        The number of atoms, inferred from the data length if not supplied.

        :return: the atom count
        :rtype: int
        """
        return self._get_n()
    @property
    def shape(self):
        """
        **LLM Docstring**

        The shape of the full force-constant matrix, `(3n, 3n)`.

        :return: the matrix shape
        :rtype: tuple[int, int]
        """
        return (3*self.n, 3*self.n)

    def _get_array(self):
        """Uses the computed n to make and symmetrize an appropriately formatted array from the lower-triangle data
        :return:
        :rtype: np.ndarray
        """
        n = self.n
        full_array = np.zeros((3*n, 3*n))
        full_array[np.tril_indices_from(full_array)] = self.fcs
        full_array = full_array + np.tril(full_array, -1).T
        return full_array

    @property
    def array(self):
        """
        **LLM Docstring**

        The full, symmetrized `(3n, 3n)` force-constant matrix reconstructed from the
        lower-triangle data.

        :return: the force-constant matrix
        :rtype: np.ndarray
        """
        return self._get_array()


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
        self.derivs = derivs
        self._n = (
            num_atoms
                if num_atoms is not None else
            reader.num_atoms
                if reader is not None else
            None
        )
        self._m = num_modes

    def __len__(self):
        """
        **LLM Docstring**

        The length of the raw flattened derivative data.

        :return: the number of stored values
        :rtype: int
        """
        return len(self.derivs)

    def _get_n_m(self):
        """
        **LLM Docstring**

        Infer and cache the atom count `n` and mode count `m` from the data length,
        using the closed-form solutions of the sizing polynomials (with a Mathematica-
        derived cubic for the fully unknown case).

        :return: None
        :rtype: None
        """
        if self._n is None:
            l = len(self)
            if self._m is None:
                # had to use Mathematica to get this from the cubic poly
                #  2*(3n-6)*(3n)^2 == 2*l - 2*(3n-6)*(3n)
                l_quad = 81*l**2 + 3120*l - 5292
                l_body = (3*np.sqrt(l_quad) - 27*l - 520)
                if l_body > 0:
                    l1 = l_body**(1/3)
                else:
                    l1 = -(-l_body)**(1/3)
                n = (1/18)*( 10 + (2**(1/3))*( l1 - 86/l1) )
                self._n = int(np.ceil(n)) # precision issues screw this up in python, but not in Mathematica (I think)
                self._m = 3*self._n - 6
            else:
                # solving a quadratic poly
                m = self._m
                self._n = int(
                    (np.sqrt(4*l*m - m**2) - m)/ (6*m)
                )
        elif self._m is None:
            l = len(self)
            self._m = int(l / (3*self._n * (1 + 3*self._n)))

    @property
    def n(self):
        """
        **LLM Docstring**

        The number of atoms, inferred from the data length if not supplied.

        :return: the atom count
        :rtype: int
        """
        if self._n is None:
            self._get_n_m()
        return self._n

    @property
    def num_modes(self):
        """
        **LLM Docstring**

        The number of modes, inferred from the data length if not supplied.

        :return: the mode count
        :rtype: int
        """
        if self._m is None:
            self._get_n_m()
        return self._m

    def _get_third_derivs(self):
        """
        **LLM Docstring**

        The first half of the raw data, holding the third derivatives.

        :return: the third-derivative data
        :rtype: np.ndarray
        """
        # fourth and third derivs are same len
        d = self.derivs
        return d[:int(len(d)/2)]

    def _get_fourth_derivs(self):
        """
        **LLM Docstring**

        The second half of the raw data, holding the (diagonal) fourth derivatives.

        :return: the fourth-derivative data
        :rtype: np.ndarray
        """
        # fourth and third derivs are same len
        d = self.derivs
        return d[int(len(d)/2):]

    @property
    def third_derivs(self):
        """
        **LLM Docstring**

        The raw third-derivative data.

        :return: the third-derivative data
        :rtype: np.ndarray
        """
        return self._get_third_derivs()

    @property
    def fourth_derivs(self):
        """
        **LLM Docstring**

        The raw fourth-derivative data.

        :return: the fourth-derivative data
        :rtype: np.ndarray
        """
        return self._get_fourth_derivs()
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
        dim_1 = (3*n)
        mode_n = 3*n - 6 if m is None else m

        full_array_1 = np.zeros((mode_n, dim_1, dim_1))
        # set the lower triangle
        inds_1, inds_2 = np.tril_indices(dim_1)
        l_per = len(inds_1)
        main_ind = np.broadcast_to(np.arange(mode_n)[:, np.newaxis], (mode_n, l_per)).flatten()
        sub_ind_1 = np.broadcast_to(inds_1, (mode_n, l_per)).flatten()
        sub_ind_2 = np.broadcast_to(inds_2, (mode_n, l_per)).flatten()
        inds = ( main_ind, sub_ind_1, sub_ind_2 )
        full_array_1[inds] = derivs
        # set the upper triangle
        inds2 = ( main_ind, sub_ind_2, sub_ind_1 ) # basically just taking a transpose
        full_array_1[inds2] = derivs

        return full_array_1
    def _get_third_deriv_array(self):
        """we make the appropriate 3D tensor from a bunch of 2D tensors
        :return:
        :rtype: np.ndarray
        """
        n = self.n
        derivs = self.third_derivs
        return self._fill_3d_tensor(n, derivs, m=self.num_modes)
    @property
    def third_deriv_array(self):
        """
        **LLM Docstring**

        The third derivatives as a full `(m, 3n, 3n)` tensor, symmetrized from the
        lower-triangle data.

        :return: the third-derivative tensor
        :rtype: np.ndarray
        """
        return self._get_third_deriv_array()
    def _get_fourth_deriv_array(self):
        """We'll make our array of fourth derivs exactly the same as the third
        admittedly this should be a 4D tensor, but we only have the diagonal elements so it's just 3D
        I should make it a 4D sparse matrix honestly... Apparently we won't need many terms in the 4D tensor so it might
        make sense to handle that bloop doop bloop in the schmoop
        :return:
        :rtype: np.ndarray
        """
        n = self.n
        derivs = self.fourth_derivs
        return SparseArray.from_diag(self._fill_3d_tensor(n, derivs, m=self.num_modes))
    @property
    def fourth_deriv_array(self):
        """
        **LLM Docstring**

        The fourth derivatives as a sparse tensor built from the diagonal elements
        Gaussian provides.

        :return: the fourth-derivative tensor
        :rtype: SparseArray
        """
        return self._get_fourth_deriv_array()

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
        self.derivs = derivs
        self._n = (
            num_atoms
                if num_atoms is not None else
            reader.num_atoms
                if reader is not None else
            None
        )

    def _get_n(self):
        """
        :return:
        :rtype: int
        """
        # derivatives with respect to 3N Cartesians...
        if self._n is None:
            self._n = int(len(self.derivs)/9) # solving 3*3n == l
        return self._n
    @property
    def n(self):
        """
        **LLM Docstring**

        The number of atoms, inferred from the data length (`3 * 3n` values) if not
        supplied.

        :return: the atom count
        :rtype: int
        """
        return self._get_n()
    @property
    def shape(self):
        """
        **LLM Docstring**

        The shape of the dipole-derivative array, `(3n, 3)`.

        :return: the array shape
        :rtype: tuple[int, int]
        """
        return (3*self.n, 3)
    @property
    def array(self):
        """
        **LLM Docstring**

        The dipole derivatives reshaped to `(3n, 3)`.

        :return: the dipole-derivative array
        :rtype: np.ndarray
        """
        return np.reshape(self.derivs, self.shape)

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
        self.derivs = derivs
        self._n = (
            num_atoms
                if num_atoms is not None else
            reader.num_atoms
                if reader is not None else
            None
        )
        self._m = num_modes
    def _get_n_m(self):
        """
        :return:
        :rtype: int
        """
        # numerical derivatives with respect to the 3n-6 normal modes of derivatives with respect to 3N Cartesians...
        # Gaussian gives us stuff out like d^2mu/dQdx and d^3mu/dQ^2dx
        if self._n is None:
            l = len(self.derivs)
            if self._m is None:
                self._n = int(1 + np.sqrt(1 + l/54)) # solving 3n*(3n-6) == l/6
                self._m = 3*self._n - 6
            else:
                self._n = l // self.num_modes // 3
        elif self._m is None:
            l = len(self.derivs)
            self._m = l // (6 * 3 * self._n)
        # return self._n
    @property
    def num_modes(self):
        """
        **LLM Docstring**

        The number of modes, inferred from the data length if not supplied.

        :return: the mode count
        :rtype: int
        """
        if self._m is None:
            self._get_n_m()
        return self._m
    @property
    def n(self):
        """
        **LLM Docstring**

        The number of atoms, inferred from the data length if not supplied.

        :return: the atom count
        :rtype: int
        """
        if self._n is None:
            self._get_n_m()
        return self._n
    # @n.setter
    # def n(self, n):
    #     self._n = n
    @property
    def shape(self):
        """
        **LLM Docstring**

        The shape of one derivative block, `(m, 3n, 3)`.

        :return: the block shape
        :rtype: tuple[int, int, int]
        """
        return (self.num_modes, 3*self.n, 3)

    @property
    def second_deriv_array(self):
        """
        **LLM Docstring**

        The second dipole derivatives (`d^2 mu / dQ dx`) reshaped to `(m, 3n, 3)`.

        :return: the second-derivative array
        :rtype: np.ndarray
        """
        nels = int(np.prod(self.shape))
        return np.reshape(self.derivs[:nels], self.shape)
    @property
    def third_deriv_array(self):
        """
        **LLM Docstring**

        The third dipole derivatives (`d^3 mu / dQ^2 dx`) as a `(m, m, 3n, 3)` tensor,
        built from the diagonal blocks Gaussian provides.

        :return: the third-derivative tensor
        :rtype: np.ndarray
        """
        nels = int(np.prod(self.shape))
        base_array = np.reshape(self.derivs[nels:], self.shape)
        full_array = np.zeros((self.num_modes, self.num_modes, 3*self.n, 3))
        for i in range(self.num_modes):
            full_array[i, i] = base_array[i]
        return full_array

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
        self.derivs = derivs
        # self._n = num_atoms if num_atoms is not None else reader.num_atoms
        self._m = num_modes
    def _get_m(self):
        """
        Returns the number of _modes_ in the system
        :return:
        :rtype: int
        """
        # derivatives with respect to (3N - 6) modes...
        if self._m is None:
            self._m = len(self.derivs)//6 # solving 2*3*n == l
        return self._m
    @property
    def num_modes(self):
        """
        **LLM Docstring**

        The number of modes, inferred from the data length if not supplied.

        :return: the mode count
        :rtype: int
        """
        return self._get_m()
    @property
    def shape(self):
        """
        **LLM Docstring**

        The shape of one derivative block, `(m, 3)`.

        :return: the block shape
        :rtype: tuple[int, int]
        """
        return (self.num_modes, 3)
    @property
    def first_derivatives(self):
        """
        **LLM Docstring**

        The first numerical dipole derivatives, reshaped to `(m, 3)`.

        :return: the first-derivative array
        :rtype: np.ndarray
        """
        return np.reshape(self.derivs[:len(self.derivs)//2], self.shape)
    @property
    def second_derivatives(self):
        """
        **LLM Docstring**

        The second numerical dipole derivatives, reshaped to `(m, 3)`.

        :return: the second-derivative array
        :rtype: np.ndarray
        """
        return np.reshape(self.derivs[len(self.derivs)//2:], self.shape)