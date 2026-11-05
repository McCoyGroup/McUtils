"""
Readouts: digestible, exportable summaries of results.

An object that implements `ReadoutInterface` builds a `Readout` (``obj.to_readout(...)``):
a backend-neutral tree of sections, tables, fields and 3D scenes. The same tree displays in
Jupyter and exports to HTML, PowerPoint, plain text, ``.npz``, pandas and JSON, and every export
reports the same values in the same (display) units.

Nothing at import time depends on Jupyter or the plotting stack: the renderers load `McUtils.Jupyter` (HTML) and
`McUtils.Plots` (scenes, PowerPoint) only when something is actually rendered. Import readout
objects directly from `McUtils.Readouts`.
"""

__all__ = []
from .Data import *; from .Data import __all__ as exposed
__all__ += exposed
from .Styles import *; from .Styles import __all__ as exposed
__all__ += exposed
from .Nodes import *; from .Nodes import __all__ as exposed
__all__ += exposed
from .Scenes import *; from .Scenes import __all__ as exposed
__all__ += exposed
from .Interface import *; from .Interface import __all__ as exposed
__all__ += exposed
from .Views import *; from .Views import __all__ as exposed
__all__ += exposed
from .Builders import *; from .Builders import __all__ as exposed
__all__ += exposed
from .Renderers import *; from .Renderers import __all__ as exposed
__all__ += exposed
del exposed
