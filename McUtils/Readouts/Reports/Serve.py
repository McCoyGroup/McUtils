"""
Serve a report file as an MCP server: ``python -m McUtils.Readouts.Reports report.md --sources my_sources.py``.

The sources module defines ``build_catalog() -> SourceCatalog``. The report file is read if it exists (else started
empty) and rewritten after every change a tool makes.
"""

import importlib
import importlib.util
import os
import sys

from .Sources import SourceCatalog
from .Document import ReportDocument
from .Render import ReportRenderer
from .Tools import report_toolset

__all__ = ["load_catalog", "serve_report"]

from .Instructions import REPORT_INSTRUCTIONS     # noqa: E402  (kept importable from here)


def load_catalog(sources):
    """``build_catalog()`` from a module given as a ``.py`` path or a dotted module name."""
    if sources.endswith(".py") or os.sep in sources:
        path = os.path.abspath(sources)
        spec = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(path))[0], path)
        mod = importlib.util.module_from_spec(spec)
        sys.path.insert(0, os.path.dirname(path))
        try:
            spec.loader.exec_module(mod)
        finally:
            sys.path.pop(0)
    else:
        mod = importlib.import_module(sources)
    if not hasattr(mod, "build_catalog"):
        raise ValueError(f"{sources!r} defines no build_catalog()")
    catalog = mod.build_catalog()
    if not isinstance(catalog, SourceCatalog):
        raise TypeError(f"build_catalog() must return a SourceCatalog, got {type(catalog).__name__}")
    return catalog


def _save(doc, path):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(doc.to_markdown())
    os.replace(tmp, path)


def serve_report(md_path, sources, out_dir=None, policy="grounded", rel_tol=1e-3, small_int_max=10, year_range=(1900, 2100), title=None, lock=(), unlock=(), call_log=None, stdin=None, stdout=None,
                 allow_derived=False, apply_edits=False, context_level=2, include_tools=None, exclude_tools=None, unit_style=None):
    """
    Load (or start) the report at ``md_path`` against the catalog of ``sources`` and serve its tools on stdio.
    ``context_level`` (1 compact, 2 standard, 3 full) sets the tools and instructions the model gets (see
    `report_toolset`). ``allow_derived`` (computed values in text) and ``apply_edits`` (the multi-edit tool) are off
    unless the owner switches them on. ``unit_style`` (``unicode``, ``ascii`` or ``latex``) is how filled values write
    their unit; it is stored in the report.
    """
    from ...JobDrivers.MCP import MCPServer
    md_path = os.path.abspath(md_path)
    catalog = sources if isinstance(sources, SourceCatalog) else load_catalog(sources)
    if os.path.exists(md_path):
        with open(md_path, encoding="utf-8") as f:
            doc = ReportDocument.from_markdown(f.read(), catalog)
        for problem in doc.validate():
            print(f"[report] {problem}", file=sys.stderr, flush=True)
    else:
        doc = ReportDocument(title or os.path.splitext(os.path.basename(md_path))[0].replace("_", " ").title(), catalog)
        _save(doc, md_path)
    if unlock:
        doc.unlock(list(unlock))
    if lock:
        doc.lock(list(lock))
    if lock or unlock:
        _save(doc, md_path)
    out_dir = os.path.abspath(out_dir or os.path.join(os.path.dirname(md_path), os.path.splitext(os.path.basename(md_path))[0] + "_out"))
    tools = report_toolset(doc, catalog, renderer=ReportRenderer(catalog), policy=policy, rel_tol=rel_tol,
                           small_int_max=small_int_max, year_range=year_range, out_dir=out_dir, on_change=lambda d: _save(d, md_path),
                           allow_derived=allow_derived, apply_edits=apply_edits, context_level=context_level, include_tools=include_tools,
                           exclude_tools=exclude_tools, unit_style=unit_style)
    MCPServer(tools, name="mcutils-report", instructions=tools.instructions,
              call_log=call_log).serve(stdin, stdout)
    return doc
