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

__all__ = [
    "PysisCalculator",
    "patch_pysis_logging",
    "run_pysisyphus",
    "pysis_interpolate",
    "prep_pysis_images"
]


@contextmanager
def suppress_logging(level=logging.CRITICAL):
    """Temporarily disables logging for a specific block of code."""
    # Record the previous disabled level to restore it later
    previous_level = logging.root.manager.disable

    logging.disable(level)
    try:
        yield
    finally:
        # Restore the original disabling level
        logging.disable(previous_level)

def _remove_handlers(logger, max_depth=8):
    """
    **LLM Docstring**

    Recursively clear the logging handlers on a logger and its parents (up to a
    depth limit), used to silence Pysisyphus's logging.

    :param logger: the logger to clear
    :param max_depth: how many parent loggers to also clear
    :type max_depth: int
    """
    logger.handlers.clear()
    if max_depth > 0:
        if logger.parent and (logger.parent is not logger):
            _remove_handlers(logger.parent, max_depth=max_depth-1)
def patch_pysis_logging():
    """
    **LLM Docstring**

    Monkey-patch Pysisyphus's logging setup so it doesn't install its own file
    handlers or write calculation output to the default directory.

    Clears existing handlers, neutralizes the logger-configuration hooks, and
    redirects the default output directory to a temporary location.
    """
    import pysisyphus
    _remove_handlers(pysisyphus.logger)

    with dev.OutputRedirect():
        import pysisyphus.init_logging
        pysisyphus.init_logging.LOGGERS.clear()
        import pysisyphus.config

    def get_fh_logger(name, log_fn, base=pysisyphus.init_logging.get_fh_logger):
        """
        **LLM Docstring**

        Replacement for Pysisyphus's file-handler logger factory that returns a
        handler-free logger.

        :param name: the logger name
        :type name: str
        :param log_fn: the (ignored) log file name
        :param base: the original factory (unused)
        :return: the cleared logger
        :rtype: logging.Logger
        """
        # base(name, log_fn)
        logger = logging.getLogger(name)
        _remove_handlers(logger)
    pysisyphus.init_logging.get_fh_logger = get_fh_logger

    import pysisyphus.optimizers.Optimizer
    def configure_opt_logger(logger, prefix, base=pysisyphus.optimizers.Optimizer.configure_opt_logger):
        """
        **LLM Docstring**

        Replacement for Pysisyphus's optimizer-logger configuration that simply clears
        the logger's handlers.

        :param logger: the optimizer logger
        :param prefix: the (ignored) log prefix
        :param base: the original configuration function (unused)
        """
        _remove_handlers(logger)
        # base(logger=logger, prefix=prefix)
        # _remove_handlers(logger)
    pysisyphus.optimizers.Optimizer.configure_opt_logger = configure_opt_logger

    import pysisyphus.calculators
    _remove_handlers(pysisyphus.calculators.logger)

    logger = logging.getLogger("calculator")
    _remove_handlers(logger)

    if pysisyphus.config.OUT_DIR_DEFAULT == 'qm_calcs':
        with tempfile.TemporaryDirectory() as tmpdir:
            pysisyphus.config.OUT_DIR_DEFAULT = tmpdir

def PysisCalculator(
        energy_evaluator,
        batched_orders=False,
        distance_units=None,
        energy_units=None,
        **kwargs
):
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
    from .PysisyphusCalculator import PysisyphusTermCalculator

    return PysisyphusTermCalculator(
        energy_evaluator,
        batched_orders=batched_orders,
        distance_units=distance_units,
        energy_units=energy_units,
        **kwargs
    )

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
    if method is not None:
        method_resolvers[name] = method
        return method
    else:
        def register(method, name=name):
            """
            **LLM Docstring**

            Decorator that registers the wrapped resolver under the captured method name.

            :param method: the resolver being registered
            :type method: Callable
            :param name: the method name
            :type name: str
            :return: the registered resolver
            :rtype: Callable
            """
            return register_method(name, method)
        return register

