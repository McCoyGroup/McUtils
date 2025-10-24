## <a id="McUtils.Devutils.Loggers.LoggingBlock">LoggingBlock</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers.py#L45)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L45?message=Update%20Docs)]
</div>

A class that extends the utility of a logger by automatically setting up a
named block of logs that add context and can be
that







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
block_settings: list
block_level_padding: str
```
<a id="McUtils.Devutils.Loggers.LoggingBlock.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, logger, log_level=None, block_level=0, block_level_padding=None, tag=None, opener=None, prompt=None, closer=None, printoptions=None, captured_output_tag='', capture_output=True, captured_error_tag='', capture_errors=None, **tag_vars): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers.py#L64)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L64?message=Update%20Docs)]
</div>


<a id="McUtils.Devutils.Loggers.LoggingBlock.tag" class="docs-object-method">&nbsp;</a> 
```python
@property
tag(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/LoggingBlock.py#L111)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/LoggingBlock.py#L111?message=Update%20Docs)]
</div>


<a id="McUtils.Devutils.Loggers.LoggingBlock.stream_redirect" class="docs-object-method">&nbsp;</a> 
```python
stream_redirect(self, tag, base_stream): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/LoggingBlock.py#L130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/LoggingBlock.py#L130?message=Update%20Docs)]
</div>


<a id="McUtils.Devutils.Loggers.LoggingBlock.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/LoggingBlock.py#L136)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/LoggingBlock.py#L136?message=Update%20Docs)]
</div>


<a id="McUtils.Devutils.Loggers.LoggingBlock.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Loggers/LoggingBlock.py#L168)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers/LoggingBlock.py#L168?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/Loggers/LoggingBlock.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/Loggers/LoggingBlock.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/Loggers/LoggingBlock.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/Loggers/LoggingBlock.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Loggers.py#L45?message=Update%20Docs)   
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