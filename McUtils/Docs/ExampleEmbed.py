"""
Puts generated example output into documentation pages **without running anything**.

`ExampleEmbedder` is the ``examples_processor`` of a `DocWalker`: it receives the final, merged
``examples`` Markdown of one documented object, removes each ``<!-- readout(...) -->`` marker, keeps the
code fence, and adds a placeholder ``<div>`` that a small inline loader fills with the stored fragment
when it scrolls into view (or its collapsed section opens). `ExampleCollector` has the same interface but
only records the pages, which is how ``ci/build_readouts.py`` finds exactly the examples the docs build
will embed.
"""

import html, os, re, shutil

from .Examples import ExampleCache, ExampleParser, ReadoutStore

__all__ = [
    "ExampleEmbedError",
    "ExampleEmbedder",
    "ExampleCollector",
    "publish_readouts"
]


class ExampleEmbedError(Exception):
    """Marked examples had no usable stored output and the embedder was ``strict``."""


# (Deliberately not in ``__all__``: the doc walker treats exported strings as importable names.)
# The loader must not contain Liquid delimiters (double braces or brace-percent), since pages go through Jekyll.
EXAMPLE_LOADER_JS = """
(function(){
if(window.mcrReadouts){return;}
var once={};
function memo(key,make){if(!once[key]){once[key]=make();}return once[key];}
function loadScript(src){return memo("s:"+src,function(){return new Promise(function(ok,no){var s=document.createElement("script");s.src=src;s.onload=ok;s.onerror=no;document.head.appendChild(s);});});}
function loadCss(href){memo("c:"+href,function(){var l=document.createElement("link");l.rel="stylesheet";l.href=href;document.head.appendChild(l);return true;});}
function mount(el){
if(el.getAttribute("data-state")){return;}
el.setAttribute("data-state","loading");
fetch(el.getAttribute("data-src")).then(function(r){if(!r.ok){throw new Error("HTTP "+r.status);}return r.text();}).then(function(markup){
var css=el.getAttribute("data-css-href");if(css){loadCss(css);}
var show=function(){el.innerHTML=markup;el.setAttribute("data-state","ready");if(window.x3dom&&window.x3dom.reload){window.x3dom.reload();}};
if((el.getAttribute("data-needs")||"").indexOf("x3dom")>=0){
var x3css=el.getAttribute("data-x3dom-css");if(x3css){loadCss(x3css);}
loadScript(el.getAttribute("data-x3dom-script")).then(show,show);
}else{show();}
}).catch(function(){el.setAttribute("data-state","failed");el.className+=" mcr-failed";});
}
var io=("IntersectionObserver" in window)?new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);mount(e.target);}});},{rootMargin:"200px"}):null;
function watch(el){
if(el.getAttribute("data-state")||el.__mcrWatched){return;}
el.__mcrWatched=true;
if(io&&el.getAttribute("data-lazy")!=="false"){io.observe(el);}else{mount(el);}
}
function scan(){var found=document.querySelectorAll(".mcr-example[data-src]");for(var i=0;i<found.length;i++){watch(found[i]);}}
window.mcrReadouts={scan:scan,mount:mount};
if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",scan);}else{scan();}
window.addEventListener("load",scan);
if("MutationObserver" in window){var pending=false;new MutationObserver(function(){if(!pending){pending=true;setTimeout(function(){pending=false;scan();},50);}}).observe(document.documentElement,{childList:true,subtree:true});}
})();
""".strip()


