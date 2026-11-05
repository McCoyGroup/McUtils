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

__all__ = ["load_catalog", "serve_report", "REPORT_INSTRUCTIONS"]

REPORT_INSTRUCTIONS = """\
You are building a report from readouts of named sources. You choose and order content and write short captions and
prose; the server renders everything.

Start with list_sources, then describe_source for each source you use: it shows the sections, what each contains, and
the source's report template. If the template has an outline, apply_template builds it in one call (optionally with
some of the template's optional sections); then adjust with add_readout, add_heading, move and remove. Read a block
with peek before writing about it.

Mutating tools only return a receipt (block id, block count, revision). Call compile to read the whole report back
(it also checks it, lists the locked blocks and sets a checkpoint) and diff to see what changed: since the last change, or since the last compile.

Blocks marked locked (by the report's template) can't be edited, moved or removed; add text around them.

Never write Markdown headings, code or markers; give plain text only. Numbers in captions and paragraphs must be
quoted as peek shows them, not computed: a number that is not in the data of the blocks you cite is rejected
(ungrounded) and nothing is written, so pass the ids of the blocks in `cites`; compile reports the tolerance in force.
The report file is saved after every change. Use render to produce HTML and PowerPoint.
"""


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


def serve_report(md_path, sources, out_dir=None, policy="grounded", rel_tol=1e-3, small_int_max=10, year_range=(1900, 2100), title=None, lock=(), unlock=(), call_log=None, stdin=None, stdout=None):
    """Load (or start) the report at ``md_path`` against the catalog of ``sources`` and serve its tools on stdio."""
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
                           small_int_max=small_int_max, year_range=year_range, out_dir=out_dir, on_change=lambda d: _save(d, md_path))
    MCPServer(tools, name="mcutils-report", instructions=REPORT_INSTRUCTIONS,
              call_log=call_log).serve(stdin, stdout)
    return doc
