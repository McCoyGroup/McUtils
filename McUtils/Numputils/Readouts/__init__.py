"""
Readouts for `McUtils.Numputils` results. The optimizers return plain tuples, so results are
wrapped in an `OptimizationRun` record (built with one of its ``from_*`` constructors) which
supports ``to_readout()``.
"""

__all__ = []
from .Optimization import *; from .Optimization import __all__ as exposed
__all__ += exposed
del exposed
