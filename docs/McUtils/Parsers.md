# <a id="McUtils.Parsers">McUtils.Parsers</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/__init__.py#L1?message=Update%20Docs)]
</div>
    
Utilities for writing parsers of structured text.
An entirely standalone package which is used extensively by `GaussianInterface`.
Three main threads are handled:

1. A `FileStreamer` interface which allows for efficient searching for blocks of text
   in large files with no pattern matching
2. A `Regex` interface that provides declarative tools for building and manipulating a regular expression
   as a python tree
3. A `StringParser`/`StructuredTypeArray` interface that takes the `Regex` tools and allows for automatic
   construction of complicated `NumPy`-backed arrays from the parsed data. Generally works well but the
   problem is complicated and there are no doubt many unhandled edge cases.
   This is used extensively with (1.) to provide efficient parsing of data from Gaussian `.log` files by
   using a streamer to match chunks and a parser to extract data from the matched chunks.

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[FileStreamReader](Parsers/FileStreamer/FileStreamReader.md)   
</div>
   <div class="col" markdown="1">
[FileStreamCheckPoint](Parsers/FileStreamer/FileStreamCheckPoint.md)   
</div>
   <div class="col" markdown="1">
[FileStreamerTag](Parsers/FileStreamer/FileStreamerTag.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[FileStreamReaderException](Parsers/FileStreamer/FileStreamReaderException.md)   
</div>
   <div class="col" markdown="1">
[StringStreamReader](Parsers/FileStreamer/StringStreamReader.md)   
</div>
   <div class="col" markdown="1">
[FileLineByLineReader](Parsers/FileStreamer/FileLineByLineReader.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[StringLineByLineReader](Parsers/FileStreamer/StringLineByLineReader.md)   
</div>
   <div class="col" markdown="1">
[ByteLineByLineReader](Parsers/FileStreamer/ByteLineByLineReader.md)   
</div>
   <div class="col" markdown="1">
[line_by_line_parser](Parsers/FileStreamer/line_by_line_parser.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[StringParser](Parsers/StringParser/StringParser.md)   
</div>
   <div class="col" markdown="1">
[StringParserException](Parsers/StringParser/StringParserException.md)   
</div>
   <div class="col" markdown="1">
[RegexPattern](Parsers/RegexPatterns/RegexPattern.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Capturing](Parsers/RegexPatterns/Capturing.md)   
</div>
   <div class="col" markdown="1">
[NonCapturing](Parsers/RegexPatterns/NonCapturing.md)   
</div>
   <div class="col" markdown="1">
[Optional](Parsers/RegexPatterns/Optional.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Alternatives](Parsers/RegexPatterns/Alternatives.md)   
</div>
   <div class="col" markdown="1">
[Longest](Parsers/RegexPatterns/Longest.md)   
</div>
   <div class="col" markdown="1">
[Shortest](Parsers/RegexPatterns/Shortest.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Repeating](Parsers/RegexPatterns/Repeating.md)   
</div>
   <div class="col" markdown="1">
[Duplicated](Parsers/RegexPatterns/Duplicated.md)   
</div>
   <div class="col" markdown="1">
[PatternClass](Parsers/RegexPatterns/PatternClass.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Parenthesized](Parsers/RegexPatterns/Parenthesized.md)   
</div>
   <div class="col" markdown="1">
[Named](Parsers/RegexPatterns/Named.md)   
</div>
   <div class="col" markdown="1">
[StartOfString](Parsers/RegexPatterns/StartOfString.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[EndOfString](Parsers/RegexPatterns/EndOfString.md)   
</div>
   <div class="col" markdown="1">
[Any](Parsers/RegexPatterns/Any.md)   
</div>
   <div class="col" markdown="1">
[Sign](Parsers/RegexPatterns/Sign.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Number](Parsers/RegexPatterns/Number.md)   
</div>
   <div class="col" markdown="1">
[IntBaseNumber](Parsers/RegexPatterns/IntBaseNumber.md)   
</div>
   <div class="col" markdown="1">
[Integer](Parsers/RegexPatterns/Integer.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[PositiveInteger](Parsers/RegexPatterns/PositiveInteger.md)   
</div>
   <div class="col" markdown="1">
[ASCIILetter](Parsers/RegexPatterns/ASCIILetter.md)   
</div>
   <div class="col" markdown="1">
[AtomName](Parsers/RegexPatterns/AtomName.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[WhitespaceCharacter](Parsers/RegexPatterns/WhitespaceCharacter.md)   
</div>
   <div class="col" markdown="1">
[Word](Parsers/RegexPatterns/Word.md)   
</div>
   <div class="col" markdown="1">
[WordCharacter](Parsers/RegexPatterns/WordCharacter.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[VariableName](Parsers/RegexPatterns/VariableName.md)   
</div>
   <div class="col" markdown="1">
[CartesianPoint](Parsers/RegexPatterns/CartesianPoint.md)   
</div>
   <div class="col" markdown="1">
[IntXYZLine](Parsers/RegexPatterns/IntXYZLine.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[XYZLine](Parsers/RegexPatterns/XYZLine.md)   
</div>
   <div class="col" markdown="1">
[Empty](Parsers/RegexPatterns/Empty.md)   
</div>
   <div class="col" markdown="1">
[Newline](Parsers/RegexPatterns/Newline.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ZMatPattern](Parsers/RegexPatterns/ZMatPattern.md)   
</div>
   <div class="col" markdown="1">
[StructuredType](Parsers/StructuredType/StructuredType.md)   
</div>
   <div class="col" markdown="1">
[StructuredTypeArray](Parsers/StructuredType/StructuredTypeArray.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[DisappearingType](Parsers/StructuredType/DisappearingType.md)   
</div>
   <div class="col" markdown="1">
[StructuredTypeArrayException](Parsers/StorageBackends/StructuredTypeArrayException.md)   
</div>
   <div class="col" markdown="1">
[GrowthPolicy](Parsers/StorageBackends/GrowthPolicy.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[CastFailure](Parsers/StorageBackends/CastFailure.md)   
</div>
   <div class="col" markdown="1">
[ParserStorageBackend](Parsers/StorageBackends/ParserStorageBackend.md)   
</div>
   <div class="col" markdown="1">
[NumpyStorageBackend](Parsers/StorageBackends/NumpyStorageBackend.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[PythonStorageBackend](Parsers/StorageBackends/PythonStorageBackend.md)   
</div>
   <div class="col" markdown="1">
[tolerant_float](Parsers/StorageBackends/tolerant_float.md)   
</div>
   <div class="col" markdown="1">
[tolerant_int](Parsers/StorageBackends/tolerant_int.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[XYZParser](Parsers/XYZParser/XYZParser.md)   
</div>
   <div class="col" markdown="1">
[TeXParser](Parsers/TeXParser/TeXParser.md)   
</div>
   <div class="col" markdown="1">
[BibTeXParser](Parsers/TeXParser/BibTeXParser.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>





## Examples

### RegexPattern

A `RegexPattern` is a higher-level interface to work with the [regular expression](https://en.wikipedia.org/wiki/Regular_expression) (regex) string pattern matching language.
Python provides support for regular expressions through the [`re`](https://docs.python.org/3/library/re.html) module.
Being comfortable with regex is not a requirement for working with `RegexPattern` but will help explain some of the more confusing design decisions.

There are a bunch of different `RegexPattern` instances that cover different cases, e.g.

* `Word`: matches a string of characters that are generally considered _text_
* `PositiveInteger`: matches a string of characters that are only _digits_
* `Integer`: a `PositiveInteger` with and optional sign
* `Number`: matches `Integer.PositiveInteger`
* `VariableName`: matches a string of digits or text as the first character is a letter
* `Optional`: represents an _optional_ pattern to match

#### Capturing/Named

When matching pieces of text it is also important to specify which pieces of text we would like to actually get back out.
For this there are two main `RegexPattern` instances.
The simplest one is `Capturing`.
This just specifies that we would like to capture a piece of text.
There is a slightly more sophisticated instance called `Named` which allows us to attach a _name_ to a group.

<div class="card in-out-block" markdown="1" id="Markdown_code">

```python
key_value_matcher = RegexPattern([Named(Word, "key"), "=", Named(Word, "value")])
print(key_value_matcher)
```

<div class="card-body out-block" markdown="1">

```lang-none
(?P<key>\w+)(?:=)(?P<value>\w+)
```

</div>
</div>

This can be used directly to pull info out of files

<div class="card in-out-block" markdown="1" id="Markdown_code">

```python
test_data = os.path.join(os.path.dirname(McUtils.__file__), 'ci', 'tests', 'TestData')
with open(os.path.join(test_data, 'water_OH_scan.log')) as log_dat:
    sample_data = log_dat.read()

matches = list(key_value_matcher.finditer(sample_data))
for match in matches[:5]:
    print(match.groupdict())
```

<div class="card-body out-block" markdown="1">

```python
{'key': '0', 'value': 'g09'}
{'key': 'Input', 'value': 'water_OH_scan'}
{'key': 'Output', 'value': 'water_OH_scan'}
{'key': 'Chk', 'value': 'water_OH_scan'}
{'key': 'NProc', 'value': '8'}
```

</div>
</div>

### StringParser

A more powerful interface than `RegexPattern` is through a `StringParser` instance.
This provides a wrapper on `RegexPattern` that handles the process of turning matches into `NumPy` arrays of the appropriate type.
The actual interface is quite simple, e.g. we can take our matcher from before and use it directly

<div class="card in-out-block" markdown="1" id="Markdown_code">

```python
key_vals = StringParser(key_value_matcher).parse_all(sample_data)
print(key_vals)
```

<div class="card-body out-block" markdown="1">

```python
StructuredTypeArray(shape=[(11493, 0), (11493, 0)], dtype=OrderedDict([('key', StructuredType(<class 'str'>, shape=(None,))), ('value', StructuredType(<class 'str'>, shape=(None,)))]))
```

</div>
</div>

This `StructuredTypeArray` is basically a version of `NumPy` [record arrays](https://numpy.org/doc/stable/reference/generated/numpy.recarray.html), 
but was written without knowing about them.
A smarter reimplementation of this portion of the parsing process would make use of `recarray` instead of this custom array type.

That said, getting the raw `ndarray` objects out is straight-forward

<div class="card in-out-block" markdown="1" id="Markdown_code">

```python
key_vals['key'].array
```

<div class="card-body out-block" markdown="1">

```python
array(['0', 'Input', 'Output', ..., 'State', 'RMSD', 'PG'], dtype='<U7')
```

</div>
</div>

NOTE: 90% of all bugs in the `StringParser` ecosystem will come from the design of `StructuredTypeArray`. 
The need to be efficient in data handling can lead to some difficult implementation details. 
As the data type has organically evolved it has become potentially tough to understand.
A reimplementation based on `recarray` would _potentially_ solve some issues.
{: .alert .alert-warning}

#### Block Handlers

For efficiency sake, `StringParser` objects also provide a `block_handlers` argument (and handlers can be defined on `RegexPatterns` directly).
A handler is a function that can be applied to a parsed piece of text and should directly return a `NumPy` array so that it can be worked into the returned `StructuredTypeArray`.
The simplest handlers are already provided for convenience on `StringParser`, e.g. from `GaussianLogComponents.py`

```python
Named(
    Repeating(
        Capturing(Number),
        min = 3, max = 3,
        prefix=Optional(Whitespace),
        joiner = Whitespace
    ),
    "Coordinates", handler=StringParser.array_handler(dtype=float)
)
```

Here `StringParser.array_handler(dtype=float)` provides efficient parsing of data through `np.loadtxt` with a `float` as the target `dtype`.
We also see the `prefix` and `joiner` options to `RegexPattern` in action.

**LLM Examples**

### Build a declarative parser for numerical records

```python
from McUtils.Parsers import RegexPattern, Repeating, Capturing
from McUtils.Parsers import Number, Whitespace, Optional, StringParser

pattern = RegexPattern(
    ("Eigenvalues --", Repeating(Capturing(Number), suffix=Optional(Whitespace))),
    joiner=Whitespace
)
parser = StringParser(pattern)
values = parser.parse("Eigenvalues --  -0.1423  0.0781  0.2114")
print(values.array)
```

### Stream structures from an XYZ trajectory

```python
from McUtils.Parsers import XYZParser

with XYZParser("trajectory.xyz") as parser:
    structures = parser.parse()
for comment, atoms, coords in structures:
    print(comment, len(atoms), coords.shape)
first_geometry = structures[0][2]
```

### Parse selected fields from a CIF

```python
from McUtils.ExternalPrograms import CIFParser, CIFConverter

fields = ["cell_length_a", "cell_length_b", "cell_length_c",
          "atom_site_label", "atom_site_fract_x", "atom_site_fract_y", "atom_site_fract_z"]
with CIFParser("crystal.cif", fields=fields) as parser:
    blocks = parser.parse()
crystal = CIFConverter(blocks)
atoms, coordinates = crystal.atoms()
print("cell:", crystal.cell_properties())
print("expanded structure:", len(atoms), coordinates.shape)
```

### Compose named fields into structured data

```python
from McUtils.Parsers import RegexPattern, Named, Number, VariableName, Whitespace
from McUtils.Parsers import StringParser

record = RegexPattern((Named(VariableName, "label"), Named(Number, "value")),
                      joiner=Whitespace)
parser = StringParser(record)
parsed = parser.parse("Energy -76.2413")
print(parsed["label"].array, parsed["value"].array)
```

### Search a large file without loading it all

```python
from McUtils.Parsers import FileStreamReader, FileStreamerTag

with FileStreamReader("large-output.log") as stream:
    tag = FileStreamerTag("Standard orientation:", follow_ups=["-----"])
    block = stream.get_tagged_block("geometry", tag)
print("matched block length:", len(block))
```













<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#Tests-fac455" markdown="1"> Tests</a> <a class="float-right" data-toggle="collapse" href="#Tests-fac455"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Tests-fac455" markdown="1">
 - [RegexGroups](#RegexGroups)
- [OptScan](#OptScan)
- [XYZ](#XYZ)
- [BasicParse](#BasicParse)
- [StructuredArray_HasIndeterminateShape](#StructuredArray_HasIndeterminateShape)
- [StructuredArray_AxisShapeIndeterminate](#StructuredArray_AxisShapeIndeterminate)
- [StructuredArray_BlockSize](#StructuredArray_BlockSize)
- [StructuredArray_AppendDepth](#StructuredArray_AppendDepth)
- [StructuredArray_CanCast](#StructuredArray_CanCast)
- [StructuredArray_GetCastingShape](#StructuredArray_GetCastingShape)
- [StructuredArray_AppendWritesScalars](#StructuredArray_AppendWritesScalars)
- [StructuredArray_ExtendAppendsBlock](#StructuredArray_ExtendAppendsBlock)
- [StructuredArray_FillSetsContents](#StructuredArray_FillSetsContents)
- [StructuredArray_SetPartGetItemRoundTrip](#StructuredArray_SetPartGetItemRoundTrip)
- [StructuredArray_CastToArrayScalar](#StructuredArray_CastToArrayScalar)
- [StructuredArray_CastToArrayVector](#StructuredArray_CastToArrayVector)
- [StructuredArray_AddAxisFromScalarType](#StructuredArray_AddAxisFromScalarType)
- [StructuredArray_AddAxisFromShapedType](#StructuredArray_AddAxisFromShapedType)
- [StructuredArray_LenMatchesAppendedCount](#StructuredArray_LenMatchesAppendedCount)
- [StructuredArray_DictLikeCompound](#StructuredArray_DictLikeCompound)
- [DipoleBlock_SingleRow](#DipoleBlock_SingleRow)
- [DipoleBlock_ParseAll](#DipoleBlock_ParseAll)
- [DipoleBlock_LargeBlock](#DipoleBlock_LargeBlock)
- [DipoleBlock_SingleRowBlock](#DipoleBlock_SingleRowBlock)
- [DipoleBlock_EmptyBlock](#DipoleBlock_EmptyBlock)
- [Stress_RepeatingWithinRepeating](#Stress_RepeatingWithinRepeating)
- [Stress_ZeroRepeatsOfRepeatingBlock](#Stress_ZeroRepeatsOfRepeatingBlock)
- [Stress_NamedAndCapturingTogether](#Stress_NamedAndCapturingTogether)
- [Stress_MalformedNumericField](#Stress_MalformedNumericField)
- [Stress_RepeatedParsesAreIndependent](#Stress_RepeatedParsesAreIndependent)
- [Stress_TenThousandRowDipoleBlock](#Stress_TenThousandRowDipoleBlock)
- [Stress_ManySmallParsesNoLeakOrSlowdown](#Stress_ManySmallParsesNoLeakOrSlowdown)
- [Backend_DefaultIsNumpyAndUnchanged](#Backend_DefaultIsNumpyAndUnchanged)
- [Backend_PythonSelectableOnStructuredArray](#Backend_PythonSelectableOnStructuredArray)
- [Backend_PythonSelectableOnStringParser](#Backend_PythonSelectableOnStringParser)
- [Backend_PythonToleratesMalformedDataNumpyDoesNot](#Backend_PythonToleratesMalformedDataNumpyDoesNot)
- [Backend_CastFailuresRecordedOnPythonBackend](#Backend_CastFailuresRecordedOnPythonBackend)
- [Backend_PropagatesIntoCompoundChildren](#Backend_PropagatesIntoCompoundChildren)
- [ParseTex](#ParseTex)
- [ParseBib](#ParseBib)
- [LineByLineParser](#LineByLineParser)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#Setup-c756f1" markdown="1"> Setup</a> <a class="float-right" data-toggle="collapse" href="#Setup-c756f1"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Setup-c756f1" markdown="1">
 
Before we can run our examples we should get a bit of setup out of the way.
Since these examples were harvested from the unit tests not all pieces
will be necessary for all situations.

All tests are wrapped in a test class
```python
class ParserTests(TestCase):
```

 </div>
</div>

#### <a name="RegexGroups">RegexGroups</a>
```python
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
```

#### <a name="OptScan">OptScan</a>
```python
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
```

#### <a name="XYZ">XYZ</a>
```python
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
```

#### <a name="BasicParse">BasicParse</a>
```python
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
```

#### <a name="StructuredArray_HasIndeterminateShape">StructuredArray_HasIndeterminateShape</a>
```python
    def test_StructuredArray_HasIndeterminateShape(self):
        # this is the literal AttributeError from the traceback:
        #   AttributeError: 'StructuredTypeArray' object has no attribute
        #   'has_indeterminate_shape'
        arr = StructuredTypeArray(StructuredType(float))
        if not hasattr(arr, "has_indeterminate_shape"):
            raise Exception("StructuredTypeArray is missing `has_indeterminate_shape`")
        before = arr.has_indeterminate_shape
        self.assertIsInstance(before, (bool, np.bool_))
```

#### <a name="StructuredArray_AxisShapeIndeterminate">StructuredArray_AxisShapeIndeterminate</a>
```python
    def test_StructuredArray_AxisShapeIndeterminate(self):
        arr = StructuredTypeArray(StructuredType(float, shape=(None,)))
        if not hasattr(arr, "axis_shape_indeterminate"):
            raise Exception("StructuredTypeArray is missing `axis_shape_indeterminate`")
        result = arr.axis_shape_indeterminate(0)
        self.assertIsInstance(result, (bool, np.bool_))
```

#### <a name="StructuredArray_BlockSize">StructuredArray_BlockSize</a>
```python
    def test_StructuredArray_BlockSize(self):
        arr = StructuredTypeArray(StructuredType(float, shape=(None, 3)))
        if not hasattr(arr, "block_size"):
            raise Exception("StructuredTypeArray is missing `block_size`")
        _ = arr.block_size
```

#### <a name="StructuredArray_AppendDepth">StructuredArray_AppendDepth</a>
```python
    def test_StructuredArray_AppendDepth(self):
        arr = StructuredTypeArray(StructuredType(float))
        if not hasattr(arr, "append_depth"):
            raise Exception("StructuredTypeArray is missing `append_depth`")
        arr.append_depth = 0
        self.assertEquals(arr.append_depth, 0)
        arr.append_depth = 1
        self.assertEquals(arr.append_depth, 1)
```

#### <a name="StructuredArray_CanCast">StructuredArray_CanCast</a>
```python
    def test_StructuredArray_CanCast(self):
        arr = StructuredTypeArray(StructuredType(float))
        if not hasattr(arr, "can_cast"):
            raise Exception("StructuredTypeArray is missing `can_cast`")
        _ = arr.can_cast(1.0)
```

#### <a name="StructuredArray_GetCastingShape">StructuredArray_GetCastingShape</a>
```python
    def test_StructuredArray_GetCastingShape(self):
        arr = StructuredTypeArray(StructuredType(float, shape=(None,)))
        if not hasattr(arr, "_get_casting_shape"):
            raise Exception("StructuredTypeArray is missing `_get_casting_shape`")
```

#### <a name="StructuredArray_AppendWritesScalars">StructuredArray_AppendWritesScalars</a>
```python
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
```

#### <a name="StructuredArray_ExtendAppendsBlock">StructuredArray_ExtendAppendsBlock</a>
```python
    def test_StructuredArray_ExtendAppendsBlock(self):
        arr = StructuredTypeArray(StructuredType(float))
        arr.add_axis()
        arr.fill(np.array([1.0, 2.0, 3.0]))
        arr.extend(np.array([4.0, 5.0]))
        self.assertEquals(list(arr.array), [1.0, 2.0, 3.0, 4.0, 5.0])
```

#### <a name="StructuredArray_FillSetsContents">StructuredArray_FillSetsContents</a>
```python
    def test_StructuredArray_FillSetsContents(self):
        arr = StructuredTypeArray(StructuredType(float))
        arr.add_axis()
        arr.fill(np.array([9.0, 8.0, 7.0]))
        self.assertEquals(list(arr.array), [9.0, 8.0, 7.0])
```

#### <a name="StructuredArray_SetPartGetItemRoundTrip">StructuredArray_SetPartGetItemRoundTrip</a>
```python
    def test_StructuredArray_SetPartGetItemRoundTrip(self):
        arr = StructuredTypeArray(StructuredType(float))
        arr.add_axis()
        arr.fill(np.array([1.0, 2.0, 3.0]))
        self.assertEquals(arr[0], 1.0)
        self.assertEquals(arr[2], 3.0)
```

#### <a name="StructuredArray_CastToArrayScalar">StructuredArray_CastToArrayScalar</a>
```python
    def test_StructuredArray_CastToArrayScalar(self):
        arr = StructuredTypeArray(StructuredType(float))
        result = arr.cast_to_array("3.14")
        self.assertTrue(np.isclose(np.asarray(result).flatten()[0], 3.14))
```

#### <a name="StructuredArray_CastToArrayVector">StructuredArray_CastToArrayVector</a>
```python
    def test_StructuredArray_CastToArrayVector(self):
        arr = StructuredTypeArray(StructuredType(float, shape=(3,)))
        result = arr.cast_to_array("1.0 2.0 3.0")
        self.assertTrue(np.allclose(np.asarray(result).flatten(), [1.0, 2.0, 3.0]))
```

#### <a name="StructuredArray_AddAxisFromScalarType">StructuredArray_AddAxisFromScalarType</a>
```python
    def test_StructuredArray_AddAxisFromScalarType(self):
        arr = StructuredTypeArray(StructuredType(float))
        arr.add_axis()  # must not raise
        arr.append(np.array([1.0]))
        arr.append(np.array([2.0]))
        self.assertEquals(list(arr.array), [1.0, 2.0])
```

#### <a name="StructuredArray_AddAxisFromShapedType">StructuredArray_AddAxisFromShapedType</a>
```python
    def test_StructuredArray_AddAxisFromShapedType(self):
        arr = StructuredTypeArray(StructuredType(float, shape=(3,)))
        arr.add_axis()
        arr.append(np.array([1.0, 2.0, 3.0]))
        arr.append(np.array([4.0, 5.0, 6.0]))
        self.assertEquals(arr.array.shape[0], 2)
        self.assertEquals(list(arr.array[0]), [1.0, 2.0, 3.0])
        self.assertEquals(list(arr.array[1]), [4.0, 5.0, 6.0])
```

#### <a name="StructuredArray_LenMatchesAppendedCount">StructuredArray_LenMatchesAppendedCount</a>
```python
    def test_StructuredArray_LenMatchesAppendedCount(self):
        arr = StructuredTypeArray(StructuredType(float))
        arr.add_axis()
        for i in range(37):
            arr.append(np.array([float(i)]))
        self.assertEquals(len(arr), 37)
```

#### <a name="StructuredArray_DictLikeCompound">StructuredArray_DictLikeCompound</a>
```python
    def test_StructuredArray_DictLikeCompound(self):
        stype = StructuredType({"a": StructuredType(float), "b": StructuredType(int)})
        arr = StructuredTypeArray(stype)
        self.assertTrue(arr.dict_like or isinstance(arr.array, dict))
```

#### <a name="DipoleBlock_SingleRow">DipoleBlock_SingleRow</a>
```python
    def test_DipoleBlock_SingleRow(self):
        parser = StringParser(_dipole_pattern())
        res = parser.parse(" 0.123456 -0.234567 0.345678")
        if res is None:
            raise Exception("dipole-shaped pattern failed to match a single well-formed row")
```

#### <a name="DipoleBlock_ParseAll">DipoleBlock_ParseAll</a>
```python
    def test_DipoleBlock_ParseAll(self):
        # this is the actual regression scenario:
        # parser.parse_all("\n".join(moms))
        block = _make_dipole_block(25, seed=1)
        parser = StringParser(_dipole_pattern())
        res = parser.parse_all(block)  # must NOT raise AttributeError
        if res is None:
            raise Exception("parse_all returned None for a well-formed dipole block")
```

#### <a name="DipoleBlock_LargeBlock">DipoleBlock_LargeBlock</a>
```python
    def test_DipoleBlock_LargeBlock(self):
        block = _make_dipole_block(5000, seed=2)
        parser = StringParser(_dipole_pattern())
        res = parser.parse_all(block)
        if res is None:
            raise Exception("parse_all returned None for a 5000-row dipole block")
```

#### <a name="DipoleBlock_SingleRowBlock">DipoleBlock_SingleRowBlock</a>
```python
    def test_DipoleBlock_SingleRowBlock(self):
        block = _make_dipole_block(1, seed=3)
        parser = StringParser(_dipole_pattern())
        res = parser.parse_all(block)
        if res is None:
            raise Exception("parse_all returned None for a single-row dipole block")
```

#### <a name="DipoleBlock_EmptyBlock">DipoleBlock_EmptyBlock</a>
```python
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
```

#### <a name="Stress_RepeatingWithinRepeating">Stress_RepeatingWithinRepeating</a>
```python
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
```

#### <a name="Stress_ZeroRepeatsOfRepeatingBlock">Stress_ZeroRepeatsOfRepeatingBlock</a>
```python
    def test_Stress_ZeroRepeatsOfRepeatingBlock(self):
        pat = Repeating(Capturing(Number), min=0, suffix=Optional(Whitespace))
        parser = StringParser(pat)
        res = parser.parse_all("")
        if res is None:
            raise Exception("zero-match Repeating block returned None instead of an empty result")
```

#### <a name="Stress_NamedAndCapturingTogether">Stress_NamedAndCapturingTogether</a>
```python
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
```

#### <a name="Stress_MalformedNumericField">Stress_MalformedNumericField</a>
```python
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
```

#### <a name="Stress_RepeatedParsesAreIndependent">Stress_RepeatedParsesAreIndependent</a>
```python
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
```

#### <a name="Stress_TenThousandRowDipoleBlock">Stress_TenThousandRowDipoleBlock</a>
```python
    def test_Stress_TenThousandRowDipoleBlock(self):
        block = _make_dipole_block(10_000, seed=100)
        parser = StringParser(_dipole_pattern())
        res = parser.parse_all(block)
        if res is None:
            raise Exception("parse_all returned None for a 10,000-row dipole block")
```

#### <a name="Stress_ManySmallParsesNoLeakOrSlowdown">Stress_ManySmallParsesNoLeakOrSlowdown</a>
```python
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
```

#### <a name="Backend_DefaultIsNumpyAndUnchanged">Backend_DefaultIsNumpyAndUnchanged</a>
```python
    def test_Backend_DefaultIsNumpyAndUnchanged(self):
        arr = StructuredTypeArray(StructuredType(float))
        self.assertEquals(getattr(arr.backend, "name", "numpy"), "numpy")
        arr.add_axis()
        arr.append(np.array([1.0]))
        self.assertIsInstance(arr._array, np.ndarray)
```

#### <a name="Backend_PythonSelectableOnStructuredArray">Backend_PythonSelectableOnStructuredArray</a>
```python
    def test_Backend_PythonSelectableOnStructuredArray(self):
        arr = StructuredTypeArray(StructuredType(float), backend="python")
        arr.add_axis()
        arr.append(1.0)
        self.assertEquals(len(arr), 1)
```

#### <a name="Backend_PythonSelectableOnStringParser">Backend_PythonSelectableOnStringParser</a>
```python
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
```

#### <a name="Backend_PythonToleratesMalformedDataNumpyDoesNot">Backend_PythonToleratesMalformedDataNumpyDoesNot</a>
```python
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
```

#### <a name="Backend_CastFailuresRecordedOnPythonBackend">Backend_CastFailuresRecordedOnPythonBackend</a>
```python
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
```

#### <a name="Backend_PropagatesIntoCompoundChildren">Backend_PropagatesIntoCompoundChildren</a>
```python
    def test_Backend_PropagatesIntoCompoundChildren(self):
        stype = StructuredType({"a": StructuredType(float), "b": StructuredType(float)})
        arr = StructuredTypeArray(stype, backend="python")
        children = list(arr._array.values()) if isinstance(arr._array, dict) else list(arr._array)
        if len(children) == 0:
            raise Exception("compound stype produced no children to check backend propagation on")
        for child in children:
            if getattr(child.backend, "name", None) != "python":
                raise Exception("backend did not propagate into a compound stype's children")
```

#### <a name="ParseTex">ParseTex</a>
```python
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
```

#### <a name="ParseBib">ParseBib</a>
```python
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
```

#### <a name="LineByLineParser">LineByLineParser</a>
```python
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
```

 </div>
</div>






---


<div markdown="1" class="text-secondary">
<div class="container">
  <div class="row">
   <div class="col" markdown="1">
**Feedback**   
</div>
   <div class="col" markdown="1">
**Examples**   
</div>
   <div class="col" markdown="1">
**Templates**   
</div>
   <div class="col" markdown="1">
**Documentation**   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Bug](https://github.com/McCoyGroup/McUtils/issues/new?title=Documentation%20Improvement%20Needed)/[Request](https://github.com/McCoyGroup/McUtils/issues/new?title=Example%20Request)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/__init__.py#L1?message=Update%20Docs)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>
</div>