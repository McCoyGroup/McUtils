import io
import numpy as np
from .FileStreamer import FileStreamReader, FileStreamerTag, FileLineByLineReader
from . import RegexPatterns as reps
__all__ = ['XYZParser']

class XYZParser(FileLineByLineReader):

    def __init__(self, *args, **kwds):
        ...

    def check_tag(self, line: str, depth: int=0, active_tag=None, label: str=None, history: list[str]=None):
        ...

    def handle_block(self, label: 'str|None', block_data, join=True, depth=0, number_pattern=None, label_pattern=None, simple_format=False):
        ...

    def parse(self, max_blocks=None):
        ...