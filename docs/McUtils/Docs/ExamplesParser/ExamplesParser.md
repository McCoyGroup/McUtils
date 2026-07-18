## <a id="McUtils.Docs.ExamplesParser.ExamplesParser">ExamplesParser</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser.py#L8)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser.py#L8?message=Update%20Docs)]
</div>

Provides a parser for unit tests to turn them into examples







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
IGNORE_UNHANDLED_STATEMENTS: bool
```
<a id="McUtils.Docs.ExamplesParser.ExamplesParser.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, unit_tests): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser.py#L13)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser.py#L13?message=Update%20Docs)]
</div>
**LLM Docstring**

Parses unit-test source into an AST and initializes lazy caches.

The constructor does not classify tests immediately; `walk_tree` populates the cached class, setup, function, and function-map fields on demand.
  - `unit_tests`: `str`
    > the Python source containing setup code and test methods


<a id="McUtils.Docs.ExamplesParser.ExamplesParser.find_setup" class="docs-object-method">&nbsp;</a> 
```python
find_setup(self, tree_iter): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L32)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L32?message=Update%20Docs)]
</div>
**LLM Docstring**

Consumes leading module-level setup nodes until the first class definition.
  - `tree_iter`: `Iterator[ast.AST]`
    > an iterator over top-level AST nodes
  - `:returns`: `tuple[ast.ClassDef | None, list[ast.AST]]`
    > the first class node, or `None`, together with the preceding setup nodes


<a id="McUtils.Docs.ExamplesParser.ExamplesParser.parse_tests" class="docs-object-method">&nbsp;</a> 
```python
parse_tests(self, tree_iter): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L54)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L54?message=Update%20Docs)]
</div>
Parses out the
  - `tree_iter`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Docs.ExamplesParser.ExamplesParser.walk_tree" class="docs-object-method">&nbsp;</a> 
```python
walk_tree(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L82)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L82?message=Update%20Docs)]
</div>
**LLM Docstring**

Separates module setup, class setup, and `test_` methods and refreshes all parser caches.

This implementation assumes the first class node exists and passes its body to `parse_tests`.
  - `:returns`: `tuple[tuple[list[ast.AST], list[ast.AST]], collections.OrderedDict[str, ast.FunctionDef]]`
    > the module/class setup pair and ordered mapping of example names to test nodes


<a id="McUtils.Docs.ExamplesParser.ExamplesParser.format_node" class="docs-object-method">&nbsp;</a> 
```python
format_node(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L105?message=Update%20Docs)]
</div>
**LLM Docstring**

Returns the source text for an AST node with its original leading indentation.
  - `node`: `ast.AST`
    > the node to format
  - `:returns`: `str`
    > the cached source fragment


<a id="McUtils.Docs.ExamplesParser.ExamplesParser.from_file" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_file(cls, tests_file): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L125)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L125?message=Update%20Docs)]
</div>
**LLM Docstring**

Creates a parser from a test source file.
  - `tests_file`: `str | os.PathLike`
    > the file to read
  - `:returns`: `ExamplesParser`
    > a parser for the file contents


<a id="McUtils.Docs.ExamplesParser.ExamplesParser.class_spec" class="docs-object-method">&nbsp;</a> 
```python
@property
class_spec(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L140)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L140?message=Update%20Docs)]
</div>
**LLM Docstring**

Returns the parsed test class and its non-test setup nodes.

Parsing is triggered lazily if necessary.
  - `:returns`: `tuple[ast.ClassDef, list[ast.AST]]`
    > the class node and class-setup list


<a id="McUtils.Docs.ExamplesParser.ExamplesParser.setup" class="docs-object-method">&nbsp;</a> 
```python
@property
setup(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L154?message=Update%20Docs)]
</div>
**LLM Docstring**

Returns module-level setup nodes preceding the test class.

Parsing is triggered lazily if necessary.
  - `:returns`: `list[ast.AST]`
    > the setup-node list


<a id="McUtils.Docs.ExamplesParser.ExamplesParser.functions" class="docs-object-method">&nbsp;</a> 
```python
@property
functions(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L168)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L168?message=Update%20Docs)]
</div>
**LLM Docstring**

Returns the ordered mapping of example names to `test_` function nodes.

The `test_` prefix is removed from each key.
  - `:returns`: `collections.OrderedDict[str, ast.FunctionDef]`
    > the parsed test-function mapping


<a id="McUtils.Docs.ExamplesParser.ExamplesParser.functions_map" class="docs-object-method">&nbsp;</a> 
```python
@property
functions_map(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L182)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L182?message=Update%20Docs)]
</div>
**LLM Docstring**

Returns the reverse mapping from referenced names to examples that use them.

Parsing and map construction are triggered lazily if necessary.
  - `:returns`: `dict[str, list[str]]`
    > the referenced-name mapping


<a id="McUtils.Docs.ExamplesParser.ExamplesParser.load_function_map" class="docs-object-method">&nbsp;</a> 
```python
load_function_map(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L197?message=Update%20Docs)]
</div>
**LLM Docstring**

Builds a reverse index of names referenced by each parsed test function.
  - `:returns`: `dict[str, list[str]]`
    > a mapping from referenced names to example keys


<a id="McUtils.Docs.ExamplesParser.ExamplesParser.get_examples_functions" class="docs-object-method">&nbsp;</a> 
```python
get_examples_functions(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L290)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L290?message=Update%20Docs)]
</div>
**LLM Docstring**

Collects names referenced by a function or AST node body.
  - `node`: `ast.AST`
    > the node whose body should be inspected
  - `:returns`: `set[str]`
    > the referenced-name set


<a id="McUtils.Docs.ExamplesParser.ExamplesParser.filter_by_name" class="docs-object-method">&nbsp;</a> 
```python
filter_by_name(self, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L309)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L309?message=Update%20Docs)]
</div>
**LLM Docstring**

Returns a shallow parser copy restricted to examples that reference a given name.
  - `name`: `str`
    > the referenced function or object name
  - `:returns`: `ExamplesParser | None`
    > a restricted parser, or `None` when no examples match
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/ExamplesParser/ExamplesParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/ExamplesParser/ExamplesParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/ExamplesParser/ExamplesParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/ExamplesParser/ExamplesParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser.py#L8?message=Update%20Docs)   
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