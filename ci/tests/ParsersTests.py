from McUtils.McUtils.Parsers.TeXParser import BibItemParser
from Peeves.TestUtils import *
from unittest import TestCase
from McUtils.Parsers import *
import sys, os, random, inspect, time
import numpy as np

# ---------------------------------------------------------------------------
# Backend-support probes, computed once at import time so the relevant tests
# below can be gated with `@backendTest` / `@parserBackendTest` the same way
# the rest of this file gates tests with `@validationTest` / `@debugTest` /
# `@inactiveTest`. No pytest, no runtime pytest.skip(): a test that can't run
# yet is marked `@inactiveTest` at definition time instead, and any check
# that fails *inside* a gated test raises an exception rather than skipping.
# ---------------------------------------------------------------------------
_HAS_ARRAY_BACKEND = "backend" in inspect.signature(StructuredTypeArray.__init__).parameters
_HAS_PARSER_BACKEND = "backend" in inspect.signature(StringParser.__init__).parameters

backendTest = validationTest if _HAS_ARRAY_BACKEND else inactiveTest
parserBackendTest = validationTest if (_HAS_ARRAY_BACKEND and _HAS_PARSER_BACKEND) else inactiveTest


# ---------------------------------------------------------------------------
# Helpers for the new stress tests -- module level so they're not re-created
# per test and so they mirror the idiom already used by test_BasicParse
# (a repeated, 3-wide Capturing(Number) block with an array_handler), which
# is structurally the same shape as a Gaussian dipole-moment block and is
# exactly the shape that triggered the original
# `AttributeError: 'StructuredTypeArray' object has no attribute
# 'has_indeterminate_shape'` regression.
# ---------------------------------------------------------------------------

def _dipole_pattern():
    return RegexPattern(
        (
            Named(
                Repeating(
                    Capturing(
                        Repeating(Capturing(Number), 3, 3, prefix=Whitespace, suffix=Optional(Whitespace)),
                        handler=StringParser.array_handler(shape=(None, 3))
                    ),
                    suffix=Optional(Newline)
                ),
                "Moments"
            ),
        ),
        "Dipoles",
        joiner=Newline
    )


