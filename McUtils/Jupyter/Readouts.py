"""
Compatibility alias: `McUtils.Jupyter.Readouts` is now `McUtils.Readouts`.

Names resolve to the same objects as in `McUtils.Readouts` (submodules are reachable as attributes, e.g.
``McUtils.Jupyter.Readouts.Nodes``, but not through ``from McUtils.Jupyter.Readouts.Nodes import ...``;
import those from `McUtils.Readouts.Nodes`).
"""
from .. import Readouts as _readouts
from ..Readouts import *
from ..Readouts import __all__

def __getattr__(name):
    if name.startswith("__"):
        raise AttributeError(name)
    return getattr(_readouts, name)
