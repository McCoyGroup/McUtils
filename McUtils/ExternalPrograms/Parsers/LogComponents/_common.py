"""
Helpers shared by the per-program ``*LogComponents`` modules.
"""
from ....Parsers import Integer

__all__ = ["strip_recursive"]


def strip_recursive(at_list):
    """
    Recursively strip whitespace (and leading integer labels) from every string in a
    nested list.

    :param at_list: the (possibly nested) list of strings
    :type at_list: list
    :return: the cleaned list
    :rtype: list
    """
    return [
        Integer.remove(s.strip()) if isinstance(s, str) else strip_recursive(s)
        for s in at_list
    ]
