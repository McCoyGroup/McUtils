import os, enum, weakref, sys
from . import Redirects as redirects

__all__ = [
    "Logger",
    "NullLogger",
    "LogLevel",
    "LoggingBlock"
]


class LogLevel(enum.Enum):
    """
    A simple log level object to standardize more pieces of the logger interface
    """
    Quiet = 0
    Warnings = 1
    Normal = 10
    Debug = 50
    MoreDebug = 75
    All = 100
    Never = 1000 # for debug statements that should really be deleted but I'm too lazy to

    def __eq__(self, other):
        """
        **LLM Docstring**

        Compare the log level against another level or a raw numeric value (`==`).

        :param other: the level or number to compare against
        :return: the comparison result
        :rtype: bool
        """
        if isinstance(other, LogLevel):
            other = other.value
        return self.value == other
    def __le__(self, other):
        """
        **LLM Docstring**

        Compare the log level against another level or a raw numeric value (`<=`).

        :param other: the level or number to compare against
        :return: the comparison result
        :rtype: bool
        """
        if isinstance(other, LogLevel):
            other = other.value
        return self.value <= other
    def __ge__(self, other):
        """
        **LLM Docstring**

        Compare the log level against another level or a raw numeric value (`>=`).

        :param other: the level or number to compare against
        :return: the comparison result
        :rtype: bool
        """
        if isinstance(other, LogLevel):
            other = other.value
        return self.value >= other
    def __lt__(self, other):
        """
        **LLM Docstring**

        Compare the log level against another level or a raw numeric value (`<`).

        :param other: the level or number to compare against
        :return: the comparison result
        :rtype: bool
        """
        if isinstance(other, LogLevel):
            other = other.value
        return self.value < other
    def __gt__(self, other):
        """
        **LLM Docstring**

        Compare the log level against another level or a raw numeric value (`>`).

        :param other: the level or number to compare against
        :return: the comparison result
        :rtype: bool
        """
        if isinstance(other, LogLevel):
            other = other.value
        return self.value > other

