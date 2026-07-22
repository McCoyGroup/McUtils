## <a id="McUtils.Profilers.Timer.Timer">Timer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer.py#L10)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer.py#L10?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
tag_printing_times: dict
default_time_format: str
default_message: str
```
<a id="McUtils.Profilers.Timer.Timer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, tag=None, file=<_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>, rounding=6, message=None, format=None, print_times=-1, number=None, globals=None, **kw): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer.py#L13)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer.py#L13?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize a reusable timing helper.

The instance can act as a context manager, a decorator, or a wrapper around `timeit.Timer`. Checkpoints are stored in a stack so nested `start`/`stop` pairs are supported, while `laps` records explicit observations made by `log`.
  - `tag`: `str | None`
    > Label included in formatted timing messages.
  - `file`: `IO[str]`
    > Text stream receiving timing messages.
  - `rounding`: `int | None`
    > Number of fractional digits used when formatting seconds.
  - `message`: `str | None`
    > Custom message template accepting `tag`, `avg`, and `tot`.
  - `format`: `str | None`
    > Custom time template accepting `hours`, `minutes`, `seconds`, `width`, and `rounding`.
  - `print_times`: `int`
    > Maximum number of messages printed for a tag; negative values disable the limit.
  - `number`: `int | None`
    > Explicit number of repetitions for `timeit`; `None` selects `autorange`.
  - `globals`: `dict | None`
    > Namespace used to execute timed callables.
  - `kw`: `Any`
    > Additional keyword arguments forwarded to `timeit.Timer` for callable timing.
  - `:returns`: `Timer`
    > A configured timer.


<a id="McUtils.Profilers.Timer.Timer.get_time_list" class="docs-object-method">&nbsp;</a> 
```python
get_time_list(self, time_elapsed): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer/Timer.py#L55)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer/Timer.py#L55?message=Update%20Docs)]
</div>
**LLM Docstring**

Decompose elapsed seconds into hours, minutes, and remaining seconds.

Minutes and hours are only promoted when the corresponding value is strictly greater than 60, matching the implementation's boundary behavior.
  - `time_elapsed`: `float`
    > Elapsed duration in seconds.
  - `:returns`: `list[int | float]`
    > Three-item list containing hours, minutes, and seconds.


