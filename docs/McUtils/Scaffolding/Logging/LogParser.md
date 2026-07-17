## <a id="McUtils.Scaffolding.Logging.LogParser">LogParser</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging.py#L15?message=Update%20Docs)]
</div>

A parser that will take a log file and stream it as a series of blocks







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
LogBlockParser: LogBlockParser
```
<a id="McUtils.Scaffolding.Logging.LogParser.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, file, block_settings=None, binary=False, block_level_padding=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging.py#L19?message=Update%20Docs)]
</div>
**LLM Docstring**

Configure block syntax and padding, then initialize a file-stream parser for the log source.
  - `file`: `object`
    > path or file-like object
  - `block_settings`: `object`
    > syntax dictionaries for each log nesting level
  - `binary`: `object`
    > whether the underlying stream yields bytes
  - `block_level_padding`: `object`
    > prefix added when synthesizing deeper block syntax
  - `kwargs`: `object`
    > keyword arguments forwarded to a callable
  - `:returns`: `None`
    > No explicit value; the method mutates state or performs I/O.


<a id="McUtils.Scaffolding.Logging.LogParser.get_block_settings" class="docs-object-method">&nbsp;</a> 
```python
get_block_settings(self, block_level): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging/LogParser.py#L46)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging/LogParser.py#L46?message=Update%20Docs)]
</div>
**LLM Docstring**

Return syntax for a nesting level, extending the deepest known syntax with repeated padding when necessary.
  - `block_level`: `object`
    > zero-based nesting depth
  - `:returns`: `dict`
    > The syntax mapping for the requested block depth.


<a id="McUtils.Scaffolding.Logging.LogParser.get_block" class="docs-object-method">&nbsp;</a> 
```python
get_block(self, level=0, tag=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging/LogParser.py#L301)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging/LogParser.py#L301?message=Update%20Docs)]
</div>

  - `level`: `Any`
    > 
  - `tag`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Logging.LogParser.get_line" class="docs-object-method">&nbsp;</a> 
```python
get_line(self, level=0, tag=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging/LogParser.py#L336)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging/LogParser.py#L336?message=Update%20Docs)]
</div>

  - `level`: `Any`
    > 
  - `tag`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.Logging.LogParser.get_blocks" class="docs-object-method">&nbsp;</a> 
```python
get_blocks(self, tag=None, level=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging/LogParser.py#L358)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging/LogParser.py#L358?message=Update%20Docs)]
</div>
**LLM Docstring**

Yield successive parsed blocks until `get_block` signals that the stream is exhausted.
  - `tag`: `object`
    > optional block or line tag
  - `level`: `object`
    > log nesting level
  - `:returns`: `collections.abc.Iterator`
    > An iterator over parsed blocks, lines, or delimited substrings.


<a id="McUtils.Scaffolding.Logging.LogParser.get_lines" class="docs-object-method">&nbsp;</a> 
```python
get_lines(self, tag=None, level=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging/LogParser.py#L384)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging/LogParser.py#L384?message=Update%20Docs)]
</div>
**LLM Docstring**

Yield successive prompt lines until `get_line` signals that the stream is exhausted.
  - `tag`: `object`
    > optional block or line tag
  - `level`: `object`
    > log nesting level
  - `:returns`: `collections.abc.Iterator`
    > An iterator over parsed blocks, lines, or delimited substrings.


<a id="McUtils.Scaffolding.Logging.LogParser.tag_match" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
tag_match(cls, tag, tag_filter): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L410)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L410?message=Update%20Docs)]
</div>
**LLM Docstring**

Test a tag against a regex string or pattern, predicate, or container-style filter.
  - `tag`: `object`
    > optional block or line tag
  - `tag_filter`: `object`
    > tag exclusion matcher
  - `:returns`: `object`
    > The regex match object or predicate/container result used as a truth value.


<a id="McUtils.Scaffolding.Logging.LogParser.post_process_treelist" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
post_process_treelist(cls, res, combine_subtrees=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L431)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L431?message=Update%20Docs)]
</div>
**LLM Docstring**

Collapse a singleton result and merge sibling dictionaries when their keys do not conflict.
  - `res`: `object`
    > list of parsed tree elements
  - `combine_subtrees`: `object`
    > whether compatible sibling dictionaries should be merged
  - `:returns`: `object`
    > the collapsed singleton, merged dictionary, or original list


<a id="McUtils.Scaffolding.Logging.LogParser.to_tree" class="docs-object-method">&nbsp;</a> 
```python
to_tree(self, tag_filter=None, depth=-1, combine_subtrees=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging/LogParser.py#L461)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging/LogParser.py#L461?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse all top-level blocks into a `TreeWrapper`, applying tag filtering, recursion depth, and subtree merging.
  - `tag_filter`: `object`
    > tag exclusion matcher
  - `depth`: `object`
    > remaining recursion depth; negative values are unlimited
  - `combine_subtrees`: `object`
    > whether compatible sibling dictionaries should be merged
  - `:returns`: `dict | list | TreeWrapper`
    > The recursively constructed tree representation.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Logging/LogParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Logging/LogParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Logging/LogParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Logging/LogParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging.py#L15?message=Update%20Docs)   
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