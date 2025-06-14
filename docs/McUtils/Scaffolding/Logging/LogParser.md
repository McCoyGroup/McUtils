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


<a id="McUtils.Scaffolding.Logging.LogParser.get_block_settings" class="docs-object-method">&nbsp;</a> 
```python
get_block_settings(self, block_level): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging/LogParser.py#L28)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging/LogParser.py#L28?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.LogParser.get_block" class="docs-object-method">&nbsp;</a> 
```python
get_block(self, level=0, tag=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging/LogParser.py#L177)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging/LogParser.py#L177?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging/LogParser.py#L212)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging/LogParser.py#L212?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging/LogParser.py#L234)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging/LogParser.py#L234?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.LogParser.get_lines" class="docs-object-method">&nbsp;</a> 
```python
get_lines(self, tag=None, level=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging/LogParser.py#L248)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging/LogParser.py#L248?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.LogParser.tag_match" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
tag_match(cls, tag, tag_filter): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L262)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L262?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.LogParser.post_process_treelist" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
post_process_treelist(cls, res, combine_subtrees=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L271?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.Logging.LogParser.to_tree" class="docs-object-method">&nbsp;</a> 
```python
to_tree(self, tag_filter=None, depth=-1, combine_subtrees=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Logging/LogParser.py#L289)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Logging/LogParser.py#L289?message=Update%20Docs)]
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