def resolve_cos_method(*, images, cos_class, energy_evaluator=None,
                       out_dir=None,
                       logger=None,
                       fixed_images=None,
                       **opts):
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
    base_calc = None
    for i in images:
        if i.calculator is None:
            if energy_evaluator is None:
                if base_calc is None:
                    for i in images:
                        if i.calculator is not None:
                            base_calc = i.calculator
                            break
                    else:
                        raise ValueError("no image has a calculator")
                i.set_calculator(base_calc.copy())
            else:
                i.set_calculator(PysisCalculator(energy_evaluator))
        if out_dir is not None:
            i.calculator.out_dir = pathlib.Path(out_dir).resolve()

    if logger is None:
        cos_class.logger = PysisyphusLogger()
    else:
        cos_class.logger = logger
    base_cos = cos_class(
        images=images,
        **opts
    )
    if fixed_images is not None:
        fixed_images = list(fixed_images)
        base_get_fixed = base_cos.get_fixed_indices
        def get_fixed_indices(self, *args, **kwargs):
            """
            **LLM Docstring**

            Wrapped `get_fixed_indices` that unions the chain-of-states object's own fixed
            indices with the externally supplied ones.

            :param args: positional arguments forwarded to the base method
            :param kwargs: keyword arguments forwarded to the base method
            :return: the combined fixed indices
            :rtype: list
            """
            base = base_get_fixed(*args, **kwargs)
            if base is None:
                return fixed_images
            else:
                return sorted(list(base) + fixed_images)
        base_cos.get_fixed_indices = get_fixed_indices
    return base_cos

@register_method('growing-string')
def resolve_gsm(*, images, calc_getter=None, energy_evaluator=None,
                max_nodes=None,
                energies=None,
                distance_metric=None,
                masses=None,
                fit_order=2,
                peak_cutoff=.5,
                min_nodes=3,
                **opts):
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
    from pysisyphus.cos.GrowingString import GrowingString
    if calc_getter is None:
        if energy_evaluator is None:
            calc_getter = lambda **kwargs: images[0].calculator.copy()
        else:
            calc_getter = lambda **kwargs: PysisCalculator(energy_evaluator, **kwargs)
    if len(images) > 2:
        split_pos = opts.get('left_images')
        if split_pos is None:
            split_pos = get_dimer_image_guess(
                images,
                energies=energies,
                distance_metric=distance_metric,
                masses=masses,
                fit_order=fit_order,
                peak_cutoff=peak_cutoff,
                min_nodes=min_nodes
            )
        opts['left_images'] = split_pos
        opts['right_images'] = len(images) - split_pos
    if max_nodes is None:
        max_nodes = len(images)
    gsm = resolve_cos_method(
        cos_class=GrowingString,
        images=images,
        calc_getter=calc_getter,
        energy_evaluator=energy_evaluator,
        max_nodes=max_nodes,
        **opts
    )
    return gsm
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
    from pysisyphus.cos.ChainOfStates import ChainOfStates
    return resolve_cos_method(
        cos_class=ChainOfStates,
        images=images,
        energy_evaluator=energy_evaluator,
        **opts
    )
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
    from pysisyphus.cos.FreezingString import FreezingString
    if calc_getter is None:
        if energy_evaluator is None:
            calc_getter = lambda **kwargs: images[0].calculator.copy()
        else:
            calc_getter = lambda **kwargs: PysisCalculator(energy_evaluator, **kwargs)
    # if len(images) > 2:
    #     opts['left_images'] = opts.get('left_images', len(images) // 2)
    #     opts['right_images'] = opts.get('right_images', len(images) - (len(images) // 2))

    return resolve_cos_method(
        cos_class=FreezingString,
        images=images,
        calc_getter=calc_getter,
        energy_evaluator=energy_evaluator,
        **opts
    )
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
    from pysisyphus.cos.SimpleZTS import SimpleZTS
    return resolve_cos_method(
        cos_class=SimpleZTS,
        images=images,
        energy_evaluator=energy_evaluator,
        **opts
    )
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
    from pysisyphus.cos.NEB import NEB
    return resolve_cos_method(
        cos_class=NEB,
        images=images,
        energy_evaluator=energy_evaluator,
        **opts
    )

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
    if geom.calculator is None:
        geom.set_calculator(PysisCalculator(energy_evaluator))
    if out_dir is not None:
        geom.calculator.out_dir = pathlib.Path(out_dir).resolve()
    return geom