class LoggingBlock:
    """
    A class that extends the utility of a logger by automatically setting up a
    named block of logs that add context and can be
    that
    """
    block_settings = [
        {
            'opener': ">>" + "-" * 25 + ' {tag} ' + "-" * 25,
            'prompt': "::{meta} ",
            'closer': '>>'+'-'*50+'<<'
        },
        {
            'opener': "::> {tag}",
            'prompt': "  >{meta} ",
            'closer': '<::'
        }
    ]
    block_level_padding= " " * 2
    def __init__(self,
                 logger,
                 log_level=None,
                 block_level=0,
                 block_level_padding=None,
                 tag=None,
                 opener=None,
                 prompt=None,
                 closer=None,
                 printoptions=None,
                 captured_output_tag="",
                 capture_output=True,
                 captured_error_tag="",
                 capture_errors=None,
                 **tag_vars
                 ):
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
        self.logger = logger
        if block_level_padding is None:
            block_level_padding = self.block_level_padding
        if block_level >= len(self.block_settings):
            padding = block_level_padding * (block_level - len(self.block_settings) + 1)
            settings = {k: padding + v for k,v in self.block_settings[-1].items()}
        else:
            settings = self.block_settings[block_level]

        self._tag = tag
        self._og_tagvars = tag_vars
        self._tagvars = tag_vars

        self._old_loglev = None
        self.log_level = log_level if log_level is not None else logger.verbosity
        self.opener = settings['opener'] if opener is None else opener
        self._old_prompt = None
        self.prompt = settings['prompt'] if prompt is None else prompt
        self.closer = settings['closer'] if closer is None else closer
        self._in_block = False

        self._print_manager=None
        self.printopts = printoptions
        self.captured_output_tag = captured_output_tag
        self._capture_output = capture_output
        if capture_errors is None:
            capture_errors = capture_output
        self.captured_error_tag = captured_error_tag
        self._capture_errors = capture_errors
        self._redirect = None

    @property
    def tag(self):
        """
        **LLM Docstring**

        The resolved (formatted) block tag, computed lazily from a string, a
        `(template, vars)` pair, or a callable.

        :return: the tag string
        :rtype: str
        """
        if self._tag is None:
            self._tag = ""
        elif not isinstance(self._tag, str):
            if callable(self._tag):
                self._tag = self._tag()
            else:
                tag_vars = self._tag[1] # type:dict
                tag_vars = tag_vars.get('preformatter', lambda **kw:kw)(**tag_vars)
                self._tag = self._tag[0].format(**tag_vars)
        elif self._tagvars is not None:
            tag_vars = self._tagvars
            tag_vars = tag_vars.get('preformatter', lambda **kw:kw)(**tag_vars)
            self._tag = self._tag.format(**tag_vars)
            self._tagvars = None

        return self._tag

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
        def _print(msg):
            """
            **LLM Docstring**

            Route a captured message through the logger with the block's tag, or straight to
            the base stream when a log print is already in progress.

            :param msg: the captured message
            :return: the logger's print result, if any
            """
            if Logger._in_log_print: #TODO: make thread safe
                print(msg, file=base_stream)
            else:
                return logger.log_print("{tag}{msg}", tag=tag, msg=msg, file=base_stream)
        return _print

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
        return redirects.StreamRedirect(self._print_capturing(self.logger, tag, base_stream))

    _redirect_capture_manager_stack = []
    def __enter__(self):
        """
        **LLM Docstring**

        Open the block: print the opener, start output capture (if enabled and none is
        already active), raise the logger's prompt/verbosity/nesting, and apply any
        numpy print options.
        """
        if self.log_level <= self.logger.verbosity:
            self._in_block = True
            self.logger.log_print(self.opener, tag=self.tag, padding="")
            if len(self._redirect_capture_manager_stack) == 0: # only allow one at a time
                if self._capture_output or self._capture_errors:
                    self._redirect = redirects.OutputRedirect(
                        stdout=(
                            self.stream_redirect(self.captured_output_tag, sys.stdout)
                                if self._capture_output else
                            None
                        ),
                        capture_output=self._capture_output,
                        stderr=(
                            self.stream_redirect(self.captured_error_tag, sys.stderr)
                                if self._capture_errors else
                            None
                        ),
                        capture_errors=self._capture_errors
                    )
                    self._redirect.__enter__()
                    self._redirect_capture_manager_stack.append(self)

            self._old_prompt = self.logger.padding
            self.logger.padding = self.prompt
            self._old_loglev = self.logger.verbosity
            self.logger.verbosity = self.log_level
            self.logger.block_level += 1

            if self.printopts is not None and self._print_manager is None:
                from numpy import printoptions
                self._print_manager = printoptions(**self.printopts)
                self._print_manager.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        **LLM Docstring**

        Close the block: stop output capture, print the closer, and restore the
        logger's prompt, verbosity, and nesting.

        :param exc_type: the exception type, if any
        :param exc_val: the exception value, if any
        :param exc_tb: the traceback, if any
        """
        if self._in_block:
            self._in_block = False
            try:
                if self._redirect is not None:
                    if self._redirect_capture_manager_stack[-1] is self:
                        self._redirect_capture_manager_stack.pop()
                    self._redirect.__exit__(exc_type, exc_val, exc_tb)
                    self._redirect = None
            finally:
                self.logger.log_print(self.closer, tag=self.tag, padding="")
                self.logger.padding = self._old_prompt
                self._old_prompt = None
                self.logger.verbosity = self._old_loglev
                self._old_loglev = None
                self.logger.block_level -= 1

                if self._print_manager is not None:
                    self._print_manager.__exit__(exc_type, exc_val, exc_tb)
                    self._print_manager = None

class Logger:
    """
    Defines a simple logger object to write log data to a file based on log levels.
    """

    LogLevel = LogLevel

    _loggers = weakref.WeakValueDictionary()
    default_verbosity = LogLevel.Normal
    def __init__(self,
                 log_file=None,
                 log_level=None,
                 print_function=None,
                 padding="",
                 newline="\n",
                 repad_messages=True,
                 block_options=None
                 ):
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
        self.log_file = log_file
        self.verbosity = log_level if log_level is not None else self.default_verbosity
        self.repad = repad_messages
        self.padding = padding
        self.newline = newline
        self.block_level = 0 # just an int to pass to `block(...)` so that it can
        self.auto_flush = True
        if print_function is None:
            print_function = print
        self.print_function = print_function
        self.active = True
        self.block_options = {} if block_options is None else block_options

    def to_state(self, serializer=None):
        """
        **LLM Docstring**

        Return the serializable state of the logger (dropping the print function when
        it's the builtin `print`).

        :param serializer: an optional serializer
        :return: the state dict
        :rtype: dict
        """
        return {
            'log_file': self.log_file,
            'verbosity': self.verbosity,
            'padding': self.padding,
            'newline': self.newline,
            'print_function': None if self.print_function is print else self.print_function
        }
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
        return cls(**state)

    def block(self, **kwargs):
        """
        **LLM Docstring**

        Open a nested logging block on this logger.

        :param kwargs: options forwarded to `LoggingBlock` (merged with the defaults)
        :return: the logging block
        :rtype: LoggingBlock
        """
        return LoggingBlock(self, block_level=self.block_level, **dict(self.block_options, **kwargs))

    def register(self, key):
        """
        Registers the logger under the given key
        :param key:
        :type key:
        :return:
        :rtype:
        """
        self._loggers[key] = self
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
        if key in cls._loggers:
            logger = cls._loggers[key]
        elif isinstance(key, Logger):
            logger = key
        elif key is True:
            logger = cls()
        else:
            if isinstance(key, str):
                try:
                    ll = LogLevel[key]
                except KeyError:
                    if construct:
                        logger = cls(key)
                    else:
                        logger = None
                else:
                    logger = cls(log_level=ll)
            else:
                logger = None
        if logger is None:
            logger = NullLogger()

        return logger

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

        def preformat(*args, **kwargs):
            """
            **LLM Docstring**

            Apply the captured key-functions to the matching keyword arguments, returning the
            (unchanged) positional args and the transformed keyword args.

            :param args: the positional arguments (passed through)
            :param kwargs: the keyword arguments (matching keys are transformed)
            :return: `(args, kwargs)`
            :rtype: tuple
            """

            for k,v in kwargs.items():
                if k in key_functions:
                    kwargs[k] = key_functions[k](v)

            return args, kwargs
        return preformat

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
        if preformatter is not None:
            args = preformatter(*params, **kwargs)
            if isinstance(args, dict):
                kwargs = args
                params = ()
            elif (
                    isinstance(args, tuple)
                    and len(args) == 2
                    and isinstance(args[1], dict)
            ):
                params, kwargs = args
            else:
                params = ()
                kwargs = args

        if _repad is None: _repad = self.repad
        if _repad:
            kwargs = {
                k: (
                    self.pad_newlines(v, newline=_newline, padding=_padding, **kwargs)
                        if isinstance(v, str) else
                    v
                )
                for k,v in kwargs.items()
            }

        if len(kwargs) > 0:
            message = message.format(*params, **kwargs)
        elif len(params) > 0:
            message = message.format(*params)
        return message

    def format_metainfo(self, metainfo):
        """
        **LLM Docstring**

        Format block meta-information as a JSON string (or empty string when absent).

        :param metainfo: the meta-information
        :return: the formatted meta string
        :rtype: str
        """
        if metainfo is None:
            return ""
        else:
            import json
            return json.dumps(metainfo)

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
        if not isinstance(obj, str): obj = '{}'.format(obj)
        if padding is None: padding = self.padding
        if newline is None: newline = self.newline
        rep = (newline + padding).format(**kwargs)
        return obj.replace("\n", rep)
    @staticmethod
    def split_lines(obj):
        """
        **LLM Docstring**

        Split a value's string form into lines.

        :param obj: the value
        :return: the lines
        :rtype: list[str]
        """
        return str(obj).splitlines()
    @staticmethod
    def prep_array(obj):
        """
        **LLM Docstring**

        Render a numpy array to lines without truncation (wide/high print limits).

        :param obj: the array
        :return: the rendered lines
        :rtype: list[str]
        """
        import numpy as np
        with np.printoptions(linewidth=1e8, edgeitems=1e3, threshold=1e8):
            return str(obj).splitlines()
    @staticmethod
    def prep_dict(obj):
        """
        **LLM Docstring**

        Render a dict as `key: value` lines.

        :param obj: the dict
        :return: the rendered lines
        :rtype: list[str]
        """
        return ["{k}: {v}".format(k=k, v=v) for k,v in obj.items()]

    def log_print(self,
                  message,
                  *messrest,
                  message_prepper=None,
                  padding=None, newline=None,
                  log_level=None,
                  metainfo=None, print_function=None,
                  print_options=None,
                  sep=None, end=None, file=None, flush=None,
                  preformatter=None,
                  **kwargs
                  ):
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


        if log_level is None:
            log_level = self.default_verbosity

        if log_level <= self.verbosity:

            if padding is None:
                padding = self.padding
            if newline is None:
                newline = self.newline
            if print_function is None:
                print_function = self.print_function

            if message_prepper is not None:
                message = message_prepper(message, *messrest)
                messrest = ()

            if len(messrest) > 0:
                message = [message, *messrest]

            if not isinstance(message, str):
                joiner = (newline + padding)
                message = joiner.join(
                    [padding + message[0]]
                    + list(message[1:])
                )
            else:
                message = padding + message

            # print(">>>>", repr(message), params)

            if print_options is None:
                print_options = {}
            if sep is not None:
                print_options['sep'] = sep
            if end is not None:
                print_options['end'] = end
            if file is not None:
                print_options['file'] = file
            if flush is not None:
                print_options['flush'] = flush

            if 'flush' not in print_options:
                print_options['flush'] = self.auto_flush

            if log_level <= self.verbosity:

                msg = self.format_message(message,
                                          meta=self.format_metainfo(metainfo),
                                          preformatter=preformatter,
                                          _newline=newline,
                                          _padding=padding,
                                          **kwargs)
                if isinstance(print_function, str) and print_function == 'echo':
                    if self.log_file is not None:
                        self._print_message(print, msg, self.log_file, print_options)
                    self._print_message(print, msg, None, print_options)
                else:
                    self._print_message(print_function, msg, self.log_file, print_options)

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
        try:
            cls._in_log_print = True
            if isinstance(log, str):
                if not os.path.isdir(os.path.dirname(log)):
                    try:
                        os.makedirs(os.path.dirname(log))
                    except OSError:
                        pass
                # O_NONBLOCK is *nix only
                with open(log, mode="a", buffering=1 if print_options['flush'] else -1) as lf:  # this is potentially quite slow but I am also quite lazy
                    print_function(msg, **dict(print_options, file=lf))
            elif log is None:
                print_function(msg, **print_options)
            else:
                print_function(msg, **dict(print_options, file=log))
        finally:
            cls._in_log_print = False

    def __repr__(self):
        """
        **LLM Docstring**

        Return a representation showing the log file and verbosity.

        :return: the representation
        :rtype: str
        """
        return "{}({}, {})".format(
            type(self).__name__,
            self.log_file,
            self.verbosity
        )

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
        super().__init__(*log_files, **logger_opts)
        self.active = False
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
        pass
    def __bool__(self):
        """
        **LLM Docstring**

        A null logger is always falsy.

        :return: `False`
        :rtype: bool
        """
        return False
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
        return super().block(capture_output=capture_output, **kwargs)
