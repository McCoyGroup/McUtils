"""
A growing package of assorted functionality that finds use across many different packages, but doesn't attempt to
provide a single unified interface for doing certain types of projects.

All of the McUtils packages stand mostly on their own, but there will be little calls into one another here and there,
especially pieces using `Numputils`

The more scientifically-focused `Psience` package makes significant use of `McUtils` as do various packages that have
been written over the years.
"""

__all__ = []

import McUtils.Data as Data
__all__ += ["Data"]
import McUtils.Numputils as Numputils
__all__ += ["Numputils"]
import McUtils.ExternalPrograms as ExternalPrograms
__all__ += ["ExternalPrograms"]
import McUtils.Plots as Plots
__all__ += ["Plots"]
import McUtils.Jupyter as Jupyter
__all__ += ["Jupyter"]
import McUtils.Parsers as Parsers
__all__ += ["Parsers"]
import McUtils.Formatters as Formatters
__all__ += ["Formatters"]
import McUtils.Coordinerds as Coordinerds
__all__ += ["Coordinerds"]
import McUtils.Zachary as Zachary
__all__ += ["Zachary"]
import McUtils.GaussianInterface as GaussianInterface
__all__ += ["GaussianInterface"]
import McUtils.Extensions as Extensions
__all__ += ["Extensions"]
import McUtils.Scaffolding as Scaffolding
__all__ += ["Scaffolding"]
import McUtils.Parallelizers as Parallelizers
__all__ += ["Parallelizers"]
import McUtils.Devutils as Devutils
__all__ += ["Devutils"]
import McUtils.Docs as Docs
__all__ += ["Docs"]
import McUtils.Misc as Misc
__all__ += ["Misc"]