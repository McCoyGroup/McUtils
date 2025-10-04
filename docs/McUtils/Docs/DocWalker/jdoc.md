# <a id="McUtils.Docs.DocWalker.jdoc">jdoc</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/DocWalker.py#L1094)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker.py#L1094?message=Update%20Docs)]
</div>

```python
jdoc(obj, max_depth=1, engine=None): 
```
provides documentation in a Jupyter-friendly environment
  - `obj`: `Any`
    > the object to extract documentation for
  - `max_depth`: `int`
    > the depth in the object tree to go down to (default: `1`)
  - `:returns`: `..Jupyter.Component`
    > 


<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#Details-4b59fc" markdown="1"> Details</a> <a class="float-right" data-toggle="collapse" href="#Details-4b59fc"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse " id="Details-4b59fc" markdown="1">
 Makes use of the `JHTML` system to nicely format documentation as well as the
documentation utilities found in `McUtils.Docs` (which were orginally written
as part of the `Peeves` package).

Asking for too many pieces of documentation at once can really slow things down,
so by default the object tree is traversed only shallowly.
In principle, the documentation could be directly exported to an HTML document as
no `Widget`-necessary bits are used (at least as on when I write this) but a better
choice is to generate Markdown docs using the standard `DocsBuilder` approach.
This provides flexibility and can be ingested into any number of Markdown->HTML systems.

 </div>
</div>


## Examples
Get documentation for `jdoc`

```python
jdoc(jdoc)
```

Get documentation for an entire module

```python
import McUtils.Docs as MDoc
jdoc(Mdoc)
```






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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/DocWalker/jdoc.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/DocWalker/jdoc.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/DocWalker/jdoc.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/DocWalker/jdoc.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker.py#L1094?message=Update%20Docs)   
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