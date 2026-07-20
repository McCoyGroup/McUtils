"""
Defines options for different numerical things
"""
__all__ = ['Options']
import numpy as np

class OptionsContainer:
    """
    A singleton Options object that can be used to configure options for numerical stuff
    """
    NORM_ZERO_THRESH = None
    ZERO_THRESHOLD = 1e-08
    ZERO_PLACEHOLDER = None

    @property
    def zero_threshold(self):
        """
        **LLM Docstring**

        Threshold below which a numerical value is treated as zero.

        Backed by the `ZERO_THRESHOLD` class attribute; exposed as a property so the
        default can be swapped out later without changing call sites.

        :return: the current zero threshold
        :rtype: float
        """
        ...

    @zero_threshold.setter
    def zero_threshold(self, v):
        """
        **LLM Docstring**

        Threshold below which a numerical value is treated as zero.

        Backed by the `ZERO_THRESHOLD` class attribute; exposed as a property so the
        default can be swapped out later without changing call sites.

        :return: the current zero threshold
        :rtype: float
        """
        ...

    @property
    def norm_zero_threshold(self):
        """
        **LLM Docstring**

        Threshold below which a vector *norm* is treated as zero.

        Falls back to `zero_threshold` when `NORM_ZERO_THRESH` has not been set, so
        norm-specific tolerances can be tuned independently when needed.

        :return: the current norm-zero threshold
        :rtype: float
        """
        ...

    @norm_zero_threshold.setter
    def norm_zero_threshold(self, v):
        """
        **LLM Docstring**

        Threshold below which a vector *norm* is treated as zero.

        Falls back to `zero_threshold` when `NORM_ZERO_THRESH` has not been set, so
        norm-specific tolerances can be tuned independently when needed.

        :return: the current norm-zero threshold
        :rtype: float
        """
        ...

    @property
    def zero_placeholder(self):
        """
        **LLM Docstring**

        Placeholder value substituted in place of a true zero (e.g. to avoid
        divide-by-zero).

        Falls back to `zero_threshold` when `ZERO_PLACEHOLDER` has not been set.

        :return: the current zero placeholder
        :rtype: float
        """
        ...

    @zero_placeholder.setter
    def zero_placeholder(self, v):
        """
        **LLM Docstring**

        Placeholder value substituted in place of a true zero (e.g. to avoid
        divide-by-zero).

        Falls back to `zero_threshold` when `ZERO_PLACEHOLDER` has not been set.

        :return: the current zero placeholder
        :rtype: float
        """
        ...
Options = OptionsContainer()
Options.__name__ = 'Options'
Options.__doc__ = OptionsContainer.__doc__