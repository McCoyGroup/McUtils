
import os
import tempfile
import logging
from contextlib import contextmanager
import pathlib

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
    logger.handlers.clear()
    if max_depth > 0:
        if logger.parent and (logger.parent is not logger):
            _remove_handlers(logger.parent, max_depth=max_depth-1)
def patch_pysis_logging():
    import pysisyphus
    _remove_handlers(pysisyphus.logger)

    with dev.OutputRedirect():
        import pysisyphus.init_logging
        pysisyphus.init_logging.LOGGERS.clear()
        import pysisyphus.config

    def get_fh_logger(name, log_fn, base=pysisyphus.init_logging.get_fh_logger):
        base(name, log_fn)
        logger = logging.getLogger(name)
        _remove_handlers(logger)
    pysisyphus.init_logging.get_fh_logger = get_fh_logger

    import pysisyphus.optimizers.Optimizer
    def configure_opt_logger(logger, prefix, base=pysisyphus.optimizers.Optimizer.configure_opt_logger):
        _remove_handlers(logger)
        # base(logger=logger, prefix=prefix)
        # _remove_handlers(logger)
    pysisyphus.optimizers.Optimizer.configure_opt_logger = configure_opt_logger

    import pysisyphus.calculators
    _remove_handlers(pysisyphus.calculators.logger)

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
    if method is not None:
        method_resolvers[name] = method
        return method
    else:
        def register(method, name=name):
            return register_method(name, method)
        return register

def resolve_cos_method(*, images, cos_class, energy_evaluator=None,
                       out_dir=None,
                       logger=None,
                       **opts):
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
    return cos_class(
        images=images,
        **opts
    )
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
    from pysisyphus.cos.ChainOfStates import ChainOfStates
    return resolve_cos_method(
        cos_class=ChainOfStates,
        images=images,
        energy_evaluator=energy_evaluator,
        **opts
    )
@register_method('freezing-string')
def resolve_freezing_string(*, images, calc_getter=None, energy_evaluator=None, **opts):
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
    from pysisyphus.cos.SimpleZTS import SimpleZTS
    return resolve_cos_method(
        cos_class=SimpleZTS,
        images=images,
        energy_evaluator=energy_evaluator,
        **opts
    )
@register_method('neb')
def resolve_neb(*, images, energy_evaluator=None, **opts):
    from pysisyphus.cos.NEB import NEB
    return resolve_cos_method(
        cos_class=NEB,
        images=images,
        energy_evaluator=energy_evaluator,
        **opts
    )

@register_method('optimize')
def resolve_optimize(*, geom, energy_evaluator=None, out_dir=None, **opts):
    if geom.calculator is None:
        geom.set_calculator(PysisCalculator(energy_evaluator))
    if out_dir is not None:
        geom.calculator.out_dir = pathlib.Path(out_dir).resolve()
    return geom

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
                  use_max_for_guess=False,
                  eliminate_guess_nodes=True,
                  **opts):
    if not climb: raise NotImplementedError("dimer calcs only implemented for `climb=True`")

    from pysisyphus.calculators.Dimer import Dimer
    if image_guess is None:
        for i in images:
            if i.calculator is None:
                i.set_calculator(PysisCalculator(energy_evaluator))
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
    if isinstance(method_name, str):
        method_name = method_aliases.get(method_name, method_name)
        method_name = method_resolvers[method_name]
    generator = method_name(logger=logger, **opts)
    if logger is not None:
        generator.logger = logger
    return generator

optimizer_resolvers = {}
def register_optimizer(name, method=None):
    if method is not None:
        optimizer_resolvers[name] = method
        return method
    else:
        def register(method, name=name):
            return register_optimizer(name, method)
        return register

def resolve_generic_optimizer(name):
    import pysisyphus.optimizers
    mod = getattr(pysisyphus.optimizers, name)
    cls = getattr(mod, name)
    def resolve(traj, **opts):
        return cls(traj, **opts)
    return resolve
@register_optimizer('string')
def resolve_string_optimizer(traj, **opts):
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
    from pysisyphus.optimizers.LBFGS import LBFGS
    return LBFGS(
        traj,
        **opts
    )