# Opt-in (``debug=True``): a corner badge and console log reporting how many readouts on the page have loaded.
EXAMPLE_DEBUG_JS = """
(function(){
if(window.mcrDebug){return;}
window.mcrDebug=true;
var badge=document.createElement("div");
badge.style.cssText="position:fixed;right:8px;bottom:8px;z-index:99999;background:#222;color:#fff;font:12px/1.4 monospace;padding:4px 8px;border-radius:4px;opacity:.85";
function count(){
var all=document.querySelectorAll(".mcr-example"),c={ready:0,loading:0,failed:0,waiting:0,missing:0,error:0};
for(var i=0;i<all.length;i++){var e=all[i],s=e.getAttribute("data-state");
if(e.className.indexOf("mcr-missing")>=0){c.missing++;}else if(e.className.indexOf("mcr-error")>=0){c.error++;}
else if(s==="ready"){c.ready++;}else if(s==="loading"){c.loading++;}else if(s==="failed"){c.failed++;}else{c.waiting++;}}
return [all.length,c];
}
var last="";
function update(){
var r=count(),text="readouts: "+r[1].ready+"/"+r[0]+" loaded";
for(var k in r[1]){if(k!=="ready"&&r[1][k]){text+=", "+r[1][k]+" "+k;}}
badge.textContent=text;
if(text!==last){last=text;console.info("[mcr] "+text);}
}
function start(){document.body.appendChild(badge);update();setInterval(update,300);}
if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",start);}else{start();}
})();
""".strip()


def _attr(value):
    return html.escape(str(value), quote=True)


class ExampleEmbedder:
    """
    Callable ``examples_processor``: ``embedder(markdown, handler_or_owner) -> markdown``.

    :param store: the `ReadoutStore` (or its root directory)
    :param url_template: where a published fragment lives. ``{key}`` and ``{key2}`` (its first two
        characters) are replaced. The default goes through Jekyll's ``relative_url`` filter, which honours the
        site's ``baseurl``; use e.g. ``"/readouts/{key2}/{key}/fragment.html"`` for a plain absolute path.
    :param stylesheet_url_template: the same for the shared ``mcr.css`` (used for ``css="stylesheet"`` entries)
    :param lazy: fetch fragments when they become visible (default) rather than on page load
    :param strict: make `finish` raise if any marked block had no stored output or a failed one
    :param warn: callable for warnings (default ``print``)
    :param debug: also add a small script that shows a corner badge (and logs to the console) with how many
        readouts on the page have loaded, for checking a built site by eye
    """

    default_url_template = "{{ '/readouts/{key2}/{key}/fragment.html' | relative_url }}"
    default_stylesheet_url_template = "{{ '/readouts/mcr.css' | relative_url }}"

    def __init__(self, store, url_template=None, stylesheet_url_template=None, lazy=True, strict=False, warn=print,
                 loader=True, debug=False):
        self.store = store if isinstance(store, ReadoutStore) else ReadoutStore(store)
        self.cache = ExampleCache(self.store)
        self.url_template = url_template or self.default_url_template
        self.stylesheet_url_template = stylesheet_url_template or self.default_stylesheet_url_template
        self.lazy = lazy
        self.strict = strict
        self.warn = warn
        self.loader = loader
        self.debug = debug
        self.problems = []   # [(owner, id, kind, detail)]
        self.embedded = []   # [(owner, id, key)]

    # ---- the processor interface ---- #
    def __call__(self, text, handler=None, owner=None):
        if owner is None and handler is not None:
            owner = getattr(handler, "identifier", None)
        if "readout" not in text:
            return text
        parsed = ExampleParser.parse(text, owner=owner)
        blocks = parsed.blocks
        if not blocks:
            return text
        state = {"first": True}

        def replace(block):
            fence = block.raw[len(block.marker):].lstrip("\r\n")
            if not fence.endswith("\n"):
                fence += "\n"
            extra = self.placeholder(block, owner)
            if extra is None:
                return fence
            out = fence + "\n" + extra + "\n"
            if self.loader and state["first"]:
                out += "\n<script>\n" + EXAMPLE_LOADER_JS + "\n</script>\n"
                if self.debug:
                    out += "\n<script>\n" + EXAMPLE_DEBUG_JS + "\n</script>\n"
                state["first"] = False
            return out

        return parsed.render(replace)

    # ---- placeholders ---- #
    def url(self, key):
        return self.url_template.replace("{key2}", key[:2]).replace("{key}", key)

    def _problem(self, owner, block, kind, detail):
        self.problems.append((owner, block.id, kind, detail))
        if self.warn is not None:
            self.warn("readout {} for example `{}`{}: {}".format(
                kind, block.id, "" if owner is None else " ({})".format(owner), detail))

    def placeholder(self, block, owner=None):
        """The markup that follows a block's code fence, or ``None`` for ``display="none"``."""
        if block.options.get("display", "readout") == "none":
            return None
        meta = self.store.read_meta(block.key)
        if meta is None:
            self._problem(owner, block, "missing", "no stored output; run ci/build_readouts.py")
            return ('<div class="mcr-example mcr-missing" data-readout="{}" data-key="{}">'
                    "Readout not generated yet.</div>").format(_attr(block.id), block.key)
        if meta.get("status") == "error":
            err = meta.get("error") or {}
            self._problem(owner, block, "failed", "{}: {}".format(err.get("type", "error"), err.get("message", "")))
            return ('<div class="mcr-example mcr-error" data-readout="{}" data-key="{}">'
                    "This example failed when its output was generated: {}: {}</div>").format(
                _attr(block.id), block.key, _attr(err.get("type", "error")), _attr(err.get("message", "")))
        if not self.store.has_file(block.key, "fragment.html"):
            self._problem(owner, block, "missing", "the entry has no fragment")
            return None
        fragment = meta.get("fragment") or {}
        url = self.url(block.key)
        attrs = ['class="mcr-example"', 'data-readout="{}"'.format(_attr(block.id)), 'data-key="{}"'.format(block.key),
                 'data-src="{}"'.format(url)]
        if fragment.get("css") == "stylesheet":
            attrs.append('data-css-href="{}"'.format(self.stylesheet_url_template))
        needs = fragment.get("needs") or []
        if needs:
            attrs.append('data-needs="{}"'.format(_attr(" ".join(needs))))
            x3 = (fragment.get("runtime") or {}).get("x3dom") or {}
            if x3.get("script"):
                attrs.append('data-x3dom-script="{}"'.format(_attr(x3["script"])))
            if x3.get("stylesheet"):
                attrs.append('data-x3dom-css="{}"'.format(_attr(x3["stylesheet"])))
        if not self.lazy:
            attrs.append('data-lazy="false"')
        self.embedded.append((owner, block.id, block.key))
        return "<div {}><a href=\"{}\">Open readout</a></div>".format(" ".join(attrs), url)

    def finish(self):
        """Raises `ExampleEmbedError` listing every problem if ``strict``; otherwise returns the problems."""
        if self.strict and self.problems:
            raise ExampleEmbedError("{} example(s) have no usable output:\n{}".format(
                len(self.problems), "\n".join("  {} / {}: {} ({})".format(*p) for p in self.problems)))
        return list(self.problems)


