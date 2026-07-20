import abc, numpy as np, scipy.signal, math
import itertools as it
from ..Combinatorics import UniquePermutations, Binomial
from ..Numputils import SparseArray, group_by
__all__ = ['AbstractPolynomial', 'DensePolynomial', 'SparsePolynomial', 'PureMonicPolynomial', 'TensorCoefficientPoly']

class AbstractPolynomial(metaclass=abc.ABCMeta):
    """
    Provides the general interface an abstract polynomial needs ot support, including
    multiplication, addition, shifting, access of coefficients, and evaluation
    """

    @property
    @abc.abstractmethod
    def scaling(self):
        """
        **LLM Docstring**

        Abstract: the overall scalar prefactor multiplying the polynomial.

        :return: the scaling factor
        :rtype: float
        """
        ...

    @abc.abstractmethod
    def __mul__(self, other) -> 'AbstractPolynomial':
        """
        **LLM Docstring**

        Abstract: multiply this polynomial by another polynomial or a scalar.

        :param other: the multiplier
        :return: the product polynomial
        :rtype: AbstractPolynomial
        """
        ...

    @abc.abstractmethod
    def __add__(self, other) -> 'AbstractPolynomial':
        """
        **LLM Docstring**

        Abstract: add another polynomial or a scalar to this one.

        :param other: the addend
        :return: the sum polynomial
        :rtype: AbstractPolynomial
        """
        ...

    @abc.abstractmethod
    def shift(self, shift) -> 'AbstractPolynomial':
        """
        **LLM Docstring**

        Abstract: return the polynomial shifted in its variables (i.e. `p(x + shift)`).

        :param shift: the per-variable shift
        :return: the shifted polynomial
        :rtype: AbstractPolynomial
        """
        ...

    def __rmul__(self, other) -> 'AbstractPolynomial':
        """
        **LLM Docstring**

        Right multiplication, delegating to `__mul__` (multiplication is commutative
        here).

        :param other: the multiplier
        :return: the product polynomial
        :rtype: AbstractPolynomial
        """
        ...

    def __radd__(self, other) -> 'AbstractPolynomial':
        """
        **LLM Docstring**

        Right addition, delegating to `__add__`.

        :param other: the addend
        :return: the sum polynomial
        :rtype: AbstractPolynomial
        """
        ...

    def __truediv__(self, other) -> 'AbstractPolynomial':
        """
        **LLM Docstring**

        Divide the polynomial by a scalar (multiply by its reciprocal).

        :param other: the scalar divisor
        :return: the scaled polynomial
        :rtype: AbstractPolynomial
        """
        ...

    def __neg__(self):
        """
        **LLM Docstring**

        Negate the polynomial.

        :return: the negated polynomial
        :rtype: AbstractPolynomial
        """
        ...

    def __sub__(self, other):
        """
        **LLM Docstring**

        Subtract another polynomial or scalar (add its negation).

        :param other: the subtrahend
        :return: the difference polynomial
        :rtype: AbstractPolynomial
        """
        ...

    def __rsub__(self, other):
        """
        **LLM Docstring**

        Right subtraction (`other - self`), via negation and addition.

        :param other: the minuend
        :return: the difference polynomial
        :rtype: AbstractPolynomial
        """
        ...

