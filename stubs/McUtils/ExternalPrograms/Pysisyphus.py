import os
import tempfile
import logging
from contextlib import contextmanager
import pathlib
import scipy
import numpy as np
from .. import Devutils as dev
from .. import Numputils as nput
from ..Data import AtomData
from ..Parsers import XYZParser
__all__ = ['PysisCalculator', 'patch_pysis_logging', 'run_pysisyphus', 'pysis_interpolate', 'prep_pysis_images']

@contextmanager
def suppress_logging(level=logging.CRITICAL):
    """Temporarily disables logging for a specific block of code."""
    ...

def _remove_handlers(logger, max_depth=8):
    """
    **LLM Docstring**

    Recursively clear the logging handlers on a logger and its parents (up to a
    depth limit), used to silence Pysisyphus's logging.

    :param logger: the logger to clear
    :param max_depth: how many parent loggers to also clear
    :type max_depth: int
    """
    ...

def patch_pysis_logging():
    """
    **LLM Docstring**

    Monkey-patch Pysisyphus's logging setup so it doesn't install its own file
    handlers or write calculation output to the default directory.

    Clears existing handlers, neutralizes the logger-configuration hooks, and
    redirects the default output directory to a temporary location.
    """
    ...

def PysisCalculator(energy_evaluator, batched_orders=False, distance_units=None, energy_units=None, **kwargs):
    """
    **LLM Docstring**

    Build a Pysisyphus-compatible calculator that evaluates energies (and
    derivatives) from a McUtils energy evaluator.

    :param energy_evaluator: the energy-evaluation callable
    :type energy_evaluator: Callable
    :param batched_orders: evaluate derivative orders in a batch
    :type batched_orders: bool
    :param distance_units: the distance units of the evaluator
    :type distance_units: str | None
    :param energy_units: the energy units of the evaluator
    :type energy_units: str | None
    :param kwargs: extra options for the calculator
    :return: the Pysisyphus calculator
    :rtype: PysisyphusTermCalculator
    """
    ...
method_resolvers = {}

def register_method(name, method=None):
    """
    **LLM Docstring**

    Register a path/optimization method resolver by name (usable directly or as a
    decorator).

    :param name: the method name
    :type name: str
    :param method: the resolver (or `None` to return a decorator)
    :type method: Callable | None
    :return: the registered resolver, or a decorator
    :rtype: Callable
    """
    ...

def resolve_cos_method(*, images, cos_class, energy_evaluator=None, out_dir=None, logger=None, fixed_images=None, **opts):
    """
    **LLM Docstring**

    Build a Pysisyphus chain-of-states object of the given class, ensuring every
    image has a calculator, wiring up logging and the output directory, and
    optionally forcing a set of fixed images.

    :param images: the chain images
    :type images: list
    :param cos_class: the chain-of-states class to instantiate
    :type cos_class: type
    :param energy_evaluator: an energy evaluator to build calculators from
    :type energy_evaluator: Callable | None
    :param out_dir: the calculation output directory
    :type out_dir: str | None
    :param logger: a logger for the chain-of-states object
    :param fixed_images: image indices to hold fixed
    :type fixed_images: Iterable[int] | None
    :param opts: extra options for the chain-of-states class
    :return: the chain-of-states object
    :rtype: object
    :raises ValueError: if no image has a calculator and none can be built
    """
    ...

@register_method('growing-string')
def resolve_gsm(*, images, calc_getter=None, energy_evaluator=None, max_nodes=None, energies=None, distance_metric=None, masses=None, fit_order=2, peak_cutoff=0.5, min_nodes=3, **opts):
    """
    **LLM Docstring**

    Resolve a growing-string-method chain-of-states object, splitting the images into
    left/right halves at the guessed transition state.

    :param images: the chain images
    :type images: list
    :param calc_getter: a factory for per-image calculators
    :type calc_getter: Callable | None
    :param energy_evaluator: an energy evaluator to build calculators from
    :type energy_evaluator: Callable | None
    :param max_nodes: the maximum number of nodes
    :type max_nodes: int | None
    :param energies: the per-image energies
    :type energies: Sequence | None
    :param distance_metric: the inter-image distance metric
    :type distance_metric: Callable | None
    :param masses: the atomic masses
    :type masses: Sequence | None
    :param fit_order: the polynomial fit order for the TS guess
    :type fit_order: int
    :param peak_cutoff: the fractional peak cutoff for the TS guess
    :type peak_cutoff: float
    :param min_nodes: the minimum fit nodes
    :type min_nodes: int
    :param opts: extra chain-of-states options
    :return: the growing-string object
    :rtype: object
    """
    ...

