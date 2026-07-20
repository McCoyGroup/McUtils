import re
from . import FileStreamer as Parsers
from .. import Devutils as dev
__all__ = ['TeXParser', 'BibTeXParser']

class TeXParser(Parsers.FileStreamReader):
    default_binary = False

    @classmethod
    def is_valid_tex_block(cls, block: str):
        """
        **LLM Docstring**

        Accept a TeX call block when unescaped opening braces are exactly one fewer than closing braces, matching a command whose leading `{` was consumed separately.

        :param block: the candidate TeX or BibTeX source block
        :type block: str

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        ...

    @classmethod
    def is_valid_stream_start(cls, tag_str):
        """
        **LLM Docstring**

        Accept a candidate command tag when it has a non-empty body and balanced square brackets.

        :param tag_str: a candidate command or entry-start tag
        :type tag_str: object

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        ...

    @classmethod
    def _call_match_test(cls, options):
        """
        **LLM Docstring**

        Compile allowed command names into a full-match validator that distinguishes invalid tag starts from valid-but-disallowed commands.

        :param options: a regex or iterable used to restrict accepted names or bodies
        :type options: object

        :return: compile allowed command names into a full-match validator that distinguishes invalid tag starts from valid-but-disallowed commands.
        :rtype: object
        """
        ...

    def parse_tex_call(self, allowed_calls=None, return_end_points=False):
        """
        **LLM Docstring**

        Locate an allowed TeX command, read its balanced braced argument, then consume and concatenate any immediately adjacent braced arguments; optionally return the combined source endpoints.

        :param allowed_calls: a command-name regex or iterable of allowed TeX commands
        :type allowed_calls: object

        :param return_end_points: whether to return source offsets with the parsed block
        :type return_end_points: object

        :return: The parsed block or typed result structure, with endpoint metadata when requested.
        :rtype: object
        """
        ...

    @classmethod
    def _call_body_match_test(cls, calls, options):
        """
        **LLM Docstring**

        Build a validator that first matches a command name and then full-matches the text of its first braced argument.

        :param calls: the allowed command-name expression
        :type calls: object

        :param options: a regex or iterable used to restrict accepted names or bodies
        :type options: object

        :return: build a validator that first matches a command name and then full-matches the text of its first braced argument.
        :rtype: object
        """
        ...

    @classmethod
    def _valid_environment_test(cls, block: str):
        """
        **LLM Docstring**

        Verify balanced braces, matching `\\begin{name}`/`\\end{name}` names, and equal counts of nested begin/end markers for the same environment.

        :param block: the candidate TeX or BibTeX source block
        :type block: str

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        ...

    def parse_tex_environment(self, allowed_environments=None, return_end_points=False):
        """
        **LLM Docstring**

        Extract a complete TeX environment, restricted to selected names when requested, validating nested occurrences and optionally returning its start offset.

        :param allowed_environments: an environment-name regex or iterable of allowed names
        :type allowed_environments: object

        :param return_end_points: whether to return source offsets with the parsed block
        :type return_end_points: object

        :return: The parsed block or typed result structure, with endpoint metadata when requested.
        :rtype: object
        """
        ...

class BibItemParser(Parsers.FileStreamReader):
    default_binary = False

    @classmethod
    def is_valid_tex_block(cls, block: str):
        """
        **LLM Docstring**

        Accept a BibTeX field value when escaped braces are ignored and the remaining braces are balanced.

        :param block: the candidate TeX or BibTeX source block
        :type block: str

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        ...

    @classmethod
    def is_valid_key_block(cls, block: str):
        """
        **LLM Docstring**

        Accept text consisting of optional whitespace, a word-like field name, optional whitespace, and `=`.

        :param block: the candidate TeX or BibTeX source block
        :type block: str

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        ...

    def parse_header(self, return_end_points=False):
        """
        **LLM Docstring**

        Parse the `@type{citation_key,` prefix of one BibTeX entry and return the entry type and citation key, optionally with source endpoints.

        :param return_end_points: whether to return source offsets with the parsed block
        :type return_end_points: object

        :return: The parsed block or typed result structure, with endpoint metadata when requested.
        :rtype: object
        """
        ...

    def parse_bib_line(self, allowed_fields=None, return_end_points=False):
        """
        **LLM Docstring**

        Parse one `field = value` assignment, searching backward to find the field name when unrestricted and then forward through balanced braces to the separating comma or entry terminator.

        :param allowed_fields: field names accepted while parsing a BibTeX entry
        :type allowed_fields: object

        :param return_end_points: whether to return source offsets with the parsed block
        :type return_end_points: object

        :return: The parsed block or typed result structure, with endpoint metadata when requested.
        :rtype: object
        """
        ...

class BibTeXParser(Parsers.FileStreamReader):
    default_binary = False

    @classmethod
    def is_valid_tex_block(cls, block: str):
        """
        **LLM Docstring**

        Accept a BibTeX entry block when the consumed opening brace leaves one more closing brace than opening braces.

        :param block: the candidate TeX or BibTeX source block
        :type block: str

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        ...
    _bib_item_pattern = '\\@\\w+\\{'

    @classmethod
    def is_valid_stream_start(cls, tag_str):
        """
        **LLM Docstring**

        Compile the entry-start pattern once and full-match candidate strings such as `@article{`.

        :param tag_str: a candidate command or entry-start tag
        :type tag_str: object

        :return: compile the entry-start pattern once and full-match candidate strings such as `@article{`.
        :rtype: object
        """
        ...

    @classmethod
    def _call_match_test(cls, options):
        """
        **LLM Docstring**

        Compile allowed BibTeX entry types into a validator for entry-start tags.

        :param options: a regex or iterable used to restrict accepted names or bodies
        :type options: object

        :return: compile allowed BibTeX entry types into a validator for entry-start tags.
        :rtype: object
        """
        ...

    def parse_bib_item(self, allowed_items=None, return_end_points=False):
        """
        **LLM Docstring**

        Extract one complete balanced BibTeX entry, optionally restricting the accepted entry types and returning source endpoints.

        :param allowed_items: entry-type names accepted while parsing BibTeX
        :type allowed_items: object

        :param return_end_points: whether to return source offsets with the parsed block
        :type return_end_points: object

        :return: The parsed block or typed result structure, with endpoint metadata when requested.
        :rtype: object
        """
        ...

    @classmethod
    def parse_bib_body(self, text, allowed_fields=None, parse_lines=True):
        """
        **LLM Docstring**

        Parse an entry string into its type, citation key, header endpoints, and a mapping from field names to `(endpoints, original_assignment_text)` records; field parsing can be disabled.

        :param text: the complete BibTeX entry text
        :type text: object

        :param allowed_fields: field names accepted while parsing a BibTeX entry
        :type allowed_fields: object

        :param parse_lines: whether individual BibTeX fields are parsed after the header
        :type parse_lines: object

        :return: The parsed block or typed result structure, with endpoint metadata when requested.
        :rtype: object
        """
        ...