class DensePolynomial(AbstractPolynomial):
    """
    A straightforward dense n-dimensional polynomial data structure with
    multiplications and shifts
    """

    def __init__(self, coeffs, prefactor=None, shift=None, stack_dim=0):
        """
        **LLM Docstring**

        Build a dense n-dimensional polynomial from a coefficient tensor, with a deferred
        scalar prefactor and variable shift.

        The coefficient tensor is indexed by per-variable powers; a leading `stack_dim`
        axes hold a batch/stack of polynomials. The `prefactor` and `shift` are applied
        lazily the first time the coefficients are materialized.

        :param coeffs: the coefficient tensor (dense or `SparseArray`)
        :type coeffs: np.ndarray | SparseArray
        :param prefactor: an overall scalar multiplier (applied lazily)
        :type prefactor: float | None
        :param shift: a per-variable shift to apply (applied lazily)
        :type shift: np.ndarray | None
        :param stack_dim: the number of leading stack/batch axes
        :type stack_dim: int
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the coefficient shape and scaling.

        :return: the representation
        :rtype: str
        """
        ...

    @classmethod
    def from_tensors(cls, tensors, prefactor=None, shift=None, rescale=True):
        """
        **LLM Docstring**

        Build a `DensePolynomial` from a list of derivative/coefficient tensors (one per
        order), condensing them into a single coefficient tensor.

        :param tensors: the per-order coefficient tensors
        :type tensors: list
        :param prefactor: an overall scalar multiplier
        :type prefactor: float | None
        :param shift: a per-variable shift
        :type shift: np.ndarray | None
        :param rescale: divide each tensor entry by its permutation count
        :type rescale: bool
        :return: the polynomial
        :rtype: DensePolynomial
        """
        ...

    @property
    def shape(self):
        """
        **LLM Docstring**

        The shape of the coefficient tensor (including the stack axes).

        :return: the coefficient shape
        :rtype: tuple
        """
        ...

    @property
    def scaling(self):
        """
        **LLM Docstring**

        The overall scalar prefactor (1 when unset). Setting it stores a new deferred
        prefactor.

        :return: the scaling factor
        :rtype: float
        """
        ...

    @scaling.setter
    def scaling(self, s):
        """
        **LLM Docstring**

        The overall scalar prefactor (1 when unset). Setting it stores a new deferred
        prefactor.

        :return: the scaling factor
        :rtype: float
        """
        ...

    @property
    def coeffs(self) -> 'np.ndarray|SparseArray':
        """
        **LLM Docstring**

        The materialized coefficient tensor, applying (and then clearing) any deferred
        shift and prefactor on first access. Setting it replaces the raw coefficients.

        :return: the coefficient tensor
        :rtype: np.ndarray | SparseArray
        """
        ...

    @coeffs.setter
    def coeffs(self, cs):
        """
        **LLM Docstring**

        The materialized coefficient tensor, applying (and then clearing) any deferred
        shift and prefactor on first access. Setting it replaces the raw coefficients.

        :return: the coefficient tensor
        :rtype: np.ndarray | SparseArray
        """
        ...

    @property
    def coordinate_dim(self):
        """
        **LLM Docstring**

        The number of polynomial variables (the coefficient rank minus the stack axes).

        :return: the coordinate dimension
        :rtype: int
        """
        ...

    @classmethod
    def _manage_stack_bcast(cls, c1, c2, s1, s2):
        """
        **LLM Docstring**

        Broadcast two coefficient tensors (and their stack dimensions) to a common
        stack/coordinate shape so they can be convolved or combined.

        :param c1: the first coefficient tensor
        :param c2: the second coefficient tensor
        :param s1: the first tensor's stack dimension
        :type s1: int
        :param s2: the second tensor's stack dimension
        :type s2: int
        :return: `(c1, c2, stack_dim)` broadcast to a common shape
        :rtype: tuple
        :raises ValueError: if the stack shapes can't be broadcast
        """
        ...

    @classmethod
    def _sparse_convolve_vals_inds(cls, vals1, vals2, inds1, inds2):
        """
        **LLM Docstring**

        Convolve two sparse coefficient sets by forming the outer product of their
        values and the pairwise sums of their indices, then summing duplicate indices.

        :param vals1: the first value array
        :type vals1: np.ndarray
        :param vals2: the second value array
        :type vals2: np.ndarray
        :param inds1: the first index arrays (one per axis)
        :param inds2: the second index arrays (one per axis)
        :return: the convolved `(indices, values)`
        :rtype: tuple
        """
        ...

    @classmethod
    def _sparse_convolve_single(cls, coeffs_1, coeffs_2):
        """
        **LLM Docstring**

        Convolve two sparse coefficient tensors (polynomial multiplication) into a new
        `SparseArray`.

        :param coeffs_1: the first coefficient tensor
        :type coeffs_1: SparseArray
        :param coeffs_2: the second coefficient tensor
        :type coeffs_2: SparseArray
        :return: the convolved coefficients
        :rtype: SparseArray
        """
        ...

    @classmethod
    def _sparse_convolve_stacks(cls, coeffs_1, coeffs_2, stack_dim):
        """
        **LLM Docstring**

        Convolve two stacked sparse coefficient tensors, matching up the stack indices
        and convolving the coordinate blocks within each matching stack.

        :param coeffs_1: the first stacked coefficient tensor
        :type coeffs_1: SparseArray
        :param coeffs_2: the second stacked coefficient tensor
        :type coeffs_2: SparseArray
        :param stack_dim: the number of leading stack axes
        :type stack_dim: int
        :return: the convolved coefficients
        :rtype: SparseArray
        """
        ...

    def __mul__(self, other) -> 'DensePolynomial':
        """
        **LLM Docstring**

        Multiply this polynomial by another (convolving their coefficient tensors) or by
        a scalar.

        :param other: the multiplier polynomial or scalar
        :return: the product polynomial (or `0`/`self` for the scalar special cases)
        :rtype: DensePolynomial
        """
        ...

    def _force_consistent_addition_shapes(self, other):
        """
        **LLM Docstring**

        Broadcast the two polynomials' stack shapes to a common shape ahead of addition,
        returning their (possibly broadcast) coefficient tensors.

        :param other: the other polynomial
        :type other: DensePolynomial
        :return: the two coefficient tensors
        :rtype: tuple
        """
        ...

    @staticmethod
    def _enforce_ndarray_padding(fcs: np.ndarray, consistent_shape, pad_fcs, fc_padding):
        """
        **LLM Docstring**

        Pad a dense coefficient tensor (expanding new axes as needed) up to a common
        coordinate shape for addition.

        :param fcs: the coefficient tensor
        :type fcs: np.ndarray
        :param consistent_shape: the target shape
        :param pad_fcs: the tensor's current padded shape
        :param fc_padding: the number of axes to add
        :type fc_padding: int
        :return: the padded tensor
        :rtype: np.ndarray
        """
        ...

    @staticmethod
    def _enforce_sparse_padding(fcs: SparseArray, consistent_shape, pad_fcs, fc_padding):
        """
        **LLM Docstring**

        Pad a sparse coefficient tensor (expanding new axes as needed) up to a common
        coordinate shape for addition.

        :param fcs: the coefficient tensor
        :type fcs: SparseArray
        :param consistent_shape: the target shape
        :param pad_fcs: the tensor's current padded shape
        :param fc_padding: the number of axes to add
        :type fc_padding: int
        :return: the padded tensor
        :rtype: SparseArray
        """
        ...

    @classmethod
    def _enforce_addition_padding(cls, fcs, consistent_shape, pad_fcs, fc_padding):
        """
        **LLM Docstring**

        Pad a coefficient tensor (dense or sparse) to a common coordinate shape for
        addition.

        :param fcs: the coefficient tensor
        :type fcs: np.ndarray | SparseArray
        :param consistent_shape: the target shape
        :param pad_fcs: the tensor's current padded shape
        :param fc_padding: the number of axes to add
        :type fc_padding: int
        :return: the padded tensor
        :rtype: np.ndarray | SparseArray
        """
        ...

    def __add__(self, other) -> 'DensePolynomial':
        """
        **LLM Docstring**

        Add another polynomial (aligning and padding their coefficient tensors) or a
        scalar (added to the constant term).

        :param other: the addend polynomial or scalar
        :return: the sum polynomial
        :rtype: DensePolynomial
        """
        ...

    def shift(self, shift) -> 'DensePolynomial':
        """
        **LLM Docstring**

        Return the polynomial with an added deferred variable shift (`p(x + shift)`).

        :param shift: the per-variable shift (scalar or vector)
        :return: the shifted polynomial
        :rtype: DensePolynomial
        """
        ...

    @classmethod
    def compute_shifted_coeffs(cls, poly_coeffs, shift, stack_dim=0):
        """
        **LLM Docstring**

        Compute the coefficient tensor of a polynomial after a variable shift
        (`p(x + shift)`), via a factorial-weighted convolution of the coefficients with
        the shift powers (a Taylor re-expansion).

        :param poly_coeffs: the original coefficient tensor
        :type poly_coeffs: np.ndarray
        :param shift: the per-variable shift
        :type shift: np.ndarray | float
        :param stack_dim: the number of leading stack axes
        :type stack_dim: int
        :return: the shifted coefficient tensor
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def fill_tensors(self, tensors, idx, value, stack_dim, pcache, permute, rescale):
        """
        **LLM Docstring**

        Scatter a single coefficient value into the per-order derivative tensors,
        filling every index permutation (optionally rescaling by the permutation count)
        so the resulting tensors are symmetric.

        :param tensors: the per-order tensors being filled (modified in place)
        :type tensors: list
        :param idx: the coefficient's power index (with any stack prefix)
        :type idx: tuple
        :param value: the coefficient value
        :param stack_dim: the number of leading stack axes
        :type stack_dim: int
        :param pcache: a cache of index permutations
        :type pcache: dict
        :param permute: fill all index permutations
        :type permute: bool
        :param rescale: divide the value across its permutations
        :type rescale: bool
        """
        ...

    @classmethod
    def extract_tensors(cls, coeffs, stack_dim=None, permute=True, rescale=True, cutoff=1e-15):
        """
        **LLM Docstring**

        Decompose a coefficient tensor into a list of per-order (symmetric) derivative
        tensors, scattering each nonzero coefficient across its index permutations.

        :param coeffs: the coefficient tensor (dense or sparse)
        :type coeffs: np.ndarray | SparseArray
        :param stack_dim: the number of leading stack axes
        :type stack_dim: int | None
        :param permute: fill all index permutations
        :type permute: bool
        :param rescale: divide each value across its permutations
        :type rescale: bool
        :param cutoff: the magnitude below which dense entries are treated as zero
        :type cutoff: float
        :return: the per-order tensors (index 0 is the constant term)
        :rtype: list
        """
        ...

    @classmethod
    def condense_tensors(cls, tensors, rescale=True, allow_sparse=True):
        """
        **LLM Docstring**

        Collapse a list of per-order derivative tensors back into a single (dense or
        sparse) coefficient tensor, choosing a sparse representation when the density is
        low.

        :param tensors: the per-order tensors
        :type tensors: list
        :param rescale: multiply each entry by its permutation count
        :type rescale: bool
        :param allow_sparse: allow returning a `SparseArray` when sparse enough
        :type allow_sparse: bool
        :return: `(coefficient_tensor, stack_dim)`
        :rtype: tuple
        """
        ...

    @property
    def coefficient_tensors(self):
        """
        **LLM Docstring**

        The per-order (permutation-rescaled) derivative tensors of the polynomial,
        computed lazily.

        :return: the per-order coefficient tensors
        :rtype: list
        """
        ...

    @property
    def unscaled_coefficient_tensors(self):
        """
        **LLM Docstring**

        The per-order derivative tensors without permutation rescaling, computed lazily.

        :return: the per-order unscaled coefficient tensors
        :rtype: list
        """
        ...

    def transform(self, lin_transf):
        """
        Applies (for now) a linear transformation to the polynomial
        """
        ...

    def outer(self, other):
        """
        **LLM Docstring**

        Form the outer-product polynomial of this one with another coefficient tensor
        (no stack dimensions supported).

        :param other: the other polynomial/coefficients
        :return: the outer-product polynomial
        :rtype: DensePolynomial
        """
        ...

    @classmethod
    def _coord_deriv(cls, coeffs, coord, stack_dim):
        """
        **LLM Docstring**

        Differentiate a coefficient tensor once with respect to one coordinate (power
        down-shift with the integer-power scaling).

        :param coeffs: the coefficient tensor
        :type coeffs: np.ndarray
        :param coord: the coordinate index (relative to the coordinate axes)
        :type coord: int
        :param stack_dim: the number of leading stack axes
        :type stack_dim: int
        :return: the differentiated coefficients (or `0` if constant in that coordinate)
        :rtype: np.ndarray | int
        """
        ...

    def deriv(self, coord):
        """
        **LLM Docstring**

        Differentiate the polynomial with respect to one coordinate.

        :param coord: the coordinate index
        :type coord: int
        :return: the derivative polynomial (or `0` if constant in that coordinate)
        :rtype: DensePolynomial | int
        """
        ...

    @classmethod
    def _apply_dense_grad(cls, coeffs, stack_dim, shape, n, c):
        """
        **LLM Docstring**

        Build the gradient of a dense coefficient tensor: a new leading axis holding the
        derivative with respect to each coordinate.

        :param coeffs: the coefficient tensor
        :type coeffs: np.ndarray
        :param stack_dim: the number of leading stack axes
        :type stack_dim: int
        :param shape: the coefficient shape
        :param n: the number of coordinates
        :type n: int
        :param c: the per-coordinate shape
        :return: the gradient coefficient tensor
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def _take_sparse_position_derivs(cls, stack_dim, axis, nzvals, nzinds):
        """
        **LLM Docstring**

        Differentiate the sparse coefficient data with respect to one coordinate,
        dropping the zero-power terms and applying the integer-power scaling.

        :param stack_dim: the number of leading stack axes
        :type stack_dim: int
        :param axis: the coordinate axis (relative to the coordinate axes)
        :type axis: int
        :param nzvals: the nonzero values
        :type nzvals: np.ndarray
        :param nzinds: the nonzero indices (one array per axis)
        :return: the differentiated `(values, indices)`, or `0` if constant
        :rtype: tuple | int
        """
        ...

    @classmethod
    def _apply_sparse_grad(cls, coeffs: SparseArray, stack_dim, shape, n, c):
        """
        **LLM Docstring**

        Build the gradient of a sparse coefficient tensor by differentiating along each
        coordinate and stacking the results under a new leading axis.

        :param coeffs: the coefficient tensor
        :type coeffs: SparseArray
        :param stack_dim: the number of leading stack axes
        :type stack_dim: int
        :param shape: the coefficient shape
        :param n: the number of coordinates
        :type n: int
        :param c: the per-coordinate shape
        :return: the gradient coefficient tensor
        :rtype: SparseArray
        """
        ...

    @classmethod
    def _apply_grad(cls, coeffs, stack_dim):
        """
        **LLM Docstring**

        Build the gradient coefficient tensor (dense or sparse) of a coefficient tensor.

        :param coeffs: the coefficient tensor
        :type coeffs: np.ndarray | SparseArray
        :param stack_dim: the number of leading stack axes
        :type stack_dim: int
        :return: the gradient coefficient tensor
        :rtype: np.ndarray | SparseArray
        """
        ...

    def grad(self):
        """
        **LLM Docstring**

        Return the gradient polynomial, whose leading stack axis indexes the derivative
        with respect to each coordinate.

        :return: the gradient polynomial
        :rtype: DensePolynomial
        """
        ...

    def clip(self, threshold=1e-15):
        """
        **LLM Docstring**

        Drop coefficients below a magnitude threshold, returning a trimmed polynomial
        (or `0` if everything is clipped).

        :param threshold: the magnitude cutoff
        :type threshold: float
        :return: the clipped polynomial (or `0`)
        :rtype: DensePolynomial | int
        """
        ...

    def make_sparse_backed(self, threshold=1e-15):
        """
        **LLM Docstring**

        Return an equivalent polynomial whose coefficients are stored as a `SparseArray`
        (after clipping small entries).

        :param threshold: the clipping magnitude cutoff
        :type threshold: float
        :return: the sparse-backed polynomial
        :rtype: DensePolynomial
        """
        ...

