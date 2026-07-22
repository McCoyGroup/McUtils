## <a id="McUtils.Profilers.Profiler.BlockProfiler">BlockProfiler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Profiler.py#L9)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Profiler.py#L9?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
profiler_modes: dict
```
<a id="McUtils.Profilers.Profiler.BlockProfiler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name='Profiled Block', inactive=False, print_res=True, logger=None, print_options=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Profiler.py#L10)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Profiler.py#L10?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize common state for a profiling context manager.
  - `name`: `str`
    > Label used in printed profile output.
  - `inactive`: `bool`
    > Whether entering the context should skip profiling.
  - `print_res`: `bool | str | IO[str]`
    > Output policy: truthy values print, a writable object receives output, and `'raise'` raises the report as `ValueError`.
  - `logger`: `Any | None`
    > Optional logger exposing `log_print`.
  - `print_options`: `dict | None`
    > Keyword arguments forwarded to `format_profile`.
  - `:returns`: `BlockProfiler`
    > Initialized profiler state.


<a id="McUtils.Profilers.Profiler.BlockProfiler.mode_dispatch" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
mode_dispatch(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L37)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L37?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the profiler-mode dispatch table.

Built-in mappings select deterministic `cProfile` or sampling `pyinstrument`; entries from `profiler_modes` override or extend those defaults.
  - `:returns`: `dict[str | None, type[BlockProfiler]]`
    > Mapping from mode names to profiler classes.


<a id="McUtils.Profilers.Profiler.BlockProfiler.profiler" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
profiler(cls, name='Profiled Block', print_res=True, mode=None, inactive=False, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L55)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L55?message=Update%20Docs)]
</div>
Dispatcher to the various `BlockProfiler` subclasses


<a id="McUtils.Profilers.Profiler.BlockProfiler.start_profiler" class="docs-object-method">&nbsp;</a> 
```python
start_profiler(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Profiler/BlockProfiler.py#L72)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Profiler/BlockProfiler.py#L72?message=Update%20Docs)]
</div>
**LLM Docstring**

Start the backend-specific profiler.

Subclasses must implement this hook.
  - `:returns`: `None`
    > This abstract implementation always raises.


<a id="McUtils.Profilers.Profiler.BlockProfiler.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Profiler/BlockProfiler.py#L86)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Profiler/BlockProfiler.py#L86?message=Update%20Docs)]
</div>
**LLM Docstring**

Start profiling when the profiler is active and not already running.

The implementation does not explicitly return the profiler instance.
  - `:returns`: `None`
    > `None`.


<a id="McUtils.Profilers.Profiler.BlockProfiler.stop_profiler" class="docs-object-method">&nbsp;</a> 
```python
stop_profiler(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Profiler/BlockProfiler.py#L101)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Profiler/BlockProfiler.py#L101?message=Update%20Docs)]
</div>
**LLM Docstring**

Stop the backend-specific profiler and capture any required report state.

Subclasses must implement this hook.
  - `:returns`: `None`
    > This abstract implementation always raises.


<a id="McUtils.Profilers.Profiler.BlockProfiler.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Profiler/BlockProfiler.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Profiler/BlockProfiler.py#L115?message=Update%20Docs)]
</div>
**LLM Docstring**

Stop an active profile and optionally emit its formatted report.
  - `exc_type`: `type[BaseException] | None`
    > Exception type raised in the managed block, if any.
  - `exc_val`: `BaseException | None`
    > Exception instance raised in the managed block, if any.
  - `exc_tb`: `types.TracebackType | None`
    > Associated traceback, if any.
  - `:returns`: `None`
    > `None`; exceptions are not suppressed.


<a id="McUtils.Profilers.Profiler.BlockProfiler.format_profile" class="docs-object-method">&nbsp;</a> 
```python
format_profile(self, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Profiler/BlockProfiler.py#L135)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Profiler/BlockProfiler.py#L135?message=Update%20Docs)]
</div>
**LLM Docstring**

Format backend-specific profiling results.

Subclasses must implement this hook.
  - `opts`: `Any`
    > Backend-specific formatting options.
  - `:returns`: `str`
    > This abstract implementation always raises.


<a id="McUtils.Profilers.Profiler.BlockProfiler.print_profile" class="docs-object-method">&nbsp;</a> 
```python
print_profile(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Profiler/BlockProfiler.py#L151)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Profiler/BlockProfiler.py#L151?message=Update%20Docs)]
</div>
**LLM Docstring**

Format and route the profile report according to the configured output policy.

The report is prefixed with the block name. It is raised as `ValueError` for `print_res='raise'`, written with `print` when `print_res` is file-like, sent to standard output otherwise, or passed to `logger.log_print` when a logger is configured.
  - `:returns`: `None`
    > `None`, unless the configured policy raises the report.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Profilers/Profiler/BlockProfiler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Profilers/Profiler/BlockProfiler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Profilers/Profiler/BlockProfiler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Profilers/Profiler/BlockProfiler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Profiler.py#L9?message=Update%20Docs)   
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