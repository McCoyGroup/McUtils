"""
Simple utilities that support constructing Regex patterns
"""
import re
from collections import OrderedDict
from .StructuredType import StructuredType, DisappearingType
__reload_hook__ = ['.StructuredType']
__all__ = ['RegexPattern', 'Capturing', 'NonCapturing', 'Optional', 'Alternatives', 'Longest', 'Shortest', 'Repeating', 'Duplicated', 'PatternClass', 'Parenthesized', 'Named', 'StartOfString', 'EndOfString', 'Any', 'Sign', 'Number', 'IntBaseNumber', 'Integer', 'PositiveInteger', 'ASCIILetter', 'AtomName', 'WhitespaceCharacter', 'Whitespace', 'Word', 'WordCharacter', 'VariableName', 'CartesianPoint', 'IntXYZLine', 'XYZLine', 'Empty', 'Newline', 'ZMatPattern']

class RegexPattern:
    """
    Represents a combinator structure for building more complex regexes

    It might be worth working with this combinator structure in a _lazy_ fashion so that we can drill down
    into the expression structure... that way we can define a sort-of Regex calculus that we can use to build up higher
    order regexes but still be able to recursively inspect subparts?
    """

    def __init__(self, pat, name=None, children=None, parents=None, dtype=None, repetitions=None, key=None, joiner='', join_function=None, wrapper_function=None, suffix=None, prefix=None, parser=None, handler=None, default_value=None, capturing=None, allow_inner_captures=False, escape=True):
        """
        :param pat:
        :type pat: str | callable
        :param name:
        :type name: str
        :param dtype:
        :type dtype:
        :param repetitions:
        :type repetitions:
        :param key:
        :type key:
        :param joiner:
        :type joiner:
        :param children:
        :type children:
        :param parents:
        :type parents:
        :param wrapper_function:
        :type wrapper_function:
        :param suffix:
        :type suffix:
        :param prefix:
        :type prefix:
        :param parser:
        :type parser:
        :param handler:
        :type handler:
        :param capturing:
        :type capturing:
        :param allow_inner_captures:
        :type allow_inner_captures:
        """
        ...

    @property
    def pat(self):
        """
        **LLM Docstring**

        Return or replace the primitive pattern/wrapper used by this node; setting it invalidates all compiled caches.

        :param pat: a literal regex fragment or callable wrapper
        :type pat: object

        :return: return or replace the primitive pattern/wrapper used by this node; setting it invalidates all compiled caches.
        :rtype: object
        """
        ...

    @pat.setter
    def pat(self, pat):
        """
        **LLM Docstring**

        Return or replace the primitive pattern/wrapper used by this node; setting it invalidates all compiled caches.

        :param pat: a literal regex fragment or callable wrapper
        :type pat: object

        :return: return or replace the primitive pattern/wrapper used by this node; setting it invalidates all compiled caches.
        :rtype: object
        """
        ...

    @property
    def children(self):
        """

        :return:
        :rtype: tuple[RegexPattern]
        """
        ...

    @property
    def child_count(self):
        """

        :return:
        :rtype: int
        """
        ...

    @property
    def child_map(self):
        """Returns the map to subregexes for named regex components

        :return:
        :rtype: Dict[str, RegexPattern]
        """
        ...

    @property
    def parents(self):
        """

        :return:
        :rtype: tuple[RegexPattern]
        """
        ...

    @property
    def joiner(self):
        """

        :return:
        :rtype: str
        """
        ...

    @joiner.setter
    def joiner(self, j):
        """
        **LLM Docstring**

        Return or replace the separator placed between built child patterns; setting it invalidates the pattern-string cache.

        :param j: the separator used to join child regex strings
        :type j: object

        :return: return or replace the separator placed between built child patterns; setting it invalidates the pattern-string cache.
        :rtype: object
        """
        ...

    @property
    def join_function(self):
        """

        :return:
        :rtype: function
        """
        ...

    @join_function.setter
    def join_function(self, j):
        """
        **LLM Docstring**

        Return or replace the callable that combines the joiner and built children; setting it invalidates the pattern-string cache.

        :param j: the separator used to join child regex strings
        :type j: object

        :return: return or replace the callable that combines the joiner and built children; setting it invalidates the pattern-string cache.
        :rtype: object
        """
        ...

    @property
    def suffix(self):
        """

        :return:
        :rtype: str | RegexPattern
        """
        ...

    @suffix.setter
    def suffix(self, e):
        """
        **LLM Docstring**

        Return or replace the suffix appended after the combined children; setting it invalidates the pattern-string cache.

        :param e: the new suffix pattern
        :type e: object

        :return: return or replace the suffix appended after the combined children; setting it invalidates the pattern-string cache.
        :rtype: object
        """
        ...

    @property
    def prefix(self):
        """

        :return:
        :rtype: str | RegexPattern
        """
        ...

    @prefix.setter
    def prefix(self, s):
        """
        **LLM Docstring**

        Return or replace the prefix prepended before the combined children; setting it invalidates the pattern-string cache.

        :param s: the shape assigned to the object
        :type s: object

        :return: return or replace the prefix prepended before the combined children; setting it invalidates the pattern-string cache.
        :rtype: object
        """
        ...

    @property
    def dtype(self):
        """Returns the StructuredType for the matched object

        The basic thing we do is build the type from the contained child dtypes
        The process effectively works like this:
            If there's a single object, we use its dtype no matter what
            Otherwise, we add together our type objects one by one, allowing the StructuredType to handle the calculus

        After we've built our raw types, we compute the shape on top of these, using the assigned repetitions object
        One thing I realize now I failed to do is to include the effects of sub-repetitions... only a single one will
        ever get called.

        :return:
        :rtype: None | StructuredType
        """
        ...

    @property
    def is_repeating(self):
        """
        **LLM Docstring**

        Report whether repetition metadata is stored as a `(minimum, maximum)` tuple.

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        ...

    @property
    def capturing(self):
        """
        **LLM Docstring**

        Report whether this node captures directly, including the implicit case where a repeating node contains capturing descendants.

        :param cap: whether this node captures directly
        :type cap: object

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        ...

    @capturing.setter
    def capturing(self, cap):
        """
        **LLM Docstring**

        Report whether this node captures directly, including the implicit case where a repeating node contains capturing descendants.

        :param cap: whether this node captures directly
        :type cap: object

        :return: `True` when the condition described above holds; otherwise `False`.
        :rtype: bool
        """
        ...

    def get_capturing_groups(self, allow_inners=None):
        """
        We walk down the tree to find the children with capturing groups in them and
        then find the outermost RegexPattern for those unless allow_inners is on in which case we pull them all
        """
        ...

    @property
    def captures(self):
        """Subtly different from capturing n that it will tell us if we need to use the group in post-processing, essentially

        :return:
        :rtype:
        """
        ...

    @property
    def capturing_groups(self):
        """Returns the capturing children for the pattern

        :return:
        :rtype:
        """
        ...

    @property
    def named_groups(self):
        """Returns the named children for the pattern

        :return:
        :rtype:
        """
        ...

    def combine(self, other, *args, **kwargs):
        """Combines self and other

            :param other:
            :type other: RegexPattern | str
            :return:
            :rtype: str | callable
            """
        ...

    def wrap(self, *args, **kwargs):
        """
        Applies wrapper function
        """
        ...

    @staticmethod
    def _join_kids(joiner, kids, no_capture=True):
        """
        **LLM Docstring**

        Group ungrouped children when more than one is present, then join them with the requested separator.

        :param joiner: text or a pattern inserted between children
        :type joiner: object

        :param kids: already-built child regex strings
        :type kids: object

        :param no_capture: whether the resulting regex must avoid a capturing group
        :type no_capture: object

        :return: group ungrouped children when more than one is present, then join them with the requested separator.
        :rtype: object
        """
        ...

    def build(self, joiner=None, prefix=None, suffix=None, recompile=True, no_captures=False, verbose=False):
        """
        **LLM Docstring**

        Recursively build the regex text for this node, suppressing inner captures when an outer node captures, applying prefix/joiner/suffix and wrapper functions, and caching the normal capturing form.

        :param joiner: text or a pattern inserted between children
        :type joiner: object

        :param prefix: text or a pattern prepended to this node
        :type prefix: object

        :param suffix: text or a pattern appended to this node
        :type suffix: object

        :param recompile: whether to rebuild instead of reusing cached regex text
        :type recompile: object

        :param no_captures: whether captures are suppressed throughout this build
        :type no_captures: object

        :param verbose: whether to print intermediate regex construction details
        :type verbose: object

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        ...

    @property
    def compiled(self):
        """
        **LLM Docstring**

        Compile and cache the regex string returned by `build`.

        :return: The cached compiled regular-expression object.
        :rtype: object
        """
        ...

    def add_parent(self, parent):
        """
        **LLM Docstring**

        Register an ancestor that must be invalidated when this node changes.

        :param parent: the parent reader or regex node
        :type parent: object

        :return: None.
        :rtype: None
        """
        ...

    def remove_parent(self, parent):
        """
        **LLM Docstring**

        Remove a previously registered ancestor.

        :param parent: the parent reader or regex node
        :type parent: object

        :return: None.
        :rtype: None
        """
        ...

    def add_child(self, child):
        """
        **LLM Docstring**

        Append one child, update named/capturing-descendant flags, and invalidate this node and its ancestors.

        :param child: the child pattern to add or remove
        :type child: object

        :return: None.
        :rtype: None
        """
        ...

    def add_children(self, children):
        """
        **LLM Docstring**

        Append several children, merge their named/capturing-descendant flags, and invalidate caches.

        :param children: child patterns combined by this node
        :type children: object

        :return: None.
        :rtype: None
        """
        ...

    def remove_child(self, child):
        """
        **LLM Docstring**

        Remove one child, recompute descendant flags from the remaining children, and invalidate caches.

        :param child: the child pattern to add or remove
        :type child: object

        :return: None.
        :rtype: None
        """
        ...

    def insert_child(self, index, child):
        """
        **LLM Docstring**

        Insert a child at a specific position and invalidate cached pattern state.

        :param index: the insertion position
        :type index: object

        :param child: the child pattern to add or remove
        :type child: object

        :return: None.
        :rtype: None
        """
        ...

    def invalidate_cache(self):
        """
        **LLM Docstring**

        Clear built-string, compiled-regex, and capturing-group caches, then recursively invalidate all parents.

        :return: None.
        :rtype: None
        """
        ...

    def __copy__(self):
        """
        **LLM Docstring**

        Make a shallow node copy with an independent child list, no parents, and no built-pattern cache.

        :return: An independent shallow copy of the regex node.
        :rtype: object
        """
        ...

    def __add__(self, other):
        """Combines self and other

        :param other:
        :type other: RegexPattern
        :return:
        :rtype:
        """
        ...

    def __radd__(self, other):
        """Combines self and other

        :param other:
        :type other: RegexPattern
        :return:
        :rtype:
        """
        ...

    def __call__(self, other, *args, name=None, dtype=None, repetitions=None, key=None, joiner=None, join_function=None, wrap_function=None, suffix=None, prefix=None, multiline=None, parser=None, handler=None, capturing=None, default=None, allow_inner_captures=None, **kwargs):
        """Wraps self around other

        :param other:
        :type other: RegexPattern
        :return:
        :rtype:
        """
        ...

    def __repr__(self):
        """
        **LLM Docstring**

        Return a diagnostic representation containing the key, child count, and primitive pattern.

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        ...

    def __str__(self):
        """
        **LLM Docstring**

        Build and return the regex source string.

        :return: The regex source or textual representation constructed by the operation.
        :rtype: str
        """
        ...

    def __getitem__(self, item):
        """
        **LLM Docstring**

        Look up a directly named child by its key.

        :param item: the child key or array index/slice being accessed
        :type item: object

        :return: The named child or populated array portion selected by the index.
        :rtype: object
        """
        ...

    def match(self, txt, *args):
        """
        **LLM Docstring**

        Match the compiled pattern only at the beginning of the input.

        :param txt: the input text or text block to parse
        :type txt: object

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :return: match the compiled pattern only at the beginning of the input.
        :rtype: object
        """
        ...

    def fullmatch(self, txt, *args):
        """
        **LLM Docstring**

        Require the compiled pattern to match the complete input.

        :param txt: the input text or text block to parse
        :type txt: object

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :return: require the compiled pattern to match the complete input.
        :rtype: object
        """
        ...

    def search(self, txt, *args):
        """
        **LLM Docstring**

        Find the first occurrence of the compiled pattern in the input.

        :param txt: the input text or text block to parse
        :type txt: object

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :return: find the first occurrence of the compiled pattern in the input.
        :rtype: object
        """
        ...

    def findall(self, txt, *args):
        """
        **LLM Docstring**

        Return all non-overlapping matches of the compiled pattern.

        :param txt: the input text or text block to parse
        :type txt: object

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :return: return all non-overlapping matches of the compiled pattern.
        :rtype: object
        """
        ...

    def finditer(self, txt, *args):
        """
        **LLM Docstring**

        Iterate over match objects for all non-overlapping matches.

        :param txt: the input text or text block to parse
        :type txt: object

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :return: An iterator yielding the records described above.
        :rtype: object
        """
        ...

    def sub(self, rep, txt, *args):
        """
        **LLM Docstring**

        Replace matches using `re.sub`.

        :param rep: the replacement string or callable
        :type rep: object

        :param txt: the input text or text block to parse
        :type txt: object

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :return: replace matches using `re.sub`.
        :rtype: object
        """
        ...

    def subn(self, rep, txt, *args):
        """
        **LLM Docstring**

        Replace matches and return both the resulting text and replacement count.

        :param rep: the replacement string or callable
        :type rep: object

        :param txt: the input text or text block to parse
        :type txt: object

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :return: replace matches and return both the resulting text and replacement count.
        :rtype: object
        """
        ...

    def replace(self, txt, replacement, *args):
        """
        **LLM Docstring**

        Replace matches with a supplied replacement string or callable.

        :param txt: the input text or text block to parse
        :type txt: object

        :param replacement: the replacement string or callable
        :type replacement: object

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :return: replace matches with a supplied replacement string or callable.
        :rtype: object
        """
        ...

    def remove(self, txt, *args):
        """
        **LLM Docstring**

        Delete every match by replacing it with an empty string.

        :param txt: the input text or text block to parse
        :type txt: object

        :param args: positional arguments forwarded to the wrapped callable
        :type args: tuple

        :return: delete every match by replacing it with an empty string.
        :rtype: object
        """
        ...

