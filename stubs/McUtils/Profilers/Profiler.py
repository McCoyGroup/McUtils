import cProfile, pstats, io, abc, sys, os
__all__ = ['BlockProfiler']

class BlockProfiler(metaclass=abc.ABCMeta):

    def __init__(self, name='Profiled Block', inactive=False, print_res=True, logger=None, print_options=None):
        """
        **LLM Docstring**

        Initialize common state for a profiling context manager.

        :param name: Label used in printed profile output.
        :type name: str
        :param inactive: Whether entering the context should skip profiling.
        :type inactive: bool
        :param print_res: Output policy: truthy values print, a writable object receives output, and `'raise'` raises the report as `ValueError`.
        :type print_res: bool | str | IO[str]
        :param logger: Optional logger exposing `log_print`.
        :type logger: Any | None
        :param print_options: Keyword arguments forwarded to `format_profile`.
        :type print_options: dict | None
        :return: Initialized profiler state.
        :rtype: BlockProfiler
        """
        ...
    profiler_modes = {}

    @classmethod
    def mode_dispatch(cls):
        """
        **LLM Docstring**

        Return the profiler-mode dispatch table.

        Built-in mappings select deterministic `cProfile` or sampling `pyinstrument`; entries from `profiler_modes` override or extend those defaults.

        :return: Mapping from mode names to profiler classes.
        :rtype: dict[str | None, type[BlockProfiler]]
        """
        ...

    @classmethod
    def profiler(cls, name='Profiled Block', print_res=True, mode=None, inactive=False, **kwargs):
        """
        Dispatcher to the various `BlockProfiler` subclasses
        """
        ...

    @abc.abstractmethod
    def start_profiler(self):
        """
        **LLM Docstring**

        Start the backend-specific profiler.

        Subclasses must implement this hook.

        :return: This abstract implementation always raises.
        :rtype: None
        :raises NotImplementedError: Always raised by the base implementation.
        """
        ...

    def __enter__(self):
        """
        **LLM Docstring**

        Start profiling when the profiler is active and not already running.

        The implementation does not explicitly return the profiler instance.

        :return: `None`.
        :rtype: None
        """
        ...

    @abc.abstractmethod
    def stop_profiler(self):
        """
        **LLM Docstring**

        Stop the backend-specific profiler and capture any required report state.

        Subclasses must implement this hook.

        :return: This abstract implementation always raises.
        :rtype: None
        :raises NotImplementedError: Always raised by the base implementation.
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Stop an active profile and optionally emit its formatted report.

        :param exc_type: Exception type raised in the managed block, if any.
        :type exc_type: type[BaseException] | None
        :param exc_val: Exception instance raised in the managed block, if any.
        :type exc_val: BaseException | None
        :param exc_tb: Associated traceback, if any.
        :type exc_tb: types.TracebackType | None
        :return: `None`; exceptions are not suppressed.
        :rtype: None
        """
        ...

    @abc.abstractmethod
    def format_profile(self, **opts):
        """
        **LLM Docstring**

        Format backend-specific profiling results.

        Subclasses must implement this hook.

        :param opts: Backend-specific formatting options.
        :type opts: Any
        :return: This abstract implementation always raises.
        :rtype: str
        :raises NotImplementedError: Always raised by the base implementation.
        """
        ...

    def print_profile(self):
        """
        **LLM Docstring**

        Format and route the profile report according to the configured output policy.

        The report is prefixed with the block name. It is raised as `ValueError` for `print_res='raise'`, written with `print` when `print_res` is file-like, sent to standard output otherwise, or passed to `logger.log_print` when a logger is configured.

        :return: `None`, unless the configured policy raises the report.
        :rtype: None
        """
        ...

class PyinstrumentBlockProfiler(BlockProfiler):

    def __init__(self, name='Profiled Block', inactive=False, print_res=True, logger=None, print_options=None, **opts):
        """
        **LLM Docstring**

        Create a sampling profiler backed by `pyinstrument.Profiler`.

        :param name: Label used in profile output.
        :type name: str
        :param inactive: Whether profiling is disabled.
        :type inactive: bool
        :param print_res: Output policy inherited from `BlockProfiler`.
        :type print_res: bool | str | IO[str]
        :param logger: Optional logger exposing `log_print`.
        :type logger: Any | None
        :param print_options: Options applied when printing the profile.
        :type print_options: dict | None
        :param opts: Options forwarded to `pyinstrument.Profiler`.
        :type opts: Any
        :return: Configured sampling profiler.
        :rtype: PyinstrumentBlockProfiler
        """
        ...

    def start_profiler(self):
        """
        **LLM Docstring**

        Start the underlying `pyinstrument` profiler.

        :return: `None`.
        :rtype: None
        """
        ...

    def stop_profiler(self):
        """
        **LLM Docstring**

        Stop the underlying `pyinstrument` profiler.

        :return: `None`.
        :rtype: None
        """
        ...

    def format_profile(self, unicode=True, color=True, **print_options):
        """
        **LLM Docstring**

        Render the `pyinstrument` session as text.

        :param unicode: Whether to use Unicode drawing characters.
        :type unicode: bool
        :param color: Whether to include terminal color codes.
        :type color: bool
        :param print_options: Additional options forwarded to `Profiler.output_text`.
        :type print_options: Any
        :return: Text representation of the captured sampling profile.
        :rtype: str
        """
        ...

class CProfileBlockProfiler(BlockProfiler):
    """
    Simple class to profile a block of code
    """

    def __init__(self, name='Profile Block', print_res=True, inactive=False, strip_dirs=None, sort_by='cumulative', num_lines=50, filter=None, logger=None):
        """
        :param name: name of profiled block
        :type name: str
        :param strip_dirs: directory paths to strip from report
        :type strip_dirs: None | Iterable[str]
        """
        ...

    def start_profiler(self):
        """
        **LLM Docstring**

        Create and enable a new deterministic `cProfile.Profile`.

        :return: `None`.
        :rtype: None
        """
        ...

    def stop_profiler(self):
        """
        **LLM Docstring**

        Disable profiling and build the textual statistics report.

        Statistics are sorted by `sort_by`; the configured filter values, when present, are passed before `num_lines` to `pstats.Stats.print_stats`. The generated text is stored in `stat_block`.

        :return: `None`.
        :rtype: None
        """
        ...

    def format_profile(self):
        """
        **LLM Docstring**

        Return the captured deterministic profile, optionally stripping path fragments.

        Each configured string in `strip_dirs` is removed with a plain string replacement.

        :return: Formatted `cProfile` statistics text.
        :rtype: str
        """
        ...