"""
Syntax highlighting for code shown through JHTML, done in the browser by a CDN-loaded highlighter (highlight.js).

Widget bodies are written with ``innerHTML``, so a script placed in them never runs; `CodeHighlighter` instead shows
one small loader once (through the display API, which does run scripts in a trusted notebook). The loader fetches the
highlighter and its stylesheet from the CDN and then watches the page: any ``<pre><code class="language-...">`` that
appears, whether it came from a Markdown fence, from `HighlightedCode`, or was added later by a click handler, is
highlighted once. Static pages get the same thing from ``<link>``/``<script>`` elements (`head_elements`).
"""
import json

__all__ = ["CodeHighlighter"]


class CodeHighlighter:
    """
    Where the highlighter comes from and how a page is told to use it.

    :cvar version: the highlight.js release to load (pinned)
    :cvar theme: the highlight.js stylesheet (``github`` is close to the Pygments look the docs site uses)
    """
    version = "11.9.0"
    theme = "github"
    cdn = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/{version}"

    @classmethod
    def script_url(cls):
        """The URL of the highlighter script."""
        return cls.cdn.format(version=cls.version) + "/highlight.min.js"

    @classmethod
    def style_url(cls):
        """The URL of the highlighter's stylesheet."""
        return cls.cdn.format(version=cls.version) + "/styles/{}.min.css".format(cls.theme)

    LOADER_JS = r"""
(function(){
if(window.__mcuHighlight){return;}
window.__mcuHighlight=true;
var SCRIPT=__SCRIPT__,STYLE=__STYLE__;
var SELECTOR='pre > code[class*="language-"]:not([data-mcu-hl])';
var loading=null;
function style(){
  if(document.getElementById('mcu-hljs-css')){return;}
  var l=document.createElement('link');l.id='mcu-hljs-css';l.rel='stylesheet';l.href=STYLE;document.head.appendChild(l);
}
function load(){
  if(window.hljs){return Promise.resolve(window.hljs);}
  if(!loading){
    style();
    loading=new Promise(function(resolve,reject){
      var s=document.createElement('script');s.src=SCRIPT;
      s.onload=function(){resolve(window.hljs);};
      s.onerror=function(){loading=null;s.remove();reject(new Error('highlighter not reachable'));};
      document.head.appendChild(s);
    });
  }
  return loading;
}
var queued=false;
function run(){
  queued=false;
  var found=document.querySelectorAll(SELECTOR),todo=[];
  for(var i=0;i<found.length;i++){if(found[i].children.length===0){todo.push(found[i]);}}   // already marked-up code is left alone
  if(!todo.length){return;}
  load().then(function(h){
    todo.forEach(function(el){
      if(el.getAttribute('data-mcu-hl')){return;}
      el.setAttribute('data-mcu-hl','1');
      try{h.highlightElement(el);}catch(e){}
    });
  }).catch(function(){});
}
function schedule(){if(!queued){queued=true;(window.requestAnimationFrame||setTimeout)(run);}}
new MutationObserver(function(ms){
  for(var i=0;i<ms.length;i++){if(ms[i].addedNodes.length){schedule();return;}}
}).observe(document.documentElement,{childList:true,subtree:true});
schedule();
})();
"""

    @classmethod
    def loader_js(cls):
        """The page loader/watcher script."""
        return cls.LOADER_JS.replace("__SCRIPT__", json.dumps(cls.script_url())).replace("__STYLE__", json.dumps(cls.style_url()))

    _shown = False
    @classmethod
    def ensure_loaded(cls, force=False):
        """
        Shows the loader in the notebook (once per kernel unless ``force``); the loader itself does nothing a second
        time on the same page, so showing it again, for instance after clearing outputs, is always safe.

        :param force: show it even if it was shown before
        :type force: bool
        :return: whether the loader was shown
        :rtype: bool
        """
        if cls._shown and not force:
            return False
        from .WidgetTools import JupyterAPIs
        display = JupyterAPIs.get_display_api()
        if display is None:
            return False
        cls._shown = True
        display.display(display.HTML("<script>" + cls.loader_js() + "</script>"))
        return True

    @classmethod
    def head_elements(cls):
        """
        The elements a standalone HTML page needs in its ``<head>`` to highlight its code blocks.

        :return: stylesheet and script elements
        :rtype: list
        """
        from .JHTML import JHTML
        return [
            JHTML.Link(rel="stylesheet", href=cls.style_url()),
            JHTML.Script(src=cls.script_url()),
            JHTML.Script("document.addEventListener('DOMContentLoaded',function(){"
                         "if(window.hljs){document.querySelectorAll('pre > code[class*=\"language-\"]').forEach(function(el){"
                         "if(el.children.length===0){hljs.highlightElement(el);}});}});"),
        ]
