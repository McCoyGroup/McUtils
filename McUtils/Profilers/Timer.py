"""Provides a little timer for testing

"""
import timeit, functools, time, sys, inspect
import uuid
from collections import deque

__all__ = ["Timer"]

class Timer:

    tag_printing_times = {}
    def __init__(self, tag=None, file=sys.stderr, rounding=6, message=None, format=None, print_times=-1, number=None, globals=None, **kw):
        """
        **LLM Docstring**

        Initialize a reusable timing helper.

        The instance can act as a context manager, a decorator, or a wrapper around `timeit.Timer`. Checkpoints are stored in a stack so nested `start`/`stop` pairs are supported, while `laps` records explicit observations made by `log`.

        :param tag: Label included in formatted timing messages.
        :type tag: str | None
        :param file: Text stream receiving timing messages.
        :type file: IO[str]
        :param rounding: Number of fractional digits used when formatting seconds.
        :type rounding: int | None
        :param message: Custom message template accepting `tag`, `avg`, and `tot`.
        :type message: str | None
        :param format: Custom time template accepting `hours`, `minutes`, `seconds`, `width`, and `rounding`.
        :type format: str | None
        :param print_times: Maximum number of messages printed for a tag; negative values disable the limit.
        :type print_times: int
        :param number: Explicit number of repetitions for `timeit`; `None` selects `autorange`.
        :type number: int | None
        :param globals: Namespace used to execute timed callables.
        :type globals: dict | None
        :param kw: Additional keyword arguments forwarded to `timeit.Timer` for callable timing.
        :type kw: Any
        :return: A configured timer.
        :rtype: Timer
        """
        self.kw = kw
        self.number = number
        self.file = file
        self.tag = tag
        self.message = message
        self.format = format
        self.rounding = rounding
        self.checkpoints = deque()
        self.print_times = print_times
        self.latest = None
        self.globals = globals
        self.laps = []

    def get_time_list(self, time_elapsed):
        """
        **LLM Docstring**

        Decompose elapsed seconds into hours, minutes, and remaining seconds.

        Minutes and hours are only promoted when the corresponding value is strictly greater than 60, matching the implementation's boundary behavior.

        :param time_elapsed: Elapsed duration in seconds.
        :type time_elapsed: float
        :return: Three-item list containing hours, minutes, and seconds.
        :rtype: list[int | float]
        """
        run_time = [0, 0, time_elapsed]
        if run_time[2] > 60:
            run_time[1] = int(run_time[2] / 60)
            run_time[2] = run_time[2] % 60
            if run_time[1] > 60:
                run_time[0] = int(run_time[1] / 60)
                run_time[1] = run_time[1] % 60
        return run_time

    def start(self):
        """
        **LLM Docstring**

        Push the current wall-clock timestamp onto the checkpoint stack.

        :return: `None`.
        :rtype: None
        """
        self.checkpoints.append(time.time())

    def stop(self):
        """
        **LLM Docstring**

        Pop the latest checkpoint and return the elapsed wall-clock time.

        :return: Seconds elapsed since the matching `start` call.
        :rtype: float
        """
        t = time.time()
        cp = self.checkpoints.pop()
        return t - cp

    def log(self):
        """
        **LLM Docstring**

        Record a lap from the current top checkpoint to the current time.

        The checkpoint remains on the stack; a two-item `[start, end]` list is appended to `laps`.

        :return: `None`.
        :rtype: None
        """
        t = time.time()
        self.laps.append([self.checkpoints[-1], t])

    def __enter__(self):
        """
        **LLM Docstring**

        Start timing and return this timer for context-manager use.

        :return: This timer instance.
        :rtype: Timer
        """
        self.start()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Stop the active checkpoint, save its duration, and print the timing message.

        :param exc_type: Exception type raised in the managed block, if any.
        :type exc_type: type[BaseException] | None
        :param exc_val: Exception instance raised in the managed block, if any.
        :type exc_val: BaseException | None
        :param exc_tb: Traceback associated with the exception, if any.
        :type exc_tb: types.TracebackType | None
        :return: `None`; exceptions are not suppressed.
        :rtype: None
        """
        self.latest = self.stop()
        self.print_timing(self.latest)

    default_time_format = "{hours}:{minutes:0>2}:{seconds:0>{width}.{rounding}f}"
    def format_time(self, timelist, format=None, rounding=6):
        """
        **LLM Docstring**

        Format an `[hours, minutes, seconds]` sequence with the configured time template.

        When `rounding` is not `None`, the instance-level rounding value replaces the argument, as implemented. If rounding ultimately resolves to `None`, it is inferred from the string representation of the seconds value.

        :param timelist: Hours, minutes, and seconds to format.
        :type timelist: Sequence[int | float]
        :param format: Optional replacement for the instance time template.
        :type format: str | None
        :param rounding: Requested fractional precision; a non-`None` value causes `self.rounding` to be used.
        :type rounding: int | None
        :return: Formatted duration string.
        :rtype: str
        """
        if format is None:
            format = self.format
        if format is None:
            format = self.default_time_format
        if rounding is not None:
            rounding = self.rounding
        if rounding is None:
            rounding = len(str(timelist[-1])) - len(str(int(timelist[-1]))) + 1
        return format.format(hours=timelist[0], minutes=timelist[1], seconds=timelist[2],
                          width=rounding+3,
                          rounding=rounding
                          )


    default_message = "{tag}: took {avg} per loop with {tot} overall"
    def format_timing(self, time_elapsed, *, message=None, format=None, rounding=None, tag=None, steps=None):
        """
        **LLM Docstring**

        Build the complete timing message for a total duration and repetition count.

        The method formats both the total elapsed time and the per-step average. Missing `tag`, `steps`, `message`, and `rounding` values fall back to the corresponding instance configuration, with one step used when no repetition count is available.

        :param time_elapsed: Total elapsed duration in seconds.
        :type time_elapsed: float
        :param message: Message template accepting `tag`, `avg`, and `tot`.
        :type message: str | None
        :param format: Time template passed to `format_time`.
        :type format: str | None
        :param rounding: Fractional-second precision.
        :type rounding: int | None
        :param tag: Label inserted into the message.
        :type tag: str | None
        :param steps: Number of repetitions used to compute the average.
        :type steps: int | None
        :return: Fully formatted timing message.
        :rtype: str
        """
        run_time = self.get_time_list(time_elapsed)
        if tag is None:
            tag = self.tag
        if steps is None:
            steps = self.number
        if steps is None:
            steps = 1
        run_time_averaged = self.get_time_list(time_elapsed / steps)
        if message is None:
            message = self.message
        if message is None:
            message = self.default_message
        if rounding is None:
            rounding = self.rounding
        run_time_averaged = self.format_time(run_time_averaged, format=format, rounding=rounding)
        run_time = self.format_time(run_time, format=format, rounding=rounding)
        return message.format(
            tag=tag,
            avg=run_time_averaged,
            tot=run_time
        )

    def print_timing(self, time_elapsed, tag=None, steps=None):
        """
        **LLM Docstring**

        Print a formatted timing message subject to the per-tag print limit.

        Counts are shared through `Timer.tag_printing_times`. A negative `print_times` value permits unlimited output.

        :param time_elapsed: Total elapsed duration in seconds.
        :type time_elapsed: float
        :param tag: Label whose output count should be tracked.
        :type tag: str | None
        :param steps: Number of repetitions used for the average.
        :type steps: int | None
        :return: `None`.
        :rtype: None
        """
        if tag is None:
            tag = self.tag
        if tag not in self.tag_printing_times:
            self.tag_printing_times[tag] = 0
        if self.print_times < 0 or self.tag_printing_times[tag] < self.print_times:
            print(self.format_timing(time_elapsed, tag=tag, steps=steps), file=self.file)
            self.tag_printing_times[tag] += 1

    def timeit(self, stmt, *args, **kwargs):
        """
        **LLM Docstring**

        Time a statement string or Python callable and report the result.

        String statements are passed directly to `timeit.Timer`; callable inputs are installed into a namespace under generated temporary names and invoked through a generated statement. When `number` is `None`, `autorange` chooses the repetition count. Callable timing returns the value from the final invocation, while string timing returns `None` as the value.

        :param stmt: Source statement or callable to benchmark.
        :type stmt: str | Callable
        :param args: Positional arguments supplied to a callable statement.
        :type args: Any
        :param kwargs: Keyword arguments supplied to a callable statement.
        :type kwargs: Any
        :return: Tuple of the final callable result (or `None`), total elapsed seconds, and repetition count.
        :rtype: tuple[Any, float, int]
        """
        globals = self.globals
        val = None
        number = self.number
        tag = self.tag
        id = "_" + str(uuid.uuid4()).replace("-", "_")
        if isinstance(stmt, str):
            if globals is None:
                globals = inspect.stack(1)[0].frame.f_locals
            timer = timeit.Timer(stmt)
            if tag is None:
                if hasattr(stmt, '__name__'):
                    tag = stmt.__name__
                else:
                    tag = str(stmt)
        else:
            if globals is None:
                try:
                    globals = stmt.__globals__
                except AttributeError:
                    globals = inspect.stack(1)[0].frame.f_locals

            globals[f'_{id}_func'] = stmt
            globals[f'_{id}_args'] = args
            globals[f'_{id}_kwargs'] = kwargs
            timer = timeit.Timer(
                f"""