class SparsePolynomial(AbstractPolynomial):
    """
    A semi-symbolic representation of a polynomial of tensor
    coefficients
    """

    def __init__(self, terms: dict, prefactor=1, ndim=None, canonicalize=True):
        """
        **LLM Docstring**

        Build a semi-symbolic sparse polynomial from a `{sorted_index_tuple: coefficient}`
        term mapping.

        :param terms: the term mapping (keys are sorted variable-index tuples)
        :type terms: dict
        :param prefactor: an overall scalar multiplier
        :type prefactor: float
        :param ndim: the number of variables (inferred if omitted)
        :type ndim: int | None
        :param canonicalize: accepted for interface parity
        :type canonicalize: bool
        """
        ...

    @property
    def scaling(self):
        """
        **LLM Docstring**

        The overall scalar prefactor (1 when unset). Setting it stores a new prefactor.

        :return: the scaling factor
        :rtype: float
        """
        ...

    @scaling.setter
    def scaling(self, s):
        """
        **LLM Docstring**

        The overall scalar prefactor (1 when unset). Setting it stores a new prefactor.

        :return: the scaling factor
        :rtype: float
        """
        ...

    def expand(self):
        """
        **LLM Docstring**

        Fold the prefactor into the term coefficients, returning an equivalent polynomial
        with unit prefactor.

        :return: the expanded polynomial
        :rtype: SparsePolynomial
        """
        ...

    @classmethod
    def monomial(cls, idx, value=1):
        """
        **LLM Docstring**

        Build a single-term polynomial for the monomial at the given index.

        :param idx: the monomial's variable-index tuple
        :type idx: tuple
        :param value: the coefficient
        :return: the monomial polynomial
        :rtype: SparsePolynomial
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the terms and prefactor.

        :return: the representation
        :rtype: str
        """
        ...

    def __mul__(self, other):
        """
        **LLM Docstring**

        Multiply by another sparse polynomial (merging index tuples and summing
        coefficients) or by a scalar.

        :param other: the multiplier polynomial or scalar
        :return: the product polynomial
        :rtype: SparsePolynomial
        """
        ...

    def __add__(self, other):
        """
        **LLM Docstring**

        Add another sparse polynomial (merging matching terms) or a scalar (added to the
        constant term).

        :param other: the addend polynomial or scalar
        :return: the sum polynomial (or `0` if everything cancels)
        :rtype: SparsePolynomial | int
        """
        ...

    @classmethod
    def _to_tensor_idx(cls, term, ndim, tupleate=True):
        """
        **LLM Docstring**

        Convert a sorted variable-index term into a per-variable power tuple (or array)
        of length `ndim`.

        :param term: the sorted variable-index tuple
        :type term: tuple
        :param ndim: the number of variables
        :type ndim: int
        :param tupleate: return a tuple rather than an array
        :type tupleate: bool
        :return: the per-variable power index
        :rtype: tuple | np.ndarray
        """
        ...

    @property
    def shape(self):
        """
        **LLM Docstring**

        The dense coefficient shape implied by the terms (per-variable max power + 1),
        computed lazily.

        :return: the dense shape
        :rtype: tuple
        """
        ...

    def as_dense(self) -> DensePolynomial:
        """
        **LLM Docstring**

        Convert to an equivalent `DensePolynomial`, filling a dense coefficient tensor
        from the terms.

        :return: the dense polynomial
        :rtype: DensePolynomial
        """
        ...

    def _get_sparse_shift_terms(self, term_vector, shift_vector) -> dict:
        """
        Provides the set of terms corresponding to shifting a term of the form
         `prod(x[i]**p[i])` (where `p` is the `term_vector`) by the corresponding `shift_vector`


        :param term_vector:
        :param shift_vector:
        :return:
        """
        ...

    def shift(self, shift) -> 'SparsePolynomial':
        """
        **LLM Docstring**

        Return the polynomial shifted in its variables (`p(x + shift)`), expanding each
        term via the binomial theorem.

        :param shift: the per-variable shift
        :type shift: np.ndarray
        :return: the shifted polynomial
        :rtype: SparsePolynomial
        """
        ...

