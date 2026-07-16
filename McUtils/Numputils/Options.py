"""
Defines options for different numerical things
"""

__all__ = [
    "Options"
]

import numpy as np

class OptionsContainer:
    """
    A singleton Options object that can be used to configure options for numerical stuff
    """

    NORM_ZERO_THRESH = None
    ZERO_THRESHOLD = 1.0e-8
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
        # just here so I can modify later
        return self.ZERO_THRESHOLD
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
        self.ZERO_THRESHOLD = v

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
        if self.NORM_ZERO_THRESH is None:
            return self.zero_threshold
        else:
            return self.NORM_ZERO_THRESH
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
        self.NORM_ZERO_THRESH = v

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
        if self.ZERO_PLACEHOLDER is None:
            return self.zero_threshold
        else:
            return self.ZERO_PLACEHOLDER
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
        self.ZERO_PLACEHOLDER = v

Options = OptionsContainer()
Options.__name__ = "Options"
Options.__doc__ = OptionsContainer.__doc__