import numpy as np, re
from collections import OrderedDict
from .RegexPatterns import *
from .StructuredType import *
__all__ = ['StringParser', 'StringParserException']
__reload_hook__ = ['.RegexPatterns']

class StringParserException(Exception):
    ...

class StringParser:
    """
    A convenience class that makes it easy to pull blocks out of strings and whatnot
    """

    def __init__(self, regex: RegexPattern):
        """
        **LLM Docstring**

        Store the declarative `RegexPattern` used by parsing methods when no override is supplied.

        :param regex: the pattern override; defaults to the parser's stored pattern
        :type regex: RegexPattern
        """
        ...

    def parse(self, txt, regex=None, block_handlers=None, dtypes=None, out=None):
        """Finds a single match for the and applies parsers for the specified regex in txt

        :param txt: a chunk of text to be matched
        :type txt: str
        :param regex: the regex to match in _txt_
        :type regex: RegexPattern
        :param block_handlers: handlers for the matched blocks in _regex_ -- usually comes from _regex_
        :type block_handlers: iterable[callable] | OrderedDict[str: callable]
        :param dtypes: the types of the data that we expect to match -- usually comes from _regex_
        :type dtypes: iterable[type | StructuredType] | OrderedDict[str: type | StructuredType]
        :param out: where to place the parsed out data -- usually comes from _regex_
        :type out: None | StructuredTypeArray | iterable[StructuredTypeArray] | OrderedDict[str: StructuredTypeArray]
        :return:
        :rtype:
        """
        ...

    def parse_all(self, txt, regex=None, num_results=None, block_handlers=None, dtypes=None, out=None):
        """
        **LLM Docstring**

        Find all non-overlapping matches, allocate or reuse typed result storage, add a result axis for newly allocated arrays, and insert every match through the shared match-processing pipeline.

        :param txt: the input text or text block to parse
        :type txt: object

        :param regex: the pattern override; defaults to the parser's stored pattern
        :type regex: object

        :param num_results: the maximum number of matches to consume
        :type num_results: object

        :param block_handlers: post-processors aligned with captured groups
        :type block_handlers: object

        :param dtypes: the structured result type inferred from or supplied for the pattern
        :type dtypes: object

        :param out: existing result storage or an insertion-control mapping
        :type out: object

        :return: The parsed block or typed result structure, with endpoint metadata when requested.
        :rtype: object
        """
        ...

    class MatchIterator:

        class Match:

            def __init__(self, parent, block):
                """
                **LLM Docstring**

                Store the parent iterator and one raw `re.Match` object.

                :param parent: the parent reader or regex node
                :type parent: object

                :param block: the candidate TeX or BibTeX source block
                :type block: object
                """
                ...

            @property
            def value(self):
                """
                **LLM Docstring**

                Allocate typed result storage and parse this match into it on demand.

                :return: allocate typed result storage and parse this match into it on demand.
                :rtype: object
                """
                ...

        def __init__(self, parser, match_iter, num_results, dtypes, block_handlers):
            """
            **LLM Docstring**

            Store parsing metadata and optionally cap the underlying match iterator with `itertools.islice`.

            :param parser: an optional callable that converts extracted block text
            :type parser: object

            :param match_iter: an iterator of raw regex matches
            :type match_iter: object

            :param num_results: the maximum number of matches to consume
            :type num_results: object

            :param dtypes: the structured result type inferred from or supplied for the pattern
            :type dtypes: object

            :param block_handlers: post-processors aligned with captured groups
            :type block_handlers: object
            """
            ...

        def __iter__(self):
            """
            **LLM Docstring**

            Yield lazy wrapper objects for each remaining regex match.

            :return: An iterator yielding the records described above.
            :rtype: object
            """
            ...

        def __next__(self):
            """
            **LLM Docstring**

            Return a lazy wrapper for the next regex match.

            :return: return a lazy wrapper for the next regex match.
            :rtype: object
            """
            ...

    def parse_iter(self, txt, regex=None, num_results=None, block_handlers=None, dtypes=None):
        """
        **LLM Docstring**

        Create a lazy iterator over matches, carrying the inferred dtypes and block handlers needed to parse each match on demand.

        :param txt: the input text or text block to parse
        :type txt: object

        :param regex: the pattern override; defaults to the parser's stored pattern
        :type regex: object

        :param num_results: the maximum number of matches to consume
        :type num_results: object

        :param block_handlers: post-processors aligned with captured groups
        :type block_handlers: object

        :param dtypes: the structured result type inferred from or supplied for the pattern
        :type dtypes: object

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        ...

    @classmethod
    def get_regex_block_handlers(cls, regex):
        """Uses the uncompiled RegexPattern to determine what blocks exist and what handlers they should use

        :param regex:
        :type regex: RegexPattern
        :return:
        :rtype:
        """
        ...

    @classmethod
    def get_regex_dtypes(cls, regex):
        """Uses the uncompiled RegexPattern to determine which StructuredTypes to return

        :param regex:
        :type regex: RegexPattern
        :return:
        :rtype:
        """
        ...

    def _set_up_result_arrays(self, dtypes):
        """
        **LLM Docstring**

        Construct one `StructuredTypeArray` from the inferred structured dtype.

        :param dtypes: the structured result type inferred from or supplied for the pattern
        :type dtypes: object

        :return: construct one `StructuredTypeArray` from the inferred structured dtype.
        :rtype: object
        """
        ...

    def _split_match_groups(self, groups, handlers, res):
        """This is _supposed_ to be splitting my groups so that the appropriate handler handles them, but it's missing a corner case
        Sometimes we have something like:
            RegexPattern((Capturing(Number), ..., Capturing(Number), ..., Capturing(Number))

        This happens to make 3 handlers even though it's really a single array of data...
        Then the grouping sees this and says "Aha! Must transpose"
        In reality it shouldn't even be bothering to touch it though...

        :param groups:
        :type groups:
        :param handlers:
        :type handlers:
        :param res:
        :type res:
        :return:
        :rtype:
        """
        ...

    def _handle_insert_result(self, array, handler, data, single=True, append=False):
        """Handles the process of actually inserting the matches data/groups into array, applying any necessary
        handler in the process

        :param array: the array the data should be inserted into
        :type array: StructuredTypeArray
        :param handler: handler function for further processing of the matched data
        :type handler: None | callable
        :param data: matched data
        :type data: iterable[str]
        :param single: whether data should be treated as a single object (e.g. a subarray) or as multiple data objects
        :type single: bool
        :param append: whether the data should be appended or whether the array should entirely re-assign itself / which axes to assign to
        :type append: bool | iterable[int]
        """
        ...

    def _handle_parse_match(self, match, res, block_handlers, append=False, single=None, default_value=''):
        """Figures out how to handle the matched data from the parser
        In general the way we _want_ to do this is to basically do the most minimal amount of processing we can
        and then use the efficient methods inside StructuredTypeArray to cast this to properly typed arrays

        One issue is that we can end up with stuff that looks like:
            [
                [ group_a match_1, group_a match_2, group_b match_1, ... ]
                ...
            ]
        where we need to first chop the data into group_a, group_b, ...

        The type-calculus in RegexPattern and StructuredType can give us a "block size" for each subarray inside the
        StructuredTypeArray which indicates how many elements it expects to see from the group

        We use that to chop up the array as needed in these multi-match cases before trying to feed it into the
        StructuredTypeArray

        Complicating that, though, is that we sometimes need to do an extra layer of parsing on our matches

        Imagine that we found every instance of Repeating(Capturing(Number), suffix=Optional(Whitespace))

        This could give us something like
            [
                '-1232.123-234.345 3434.3434 10000000000',
                '5',
                '6'
            ]

        It would be hard to say what we should do with this, so we'll assume (possibly incorrectly) that we won't get a
        ragged array. If we need to introduce raggedness we'll do it later

        Even then, we could have
            [
                '-1232.123-234.345 3434.3434 10000000000',
                '5         5       5         5',
                '6         6       6         6'
            ]

        Here we'd need to go through line-by-line and apply the subparser of Number to each line to split it up

        On the other hand, what if we matched Duplicated(Capturing(Number), 4, riffle=Optional(Whitespace))?

        Then we'd have
            [
                ['-1232.123', '-234.345', '3434.3434', '10000000000'],
                ['5',         '5',        '5',         '5'],
                ['6',         '6',        '6',         '6']
            ]

        And here we wouldn't want to apply the subparser.

        The only way we could determine the difference is by comparing the shape of the StructuredTypeArray to the
        matched data. This means our block_handlers need to take the passed res array to figure their shit out too.


        :param append: whether to append the data or not
        :type append:
        :param single: whether the matched data should be treated like a singular object
        :type single:
        :param default_value:
        :type default_value:
        :param match:
        :type match: re.Match | iterable[re.Match]
        :param res:
        :type res:
        :param block_handlers:
        :type block_handlers:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def _get_regex_handler(cls, r):
        """
        **LLM Docstring**

        Return an explicit handler when present; return no handler for scalar primitive captures; otherwise construct a recursive parser that removes the outer capture and parses repeated or compound matched text into compatible result arrays.

        :param r: the regex node or structured result array processed by the helper
        :type r: object

        :return: A callable compatible with the parser's block-handler interface, or `None` for directly castable scalar captures.
        :rtype: object
        """
        ...

    @classmethod
    def handler_method(cls, method):
        """Turns a regular function into a handler method by adding in (and ignoring) the array argument

        :param method:
        :type method:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def load_array(data, dtype='float'):
        """
        **LLM Docstring**

        Parse whitespace-delimited text into a NumPy array with `numpy.loadtxt`.

        :param data: the input bytes, text, matched values, or replacement data
        :type data: object

        :param dtype: the declared value type for captures
        :type dtype: object

        :return: The parsed NumPy array.
        :rtype: object
        """
        ...

    @classmethod
    def to_array(cls, data, array=None, append=False, dtype='float', shape=None, pre=None):
        """A method to take a string or iterable of strings and quickly dump it to a NumPy array of the right dtype (if it can be cast as one)

        :param data:
        :type data:
        :param dtype:
        :type dtype:
        :return:
        :rtype:
        """
        ...

    @classmethod
    def array_handler(cls, array=None, append=False, dtype='float', shape=None, pre=None):
        """Returns a handler that uses to_array

        :param dtype:
        :type dtype:
        :param array:
        :type array:
        :param shape:
        :type shape:
        :return:
        :rtype:
        """
        ...