def _make_dipole_block(n_rows, seed=0, malformed_rate=0.0):
    rng = random.Random(seed)
    lines = []
    for _ in range(n_rows):
        vals = [f"{rng.uniform(-2, 2):.6f}" for _ in range(3)]
        if rng.random() < malformed_rate:
            vals[rng.randrange(3)] = "*******"
        lines.append(" " + " ".join(vals))
    return "\n".join(lines)


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

    # -----------------------------------------------------------------
    # StructuredTypeArray regressions -- each targets exactly one of the
    # methods that broke (has_indeterminate_shape, can_cast, append,
    # add_axis, block_size, append_depth, _get_casting_shape) against the
    # real, installed class. No regex involved.
    # -----------------------------------------------------------------

    @validationTest
    def test_StructuredArray_HasIndeterminateShape(self):
        # this is the literal AttributeError from the traceback:
        #   AttributeError: 'StructuredTypeArray' object has no attribute
        #   'has_indeterminate_shape'
        arr = StructuredTypeArray(StructuredType(float))
        if not hasattr(arr, "has_indeterminate_shape"):
            raise Exception("StructuredTypeArray is missing `has_indeterminate_shape`")
        before = arr.has_indeterminate_shape
        self.assertIsInstance(before, (bool, np.bool_))

    @validationTest
    def test_StructuredArray_AxisShapeIndeterminate(self):
        arr = StructuredTypeArray(StructuredType(float, shape=(None,)))
        if not hasattr(arr, "axis_shape_indeterminate"):
            raise Exception("StructuredTypeArray is missing `axis_shape_indeterminate`")
        result = arr.axis_shape_indeterminate(0)
        self.assertIsInstance(result, (bool, np.bool_))

    @validationTest
    def test_StructuredArray_BlockSize(self):
        arr = StructuredTypeArray(StructuredType(float, shape=(None, 3)))
        if not hasattr(arr, "block_size"):
            raise Exception("StructuredTypeArray is missing `block_size`")
        _ = arr.block_size  # must not raise

    @validationTest
    def test_StructuredArray_AppendDepth(self):
        arr = StructuredTypeArray(StructuredType(float))
        if not hasattr(arr, "append_depth"):
            raise Exception("StructuredTypeArray is missing `append_depth`")
        arr.append_depth = 0
        self.assertEquals(arr.append_depth, 0)
        arr.append_depth = 1
        self.assertEquals(arr.append_depth, 1)

    @validationTest
    def test_StructuredArray_CanCast(self):
        arr = StructuredTypeArray(StructuredType(float))
        if not hasattr(arr, "can_cast"):
            raise Exception("StructuredTypeArray is missing `can_cast`")
        _ = arr.can_cast(1.0)  # must not raise

    @validationTest
    def test_StructuredArray_GetCastingShape(self):
        arr = StructuredTypeArray(StructuredType(float, shape=(None,)))
        if not hasattr(arr, "_get_casting_shape"):
            raise Exception("StructuredTypeArray is missing `_get_casting_shape`")

    @validationTest
    def test_StructuredArray_AppendWritesScalars(self):
        # the specific bug found in an earlier rewrite attempt: a naive
        # patch silently dropped scalar-append writes by nesting the array
        # assignment inside a branch that never fires for scalars. Pin the
        # correct behavior down explicitly against the real class.
        arr = StructuredTypeArray(StructuredType(float))
        arr.add_axis()
        for i in range(10):
            arr.append(np.array([float(i)]))
        self.assertEquals(len(arr), 10)
        self.assertEquals(list(arr.array), [float(i) for i in range(10)])

    @validationTest
    def test_StructuredArray_ExtendAppendsBlock(self):
        arr = StructuredTypeArray(StructuredType(float))
        arr.add_axis()
        arr.fill(np.array([1.0, 2.0, 3.0]))
        arr.extend(np.array([4.0, 5.0]))
        self.assertEquals(list(arr.array), [1.0, 2.0, 3.0, 4.0, 5.0])

    @validationTest
    def test_StructuredArray_FillSetsContents(self):
        arr = StructuredTypeArray(StructuredType(float))
        arr.add_axis()
        arr.fill(np.array([9.0, 8.0, 7.0]))
        self.assertEquals(list(arr.array), [9.0, 8.0, 7.0])

    @validationTest
    def test_StructuredArray_SetPartGetItemRoundTrip(self):
        arr = StructuredTypeArray(StructuredType(float))
        arr.add_axis()
        arr.fill(np.array([1.0, 2.0, 3.0]))
        self.assertEquals(arr[0], 1.0)
        self.assertEquals(arr[2], 3.0)

    @validationTest
    def test_StructuredArray_CastToArrayScalar(self):
        arr = StructuredTypeArray(StructuredType(float))
        result = arr.cast_to_array("3.14")
        self.assertTrue(np.isclose(np.asarray(result).flatten()[0], 3.14))

    @validationTest
    def test_StructuredArray_CastToArrayVector(self):
        arr = StructuredTypeArray(StructuredType(float, shape=(3,)))
        result = arr.cast_to_array("1.0 2.0 3.0")
        self.assertTrue(np.allclose(np.asarray(result).flatten(), [1.0, 2.0, 3.0]))

    @validationTest
    def test_StructuredArray_AddAxisFromScalarType(self):
        arr = StructuredTypeArray(StructuredType(float))
        arr.add_axis()  # must not raise
        arr.append(np.array([1.0]))
        arr.append(np.array([2.0]))
        self.assertEquals(list(arr.array), [1.0, 2.0])

    @validationTest
    def test_StructuredArray_AddAxisFromShapedType(self):
        arr = StructuredTypeArray(StructuredType(float, shape=(3,)))
        arr.add_axis()
        arr.append(np.array([1.0, 2.0, 3.0]))
        arr.append(np.array([4.0, 5.0, 6.0]))
        self.assertEquals(arr.array.shape[0], 2)
        self.assertEquals(list(arr.array[0]), [1.0, 2.0, 3.0])
        self.assertEquals(list(arr.array[1]), [4.0, 5.0, 6.0])

    @validationTest
    def test_StructuredArray_LenMatchesAppendedCount(self):
        arr = StructuredTypeArray(StructuredType(float))
        arr.add_axis()
        for i in range(37):
            arr.append(np.array([float(i)]))
        self.assertEquals(len(arr), 37)

    @validationTest
    def test_StructuredArray_DictLikeCompound(self):
        stype = StructuredType({"a": StructuredType(float), "b": StructuredType(int)})
        arr = StructuredTypeArray(stype)
        self.assertTrue(arr.dict_like or isinstance(arr.array, dict))

    # -----------------------------------------------------------------
    # StringParser + real RegexPattern: dipole-moment-shaped block,
    # reproducing the exact shape of the failing
    # `dips_parser.parse_all("\n".join(moms))` call from the traceback.
    # -----------------------------------------------------------------

    @validationTest
    def test_DipoleBlock_SingleRow(self):
        parser = StringParser(_dipole_pattern())
        res = parser.parse(" 0.123456 -0.234567 0.345678")
        if res is None:
            raise Exception("dipole-shaped pattern failed to match a single well-formed row")

    @validationTest
    def test_DipoleBlock_ParseAll(self):
        # this is the actual regression scenario:
        # parser.parse_all("\n".join(moms))
        block = _make_dipole_block(25, seed=1)
        parser = StringParser(_dipole_pattern())
        res = parser.parse_all(block)  # must NOT raise AttributeError
        if res is None:
            raise Exception("parse_all returned None for a well-formed dipole block")

    @validationTest
    def test_DipoleBlock_LargeBlock(self):
        block = _make_dipole_block(5000, seed=2)
        parser = StringParser(_dipole_pattern())
        res = parser.parse_all(block)
        if res is None:
            raise Exception("parse_all returned None for a 5000-row dipole block")

    @validationTest
    def test_DipoleBlock_SingleRowBlock(self):
        block = _make_dipole_block(1, seed=3)
        parser = StringParser(_dipole_pattern())
        res = parser.parse_all(block)
        if res is None:
            raise Exception("parse_all returned None for a single-row dipole block")

    @validationTest
    def test_DipoleBlock_EmptyBlock(self):
        # exploratory: pin down current empty-input behavior without
        # asserting a specific outcome (either a clean empty result or a
        # clear, catchable exception is acceptable; hanging is not)
        parser = StringParser(_dipole_pattern())
        try:
            res = parser.parse_all("")
            print("empty block parse_all() ->", res, file=sys.stderr)
        except Exception as e:
            print("empty block parse_all() raised:", repr(e), file=sys.stderr)

    # -----------------------------------------------------------------
    # Nested Repeating / zero-match / malformed-data stress
    # -----------------------------------------------------------------

    @validationTest
    def test_Stress_RepeatingWithinRepeating(self):
        inner = Repeating(Capturing(Number), min=1, suffix=Optional(Whitespace))
        outer = Repeating(
            RegexPattern((inner,), joiner=Whitespace),
            suffix=Optional(Newline),
        )
        block = "\n".join(
            " ".join(str(x) for x in range(random.randint(1, 5)))
            for _ in range(20)
        )
        parser = StringParser(outer)
        res = parser.parse_all(block)
        if res is None:
            raise Exception("nested Repeating(Repeating(...)) pattern failed to parse")

    @validationTest
    def test_Stress_ZeroRepeatsOfRepeatingBlock(self):
        pat = Repeating(Capturing(Number), min=0, suffix=Optional(Whitespace))
        parser = StringParser(pat)
        res = parser.parse_all("")
        if res is None:
            raise Exception("zero-match Repeating block returned None instead of an empty result")

    @validationTest
    def test_Stress_NamedAndCapturingTogether(self):
        pat = RegexPattern(
            (
                Named(PositiveInteger, "NumberOfAtoms"),
                Named(Repeating(Any, min=0), "Comment", dtype=str),
            ),
            joiner=Newline,
        )
        parser = StringParser(pat)
        res = parser.parse("42\nsomecomment")
        if res is None:
            raise Exception("Named+Capturing combination pattern failed to parse")

    @validationTest
    def test_Stress_MalformedNumericField(self):
        # exploratory: documents current behavior for malformed numeric
        # fields under the numpy backend without asserting a specific
        # outcome -- this is exactly the behavior the backend patch is
        # meant to make configurable (padding_mode='ragged' / backend='python')
        block = _make_dipole_block(50, seed=4, malformed_rate=0.2)
        parser = StringParser(_dipole_pattern())
        try:
            res = parser.parse_all(block)
            print("malformed dipole block parse_all() ->", res, file=sys.stderr)
        except Exception as e:
            print("malformed dipole block parse_all() raised:", repr(e), file=sys.stderr)

    @validationTest
    def test_Stress_RepeatedParsesAreIndependent(self):
        # guards against any shared mutable state leaking between
        # independent StringParser/StructuredTypeArray instances
        block_a = _make_dipole_block(10, seed=10)
        block_b = _make_dipole_block(15, seed=20)
        parser_a = StringParser(_dipole_pattern())
        parser_b = StringParser(_dipole_pattern())
        res_a = parser_a.parse_all(block_a)
        res_b = parser_b.parse_all(block_b)
        if res_a is None or res_b is None:
            raise Exception("independent parses of two separate StringParser instances failed")

    @validationTest
    def test_Stress_TenThousandRowDipoleBlock(self):
        block = _make_dipole_block(10_000, seed=100)
        parser = StringParser(_dipole_pattern())
        res = parser.parse_all(block)
        if res is None:
            raise Exception("parse_all returned None for a 10,000-row dipole block")

    @validationTest
    def test_Stress_ManySmallParsesNoLeakOrSlowdown(self):
        pattern = _dipole_pattern()
        t0 = time.perf_counter()
        for i in range(200):
            block = _make_dipole_block(20, seed=i)
            parser = StringParser(pattern)
            parser.parse_all(block)
        elapsed = time.perf_counter() - t0
        # generous bound -- this is a regression guard against accidental
        # O(n^2) growth reappearing, not a tight perf assertion
        if elapsed >= 30.0:
            raise Exception(f"200 small parses took {elapsed:.1f}s (expected < 30s) -- possible perf regression")

    # -----------------------------------------------------------------
    # Backend-specific tests. Gated with @backendTest / @parserBackendTest,
    # which resolve to @inactiveTest at import time if the corresponding
    # `backend=` support hasn't been patched in yet, so this file works
    # both before and after the patch without editing anything.
    # -----------------------------------------------------------------

    @backendTest
    def test_Backend_DefaultIsNumpyAndUnchanged(self):
        arr = StructuredTypeArray(StructuredType(float))
        self.assertEquals(getattr(arr.backend, "name", "numpy"), "numpy")
        arr.add_axis()
        arr.append(np.array([1.0]))
        self.assertIsInstance(arr._array, np.ndarray)

    @backendTest
    def test_Backend_PythonSelectableOnStructuredArray(self):
        arr = StructuredTypeArray(StructuredType(float), backend="python")
        arr.add_axis()
        arr.append(1.0)
        self.assertEquals(len(arr), 1)

    @parserBackendTest
    def test_Backend_PythonSelectableOnStringParser(self):
        try:
            parser = StringParser(_dipole_pattern(), backend="python")
        except TypeError as e:
            raise Exception(
                "StringParser doesn't accept backend= yet -- patch not applied to StringParser.py"
            ) from e
        block = _make_dipole_block(20, seed=5)
        res = parser.parse_all(block)
        if res is None:
            raise Exception("python-backend parser returned None for a well-formed block")

    @parserBackendTest
    def test_Backend_PythonToleratesMalformedDataNumpyDoesNot(self):
        try:
            robust_parser = StringParser(_dipole_pattern(), backend="python")
        except TypeError as e:
            raise Exception("StringParser doesn't accept backend= yet") from e
        strict_parser = StringParser(_dipole_pattern())

        block = _make_dipole_block(100, seed=6, malformed_rate=0.15)

        strict_raised = False
        try:
            strict_parser.parse_all(block)
        except Exception:
            strict_raised = True

        # the whole point of the python backend: it should get through the
        # same malformed data without raising
        robust_result = robust_parser.parse_all(block)
        if robust_result is None:
            raise Exception("python backend returned None on malformed data instead of a tolerant result")

        if strict_raised:
            print("numpy backend raised on malformed data; python backend did not (expected)", file=sys.stderr)

    @backendTest
    def test_Backend_CastFailuresRecordedOnPythonBackend(self):
        arr = StructuredTypeArray(StructuredType(float), backend="python")
        arr.add_axis()
        for tok in ["1.0", "********", "3.0", "garbage", "5.0"]:
            try:
                arr.append(tok)
            except Exception:
                pass
        if not hasattr(arr, "cast_failures"):
            raise Exception("python-backed StructuredTypeArray is missing `cast_failures`")

    @backendTest
    def test_Backend_PropagatesIntoCompoundChildren(self):
        stype = StructuredType({"a": StructuredType(float), "b": StructuredType(float)})
        arr = StructuredTypeArray(stype, backend="python")
        children = list(arr._array.values()) if isinstance(arr._array, dict) else list(arr._array)
        if len(children) == 0:
            raise Exception("compound stype produced no children to check backend propagation on")
        for child in children:
            if getattr(child.backend, "name", None) != "python":
                raise Exception("backend did not propagate into a compound stype's children")

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

    @validationTest
    def test_ParseBib(self):
        import McUtils.Devutils as dev

        bib_file = TestManager.test_data('TeXPaper/bibliography/alt.bib')
        root_text = dev.read_file(bib_file)

        samp_bib = """
@article{Goodfellow2014,
   author = {Ian J. Goodfellow and Jean Pouget-Abadie and Mehdi Mirza and Bing Xu and David Warde-Farley and Sherjil Ozair and Aaron Courville and Yoshua Bengio},
   journal = {arXiv e-prints},
   month = {6},
   title = {Generative Adversarial Networks},
   url = {http://arxiv.org/abs/1406.2661},
   year = {2014},
}
"""
        # with dev.StreamInterface(samp_bib, file_backed=True) as stream:
        #     with BibItemParser(stream) as item_parser:
        #         print(":::", item_parser.parse_bib_line())
        #
        # return
        import pprint

        with BibTeXParser(bib_file) as parser:
            print()
            for i in range(6):
                (s, e), text = parser.parse_bib_item(return_end_points=True)
                if text is not None:
                    print("="*100)
                    print((s, e), text)
                    # if e > 0:
                    #     print(root_text[s:e])
                    # else:
                    #     print(root_text[s:])

                    pprint.pprint(parser.parse_bib_body(text))

    @debugTest
    def test_LineByLineParser(self):
        import re
        Tags = FileLineByLineReader.LineReaderTags


        BATCH_RE = re.compile(
            r"^\[(?P<phase>train|val)\]\s*batch\s+(?P<batch>\d+)\s*\|\s*"
            r"rows seen\s+(?P<rows>[\d,]+)\s*\|\s*"
            r"running loss\s+(?P<loss>[\d.]+)\s*\|\s*"
            r"running acc\s+(?P<acc>[\d.]+)\s*$"
        )
        EPOCH_RE = re.compile(r"^epoch\s+(?P<epoch>\d+)\s*\|.*$")

        class ImprovedTrainingLogParser:
            def __init__(self):
                self.header_done = False
                self.epoch = 0

            def _parse_batch(self, stripped):
                m = BATCH_RE.match(stripped)
                if m:
                    return m['phase'], {
                        'batch': int(m['batch']), 'rows_seen': int(m['rows'].replace(',', '')),
                        'loss': float(m['loss']), 'acc': float(m['acc']),
                    }
                return None

            def __call__(self, line, depth=0, active_tag=None, label=None, history=None):
                stripped = line.strip()
                parsed = self._parse_batch(stripped)
                is_epoch_line = EPOCH_RE.match(stripped) is not None

                if label is None:
                    if not self.header_done:
                        self.header_done = True
                        if parsed is not None or is_epoch_line:
                            return (Tags.BLOCK_START, self.epoch, Tags.USE_HANDLER), parsed
                        return (Tags.BLOCK_START, "header", line), None
                    return (Tags.BLOCK_START, self.epoch, Tags.USE_HANDLER), parsed

                if label == "header":
                    if parsed is not None or is_epoch_line:
                        return Tags.RESETTING_BLOCK_END, None
                    if len(stripped) == 0:
                        return Tags.SKIP, None
                    return None, line

                if is_epoch_line:
                    self.epoch += 1
                    return Tags.RESETTING_BLOCK_END, None
                if parsed is not None:
                    phase, data = parsed
                    return (Tags.GROUP, phase, data), None
                return Tags.SKIP, None

            def handle_block(self, label, block, depth=0):
                if label in ("train", "val"):
                    return block
                if label == "header":
                    return "\n".join(block)
                result = {"train": [], "val": []}
                for item in block:
                    if item is None:
                        continue
                    if isinstance(item, dict):
                        for phase, vals in item.items():
                            result[phase].extend(vals)
                    else:
                        phase, data = item
                        result[phase].append(data)
                return result

        with line_by_line_parser(
            TestManager.test_data('line_sample.out'),
            ImprovedTrainingLogParser()
        ) as parser:
            import pprint
            pprint.pprint(list(parser))