## <a id="McUtils.Docs.Stubs.ExampleHandler">ExampleHandler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs.py#L1290)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L1290?message=Update%20Docs)]
</div>

Extracts runnable examples from each package's test file (see
`locate_test_file`) during `parse()`, writing each one under
`<out_dir>/examples/<package_name>/` immediately (there's no reason to
defer per-example writes -- they don't depend on any other package).
At `write()` time, writes the single aggregated usage_graph.json built
up across every package's examples.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
name: str
TEST_FILENAME_TEMPLATE: str
EXAMPLES_DIRNAME: str
EXAMPLE_FILENAME_TEMPLATE: str
USAGE_GRAPH_FILENAME: str
EXAMPLE_FILE_HEADER_TEMPLATE: str
EXAMPLES_PARSER_UNAVAILABLE_WARNING: str
EXAMPLES_PARSE_ERROR_TEMPLATE: str
```
<a id="McUtils.Docs.Stubs.ExampleHandler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, dispatcher, filter=None, exclude=<function default_exclude at 0x7fcf5b93baf0>): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs.py#L1301)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L1301?message=Update%20Docs)]
</div>
Args:
filter: optional ``(qualname, package_name) -> bool``, checked
    against ``"{TestClassName}.{test_method_name}"``. If
    given, only matching examples are written at all; ``None``
    (default) applies no filter.
exclude: optional ``(qualname, package_name) -> bool``,
    inverted from `filter`. Defaults to :func:`default_exclude`;
    pass ``None`` to disable.


<a id="McUtils.Docs.Stubs.ExampleHandler.wanted" class="docs-object-method">&nbsp;</a> 
```python
wanted(self, qualname, package_name=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/ExampleHandler.py#L1316)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/ExampleHandler.py#L1316?message=Update%20Docs)]
</div>
True if `qualname` (a ``"{TestClass}.{test_method}"`` name)
should actually be written as an example, given this handler's
`filter`/`exclude`.


<a id="McUtils.Docs.Stubs.ExampleHandler.locate_test_file" class="docs-object-method">&nbsp;</a> 
```python
locate_test_file(self, package_name, tests_directory): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/ExampleHandler.py#L1343)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/ExampleHandler.py#L1343?message=Update%20Docs)]
</div>
Mirrors McUtils.Docs.DocBuilder's `tests_directory` convention:
a flat directory containing one `<PackageName>Tests.py` file per
top-level package (e.g. `ci/tests/CombinatoricsTests.py`).
Returns None if tests_directory is falsy or the file doesn't
exist.


<a id="McUtils.Docs.Stubs.ExampleHandler.build_usage_graph_for_package" class="docs-object-method">&nbsp;</a> 
```python
build_usage_graph_for_package(self, package_name, parser): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/ExampleHandler.py#L1421)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/ExampleHandler.py#L1421?message=Update%20Docs)]
</div>
Combine ExamplesParser.functions_map (bare name -> example
names referencing it) with our own name resolution to produce
{fully_qualified_name: {example_ids}}, applying the dispatcher's
dependency_blacklist exactly as record_module_dependencies does.
Does not mutate dispatcher.usage_graph -- caller merges it in, so
this can also be inspected/tested standalone.


<a id="McUtils.Docs.Stubs.ExampleHandler.extract_examples" class="docs-object-method">&nbsp;</a> 
```python
extract_examples(self, package_name, tests_directory=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/ExampleHandler.py#L1482)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/ExampleHandler.py#L1482?message=Update%20Docs)]
</div>
For one top-level package: locate its test file (see
locate_test_file), parse it with McUtils.Docs.ExamplesParser,
write each example under
<out_dir>/examples/<package_name>/, and merge its usage into
dispatcher.usage_graph. Safe to call even when no test file
exists, ExamplesParser isn't importable, or parsing fails --
returns 0 and (for the latter two) prints a warning rather than
raising, since example extraction is a best-effort bonus on top
of the stubs/summaries, not something that should block the rest
of the pipeline.

Returns the number of examples written.


<a id="McUtils.Docs.Stubs.ExampleHandler.write_usage_graph" class="docs-object-method">&nbsp;</a> 
```python
write_usage_graph(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/ExampleHandler.py#L1521)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/ExampleHandler.py#L1521?message=Update%20Docs)]
</div>
Write usage_graph.json at the root of out_dir: {fully
qualified name: [example ids that use it]}, blacklist-filtered
the same way as dependency_graph.json.


<a id="McUtils.Docs.Stubs.ExampleHandler.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, package_name, pkg_src_path): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/ExampleHandler.py#L1531)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/ExampleHandler.py#L1531?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.Stubs.ExampleHandler.write" class="docs-object-method">&nbsp;</a> 
```python
write(self, components): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/Stubs/ExampleHandler.py#L1536)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs/ExampleHandler.py#L1536?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/Stubs/ExampleHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/Stubs/ExampleHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/Stubs/ExampleHandler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/Stubs/ExampleHandler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/Stubs.py#L1290?message=Update%20Docs)   
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