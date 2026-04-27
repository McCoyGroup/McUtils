import io

import numpy as np
from .FileStreamer import FileStreamReader, FileStreamerTag
from .RegexPatterns import PositiveInteger

__all__ = [
    "XYZParser"
]

class XYZParser(FileStreamReader):
    def __init__(self, file, has_comments=True, **kw):
        self.has_comments = has_comments
        super().__init__(file, **kw)
    @classmethod
    def _check_is_int(cls, tag):
        return PositiveInteger.match(tag.strip())
    def find_block(self):
        int_tag = self.get_tagged_block(None, '\n',
                                        tag_validator=self._check_is_int)
        if int_tag is None: return None
        num_follows = int(int_tag.strip())
        if not self.has_comments:
            num_follows = num_follows - 1
        full_tag = FileStreamerTag('\n', follow_ups=['\n']*num_follows, skip_tag=True)
        return self.get_tagged_block(None, full_tag, allow_terminal=True)

    def parse_xyz_block(self, block, include_comment=True):
        if self.has_comments:
            comment, block = block.split('\n', 1)
        else:
            comment = None
        atoms = np.loadtxt(io.StringIO(block), usecols=[0], dtype=str)
        coords = np.loadtxt(io.StringIO(block), usecols=[1, 2, 3])

        if include_comment:
            return comment, atoms, coords
        else:
            return atoms, coords

    def parse(self, max_blocks=None, include_comment=True):
        blocks = []
        block = self.find_block()
        if max_blocks is not None:
            blocks.append(self.parse_xyz_block(block, include_comment=include_comment))
            for i in range(max_blocks-1):
                block = self.find_block()
                if block is None:
                    break
                blocks.append(self.parse_xyz_block(block, include_comment=include_comment))
        else:
            while block is not None:
                blocks.append(self.parse_xyz_block(block, include_comment=include_comment))
                block = self.find_block()

        return blocks

