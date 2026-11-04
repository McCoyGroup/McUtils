"""
Marked documentation examples in interactive (notebook) documentation.

`LiveExamplePage` runs the marked blocks of one examples text on demand, in a namespace that persists between
runs, and turns what they produce into the same `Readout` the documentation build stores
(through `ExampleView`). `McUtils.Docs.jdoc` uses it to put a **Run** button under each marked block.
Nothing here runs during a documentation build.
"""

import json
import os

from .Examples import ExampleParser, ExampleMarkerError, ExampleView, ExampleRunner, ReadoutStore

__all__ = ["LiveExamplePage", "LiveExampleResult", "split_examples"]


def split_examples(text, owner=None):
    """
    Splits examples Markdown into the pieces an interactive view renders separately.

    :return: ``[("text", markdown)]`` and ``[("code", block)]`` pieces in page order, where the markdown of a
        code piece is ``block.fence``; ``None`` if ``text`` has no (valid) markers, so the caller can render it
        as plain Markdown exactly as before
    """
    if not ExampleParser.has_markers(text):
        return None
    try:
        parsed = ExampleParser.parse(text, owner=owner)
    except ExampleMarkerError:
        return None
    pieces = []
    for seg in parsed.segments:
        if isinstance(seg, str):
            if seg.strip():
                pieces.append(("text", seg))
        else:
            pieces.append(("code", seg))
    return pieces if any(kind == "code" for kind, _ in pieces) else None


class Fragment(str):
    """Marks a string as ready-made HTML rather than text to be escaped."""


class LiveExampleResult:
    """
    What running a block gave: ``status`` is ``"ok"``, ``"empty"`` (``display="none"``, or nothing to show) or
    ``"error"``; ``view`` is the `ExampleView` (``ok`` only); ``error`` the traceback text (``error`` only).
    """

    def __init__(self, block, status, view=None, error=None, duration=None):
        self.block = block
        self.status = status
        self.view = view
        self.error = error
        self.duration = duration

    @property
    def ok(self):
        return self.status == "ok"

    def fragment(self, style=None, css="inline"):
        """The output as an embeddable `FragmentResult` (the same thing the build stores), or ``None``."""
        if self.view is None:
            return None
        return self.view.to_fragment(style=style, css=css)

    def element(self, mode="widget", style=None, css="inline", **opts):
        """The output as a JHTML element (no code), or ``None``."""
        if self.view is None:
            return None
        return self.view.to_element(mode, style=style, css=css, include_code=False, **opts)

    def __repr__(self):
        return "{}({!r}, {})".format(type(self).__name__, self.block.id, self.status)


