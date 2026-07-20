# <a id="McUtils.Docs.HTMLDocs.static_doc">static_doc</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/HTMLDocs.py#L602)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs.py#L602?message=Update%20Docs)]
</div>

```python
static_doc(obj, max_depth=1, title=None, out_file=None, include_finx_js=True, verbose=False, return_string=False): 
```
The static-HTML sibling of `McUtils.Docs.jdoc`.

Walks `obj` with the exact same `DocWalker` machinery `jdoc` uses
(`ModuleWriter`, `ClassWriter`, `FunctionWriter`, `MethodWriter`,
`ObjectWriter`, `IndexWriter`), but renders through a
`StaticHTMLTemplateEngine` instead of the ipywidget-producing
`InteractiveTemplateEngine`. Both engines build their output out of the
same `McUtils.Jupyter.JHTML` element interfaces; this one just never
triggers JHTML's widget-dispatch path, so the whole tree comes back as
one self-contained static HTML document (finx CSS/JS baked in) instead
of a live widget tree.
  - `obj`: `Any`
    > the object (module, class, function, ...) to document
  - `max_depth`: `Any`
    > how far down the object tree to recurse (same meaning as in `jdoc`)
  - `title`: `Any`
    > page title (defaults to the object's name)
  - `out_file`: `Any`
    > if given, the HTML is written to this path and the path is returned;
    otherwise the HTML string itself is returned
  - `include_finx_js`: `Any`
    > whether to bake in finx's `init.js` (+ a CDN jQuery) for
    the sidebar-toggle behavior; the CSS is always included
  - `verbose`: `Any`
    > `DocWalker` prints a line per module/class it visits;
    set `True` to see that progress chatter
  - `:returns`: `_`
    > the HTML string, or the path written to if `out_file` was given











---


<div markdown="1" class="text-secondary">
<div class="container">
  <div class="row">
   <div class="col" markdown="1">
**Feedback**   
</div>
   <div class="col" markdown="1">
**Examples**   
</div>
   <div class="col" markdown="1">
**Templates**   
</div>
   <div class="col" markdown="1">
**Documentation**   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Bug](https://github.com/McCoyGroup/McUtils/issues/new?title=Documentation%20Improvement%20Needed)/[Request](https://github.com/McCoyGroup/McUtils/issues/new?title=Example%20Request)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/HTMLDocs/static_doc.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/HTMLDocs/static_doc.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/HTMLDocs/static_doc.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/HTMLDocs/static_doc.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/HTMLDocs.py#L602?message=Update%20Docs)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>
</div>