@register_optimizer('rfo')
def resolve_lrfo_optimizer(traj, **opts):
    from pysisyphus.optimizers.RFOptimizer import RFOptimizer
    return RFOptimizer(
        traj,
        **opts
    )
@register_optimizer('plbfgs')
def resolve_plbfgs_optimizer(traj, **opts):
    from pysisyphus.optimizers.PreconLBFGS import PreconLBFGS
    return PreconLBFGS(
        traj,
        **opts
    )
@register_optimizer('rsprfo')
def resolve_rsprfo_optimizer(traj, **opts):
    from pysisyphus.tsoptimizers.RSPRFOptimizer import RSPRFOptimizer
    return RSPRFOptimizer(
        traj,
        **opts
    )
@register_optimizer('trim')
def resolve_trim_optimizer(traj, **opts):
    from pysisyphus.tsoptimizers import TRIM
    return TRIM(
        traj,
        **opts
    )

class PysisyphusLogger:
    def __init__(self, log_file=None):
        self.base_logger = dev.Logger.lookup(log_file)
    def log(self, log_level, *args, **opts):
        self.base_logger.log_print(*args, **opts, log_level=log_level)
    def debug(self, *args, **opts):
        self.base_logger.log_print(*args, log_level=self.base_logger.LogLevel.Debug, **opts)
    def error(self, *args, **opts):
        self.base_logger.log_print(*args, **opts)


optimizer_method_map = {
    'growing-string':'string',
    'freezing-string':'string',
    'zero-temperature-string':'string',
    'chain-of-states':'string',
    'neb':'lbfgs',
    'dimer':'lbfgs'
}
def resolve_pysis_optimizer(optimizer, method_name, generator, logger=None,
                            **opts):
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
        **kwargs
):
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
    elif hasattr(logger, 'log_print'):
        logger = PysisyphusLogger(logger)
    with dev.DefaultDirectory(out_dir) as od:
        import pysisyphus.config
        cur_od = pysisyphus.config.OUT_DIR_DEFAULT
        try:
            pysisyphus.config.OUT_DIR_DEFAULT = od
            generator = resolve_pysis_method(method, energy_evaluator=energy_evaluator,
                                             out_dir=od,
                                             logger=logger, **kwargs)
            optimizer = resolve_pysis_optimizer(optimizer, method, generator,
                                                out_dir=od,
                                                logger=logger,
                                                **optimizer_settings)
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
    if method is not None:
        interpolator_resolvers[name] = method
        return method
    else:
        def register(method, name=name):
            return register_interpolator(name, method)
        return register
@register_interpolator('idpp')
def resolve_idpp(geoms, **opts):
    from pysisyphus.interpolate.IDPP import IDPP
    return IDPP(geoms, **opts)
@register_interpolator('linear')
def resolve_linear(geoms, **opts):
    from pysisyphus.interpolate.Interpolator import Interpolator
    return Interpolator(geoms, **opts)
@register_interpolator('redund')
def resolve_redund(geoms, **opts):
    from pysisyphus.interpolate.Redund import Redund
    return Redund(geoms, **opts)
def resolve_pysis_interpolator(interpolator, traj, logger=None, **opts):
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

def prep_pysis_images(atoms,
                      geometry,
                      coord_type='cartesian',
                      coord_kwargs=None,
                      **opts):
    patch_pysis_logging()

    from pysisyphus.Geometry import Geometry
    from pysisyphus.intcoords.helpers import form_coordinate_union

    import pysisyphus.intcoords.logging_conf
    _remove_handlers(pysisyphus.intcoords.logging_conf.logger)

    pre_union = coord_type == "cartesian" or (coord_kwargs is not None and 'typed_prims' in coord_kwargs)
    geometry = np.asanyarray(geometry)
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
    interpolator = resolve_pysis_interpolator(interpolator, geoms, **opts)
    all_geoms = interpolator.interpolate()
    return [a.cart_coords.reshape(-1, 3) for a in all_geoms]