@register_method('chain-of-states')
def resolve_chain_of_states(*, images, energy_evaluator=None, **opts):
    """
    **LLM Docstring**

    Resolve a generic chain-of-states object.

    :param images: the chain images
    :type images: list
    :param energy_evaluator: an energy evaluator to build calculators from
    :type energy_evaluator: Callable | None
    :param opts: extra chain-of-states options
    :return: the chain-of-states object
    :rtype: object
    """
    ...

@register_method('freezing-string')
def resolve_freezing_string(*, images, calc_getter=None, energy_evaluator=None, **opts):
    """
    **LLM Docstring**

    Resolve a freezing-string-method chain-of-states object.

    :param images: the chain images
    :type images: list
    :param calc_getter: a factory for per-image calculators
    :type calc_getter: Callable | None
    :param energy_evaluator: an energy evaluator to build calculators from
    :type energy_evaluator: Callable | None
    :param opts: extra chain-of-states options
    :return: the freezing-string object
    :rtype: object
    """
    ...

@register_method('zero-temperature-string')
def resolve_zta(*, images, energy_evaluator=None, **opts):
    """
    **LLM Docstring**

    Resolve a zero-temperature-string (SimpleZTS) chain-of-states object.

    :param images: the chain images
    :type images: list
    :param energy_evaluator: an energy evaluator to build calculators from
    :type energy_evaluator: Callable | None
    :param opts: extra chain-of-states options
    :return: the ZTS object
    :rtype: object
    """
    ...

@register_method('neb')
def resolve_neb(*, images, energy_evaluator=None, **opts):
    """
    **LLM Docstring**

    Resolve a nudged-elastic-band chain-of-states object.

    :param images: the chain images
    :type images: list
    :param energy_evaluator: an energy evaluator to build calculators from
    :type energy_evaluator: Callable | None
    :param opts: extra chain-of-states options
    :return: the NEB object
    :rtype: object
    """
    ...

@register_method('optimize')
def resolve_optimize(*, geom, energy_evaluator=None, out_dir=None, **opts):
    """
    **LLM Docstring**

    Resolve a single-geometry optimization target, ensuring it has a calculator and
    output directory.

    :param geom: the geometry to optimize
    :param energy_evaluator: an energy evaluator to build a calculator from
    :type energy_evaluator: Callable | None
    :param out_dir: the calculation output directory
    :type out_dir: str | None
    :param opts: unused extra options
    :return: the (calculator-equipped) geometry
    :rtype: object
    """
    ...

@register_method('ts')
def resolve_ts(*, images, energy_evaluator=None, energies=None, image_guess=None, distance_metric=None, masses=None, fit_order=2, peak_cutoff=0.5, min_nodes=3, climb=True, logger=None, out_dir=None, use_max_for_guess=True, eliminate_guess_nodes=True, **opts):
    """
    **LLM Docstring**

    Resolve a climbing-image transition-state target: guess the TS image along the
    chain and return it (with a calculator attached).

    :param images: the chain images
    :type images: list
    :param energy_evaluator: an energy evaluator to build calculators from
    :type energy_evaluator: Callable | None
    :param energies: the per-image energies
    :type energies: Sequence | None
    :param image_guess: an explicit TS image index
    :type image_guess: int | None
    :param distance_metric: the inter-image distance metric
    :type distance_metric: Callable | None
    :param masses: the atomic masses
    :type masses: Sequence | None
    :param fit_order: the polynomial fit order
    :type fit_order: int
    :param peak_cutoff: the fractional peak cutoff
    :type peak_cutoff: float
    :param min_nodes: the minimum fit nodes
    :type min_nodes: int
    :param climb: must be `True` (only climbing TS is implemented)
    :type climb: bool
    :param logger: a logger
    :param out_dir: the output directory
    :type out_dir: str | None
    :param use_max_for_guess: use the energy maximum as the guess
    :type use_max_for_guess: bool
    :param eliminate_guess_nodes: drop guess nodes afterward
    :type eliminate_guess_nodes: bool
    :param opts: extra options
    :return: the target TS geometry
    :rtype: object
    :raises NotImplementedError: if `climb` is `False`
    """
    ...