def is_grouped(p):
    """Takes a string pattern and tries to check if it's already in a singular construct (usually grouped...)

    :param p: pattern
    :type p: str
    :return:
    :rtype:
    """
    ...

def group(p, no_capture=False):
    """
    **LLM Docstring**

    Wrap a pattern in a capturing group, or in a non-capturing group when `no_capture` is true.

    :param p: the regex source fragment to wrap
    :type p: object

    :param no_capture: whether the resulting regex must avoid a capturing group
    :type no_capture: object

    :return: The regex source or textual representation constructed by the operation.
    :rtype: str
    """
    ...

def non_capturing(p, *a, **kw):
    """
    **LLM Docstring**

    Wrap a pattern in a `(?:...)` group.

    :param p: the regex source fragment to wrap
    :type p: object

    :param a: positional arguments captured for the wrapper callable
    :type a: object

    :param kw: extra keyword arguments forwarded to the underlying stream constructor
    :type kw: object

    :return: The regex source or textual representation constructed by the operation.
    :rtype: str
    """
    ...

def optional(p, no_capture=False):
    """
    **LLM Docstring**

    Apply `?` to an already grouped atom, otherwise first place the pattern in a non-capturing group.

    :param p: the regex source fragment to wrap
    :type p: object

    :param no_capture: whether the resulting regex must avoid a capturing group
    :type no_capture: object

    :return: The regex source or textual representation constructed by the operation.
    :rtype: str
    """
    ...

