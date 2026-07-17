## <a id="McUtils.Parsers.FileStreamer.FileStreamerTag">FileStreamerTag</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/FileStreamer.py#L1776)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer.py#L1776?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Parsers.FileStreamer.FileStreamerTag.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, tag_alternatives=None, follow_ups=None, offset=None, direction='forward', skip_tag=True, seek=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/FileStreamer.py#L1777)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer.py#L1777?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize one or more alternative delimiters plus optional follow-up delimiters, offset, direction, skip, and seek behavior into a tag specification.
  - `tag_alternatives`: `object`
    > one delimiter or a collection of alternative delimiters

  - `follow_ups`: `object`
    > additional delimiters that must be located in sequence after the first tag

  - `offset`: `object`
    > an additional cursor displacement applied after a match

  - `direction`: `object`
    > the direction in which delimiters are searched

  - `skip_tag`: `object`
    > whether the returned position should lie after the matched delimiter

  - `seek`: `object`
    > whether finding a delimiter should move the stream cursor


<a id="McUtils.Parsers.FileStreamer.FileStreamerTag.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/FileStreamer/FileStreamerTag.py#L1819)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer/FileStreamerTag.py#L1819?message=Update%20Docs)]
</div>
**LLM Docstring**

Show the configured tag alternatives and the skip/seek flags.
  - `:returns`: `str`
    > The regex source or textual representation constructed by the operation.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/FileStreamer/FileStreamerTag.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/FileStreamer/FileStreamerTag.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/FileStreamer/FileStreamerTag.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/FileStreamer/FileStreamerTag.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/FileStreamer.py#L1776?message=Update%20Docs)   
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