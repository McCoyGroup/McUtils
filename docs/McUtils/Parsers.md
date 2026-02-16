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
[StringParser](Parsers/StringParser/StringParser.md)   
</div>
   <div class="col" markdown="1">
[StringParserException](Parsers/StringParser/StringParserException.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[RegexPattern](Parsers/RegexPatterns/RegexPattern.md)   
</div>
   <div class="col" markdown="1">
[Capturing](Parsers/RegexPatterns/Capturing.md)   
</div>
   <div class="col" markdown="1">
[NonCapturing](Parsers/RegexPatterns/NonCapturing.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Optional](Parsers/RegexPatterns/Optional.md)   
</div>
   <div class="col" markdown="1">
[Alternatives](Parsers/RegexPatterns/Alternatives.md)   
</div>
   <div class="col" markdown="1">
[Longest](Parsers/RegexPatterns/Longest.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Shortest](Parsers/RegexPatterns/Shortest.md)   
</div>
   <div class="col" markdown="1">
[Repeating](Parsers/RegexPatterns/Repeating.md)   
</div>
   <div class="col" markdown="1">
[Duplicated](Parsers/RegexPatterns/Duplicated.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[PatternClass](Parsers/RegexPatterns/PatternClass.md)   
</div>
   <div class="col" markdown="1">
[Parenthesized](Parsers/RegexPatterns/Parenthesized.md)   
</div>
   <div class="col" markdown="1">
[Named](Parsers/RegexPatterns/Named.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Any](Parsers/RegexPatterns/Any.md)   
</div>
   <div class="col" markdown="1">
[Sign](Parsers/RegexPatterns/Sign.md)   
</div>
   <div class="col" markdown="1">
[Number](Parsers/RegexPatterns/Number.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[IntBaseNumber](Parsers/RegexPatterns/IntBaseNumber.md)   
</div>
   <div class="col" markdown="1">
[Integer](Parsers/RegexPatterns/Integer.md)   
</div>
   <div class="col" markdown="1">
[PositiveInteger](Parsers/RegexPatterns/PositiveInteger.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ASCIILetter](Parsers/RegexPatterns/ASCIILetter.md)   
</div>
   <div class="col" markdown="1">
[AtomName](Parsers/RegexPatterns/AtomName.md)   
</div>
   <div class="col" markdown="1">
[WhitespaceCharacter](Parsers/RegexPatterns/WhitespaceCharacter.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Word](Parsers/RegexPatterns/Word.md)   
</div>
   <div class="col" markdown="1">
[WordCharacter](Parsers/RegexPatterns/WordCharacter.md)   
</div>
   <div class="col" markdown="1">
[VariableName](Parsers/RegexPatterns/VariableName.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[CartesianPoint](Parsers/RegexPatterns/CartesianPoint.md)   
</div>
   <div class="col" markdown="1">
[IntXYZLine](Parsers/RegexPatterns/IntXYZLine.md)   
</div>
   <div class="col" markdown="1">
[XYZLine](Parsers/RegexPatterns/XYZLine.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Empty](Parsers/RegexPatterns/Empty.md)   
</div>
   <div class="col" markdown="1">
[Newline](Parsers/RegexPatterns/Newline.md)   
</div>
   <div class="col" markdown="1">
[ZMatPattern](Parsers/RegexPatterns/ZMatPattern.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[StructuredType](Parsers/StructuredType/StructuredType.md)   
</div>
   <div class="col" markdown="1">
[StructuredTypeArray](Parsers/StructuredType/StructuredTypeArray.md)   
</div>
   <div class="col" markdown="1">
[DisappearingType](Parsers/StructuredType/DisappearingType.md)   
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

## RegexPattern

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

### Capturing/Named

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

## StringParser

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

### Block Handlers

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












<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#Tests-69b9dd" markdown="1"> Tests</a> <a class="float-right" data-toggle="collapse" href="#Tests-69b9dd"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Tests-69b9dd" markdown="1">
 - [RegexGroups](#RegexGroups)
- [OptScan](#OptScan)
- [XYZ](#XYZ)
- [BasicParse](#BasicParse)
- [ParseTex](#ParseTex)
- [ParseBib](#ParseBib)

<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
### <a class="collapse-link" data-toggle="collapse" href="#Setup-667578" markdown="1"> Setup</a> <a class="float-right" data-toggle="collapse" href="#Setup-667578"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Setup-667578" markdown="1">
 
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