def get_dimer_image_guess(base_images, energies=None, distance_metric=None, masses=None, *, fit_order=2, peak_cutoff, min_nodes=3, use_max_for_guess=False):
    """
    **LLM Docstring**

    Guess the transition-state image along a chain, either by the raw energy maximum
    or by fitting the energy-vs-(mass-weighted-)distance profile and locating its
    peak.

    :param base_images: the chain images
    :type base_images: list
    :param energies: the per-image energies (computed if omitted)
    :type energies: Sequence | None
    :param distance_metric: the inter-image distance metric
    :type distance_metric: Callable | None
    :param masses: the atomic masses
    :type masses: Sequence | None
    :param fit_order: the polynomial fit order
    :type fit_order: int
    :param peak_cutoff: the fractional peak cutoff for the fit region
    :type peak_cutoff: float
    :param min_nodes: the minimum fit nodes
    :type min_nodes: int
    :param use_max_for_guess: use the raw energy maximum as the guess
    :type use_max_for_guess: bool
    :return: the guessed TS image index
    :rtype: int
    """
    ...

@register_method('dimer')
def resolve_dimer(*, images, energy_evaluator=None, energies=None, image_guess=None, distance_metric=None, masses=None, fit_order=2, peak_cutoff=0.5, min_nodes=3, displacement_vector=None, climb=True, logger=None, out_dir=None, use_max_for_guess=True, eliminate_guess_nodes=True, fixed_images=None, **opts):
    """
    **LLM Docstring**

    Resolve a dimer-method transition-state target: guess the TS image, seed the
    dimer orientation from the neighbouring image, and attach a Pysisyphus `Dimer`
    calculator.

    :param images: the chain images
    :type images: list
    :param energy_evaluator: an energy evaluator to build calculators from
    :type energy_evaluator: Callable | None
    :param energies: the per-image energies
    :type energies: Sequence | None
    :param image_guess: an explicit TS image index
    :type image_guess: int | None
    :param distance_metric: the inter-image distance metric
    :type distance_metric: Callable | None
    :param masses: the atomic masses
    :type masses: Sequence | None
    :param fit_order: the polynomial fit order
    :type fit_order: int
    :param peak_cutoff: the fractional peak cutoff
    :type peak_cutoff: float
    :param min_nodes: the minimum fit nodes
    :type min_nodes: int
    :param displacement_vector: the initial dimer orientation (derived if omitted)
    :type displacement_vector: np.ndarray | None
    :param climb: must be `True` (only climbing dimer is implemented)
    :type climb: bool
    :param logger: a logger
    :param out_dir: the output directory
    :type out_dir: str | None
    :param use_max_for_guess: use the energy maximum as the guess
    :type use_max_for_guess: bool
    :param eliminate_guess_nodes: drop the guess node afterward
    :type eliminate_guess_nodes: bool
    :param fixed_images: must be `None` (fixed images unsupported with dimer)
    :type fixed_images: Iterable | None
    :param opts: extra dimer options
    :return: the target geometry with the dimer calculator attached
    :rtype: object
    :raises NotImplementedError: if `climb` is `False`
    :raises ValueError: if `fixed_images` is given
    """
    ...

def resolve_pysis_method(method_name, logger=None, **opts):
    """
    **LLM Docstring**

    Resolve a method name (honoring aliases) to its registered resolver and build the
    method object, attaching a logger if given.

    :param method_name: the method name or an already-resolved callable
    :type method_name: str | Callable
    :param logger: a logger to attach
    :param opts: options forwarded to the resolver
    :return: the built method object
    :rtype: object
    """
    ...
