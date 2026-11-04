"""
A small, uniform way to retire old import paths without breaking callers.

Behavior is controlled by the ``MCUTILS_DEPRECATIONS`` environment variable:

- ``warn`` (default): emit a `McUtilsDeprecationWarning` once per process per deprecated name
- ``error``: raise `McUtilsDeprecationError` instead, so every remaining caller can be found (use this in CI)
- ``ignore``: stay silent
"""

import os, sys, warnings

__all__ = [
    "McUtilsDeprecationWarning",
    "McUtilsDeprecationError",
    "deprecation_mode",
    "warn_deprecated",
    "deprecate_module_namespace",
    "list_deprecations",
]


class McUtilsDeprecationWarning(DeprecationWarning):
    """
    Emitted when a deprecated McUtils import path is used. A subclass of `DeprecationWarning` so it can be filtered
    separately; shown by default (plain `DeprecationWarning`s are hidden outside of `__main__`).
    """

class McUtilsDeprecationError(RuntimeError):
    """Raised instead of warning when ``MCUTILS_DEPRECATIONS=error``."""

warnings.filterwarnings("default", category=McUtilsDeprecationWarning)

_REGISTRY = {}  # old name -> metadata; also records what has already been warned about
_WARNED = set()
_SKIP_PREFIXES = ("<frozen importlib",)


def deprecation_mode():
    """The current mode: ``'warn'``, ``'error'`` or ``'ignore'``"""
    mode = os.environ.get("MCUTILS_DEPRECATIONS", "warn").strip().lower()
    return mode if mode in {"warn", "error", "ignore"} else "warn"


def _caller_stacklevel(skip=2):
    """Find the first frame that belongs to neither importlib nor this module (so the warning points at user code)"""
    level = skip
    frame = sys._getframe(skip - 1)
    while frame is not None and frame.f_code.co_filename.startswith(_SKIP_PREFIXES):
        frame = frame.f_back
        level += 1
    return level


def warn_deprecated(old, new, *, since=None, remove_in=None, message=None, once=True):
    """
    Warn (or raise, depending on `deprecation_mode`) that `old` is deprecated in favor of `new`.

    :param old: the dotted name of the deprecated object/module
    :param new: the dotted name (or short instruction) to use instead
    :param since: version the deprecation started in
    :param remove_in: version it is scheduled to be removed in
    :param once: only warn the first time `old` is used in a process
    """
    mode = deprecation_mode()
    _REGISTRY.setdefault(old, dict(new=new, since=since, remove_in=remove_in))
    if mode == "ignore" or (once and mode == "warn" and old in _WARNED):
        return
    if message is None:
        message = f"`{old}` is deprecated"
        if since is not None: message += f" (since {since})"
        if remove_in is not None: message += f" and will be removed in {remove_in}"
        message += f"; use `{new}` instead"
    if mode == "error":
        raise McUtilsDeprecationError(message)
    _WARNED.add(old)
    warnings.warn(message, McUtilsDeprecationWarning, stacklevel=_caller_stacklevel(3))


def deprecate_module_namespace(module_name, namespace, sources, *, new, since=None, remove_in=None):
    """
    Turn a module into a deprecated alias for names that live elsewhere. Call it from the old module with
    ``globals()``; it installs a module-level ``__getattr__`` (PEP 562), a ``__dir__`` and an ``__all__``.
    Names resolve to the *same objects* as in their new home (so `isinstance` and pickles still work) and the first
    attribute access (which includes ``from old import Name`` and ``import *``) warns; a bare import does not.

    :param module_name: ``__name__`` of the old module
    :param namespace: ``globals()`` of the old module
    :param sources: the modules the names now live in
    :param new: what to tell the user to import instead
    """
    exposed = []
    for src in sources:
        exposed.extend(getattr(src, "__all__", [n for n in vars(src) if not n.startswith("_")]))
    exposed = list(dict.fromkeys(exposed))
    _REGISTRY.setdefault(module_name, dict(new=new, since=since, remove_in=remove_in))

    def __getattr__(name):
        if name.startswith("__") or name not in exposed:
            raise AttributeError(f"module {module_name!r} has no attribute {name!r}")
        warn_deprecated(module_name, new, since=since, remove_in=remove_in)
        for src in sources:
            if hasattr(src, name):
                return getattr(src, name)
        raise AttributeError(name)

    namespace["__getattr__"] = __getattr__
    namespace["__dir__"] = lambda: sorted(set(namespace) | set(exposed))
    namespace["__all__"] = exposed


def list_deprecations():
    """Everything registered so far, as ``{old: {new, since, remove_in}}``"""
    return dict(_REGISTRY)
