"""
Utilities for writing parsers of structured text.
An entirely standalone package which is used extensively by `GaussianInterface`.
Three main threads are handled:

1. A `FileStreamer` interface which allows for efficient searching for blocks of text
   in large files with no pattern matching
2. A `Regex` interface that provides declarative tools for building and manipulating a regular expression
   as a python tree
3. A `StringParser`/`StructuredTypeArray` interface that takes the `Regex` tools and allows for automatic
   construction of complicated `NumPy`-backed arrays from the parsed data. Generally works well but the
   problem is complicated and there are no doubt many unhandled edge cases.
   This is used extensively with (1.) to provide efficient parsing of data from Gaussian `.log` files by
   using a streamer to match chunks and a parser to extract data from the matched chunks.
"""
__all__ = ['FileStreamReader', 'FileStreamCheckPoint', 'FileStreamerTag', 'FileStreamReaderException', 'StringStreamReader', 'FileLineByLineReader', 'StringLineByLineReader', 'StringParser', 'StringParserException', 'RegexPattern', 'Capturing', 'NonCapturing', 'Optional', 'Alternatives', 'Longest', 'Shortest', 'Repeating', 'Duplicated', 'PatternClass', 'Parenthesized', 'Named', 'StartOfString', 'EndOfString', 'Any', 'Sign', 'Number', 'IntBaseNumber', 'Integer', 'PositiveInteger', 'ASCIILetter', 'AtomName', 'WhitespaceCharacter', 'Whitespace', 'Word', 'WordCharacter', 'VariableName', 'CartesianPoint', 'IntXYZLine', 'XYZLine', 'Empty', 'Newline', 'ZMatPattern', 'StructuredType', 'StructuredTypeArray', 'DisappearingType', 'XYZBlock', 'XYZParser', 'TeXParser', 'BibTeXParser']
from .FileStreamer import *
from .StringParser import *
from .RegexPatterns import *
from .StructuredType import *
from .Parsers import *
from .XYZParser import *
from .TeXParser import *