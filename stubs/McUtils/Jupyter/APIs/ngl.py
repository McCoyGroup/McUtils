import numpy as np
from ..JHTML import JHTML, HTML, HTMLWidgets
__all__ = ['NGLAPI']
__reload_hook__ = ['..JHTML', '..Apps']

class NGLAPI:
    _api_versions = {}

    @classmethod
    def load(cls, version='v5'):
        ...