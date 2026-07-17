## <a id="McUtils.Parsers.TeXParser.TeXParser">TeXParser</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/TeXParser.py#L11)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/TeXParser.py#L11?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_binary: bool
```
<a id="McUtils.Parsers.TeXParser.TeXParser.is_valid_tex_block" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_valid_tex_block(cls, block: str): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L13)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L13?message=Update%20Docs)]
</div>
**LLM Docstring**

Accept a TeX call block when unescaped opening braces are exactly one fewer than closing braces, matching a command whose leading `{` was consumed separately.
  - `block`: `str`
    > the candidate TeX or BibTeX source block

  - `:returns`: `bool`
    > `True` when the condition described above holds; otherwise `False`.


<a id="McUtils.Parsers.TeXParser.TeXParser.is_valid_stream_start" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_valid_stream_start(cls, tag_str): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L28)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L28?message=Update%20Docs)]
</div>
**LLM Docstring**

Accept a candidate command tag when it has a non-empty body and balanced square brackets.
  - `tag_str`: `object`
    > a candidate command or entry-start tag

  - `:returns`: `bool`
    > `True` when the condition described above holds; otherwise `False`.


<a id="McUtils.Parsers.TeXParser.TeXParser.parse_tex_call" class="docs-object-method">&nbsp;</a> 
```python
parse_tex_call(self, allowed_calls=None, return_end_points=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/TeXParser/TeXParser.py#L82)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/TeXParser/TeXParser.py#L82?message=Update%20Docs)]
</div>
**LLM Docstring**

Locate an allowed TeX command, read its balanced braced argument, then consume and concatenate any immediately adjacent braced arguments; optionally return the combined source endpoints.
  - `allowed_calls`: `object`
    > a command-name regex or iterable of allowed TeX commands

  - `return_end_points`: `object`
    > whether to return source offsets with the parsed block

  - `:returns`: `object`
    > The parsed block or typed result structure, with endpoint metadata when requested.


<a id="McUtils.Parsers.TeXParser.TeXParser.parse_tex_environment" class="docs-object-method">&nbsp;</a> 
```python
parse_tex_environment(self, allowed_environments=None, return_end_points=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/TeXParser/TeXParser.py#L212)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/TeXParser/TeXParser.py#L212?message=Update%20Docs)]
</div>
**LLM Docstring**

Extract a complete TeX environment, restricted to selected names when requested, validating nested occurrences and optionally returning its start offset.
  - `allowed_environments`: `object`
    > an environment-name regex or iterable of allowed names

  - `return_end_points`: `object`
    > whether to return source offsets with the parsed block

  - `:returns`: `object`
    > The parsed block or typed result structure, with endpoint metadata when requested.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/TeXParser/TeXParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/TeXParser/TeXParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/TeXParser/TeXParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/TeXParser/TeXParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/TeXParser.py#L11?message=Update%20Docs)   
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