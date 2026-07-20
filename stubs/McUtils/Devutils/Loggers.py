import os, enum, weakref, sys
from . import Redirects as redirects
__all__ = ['Logger', 'NullLogger', 'LogLevel', 'LoggingBlock']

class LogLevel(enum.Enum):
    """
    A simple log level object to standardize more pieces of the logger interface
    """
    'Real access pattern: LogLevel.<MemberName> (this is an enum with 7 members, e.g. LogLevel.Quiet == 0). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:'
    _MEMBERS = {'Quiet': 0, 'Warnings': 1, 'Normal': 10, 'Debug': 50, 'MoreDebug': 75, 'All': 100, 'Never': 1000}

    def __eq__(self, other):
        """
        **LLM Docstring**

        Compare the log level against another level or a raw numeric value (`==`).

        :param other: the level or number to compare against
        :return: the comparison result
        :rtype: bool
        """
        ...

    def __le__(self, other):
        """
        **LLM Docstring**

        Compare the log level against another level or a raw numeric value (`<=`).

        :param other: the level or number to compare against
        :return: the comparison result
        :rtype: bool
        """
        ...

    def __ge__(self, other):
        """
        **LLM Docstring**

        Compare the log level against another level or a raw numeric value (`>=`).

        :param other: the level or number to compare against
        :return: the comparison result
        :rtype: bool
        """
        ...

    def __lt__(self, other):
        """
        **LLM Docstring**

        Compare the log level against another level or a raw numeric value (`<`).

        :param other: the level or number to compare against
        :return: the comparison result
        :rtype: bool
        """
        ...

    def __gt__(self, other):
        """
        **LLM Docstring**

        Compare the log level against another level or a raw numeric value (`>`).

        :param other: the level or number to compare against
        :return: the comparison result
        :rtype: bool
        """
        ...

class LoggingBlock:
    """
    A class that extends the utility of a logger by automatically setting up a
    named block of logs that add context and can be
    that
    """
    block_level_padding = ' ' * 2

    def __init__(self, logger, log_level=None, block_level=0, block_level_padding=None, tag=None, opener=None, prompt=None, closer=None, printoptions=None, captured_output_tag='', capture_output=True, captured_error_tag='', capture_errors=None, **tag_vars):
        """
        **LLM Docstring**

        Set up a nested, tagged block of log output with its own verbosity, prompt, and
        optional stdout/stderr capture.

        :param logger: the owning logger
        :type logger: Logger
        :param log_level: the block's verbosity (defaults to the logger's)
        :param block_level: the nesting depth (selects the opener/prompt/closer style)
        :type block_level: int
        :param block_level_padding: the per-level indentation
        :param tag: the block tag (string, `(template, vars)`, or callable)
        :param opener: an explicit opener line
        :param prompt: an explicit per-line prompt
        :param closer: an explicit closer line
        :param printoptions: numpy print options to apply within the block
        :type printoptions: dict | None
        :param captured_output_tag: tag prefix for captured stdout
        :type captured_output_tag: str
        :param capture_output: capture stdout within the block
        :type capture_output: bool
        :param captured_error_tag: tag prefix for captured stderr
        :type captured_error_tag: str
        :param capture_errors: capture stderr (defaults to `capture_output`)
        :type capture_errors: bool | None
        :param tag_vars: variables used to format the tag
        """
        ...

    @property
    def tag(self):
        """
        **LLM Docstring**

        The resolved (formatted) block tag, computed lazily from a string, a
        `(template, vars)` pair, or a callable.

        :return: the tag string
        :rtype: str
        """
        ...

    @classmethod
    def _print_capturing(cls, logger, tag, base_stream):
        """
        **LLM Docstring**

        Build a `print`-like callback that routes captured output through the logger
        (falling back to the base stream while a log print is already in progress).

        :param logger: the logger to route through
        :type logger: Logger
        :param tag: the tag prefix for captured lines
        :type tag: str
        :param base_stream: the underlying stream
        :return: the capturing print callback
        :rtype: Callable
        """
        ...

    def stream_redirect(self, tag, base_stream):
        """
        **LLM Docstring**

        Build a `StreamRedirect` that routes writes through the logger with the given
        tag.

        :param tag: the tag prefix
        :type tag: str
        :param base_stream: the underlying stream
        :return: the stream redirect
        :rtype: redirects.StreamRedirect
        """
        ...
    _redirect_capture_manager_stack = []

    def __enter__(self):
        """
        **LLM Docstring**

        Open the block: print the opener, start output capture (if enabled and none is
        already active), raise the logger's prompt/verbosity/nesting, and apply any
        numpy print options.
        """
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close the block: stop output capture, print the closer, and restore the
        logger's prompt, verbosity, and nesting.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        ...