class LiveExamplePage:
    """
    Runs the marked blocks of one examples text interactively.

    Blocks share a namespace in order (the chain used for their stored keys): running a block first runs, once,
    the earlier blocks of its chain that haven't run yet; running a block again re-runs only that block.
    Each block is seeded from its key like the build does, so a seeded example gives the output stored for it.

    :param text: Markdown with marked examples
    :param owner: the documented object's name (used for default ids)
    :param store: a `ReadoutStore` (or its directory) holding the output the documentation build stored, for
        showing it before a block is run
    :param namespace: ``None`` (default) for a private namespace per chain of blocks, a dict to run every block in
        (e.g. the notebook's namespace), or ``"user"`` for IPython's ``user_ns``
    :param timeout: per-block time limit in seconds (a marker's ``timeout`` overrides it)
    :param imports: start each chain with the owner's public names (see `ExampleRunner`); ignored if ``runner`` is given
    :param runner: an `ExampleRunner` to execute with; defaults to one with the given ``timeout``
    """

    def __init__(self, text, owner=None, store=None, namespace=None, timeout=60, runner=None, to_readout=None,
                 imports=True):
        self.owner = owner
        self.parsed = ExampleParser.parse(text, owner=owner)
        if isinstance(store, (str, os.PathLike)):
            store = ReadoutStore(store)
        self.store = store
        self.runner = runner or ExampleRunner(store, timeout=timeout, to_readout=to_readout, imports=imports)
        self.namespace = namespace
        self._namespaces = {}
        self._ran = set()
        self.results = {}

    @property
    def blocks(self):
        return self.parsed.blocks

    def block(self, block):
        """Resolves a block given as an `ExampleBlock`, an id, or an index."""
        blocks = self.blocks
        if isinstance(block, int):
            return blocks[block]
        if isinstance(block, str):
            for b in blocks:
                if b.id == block:
                    return b
            raise KeyError("no example with id {!r}".format(block))
        # a block from another parse of the same text (`split_examples` parses separately from the page that runs
        # it) is the same example: match it by key, which chains in everything before it
        for b in blocks:
            if b is block:
                return b
        for b in blocks:
            if b.key == block.key and b.id == block.id:
                return b
        raise KeyError("example {!r} is not on this page".format(getattr(block, "id", block)))

    # ---- stored output ---- #
    def stored_fragment(self, block):
        """The HTML the documentation build stored for ``block``, or ``None`` (not stored, failed, or no store)."""
        if self.store is None:
            return None
        block = self.block(block)
        meta = self.store.read_meta(block.key)
        if meta is None or meta.get("status") != "ok" or not self.store.has_file(block.key, "fragment.html"):
            return None
        return self.store.read_file(block.key, "fragment.html")

    def stored_output(self, block):
        """The `FragmentResult` the build stored for ``block`` (with what it needs to run), or ``None``."""
        html = self.stored_fragment(block)
        if html is None:
            return None
        from ..Readouts.Renderers.HTML import FragmentResult
        info = self.store.read_meta(self.block(block).key).get("fragment") or {}
        return FragmentResult(html, info.get("needs", ()), info.get("runtime"), info.get("head", ()))

    # ---- running ---- #
    def _namespace_for(self, block):
        ns = self.namespace
        if ns == "user":
            from IPython import get_ipython
            shell = get_ipython()
            if shell is None:
                raise RuntimeError("namespace='user' needs a running IPython session")
            return shell.user_ns
        if ns is not None:
            return ns
        start = self.parsed.chain(block)[0].index
        if start not in self._namespaces:
            self._namespaces[start] = self.runner.new_namespace(self.owner)
        return self._namespaces[start]

    def _execute(self, block, namespace):
        outcome = self.runner.execute(block, namespace)
        self._ran.add(block.id)
        return ExampleView(block, outcome["value"], outcome["stdout"], self.runner.to_readout,
                           self.runner.max_output), outcome["duration"]

    def run(self, block):
        """
        Runs ``block`` (after any earlier blocks of its chain that haven't run) and returns its `ExampleView`.

        :raises: whatever the example raises
        """
        block = self.block(block)
        namespace = self._namespace_for(block)
        for earlier in self.parsed.chain(block)[:-1]:
            if earlier.id not in self._ran:
                self._execute(earlier, namespace)
        view, _ = self._execute(block, namespace)
        return view

    def try_run(self, block):
        """Like `run`, but returns a `LiveExampleResult` instead of raising (a failure is ``status="error"``)."""
        block = self.block(block)
        try:
            view = self.run(block)
        except (Exception, SystemExit) as e:
            result = LiveExampleResult(block, "error", error=self.runner.format_error(e))
        else:
            if view.display == "none":
                result = LiveExampleResult(block, "empty", view)
            else:
                try:
                    node = view.node()
                except (Exception, SystemExit) as e:   # e.g. display="readout" with no value
                    result = LiveExampleResult(block, "error", error=self.runner.format_error(e))
                else:   # no node: nothing worth showing (a trivial readout is suppressed unless show_trivial)
                    result = LiveExampleResult(block, "empty" if node is None else "ok", view)
        self.results[block.id] = result
        return result

    def reset(self):
        """Forgets every namespace and run, so the next run starts the page again."""
        self._namespaces.clear()
        self._ran.clear()
        self.results.clear()

    # ---- notebook controls ---- #
    def control(self, block, show_stored=True, label="Run"):
        """
        A **Run** button with an output area under it, built from `JHTML` elements: the click is a JHTML
        ``event_handlers`` entry and the output is written into a ``JHTML.Div`` through its content setters, so
        the interaction goes through the ``ActiveHTMLWidget`` layer and never touches ``ipywidgets`` directly.
        The first display also checks that the ``ActiveHTMLWidget`` extension is installed (see
        `HTMLWidgets.check_extension`) and says how to install it if not.

        The button runs the block (and whatever it needs). With ``show_stored``, a block whose output the
        documentation build stored shows that output and gets no button; a block without stored output gets the button.

        :param block: the block, id or index
        :param show_stored: show the stored output before the first run
        :param label: the button text
        :return: a ``JHTML.Div`` holding the button and the output area
        """
        from ..Jupyter import JHTML
        from ..Jupyter.Apps.Themes import AppHTML
        block = self.block(block)
        self.show_runtime()
        out = JHTML.Div(cls="mcr-live-output", dynamic=True, style={"margin-top": ".6em", "min-width": "0"})

        def show(display):
            self.place(out, display)

        if show_stored:
            stored = self.stored_output(block)
            if stored is not None:
                # the documentation build already has this output, so there is nothing to run
                show(stored)
                return JHTML.Div(out, cls="mcr-live-example", style={"margin": ".4em 0 1.2em 0"})

        def run(*_):
            result = self.try_run(block)
            self.show_result(result, show)
            if result.status != "error":
                # the output stays, the button goes; after a failure it stays so the example can be retried
                button.set_attribute("display", "none")

        # the Apps element factory: the button takes the look of whichever Apps theme is active (native `mcui-button`,
        # or Bootstrap's `btn`), like the Opener and the rest of the documentation view, instead of the browser default
        button = AppHTML.Bootstrap.Button(label, event_handlers={"click": run}, cls="mcr-run btn-sm", variant="primary")
        return JHTML.Div(button, out, cls="mcr-live-example", style={"margin": ".4em 0 1.2em 0"})

    _runtime_shown = False

    def show_runtime(self):
        """
        Shows, once per page object, the script (`X3DOM_WATCHER_JS`) that loads the X3DOM runtime when a 3D scene
        appears. The ActiveHTMLWidget frontend sets ``innerHTML`` without running scripts, and a readout fragment is
        markup only, so something on the page has to load the runtime; the display API runs scripts when it is
        shown in a trusted notebook. It is shown where ``jdoc`` is called (a callback's display output goes
        elsewhere), and it does nothing a second time.
        """
        if self._runtime_shown:
            return
        self._runtime_shown = True
        from ..Jupyter.JHTML.WidgetTools import JupyterAPIs
        from ..Readouts.Renderers.HTML import HTMLReadoutRenderer
        from .ExampleEmbed import X3DOM_WATCHER_JS
        try:
            runtime = HTMLReadoutRenderer(x3dom_path=getattr(self.runner, "x3dom_path", None)).runtime_info()
        except ValueError:      # 'local'/'inline' only make sense in standalone documents
            runtime = HTMLReadoutRenderer().runtime_info()
        script = X3DOM_WATCHER_JS.replace("__RUNTIME__", json.dumps(runtime))
        display = JupyterAPIs.get_display_api()
        if display is not None:
            display.display(display.HTML("<script>" + script + "</script>"))

    @staticmethod
    def place(target, display):
        """
        Replaces the content of a JHTML element: `Fragment` and plain JHTML elements are written into its
        ``html_string``, strings are shown as escaped text, and live JHTML widgets become its child. A readout
        `FragmentResult` is written the same way; if it holds a 3D scene, the page's X3DOM watcher (see
        `show_runtime`) loads the runtime and starts it.
        """
        from ..Readouts.Renderers.HTML import FragmentResult
        from ..Jupyter import JHTML
        from ..Jupyter.JHTML.HTML import HTML as _HTML
        from ..Jupyter.JHTML.HTMLWidgets import ActiveHTMLWrapper
        if isinstance(display, FragmentResult):
            target.html_string = display.html
        elif isinstance(display, ActiveHTMLWrapper):
            target.html_string = ""
            target.children = [target.canonicalize_widget(display)]
        else:
            if isinstance(display, Fragment):
                markup = str(display)
            elif isinstance(display, str):
                markup = JHTML.Pre(display).tostring()
            elif isinstance(display, _HTML.XMLElement):
                markup = display.tostring()
            else:
                raise TypeError("don't know how to place {}".format(type(display).__name__))
            target.html_string = markup

    def show_result(self, result, show):
        """Calls ``show(display)`` with what a `LiveExampleResult` should look like in a JHTML output area."""
        if result.status == "error":
            show("Example `{}` failed:\n{}".format(result.block.id, result.error))
        elif result.status == "empty":
            show("Ran `{}` (nothing to display).".format(result.block.id))
        else:
            fragment = result.fragment()
            show(fragment if fragment is not None else "Ran `{}` (nothing to display).".format(result.block.id))
