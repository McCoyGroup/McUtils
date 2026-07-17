## <a id="McUtils.Parsers.TeXParser.BibTeXParser">BibTeXParser</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/TeXParser.py#L387)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/TeXParser.py#L387?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_binary: bool
```
<a id="McUtils.Parsers.TeXParser.BibTeXParser.is_valid_tex_block" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_valid_tex_block(cls, block: str): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L389)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L389?message=Update%20Docs)]
</div>
**LLM Docstring**

Accept a BibTeX entry block when the consumed opening brace leaves one more closing brace than opening braces.
  - `block`: `str`
    > the candidate TeX or BibTeX source block

  - `:returns`: `bool`
    > `True` when the condition described above holds; otherwise `False`.


<a id="McUtils.Parsers.TeXParser.BibTeXParser.is_valid_stream_start" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
is_valid_stream_start(cls, tag_str): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L405)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L405?message=Update%20Docs)]
</div>
**LLM Docstring**

Compile the entry-start pattern once and full-match candidate strings such as `@article{`.
  - `tag_str`: `object`
    > a candidate command or entry-start tag

  - `:returns`: `object`
    > compile the entry-start pattern once and full-match candidate strings such as `@article{`.


<a id="McUtils.Parsers.TeXParser.BibTeXParser.parse_bib_item" class="docs-object-method">&nbsp;</a> 
```python
parse_bib_item(self, allowed_items=None, return_end_points=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/TeXParser/BibTeXParser.py#L457)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/TeXParser/BibTeXParser.py#L457?message=Update%20Docs)]
</div>
**LLM Docstring**

Extract one complete balanced BibTeX entry, optionally restricting the accepted entry types and returning source endpoints.
  - `allowed_items`: `object`
    > entry-type names accepted while parsing BibTeX

  - `return_end_points`: `object`
    > whether to return source offsets with the parsed block

  - `:returns`: `object`
    > The parsed block or typed result structure, with endpoint metadata when requested.


<a id="McUtils.Parsers.TeXParser.BibTeXParser.parse_bib_body" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_bib_body(self, text, allowed_fields=None, parse_lines=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L494)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L494?message=Update%20Docs)]
</div>
**LLM Docstring**

Parse an entry string into its type, citation key, header endpoints, and a mapping from field names to `(endpoints, original_assignment_text)` records; field parsing can be disabled.
  - `text`: `object`
    > the complete BibTeX entry text

  - `allowed_fields`: `object`
    > field names accepted while parsing a BibTeX entry

  - `parse_lines`: `object`
    > whether individual BibTeX fields are parsed after the header

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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/TeXParser/BibTeXParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/TeXParser/BibTeXParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/TeXParser/BibTeXParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/TeXParser/BibTeXParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/TeXParser.py#L387?message=Update%20Docs)   
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