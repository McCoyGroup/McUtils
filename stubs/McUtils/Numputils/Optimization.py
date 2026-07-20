import collections, abc
import functools
import numpy as np
import itertools
from .. import Devutils as dev
from . import VectorOps as vec_ops
from . import Misc as misc
from . import TransformationMatrices as tfs
from . import SetOps as set_ops
__all__ = ['iterative_step_minimize', 'iterative_chain_minimize', 'scipy_minimize', 'GradientDescentStepFinder', 'NewtonStepFinder', 'QuasiNewtonStepFinder', 'ConjugateGradientStepFinder', 'EigenvalueFollowingStepFinder', 'NudgedElasticBandStepFinder', 'jacobi_maximize', 'LineSearchRotationGenerator', 'GradientDescentRotationGenerator', 'OperatorMatrixRotationGenerator', 'displacement_localizing_rotation_generator', 'polyfit_maxima', 'polyfit_minima', 'polyfit_critical_points', 'peak_fit_maxiumum']
default_jacobian_step_finder = 'conjugate-gradient'
default_hessian_step_finder = 'newton'

def lookup_method_name(method):
    """
    **LLM Docstring**

    Map a step-finder method name to its class.

    :param method: the method name (e.g. `'newton'`, `'conjugate-gradient'`)
    :type method: str
    :return: the step-finder class, or `None` if the name is unknown
    :rtype: type | None
    """
    ...

def get_step_finder(spec, method=None, jacobian=None, hessian=None, **extra_init):
    """
    **LLM Docstring**

    Resolve a step-finder specification into a ready-to-call step-finder instance.

    Accepts a bare function (plus `method`/`jacobian`/`hessian`), a spec dict, or an
    already-built step finder. A method name is looked up via `lookup_method_name`,
    defaulting to the Newton finder when a Hessian is available and the
    conjugate-gradient finder otherwise.

    :param spec: a function, spec dict, or existing step finder
    :type spec: Callable | dict | object
    :param method: the optimization method name or class
    :type method: str | type | None
    :param jacobian: the gradient function
    :type jacobian: Callable | None
    :param hessian: the Hessian function
    :type hessian: Callable | None
    :param extra_init: extra keyword arguments forwarded to the finder constructor
    :return: the step-finder instance
    :rtype: object
    """
    ...
oscillation_overlap_cutoff_min = 0.95
oscillation_overlap_cutoff_max = 1.05

def iterative_step_minimize_step(step_predictor, guess, mask, tol, orthogonal_projector, orthogonal_projection_generator, region_constraints, unitary, max_displacement, max_displacement_norm, generate_rotation, prev_steps, max_gradient_error, termination_function, is_climbing):
    """
    **LLM Docstring**

    Take a single minimization step for the still-active members of a batch.

    Applies any orthogonal/unitary projector to the predicted step and gradient,
    caps the displacement, enforces region constraints, checks convergence (and any
    termination function), damps oscillating steps, and returns the accepted step
    together with the updated active mask.

    :param step_predictor: the step-finder producing `(step, gradient)`
    :type step_predictor: Callable
    :param guess: current parameters for the active members, shape `(batch, n)`
    :type guess: np.ndarray
    :param mask: indices of the active batch members
    :type mask: np.ndarray | tuple
    :param tol: gradient convergence tolerance
    :type tol: float
    :param orthogonal_projector: fixed projector applied to steps
    :type orthogonal_projector: np.ndarray | None
    :param orthogonal_projection_generator: per-guess projector generator
    :type orthogonal_projection_generator: Callable | None
    :param region_constraints: `(min, max)` bounds per coordinate
    :type region_constraints: np.ndarray | None
    :param unitary: constrain steps to the unit sphere
    :type unitary: bool
    :param max_displacement: cap on the max per-coordinate step
    :type max_displacement: float | None
    :param max_displacement_norm: cap on the step norm
    :type max_displacement_norm: float | None
    :param generate_rotation: also build the rotation for unitary steps (unsupported >3D)
    :type generate_rotation: bool
    :param prev_steps: recent steps, used for oscillation detection
    :type prev_steps: np.ndarray | None
    :param max_gradient_error: use the max-abs gradient (vs. its norm) as the error
    :type max_gradient_error: bool
    :param termination_function: optional early-termination predicate
    :type termination_function: Callable | None
    :param is_climbing: per-member climbing-image flags (for chain methods)
    :type is_climbing: np.ndarray | None
    :return: `(step, errors, new_mask, done)`
    :rtype: tuple
    """
    ...

def iterative_step_minimize(guess, step_predictor, jacobian=None, hessian=None, *, method=None, unitary=False, generate_rotation=False, dtype='float64', orthogonal_directions=None, orthogonal_projection_generator=None, region_constraints=None, function=None, max_displacement=None, max_displacement_norm=None, oscillation_damping_factor=None, termination_function=None, prevent_oscillations=None, tol=1e-08, use_max_for_error=True, max_iterations=100, convergence_metric=None, track_best=False, return_trajectory=False, logger=None, log_guess=True):
    """
    **LLM Docstring**

    Minimize a function over a batch of starting guesses by repeatedly applying a
    step finder until the gradient converges or the iteration cap is hit.

    Supports batched guesses, orthogonal/unitary projection, region constraints,
    oscillation damping, best-point tracking, and optional trajectory return. Each
    iteration only advances the members that have not yet converged.

    :param guess: starting guesses, shape `(..., n)`
    :type guess: np.ndarray
    :param step_predictor: a step finder, spec, or function
    :type step_predictor: Callable | dict | object
    :param jacobian: the gradient function
    :type jacobian: Callable | None
    :param hessian: the Hessian function
    :type hessian: Callable | None
    :param method: the optimization method name/class
    :type method: str | type | None
    :param unitary: constrain the optimization to the unit sphere
    :type unitary: bool
    :param generate_rotation: also return the accumulated unitary rotation
    :type generate_rotation: bool
    :param dtype: working dtype for the guesses
    :type dtype: str
    :param orthogonal_directions: directions to project out of every step
    :type orthogonal_directions: np.ndarray | None
    :param orthogonal_projection_generator: per-guess projector generator
    :type orthogonal_projection_generator: Callable | None
    :param region_constraints: `(min, max)` bounds per coordinate
    :type region_constraints: np.ndarray | None
    :param function: the objective (needed for best-value tracking)
    :type function: Callable | None
    :param max_displacement: cap on the max per-coordinate step
    :type max_displacement: float | None
    :param max_displacement_norm: cap on the step norm
    :type max_displacement_norm: float | None
    :param oscillation_damping_factor: adaptive damping factor for oscillating steps
    :type oscillation_damping_factor: float | None
    :param termination_function: optional early-termination predicate
    :type termination_function: Callable | None
    :param prevent_oscillations: keep this many prior steps for oscillation detection
    :type prevent_oscillations: bool | int | None
    :param tol: gradient convergence tolerance
    :type tol: float
    :param use_max_for_error: use max-abs gradient rather than its norm as the error
    :type use_max_for_error: bool
    :param max_iterations: maximum number of iterations
    :type max_iterations: int
    :param convergence_metric: unused placeholder
    :type convergence_metric: Callable | None
    :param track_best: keep the best point/value seen per member
    :type track_best: bool
    :param return_trajectory: also return the per-iteration trajectory
    :type return_trajectory: bool
    :param logger: optional logger
    :type logger: object | None
    :param log_guess: log the guess at each iteration
    :type log_guess: bool
    :return: `(result, converged, (errors, iterations))` (plus trajectory if requested)
    :rtype: tuple
    """
    ...
scipy_no_hessian_methods = {'cg', 'bfgs'}
scipy_no_grad_methods = {'nelder-mead'}
use_scipy_linesearch = False