def alternatives(p, no_capture=False):
    """
    **LLM Docstring**

    Ensure an alternation expression is grouped, choosing capturing or non-capturing grouping from `no_capture`.

    :param p: the regex source fragment to wrap
    :type p: object

    :param no_capture: whether the resulting regex must avoid a capturing group
    :type no_capture: object

    :return: The regex source or textual representation constructed by the operation.
    :rtype: str
    """
    ...

def shortest(p, no_capture=False):
    """
    **LLM Docstring**

    Convert a pattern to a lazy zero-or-more expression, or make an existing `*`/`+` quantifier lazy.

    :param p: the regex source fragment to wrap
    :type p: object

    :param no_capture: whether the resulting regex must avoid a capturing group
    :type no_capture: object

    :return: The regex source or textual representation constructed by the operation.
    :rtype: str
    """
    ...

def repeating(p, min=1, max=None, no_capture=False):
    """
    **LLM Docstring**

    Apply `*`, `+`, `{n}`, `{n,}`, or `{n,m}` according to the supplied bounds, then capture the entire repetition unless `no_capture` is true.

    :param p: the regex source fragment to wrap
    :type p: object

    :param min: the minimum repetition count, or `None` for zero
    :type min: object

    :param max: the maximum repetition count, or `None` for no upper bound
    :type max: object

    :param no_capture: whether the resulting regex must avoid a capturing group
    :type no_capture: object

    :return: The regex source or textual representation constructed by the operation.
    :rtype: str
    """
    ...

