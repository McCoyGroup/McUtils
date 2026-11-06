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
the source's report template. If the requested source is not listed, tell the user which sources are available and
stop: do not substitute another source, add a heading implying it exists, or write about it from memory. If the
template has an outline, apply_template builds it in one call (optionally with some of the template's optional
sections); then adjust with add_readout, add_heading, add_text, move, move_section and remove.

Two kinds of names: a source handle (hoh) and section name (frequencies) are for describe_source, peek, add_readout and
apply_template; a block id (h1, r2, p1) comes from outline or compile and is for after, under, cites, move, edit_text,
set_caption and remove. peek reads a source's section, never a block or a paragraph. `after` is one block id; to add
under a heading use `under` with the heading id. Moving a heading does not move what is under it; move_section does.

Mutating tools only return a receipt (block id, block count, revision). Call compile to read the whole report back
(it only reads: it checks the report, lists the locked blocks and counts the text by status). To see what you
changed, call diff: since='last_change' is the most recent request; since='template' is everything since
apply_template; since='start' is everything since the report was opened; checkpoint(label) records your own baseline
to give to diff(since=...) later. Say which baseline a summary of changes is relative to.

Blocks marked locked (by the report's template) can't be edited, captioned, moved or removed. If asked to change one,
report that limit to the user and stop; do not recreate its content or add text next to it to simulate the edit, and
add supplementary text around it only if the user separately asks for that.

Never write Markdown headings, code or markers; give plain text only. Numbers in captions and paragraphs must be
quoted as peek shows them, not computed: a number that is not in the data of the blocks you cite is rejected
(ungrounded) and nothing is written, and text under the grounded policy must cite blocks (`cites`). Statuses: checked
means a number in the text was verified against the cited data; no_numbers means the text had nothing to verify, so
nothing about its claims was checked. The checker verifies numbers only, not scientific interpretation: do not state
classifications or assignments (such as which mode is a stretch) that the source does not provide. compile reports
the tolerance in force.

The report file is saved after every change. A successful compile is enough to finish a report-writing request
(compile(full_text=True) reads the saved prose). Use render only when the user asks for exported files; when it
succeeds, report the paths and finish rather than rendering or inspecting the same output again.
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