def scipy_minimize(coords, function, jacobian=None, hessian=None, optimizer_settings=None, unitary=True, orthogonal_projector=None, orthogonal_projection_generator=None, line_search=None, return_trajectory=False, method='bfgs', max_iterations=None, tol=1e-08, line_search_step=None, max_displacement=0.01, region_constraints=None, logger=None):
    """
    **LLM Docstring**

    Minimize a function with `scipy.optimize.minimize`, wired up for this module's
    conventions (batched-style flattening, optional unitary/orthogonal projection,
    displacement capping, trajectory logging).

    When line search is disabled, `scipy`'s Wolfe line search is temporarily
    monkey-patched with a fixed-max-displacement step so each step size is bounded.

    :param coords: the starting coordinates
    :type coords: np.ndarray
    :param function: the objective function
    :type function: Callable
    :param jacobian: the gradient function
    :type jacobian: Callable | None
    :param hessian: the Hessian function
    :type hessian: Callable | None
    :param optimizer_settings: extra options passed through to `scipy`
    :type optimizer_settings: dict | None
    :param unitary: apply a unit-sphere projection to the gradient
    :type unitary: bool
    :param orthogonal_projector: fixed projector applied to the gradient
    :type orthogonal_projector: np.ndarray | None
    :param orthogonal_projection_generator: per-guess projector generator
    :type orthogonal_projection_generator: Callable | None
    :param line_search: whether to use `scipy`'s line search (else fixed steps)
    :type line_search: bool | None
    :param return_trajectory: also return the optimization trajectory
    :type return_trajectory: bool
    :param method: the `scipy` method (`'quasi-newton'` maps to BFGS)
    :type method: str
    :param max_iterations: maximum iterations
    :type max_iterations: int | None
    :param tol: gradient tolerance
    :type tol: float
    :param line_search_step: fixed step to return when line search is off
    :type line_search_step: float | None
    :param max_displacement: cap on the max per-coordinate step
    :type max_displacement: float
    :param region_constraints: per-coordinate bounds
    :type region_constraints: dict | None
    :param logger: optional logger
    :type logger: object | None
    :return: `(success, result[, scipy_result])`, with a trajectory when requested
    :rtype: tuple
    """
    ...

def _find_peak(v):
    """
    **LLM Docstring**

    Return the index of the maximum-energy image in a chain (the transition-state
    guess).

    :param v: the per-image values
    :type v: np.ndarray
    :return: the index of the peak
    :rtype: int
    """
    ...
default_chain_step_finder = 'neb'

def iterative_chain_minimize(chain_guesses, step_predictors, jacobian=None, hessian=None, *, method=None, unitary=False, function=None, climb=None, climbing_nodes=None, climbing_node_identifier=None, generate_rotation=False, dtype='float64', orthogonal_directions=None, orthogonal_projection_generator=None, prevent_oscillations=None, region_constraints=None, convergence_metric=None, termination_function=None, reparametrizer=None, max_displacement=None, max_displacement_norm=None, tol=1e-08, max_iterations=100, use_max_for_error=True, periodic=False, reembed=None, embedding_options=None, fixed_images=None, return_trajectory=False, logger=None, log_guess=False):
    """
    **LLM Docstring**

    Minimize a chain of images (e.g. a reaction path) by applying per-image step
    finders, with optional climbing-image, spring/NEB, reparametrization, and
    re-embedding support.

    Generalizes `iterative_step_minimize` to a `(batch, n_images, n)` chain: each
    image is stepped by its own step finder (which sees its neighbours through the
    chain step-finder wrappers), climbing images are handled specially, and the
    chain can be reparametrized/re-embedded between iterations.

    :param chain_guesses: the initial chain(s), shape `(..., n_images, n)`
    :type chain_guesses: np.ndarray
    :param step_predictors: one step finder (broadcast) or one per image
    :type step_predictors: Callable | Iterable
    :param jacobian: the per-image gradient function
    :type jacobian: Callable | None
    :param hessian: the per-image Hessian function
    :type hessian: Callable | None
    :param method: the optimization method name/class
    :type method: str | type | None
    :param unitary: constrain images to the unit sphere
    :type unitary: bool
    :param function: the image objective (for climbing detection / tracking)
    :type function: Callable | None
    :param climb: enable climbing-image behavior
    :type climb: bool | None
    :param climbing_nodes: explicit climbing-image indices
    :type climbing_nodes: Iterable[int] | None
    :param climbing_node_identifier: callable choosing the climbing image(s)
    :type climbing_node_identifier: Callable | None
    :param generate_rotation: also return unitary rotations (unsupported)
    :type generate_rotation: bool
    :param dtype: working dtype
    :type dtype: str
    :param orthogonal_directions: directions to project out of every step
    :type orthogonal_directions: np.ndarray | None
    :param orthogonal_projection_generator: per-guess projector generator
    :type orthogonal_projection_generator: Callable | None
    :param prevent_oscillations: oscillation-detection history length
    :type prevent_oscillations: bool | int | None
    :param region_constraints: per-coordinate bounds
    :type region_constraints: np.ndarray | None
    :param convergence_metric: unused placeholder
    :type convergence_metric: Callable | None
    :param termination_function: optional early-termination predicate
    :type termination_function: Callable | None
    :param reparametrizer: callable redistributing images along the path
    :type reparametrizer: Callable | None
    :param max_displacement: cap on the max per-coordinate step
    :type max_displacement: float | None
    :param max_displacement_norm: cap on the step norm
    :type max_displacement_norm: float | None
    :param tol: gradient convergence tolerance
    :type tol: float
    :param max_iterations: maximum iterations
    :type max_iterations: int
    :param use_max_for_error: use max-abs gradient rather than its norm as the error
    :type use_max_for_error: bool
    :param periodic: treat the chain as periodic (wrap endpoints)
    :type periodic: bool
    :param reembed: re-embed images between iterations
    :type reembed: bool | None
    :param embedding_options: options for the re-embedding
    :type embedding_options: dict | None
    :param fixed_images: image indices to hold fixed (e.g. endpoints)
    :type fixed_images: Iterable[int] | None
    :param return_trajectory: also return the trajectory
    :type return_trajectory: bool
    :param logger: optional logger
    :type logger: object | None
    :param log_guess: log each image guess
    :type log_guess: bool
    :return: `(chain, converged, (errors, iterations))` (plus trajectory if requested)
    :rtype: tuple
    """
    ...

class Damper:

    def __init__(self, damping_parameter=None, damping_exponent=None, restart_interval=10):
        """
        **LLM Docstring**

        Set up a step damper with a (possibly decaying) damping factor.

        :param damping_parameter: base damping factor (`None` disables damping)
        :type damping_parameter: float | None
        :param damping_exponent: exponent applied to grow/decay the factor over iterations
        :type damping_exponent: float | None
        :param restart_interval: iteration count after which the decay resets
        :type restart_interval: int
        """
        ...

    def get_damping_factor(self):
        """
        **LLM Docstring**

        Return the current damping factor, advancing (and periodically resetting) the
        internal iteration counter.

        :return: the damping factor, or `None` if damping is disabled
        :rtype: float | None
        """
        ...

