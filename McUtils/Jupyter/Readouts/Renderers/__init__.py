"""
Renderers turn a readout tree into a concrete output. Each renderer dispatches on node class
(through the MRO), after first giving the node a chance to render itself through a hook method
(``to_html``, ``to_presml``, ``to_text``), so new node types and new backends can be added
independently.
"""

__all__ = []
from .Base import *; from .Base import __all__ as exposed
__all__ += exposed
from .Text import *; from .Text import __all__ as exposed
__all__ += exposed
from .Data import *; from .Data import __all__ as exposed
__all__ += exposed
from .HTML import *; from .HTML import __all__ as exposed
__all__ += exposed
from .PowerPoint import *; from .PowerPoint import __all__ as exposed
__all__ += exposed
del exposed
