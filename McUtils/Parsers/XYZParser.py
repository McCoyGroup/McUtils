import io

import numpy as np
from .FileStreamer import FileStreamReader, FileStreamerTag, FileLineByLineReader
from . import RegexPatterns as reps

__all__ = [
    "XYZParser"
]

class XYZParser(FileLineByLineReader):
    def __init__(self, *args, **kwds):
        super().__init__(*args, max_nesting_depth=0, **kwds)
    def check_tag(self, line:str, depth:int=0, active_tag=None, label:str=None, history:list[str]=None):
        if isinstance(label, int):
            check_block_end = True
            if len(history) < label:
                return None
        else:
            check_block_end = (history is None or len(history) == 0)

        if len(line.strip()) == 0:
            if history is None or len(history) == 0:
                return self.LineReaderTags.SKIP
            else:
                prev = history[-1]
                if isinstance(prev, int):
                    return None
                else:
                    return self.LineReaderTags.BLOCK_END
        elif check_block_end and reps.PositiveInteger.match(line):
            return self.LineReaderTags.BLOCK_START, int(line.strip()), None
        else:
            return None

    # WhitespaceSplit = reps.RegexPattern([reps.Whitespace, reps.Number])
    def handle_block(self, label:'str|None', block_data, join=True, depth=0,
                     number_pattern=None,
                     label_pattern=None,
                     simple_format=False):

        if label is None:
            comment = None
        else:
            if len(block_data) > label:
                comment = block_data[0]
                block_data = block_data[1:]
            else:
                comment = None

        if simple_format:
            if number_pattern is None:
                number_pattern = reps.Number
            elif isinstance(number_pattern, str):
                number_pattern = reps.RegexPattern(number_pattern)
            tags = [
                reps.Word.match(b)
                for b in block_data
            ]
            nums = np.array([
                number_pattern.finditer(b)
                for b in block_data
                ])
        else:
            if number_pattern is None:
                number_pattern = reps.Number
            elif isinstance(number_pattern, str):
                number_pattern = reps.RegexPattern(number_pattern)
            split_first = reps.RegexPattern([reps.Whitespace, number_pattern])
            nums = []
            tags = []
            for b in block_data:
                match = split_first.search(b)
                if match is None:
                    raise ValueError(f"couldn't parse line {b}")
                start = match.start()
                tags.append(b[:start].strip())
                nums.append(number_pattern.findall(b[start:]))
        if comment is None:
            comment = ''
        return comment, tags, np.array(nums).astype(float)

    # MAX_BLOCKS = 10
    def parse(self, max_blocks=None):
        supplier = iter(self)
        if max_blocks is None:
            blocks = list(supplier)
        else:
            blocks = []
            for i in range(max_blocks):
                blocks.append(next(supplier))
        return [
            b
                if not isinstance(b, dict) else
            list(b.values())[0]
            for b in blocks
        ]

    # @classmethod
    # def _check_is_int(cls, tag):
    #     return PositiveInteger.match(tag.strip())
    # def find_block(self):
    #     int_tag = self.get_tagged_block(None, '\n',
    #                                     validator=self._check_is_int)
    #     if int_tag is None: return None
    #     num_follows = int(int_tag.strip())
    #     if not self.has_comments:
    #         num_follows = num_follows - 1
    #     full_tag = FileStreamerTag('\n', follow_ups=['\n']*num_follows, skip_tag=True)
    #     return self.get_tagged_block(None, full_tag, allow_terminal=True)
    #
    # def parse_xyz_block(self, block, include_comment=True):
    #     if self.has_comments:
    #         comment, block = block.split('\n', 1)
    #     else:
    #         comment = None
    #     atoms = np.loadtxt(io.StringIO(block), usecols=[0], dtype=str)
    #     coords = np.loadtxt(io.StringIO(block), usecols=[1, 2, 3])
    #
    #     if include_comment:
    #         return comment, atoms, coords
    #     else:
    #         return atoms, coords
    #
    # def parse(self, max_blocks=None, include_comment=True):
    #     blocks = []
    #     block = self.find_block()
    #     if block is None:
    #         return None
    #     if max_blocks is not None:
    #         blocks.append(self.parse_xyz_block(block, include_comment=include_comment))
    #         for i in range(max_blocks-1):
    #             block = self.find_block()
    #             if block is None:
    #                 break
    #             blocks.append(self.parse_xyz_block(block, include_comment=include_comment))
    #     else:
    #         while block is not None:
    #             blocks.append(self.parse_xyz_block(block, include_comment=include_comment))
    #             block = self.find_block()
    #
    #     return blocks