def duplicated(p, num, riffle='', no_capture=False):
    """
    **LLM Docstring**

    Repeat the same pattern exactly `num` times with `riffle` inserted between copies.

    :param p: the regex source fragment to wrap
    :type p: object

    :param num: the number of matches, blocks, elements, or copies requested
    :type num: object

    :param riffle: text inserted between duplicated pattern copies
    :type riffle: object

    :param no_capture: whether the resulting regex must avoid a capturing group
    :type no_capture: object

    :return: The regex source or textual representation constructed by the operation.
    :rtype: str
    """
    ...

def named(p, n, no_capture=False):
    """
    **LLM Docstring**

    Wrap a pattern in a Python named capture, or suppress the named capture when `no_capture` is true.

    :param p: the regex source fragment to wrap
    :type p: object

    :param n: the requested count or fixed repetition count
    :type n: object

    :param no_capture: whether the resulting regex must avoid a capturing group
    :type no_capture: object

    :return: The regex source or textual representation constructed by the operation.
    :rtype: str
    """
    ...
grp_p = group
Capturing = RegexPattern(grp_p, 'Capturing', capturing=True)
Capturing.__name__ = 'Capturing'
Capturing.__doc__ = '\n    Represents a capturing group in a RegexPattern\n    '
non_cap_p = non_capturing
NonCapturing = RegexPattern(non_cap_p, 'NonCapturing', dtype=DisappearingType)
NonCapturing.__name__ = 'NonCapturing'
NonCapturing.__doc__ = '\n    Represents something that should not be captured in a RegexPattern\n    '
op_p = optional