global _{id}_val
_{id}_val = _{id}_func(*_{id}_args, **_{id}_kwargs)
""", globals=globals,
                **self.kw
            )
            if tag is None:
                if hasattr(stmt, '__name__'):
                    tag = stmt.__name__
                else:
                    tag = str(stmt)

        if number is None:
            number, elapsed_time = timer.autorange()
        else:
            elapsed_time = timer.timeit(number)

        if not isinstance(stmt, str):
            val = globals[f"_{id}_val"]

        self.print_timing(elapsed_time, steps=number, tag=tag)
        return val, elapsed_time, number

    def __call__(self, fn): # for use as a decorator
        """
        **LLM Docstring**

        Wrap a function so each invocation is benchmarked through `timeit`.

        :param fn: Function to time.
        :type fn: Callable
        :return: Metadata-preserving wrapper that returns the final timed invocation's value.
        :rtype: Callable
        """
        @functools.wraps(fn)
        def timed_fn(*args, **kwargs):
            """
            **LLM Docstring**

            Time one decorated function call and return the value from its final repetition.

            :param args: Positional arguments forwarded to the decorated function.
            :type args: Any
            :param kwargs: Keyword arguments forwarded to the decorated function.
            :type kwargs: Any
            :return: Value produced by the last timed invocation.
            :rtype: Any
            """
            return self.timeit(fn, *args, **kwargs)[0]
        return timed_fn