<a id="McUtils.Profilers.Timer.Timer.start" class="docs-object-method">&nbsp;</a> 
```python
start(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer/Timer.py#L77)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer/Timer.py#L77?message=Update%20Docs)]
</div>
**LLM Docstring**

Push the current wall-clock timestamp onto the checkpoint stack.
  - `:returns`: `None`
    > `None`.


<a id="McUtils.Profilers.Timer.Timer.stop" class="docs-object-method">&nbsp;</a> 
```python
stop(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer/Timer.py#L88)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer/Timer.py#L88?message=Update%20Docs)]
</div>
**LLM Docstring**

Pop the latest checkpoint and return the elapsed wall-clock time.
  - `:returns`: `float`
    > Seconds elapsed since the matching `start` call.


<a id="McUtils.Profilers.Timer.Timer.log" class="docs-object-method">&nbsp;</a> 
```python
log(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer/Timer.py#L101)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer/Timer.py#L101?message=Update%20Docs)]
</div>
**LLM Docstring**

Record a lap from the current top checkpoint to the current time.

The checkpoint remains on the stack; a two-item `[start, end]` list is appended to `laps`.
  - `:returns`: `None`
    > `None`.


<a id="McUtils.Profilers.Timer.Timer.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer/Timer.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer/Timer.py#L115?message=Update%20Docs)]
</div>
**LLM Docstring**

Start timing and return this timer for context-manager use.
  - `:returns`: `Timer`
    > This timer instance.


<a id="McUtils.Profilers.Timer.Timer.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer/Timer.py#L126)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer/Timer.py#L126?message=Update%20Docs)]
</div>
**LLM Docstring**

Stop the active checkpoint, save its duration, and print the timing message.
  - `exc_type`: `type[BaseException] | None`
    > Exception type raised in the managed block, if any.
  - `exc_val`: `BaseException | None`
    > Exception instance raised in the managed block, if any.
  - `exc_tb`: `types.TracebackType | None`
    > Traceback associated with the exception, if any.
  - `:returns`: `None`
    > `None`; exceptions are not suppressed.


<a id="McUtils.Profilers.Timer.Timer.format_time" class="docs-object-method">&nbsp;</a> 
```python
format_time(self, timelist, format=None, rounding=6): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer/Timer.py#L145)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer/Timer.py#L145?message=Update%20Docs)]
</div>
**LLM Docstring**

Format an `[hours, minutes, seconds]` sequence with the configured time template.

When `rounding` is not `None`, the instance-level rounding value replaces the argument, as implemented. If rounding ultimately resolves to `None`, it is inferred from the string representation of the seconds value.
  - `timelist`: `Sequence[int | float]`
    > Hours, minutes, and seconds to format.
  - `format`: `str | None`
    > Optional replacement for the instance time template.
  - `rounding`: `int | None`
    > Requested fractional precision; a non-`None` value causes `self.rounding` to be used.
  - `:returns`: `str`
    > Formatted duration string.


<a id="McUtils.Profilers.Timer.Timer.format_timing" class="docs-object-method">&nbsp;</a> 
```python
format_timing(self, time_elapsed, *, message=None, format=None, rounding=None, tag=None, steps=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer/Timer.py#L177)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer/Timer.py#L177?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the complete timing message for a total duration and repetition count.

The method formats both the total elapsed time and the per-step average. Missing `tag`, `steps`, `message`, and `rounding` values fall back to the corresponding instance configuration, with one step used when no repetition count is available.
  - `time_elapsed`: `float`
    > Total elapsed duration in seconds.
  - `message`: `str | None`
    > Message template accepting `tag`, `avg`, and `tot`.
  - `format`: `str | None`
    > Time template passed to `format_time`.
  - `rounding`: `int | None`
    > Fractional-second precision.
  - `tag`: `str | None`
    > Label inserted into the message.
  - `steps`: `int | None`
    > Number of repetitions used to compute the average.
  - `:returns`: `str`
    > Fully formatted timing message.


<a id="McUtils.Profilers.Timer.Timer.print_timing" class="docs-object-method">&nbsp;</a> 
```python
print_timing(self, time_elapsed, tag=None, steps=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer/Timer.py#L222)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer/Timer.py#L222?message=Update%20Docs)]
</div>
**LLM Docstring**

Print a formatted timing message subject to the per-tag print limit.

Counts are shared through `Timer.tag_printing_times`. A negative `print_times` value permits unlimited output.
  - `time_elapsed`: `float`
    > Total elapsed duration in seconds.
  - `tag`: `str | None`
    > Label whose output count should be tracked.
  - `steps`: `int | None`
    > Number of repetitions used for the average.
  - `:returns`: `None`
    > `None`.


<a id="McUtils.Profilers.Timer.Timer.timeit" class="docs-object-method">&nbsp;</a> 
```python
timeit(self, stmt, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer/Timer.py#L247)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer/Timer.py#L247?message=Update%20Docs)]
</div>
**LLM Docstring**

Time a statement string or Python callable and report the result.

String statements are passed directly to `timeit.Timer`; callable inputs are installed into a namespace under generated temporary names and invoked through a generated statement. When `number` is `None`, `autorange` chooses the repetition count. Callable timing returns the value from the final invocation, while string timing returns `None` as the value.
  - `stmt`: `str | Callable`
    > Source statement or callable to benchmark.
  - `args`: `Any`
    > Positional arguments supplied to a callable statement.
  - `kwargs`: `Any`
    > Keyword arguments supplied to a callable statement.
  - `:returns`: `tuple[Any, float, int]`
    > Tuple of the final callable result (or `None`), total elapsed seconds, and repetition count.


<a id="McUtils.Profilers.Timer.Timer.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, fn): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/Timer/Timer.py#L312)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer/Timer.py#L312?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap a function so each invocation is benchmarked through `timeit`.
  - `fn`: `Callable`
    > Function to time.
  - `:returns`: `Callable`
    > Metadata-preserving wrapper that returns the final timed invocation's value.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Profilers/Timer/Timer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Profilers/Timer/Timer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Profilers/Timer/Timer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Profilers/Timer/Timer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/Timer.py#L10?message=Update%20Docs)   
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