def opnb_p(p, no_capture=False):
    """
    **LLM Docstring**

    Wrap a pattern in an optional non-capturing group.

    :param p: the regex source fragment to wrap
    :type p: object

    :param no_capture: whether the resulting regex must avoid a capturing group
    :type no_capture: object

    :return: The regex source or textual representation constructed by the operation.
    :rtype: str
    """
    ...
Optional = RegexPattern(optional, 'Optional')
Optional.__name__ = 'Optional'
Optional.__doc__ = '\n    Represents something that should be optional in a RegexPattern\n    '
Alternatives = RegexPattern(alternatives, joiner='|')
Alternatives.__name__ = 'Alternatives'
Alternatives.__doc__ = '\n    Represents a set of alternatives in a RegexPattern\n    '
lm_p = repeating
Longest = RegexPattern(lm_p, 'Longest')
Longest.__name__ = 'Longest'
Longest.__doc__ = '\n    Represents that the longest match of the enclosed pattern should be searched for\n    '
sm_p = shortest
Shortest = RegexPattern(sm_p, 'Shortest')
Shortest.__name__ = 'Shortest'
Shortest.__doc__ = '\n    Represents that the shortest match of the enclosed pattern should be searched for\n    '

def wrap_repeats(self, min=None, max=None, no_capture=None):
    """
    **LLM Docstring**

    Store repetition bounds on a `RegexPattern` when the `Repeating` wrapper is applied.

    :param min: the minimum repetition count, or `None` for zero
    :type min: object

    :param max: the maximum repetition count, or `None` for no upper bound
    :type max: object

    :param no_capture: whether the resulting regex must avoid a capturing group
    :type no_capture: object

    :return: None.
    :rtype: None
    """
    ...