class PureMonicPolynomial(SparsePolynomial):

    def __init__(self, terms: dict, prefactor=1, canonicalize=True):
        """
        **LLM Docstring**

        Build a monic-monomial polynomial from a term mapping, canonicalizing (and
        merging) the monomial keys by default.

        :param terms: the `{monomial_key_tuple: coefficient}` mapping
        :type terms: dict
        :param prefactor: an overall scalar multiplier
        :type prefactor: float
        :param canonicalize: canonicalize and merge the keys
        :type canonicalize: bool
        """
        ...

    @property
    def shape(self):
        """
        **LLM Docstring**

        Not supported: monic-monomial polynomials have no dense counterpart.

        :raises ValueError: always
        """
        ...

    def as_dense(self):
        """
        **LLM Docstring**

        Not supported: monic-monomial polynomials have no dense counterpart.

        :raises ValueError: always
        """
        ...

    def shift(self, shift) -> DensePolynomial:
        """
        **LLM Docstring**

        Not supported: monic-monomial polynomials have no dense counterpart.

        :param shift: the (ignored) shift
        :raises ValueError: always
        """
        ...

    @classmethod
    def monomial(cls, idx, value=1):
        """
        **LLM Docstring**

        Build a single-term polynomial for one monomial key.

        :param idx: the monomial key
        :param value: the coefficient
        :return: the monomial polynomial
        :rtype: PureMonicPolynomial
        """
        ...

    @classmethod
    def key_hash(cls, monomial_tuple):
        """
        **LLM Docstring**

        Cheap order-independent hash of a monomial key (sum of the per-index hashes),
        used to quickly test key equivalence.

        :param monomial_tuple: the monomial key
        :type monomial_tuple: tuple
        :return: the hash
        :rtype: int
        """
        ...

    @classmethod
    @abc.abstractmethod
    def canonical_key(cls, monomial_tuple):
        """
        **LLM Docstring**

        Abstract: put a monomial key into canonical (sorted) form so equivalent keys
        compare equal.

        :param monomial_tuple: the monomial key
        :type monomial_tuple: tuple
        :return: the canonicalized key
        :rtype: tuple
        """
        ...

    def direct_multiproduct(self, other, key_value_generator):
        """
        **LLM Docstring**

        Multiply with another monic polynomial using a generator that yields the
        `(key, value)` contributions for each pair of terms, merging canonicalized keys.

        :param other: the other polynomial
        :type other: PureMonicPolynomial
        :param key_value_generator: yields `(key, value)` pairs for each term pair
        :type key_value_generator: Callable
        :return: the product polynomial
        :rtype: PureMonicPolynomial
        :raises TypeError: if `other` isn't a monic polynomial
        """
        ...

    def direct_product(self, other, key_func=None, mul=None):
        """
        **LLM Docstring**

        Multiply with another monic polynomial (or scalar) using optional key-combining
        and value-multiplying callbacks, merging canonicalized keys.

        :param other: the other polynomial or a scalar
        :param key_func: combines two keys into the product key (concatenation by default)
        :type key_func: Callable | None
        :param mul: multiplies two coefficients (ordinary product by default)
        :type mul: Callable | None
        :return: the product polynomial
        :rtype: PureMonicPolynomial
        """
        ...

    def rebuild(self, new_terms, prefactor=None, canonicalize=None):
        """
        **LLM Docstring**

        Build a new polynomial of the same type from a term mapping, inheriting the
        prefactor by default.

        :param new_terms: the new term mapping
        :type new_terms: dict
        :param prefactor: the prefactor (inherited if omitted)
        :type prefactor: float | None
        :param canonicalize: canonicalize the keys (off by default)
        :type canonicalize: bool | None
        :return: the rebuilt polynomial
        :rtype: PureMonicPolynomial
        """
        ...

    def filter(self, keys, mode='match'):
        """
        **LLM Docstring**

        Filter the polynomial's terms by their monomial keys under one of three modes.

        :param keys: the keys to test against
        :param mode: `'match'` (exact key sets), `'include'` (only these keys), or `'exclude'`
        :type mode: str
        :return: the filtered polynomial
        :rtype: PureMonicPolynomial
        :raises ValueError: for an unknown mode
        """
        ...

    def _filter_exact(self, test_keys):
        """
        **LLM Docstring**

        Keep only the terms that contain every key in one of the required key sets (with
        multiplicity).

        :param test_keys: the required key sets
        :return: the filtered polynomial
        :rtype: PureMonicPolynomial
        """
        ...

    def _filter_include(self, test_keys):
        """
        **LLM Docstring**

        Keep only the terms whose monomial keys are all drawn from the allowed key set.

        :param test_keys: the allowed keys
        :return: the filtered polynomial
        :rtype: PureMonicPolynomial
        """
        ...

    def _filter_exclude(self, test_keys):
        """
        **LLM Docstring**

        Keep only the terms that contain none of the excluded keys.

        :param test_keys: the excluded keys
        :return: the filtered polynomial
        :rtype: PureMonicPolynomial
        """
        ...

    def __mul__(self, other):
        """
        **LLM Docstring**

        Multiply by another monic polynomial (or scalar) via `direct_product`.

        :param other: the multiplier
        :return: the product polynomial
        :rtype: PureMonicPolynomial
        """
        ...

class TensorCoefficientPoly(PureMonicPolynomial):
    """
    Represents a polynomial constructed using tensor elements as monomials
    by tracking sets of indices
    """

    @classmethod
    def canonical_key(cls, monomial_tuple):
        """
        **LLM Docstring**

        Canonicalize a monomial key of tensor-coefficient index tuples by grouping the
        index tuples by length and sorting within each length group.

        :param monomial_tuple: the monomial key (a tuple of index tuples)
        :type monomial_tuple: tuple
        :return: the canonicalized key
        :rtype: tuple
        """
        ...