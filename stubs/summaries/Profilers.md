### `Profiler.py`
  - **class `BlockProfiler`**
    - `__init__(name='Profiled Block', inactive=False, print_res=True, logger=None, print_options=None)`
    - `mode_dispatch()` — Built-in mappings select deterministic `cProfile` or sampling `pyinstrument`; entries from `profile…
    - `profiler(name='Profiled Block', print_res=True, mode=None, inactive=False, **kwargs)` — Dispatcher to the various `BlockProfiler` subclasses
    - `start_profiler()` — :return: This abstract implementation always raises.
    - `stop_profiler()` — Stop the backend-specific profiler and capture any required report state.
    - `format_profile(**opts)` — :return: This abstract implementation always raises.
    - `print_profile()` — Format and route the profile report according to the configured output policy.
  - **class `PyinstrumentBlockProfiler`** (BlockProfiler)
    - `__init__(name='Profiled Block', inactive=False, print_res=True, logger=None, print_options=None, **opts)`
    - `start_profiler()` — **LLM Docstring**
    - `stop_profiler()` — **LLM Docstring**
    - `format_profile(unicode=True, color=True, **print_options)` — Render the `pyinstrument` session as text.
  - **class `CProfileBlockProfiler`** (BlockProfiler)
    > Simple class to profile a block of code
    - `__init__(name='Profile Block', print_res=True, inactive=False, strip_dirs=None, sort_by='cumulative', num_lines=50, filter=None, logger=None)`
    - `start_profiler()` — Create and enable a new deterministic `cProfile.Profile`.
    - `stop_profiler()` — Disable profiling and build the textual statistics report.
    - `format_profile()` — Return the captured deterministic profile, optionally stripping path fragments.

### `Timer.py` — Provides a little timer for testing
  - **class `Timer`**
    - `__init__(tag=None, file=sys.stderr, rounding=6, message=None, format=None, print_times=-1, number=None, globals=None, **kw)`
    - `get_time_list(time_elapsed)` — Decompose elapsed seconds into hours, minutes, and remaining seconds.
    - `start()` — Push the current wall-clock timestamp onto the checkpoint stack.
    - `stop()` — Pop the latest checkpoint and return the elapsed wall-clock time.
    - `log()` — Record a lap from the current top checkpoint to the current time.
    - `format_time(timelist, format=None, rounding=6)` — Format an `[hours, minutes, seconds]` sequence with the configured time template.
    - `format_timing(time_elapsed, *, message=None, format=None, rounding=None, tag=None, steps=None)` — Build the complete timing message for a total duration and repetition count.
    - `print_timing(time_elapsed, tag=None, steps=None)` — Print a formatted timing message subject to the per-tag print limit.
    - `timeit(stmt, *args, **kwargs)` — Time a statement string or Python callable and report the result.