Repeating = RegexPattern(repeating, 'Repeating', wrapper_function=wrap_repeats)
Repeating.__name__ = 'Repeating'
Repeating.__doc__ = '\n    Represents that the patten can be repeated\n    '

def wrap_name(self, n):
    """
    **LLM Docstring**

    Assign a capture key and, when unnamed, use that key as the node's descriptive name.

    :param n: the requested count or fixed repetition count
    :type n: object

    :return: None.
    :rtype: None
    """
    ...
Named = RegexPattern(named, 'Named', wrapper_function=wrap_name, capturing=True)
Named.__name__ = 'Named'
Named.__doc__ = '\n    Represents a named group. These are _always_ captured, to the exclusion of all else.\n    '

def wrap_duplicate_type(self, n, riffle=''):
    """
    **LLM Docstring**

    Update the node's declared dtype shape to prepend the fixed duplication count.

    :param n: the requested count or fixed repetition count
    :type n: object

    :param riffle: text inserted between duplicated pattern copies
    :type riffle: object

    :return: None.
    :rtype: None
    """
    ...
Duplicated = RegexPattern(duplicated, 'Duplicated', wrapper_function=wrap_duplicate_type)
Duplicated.__name__ = 'Duplicated'
Duplicated.__doc__ = '\n    Represents an explicitly duplicated pattern\n    '
pc_p = lambda p, no_capture=False: '[' + p + ']'
PatternClass = RegexPattern(pc_p, 'PatternClass')
PatternClass.__name__ = 'PatternClass'
PatternClass.__doc__ = '\n    Represents a pattern class, for wrapping other patterns\n'
parened_p = lambda p, no_capture=False: '\\(' + p + '\\)'
Parenthesized = RegexPattern(parened_p, 'Parenthesized')
Parenthesized.__name__ = 'Parenthesized'
Parenthesized.__doc__ = '\n    Represents that something should be wrapped in parentheses, not treated as Capturing\n    '
any_p = '.'
Any = RegexPattern(any_p, 'Any')
Any.__name__ = 'Any'
Any.__doc__ = '\n    Represents any character\n    '
start_p = '^'
StartOfString = RegexPattern(start_p, 'StartOfString')
StartOfString.__name__ = 'StartOfString'
StartOfString.__doc__ = ''
end_p = '$'
EndOfString = RegexPattern(end_p, 'EndOfString')
EndOfString.__name__ = 'EndOfString'
EndOfString.__doc__ = ''
sign_p = '[\\+\\-]'
Sign = RegexPattern(sign_p, 'Sign')
Sign.__name__ = 'Sign'
Sign.__doc__ = '\n    Represents a +/- sign\n    '
paren_p = '\\(' + '.*?' + '\\)'
num_p = opnb_p(sign_p) + '\\d*\\.\\d+'
Number = RegexPattern(num_p, 'Number', dtype=float)
Number.__name__ = 'Number'
Number.__doc__ = '\n    Represents a real number, like -1.23434; doesn\'t support "E" notation\n    '
num_p = opnb_p(sign_p) + '\\d+\\.\\d*'
IntBaseNumber = RegexPattern(num_p, 'IntBaseNumber', dtype=float)
IntBaseNumber.__name__ = 'IntBaseNumber'
IntBaseNumber.__doc__ = '\n    Represents a real number with definite integer part, like -1.23434 or 0.; doesn\'t support "E" notation\n    '
int_p = opnb_p(sign_p) + '\\d+'
Integer = RegexPattern(int_p, 'Integer', dtype=int)
Integer.__name__ = 'Integer'
Integer.__doc__ = '\n    Represents an integer\n    '
posint_p = '\\d+'
PositiveInteger = RegexPattern(posint_p, 'PositiveInteger', dtype=int)
PositiveInteger.__name__ = 'PositiveInteger'
PositiveInteger.__doc__ = '\n    Represents a positive integer (i.e. just a string of digits)\n    '
ascii_p = '[a-zA-Z]'
ASCIILetter = RegexPattern(ascii_p, 'ASCIILetter', dtype=str)
ASCIILetter.__name__ = 'ASCIILetter'
ASCIILetter.__doc__ = '\n    Represents a single ASCII letter\n    '
name_p = ascii_p + '{1,2}'
AtomName = RegexPattern(name_p, 'AtomName', dtype=str)
AtomName.__name__ = 'AtomName'
AtomName.__doc__ = '\n    Represents an atom symbol like Cl or O (this is misnamed, I know)\n    '
ws_char_class = '(?!\\n)\\s'
WhitespaceCharacter = RegexPattern(ws_char_class, 'WhitespaceCharacter', dtype=str)
WhitespaceCharacter.__name__ = 'WhitespaceCharacter'
WhitespaceCharacter.__doc__ = '\n    Represents a single whitespace character\n    '
ws_p = non_capturing(ws_char_class) + '*'
wsr_p = non_capturing(ws_char_class) + '+'
Whitespace = RegexPattern(ws_p, 'Whitespace', dtype=str)
Whitespace.__name__ = 'WhitespaceCharacter'
Whitespace.__doc__ = '\n    Represents a block of whitespace\n    '
WordCharacter = RegexPattern('\\w', 'WordCharacter', dtype=str)
WordCharacter.__name__ = 'WordCharacter'
WordCharacter.__doc__ = '\n    Represents a single number or letter (i.e. non-whitespace)\n    '
Word = RegexPattern('[^\\W\\d_]\\w*', 'Word', dtype=str)
Word.__name__ = 'Word'
Word.__doc__ = '\n    Represents a block of WordCharacters\n    '
VariableName = RegexPattern((ASCIILetter, Word), joiner='', dtype=str)
VariableName.__name__ = 'VariableName'
VariableName.__doc__ = '\n    Represents a possible variable name sans underscored, basically an ASCIILetter and then a word\n    '
ascii_punc_char_class = '\\.,<>?/\'\\";:{}\\[\\]\\+=\\(\\)\\*&\\^%$#@!~`'
ASCIIPunctuation = RegexPattern(ascii_punc_char_class, 'ASCIIPunctuation', dtype=str)
ASCIIPunctuation.__name__ = 'ASCIIPunctuation'
ASCIIPunctuation.__doc__ = '\n    Represents a single piece of punctuation\n    '
cart_p = ws_p.join([grp_p(num_p)] * 3)
CartesianPoint = RegexPattern(cart_p, 'CartesianPoint', dtype=(float, (3,)))
CartesianPoint.__name__ = 'CartesianPoint'
CartesianPoint.__doc__ = "\n    Represents a 'point', i.e. 3 numbers separated by whitespace\n    "
acart_p = '(' + int_p + ')' + ws_p + cart_p
IntXYZLine = RegexPattern(acart_p, 'IntXYZLine', dtype=(int, (float, (3,))))
IntXYZLine.__name__ = 'IntXYZLine'
aNcart_p = '(' + name_p + ')' + ws_p + cart_p
XYZLine = RegexPattern(aNcart_p, 'XYZLine', dtype=(str, (float, (3,))))
XYZLine.__name__ = 'XYZLine'
Empty = RegexPattern('', 'Empty')
Empty.__name__ = 'Empty'
Empty.__doc__ = "\n    Represents an empty pattern...I can't remember why this is here\n    "
Newline = RegexPattern('\\n', 'Newline', dtype=str)
Newline.__name__ = 'Newline'
Newline.__doc__ = '\n    Represents a newline character\n    '
ZMatPattern = Capturing(AtomName)
ZMatPattern.name = 'ZMatPattern'
ZMatPattern.__name__ = 'ZMatPattern'
ZMatPattern.__doc__ = '\n    Represents Z-matrix block\n    '