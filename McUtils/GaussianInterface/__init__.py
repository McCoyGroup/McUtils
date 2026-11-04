"""
**Deprecated.** The Gaussian readers now live in `McUtils.ExternalPrograms.Parsers`, alongside the readers for the
other electronic structure programs::

    from McUtils.ExternalPrograms.Parsers import GaussianLogReader, GaussianFChkReader

This package is kept as a thin alias (resolving to the very same classes) until the Gaussian parsers are folded into
`ExternalPrograms` proper. Using any name from it emits a `McUtilsDeprecationWarning`; set
``MCUTILS_DEPRECATIONS=error`` to turn those into errors so remaining callers can be found.
"""
from ..Devutils.Deprecation import deprecate_module_namespace
from ..ExternalPrograms.Parsers import GaussianImporter as _importer
from ..ExternalPrograms.Parsers import FChkDerivatives as _derivatives

deprecate_module_namespace(
    __name__, globals(), [_importer, _derivatives],
    new="McUtils.ExternalPrograms.Parsers",
    since="1.8.0",
    remove_in="2.0.0"
)
