# <a id="McUtils.Parsers">McUtils.Parsers</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/__init__.py#L1?message=Update%20Docs)]
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
[FileStreamReader](McUtils/McUtils/Parsers/FileStreamer/FileStreamReader.md)   
</div>
   <div class="col" markdown="1">
[FileStreamCheckPoint](McUtils/McUtils/Parsers/FileStreamer/FileStreamCheckPoint.md)   
</div>
   <div class="col" markdown="1">
[FileStreamerTag](McUtils/McUtils/Parsers/FileStreamer/FileStreamerTag.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[FileStreamReaderException](McUtils/McUtils/Parsers/FileStreamer/FileStreamReaderException.md)   
</div>
   <div class="col" markdown="1">
[StringStreamReader](McUtils/McUtils/Parsers/FileStreamer/StringStreamReader.md)   
</div>
   <div class="col" markdown="1">
[FileLineByLineReader](McUtils/McUtils/Parsers/FileStreamer/FileLineByLineReader.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[StringLineByLineReader](McUtils/McUtils/Parsers/FileStreamer/StringLineByLineReader.md)   
</div>
   <div class="col" markdown="1">
[RegexPattern](McUtils/McUtils/Parsers/RegexPatterns/RegexPattern.md)   
</div>
   <div class="col" markdown="1">
[Capturing](McUtils/McUtils/Parsers/RegexPatterns/Capturing.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[NonCapturing](McUtils/McUtils/Parsers/RegexPatterns/NonCapturing.md)   
</div>
   <div class="col" markdown="1">
[Optional](McUtils/McUtils/Parsers/RegexPatterns/Optional.md)   
</div>
   <div class="col" markdown="1">
[Alternatives](McUtils/McUtils/Parsers/RegexPatterns/Alternatives.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Longest](McUtils/McUtils/Parsers/RegexPatterns/Longest.md)   
</div>
   <div class="col" markdown="1">
[Shortest](McUtils/McUtils/Parsers/RegexPatterns/Shortest.md)   
</div>
   <div class="col" markdown="1">
[Repeating](McUtils/McUtils/Parsers/RegexPatterns/Repeating.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Duplicated](McUtils/McUtils/Parsers/RegexPatterns/Duplicated.md)   
</div>
   <div class="col" markdown="1">
[PatternClass](McUtils/McUtils/Parsers/RegexPatterns/PatternClass.md)   
</div>
   <div class="col" markdown="1">
[Parenthesized](McUtils/McUtils/Parsers/RegexPatterns/Parenthesized.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Named](McUtils/McUtils/Parsers/RegexPatterns/Named.md)   
</div>
   <div class="col" markdown="1">
[Any](McUtils/McUtils/Parsers/RegexPatterns/Any.md)   
</div>
   <div class="col" markdown="1">
[Sign](McUtils/McUtils/Parsers/RegexPatterns/Sign.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Number](McUtils/McUtils/Parsers/RegexPatterns/Number.md)   
</div>
   <div class="col" markdown="1">
[Integer](McUtils/McUtils/Parsers/RegexPatterns/Integer.md)   
</div>
   <div class="col" markdown="1">
[PositiveInteger](McUtils/McUtils/Parsers/RegexPatterns/PositiveInteger.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ASCIILetter](McUtils/McUtils/Parsers/RegexPatterns/ASCIILetter.md)   
</div>
   <div class="col" markdown="1">
[AtomName](McUtils/McUtils/Parsers/RegexPatterns/AtomName.md)   
</div>
   <div class="col" markdown="1">
[WhitespaceCharacter](McUtils/McUtils/Parsers/RegexPatterns/WhitespaceCharacter.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Word](McUtils/McUtils/Parsers/RegexPatterns/Word.md)   
</div>
   <div class="col" markdown="1">
[WordCharacter](McUtils/McUtils/Parsers/RegexPatterns/WordCharacter.md)   
</div>
   <div class="col" markdown="1">
[VariableName](McUtils/McUtils/Parsers/RegexPatterns/VariableName.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[CartesianPoint](McUtils/McUtils/Parsers/RegexPatterns/CartesianPoint.md)   
</div>
   <div class="col" markdown="1">
[IntXYZLine](McUtils/McUtils/Parsers/RegexPatterns/IntXYZLine.md)   
</div>
   <div class="col" markdown="1">
[XYZLine](McUtils/McUtils/Parsers/RegexPatterns/XYZLine.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[Empty](McUtils/McUtils/Parsers/RegexPatterns/Empty.md)   
</div>
   <div class="col" markdown="1">
[Newline](McUtils/McUtils/Parsers/RegexPatterns/Newline.md)   
</div>
   <div class="col" markdown="1">
[ZMatPattern](McUtils/McUtils/Parsers/RegexPatterns/ZMatPattern.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[StringParser](McUtils/McUtils/Parsers/StringParser/StringParser.md)   
</div>
   <div class="col" markdown="1">
[StringParserException](McUtils/McUtils/Parsers/StringParser/StringParserException.md)   
</div>
   <div class="col" markdown="1">
[StructuredType](McUtils/McUtils/Parsers/StructuredType/StructuredType.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[StructuredTypeArray](McUtils/McUtils/Parsers/StructuredType/StructuredTypeArray.md)   
</div>
   <div class="col" markdown="1">
[DisappearingType](McUtils/McUtils/Parsers/StructuredType/DisappearingType.md)   
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/__init__.py#L1?message=Update%20Docs)   
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