class Logger:
    """
    Defines a simple logger object to write log data to a file based on log levels.
    """
    LogLevel = LogLevel
    _loggers = weakref.WeakValueDictionary()
    default_verbosity = LogLevel.Normal

    def __init__(self, log_file=None, log_level=None, print_function=None, padding='', newline='\n', repad_messages=True, block_options=None):
        """
        **LLM Docstring**

        Set up a logger that writes to a file (or stdout) based on log levels.

        :param log_file: the log file path (stdout if omitted)
        :type log_file: str | None
        :param log_level: the verbosity threshold
        :param print_function: the print callable (defaults to `print`)
        :type print_function: Callable | None
        :param padding: the per-line prefix padding
        :type padding: str
        :param newline: the newline string
        :type newline: str
        :param repad_messages: re-pad newlines within message arguments
        :type repad_messages: bool
        :param block_options: default options for `block`
        :type block_options: dict | None
        """
        ...

    def to_state(self, serializer=None):
        """
        **LLM Docstring**

        Return the serializable state of the logger (dropping the print function when
        it's the builtin `print`).

        :param serializer: an optional serializer
        :return: the state dict
        :rtype: dict
        """
        ...

    @classmethod
    def from_state(cls, state, serializer=None):
        """
        **LLM Docstring**

        Rebuild a logger from its serialized state.

        :param state: the state dict
        :type state: dict
        :param serializer: an optional serializer
        :return: the logger
        :rtype: Logger
        """
        ...

    def block(self, **kwargs):
        """
        **LLM Docstring**

        Open a nested logging block on this logger.

        :param kwargs: options forwarded to `LoggingBlock` (merged with the defaults)
        :return: the logging block
        :rtype: LoggingBlock
        """
        ...

    def register(self, key):
        """
        Registers the logger under the given key
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def lookup(cls, key, construct=False):
        """
        Looks up a logger. Has the convenient, but potentially surprising
        behavior that if no logger is found a `NullLogger` is returned.
        :param key:
        :type key:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def preformat_keys(key_functions):
        """
        Generates a closure that will take the supplied
        keys/function pairs and update them appropriately

        :param key_functions:
        :type key_functions:
        :return:
        :rtype:
        """
        ...

    def format_message(self, message, *params, preformatter=None, _repad=None, _newline=None, _padding=None, **kwargs):
        """
        **LLM Docstring**

        Format a message template with the given parameters, optionally running a
        preformatter over the arguments and re-padding multi-line string arguments.

        :param message: the message template
        :type message: str
        :param params: positional format arguments
        :param preformatter: a callable transforming the arguments first
        :type preformatter: Callable | None
        :param _repad: re-pad newlines in string arguments
        :type _repad: bool | None
        :param _newline: the newline override
        :param _padding: the padding override
        :param kwargs: keyword format arguments
        :return: the formatted message
        :rtype: str
        """
        ...

    def format_metainfo(self, metainfo):
        """
        **LLM Docstring**

        Format block meta-information as a JSON string (or empty string when absent).

        :param metainfo: the meta-information
        :return: the formatted meta string
        :rtype: str
        """
        ...

    def pad_newlines(self, obj, padding=None, newline=None, **kwargs):
        """
        **LLM Docstring**

        Replace newlines in a value with the newline-plus-padding prefix so multi-line
        output stays aligned under the current prompt.

        :param obj: the value (coerced to a string)
        :param padding: the padding (defaults to the logger's)
        :param newline: the newline (defaults to the logger's)
        :param kwargs: variables used to format the prefix
        :return: the re-padded string
        :rtype: str
        """
        ...

    @staticmethod
    def split_lines(obj):
        """
        **LLM Docstring**

        Split a value's string form into lines.

        :param obj: the value
        :return: the lines
        :rtype: list[str]
        """
        ...

    @staticmethod
    def prep_array(obj):
        """
        **LLM Docstring**

        Render a numpy array to lines without truncation (wide/high print limits).

        :param obj: the array
        :return: the rendered lines
        :rtype: list[str]
        """
        ...

    @staticmethod
    def prep_dict(obj):
        """
        **LLM Docstring**

        Render a dict as `key: value` lines.

        :param obj: the dict
        :return: the rendered lines
        :rtype: list[str]
        """
        ...

    def log_print(self, message, *messrest, message_prepper=None, padding=None, newline=None, log_level=None, metainfo=None, print_function=None, print_options=None, sep=None, end=None, file=None, flush=None, preformatter=None, **kwargs):
        """
        :param message: message to print
        :type message: str | Iterable[str]
        :param params:
        :type params:
        :param print_options: options to be passed through to print
        :type print_options:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        ...
    _in_log_print = False

    @classmethod
    def _print_message(cls, print_function, msg, log, print_options):
        """
        **LLM Docstring**

        Actually emit a formatted message: to a log file (creating its directory),
        to stdout, or to a supplied stream, guarding against re-entrant log prints.

        :param print_function: the print callable
        :type print_function: Callable
        :param msg: the formatted message
        :type msg: str
        :param log: the log file path, `None` (stdout), or a stream
        :param print_options: options passed to the print callable
        :type print_options: dict
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the log file and verbosity.

        :return: the representation
        :rtype: str
        """
        ...

class NullLogger(Logger):
    """
    A logger that implements the interface, but doesn't ever print.
    Allows code to avoid a bunch of "if logger is not None" blocks
    """

    def __init__(self, *log_files, **logger_opts):
        """
        **LLM Docstring**

        A logger that implements the interface but never prints (so callers can avoid
        `if logger is not None` checks).

        :param log_files: forwarded to `Logger`
        :param logger_opts: forwarded to `Logger`
        """
        ...

    def log_print(self, message, *params, print_options=None, padding=None, newline=None, **kwargs):
        """
        **LLM Docstring**

        No-op: discards the message.

        :param message: the (ignored) message
        :param params: ignored positional arguments
        :param print_options: ignored
        :param padding: ignored
        :param newline: ignored
        :param kwargs: ignored
        """
        ...

    def __bool__(self):
        """
        **LLM Docstring**

        A null logger is always falsy.

        :return: `False`
        :rtype: bool
        """
        ...

    def block(self, capture_output=False, **kwargs):
        """
        **LLM Docstring**

        Open a logging block with output capture disabled by default.

        :param capture_output: capture stdout/stderr (off by default)
        :type capture_output: bool
        :param kwargs: options forwarded to `Logger.block`
        :return: the logging block
        :rtype: LoggingBlock
        """
        ...