class LineSearcher(metaclass=abc.ABCMeta):
    """
    Adapted from scipy.optimize to handle multiple structures at once
    """

    def __init__(self, func, min_alpha=0, **opts):
        """
        **LLM Docstring**

        Initialize a line searcher around an objective function.

        :param func: the objective, called as `func(points, mask)`
        :type func: Callable
        :param min_alpha: minimum allowed step length
        :type min_alpha: float
        :param opts: default options forwarded to the search
        """
        ...

    @abc.abstractmethod
    def check_scalar_converged(self, phi_vals, alphas, **opts):
        """
        **LLM Docstring**

        Abstract: test whether the line-search values satisfy the convergence criterion.

        :param phi_vals: objective values along the search direction
        :type phi_vals: np.ndarray
        :param alphas: current step lengths
        :type alphas: np.ndarray
        :return: a boolean convergence mask
        :rtype: np.ndarray
        """
        ...

    @abc.abstractmethod
    def update_alphas(self, phi_vals, alphas, iteration, old_phi_vals, old_alphas_vals, mask, **opts):
        """
        **LLM Docstring**

        Abstract: propose new step lengths for the next line-search iteration.

        :param phi_vals: current objective values
        :type phi_vals: np.ndarray
        :param alphas: current step lengths
        :type alphas: np.ndarray
        :param iteration: the line-search iteration index
        :type iteration: int
        :param old_phi_vals: recent historical objective values
        :type old_phi_vals: list | None
        :param old_alphas_vals: recent historical step lengths
        :type old_alphas_vals: list | None
        :param mask: indices of the active members
        :type mask: np.ndarray
        :return: the updated step lengths
        :rtype: np.ndarray
        """
        ...
    default_alpha = 0.001

    def get_default_alpha(self, am):
        """
        **LLM Docstring**

        Return the fallback step length used when the line search fails to converge.

        :param am: the current step lengths for the unconverged members
        :type am: np.ndarray
        :return: the default step lengths
        :rtype: np.ndarray
        """
        ...

    def scalar_search(self, scalar_func, guess_alpha, min_alpha=None, max_iterations=15, history_length=1, **opts):
        """
        **LLM Docstring**

        Run the 1-D line search: iteratively update step lengths until each member's
        objective along the search direction meets the convergence test (or the
        iteration cap is hit).

        :param scalar_func: the directional objective `phi(alphas, mask)`
        :type scalar_func: Callable
        :param guess_alpha: initial step length(s)
        :type guess_alpha: np.ndarray
        :param min_alpha: minimum allowed step length
        :type min_alpha: float | None
        :param max_iterations: maximum line-search iterations
        :type max_iterations: int
        :param history_length: how many past iterations to retain
        :type history_length: int
        :param opts: extra options forwarded to the convergence/update hooks
        :return: `(alphas, (phi_vals, is_converged))`
        :rtype: tuple
        """
        ...

    def prep_search(self, initial_geom, search_dir, guess_alpha=1, **opts):
        """
        **LLM Docstring**

        Prepare the line search: build the initial step length, the option dict, and
        the directional objective function.

        :param initial_geom: the base points
        :type initial_geom: np.ndarray
        :param search_dir: the search directions
        :type search_dir: np.ndarray
        :param guess_alpha: initial step length
        :type guess_alpha: float
        :param opts: extra options
        :return: `(guess_alpha, opts, phi)`
        :rtype: tuple
        """
        ...

    @classmethod
    def _dir_func(cls, func, initial_geom, search_dir):
        """
        **LLM Docstring**

        Build the directional objective `phi(alphas, mask) = func(geom + alpha *
        search_dir)`.

        :param func: the objective function
        :type func: Callable
        :param initial_geom: the base points
        :type initial_geom: np.ndarray
        :param search_dir: the search directions
        :type search_dir: np.ndarray
        :return: the directional objective
        :rtype: Callable
        """
        ...

    def __call__(self, initial_geom, search_dir, **base_opts):
        """
        **LLM Docstring**

        Run the line search for the given points and search directions.

        :param initial_geom: the base points
        :type initial_geom: np.ndarray
        :param search_dir: the search directions
        :type search_dir: np.ndarray
        :param base_opts: extra options merged over the searcher defaults
        :return: `(alphas, (phi_vals, is_converged))`
        :rtype: tuple
        """
        ...

class ArmijoSearch(LineSearcher):

    def __init__(self, func, c1=0.0001, min_alpha=None, fixed_step_cutoff=1e-08, der_max=100.0, guess_alpha=1):
        """
        **LLM Docstring**

        Initialize an Armijo (sufficient-decrease) line search.

        :param func: the objective function
        :type func: Callable
        :param c1: the Armijo sufficient-decrease parameter
        :type c1: float
        :param min_alpha: minimum allowed step length
        :type min_alpha: float | None
        :param fixed_step_cutoff: gradient magnitude below which a unit step is used
        :type fixed_step_cutoff: float | None
        :param der_max: cap on the magnitude of the directional derivative
        :type der_max: float
        :param guess_alpha: initial step length
        :type guess_alpha: float
        """
        ...

    def prep_search(self, initial_geom, search_dir, *, initial_grad, min_alpha=None, **rest):
        """
        **LLM Docstring**

        Prepare the Armijo search: compute (and clip) the initial directional
        derivative and the baseline objective value, and pick the starting step length.

        :param initial_geom: the base points
        :type initial_geom: np.ndarray
        :param search_dir: the search directions
        :type search_dir: np.ndarray
        :param initial_grad: the gradient at the base points
        :type initial_grad: np.ndarray
        :param min_alpha: minimum allowed step length
        :type min_alpha: float | None
        :param rest: extra options forwarded to the base preparation
        :return: `(guess_alpha, opts, phi)`
        :rtype: tuple
        """
        ...
    converged_tolerance = 1e-08

    def check_scalar_converged(self, phi_vals, alphas, *, phi0, c1, derphi0, tol=None):
        """
        **LLM Docstring**

        Apply the Armijo sufficient-decrease test `phi(a) <= phi0 + c1 * a * derphi0`.

        :param phi_vals: objective values along the search direction
        :type phi_vals: np.ndarray
        :param alphas: current step lengths
        :type alphas: np.ndarray
        :param phi0: baseline objective value
        :type phi0: np.ndarray
        :param c1: sufficient-decrease parameter
        :type c1: float
        :param derphi0: baseline directional derivative
        :type derphi0: np.ndarray
        :param tol: comparison tolerance
        :type tol: float | None
        :return: the convergence mask
        :rtype: np.ndarray
        """
        ...

    def get_default_alpha(self, am, *, phi0, **etc):
        """
        **LLM Docstring**

        Return the fallback step length (scaled by the inverse baseline value) when the
        Armijo search fails to converge.

        :param am: current step lengths for the unconverged members
        :type am: np.ndarray
        :param phi0: baseline objective value
        :type phi0: np.ndarray
        :return: the default step lengths
        :rtype: np.ndarray
        """
        ...

    def update_alphas(self, phi_vals, alphas, iteration, old_phi_vals, old_alphas_vals, mask, *, phi0, c1, derphi0, zero_cutoff=1e-16):
        """
        **LLM Docstring**

        Propose the next Armijo step length by quadratic (first iteration) then cubic
        (subsequent) interpolation of the objective along the search direction, with
        safeguards that halve the step when the interpolation misbehaves.

        :param phi_vals: current objective values
        :type phi_vals: np.ndarray
        :param alphas: current step lengths
        :type alphas: np.ndarray
        :param iteration: the line-search iteration index
        :type iteration: int
        :param old_phi_vals: recent historical objective values
        :type old_phi_vals: list
        :param old_alphas_vals: recent historical step lengths
        :type old_alphas_vals: list
        :param mask: indices of the active members
        :type mask: np.ndarray
        :param phi0: baseline objective value
        :type phi0: np.ndarray
        :param c1: sufficient-decrease parameter
        :type c1: float
        :param derphi0: baseline directional derivative
        :type derphi0: np.ndarray
        :param zero_cutoff: small-denominator guard
        :type zero_cutoff: float
        :return: the updated step lengths
        :rtype: np.ndarray
        """
        ...

class _WolfeLineSearch(LineSearcher):
    """
    Adapted from scipy.optimize
    """

    def __init__(self, func, grad, **opts):
        """
        **LLM Docstring**

        Initialize a Wolfe-condition line search (which also needs the gradient).

        :param func: the objective function
        :type func: Callable
        :param grad: the gradient function
        :type grad: Callable
        :param opts: default options
        """
        ...

    @classmethod
    def _grad_func(cls, jac, initial_geom, search_dir):
        """
        **LLM Docstring**

        Build the directional-derivative function `derphi(alphas, mask)` from the
        gradient along the search direction.

        :param jac: the gradient function
        :type jac: Callable
        :param initial_geom: the base points
        :type initial_geom: np.ndarray
        :param search_dir: the search directions
        :type search_dir: np.ndarray
        :return: the directional-derivative function
        :rtype: Callable
        """
        ...

    def prep_search(self, initial_geom, search_dir):
        """
        **LLM Docstring**

        Prepare the Wolfe search (not yet implemented).

        :param initial_geom: the base points
        :type initial_geom: np.ndarray
        :param search_dir: the search directions
        :type search_dir: np.ndarray
        :raises NotImplementedError: always
        """
        ...

    def check_scalar_converged(self, phi_vals, alphas, **opts):
        """
        **LLM Docstring**

        Wolfe convergence test (not yet implemented).

        :param phi_vals: objective values
        :type phi_vals: np.ndarray
        :param alphas: step lengths
        :type alphas: np.ndarray
        """
        ...

