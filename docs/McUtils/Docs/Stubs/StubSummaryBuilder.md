## <a id="McUtils.Docs.Stubs.StubSummaryBuilder">StubSummaryBuilder</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs.py#L43)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L43?message=Update%20Docs)]
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
EXAMPLES_DIRNAME: str
USAGE_GRAPH_FILENAME: str
TEST_FILENAME_TEMPLATE: str
EXAMPLE_FILENAME_TEMPLATE: str
EXAMPLE_FILE_HEADER_TEMPLATE: str
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
EXAMPLES_PARSER_UNAVAILABLE_WARNING: str
EXAMPLES_PARSE_ERROR_TEMPLATE: str
NO_PACKAGES_DISCOVERED_ERROR: str
PACKAGE_NOT_FOUND_ERROR_TEMPLATE: str
NO_TOP_LEVEL_PACKAGES_ERROR_TEMPLATE: str
ROOT_DIR_NOT_FOUND_ERROR: str
ModuleData: ModuleData
```
<a id="McUtils.Docs.Stubs.StubSummaryBuilder.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, root_src_dir=None, out_dir='stubs', max_doc_len=800, min_words=5, write_sidecar_file=False, verbose=False, allow_static_mode=True, tests_directory=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs.py#L322)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L322?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.root_module_name" class="docs-object-method">&nbsp;</a> 
```python
@property
root_module_name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L337)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L337?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.resolved_root_dir" class="docs-object-method">&nbsp;</a> 
```python
@property
resolved_root_dir(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L340)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L340?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.packages" class="docs-object-method">&nbsp;</a> 
```python
@property
packages(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L343)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L343?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.sidecar" class="docs-object-method">&nbsp;</a> 
```python
@property
sidecar(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L346)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L346?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.report" class="docs-object-method">&nbsp;</a> 
```python
@property
report(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L349)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L349?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.dynamic_mode" class="docs-object-method">&nbsp;</a> 
```python
@property
dynamic_mode(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L352)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L352?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.dependency_graph" class="docs-object-method">&nbsp;</a> 
```python
@property
dependency_graph(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L355)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L355?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.usage_graph" class="docs-object-method">&nbsp;</a> 
```python
@property
usage_graph(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L358)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L358?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.collapse_scalar_assign_runs" class="docs-object-method">&nbsp;</a> 
```python
collapse_scalar_assign_runs(self, body, min_group=6, context=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L371)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L371?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.is_collapsed_registry" class="docs-object-method">&nbsp;</a> 
```python
is_collapsed_registry(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L419)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L419?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.externalize_large_literal" class="docs-object-method">&nbsp;</a> 
```python
externalize_large_literal(self, node, module_key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L450)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L450?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.is_simple_assign" class="docs-object-method">&nbsp;</a> 
```python
is_simple_assign(self, node, max_len=120): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L483)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L483?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.is_all_operation" class="docs-object-method">&nbsp;</a> 
```python
is_all_operation(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L500)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L500?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L557)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L557?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L651)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L651?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L746)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L746?message=Update%20Docs)]
</div>
Write dependency_graph.json at the root of out_dir. See
record_module_dependencies for how entries are determined.


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.locate_test_file" class="docs-object-method">&nbsp;</a> 
```python
locate_test_file(self, package_name, tests_directory): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L766)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L766?message=Update%20Docs)]
</div>
Mirrors McUtils.Docs.DocBuilder's `tests_directory` convention:
a flat directory containing one `<PackageName>Tests.py` file per
top-level package (e.g. `ci/tests/CombinatoricsTests.py`).
Returns None if tests_directory is falsy or the file doesn't
exist.


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.build_usage_graph_for_package" class="docs-object-method">&nbsp;</a> 
```python
build_usage_graph_for_package(self, package_name, parser): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L842)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L842?message=Update%20Docs)]
</div>
Combine ExamplesParser.functions_map (bare name -> example
names referencing it) with our own name resolution to produce
{fully_qualified_name: {example_ids}}, applying
self.dependency_blacklist exactly as record_module_dependencies
does. Does not mutate self.usage_graph -- caller merges it in,
so this can also be inspected/tested standalone.


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.extract_examples" class="docs-object-method">&nbsp;</a> 
```python
extract_examples(self, package_name, tests_directory=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L891)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L891?message=Update%20Docs)]
</div>
For one top-level package: locate its test file (see
locate_test_file), parse it with McUtils.Docs.ExamplesParser,
write each example under
<out_dir>/<root_module_name>/<package_name>/examples/, and
merge its usage into self.usage_graph. Safe to call even when
no test file exists, ExamplesParser isn't importable, or
parsing fails -- returns 0 and (for the latter two) prints a
warning rather than raising, since example extraction is a
best-effort bonus on top of the stubs/summaries, not something
that should block the rest of the pipeline.

Returns the number of examples written.


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.write_usage_graph" class="docs-object-method">&nbsp;</a> 
```python
write_usage_graph(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L928)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L928?message=Update%20Docs)]
</div>
Write usage_graph.json at the root of out_dir: {fully
qualified name: [example ids that use it]}, blacklist-filtered
the same way as dependency_graph.json.


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.stub_function" class="docs-object-method">&nbsp;</a> 
```python
stub_function(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L938)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L938?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.stub_class" class="docs-object-method">&nbsp;</a> 
```python
stub_class(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L947)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L947?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.stub_module" class="docs-object-method">&nbsp;</a> 
```python
stub_module(self, source, module_key, dynamic_all=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L978)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L978?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.stub_package" class="docs-object-method">&nbsp;</a> 
```python
stub_package(self, src_dir, out_dir, package_name=None, keep_full=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1033)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1033?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.write_sidecar_files" class="docs-object-method">&nbsp;</a> 
```python
write_sidecar_files(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1070)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1070?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.first_line" class="docs-object-method">&nbsp;</a> 
```python
first_line(self, docstring, max_len=100): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1088)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1088?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.class_doc_summary" class="docs-object-method">&nbsp;</a> 
```python
class_doc_summary(self, full_doc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1113)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1113?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.render_params" class="docs-object-method">&nbsp;</a> 
```python
render_params(self, args, skip_first=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1125)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1125?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.summarize_class" class="docs-object-method">&nbsp;</a> 
```python
summarize_class(self, node, indent='  '): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1185)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1185?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.summarize_module" class="docs-object-method">&nbsp;</a> 
```python
summarize_module(self, path, rel_path): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1216)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1216?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.build_package_summary" class="docs-object-method">&nbsp;</a> 
```python
build_package_summary(self, src_dir, out_file): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1246)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1246?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.discover_top_level_packages" class="docs-object-method">&nbsp;</a> 
```python
discover_top_level_packages(self, root_module_name, try_dynamic=True, src_dir=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1293)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1293?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.generate" class="docs-object-method">&nbsp;</a> 
```python
generate(self, package_name, root_module_name=None, update_current=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1368)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1368?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.generate_all" class="docs-object-method">&nbsp;</a> 
```python
generate_all(self, root_module_name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1423)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1423?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.write_llm_readme" class="docs-object-method">&nbsp;</a> 
```python
write_llm_readme(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1437)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1437?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1466)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1466?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.StubSummaryBuilder.write_index" class="docs-object-method">&nbsp;</a> 
```python
write_index(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1496)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/StubSummaryBuilder.py#L1496?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L43?message=Update%20Docs)   
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