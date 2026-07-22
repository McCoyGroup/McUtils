"""
A place to store all utilities related to combinatorics.
Currently only contains a subpackage for working with permutations.
That package is used in the `BasisReps` work in `Psience`.

It handles both integer partitions and unique permutations.
It

Might be worth extending to handle more lattice-path stuff.
"""

__all__ = []
from .Permutations import *; from .Permutations import __all__ as exposed
__all__ += exposed
from .Sequences import *; from .Sequences import __all__ as exposed
__all__ += exposed
from .YoungTableaux import *; from .YoungTableaux import __all__ as exposed
__all__ += exposed