"""
Reports: composing readouts into documents.

A report is an ordered list of headings, readouts of named sources, prose and callouts (`ReportDocument`), built
against a `SourceCatalog`, serialized to Markdown in the readout-marker format of `McUtils.Docs`, and rendered to HTML
and PowerPoint (`ReportRenderer`).

Import from this subpackage directly (``from McUtils.Readouts.Reports import ReportDocument``); `McUtils.Readouts`
doesn't import it, because rendering pulls in `McUtils.Docs`.
"""

__all__ = []
from .Sources import *; from .Sources import __all__ as exposed
__all__ += exposed
from .Document import *; from .Document import __all__ as exposed
__all__ += exposed
from .History import *; from .History import __all__ as exposed
__all__ += exposed
from .Grounding import *; from .Grounding import __all__ as exposed
__all__ += exposed
from .Templates import *; from .Templates import __all__ as exposed
__all__ += exposed
from .Harness import *; from .Harness import __all__ as exposed
__all__ += exposed
from .Tools import *; from .Tools import __all__ as exposed
__all__ += exposed
from .Serve import *; from .Serve import __all__ as exposed
__all__ += exposed
from .Render import *; from .Render import __all__ as exposed
__all__ += exposed
del exposed
