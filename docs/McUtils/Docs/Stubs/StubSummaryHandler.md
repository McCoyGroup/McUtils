## <a id="McUtils.Docs.Stubs.StubSummaryHandler">StubSummaryHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs.py#L1188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L1188?message=Update%20Docs)]
</div>

Generates per-module stubs + a per-package API summary during
`parse()`. At `write()` time -- once every package has been parsed --
writes the artifacts that depend on the full set having been built:
dependency_graph.json, the sidecar data file (if enabled),
summaries/index.md, and LLM.md.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
name: str
```
<a id="McUtils.Docs.Stubs.StubSummaryHandler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, dispatcher, builder=None, filter=None, exclude=<function default_exclude at 0x7f04bb4e1940>): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs.py#L1198)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L1198?message=Update%20Docs)]
</div>
Args:
filter: optional ``(qualname, package_name) -> bool`` forwarded
    to the builder -- only affects which functions/classes
    appear in the API *summary*; stub files always preserve
    every real function/class. Defaults to ``None`` (no
    filtering).
exclude: optional ``(qualname, package_name) -> bool``
    forwarded to the builder. Defaults to
    :func:`default_exclude`; pass ``None`` to disable.


<a id="McUtils.Docs.Stubs.StubSummaryHandler.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, package_name, pkg_src_path): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryHandler.py#L1218)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryHandler.py#L1218?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryHandler.write" class="docs-object-method">&nbsp;</a> 
```python
write(self, components): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryHandler.py#L1255)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryHandler.py#L1255?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/Stubs/StubSummaryHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/Stubs/StubSummaryHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/Stubs/StubSummaryHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/Stubs/StubSummaryHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L1188?message=Update%20Docs)   
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