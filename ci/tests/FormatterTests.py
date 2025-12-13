from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Formatters import *
import os, inspect

class FormatterTests(TestCase):

    @debugTest
    def test_TreeToTable(self):
        print()
        print(
            TableFormatter.format_tree(
                {
                    'A': {
                        "a": {'x': [0, 1], 'y': [1, 2], 'z': [2, 3]},
                        "b": {'x': [0, 1], 'y': [-1, 0], 'z': [-2, -1]},
                        "c": {'x': [4, 5], 'y': [5, 6], 'z': [6, 7]},
                    },
                    'J': {
                        "a": {'x': [0, -1], 'y': [1, 0], 'z': [2, 1]},
                        "b": {'x': [10, 9], 'y': [-11, -12], 'z': [-21, -22]},
                        "c": {'x': [14, 13], 'y': [15, 14], 'z': [16, 15]},
                    }
                },
                column_join="|",
                header_normalization_function=lambda headers,spans:(
                    headers + [["cm-1"]*len(headers[-1])],
                    spans + [spans[-1]]
                )
            )
        )
