## <a id="McUtils.Docs.Stubs.StubSummaryBuilder">StubSummaryBuilder</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs.py#L41)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L41?message=Update%20Docs)]
</div>

Parameters
----------
root_src_dir : str or None
    Path to the root module's source directory (the folder
    containing its __init__.py). If None, the root module must be
    importable and its location is resolved from that import.
out_dir : str
    Output directory. Stub trees are written to
    `<out_dir>/<root_module_name>/<pkg_name>/...`, summaries to
    `<out_dir>/summaries/<pkg_name>.md`, and the graph index to
    `<out_dir>/summaries/index.md`.
max_doc_len : int
    Cap on class docstrings in summaries: first paragraph or this
    many characters, whichever comes first.
min_words : int
    For one-line descriptions: skip docstring lines with this many
    words or fewer (filters out short placeholder lines), using the
    first line that exceeds it.
write_sidecar_file : bool
    If True, externalized large literals are written to a shared
    `_registry_data.json` (+ loader module) under out_dir, and stubs
    get a loader call to fetch them. If False (default), only a
    key/shape summary comment is left in the stub and the raw data
    is dropped entirely.

Overridable methods
--------------------
Every step is a plain instance method, so a subclass can override
any piece of the pipeline, e.g.:

    class MyBuilder(StubSummaryBuilder):
        def discover_top_level_packages(self, root_module_name):
            # custom discovery logic, e.g. a hardcoded package list
            ...

        def build_package_summary(self, src_dir, out_file):
            # custom summary format
            ...







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
DATA_SIDECAR_THRESHOLD: int
SUMMARIES_DIRNAME: str
INDEX_FILENAME: str
LLM_README_FILENAME: str
INIT_FILENAME: str
PACKAGE_SUMMARY_FILENAME_TEMPLATE: str
SIDECAR_MODULE_NAME: str
SIDECAR_JSON_FILENAME: str
SIDECAR_LOADER_FILENAME: str
SIDECAR_LOADER_FUNC_NAME: str
DEPENDENCY_GRAPH_FILENAME: str
STDLIB_BLACKLIST_PACKAGES: frozenset
COMMON_THIRD_PARTY_BLACKLIST_PACKAGES: frozenset
DEFAULT_DEPENDENCY_BLACKLIST: frozenset
TRUNCATION_MARKER: str
ENUM_ACCESS_NOTE_TEMPLATE: str
CLASS_ATTR_ACCESS_NOTE_TEMPLATE: str
MODULE_SCALAR_ACCESS_NOTE_TEMPLATE: str
EXTERNALIZED_DATA_NOTE_TEMPLATE: str
OMITTED_DATA_NOTE_TEMPLATE: str
DESCRIBE_DICT_SMALL_TEMPLATE: str
DESCRIBE_DICT_LARGE_TEMPLATE: str
DESCRIBE_LIST_SMALL_TEMPLATE: str
DESCRIBE_LIST_LARGE_TEMPLATE: str
DESCRIBE_SCALAR_TEMPLATE: str
SIDECAR_LOADER_TEMPLATE: str
INDEX_HEADER_TEMPLATE: str
INDEX_INTRO_TEMPLATE: str
INDEX_ENTRY_TEMPLATE: str
SIDECAR_PRESENT_NOTE_TEMPLATE: str
SIDECAR_ABSENT_NOTE: str
DEPENDENCY_GRAPH_NOTE_TEMPLATE: str
LLM_README_TEMPLATE: str
SUMMARY_HEADER_TEMPLATE: str
SUMMARY_SOURCE_LINE_TEMPLATE: str
SUMMARY_STUB_LINE_TEMPLATE: str
SUMMARY_SUMMARY_LINE_TEMPLATE: str
SUMMARY_SIDECAR_LINE_TEMPLATE: str
SYNTAX_ERROR_WARNING_TEMPLATE: str
IMPORT_FALLBACK_INFO_TEMPLATE: str
NO_PACKAGES_DISCOVERED_ERROR: str
PACKAGE_NOT_FOUND_ERROR_TEMPLATE: str
NO_TOP_LEVEL_PACKAGES_ERROR_TEMPLATE: str
ROOT_DIR_NOT_FOUND_ERROR: str
ModuleData: ModuleData
```
<a id="McUtils.Docs.Stubs.StubSummaryBuilder.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, root_src_dir=None, out_dir='stubs', max_doc_len=800, min_words=5, write_sidecar_file=False, verbose=False, allow_static_mode=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs.py#L304)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L304?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.root_module_name" class="docs-object-method">&nbsp;</a> 
```python
@property
root_module_name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L318)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L318?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.resolved_root_dir" class="docs-object-method">&nbsp;</a> 
```python
@property
resolved_root_dir(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L321)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L321?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.packages" class="docs-object-method">&nbsp;</a> 
```python
@property
packages(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L324)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L324?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.sidecar" class="docs-object-method">&nbsp;</a> 
```python
@property
sidecar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L327)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L327?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.report" class="docs-object-method">&nbsp;</a> 
```python
@property
report(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L330)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L330?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.dynamic_mode" class="docs-object-method">&nbsp;</a> 
```python
@property
dynamic_mode(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L333)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L333?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.dependency_graph" class="docs-object-method">&nbsp;</a> 
```python
@property
dependency_graph(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L336)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L336?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.collapse_scalar_assign_runs" class="docs-object-method">&nbsp;</a> 
```python
collapse_scalar_assign_runs(self, body, min_group=6, context=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L349)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L349?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.is_collapsed_registry" class="docs-object-method">&nbsp;</a> 
```python
is_collapsed_registry(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L397)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L397?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.externalize_large_literal" class="docs-object-method">&nbsp;</a> 
```python
externalize_large_literal(self, node, module_key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L428)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L428?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.is_simple_assign" class="docs-object-method">&nbsp;</a> 
```python
is_simple_assign(self, node, max_len=120): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L461)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L461?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.is_all_operation" class="docs-object-method">&nbsp;</a> 
```python
is_all_operation(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L478)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L478?message=Update%20Docs)]
</div>
True for any statement that assigns to, augments, or mutates
`__all__` -- `__all__ = [...]`, `__all__ += [...]`,
`__all__: list = [...]`, `__all__.append(...)`,
`__all__.extend(...)`, etc. These must ALWAYS be kept verbatim
and in their original relative order in the stub: dropping any
one of them (as AugAssign lines silently were before this
check existed) leaves `__all__` wrong at import time, which
breaks the source tree for anything that relies on it --
including this tool's own `discover_top_level_packages`.


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.resolve_dynamic_all" class="docs-object-method">&nbsp;</a> 
```python
resolve_dynamic_all(self, package_name, rel_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L535)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L535?message=Update%20Docs)]
</div>
If we're in dynamic_mode (the root module was really
importable), look up this specific module's real, fully-resolved
`__all__` -- so the stub can bake in the exact final result
instead of copying the source's accumulation logic.