class ExampleCollector:
    """
    The same interface as `ExampleEmbedder`, but only records the pages that have marked examples and
    returns the text unchanged. ``pages`` maps an owner to the text seen for it.
    """

    def __init__(self):
        self.pages = {}
        self.ids = {}

    def __call__(self, text, handler=None, owner=None):
        if owner is None and handler is not None:
            owner = getattr(handler, "identifier", None)
        if "readout" not in text:
            return text
        parsed = ExampleParser.parse(text, owner=owner)
        if parsed.blocks:
            self.pages[owner] = text
            for b in parsed.blocks:
                other = self.ids.setdefault(b.id, owner)
                if other != owner:
                    raise ValueError("example id `{}` is used by both `{}` and `{}`; ids must be unique across "
                                     "pages because the manifest is keyed by id".format(b.id, other, owner))
        return text

    def parsed_pages(self):
        return [(owner, ExampleParser.parse(text, owner=owner)) for owner, text in self.pages.items()]


def publish_readouts(store, target, stylesheet=True):
    """
    Copies a store into a site directory as ``<target>/readouts`` (when it isn't already there).
    Returns the destination.
    """
    store = store if isinstance(store, ReadoutStore) else ReadoutStore(store)
    dest = os.path.join(target, "readouts")
    if os.path.abspath(dest) == os.path.abspath(store.root) or not os.path.isdir(store.root):
        return dest
    os.makedirs(dest, exist_ok=True)
    for name in os.listdir(store.root):
        src = os.path.join(store.root, name)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(dest, name), dirs_exist_ok=True)
        elif name == ReadoutStore.stylesheet_name and stylesheet:
            shutil.copy2(src, os.path.join(dest, name))
    return dest
