"""
Implements all of the Taylor-series derived functionality in Zachary (i.e. all the finite-difference stuff and the function expansions)
"""
from .Derivatives import *
from .FunctionExpansions import *
__all__ = ['FiniteDifferenceFunction', 'FiniteDifferenceError', 'finite_difference', 'FiniteDifference1D', 'RegularGridFiniteDifference', 'IrregularGridFiniteDifference', 'FiniteDifferenceData', 'FiniteDifferenceMatrix', 'FunctionExpansion', 'FiniteDifferenceDerivative']
from .FiniteDifferenceFunction import *