class GradientDescentStepFinder:
    supports_hessian = False
    line_search = ArmijoSearch

    def __init__(self, func, jacobian, damping_parameter=None, damping_exponent=None, line_search=True, restart_interval=10, logger=None):
        """
        **LLM Docstring**

        Initialize a gradient-descent step finder.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param damping_parameter: base step-damping factor
        :type damping_parameter: float | None
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float | None
        :param line_search: `True` to use the default line search, `False`/`None` to disable
        :type line_search: bool | Callable
        :param restart_interval: damping restart interval
        :type restart_interval: int
        :param logger: optional logger
        :type logger: object | None
        """
        ...

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce a gradient-descent step (the negative gradient, optionally projected,
        line-searched, and damped) for the active members.

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices (or `(mask, chain_data)` for chain minimizers)
        :type mask: np.ndarray | tuple
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        ...

class NetwonDirectHessianGenerator:
    line_search = ArmijoSearch

    def __init__(self, func, jacobian, hessian, hess_mode='direct', line_search=True, damping_parameter=None, damping_exponent=None, restart_interval=10):
        """
        **LLM Docstring**

        Initialize a direct-Hessian Newton step generator.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param hessian: the Hessian function
        :type hessian: Callable
        :param hess_mode: `'direct'` (invert the Hessian) or `'inverse'` (already inverse)
        :type hess_mode: str
        :param line_search: line-search setting
        :type line_search: bool | Callable
        :param damping_parameter: step-damping factor
        :type damping_parameter: float | None
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float | None
        :param restart_interval: damping restart interval
        :type restart_interval: int
        """
        ...

    def wrap_hessian(self, func, mode):
        """
        **LLM Docstring**

        Wrap the Hessian function so it returns the (inverse) Hessian in the form the
        step generator expects.

        :param func: the Hessian (or inverse-Hessian) function
        :type func: Callable
        :param mode: `'direct'` to invert the Hessian, otherwise pass through
        :type mode: str
        :return: a function returning the inverse Hessian
        :rtype: Callable
        """
        ...

    def __call__(self, guess, mask, return_vals=False, projector=None):
        """
        **LLM Docstring**

        Produce the Newton step `-H⁻¹ g` (optionally projected, line-searched, damped).

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param return_vals: unsupported
        :type return_vals: bool
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        ...

class NewtonStepFinder:
    supports_hessian = True

    def __init__(self, func, jacobian=None, hessian=None, *, check_generator=True, logger=None, **generator_opts):
        """
        **LLM Docstring**

        Initialize a Newton step finder, building a direct-Hessian generator from the
        supplied Jacobian/Hessian unless one is already provided.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function (or a ready generator)
        :type jacobian: Callable | None
        :param hessian: the Hessian function
        :type hessian: Callable | None
        :param check_generator: build a generator when needed
        :type check_generator: bool
        :param logger: optional logger
        :type logger: object | None
        :param generator_opts: extra options for the generator
        """
        ...

    @classmethod
    def _prep_generator(cls, func, jac, hess, opts):
        """
        **LLM Docstring**

        Return a step generator for the Newton method, requiring a Hessian (or a func
        that already exposes `jacobian`/`hessian_inverse`).

        :param func: the objective function
        :type func: Callable
        :param jac: the gradient function
        :type jac: Callable
        :param hess: the Hessian function
        :type hess: Callable | None
        :param opts: extra generator options
        :type opts: dict
        :return: the step generator
        :rtype: object
        """
        ...

    def __call__(self, guess, mask, return_vals=False, projector=None):
        """
        **LLM Docstring**

        Produce a Newton step for the active members.

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices (or chain-minimizer tuple)
        :type mask: np.ndarray | tuple
        :param return_vals: unsupported
        :type return_vals: bool
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        ...

class QuasiNewtonStepFinder:
    supports_hessian = False

    def __init__(self, func, jacobian, approximation_type='bfgs', logger=None, **generator_opts):
        """
        **LLM Docstring**

        Initialize a quasi-Newton step finder, selecting the Hessian-approximation
        scheme by name.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param approximation_type: the approximator name (e.g. `'bfgs'`, `'sr1'`)
        :type approximation_type: str
        :param logger: optional logger
        :type logger: object | None
        :param generator_opts: extra options for the approximator
        """
        ...

    @classmethod
    def get_hessian_approximations(cls):
        """
        **LLM Docstring**

        Return the mapping from approximation name to Hessian-approximator class.

        :return: the name-to-class mapping
        :rtype: dict
        """
        ...

    @property
    def hessian_approximations(self):
        """
        **LLM Docstring**

        The mapping from approximation name to Hessian-approximator class.

        :return: the name-to-class mapping
        :rtype: dict
        """
        ...

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce a quasi-Newton step for the active members via the chosen approximator.

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices (or chain-minimizer tuple)
        :type mask: np.ndarray | tuple
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        ...

class QuasiNetwonHessianApproximator:
    orthogonal_dirs_cutoff = 1e-16
    line_search = ArmijoSearch

    def __init__(self, func, jacobian, initial_beta=1, damping_parameter=None, damping_exponent=None, line_search=True, restart_interval=10, restart_hessian_norm=1e-12, approximation_mode='inverse'):
        """
        **LLM Docstring**

        Initialize a quasi-Newton Hessian approximator, tracking the previous
        gradient/step/Hessian across iterations.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param initial_beta: initial (inverse) Hessian scale
        :type initial_beta: float
        :param damping_parameter: step-damping factor
        :type damping_parameter: float | None
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float | None
        :param line_search: line-search setting
        :type line_search: bool | Callable
        :param restart_interval: damping restart interval
        :type restart_interval: int
        :param restart_hessian_norm: step-norm below which the Hessian is reset
        :type restart_hessian_norm: float
        :param approximation_mode: `'direct'` (Hessian) or `'inverse'` (inverse Hessian)
        :type approximation_mode: str
        """
        ...

    def identities(self, guess, mask):
        """
        **LLM Docstring**

        Return (cached) identity matrices matching the active members' shape.

        :param guess: the current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :return: the identity tensors
        :rtype: np.ndarray
        """
        ...

    def initialize_hessians(self, guess, mask):
        """
        **LLM Docstring**

        Return the initial (inverse) Hessian estimate (a scaled identity).

        :param guess: the current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :return: the initial Hessian estimate
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def take_nonzero_norm_regions(cls, norms, tensors, cutoff=None):
        """
        **LLM Docstring**

        Select the members whose supplied norms are all above a cutoff, returning their
        indices and the correspondingly filtered tensors (to avoid divide-by-zero in the
        Hessian update).

        :param norms: the norm arrays that must be nonzero
        :type norms: list[np.ndarray]
        :param tensors: tensors to filter to the safe members
        :type tensors: list[np.ndarray]
        :param cutoff: the nonzero cutoff
        :type cutoff: float | None
        :return: `(good_positions, filtered_tensors)`
        :rtype: tuple
        """
        ...

    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Abstract: compute the updated (inverse) Hessian from the gradient/step
        differences.

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous (inverse) Hessian
        :type prev_hess: np.ndarray
        :return: the updated Hessian
        :rtype: np.ndarray
        """
        ...

    def get_jacobian_updates(self, guess, mask, gradient_modifer=None):
        """
        **LLM Docstring**

        Evaluate the current gradient and its difference from the previous gradient.

        :param guess: the current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :return: `(new_jacobians, jacobian_differences)`
        :rtype: tuple
        """
        ...

    def restart_hessian_approximation(self):
        """
        **LLM Docstring**

        Decide whether to reset the Hessian approximation (on a near-zero previous step
        or a numerical blow-up).

        :return: whether to restart
        :rtype: bool
        """
        ...

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce a quasi-Newton step: update the (inverse) Hessian, form the step `-B g`,
        optionally project/line-search/damp it, and cache the state for the next
        iteration.

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        ...

class BFGSApproximator(QuasiNetwonHessianApproximator):
    orthogonal_dirs_cutoff = 1e-16

    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Compute the BFGS (inverse) Hessian update from the gradient and step
        differences, guarding against zero curvature.

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous (inverse) Hessian
        :type prev_hess: np.ndarray
        :return: the updated Hessian
        :rtype: np.ndarray
        """
        ...

class DFPApproximator(QuasiNetwonHessianApproximator):
    orthogonal_dirs_cutoff = 1e-08

    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Compute the DFP (Davidon-Fletcher-Powell) (inverse) Hessian update.

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous (inverse) Hessian
        :type prev_hess: np.ndarray
        :return: the updated Hessian
        :rtype: np.ndarray
        """
        ...