@register_method('ts')
def resolve_ts(*, images,
               energy_evaluator=None,
               energies=None,
               image_guess=None,
               distance_metric=None,
               masses=None,
               fit_order=2,
               peak_cutoff=.5,
               min_nodes=3,
               climb=True,
               logger=None,
               out_dir=None,
               use_max_for_guess=True,
               eliminate_guess_nodes=True,
               **opts):
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
    if not climb: raise NotImplementedError("ts calcs only implemented for `climb=True`")

    if image_guess is None:
        for i in images:
            if i.calculator is None:
                i.set_calculator(PysisCalculator(energy_evaluator))
            if out_dir is not None:
                i.calculator.out_dir = pathlib.Path(out_dir).resolve()
        image_guess = get_dimer_image_guess(
            base_images=images,
            energies=energies,
            distance_metric=distance_metric,
            masses=masses,
            fit_order=fit_order,
            peak_cutoff=peak_cutoff,
            min_nodes=min_nodes,
            use_max_for_guess=use_max_for_guess
        )
    target_image = images[image_guess]
    if target_image.calculator is None:
        target_image.set_calculator(PysisCalculator(energy_evaluator))
    if out_dir is not None:
        target_image.calculator.out_dir = pathlib.Path(out_dir).resolve()

    return target_image

def get_dimer_image_guess(base_images,
                          energies=None,
                          distance_metric=None,
                          masses=None,
                          *,
                          fit_order=2,
                          peak_cutoff,
                          min_nodes=3,
                          use_max_for_guess=False
                          ):
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
    if energies is None:
        for m in base_images:
            m.calc_energy()
        energies = [m.results['energy'] for m in base_images]
    energies = np.array(energies)
    product = np.argmin(energies)
    ts = np.argmax(energies)
    if use_max_for_guess:
        if ts > 0:
            if ts < len(energies) - 1:
                if energies[ts + 1] < energies[ts - 1]:
                    ts = ts - 1
            else:
                ts = len(energies) - 2
        return ts

    if product > ts:
        reactant = np.argmin(energies[:ts])
    else:
        reactant = np.argmin(energies[ts:])

    offset_energies = (energies - energies[reactant]) / (energies[ts] - energies[reactant])

    if masses is None:
        symbols = base_images[0].atoms
        masses = [AtomData[a, "Mass"] for a in symbols]
    geoms = np.array([b.cart_coords.reshape(-1, 3) for b in base_images])
    if distance_metric is None:
        distance_metric = lambda *args, **kwargs: nput.incremental_eckart_rmsd(*args, mass_weighted=True, **kwargs)
    distances = distance_metric(
        geoms,
        masses=masses,
    )

    distances = nput.vec_rescale(distances)

    ts_pos_guess, _ = nput.peak_fit_maxiumum(distances, offset_energies,
                                             peak_cutoff=peak_cutoff,
                                             min_nodes=min_nodes,
                                             fit_order=fit_order)

    # find the two images nearest to this guessed value
    insert_idx = np.searchsorted(distances, ts_pos_guess)

    return insert_idx

@register_method('dimer')
def resolve_dimer(*, images, energy_evaluator=None,
                  energies=None,
                  image_guess=None,
                  distance_metric=None,
                  masses=None,
                  fit_order=2,
                  peak_cutoff=.5,
                  min_nodes=3,
                  displacement_vector=None,
                  climb=True,
                  logger=None,
                  out_dir=None,
                  use_max_for_guess=True,
                  eliminate_guess_nodes=True,
                  fixed_images=None,
                  **opts):
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
    if not climb: raise NotImplementedError("dimer calcs only implemented for `climb=True`")

    if fixed_images is not None:
        raise ValueError("can't run dimer with fixed images")

    from pysisyphus.calculators.Dimer import Dimer
    if image_guess is None:
        for i in images:
            if i.calculator is None:
                i.set_calculator(PysisCalculator(energy_evaluator))
            if out_dir is not None:
                i.calculator.out_dir = pathlib.Path(out_dir).resolve()
        image_guess = get_dimer_image_guess(
            base_images=images,
            energies=energies,
            distance_metric=distance_metric,
            masses=masses,
            fit_order=fit_order,
            peak_cutoff=peak_cutoff,
            min_nodes=min_nodes,
            use_max_for_guess=use_max_for_guess
        )
    if displacement_vector is None:
        displacement_vector = images[image_guess + 1].cart_coords - images[image_guess].cart_coords
    target_image = images[image_guess]
    if target_image.calculator is None:
        target_image.set_calculator(PysisCalculator(energy_evaluator))
    if out_dir is not None:
        target_image.calculator.out_dir = pathlib.Path(out_dir).resolve()

    with dev.OutputRedirect():
        dimer_calc = Dimer(
            calculator=target_image.calculator,
            N_raw=displacement_vector,  # optional: seed orientation from COS tangent
            out_dir=out_dir,
            **opts
        )
    if logger is not None:
        dimer_calc.logger = logger
    target_image.set_calculator(dimer_calc)
    if out_dir is not None:
        target_image.calculator.out_dir = pathlib.Path(out_dir).resolve()
    if eliminate_guess_nodes:
        target_image.eliminated_nodes = [image_guess + 1]

    return target_image