optimizer_resolvers = {}

def register_optimizer(name, method=None):
    """
    **LLM Docstring**

    Register a Pysisyphus optimizer resolver by name (usable directly or as a
    decorator).

    :param name: the optimizer name
    :type name: str
    :param method: the resolver (or `None` to return a decorator)
    :type method: Callable | None
    :return: the registered resolver, or a decorator
    :rtype: Callable
    """
    ...

def resolve_generic_optimizer(name):
    """
    **LLM Docstring**

    Build a resolver for a Pysisyphus optimizer looked up by name from the
    `pysisyphus.optimizers` package.

    :param name: the optimizer module/class name
    :type name: str
    :return: a resolver that instantiates the optimizer for a trajectory
    :rtype: Callable
    """
    ...

@register_optimizer('string')
def resolve_string_optimizer(traj, **opts):
    """
    **LLM Docstring**

    Instantiate Pysisyphus's `StringOptimizer` for a trajectory, marking it as a
    fully grown fixed-size string.

    :param traj: the string trajectory
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

@register_optimizer('lbfgs')
def resolve_lbfgs_optimizer(traj, **opts):
    """
    **LLM Docstring**

    Instantiate Pysisyphus's `LBFGS` optimizer for a trajectory.

    :param traj: the trajectory/geometry to optimize
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

@register_optimizer('rfo')
def resolve_lrfo_optimizer(traj, **opts):
    """
    **LLM Docstring**

    Instantiate Pysisyphus's `RFOptimizer` (rational-function optimization) for a
    trajectory.

    :param traj: the trajectory/geometry to optimize
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

@register_optimizer('plbfgs')
def resolve_plbfgs_optimizer(traj, **opts):
    """
    **LLM Docstring**

    Instantiate Pysisyphus's `PreconLBFGS` (preconditioned L-BFGS) optimizer for a
    trajectory.

    :param traj: the trajectory/geometry to optimize
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

@register_optimizer('bfgs')
def resolve_bfgs_optimizer(traj, **opts):
    """
    **LLM Docstring**

    Instantiate Pysisyphus's `BFGS` optimizer for a trajectory.

    :param traj: the trajectory/geometry to optimize
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

@register_optimizer('rsprfo')
def resolve_rsprfo_optimizer(traj, **opts):
    """
    **LLM Docstring**

    Instantiate Pysisyphus's `RSPRFOptimizer` (restricted-step partitioned RFO
    transition-state optimizer) for a trajectory.

    :param traj: the trajectory/geometry to optimize
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

@register_optimizer('rsirfo')
def resolve_rsirfo_optimizer(traj, **opts):
    """
    **LLM Docstring**

    Instantiate Pysisyphus's `RSIRFOptimizer` (restricted-step image-RFO
    transition-state optimizer) for a trajectory.

    :param traj: the trajectory/geometry to optimize
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

@register_optimizer('trim')
def resolve_trim_optimizer(traj, **opts):
    """
    **LLM Docstring**

    Instantiate Pysisyphus's `TRIM` transition-state optimizer for a trajectory.

    :param traj: the trajectory/geometry to optimize
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

@register_optimizer('fire')
def resolve_fire_optimizer(traj, **opts):
    """
    **LLM Docstring**

    Instantiate Pysisyphus's `FIRE` optimizer for a trajectory.

    :param traj: the trajectory/geometry to optimize
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

@register_optimizer('cubic-newton')
def resolve_cubic_newton_optimizer(traj, **opts):
    """
    **LLM Docstring**

    Instantiate the registered Pysisyphus optimizer for a trajectory.

    This resolver is registered under several optimizer names (cubic-newton,
    conjugate-gradient, gradient-descent); each registration imports and wraps the
    corresponding Pysisyphus optimizer class.

    :param traj: the trajectory/geometry to optimize
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

