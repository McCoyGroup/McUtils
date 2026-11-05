"""
Rendering a `ReportDocument`: Markdown, a single-file HTML page and a PowerPoint deck.

HTML goes through the docs pipeline: the document's Markdown has one marked example per readout block
(``report_source("handle", digest=...)``), an `McUtils.Docs.ExampleRunner` runs them against the catalog and stores
each fragment, and `McUtils.Docs.static_markdown` writes the stored fragments into one page. Blocks are cached by
content, so rendering an unchanged document runs nothing and a changed source (a new digest) re-runs only its blocks.
PowerPoint is built from the equivalent `Readout` tree.
"""

import os
import re

__all__ = ["ReportRenderError", "RenderResult", "ReportRenderer"]


class ReportRenderError(RuntimeError):
    """A strict render found readout blocks that failed or were missing."""

    def __init__(self, message, result=None):
        super().__init__(message)
        self.result = result


class RenderResult:
    """
    :ivar paths: ``{"md": ..., "html": ..., "pptx": ...}`` for what was written
    :ivar statuses: readout block id -> ``"ok"``, ``"error"`` or ``"missing"``
    :ivar problems: human-readable strings, one per failed or missing block (or failed format)
    :ivar executed: ids of the readout blocks whose code actually ran this time (cached ones don't)
    """

    def __init__(self):
        self.paths = {}
        self.statuses = {}
        self.problems = []
        self.executed = []

    @property
    def ok(self):
        return not self.problems

    def merge(self, other):
        self.paths.update(other.paths)
        self.statuses.update(other.statuses)
        self.problems.extend(other.problems)
        self.executed.extend(other.executed)
        return self

    def __repr__(self):
        return f"RenderResult(ok={self.ok}, paths={self.paths}, problems={len(self.problems)})"


def _slug(text):
    return re.sub(r"[^0-9a-zA-Z]+", "-", str(text)).strip("-").lower() or "report"


class ReportRenderer:
    """
    :param catalog: the `SourceCatalog` the document's readouts come from
    :param store: where HTML fragments are cached: ``None`` (``readouts/`` beside the output), a directory, or a
        `McUtils.Docs.ReadoutStore`
    :param style: the readout style/theme preset for HTML and PowerPoint
    :param css: ``"inline"`` or ``"stylesheet"`` (see `ExampleRunner`)
    :param timeout: per-readout time limit in seconds
    :param strict: raise `ReportRenderError` if any readout block failed (nothing is written then); otherwise the
        page is written with an error note in place of the failed block and ``RenderResult.ok`` is false
    """

    def __init__(self, catalog, store=None, style=None, css="inline", timeout=120, strict=True):
        self.catalog = catalog
        self.store = store
        self.style = style
        self.css = css
        self.timeout = timeout
        self.strict = strict

    def _resolve_store(self, out_file):
        from ...Docs.Examples import ReadoutStore
        if isinstance(self.store, ReadoutStore):
            return self.store
        root = self.store if self.store is not None else os.path.join(os.path.dirname(os.path.abspath(out_file)),
                                                                      "readouts")
        return ReadoutStore(root)

    def render_html(self, doc, out_file, refresh=False):
        from ...Docs.Examples import ExampleRunner, ExampleParser
        from ...Docs.HTMLDocs import static_markdown
        result = RenderResult()
        store = self._resolve_store(out_file)
        slug = _slug(doc.title)
        md = doc.to_markdown()
        runner = ExampleRunner(store, namespace=self.catalog.namespace(), imports=False, css=self.css,
                               style=self.style, timeout=self.timeout)
        ran = runner.run_text(md, owner=slug, refresh=refresh)
        result.executed = [r.block.id for r in ran if getattr(r, "status", None) in ("ok", "error")]
        for block in ExampleParser.parse(md, owner=slug).blocks:
            meta = store.read_meta(block.key)
            if meta is None:
                result.statuses[block.id] = "missing"
                result.problems.append(f"readout {block.id}: no stored output")
            elif meta.get("status") == "error":
                err = meta.get("error") or {}
                result.statuses[block.id] = "error"
                result.problems.append(f"readout {block.id} failed: {err.get('type', 'error')}: {err.get('message', '')}")
            else:
                result.statuses[block.id] = "ok"
        if self.strict and result.problems:
            raise ReportRenderError("the report has readout blocks that failed: " + "; ".join(result.problems), result)
        os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)
        static_markdown(md, title=doc.title, out_file=out_file, readouts=store, strict_readouts=False, owner=slug)
        result.paths["html"] = out_file
        return result

    def render_pptx(self, doc, out_file, rasterizer=None):
        result = RenderResult()
        try:
            readout = doc.to_readout()
            os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)
            readout.to_pptx(out_file, style=self.style, rasterizer=rasterizer)
        except Exception as e:  # noqa: BLE001 - reported, or raised when strict
            msg = f"pptx: {type(e).__name__}: {e}"
            if self.strict:
                raise ReportRenderError(msg, result) from e
            result.problems.append(msg)
            return result
        result.paths["pptx"] = out_file
        return result

    def render(self, doc, out_dir, formats=("md", "html", "pptx"), refresh=False, rasterizer=None):
        """Writes ``report.md`` / ``report.html`` / ``report.pptx`` into ``out_dir``."""
        os.makedirs(out_dir, exist_ok=True)
        result = RenderResult()
        if "md" in formats:
            path = os.path.join(out_dir, "report.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(doc.to_markdown())
            result.paths["md"] = path
        if "html" in formats:
            result.merge(self.render_html(doc, os.path.join(out_dir, "report.html"), refresh=refresh))
        if "pptx" in formats:
            result.merge(self.render_pptx(doc, os.path.join(out_dir, "report.pptx"), rasterizer=rasterizer))
        return result