method_aliases = {
    'gsm':'growing-string',
    'cos':'chain-of-states',
    'fsm':'freezing-string',
    'zts':'zero-temperature-string',
    'string':'zero-temperature-string'
}
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
    if isinstance(method_name, str):
        method_name = method_aliases.get(method_name, method_name)
        method_name = method_resolvers[method_name]
    generator = method_name(logger=logger, **opts)
    if logger is not None:
        generator.logger = logger
    return generator

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
    if method is not None:
        optimizer_resolvers[name] = method
        return method
    else:
        def register(method, name=name):
            """
            **LLM Docstring**

            Decorator that registers the wrapped resolver under the captured optimizer name.

            :param method: the resolver being registered
            :type method: Callable
            :param name: the optimizer name
            :type name: str
            :return: the registered resolver
            :rtype: Callable
            """
            return register_optimizer(name, method)
        return register

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
    import pysisyphus.optimizers
    mod = getattr(pysisyphus.optimizers, name)
    cls = getattr(mod, name)
    def resolve(traj, **opts):
        """
        **LLM Docstring**

        Instantiate the resolved optimizer class for a trajectory.

        :param traj: the trajectory/geometry to optimize
        :param opts: extra optimizer options
        :return: the optimizer instance
        :rtype: object
        """
        return cls(traj, **opts)
    return resolve
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
    from pysisyphus.optimizers.StringOptimizer import StringOptimizer
    if not hasattr(traj, 'string_size'):
        traj.string_size = len(
            traj.all_cart_coords
        )
        traj.fully_grown = True
    return StringOptimizer(
        traj,
        **opts
    )
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
    from pysisyphus.optimizers.LBFGS import LBFGS
    return LBFGS(
        traj,
        **opts
    )
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
    from pysisyphus.optimizers.RFOptimizer import RFOptimizer
    return RFOptimizer(
        traj,
        **opts
    )
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
    from pysisyphus.optimizers.PreconLBFGS import PreconLBFGS
    return PreconLBFGS(
        traj,
        **opts
    )
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
    from pysisyphus.optimizers.BFGS import BFGS
    return BFGS(
        traj,
        **opts
    )
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
    from pysisyphus.tsoptimizers.RSPRFOptimizer import RSPRFOptimizer
    return RSPRFOptimizer(
        traj,
        **opts
    )
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
    from pysisyphus.tsoptimizers.RSIRFOptimizer import RSIRFOptimizer
    return RSIRFOptimizer(
        traj,
        **opts
    )
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
    from pysisyphus.tsoptimizers import TRIM
    return TRIM(
        traj,
        **opts
    )
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
    from pysisyphus.optimizers.FIRE import FIRE
    return FIRE(
        traj,
        **opts
    )
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
    from pysisyphus.optimizers.CubicNewton import CubicNewton
    return CubicNewton(
        traj,
        **opts
    )
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
    from pysisyphus.optimizers.ConjugateGradient import ConjugateGradient
    return ConjugateGradient(
        traj,
        **opts
    )
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
    from pysisyphus.optimizers.SteepestDescent import SteepestDescent
    return SteepestDescent(
        traj,
        **opts
    )