@register_optimizer('conjugate-gradient')
def resolve_cubic_newton_optimizer(traj, **opts):
    """
    **LLM Docstring**

    Instantiate the registered Pysisyphus optimizer for a trajectory.

    This resolver is registered under several optimizer names (cubic-newton,
    conjugate-gradient, gradient-descent); each registration imports and wraps the
    corresponding Pysisyphus optimizer class.

    :param traj: the trajectory/geometry to optimize
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

@register_optimizer('gradient-descent')
def resolve_cubic_newton_optimizer(traj, **opts):
    """
    **LLM Docstring**

    Instantiate the registered Pysisyphus optimizer for a trajectory.

    This resolver is registered under several optimizer names (cubic-newton,
    conjugate-gradient, gradient-descent); each registration imports and wraps the
    corresponding Pysisyphus optimizer class.

    :param traj: the trajectory/geometry to optimize
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

class PysisyphusLogger:

    def __init__(self, log_file=None):
        """
        **LLM Docstring**

        Wrap a McUtils logger for use as a Pysisyphus logger.

        :param log_file: the log file (or logger) to wrap
        :type log_file: str | object | None
        """
        ...

    def log(self, log_level, *args, **opts):
        """
        **LLM Docstring**

        Log a message at the given level.

        :param log_level: the log level
        :param args: the message parts
        :param opts: extra logging options
        """
        ...

    def debug(self, *args, **opts):
        """
        **LLM Docstring**

        Log a debug-level message.

        :param args: the message parts
        :param opts: extra logging options
        """
        ...

    def error(self, *args, **opts):
        """
        **LLM Docstring**

        Log an error-level message.

        :param args: the message parts
        :param opts: extra logging options
        """
        ...

def resolve_pysis_optimizer(optimizer, method_name, generator, logger=None, **opts):
    """
    **LLM Docstring**

    Resolve and instantiate the optimizer for a method: pick the default optimizer
    for the method when none is given, look up the resolver, and build it with
    logging suppressed.

    :param optimizer: the optimizer name/callable (or `None` for the method default)
    :type optimizer: str | Callable | None
    :param method_name: the method name (used to choose the default optimizer)
    :type method_name: str
    :param generator: the method object/trajectory to optimize
    :param logger: a logger to attach
    :param opts: extra optimizer options
    :return: the optimizer instance
    :rtype: object
    """
    ...

def parse_trj(file):
    """
    **LLM Docstring**

    Parse an XYZ trajectory (`.trj`) file into its geometries.

    :param file: the trajectory file
    :type file: str
    :return: the parsed geometries
    :rtype: list
    """
    ...

def run_pysisyphus(energy_evaluator, method, optimizer=None, optimizer_settings=None, max_cycles=None, max_step=None, max_displacement=None, thresh=None, tol=None, use_max_for_error=True, log_file=None, out_dir=None, return_logs=True, patch_logging=True, logger=None, ignore_zero_steps=True, **kwargs):
    """
    **LLM Docstring**

    Run a full Pysisyphus optimization: resolve the method and optimizer, translate
    the McUtils-style convergence/step settings into Pysisyphus options, run the
    optimization (with logging patched and a symmetrized-eigh guard), and collect the
    output logs.

    :param energy_evaluator: the energy-evaluation callable
    :type energy_evaluator: Callable
    :param method: the method name (e.g. `'neb'`, `'ts'`, `'optimize'`)
    :type method: str
    :param optimizer: the optimizer name/callable (default chosen from the method)
    :type optimizer: str | Callable | None
    :param optimizer_settings: extra optimizer settings
    :type optimizer_settings: dict | None
    :param max_cycles: the maximum optimization cycles
    :type max_cycles: int | None
    :param max_step: the maximum step size
    :type max_step: float | None
    :param max_displacement: an alias for `max_step`
    :type max_displacement: float | None
    :param thresh: an explicit Pysisyphus convergence threshold preset
    :param tol: the RMS-force convergence tolerance
    :type tol: float | None
    :param use_max_for_error: converge on the max force rather than the RMS force
    :type use_max_for_error: bool
    :param log_file: a log file
    :param out_dir: the working/output directory
    :type out_dir: str | None
    :param return_logs: read and return the output-directory logs
    :type return_logs: bool
    :param patch_logging: patch Pysisyphus logging first
    :type patch_logging: bool
    :param logger: a logger to use
    :param ignore_zero_steps: swallow Pysisyphus's zero-step-length termination
    :type ignore_zero_steps: bool
    :param kwargs: extra options forwarded to the method resolver
    :return: `(generator, optimizer, logs)`
    :rtype: tuple
    """
    ...
