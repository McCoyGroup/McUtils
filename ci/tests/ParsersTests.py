from McUtils.McUtils.Parsers.TeXParser import BibItemParser
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Parsers import *
import sys, os, numpy as np

class ParserTests(TestCase):

    @validationTest
    def test_RegexGroups(self):
        # tests whether we capture subgroups or not (by default _not_)

        test_str = "1 2 3 4 a b c d "
        pattern = RegexPattern(
            (
                Capturing(
                    Repeating(
                        Capturing(Repeating(PositiveInteger, 2, 2, suffix=Optional(Whitespace)))
                    )
                ),
                Repeating(Capturing(ASCIILetter), suffix=Whitespace)
            )
        )
        self.assertEquals(len(pattern.search(test_str).groups()), 2)

    @validationTest
    def test_OptScan(self):

        eigsPattern = RegexPattern(
            (
                "Eigenvalues --",
                Repeating(Capturing(Number), suffix=Optional(Whitespace))
            ),
            joiner=Whitespace
        )

        coordsPattern = RegexPattern(
            (
                Capturing(VariableName),
                Repeating(Capturing(Number), suffix=Optional(Whitespace))
            ),
            prefix=Whitespace,
            joiner=Whitespace
        )

        full_pattern = RegexPattern(
            (
                Named(eigsPattern,
                      "Eigenvalues"
                      #parser=lambda t: np.array(Number.findall(t), 'float')
                      ),
                Named(Repeating(coordsPattern, suffix=Optional(Newline)), "Coordinates")
            ),
            joiner=Newline
        )

        with open(TestManager.test_data('scan_params_test.txt')) as test:
            test_str = test.read()

        parser = StringParser(full_pattern)
        parse_res = parser.parse_all(test_str)
        parse_single = parser.parse(test_str)
        parse_its = list(parser.parse_iter(test_str))

        self.assertEquals(parse_res.shape, [(4, 5), [(4, 32), (4, 32, 5)]])
        self.assertIsInstance(parse_res["Coordinates"][1].array, np.ndarray)
        self.assertEquals(int(parse_res["Coordinates"][1, 0].sum()), 3230)

        # print(parse_single["Coordinates"], file = sys.stderr)

    @validationTest
    def test_XYZ(self):

        with open(TestManager.test_data('test_100.xyz')) as test:
            test_str = test.read()

        # print(
        #     "\n".join(test_str.splitlines()[:15]),
        #     "\n",
        #     XYZParser.regex.search(test_str),
        #     file=sys.stderr
        # )

        res = XYZParser.parse_all(
            test_str
        )
        # print(
        #     res["Atoms"],
        #     file=sys.stderr
        # )

        atom_coords = res["Atoms"].array[1].array
        self.assertIsInstance(atom_coords, np.ndarray)
        self.assertEquals(atom_coords.shape, (100, 13, 3))

    @validationTest
    def test_BasicParse(self):
        regex = RegexPattern(
            (
                Named(PositiveInteger, "NumAtoms"),
                Named(
                    Repeating(Any, min = None), "Comment", dtype=str
                ),
                Named(
                    Repeating(
                        Capturing(
                            Repeating(Capturing(Number), 3, 3, prefix = Whitespace, suffix = Optional(Whitespace)),
                            handler= StringParser.array_handler(shape = (None, 3))
                        ),
                        suffix = Optional(Newline)
                    ),
                    "Atoms"
                )
            ),
            "XYZ",
            joiner=Newline
        )

        with open(TestManager.test_data('coord_parse.txt')) as test:
            test_str = test.read()

        res = StringParser(regex).parse(test_str)

        comment_string = res["Comment"].array[0]
        self.assertTrue('comment' in comment_string)
        self.assertEquals(res['Atoms'].array.shape, (4, 3))

        # print(
        #     # regex.dtype,
        #     "",
        #     res,
        #     print(repr(str(regex))),
        #     repr(regex.search(test_str).group("NumAtoms")),
        #     res["NumAtoms"].array,
        #     res['Atoms'].array,
        #     file = sys.stderr,
        #     sep="\n",
        #     end="\n"
        # )



    @validationTest
    def test_ParseTex(self):
        import McUtils.Devutils as dev
        root_text = dev.read_file(TestManager.test_data('samp.tex'))
        with TeXParser(TestManager.test_data('samp.tex')) as parser:
            print()
            for i in range(6):
                (s, e), text = parser.parse_tex_call(return_end_points=True)
                print((s, e), text)
                if e > 0:
                    print(root_text[s:e])
                else:
                    print(root_text[s:])

        with TeXParser(TestManager.test_data('samp.tex')) as parser:
            print()
            # print(parser.parse_tex_call("func"))
            (s, e), text = parser.parse_tex_environment(return_end_points=True)
            print((s, e), text)
            if e > 0:
                print(root_text[s:e])
            else:
                print(root_text[s:])

    @debugTest
    def test_ParseBib(self):
        import McUtils.Devutils as dev

        bib_file = TestManager.test_data('TeXPaper/bibliography/library.bib')
        root_text = dev.read_file(bib_file)

        samp_bib = """
@misc{MAB-pres-APS-2024,
   author = {Mark A Boyer and Sibert III, Edwin L}
   month = {3},
   note = {American Physical Society March Meeting},
   title = {EXPLORING HYDROGEN BONDING THROUGH REDUCED DIMENSIONAL TREATMENTS IN OBLIQUE COORDINATES},
   year = {2024}
}
"""
        # with dev.StreamInterface(samp_bib, file_backed=True) as stream:
        #     with BibItemParser(stream) as item_parser:
        #         print(":::", item_parser.parse_bib_line())

        # return
        import pprint

        with BibTeXParser(bib_file) as parser:
            print()
            for i in range(2):
                (s, e), text = parser.parse_bib_item(return_end_points=True)
                if text is not None:
                    print("="*100)
                    print((s, e), text)
                    # if e > 0:
                    #     print(root_text[s:e])
                    # else:
                    #     print(root_text[s:])

                    pprint.pprint(parser.parse_bib_body(text))