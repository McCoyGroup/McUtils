## <a id="McUtils.Docs.Stubs.PackageHandler">PackageHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs.py#L1147)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L1147?message=Update%20Docs)]
</div>

Base class for one pluggable, per-package documentation artifact.

Lifecycle, per `DocumentationPackageDispatcher` run:
  * one instance is constructed per handler *class* the dispatcher was
    given, via ``HandlerCls(dispatcher)``;
  * ``.parse(package_name, pkg_src_path)`` is called once per package
    during ``dispatcher.generate(package_name)`` and returns whatever
    "components" that handler produced for this package (a plain dict --
    this is also where any files specific to *this one package* get
    written, e.g. its stub tree or its extracted examples);
  * once every package has been generated, ``.write(components)`` is
    called once, at ``dispatcher.finalize()`` time, with
    ``{package_name: <that package's parse() result>}`` for every
    package processed so far -- this is where cross-package aggregation
    happens (an index, a combined graph, a single sidecar file, ...).







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
name: str
```
<a id="McUtils.Docs.Stubs.PackageHandler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, dispatcher): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs.py#L1169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L1169?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.PackageHandler.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, package_name, pkg_src_path): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/PackageHandler.py#L1172)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/PackageHandler.py#L1172?message=Update%20Docs)]
</div>
Do the per-package work; return this package's components.


<a id="McUtils.Docs.Stubs.PackageHandler.write" class="docs-object-method">&nbsp;</a> 
```python
write(self, components): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/PackageHandler.py#L1176)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/PackageHandler.py#L1176?message=Update%20Docs)]
</div>
Do the cross-package work, given every package's `parse()` result.

Args:
    components: ``{package_name: {handler_name: parse()-result}}``
        -- i.e. the dispatcher's full report, not just this
        handler's slice of it (so a handler can, if it wants,
        look at what a *different* handler produced).
 </div>
</div>












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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/Stubs/PackageHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/Stubs/PackageHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/Stubs/PackageHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/Stubs/PackageHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L1147?message=Update%20Docs)   
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