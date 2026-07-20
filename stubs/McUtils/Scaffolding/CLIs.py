"""
Simple package for easily creating command line interfaces in a
nestable way with automatic argument dispatch
"""
import inspect, typing, os, sys, argparse, collections
__all__ = ['CLI', 'CommandGroup', 'Command']

class Command:
    """
    A holder for a command that just automates type handling &
    that sort of thing
    """

    def __init__(self, name, method):
        """
        **LLM Docstring**

        Inspect a callable, recording its type hints and treating every parameter without a default as positional.

        :param name: registry, command, resource, or object name
        :type name: object
        :param method: callable wrapped as a command
        :type method: object
        :return: No explicit value; the method mutates state or performs I/O.
        :rtype: None
        """
        ...

    def get_help(self):
        """
        Gets single method help string
        :return:
        :rtype:
        """
        ...

    @classmethod
    def _hint_types(cls, hint):
        """
        :param hint:
        :type hint: type | str | typing.GenericAlias
        :return:
        :rtype:
        """
        ...

    @classmethod
    def _hint_str(cls, hint):
        """
        :param hint:
        :type hint: type | str | typing.GenericAlias
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def get_parse_dict(*spec):
        """
        Builds a parse spec to feed into an ArgumentParser later
        :param spec:
        :type spec:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def _get_typed(val: str, converter: callable):
        """
        **LLM Docstring**

        Convert a nonempty command-line string with the supplied converter, using `None` for the empty sentinel.

        :param val: the value being stored, converted, or installed
        :type val: str
        :param converter: callable used to convert a command-line value
        :type converter: callable
        :return: `None` for an empty string, otherwise `converter(val)`
        :rtype: object | None
        """
        ...

    def get_parse_spec(self):
        """
        Gets a parse spec that can be fed to ArgumentParser

        :return:
        :rtype:
        """
        ...

    def parse(self):
        """
        Generates a parse spec, builds an ArgumentParser, and parses the arguments

        :return:
        :rtype:
        """
        ...

    def __call__(self):
        """
        Parse argv and call bound method
        :return:
        :rtype:
        """
        ...

class CommandGroup:
    """
    Generic interface that defines an available set of commands
    as class methods.
    Basically just exists to be ingested by a CLI.
    """
    _name = ''
    _description = ''
    _tag = None

    @classmethod
    def _get_tag(cls):
        """
        **LLM Docstring**

        Return the explicit group tag or derive one by lowercasing the group name.

        :return: the command-group tag
        :rtype: str
        """
        ...

    @classmethod
    def _get_commands(cls):
        """
        Returns the commands defined on the class as well
        as their arguments and allowed types
        :return:
        :rtype:
        """
        ...

    @classmethod
    def _get_command(cls, k):
        """
        Returns the commands defined on the class as well
        as their arguments and allowed types
        :return:
        :rtype:
        """
        ...

    @classmethod
    def _get_help(cls):
        """
        Gets the help string for the CLI
        :return:
        :rtype:
        """
        ...

class CLI:
    """
    A representation of a command line interface
    which layers simple command dispatching on the basic
    ArgParse interface
    """

    def __init__(self, name, description, *groups, cmd_name=None):
        """
        :param name:
        :type name: str
        :param name:
        :type description: str
        :param cmd_name:
        :type cmd_name: str | None
        :param groups:
        :type groups: Type[CommandGroup]
        """
        ...

    def parse_group_command(self):
        """
        Parses a group and command argument (if possible) and prunes `sys.argv`

        :param group:
        :type group:
        :param command:
        :type command:
        :return:
        :rtype:
        """
        ...

    def get_command(self):
        """
        **LLM Docstring**

        Consume the group and command tokens, support the default-group shorthand, and return a bound `Command` or help text.

        :return: The resolved command or command group.
        :rtype: Command | type[CommandGroup] | str
        """
        ...

    def get_group(self, grp):
        """
        **LLM Docstring**

        Resolve a registered command group and raise an informative error for missing or absent default groups.

        :param grp: command-group tag
        :type grp: object
        :return: The resolved command or command group.
        :rtype: Command | type[CommandGroup] | str
        """
        ...

    def run_command(self):
        """
        **LLM Docstring**

        Resolve and execute the selected command, printing the result only when resolution produced help text.

        :return: the command return value, or the printed help string
        :rtype: object | str
        """
        ...

    def get_help(self):
        """
        Gets the help string for the CLI
        :return:
        :rtype:
        """
        ...

    def help(self, print_help=True):
        """
        **LLM Docstring**

        Remove the help token, generate the full help text, optionally print it, and return it.

        :param print_help: whether generated help text should be printed
        :type print_help: object
        :return: the complete CLI help text
        :rtype: str
        """
        ...

    def run_parse(self, parse, unknown):
        """
        Provides a standard entry point to running stuff using the default CLI

        :param parse:
        :type parse:
        :param unknown:
        :type unknown:
        :return:
        :rtype:
        """
        ...

    def parse_toplevel_args(self):
        """
        Parses out the top level flags that the program supports

        :return:
        :rtype:
        """
        ...

    def run(self):
        """
        Parses the arguments in `sys.argv` and dispatches to the approriate action.
        By default supports interactive sessions, running scripts, and abbreviated tracebacks.

        :return:
        :rtype:
        """
        ...