class BroydenApproximator(QuasiNetwonHessianApproximator):
    orthogonal_dirs_cutoff = 1e-08

    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Compute the (good) Broyden (inverse) Hessian update.

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous (inverse) Hessian
        :type prev_hess: np.ndarray
        :return: the updated Hessian
        :rtype: np.ndarray
        """
        ...

class SR1Approximator(QuasiNetwonHessianApproximator):
    orthogonal_dirs_cutoff = 1e-08

    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Compute the symmetric-rank-one (SR1) (inverse) Hessian update.

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous (inverse) Hessian
        :type prev_hess: np.ndarray
        :return: the updated Hessian
        :rtype: np.ndarray
        """
        ...

class CompactQuasiNewtonApproximator(QuasiNetwonHessianApproximator):

    @classmethod
    def get_direct_hessian_update_vector(cls, H, dx, y):
        """
        **LLM Docstring**

        Abstract: the update vector for the direct (Hessian) form of a compact
        quasi-Newton update.

        :param H: the current Hessian
        :type H: np.ndarray
        :param dx: the step
        :type dx: np.ndarray
        :param y: the gradient difference
        :type y: np.ndarray
        :return: the update vector
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def get_inverse_hessian_update_vector(cls, H, dx, y):
        """
        **LLM Docstring**

        Abstract: the update vector for the inverse form of a compact quasi-Newton
        update.

        :param H: the current inverse Hessian
        :type H: np.ndarray
        :param dx: the step
        :type dx: np.ndarray
        :param y: the gradient difference
        :type y: np.ndarray
        :return: the update vector
        :rtype: np.ndarray
        """
        ...

    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Compute the compact quasi-Newton (inverse) Hessian update from a subclass-
        supplied update vector (the shared PSB/Greenstadt-style rank-two form).

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous (inverse) Hessian
        :type prev_hess: np.ndarray
        :return: the updated Hessian
        :rtype: np.ndarray
        """
        ...

class PSBQuasiNewtonApproximator(CompactQuasiNewtonApproximator):

    @classmethod
    def get_direct_hessian_update_vector(cls, H, dx, y):
        """
        **LLM Docstring**

        Not supported: PSB only implements the inverse update.

        :param H: the current Hessian
        :param dx: the step
        :param y: the gradient difference
        :raises NotImplementedError: always
        """
        ...

    @classmethod
    def get_inverse_hessian_update_vector(cls, H, dx, y):
        """
        **LLM Docstring**

        The PSB (Powell symmetric Broyden) update vector, which is simply the step.

        :param H: the current inverse Hessian
        :type H: np.ndarray
        :param dx: the step
        :type dx: np.ndarray
        :param y: the gradient difference
        :type y: np.ndarray
        :return: the update vector (the step)
        :rtype: np.ndarray
        """
        ...

class GreenstadtNewtonApproximator(CompactQuasiNewtonApproximator):

    @classmethod
    def get_direct_hessian_update_vector(cls, H, dx, y):
        """
        **LLM Docstring**

        The Greenstadt update vector for the direct form (the gradient difference).

        :param H: the current Hessian
        :type H: np.ndarray
        :param dx: the step
        :type dx: np.ndarray
        :param y: the gradient difference
        :type y: np.ndarray
        :return: the update vector
        :rtype: np.ndarray
        """
        ...

    @classmethod
    def get_inverse_hessian_update_vector(cls, H, dx, y):
        """
        **LLM Docstring**

        Not supported: Greenstadt only implements the direct update.

        :param H: the current inverse Hessian
        :param dx: the step
        :param y: the gradient difference
        :raises NotImplementedError: always
        """
        ...

