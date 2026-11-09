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

    def __init__(self, message, result=None, code="render_failed"):
        super().__init__(message)
        self.result = result
        self.code, self.detail = code, message      # so a tool call reports it as an error with this code

    def to_dict(self):
        d = {"code": self.code, "detail": self.detail}
        if self.result is not None and (self.result.paths or self.result.failed):
            d["written"] = dict(self.result.paths)      # formats that were still written (see `render`)
            d["failed"] = dict(self.result.failed)
        return d


class RenderResult:
    """
    :ivar paths: ``{"md": ..., "html": ..., "pptx": ...}`` for what was written
    :ivar statuses: readout block id -> ``"ok"``, ``"error"`` or ``"missing"``
    :ivar problems: human-readable strings, one per failed or missing block (or failed format)
    :ivar executed: ids of the readout blocks whose code actually ran this time (cached ones don't)
    :ivar failed: format -> error code, for each requested format that was not written (``render`` only)
    """

    def __init__(self):
        self.paths = {}
        self.statuses = {}
        self.problems = []
        self.executed = []
        self.failed = {}

    @property
    def ok(self):
        return not self.problems

    def merge(self, other):
        self.paths.update(other.paths)
        self.statuses.update(other.statuses)
        self.problems.extend(p for p in other.problems if p not in self.problems)
        self.executed.extend(other.executed)
        self.failed.update(other.failed)
        return self

    def __repr__(self):
        return f"RenderResult(ok={self.ok}, paths={self.paths}, problems={len(self.problems)})"


def report_style(style=None):
    """
    ``style`` with the token ``stub_hidden`` on: a report writes a one-line "data only" stub for a section that holds only
    export-only arrays instead of leaving it out. A theme name, a token dict, a `ReadoutTheme` or ``None`` is accepted; a
    token dict that sets ``stub_hidden`` itself is kept as it is.
    """
    from ..Styles import ReadoutTheme
    if isinstance(style, ReadoutTheme):
        return style if style.get("stub_hidden") is not None else style.updated(stub_hidden=True)
    if style is None or isinstance(style, str):
        return {"preset": style or os.environ.get("MCUTILS_READOUT_THEME", "default"), "stub_hidden": True}
    out = dict(style)
    out.setdefault("stub_hidden", True)
    return out


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
    :param strict: raise `ReportRenderError` if any readout block failed (the HTML page is not written then);
        otherwise the page is written with an error note in place of the failed block and ``RenderResult.ok`` is
        false. `render` tries every requested format either way and only raises after the others were written
    :param finx_assets: where the HTML page's finx styles come from (see `McUtils.Docs.static_markdown`); default
        the copy vendored with McUtils, so rendering needs no network
    """

    def __init__(self, catalog, store=None, style=None, css="inline", timeout=120, strict=True, finx_assets=None):
        self.catalog = catalog
        self.store = store
        self.style = report_style(style)
        self.css = css
        self.timeout = timeout
        self.strict = strict
        self.finx_assets = finx_assets

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
        static_markdown(md, title=doc.title, out_file=out_file, readouts=store, strict_readouts=False, owner=slug,
                        finx_assets=self.finx_assets)
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
        """
        Writes ``report.md`` / ``report.html`` / ``report.pptx`` into ``out_dir``.

        Each format is attempted independently: a format that fails (a failed readout block, a missing package, a
        file or network error) is recorded in ``RenderResult.problems`` and ``RenderResult.failed`` and the others
        are still written. Under ``strict`` a `ReportRenderError` (carrying that result, and the code of the first
        failure) is raised after all requested formats were attempted.
        """
        os.makedirs(out_dir, exist_ok=True)
        result = RenderResult()
        unknown = [f for f in formats if f not in ("md", "html", "pptx")]
        if unknown:
            raise ValueError(f"unknown report format(s) {unknown}; choose from md, html, pptx")
        steps = {
            "md": lambda: self._write_markdown(doc, os.path.join(out_dir, "report.md")),
            "html": lambda: self.render_html(doc, os.path.join(out_dir, "report.html"), refresh=refresh),
            "pptx": lambda: self.render_pptx(doc, os.path.join(out_dir, "report.pptx"), rasterizer=rasterizer),
        }
        for fmt in ("md", "html", "pptx"):
            if fmt not in formats:
                continue
            try:
                part = steps[fmt]()
            except ReportRenderError as e:   # strict: failed readout blocks (HTML not written) or a failed deck
                part = e.result if e.result is not None else RenderResult()
                if not part.problems:
                    part.problems.append(str(e))
                part.failed[fmt] = e.code
            except ImportError as e:      # a missing optional package (the HTML writer needs `markdown`)
                name = getattr(e, "name", None) or str(e)
                part = self._failure(fmt, "missing_dependency",
                                     f"{fmt}: the Python package {name!r} is not installed, so the {fmt.upper()} "
                                     f"report was not written (pip install {name}); the other formats are unaffected")
            except Exception as e:  # noqa: BLE001 - one format failing must not stop the others
                part = self._failure(fmt, getattr(e, "code", None) or "render_failed",
                                     f"{fmt}: {type(e).__name__}: {e}")
            if fmt not in part.paths and fmt not in part.failed:     # e.g. HTML skipped because a readout failed
                part.failed[fmt] = "render_failed"
            result.merge(part)
        if self.strict and result.problems:
            code = next(iter(result.failed.values()), "render_failed")
            raise ReportRenderError("; ".join(result.problems), result, code=code)
        return result

    def _write_markdown(self, doc, path):
        result = RenderResult()
        with open(path, "w", encoding="utf-8") as f:
            f.write(doc.to_markdown())
        result.paths["md"] = path
        return result

    @staticmethod
    def _failure(fmt, code, message):
        result = RenderResult()
        result.problems.append(message)
        result.failed[fmt] = code
        return result