Deliberately a PASSIVE `sys.modules` lookup, not a forcing
`importlib.import_module` call: the one real import already done
in `discover_top_level_packages` naturally cascades and loads
every submodule the package actually uses (via its own `from .X
import *` chains). We only bake __all__ for modules that showed
up in memory as a result of that -- we never trigger an
additional import of our own, so we can't accidentally force-load
(and pay the cost/risk of) some module the package itself never
needed. Returns None if dynamic_mode is off, the module was
never loaded, or it has no __all__ -- the stub then falls back
to preserving whatever __all__ operations exist in its own
source, verbatim.


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.record_module_dependencies" class="docs-object-method">&nbsp;</a> 
```python
record_module_dependencies(self, source, package_name, rel_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L629)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L629?message=Update%20Docs)]
</div>
Parse the ORIGINAL (pre-stub) source of one module and record,
into self.dependency_graph, which packages/classes/methods/
functions it references from other packages. Prefers live
introspection (when dynamic_mode has the module loaded, via the
same passive sys.modules lookup used for __all__ baking) over
the static import map, since live introspection correctly
resolves re-export chains like `from .X import *` that static
parsing can't attribute to individual names. Silently returns
(records nothing) on a syntax error -- dependency tracking is a
best-effort bonus, not something that should block stubbing.


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.write_dependency_graph" class="docs-object-method">&nbsp;</a> 
```python
write_dependency_graph(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L724)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L724?message=Update%20Docs)]
</div>
Write dependency_graph.json at the root of out_dir. See
record_module_dependencies for how entries are determined.


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.stub_function" class="docs-object-method">&nbsp;</a> 
```python
stub_function(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L740)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L740?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.stub_class" class="docs-object-method">&nbsp;</a> 
```python
stub_class(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L749)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L749?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.stub_module" class="docs-object-method">&nbsp;</a> 
```python
stub_module(self, source, module_key, dynamic_all=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L780)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L780?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.stub_package" class="docs-object-method">&nbsp;</a> 
```python
stub_package(self, src_dir, out_dir, package_name=None, keep_full=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L835)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L835?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.write_sidecar_files" class="docs-object-method">&nbsp;</a> 
```python
write_sidecar_files(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L872)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L872?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.first_line" class="docs-object-method">&nbsp;</a> 
```python
first_line(self, docstring, max_len=100): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L890)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L890?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.class_doc_summary" class="docs-object-method">&nbsp;</a> 
```python
class_doc_summary(self, full_doc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L915)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L915?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.render_params" class="docs-object-method">&nbsp;</a> 
```python
render_params(self, args, skip_first=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L927)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L927?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.summarize_class" class="docs-object-method">&nbsp;</a> 
```python
summarize_class(self, node, indent='  '): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L987)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L987?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.summarize_module" class="docs-object-method">&nbsp;</a> 
```python
summarize_module(self, path, rel_path): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1018)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1018?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.build_package_summary" class="docs-object-method">&nbsp;</a> 
```python
build_package_summary(self, src_dir, out_file): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1048)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1048?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.discover_top_level_packages" class="docs-object-method">&nbsp;</a> 
```python
discover_top_level_packages(self, root_module_name, try_dynamic=True, src_dir=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1095)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1095?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.generate" class="docs-object-method">&nbsp;</a> 
```python
generate(self, package_name, root_module_name=None, update_current=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1169?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.generate_all" class="docs-object-method">&nbsp;</a> 
```python
generate_all(self, root_module_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1219)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1219?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.write_llm_readme" class="docs-object-method">&nbsp;</a> 
```python
write_llm_readme(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1233)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1233?message=Update%20Docs)]
</div>
Write LLM.md at the root of out_dir: an operating manual for
an LLM consuming this directory -- navigation order, what's real
vs. placeholder, and how to correctly read each of the lossy-
looking-but-actually-lossless compression tricks used in the
stubs (enum/constant-run collapsing, externalized data). This
matters because misreading those tricks (e.g. treating a
collapsed `_MEMBERS` dict as the real access pattern) would
actively mislead an LLM rather than just under-inform it.


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.finalize" class="docs-object-method">&nbsp;</a> 
```python
finalize(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1262)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1262?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.write_index" class="docs-object-method">&nbsp;</a> 
```python
write_index(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1290)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1290?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/Stubs/StubSummaryBuilder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/Stubs/StubSummaryBuilder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/Stubs/StubSummaryBuilder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/Stubs/StubSummaryBuilder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L41?message=Update%20Docs)   
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