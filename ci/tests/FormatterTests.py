import collections
import itertools
import re

from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Formatters import *
import os, inspect
import pprint

class FormatterTests(TestCase):

    @validationTest
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

    @validationTest
    def test_TeXTranspile(self):
        print()

        # import McUtils.Devutils as dev
        # print(dev.split_path('/ASDa/b/d/c/d/d', 3))
        # print(
        #     dev.drop_directory_prefix('', '/ASDa/b/d/c/d/d')
        # )
        # return


        transpiler = TeXTranspiler(
            TestManager.test_data('TeXPaper/main.tex'),
            figure_renaming_function=TeXTranspiler.figure_counter(),
            bib_renaming_function=lambda _:"bibliography.bib",
            bib_merge_function=TeXTranspiler.add_bibs,
            bib_cleanup_function=TeXTranspiler.pruned_bib
        )
        # print(transpiler.create_flat_tex(include_aux=False))
        # body, aux = transpiler.create_flat_tex(include_aux=True)
        # print(body)
        # pprint.pprint(aux)

        # pprint.pprint(
        #     transpiler.create_label_map(body)
        # )
        #
        # pprint.pprint(
        #     transpiler.create_ref_map(body)
        # )

        transpiler.transpile(os.path.expanduser('~/Desktop/wat'), allow_missing_styles=True)

    @validationTest
    def test_TeXWriter(self):
        array = [[1, 2, 3], [4, 500000, 6]]
        arr_tex = TeX.wrap_parens(TeX.Array(array))
        print(arr_tex.format_tex())
        o = TeX.Symbol('omega')
        i = TeX.Symbol('i')
        f = TeX.Symbol(TeX.bold('f'))
        sum = TeX.Symbol('sum')
        expr = sum[i:0:5] | o ** 2
        expr = f.Eq(arr_tex)
        print(TeX.Equation(expr, label='fmat').format_tex())

    @validationTest
    def test_FormatSpec(self):
        import inspect

        fmt = inspect.cleandoc("""
            ### My Data
            {$:b=loop_template(add_temp, l1, l2, joiner=j)}
            {$:b}
            {$:len(b)**2}
            {$:len(c:=loop_template(add_temp, l1, l2, joiner=j))**2}
            {$:c}
        
            """)

        print("",
              TemplateFormatter().format(fmt, param=2, l1=[1, 2, 3], l2=[4, 5, 6], add_temp='{} + {}', j=" + "),
              sep="\n"
              )