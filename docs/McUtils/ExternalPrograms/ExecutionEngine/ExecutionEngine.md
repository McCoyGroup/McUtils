## <a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine">ExecutionEngine</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine.py#L152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine.py#L152?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
engine_types: dict
```
<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.register" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
register(cls, name, engine=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L156?message=Update%20Docs)]
</div>
**LLM Docstring**

Register an execution-engine class by name, or return a decorator that performs the registration. Passing an engine instance uses its `name` attribute.
  - `name`: `object`
    > the registry, resource, or job name

  - `engine`: `object`
    > the execution-engine class or instance to register

  - `:returns`: `type[ExecutionEngine] | callable`
    > register an execution-engine class by name, or return a decorator that performs the registration. Passing an engine instance uses its `name` attribute.


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.resolve" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve(cls, name, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L194)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L194?message=Update%20Docs)]
</div>
**LLM Docstring**

Construct the engine class registered under `name` with the supplied options.
  - `name`: `object`
    > the registry, resource, or job name

  - `opts`: `object`
    > backend-specific construction or command options

  - `:returns`: `ExecutionEngine`
    > construct the engine class registered under `name` with the supplied options.


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine.py#L212)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine.py#L212?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize context nesting depth and retain backend-specific construction options.
  - `opts`: `object`
    > backend-specific construction or command options

  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.submit_job" class="docs-object-method">&nbsp;</a> 
```python
submit_job(self, **kwargs) -> 'ExecutionFuture': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L227)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L227?message=Update%20Docs)]
</div>
**LLM Docstring**

Abstract interface for submitting one job and returning its future.
  - `kwargs`: `object`
    > scheduler, backend, or function keyword arguments

  - `:returns`: `ExecutionFuture`
    > abstract interface for submitting one job and returning its future.


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.submit_jobs" class="docs-object-method">&nbsp;</a> 
```python
submit_jobs(self, jobs: 'list[dict]', **kwargs) -> 'ExecutionQueue': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L242)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L242?message=Update%20Docs)]
</div>
**LLM Docstring**

Submit a sequence of job-option dictionaries, overlay shared options on each entry, and return an `ExecutionQueue`.
  - `jobs`: `list[dict]`
    > per-job option dictionaries

  - `kwargs`: `object`
    > scheduler, backend, or function keyword arguments

  - `:returns`: `ExecutionQueue`
    > submit a sequence of job-option dictionaries, overlay shared options on each entry, and return an `ExecutionQueue`.


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L262)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L262?message=Update%20Docs)]
</div>
**LLM Docstring**

Increase the context nesting depth and call `startup` only on the outermost entry.
  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L276)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L276?message=Update%20Docs)]
</div>
**LLM Docstring**

Decrease the context nesting depth and call `shutdown` after leaving the outermost context.
  - `exc_type`: `object`
    > the exception class leaving the context

  - `exc_val`: `object`
    > the exception instance leaving the context

  - `exc_tb`: `object`
    > the exception traceback leaving the context

  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.startup" class="docs-object-method">&nbsp;</a> 
```python
startup(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L298)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L298?message=Update%20Docs)]
</div>
**LLM Docstring**

No-op lifecycle hook intended for engines that must acquire backend resources.
  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.ExternalPrograms.ExecutionEngine.ExecutionEngine.shutdown" class="docs-object-method">&nbsp;</a> 
```python
shutdown(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L309)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.py#L309?message=Update%20Docs)]
</div>
**LLM Docstring**

No-op lifecycle hook intended for engines that must release backend resources.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ExecutionEngine/ExecutionEngine.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ExecutionEngine.py#L152?message=Update%20Docs)   
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