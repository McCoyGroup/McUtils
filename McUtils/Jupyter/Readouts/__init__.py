"""
Readouts: digestible, exportable summaries of results.

An object that implements `ReadoutInterface` builds a `Readout` (``obj.to_readout(...)``):
a backend-neutral tree of sections, tables, fields and 3D scenes. The same tree displays in
Jupyter and exports to HTML, PowerPoint, plain text, ``.npz``, pandas and JSON, and every export
reports the same values in the same (display) units.

Despite living under `McUtils.Jupyter`, nothing here requires Jupyter.
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
from .Registry import *; from .Registry import __all__ as exposed
__all__ += exposed
from .Structures import *; from .Structures import __all__ as exposed
__all__ += exposed
from .Charts import *; from .Charts import __all__ as exposed
__all__ += exposed
from .Renderers import *; from .Renderers import __all__ as exposed
__all__ += exposed
del exposed