class PysisyphusLogger:
    def __init__(self, log_file=None):
        """
        **LLM Docstring**

        Wrap a McUtils logger for use as a Pysisyphus logger.

        :param log_file: the log file (or logger) to wrap
        :type log_file: str | object | None
        """
        self.base_logger = dev.Logger.lookup(log_file)
    def log(self, log_level, *args, **opts):
        """
        **LLM Docstring**

        Log a message at the given level.

        :param log_level: the log level
        :param args: the message parts
        :param opts: extra logging options
        """
        self.base_logger.log_print(*args, **opts, log_level=log_level)
    def debug(self, *args, **opts):
        """
        **LLM Docstring**

        Log a debug-level message.

        :param args: the message parts
        :param opts: extra logging options
        """
        self.base_logger.log_print(*args, log_level=self.base_logger.LogLevel.Debug, **opts)
    def error(self, *args, **opts):
        """
        **LLM Docstring**

        Log an error-level message.

        :param args: the message parts
        :param opts: extra logging options
        """
        self.base_logger.log_print(*args, **opts)


optimizer_method_map = {
    'growing-string':'string',
    'freezing-string':'string',
    'zero-temperature-string':'string',
    'chain-of-states':'string',
    'neb':'lbfgs',
    'dimer':'lbfgs',
    'optimize': 'lbfgs',
    'ts':'rsprfo'
}
def resolve_pysis_optimizer(optimizer, method_name, generator, logger=None,
                            **opts):
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
    if optimizer is None:
        method_name = method_aliases.get(method_name, method_name)
        optimizer = optimizer_method_map[method_name]
    if isinstance(optimizer, str):
        opt = optimizer_resolvers.get(optimizer)
        if opt is None: opt = resolve_generic_optimizer(optimizer)
        optimizer = opt

    with suppress_logging():
        # if tol is not None:
        #     if opt is not None:
        #     opts['max_rms']
        optimizer = optimizer(generator, **opts)
    if logger is not None:
        optimizer.logger = logger
        optimizer.table.logger = logger
    return optimizer

def parse_trj(file):
    """
    **LLM Docstring**

    Parse an XYZ trajectory (`.trj`) file into its geometries.

    :param file: the trajectory file
    :type file: str
    :return: the parsed geometries
    :rtype: list
    """
    with XYZParser(file) as xyz:
        geoms = xyz.parse()
    return geoms

def run_pysisyphus(
        energy_evaluator,
        method,
        optimizer=None,
        optimizer_settings=None,
        max_cycles=None,
        max_step=None,
        max_displacement=None,
        thresh=None,
        tol=None,
        use_max_for_error=True,
        log_file=None,
        out_dir=None,
        return_logs=True,
        patch_logging=True,
        logger=None,
        ignore_zero_steps=True,
        **kwargs
):
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
    if patch_logging:
        patch_pysis_logging()

    if optimizer_settings is None:
        optimizer_settings = {}
    optimizer_settings = optimizer_settings.copy()
    if max_cycles is not None:
        optimizer_settings['max_cycles'] = max_cycles
    if max_step is None and max_step is not None:
        max_step = max_displacement
    if max_step is not None:
        optimizer_settings['max_step'] = max_step
        # optimizer_settings['trust_max'] = max_step
    if thresh is None:
        if tol is not None:
            optimizer_settings['rms_force'] = tol
        if use_max_for_error:
            optimizer_settings['max_force_only'] = True
            # if use_max_for_error:
            #     optimizer_settings['max_force'] = tol
            # elif use_max_for_error is False:
            #     optimizer_settings['rms_force'] = tol
            # else:
            #     optimizer_settings['max_force'] = tol
            #     optimizer_settings['rms_force'] = tol
    if logger is None:
        logger = PysisyphusLogger(log_file)
    elif not hasattr(logger, 'log'):
        logger = PysisyphusLogger(logger)
    with dev.DefaultDirectory(out_dir) as od:
        import pysisyphus.config
        cur_od = pysisyphus.config.OUT_DIR_DEFAULT
        import pysisyphus.optimizers.exceptions
        try:
            pysisyphus.config.OUT_DIR_DEFAULT = od
            generator = resolve_pysis_method(method, energy_evaluator=energy_evaluator,
                                             out_dir=od,
                                             logger=logger, **kwargs)
            optimizer = resolve_pysis_optimizer(optimizer, method, generator,
                                                out_dir=od,
                                                logger=logger,
                                                **optimizer_settings)
            with _patched_eigh():
                if ignore_zero_steps:
                    try:
                        optimizer.run()
                    except pysisyphus.optimizers.exceptions.ZeroStepLength:
                        ...
                else:
                    optimizer.run()
        finally:
            pysisyphus.config.OUT_DIR_DEFAULT = cur_od
        if return_logs:
            logs = {
                f:(
                    dev.read_file(f)
                        if not f.endswith('.trj') else
                    parse_trj(f)
                )
                for f in os.listdir(od)
            }
        else:
            logs = None
    return generator, optimizer, logs


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
    if method is not None:
        interpolator_resolvers[name] = method
        return method
    else:
        def register(method, name=name):
            """
            **LLM Docstring**

            Decorator that registers the wrapped resolver under the captured interpolator
            name.

            :param method: the resolver being registered
            :type method: Callable
            :param name: the interpolator name
            :type name: str
            :return: the registered resolver
            :rtype: Callable
            """
            return register_interpolator(name, method)
        return register
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
    from pysisyphus.interpolate.IDPP import IDPP
    return IDPP(geoms, **opts)
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
    from pysisyphus.interpolate.Interpolator import Interpolator
    return Interpolator(geoms, **opts)
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
    from pysisyphus.interpolate.Redund import Redund
    return Redund(geoms, **opts)
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
    if isinstance(interpolator, str):
        interpolator = interpolator_resolvers[interpolator]
    return interpolator(traj, **opts)

