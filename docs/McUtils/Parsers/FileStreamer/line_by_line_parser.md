# <a id="McUtils.Parsers.FileStreamer.line_by_line_parser">line_by_line_parser</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/FileStreamer.py#L2347)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer.py#L2347?message=Update%20Docs)]
</div>

```python
line_by_line_parser(source, parse, handle_block=None, binary=False, **opts): 
```
Convenience factory that dispatches to the right `Functional*LineByLineReader`
based on the type of `source` (a string, a file/path, or bytes).
  - `source`: `Any`
    > a string, an open file/file path, or a bytes object to parse
  - `parse`: `Any`
    > `parse(line, depth=0, active_tag=None, label=None, history=None) -> (tag, data)`
  - `handle_block`: `Any`
    > optional `handle_block(label, block, depth) -> block`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/FileStreamer/line_by_line_parser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/FileStreamer/line_by_line_parser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/FileStreamer/line_by_line_parser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/FileStreamer/line_by_line_parser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer.py#L2347?message=Update%20Docs)   
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