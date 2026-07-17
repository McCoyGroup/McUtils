## <a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionQueue">ExecutionQueue</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine.py#L118)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine.py#L118?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionQueue.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, futures: 'list[ExecutionFuture]'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine.py#L119)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine.py#L119?message=Update%20Docs)]
</div>
**LLM Docstring**

Store the execution futures that form a logical submission batch.
  - `futures`: `list[ExecutionFuture]`
    > the futures included in the queue

  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionQueue.join" class="docs-object-method">&nbsp;</a> 
```python
join(self, timeout=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionQueue.py#L132)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionQueue.py#L132?message=Update%20Docs)]
</div>
**LLM Docstring**

Join each future sequentially while deducting elapsed time from a shared timeout budget.
  - `timeout`: `object`
    > maximum seconds to wait, or `None` for no deadline

  - `:returns`: `None`
    > No value is returned.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ExecutionEngine/ExecutionQueue.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ExecutionEngine/ExecutionQueue.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ExecutionEngine/ExecutionQueue.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ExecutionEngine/ExecutionQueue.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine.py#L118?message=Update%20Docs)   
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