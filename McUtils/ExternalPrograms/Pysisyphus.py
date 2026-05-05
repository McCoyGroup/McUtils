
import os
from .. import Devutils as dev
from ..Parsers import XYZParser

__all__ = [
    "PysisCalculator",
    "patch_pysis_logging",
    "run_pysisyphus"
]

def patch_pysis_logging():
    import pysisyphus
    pysisyphus.logger.removeHandler(pysisyphus.file_handler)
    pysisyphus.logger.removeHandler(pysisyphus.stdout_handler)
    with dev.OutputRedirect():
        import pysisyphus.config

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

def resolve_cos_method(*, images, cos_class, energy_evaluator=None, **opts):
    for i in images:
        if i.calculator is None:
            i.set_calculator(PysisCalculator(energy_evaluator))
    return cos_class(
        images=images,
        **opts
    )
@register_method('growing-string')
def resolve_gsm(*, images, calc_getter=None, energy_evaluator=None, **opts):
    from pysisyphus.cos.GrowingString import GrowingString
    if calc_getter is None:
        calc_getter = lambda **kwargs: PysisCalculator(energy_evaluator, **kwargs)
    if len(images) > 2:
        opts['left_images'] = opts.get('left_images', len(images) // 2)
        opts['right_images'] = opts.get('right_images', len(images) - (len(images) // 2))

    return resolve_cos_method(
        cos_class=GrowingString,
        images=images,
        calc_getter=calc_getter,
        energy_evaluator=energy_evaluator,
        **opts
    )
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
@register_method('neb')
def resolve_neb(*, images, energy_evaluator=None, **opts):
    from pysisyphus.cos.NEB import NEB
    return resolve_cos_method(
        cos_class=NEB,
        images=images,
        energy_evaluator=energy_evaluator,
        **opts
    )

method_aliases = {
    'gsm':'growing-string',
    'cos':'chain-of-states',
    'fsm':'freezing-string'
}
def resolve_pysis_method(method_name, **opts):
    if isinstance(method_name, str):
        method_name = method_aliases.get(method_name, method_name)
        method_name = method_resolvers[method_name]
    return method_name(**opts)

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

class PysisyphusLogger:
    def __init__(self, log_file=None):
        self.base_logger = dev.Logger.lookup(log_file)
    def log(self, *args, **opts):
        self.base_logger.log_print(*args, **opts)
    def debug(self, *args, **opts):
        self.base_logger.log_print(*args, log_level=self.base_logger.LogLevel.Debug, **opts)
    def error(self, *args, **opts):
        self.base_logger.log_print(*args, **opts)


optimizer_method_map = {
    'growing-string':'string',
    'freezing-string':'string',
    'chain-of-states':'lbfgs',
    'neb':'lbfgs'
}
def resolve_pysis_optimizer(optimizer, method_name, generator, **opts):
    if optimizer is None:
        method_name = method_aliases.get(method_name, method_name)
        optimizer = optimizer_method_map[method_name]
    if isinstance(optimizer, str):
        opt = optimizer_resolvers.get(optimizer)
        if opt is None: opt = resolve_generic_optimizer(optimizer)
        optimizer = opt
    return optimizer(generator, **opts)

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
        log_file=None,
        out_dir=None,
        return_logs=True,
        patch_logging=True,
        **kwargs
):
    if patch_logging:
        patch_pysis_logging()

    if optimizer_settings is None:
        optimizer_settings = {}
    if max_cycles is not None:
        optimizer_settings['max_cycles'] = max_cycles
    if max_step is not None:
        optimizer_settings['max_step'] = max_step
    logger = PysisyphusLogger(log_file)
    generator = resolve_pysis_method(method, energy_evaluator=energy_evaluator, **kwargs)
    generator.logger = logger
    with dev.DefaultDirectory(out_dir) as od:
        optimizer = resolve_pysis_optimizer(optimizer, method, generator,
                                            out_dir=od,
                                            **optimizer_settings)
        optimizer.logger = logger
        optimizer.table.logger = logger
        optimizer.run()
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