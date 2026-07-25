## <a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher">DocumentationPackageDispatcher</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs.py#L1540)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L1540?message=Update%20Docs)]
</div>

Owns package/module resolution -- discovering a root module's
top-level packages, and the per-run state that comes with that
(sidecar data, dependency/usage graphs, the accumulated report) -- and
drives a set of `PackageHandler`s over it. Each handler is responsible
for one independent documentation artifact; by default that's stubs
+summaries (`StubSummaryHandler`) and extracted examples
(`ExampleHandler`), but any `PackageHandler` subclass can be added or
swapped in via `handlers`.

Parameters
----------
root_src_dir : str or None
    Path to the root module's source directory (the folder
    containing its __init__.py). If None, the root module must be
    importable and its location is resolved from that import.
out_dir : str
    Output directory handed to every handler.
max_doc_len, min_words, write_sidecar_file : see StubSummaryBuilder --
    forwarded to the default StubSummaryHandler's builder.
tests_directory : str or None
    Forwarded to ExampleHandler; if None, example extraction is skipped.
handlers : iterable of PackageHandler subclasses, optional
    Defaults to `(StubSummaryHandler, ExampleHandler)`. Each is
    instantiated as `HandlerCls(self)`.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
INIT_FILENAME: str
STDLIB_BLACKLIST_PACKAGES: frozenset
COMMON_THIRD_PARTY_BLACKLIST_PACKAGES: frozenset
DEFAULT_DEPENDENCY_BLACKLIST: frozenset
IMPORT_FALLBACK_INFO_TEMPLATE: str
NO_PACKAGES_DISCOVERED_ERROR: str
PACKAGE_NOT_FOUND_ERROR_TEMPLATE: str
NO_TOP_LEVEL_PACKAGES_ERROR_TEMPLATE: str
ROOT_DIR_NOT_FOUND_ERROR: str
DEFAULT_HANDLERS: tuple
ModuleData: ModuleData
```
<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, root_src_dir=None, out_dir='stubs', max_doc_len=800, min_words=5, write_sidecar_file=False, verbose=False, allow_static_mode=True, tests_directory=None, handlers=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs.py#L1595)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L1595?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.root_module_name" class="docs-object-method">&nbsp;</a> 
```python
@property
root_module_name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1614)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1614?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.resolved_root_dir" class="docs-object-method">&nbsp;</a> 
```python
@property
resolved_root_dir(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1617)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1617?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.packages" class="docs-object-method">&nbsp;</a> 
```python
@property
packages(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1620)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1620?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.sidecar" class="docs-object-method">&nbsp;</a> 
```python
@property
sidecar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1623)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1623?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.report" class="docs-object-method">&nbsp;</a> 
```python
@property
report(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1626)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1626?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.dynamic_mode" class="docs-object-method">&nbsp;</a> 
```python
@property
dynamic_mode(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1629)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1629?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.dependency_graph" class="docs-object-method">&nbsp;</a> 
```python
@property
dependency_graph(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1632)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1632?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.usage_graph" class="docs-object-method">&nbsp;</a> 
```python
@property
usage_graph(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1635)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1635?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.discover_top_level_packages" class="docs-object-method">&nbsp;</a> 
```python
discover_top_level_packages(self, root_module_name, try_dynamic=True, src_dir=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1685)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1685?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.generate" class="docs-object-method">&nbsp;</a> 
```python
generate(self, package_name, root_module_name=None, update_current=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1759)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1759?message=Update%20Docs)]
</div>
Resolve `package_name`'s source path and run every handler's
`.parse()` over it, filing each handler's returned components
under `self.report[package_name][handler.name]`.


<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.generate_all" class="docs-object-method">&nbsp;</a> 
```python
generate_all(self, root_module_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1783)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1783?message=Update%20Docs)]
</div>
Discover every top-level package under `root_module_name`,
`.generate()` each one, then `.finalize()`.


<a id="McUtils.Docs.Stubs.DocumentationPackageDispatcher.finalize" class="docs-object-method">&nbsp;</a> 
```python
finalize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1798)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/DocumentationPackageDispatcher.py#L1798?message=Update%20Docs)]
</div>
Call every handler's `.write()` with the full accumulated
report (`{package_name: {handler_name: parse()-result}}`), so each
handler can do its own cross-package aggregation.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/Stubs/DocumentationPackageDispatcher.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/Stubs/DocumentationPackageDispatcher.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/Stubs/DocumentationPackageDispatcher.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/Stubs/DocumentationPackageDispatcher.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L1540?message=Update%20Docs)   
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