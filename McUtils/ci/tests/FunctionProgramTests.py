"""Portable function programs reuse the elementary function evaluation contract."""
import numpy as np

from McUtils.Zachary import Symbols
from McUtils.Zachary.Symbolic import ElementaryFunctions as ef


def test_function_programs_match_native_integer_and_float_evaluation():
    q, r = Symbols('q', 'r').vars
    functions = [q, q*(q-1), q*q + 3*r, (q+2)*(r-1),
                 ef.Sin(idx=0).compose(q+1), ef.Exp(idx=0), ef.Power(3, idx=0)]
    for dtype in [int, float]:
        points = np.array([[1, 2], [2, 4], [3, 1]], dtype=dtype)
        for function in functions:
            program = function.compile(mode='program')
            argument = points[..., 0 if function.idx is None else function.idx] if isinstance(function, ef.ElementaryFunction) else points
            np.testing.assert_array_equal(program(argument), function(argument))