class WeightedQuasiNewtonApproximator(QuasiNetwonHessianApproximator):
    base_approximators = None

    def __init__(self, func, jacobian, initial_beta=1, damping_parameter=None, damping_exponent=None, line_search=True, restart_interval=10, restart_hessian_norm=1e-05, approximation_mode='direct'):
        """
        **LLM Docstring**

        Initialize a weighted quasi-Newton approximator that blends several base
        approximators by per-member weights.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param initial_beta: initial (inverse) Hessian scale
        :type initial_beta: float
        :param damping_parameter: step-damping factor
        :type damping_parameter: float | None
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float | None
        :param line_search: line-search setting
        :type line_search: bool | Callable
        :param restart_interval: damping restart interval
        :type restart_interval: int
        :param restart_hessian_norm: step-norm reset threshold
        :type restart_hessian_norm: float
        :param approximation_mode: `'direct'` or `'inverse'`
        :type approximation_mode: str
        """
        ...

    def get_direct_weights(self, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Abstract: the blending weights for the direct-form base updates.

        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous Hessian
        :type prev_hess: np.ndarray
        :return: the per-approximator weights
        :rtype: np.ndarray
        """
        ...

    def get_inverse_weights(self, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Abstract: the blending weights for the inverse-form base updates.

        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous inverse Hessian
        :type prev_hess: np.ndarray
        :return: the per-approximator weights
        :rtype: np.ndarray
        """
        ...

    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Compute a weighted average of the base approximators' Hessian updates.

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous (inverse) Hessian
        :type prev_hess: np.ndarray
        :return: the weighted Hessian update
        :rtype: np.ndarray
        """
        ...

class BofillApproximator(WeightedQuasiNewtonApproximator):
    base_approximators = [SR1Approximator, PSBQuasiNewtonApproximator]

    def get_direct_weights(self, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Not supported: the Bofill blend is only defined for the inverse form here.

        :param jacobian_diffs: gradient differences
        :param prev_steps: previous steps
        :param prev_hess: previous Hessian
        :raises NotImplementedError: always
        """
        ...

    @classmethod
    def get_psi(self, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Compute the Bofill mixing parameter psi (the SR1/PSB blend weight) from the
        step and gradient-difference geometry.

        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous Hessian
        :type prev_hess: np.ndarray
        :return: the psi weights
        :rtype: np.ndarray
        """
        ...

    def get_inverse_weights(self, jacobian_diffs, prev_steps, prev_hess):
        """
            **LLM Docstring**

            Return the Bofill blend weights `[psi, 1 - psi]` over its two base
            approximators.

            :param jacobian_diffs: gradient differences
            :type jacobian_diffs: np.ndarray
            :param prev_steps: previous steps
            :type prev_steps: np.ndarray
            :param prev_hess: previous Hessian
            :type prev_hess: np.ndarray
            :return: the two blend weights
            :rtype: list[np.ndarray]
            """
        ...

class SchelgelApproximator(BofillApproximator):
    base_approximators = [SR1Approximator, BFGSApproximator]

    def get_direct_weights(self, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Not supported: the Schlegel blend is only defined for the inverse form here.

        :param jacobian_diffs: gradient differences
        :param prev_steps: previous steps
        :param prev_hess: previous Hessian
        :raises NotImplementedError: always
        """
        ...

    def get_psi(self, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Compute the Schlegel mixing parameter (the square root of the Bofill psi).

        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous Hessian
        :type prev_hess: np.ndarray
        :return: the psi weights
        :rtype: np.ndarray
        """
        ...

    def get_inverse_weights(self, jacobian_diffs, prev_steps, prev_hess):
        """
            **LLM Docstring**

            Return the Schlegel blend weights `[psi, 1 - psi]`.

            :param jacobian_diffs: gradient differences
            :type jacobian_diffs: np.ndarray
            :param prev_steps: previous steps
            :type prev_steps: np.ndarray
            :param prev_hess: previous Hessian
            :type prev_hess: np.ndarray
            :return: the two blend weights
            :rtype: list[np.ndarray]
            """
        ...

class ConjugateGradientStepFinder:
    supports_hessian = False

    def __init__(self, func, jacobian, approximation_type='polak-ribiere', logger=None, **generator_opts):
        """
        **LLM Docstring**

        Initialize a conjugate-gradient step finder, selecting the beta formula by name.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param approximation_type: beta scheme (`'polak-ribiere'` or `'fletcher-reeves'`)
        :type approximation_type: str
        :param logger: optional logger
        :type logger: object | None
        :param generator_opts: extra options for the step approximator
        """
        ...

    @property
    def beta_approximations(self):
        """
        **LLM Docstring**

        Return the mapping from beta-formula name to its approximator class.

        :return: the name-to-class mapping
        :rtype: dict
        """
        ...

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce a conjugate-gradient step for the active members.

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices (or chain-minimizer tuple)
        :type mask: np.ndarray | tuple
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        ...

class ConjugateGradientStepApproximator:
    line_search = ArmijoSearch

    def __init__(self, func, jacobian, damping_parameter=None, damping_exponent=None, restart_interval=50, restart_parameter=0.9, line_search=True):
        """
        **LLM Docstring**

        Initialize a conjugate-gradient step approximator, tracking the previous
        gradient and search direction.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param damping_parameter: step-damping factor
        :type damping_parameter: float | None
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float | None
        :param restart_interval: iterations between forced restarts
        :type restart_interval: int
        :param restart_parameter: Powell-style restart threshold on gradient overlap
        :type restart_parameter: float
        :param line_search: line-search setting
        :type line_search: bool | Callable
        """
        ...

    def get_beta(self, new_jacs, prev_jac, prev_step_dir):
        """
        **LLM Docstring**

        Abstract: compute the conjugate-gradient beta coefficient.

        :param new_jacs: the current gradient
        :type new_jacs: np.ndarray
        :param prev_jac: the previous gradient
        :type prev_jac: np.ndarray
        :param prev_step_dir: the previous search direction
        :type prev_step_dir: np.ndarray
        :return: the beta coefficient
        :rtype: np.ndarray
        """
        ...

    def determine_restart(self, new_jacs, mask):
        """
        **LLM Docstring**

        Decide whether to restart the conjugate-gradient direction (on the first step or
        when successive gradients are insufficiently orthogonal, Powell's criterion).

        :param new_jacs: the current gradient
        :type new_jacs: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :return: whether to restart
        :rtype: bool
        """
        ...

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce a conjugate-gradient step: form `-g + beta * previous_direction` (or a
        plain steepest-descent step on restart), then optionally project/line-search/damp
        and cache the state.

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        ...

class FletcherReevesApproximator(ConjugateGradientStepApproximator):

    def get_beta(self, new_jacs, prev_jac, prev_step_dir):
        """
        **LLM Docstring**

        Compute the Fletcher-Reeves beta (ratio of current to previous squared gradient
        norms).

        :param new_jacs: the current gradient
        :type new_jacs: np.ndarray
        :param prev_jac: the previous gradient
        :type prev_jac: np.ndarray
        :param prev_step_dir: the previous search direction
        :type prev_step_dir: np.ndarray
        :return: the beta coefficient
        :rtype: np.ndarray
        """
        ...

class PolakRibiereApproximator(ConjugateGradientStepApproximator):

    def get_beta(self, new_jacs, prev_jac, prev_step_dir):
        """
        **LLM Docstring**

        Compute the Polak-Ribiere beta (current gradient dotted with the gradient
        difference, over the previous squared gradient norm).

        :param new_jacs: the current gradient
        :type new_jacs: np.ndarray
        :param prev_jac: the previous gradient
        :type prev_jac: np.ndarray
        :param prev_step_dir: the previous search direction
        :type prev_step_dir: np.ndarray
        :return: the beta coefficient
        :rtype: np.ndarray
        """
        ...

class EigenvalueFollowingStepFinder:
    line_search = ArmijoSearch

    def __init__(self, func, jacobian, hessian, initial_beta=1, damping_parameter=None, damping_exponent=None, line_search=False, restart_interval=1, restart_hessian_norm=1e-05, hessian_approximator='bofill', approximation_mode='direct', target_mode=None, logger=None):
        """
        **LLM Docstring**

        Initialize an eigenvalue-following (P-RFO style) step finder, which shifts the
        Hessian eigenvalues to walk toward a chosen stationary point.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param hessian: the Hessian function
        :type hessian: Callable
        :param initial_beta: initial Hessian scale
        :type initial_beta: float
        :param damping_parameter: step-damping factor
        :type damping_parameter: float | None
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float | None
        :param line_search: line-search setting
        :type line_search: bool | Callable
        :param restart_interval: damping restart interval
        :type restart_interval: int
        :param restart_hessian_norm: step-norm reset threshold
        :type restart_hessian_norm: float
        :param hessian_approximator: quasi-Newton scheme for Hessian updates
        :type hessian_approximator: str
        :param approximation_mode: `'direct'` or `'inverse'`
        :type approximation_mode: str
        :param target_mode: index/vector of the eigenmode to follow
        :type target_mode: int | np.ndarray | None
        :param logger: optional logger
        :type logger: object | None
        """
        ...

    def identities(self, guess, mask):
        """
        **LLM Docstring**

        Return (cached) identity matrices matching the active members' shape.

        :param guess: the current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :return: the identity tensors
        :rtype: np.ndarray
        """
        ...

    def initialize_hessians(self, guess, mask):
        """
        **LLM Docstring**

        Return the exact Hessian at the current point as the initial estimate.

        :param guess: the current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :return: the Hessian
        :rtype: np.ndarray
        """
        ...

    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Update the Hessian estimate using the configured quasi-Newton approximator.

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous Hessian
        :type prev_hess: np.ndarray
        :return: the updated Hessian
        :rtype: np.ndarray
        """
        ...
    negative_eigenvalue_offset = 0.015
    positive_eigenvalue_offset = 0.005
    mode_tracking_overlap_cutoff = 1e-05

    def get_shift(self, evals, tf_new, target_mode):
        """
        **LLM Docstring**

        Choose the eigenvalue shift used to control the step, following the target mode
        (or the lowest eigenvalue) and offsetting to keep the shifted eigenvalue the
        right sign.

        :param evals: the Hessian eigenvalues
        :type evals: np.ndarray
        :param tf_new: the eigenvectors
        :type tf_new: np.ndarray
        :param target_mode: the mode being followed (or `None`)
        :type target_mode: np.ndarray | None
        :return: the eigenvalue shift
        :rtype: np.ndarray
        """
        ...

    def get_jacobian_updates(self, guess, mask, gradient_modifer=None):
        """
        **LLM Docstring**

        Evaluate the current gradient and its difference from the previous gradient.

        :param guess: the current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :return: `(new_jacobians, jacobian_differences)`
        :rtype: tuple
        """
        ...

    def restart_hessian_approximation(self):
        """
        **LLM Docstring**

        Decide whether to reset the Hessian approximation (on a near-zero previous
        step).

        :return: whether to restart
        :rtype: bool
        """
        ...

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce an eigenvalue-following step: update the Hessian, diagonalize it, apply
        the eigenvalue shift, and build the step in the eigenbasis (optionally
        projected/line-searched/damped).

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices (or chain-minimizer tuple)
        :type mask: np.ndarray | tuple
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        ...

class ChainMinimizingStepFinder:
    supports_hessian = True

    def __init__(self, func, jacobian, hessian=None, step_finder='conjugate-gradient', logger=None, **opts):
        """
        **LLM Docstring**

        Initialize a chain step finder that minimizes each image with a base step
        finder while adding inter-image (neighbour) contributions.

        :param func: the per-image objective
        :type func: Callable
        :param jacobian: the per-image gradient
        :type jacobian: Callable
        :param hessian: the per-image Hessian
        :type hessian: Callable | None
        :param step_finder: the base per-image method
        :type step_finder: str
        :param logger: optional logger
        :type logger: object | None
        :param opts: extra options for the base step finder
        """
        ...

    def adjust_jacobian(self, jac, guess, mask, cur, prev, next):
        """
        **LLM Docstring**

        Hook to adjust the per-image gradient given its neighbours (identity by default).

        :param jac: the base gradient
        :type jac: np.ndarray
        :param guess: the full chain
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param cur: current image index
        :type cur: int
        :param prev: previous image index
        :type prev: int | None
        :param next: next image index
        :type next: int | None
        :return: the adjusted gradient
        :rtype: np.ndarray
        """
        ...

    def adjust_hessian(self, hess, guess, mask, cur, prev, next):
        """
        **LLM Docstring**

        Hook to adjust the per-image Hessian given its neighbours (identity by default).

        :param hess: the base Hessian
        :type hess: np.ndarray
        :param guess: the full chain
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param cur: current image index
        :type cur: int
        :param prev: previous image index
        :type prev: int | None
        :param next: next image index
        :type next: int | None
        :return: the adjusted Hessian
        :rtype: np.ndarray
        """
        ...

    @abc.abstractmethod
    def image_pairwise_contribution(self, guess, mask, cur, prev, next, order=0):
        """
        **LLM Docstring**

        Abstract: the inter-image (neighbour) contribution to the objective/gradient/
        Hessian at the requested derivative order.

        :param guess: the full chain
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param cur: current image index
        :type cur: int
        :param prev: previous image index
        :type prev: int | None
        :param next: next image index
        :type next: int | None
        :param order: derivative order (`0`=value, `1`=gradient, `2`=Hessian)
        :type order: int
        :return: the contribution
        :rtype: np.ndarray | int
        """
        ...

    def wrap_func(self, func):
        """
        **LLM Docstring**

        Wrap the per-image objective so it also includes the inter-image contribution.

        :param func: the per-image objective
        :type func: Callable
        :return: the wrapped objective
        :rtype: Callable
        """
        ...

    def wrap_jac(self, jac):
        """
        **LLM Docstring**

        Wrap the per-image gradient so it includes the adjusted base gradient plus the
        inter-image contribution.

        :param jac: the per-image gradient
        :type jac: Callable
        :return: the wrapped gradient
        :rtype: Callable
        """
        ...

    def wrap_hess(self, hess):
        """
        **LLM Docstring**

        Wrap the per-image Hessian so it includes the adjusted base Hessian plus the
        inter-image contribution (or `None` when no Hessian is provided).

        :param hess: the per-image Hessian
        :type hess: Callable | None
        :return: the wrapped Hessian (or `None`)
        :rtype: Callable | None
        """
        ...

    def climbing_node_step(self, guess, mask, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Abstract: the step for a climbing image (not implemented in the base class).

        :param guess: the climbing-image parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector
        :type projector: np.ndarray | None
        :raises NotImplementedError: always in the base class
        """
        ...

    def __call__(self, guess, mask, projector=None, return_vals=False, gradient_modifer=None, is_climbing=None):
        """
        **LLM Docstring**

        Produce steps for a batch of chain images, routing climbing images through the
        climbing step and the rest through the base step finder.

        :param guess: the chain images
        :type guess: np.ndarray
        :param mask: `(mask, chain_data)` identifying active members and neighbours
        :type mask: tuple
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param is_climbing: per-member climbing flags
        :type is_climbing: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        ...

class NudgedElasticBandStepFinder(ChainMinimizingStepFinder):

    def __init__(self, func, jacobian, hessian=None, spring_constants=0.1, distance_function=None, step_finder='gradient-descent', logger=None, **opts):
        """
        **LLM Docstring**

        Initialize a nudged-elastic-band (NEB) step finder with spring couplings between
        neighbouring images.

        :param func: the per-image objective
        :type func: Callable
        :param jacobian: the per-image gradient
        :type jacobian: Callable
        :param hessian: the per-image Hessian
        :type hessian: Callable | None
        :param spring_constants: spring constant(s) between images
        :type spring_constants: float | np.ndarray
        :param distance_function: optional custom inter-image distance
        :type distance_function: Callable | None
        :param step_finder: the base per-image method
        :type step_finder: str
        :param logger: optional logger
        :type logger: object | None
        :param opts: extra options for the base step finder
        """
        ...

    def get_dist(self, p1, p2):
        """
        **LLM Docstring**

        Return the Euclidean distance between two image geometries.

        :param p1: the first geometry
        :type p1: np.ndarray
        :param p2: the second geometry
        :type p2: np.ndarray
        :return: the distance
        :rtype: np.ndarray
        """
        ...

    def get_tangent(self, guess, mask, cur, prev, next):
        """
        **LLM Docstring**

        Compute the (normalized) NEB path tangent at an image, using the energy-weighted
        tangent scheme based on the neighbouring image energies.

        :param guess: the full chain
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param cur: current image index
        :type cur: int
        :param prev: previous image index
        :type prev: int
        :param next: next image index
        :type next: int
        :return: the unit path tangent
        :rtype: np.ndarray
        """
        ...

    def adjust_jacobian(self, jac, guess, mask, cur, prev, next):
        """
        **LLM Docstring**

        Project the tangential component out of the per-image gradient (the NEB
        nudging), caching the current path tangent.

        :param jac: the base gradient
        :type jac: np.ndarray
        :param guess: the full chain
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param cur: current image index
        :type cur: int
        :param prev: previous image index
        :type prev: int | None
        :param next: next image index
        :type next: int | None
        :return: the nudged gradient
        :rtype: np.ndarray
        """
        ...

    def climbing_node_step(self, guess, mask, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Take a climbing-image step: invert the tangential force component so the image
        climbs toward the saddle along the path.

        :param guess: the climbing-image parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        ...

    def image_pairwise_contribution(self, guess, mask, cur, prev, next, order=0):
        """
        **LLM Docstring**

        Compute the NEB spring contribution to the objective/gradient/Hessian from the
        difference of the distances to the two neighbouring images.

        :param guess: the full chain
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param cur: current image index
        :type cur: int
        :param prev: previous image index
        :type prev: int | None
        :param next: next image index
        :type next: int | None
        :param order: derivative order (`0`=value, `1`=gradient, `2`=Hessian)
        :type order: int
        :return: the spring contribution
        :rtype: np.ndarray | int
        """
        ...

class AdjustedChainStepFinder(ChainMinimizingStepFinder):

    def __init__(self, pairwise_image_function, func, jacobian, hessian=None, logger=None, **opts):
        """
        **LLM Docstring**

        Initialize a chain step finder whose inter-image contribution is supplied by an
        external pairwise function.

        :param pairwise_image_function: the inter-image contribution function
        :type pairwise_image_function: Callable
        :param func: the per-image objective
        :type func: Callable
        :param jacobian: the per-image gradient
        :type jacobian: Callable
        :param hessian: the per-image Hessian
        :type hessian: Callable | None
        :param logger: optional logger
        :type logger: object | None
        :param opts: extra options for the base step finder
        """
        ...

    def image_pairwise_contribution(self, guess, mask, cur, prev, next, order=0):
        """
        **LLM Docstring**

        Delegate the inter-image contribution to the supplied pairwise function.

        :param guess: the full chain
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param cur: current image index
        :type cur: int
        :param prev: previous image index
        :type prev: int | None
        :param next: next image index
        :type next: int | None
        :param order: derivative order
        :type order: int
        :return: the contribution
        :rtype: np.ndarray | int
        """
        ...

class ChainReparametrizer:

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> '(np.ndarray, np.ndarray, np.ndarray)':
        """
        **LLM Docstring**

        Abstract: redistribute the images along the chain (implemented by subclasses).

        :param args: reparametrization inputs
        :param kwargs: reparametrization options
        :return: the reparametrized chain data
        :rtype: tuple
        """
        ...

class InterpolatingReparametrizer(ChainReparametrizer):

    def __init__(self, interpolator_type):
        """
        **LLM Docstring**

        Initialize a reparametrizer that redistributes images by interpolation.

        :param interpolator_type: the interpolator class to build from the images
        :type interpolator_type: type
        """
        ...

    def __call__(self, images, fixed_positions):
        """
        **LLM Docstring**

        Redistribute the images evenly along an interpolation of the current chain,
        holding the fixed positions in place.

        :param images: the current chain images
        :type images: np.ndarray
        :param fixed_positions: image indices to keep unchanged
        :type fixed_positions: Iterable[int]
        :return: the reparametrized images
        :rtype: np.ndarray
        """
        ...

def jacobi_maximize(initial_matrix, rotation_generator, max_iterations=100, contrib_tol=1e-16, tol=1e-08):
    """
    **LLM Docstring**

    Maximize an objective over an orthogonal transformation by sweeping 2x2
    (Jacobi) rotations over all column pairs until the gain converges (the standard
    orbital/vector localization scheme).

    :param initial_matrix: the matrix whose columns are rotated
    :type initial_matrix: np.ndarray
    :param rotation_generator: callable giving the optimal `(cos, sin, gain)` per pair
    :type rotation_generator: Callable
    :param max_iterations: maximum sweeps
    :type max_iterations: int
    :param contrib_tol: minimum per-pair gain to accept a rotation
    :type contrib_tol: float
    :param tol: convergence tolerance on the total per-sweep gain
    :type tol: float
    :return: `(rotated_matrix, accumulated_rotation, (total_gain, iterations))`
    :rtype: tuple
    """
    ...

class LineSearchRotationGenerator:

    def __init__(self, column_function, tol=1e-16, max_iterations=10):
        """
        **LLM Docstring**

        Initialize a rotation generator that finds each optimal 2x2 rotation angle by a
        quadratic-interpolation line search.

        :param column_function: the per-column objective contribution
        :type column_function: Callable
        :param tol: convergence tolerance
        :type tol: float
        :param max_iterations: maximum line-search iterations
        :type max_iterations: int
        """
        ...

    @classmethod
    def quadratic_opt(self, g0, g1, g2, f0, f1, f2):
        """
        **LLM Docstring**

        Return the vertex of the parabola through three `(angle, value)` samples (the
        quadratic-interpolation optimum), or `None` when the samples are collinear.

        :param g0: first angle
        :type g0: float
        :param g1: second angle
        :type g1: float
        :param g2: third angle
        :type g2: float
        :param f0: value at the first angle
        :type f0: float
        :param f1: value at the second angle
        :type f1: float
        :param f2: value at the third angle
        :type f2: float
        :return: the interpolated optimum angle, or `None`
        :rtype: float | None
        """
        ...

    def _phi(self, g, f_i, f_j):
        """
        **LLM Docstring**

        Evaluate the objective for the pair of columns rotated by an angle, returning the
        value, the `(cos, sin)`, and the rotated columns.

        :param g: the rotation angle
        :type g: float
        :param f_i: the first column
        :type f_i: np.ndarray
        :param f_j: the second column
        :type f_j: np.ndarray
        :return: `(value, (cos, sin), (rotated_i, rotated_j))`
        :rtype: tuple
        """
        ...

    def __call__(self, mat, col_i, col_j):
        """
        **LLM Docstring**

        Find the optimal 2x2 rotation for a pair of columns by quadratic-interpolation
        line search over the rotation angle.

        :param mat: the matrix being localized
        :type mat: np.ndarray
        :param col_i: the first column index
        :type col_i: int
        :param col_j: the second column index
        :type col_j: int
        :return: `(cos, sin, gain)` for the optimal rotation
        :rtype: tuple
        """
        ...

class GradientDescentRotationGenerator:

    def __init__(self, column_function, gradient, tol=1e-16, max_iterations=10, damping_parameter=0.9, damping_exponent=1.1, restart_interval=3):
        """
        **LLM Docstring**

        Initialize a rotation generator that finds each optimal 2x2 rotation angle by
        damped gradient descent.

        :param column_function: the per-column objective contribution
        :type column_function: Callable
        :param gradient: the per-column gradient of the objective
        :type gradient: Callable
        :param tol: convergence tolerance on the step
        :type tol: float
        :param max_iterations: maximum iterations
        :type max_iterations: int
        :param damping_parameter: step-damping factor
        :type damping_parameter: float
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float
        :param restart_interval: damping restart interval
        :type restart_interval: int
        """
        ...

    def __call__(self, mat, col_i, col_j):
        """
        **LLM Docstring**

        Find the optimal 2x2 rotation for a pair of columns by damped gradient descent
        over the rotation angle.

        :param mat: the matrix being localized
        :type mat: np.ndarray
        :param col_i: the first column index
        :type col_i: int
        :param col_j: the second column index
        :type col_j: int
        :return: `(cos, sin, gain)` for the optimal rotation
        :rtype: tuple
        """
        ...

class OperatorMatrixRotationGenerator:

    def __init__(self, one_e_func, matrix_func):
        """
        **LLM Docstring**

        Initialize a rotation generator that solves each optimal 2x2 rotation
        analytically from a supplied 2x2 operator matrix.

        :param one_e_func: the per-column objective contribution
        :type one_e_func: Callable
        :param matrix_func: callable giving the `(a, b, c)` operator-matrix entries for a pair
        :type matrix_func: Callable
        """
        ...

    def __call__(self, mat, col_i, col_j):
        """
        **LLM Docstring**

        Find the optimal 2x2 rotation for a pair of columns by analytically diagonalizing
        the supplied 2x2 operator matrix (the closed-form Jacobi angle).

        :param mat: the matrix being localized
        :type mat: np.ndarray
        :param col_i: the first column index
        :type col_i: int
        :param col_j: the second column index
        :type col_j: int
        :return: `(cos, sin, gain)` for the optimal rotation
        :rtype: tuple
        """
        ...

def displacement_localizing_rotation_generator(mat, col_i, col_j):
    """
    **LLM Docstring**

    Compute the optimal 2x2 Foster-Boys localizing rotation for a pair of
    displacement columns (each a set of 3-vectors), returning the closed-form
    `(cos, sin, gain)`.

    :param mat: the matrix of displacement columns
    :type mat: np.ndarray
    :param col_i: the first column index
    :type col_i: int
    :param col_j: the second column index
    :type col_j: int
    :return: `(cos, sin, gain)` for the localizing rotation
    :rtype: tuple
    """
    ...

def polyfit_critical_points(x, y, fit_order=2, check_curvature=None, curvature_test=None):
    """
    **LLM Docstring**

    Fit a polynomial to `(x, y)` and return the critical points of the fit (roots of
    its derivative), optionally filtered by a curvature test.

    :param x: the sample abscissae
    :type x: np.ndarray
    :param y: the sample values
    :type y: np.ndarray
    :param fit_order: the polynomial degree
    :type fit_order: int
    :param check_curvature: also compute the curvature at each critical point
    :type check_curvature: bool | None
    :param curvature_test: predicate selecting critical points by curvature sign
    :type curvature_test: Callable | None
    :return: `(roots, values[, curvature])`
    :rtype: tuple
    """
    ...

def polyfit_maxima(x, y, fit_order=2):
    """
    **LLM Docstring**

    Fit a polynomial to `(x, y)` and return its maxima (critical points with negative
    curvature).

    :param x: the sample abscissae
    :type x: np.ndarray
    :param y: the sample values
    :type y: np.ndarray
    :param fit_order: the polynomial degree
    :type fit_order: int
    :return: `(maxima_x, maxima_values, curvature)`
    :rtype: tuple
    """
    ...

def polyfit_minima(x, y, fit_order=2):
    """
    **LLM Docstring**

    Fit a polynomial to `(x, y)` and return its minima (critical points with positive
    curvature).

    :param x: the sample abscissae
    :type x: np.ndarray
    :param y: the sample values
    :type y: np.ndarray
    :param fit_order: the polynomial degree
    :type fit_order: int
    :return: `(minima_x, minima_values, curvature)`
    :rtype: tuple
    """
    ...

def get_peak_fitting_region(energies, *, peak_energy_cutoff, min_nodes):
    """
    **LLM Docstring**

    Select the indices around the peak of an energy profile to use for a peak fit:
    scan outward from the maximum while the energy stays above a cutoff, padding to a
    minimum node count.

    :param energies: the per-point energies
    :type energies: np.ndarray
    :param peak_energy_cutoff: the cutoff below which points are excluded
    :type peak_energy_cutoff: float
    :param min_nodes: minimum number of points to keep (for the fit)
    :type min_nodes: int
    :return: the selected indices
    :rtype: list[int]
    """
    ...

def peak_fit_maxiumum(x, y, *, fit_order=2, peak_cutoff, min_nodes=3):
    """
    **LLM Docstring**

    Estimate the location and height of a peak by fitting a polynomial to the points
    around it (falling back to the raw argmax if the fit has no maximum).

    :param x: the abscissae
    :type x: np.ndarray
    :param y: the values
    :type y: np.ndarray
    :param fit_order: the polynomial degree
    :type fit_order: int
    :param peak_cutoff: the cutoff for selecting the fit region
    :type peak_cutoff: float
    :param min_nodes: minimum number of points in the fit region
    :type min_nodes: int
    :return: `(peak_x, peak_value)`
    :rtype: tuple
    """
    ...