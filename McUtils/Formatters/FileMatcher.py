import re, os

__all__ = [
    "StringMatcher",
    "MatchList",
    "FileMatcher"
]

class StringMatcher:
    """
    Defines a simple filter that applies to a file and determines whether or not it matches the pattern
    """

    def __init__(self, match_patterns, negative_match = False):
        """
        **LLM Docstring**

        Initialize `StringMatcher` state from the supplied configuration.

        :param match_patterns: regex, matcher, predicate, or iterable of match specifications
        :type match_patterns: object
        :param negative_match: whether to invert the match result
        :type negative_match: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        if isinstance(match_patterns, str):
            pattern = re.compile(match_patterns)
            self.matcher = lambda f, p = pattern: re.match(p, f)
        elif hasattr(re, "Pattern") and isinstance(match_patterns, re.Pattern): # re.Pattern is new as of python3.7...
            self.matcher = lambda f, p = match_patterns: re.match(p, f)
        elif type(match_patterns).__name__=="SRE_Pattern": # pre 3.7
            self.matcher = lambda f, p = match_patterns: re.match(p, f)
        elif isinstance(match_patterns, StringMatcher):
            self.matcher = match_patterns.matches
        elif callable(match_patterns):
            self.matcher = match_patterns
        else:
            ff = type(self)
            match_patterns = tuple(ff(m) if not isinstance(m, StringMatcher) else m for m in match_patterns)
            self.matcher = lambda f, p = match_patterns: all(m.matches(f) for m in p)

        self.negate = negative_match

    def matches(self, f):
        """
        **LLM Docstring**

        Evaluate the configured matcher against the input and apply optional negation.

        :param f: string or file path being tested
        :type f: object
        :return: whether the input satisfies the matcher after optional negation
        :rtype: bool
        """
        m = self.matcher(f)
        if self.negate:
            m = not m
        return m

class MatchList(StringMatcher):
    """
    Defines a set of matches that must be matched directly (uses `set` to make this basically a constant time check)
    """

    def __init__(self, *matches, negative_match = False):
        """
        **LLM Docstring**

        Initialize `MatchList` state from the supplied configuration.

        :param matches: additional positional values forwarded or collected by this operation
        :type matches: tuple
        :param negative_match: whether to invert the match result
        :type negative_match: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        self.match_list = set(matches)
        super().__init__(lambda f, m=self.test_match: m(f), negative_match = negative_match)
    def test_match(self, f):
        """
        **LLM Docstring**

        Test constant-time membership in the stored literal match set.

        :param f: string or file path being tested
        :type f: object
        :return: whether the input is present in the literal match set
        :rtype: bool
        """
        return f in self.match_list

class FileMatcher(StringMatcher):
    """
    Defines a filter that uses StringMatcher to specifically match files
    """

    def __init__(self, match_patterns, negative_match = False, use_basename = False):
        """
        **LLM Docstring**

        Initialize `FileMatcher` state from the supplied configuration.

        :param match_patterns: regex, matcher, predicate, or iterable of match specifications
        :type match_patterns: object
        :param negative_match: whether to invert the match result
        :type negative_match: object
        :param use_basename: whether matching is performed only on `os.path.basename(f)`
        :type use_basename: object
        :return: `None`; the operation mutates state, writes output, or raises by design.
        :rtype: None
        """
        super().__init__(match_patterns, negative_match = negative_match)
        self.use_basename = use_basename

    def matches(self, f):
        """
        **LLM Docstring**

        Evaluate the configured matcher against the input and apply optional negation.

        :param f: string or file path being tested
        :type f: object
        :return: whether the input satisfies the matcher after optional negation
        :rtype: bool
        """
        f_name = f if not self.use_basename else os.path.basename(f)
        return super().matches(f_name)