interpolator_resolvers = {}

def register_interpolator(name, method=None):
    """
    **LLM Docstring**

    Register a path interpolator resolver by name (usable directly or as a
    decorator).

    :param name: the interpolator name
    :type name: str
    :param method: the resolver (or `None` to return a decorator)
    :type method: Callable | None
    :return: the registered resolver, or a decorator
    :rtype: Callable
    """
    ...

@register_interpolator('idpp')
def resolve_idpp(geoms, **opts):
    """
    **LLM Docstring**

    Build a Pysisyphus IDPP (image-dependent pair potential) interpolator.

    :param geoms: the endpoint geometries
    :type geoms: Sequence
    :param opts: extra interpolator options
    :return: the interpolator
    :rtype: object
    """
    ...

@register_interpolator('linear')
def resolve_linear(geoms, **opts):
    """
    **LLM Docstring**

    Build a Pysisyphus linear interpolator.

    :param geoms: the endpoint geometries
    :type geoms: Sequence
    :param opts: extra interpolator options
    :return: the interpolator
    :rtype: object
    """
    ...

@register_interpolator('redund')
def resolve_redund(geoms, **opts):
    """
    **LLM Docstring**

    Build a Pysisyphus redundant-internal-coordinate interpolator.

    :param geoms: the endpoint geometries
    :type geoms: Sequence
    :param opts: extra interpolator options
    :return: the interpolator
    :rtype: object
    """
    ...

def resolve_pysis_interpolator(interpolator, traj, logger=None, **opts):
    """
    **LLM Docstring**

    Resolve an interpolator name to its resolver and build the interpolator for a
    trajectory.

    :param interpolator: the interpolator name or callable
    :type interpolator: str | Callable
    :param traj: the endpoint geometries
    :type traj: Sequence
    :param logger: an (unused) logger
    :param opts: extra interpolator options
    :return: the interpolator
    :rtype: object
    """
    ...

@contextmanager
def _patched_eigh():
    """
    **LLM Docstring**

    Context manager that temporarily replaces `numpy.linalg.eigh` with a variant that
    symmetrizes its input and falls back to `scipy.linalg.eigh` on failure, guarding
    Pysisyphus against non-symmetric/ill-conditioned Hessians.

    :param: (no arguments)
    :return: the patched `eigh` function (yielded)
    :rtype: Callable
    """
    ...

def prep_pysis_images(atoms, geometry, coord_type='cartesian', coord_kwargs=None, **opts):
    """
    **LLM Docstring**

    Build Pysisyphus `Geometry` objects from atoms and one or more coordinate sets,
    forming a shared redundant-internal-coordinate union across the endpoints when a
    non-Cartesian coordinate type is requested.

    :param atoms: the element symbols
    :type atoms: Sequence[str]
    :param geometry: one geometry (2D) or several (3D)
    :type geometry: np.ndarray
    :param coord_type: the coordinate type (`'cartesian'`, `'redund'`, `'tric'`, ...)
    :type coord_type: str
    :param coord_kwargs: extra coordinate-system options
    :type coord_kwargs: dict | None
    :param opts: extra `Geometry` options
    :return: the geometry (or list of geometries)
    :rtype: object | list
    """
    ...

def pysis_interpolate(geoms, interpolator, **opts):
    """
    **LLM Docstring**

    Interpolate a path between endpoint geometries using a Pysisyphus interpolator,
    returning the interpolated Cartesian coordinates.

    :param geoms: the endpoint geometries
    :type geoms: Sequence
    :param interpolator: the interpolator name or callable
    :type interpolator: str | Callable
    :param opts: extra interpolator options
    :return: the interpolated coordinate sets
    :rtype: list[np.ndarray]
    """
    ...