# # Use 'tric', if requested; otherwise always use 'redund'
#         sp_coord_type = "tric" if coord_type == "tric" else "redund"
#         geom_0 = geoms[0].copy(coord_type=sp_coord_type)
#         geom_m1 = geoms[-1].copy(coord_type=sp_coord_type)
#         typed_prims = form_coordinate_union(geom_0, geom_m1)
#         geom_kwargs["coord_kwargs"]["typed_prims"] = typed_prims
#
#     return [
#         Geometry(geom.atoms, geom.cart_coords, coord_type=coord_type, **geom_kwargs)
#         for geom in geoms
#     ]
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
    if np.linalg.eigh.__module__ == 'numpy.linalg':
        _np_eigh = np.linalg.eigh
        def _safe_eigh(a, *args, **kwargs):
            """
            **LLM Docstring**

            Symmetrize the input matrix and diagonalize it, falling back to SciPy's `eigh`
            if NumPy's fails.

            :param a: the matrix to diagonalize
            :type a: np.ndarray
            :param args: extra positional arguments for `eigh`
            :param kwargs: extra keyword arguments for `eigh`
            :return: the eigenvalues and eigenvectors
            :rtype: tuple
            """
            a = (a + np.moveaxis(a, -1, -2)) / 2
            try:
                return _np_eigh(a, *args, **kwargs)
            except np.linalg.LinAlgError:
                return scipy.linalg.eigh(a)

        try:
            np.linalg.eigh = _safe_eigh
            yield _safe_eigh
        finally:
            np.linalg.eigh = _np_eigh
    else:
        yield np.linalg.eigh

def prep_pysis_images(atoms,
                      geometry,
                      coord_type='cartesian',
                      coord_kwargs=None,
                      **opts):
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
    patch_pysis_logging()

    from pysisyphus.Geometry import Geometry
    from pysisyphus.intcoords.helpers import form_coordinate_union

    import pysisyphus.intcoords.logging_conf
    _remove_handlers(pysisyphus.intcoords.logging_conf.logger)

    pre_union = coord_type == "cartesian" or (coord_kwargs is not None and 'typed_prims' in coord_kwargs)
    geometry = np.array(geometry)
    smol = geometry.ndim == 2
    if smol:
        geometry = [geometry]
    base_geoms = [
        Geometry(
            atoms,
            coords,
            coord_kwargs=coord_kwargs,
            coord_type=coord_type,
            **opts
        )
        for coords in geometry
    ]
    if not pre_union:
        start = base_geoms[0].copy(coord_type=coord_type)
        end = base_geoms[-1].copy(coord_type=coord_type)
        typed_prims = form_coordinate_union(start, end)
        if coord_kwargs is None:
            coord_kwargs = {}
        coord_kwargs["typed_prims"] = typed_prims
        base_geoms = [
            Geometry(geom.atoms, geom.cart_coords, coord_type=coord_type, coord_kwargs=coord_kwargs, **opts)
            for geom in base_geoms
        ]

    if smol:
        base_geoms = base_geoms[0]
    return base_geoms

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
    interpolator = resolve_pysis_interpolator(interpolator, geoms, **opts)
    all_geoms = interpolator.interpolate()
    return [a.cart_coords.reshape(-1, 3) for a in all_geoms]