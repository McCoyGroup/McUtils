## <a id="McUtils.McUtils.Parsers.StringParser.StringParser">StringParser</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StringParser.py#L79)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StringParser.py#L79?message=Update%20Docs)]
</div>

A convenience class that makes it easy to pull blocks out of strings and whatnot







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
MatchIterator: MatchIterator
```
<a id="McUtils.McUtils.Parsers.StringParser.StringParser.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, regex: McUtils.McUtils.Parsers.RegexPatterns.RegexPattern): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StringParser/StringParser.py#L84)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StringParser/StringParser.py#L84?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Parsers.StringParser.StringParser.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self, txt, regex=None, block_handlers=None, dtypes=None, out=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StringParser/StringParser.py#L87)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StringParser/StringParser.py#L87?message=Update%20Docs)]
</div>
Finds a single match for the and applies parsers for the specified regex in txt
  - `txt`: `str`
    > a chunk of text to be matched
  - `regex`: `RegexPattern`
    > the regex to match in _txt_
  - `block_handlers`: `iterable[callable] | OrderedDict[str: callable]`
    > handlers for the matched blocks in _regex_ -- usually comes from _regex_
  - `dtypes`: `iterable[type | StructuredType] | OrderedDict[str: type | StructuredType]`
    > the types of the data that we expect to match -- usually comes from _regex_
  - `out`: `None | StructuredTypeArray | iterable[StructuredTypeArray] | OrderedDict[str: StructuredTypeArray]`
    > where to place the parsed out data -- usually comes from _regex_
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Parsers.StringParser.StringParser.parse_all" class="docs-object-method">&nbsp;</a> 
```python
parse_all(self, txt, regex=None, num_results=None, block_handlers=None, dtypes=None, out=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StringParser/StringParser.py#L217)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StringParser/StringParser.py#L217?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Parsers.StringParser.StringParser.parse_iter" class="docs-object-method">&nbsp;</a> 
```python
parse_iter(self, txt, regex=None, num_results=None, block_handlers=None, dtypes=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/StringParser/StringParser.py#L315)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StringParser/StringParser.py#L315?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Parsers.StringParser.StringParser.get_regex_block_handlers" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_regex_block_handlers(cls, regex): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L339)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L339?message=Update%20Docs)]
</div>
Uses the uncompiled RegexPattern to determine what blocks exist and what handlers they should use
  - `regex`: `RegexPattern`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Parsers.StringParser.StringParser.get_regex_dtypes" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_regex_dtypes(cls, regex): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L383)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L383?message=Update%20Docs)]
</div>
Uses the uncompiled RegexPattern to determine which StructuredTypes to return
  - `regex`: `RegexPattern`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Parsers.StringParser.StringParser.handler_method" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
handler_method(cls, method): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L868)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L868?message=Update%20Docs)]
</div>
Turns a regular function into a handler method by adding in (and ignoring) the array argument
  - `method`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Parsers.StringParser.StringParser.load_array" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
load_array(data, dtype='float'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L883)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L883?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Parsers.StringParser.StringParser.to_array" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
to_array(cls, data, array=None, append=False, dtype='float', shape=None, pre=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L887)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L887?message=Update%20Docs)]
</div>
A method to take a string or iterable of strings and quickly dump it to a NumPy array of the right dtype (if it can be cast as one)
  - `data`: `Any`
    > 
  - `dtype`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Parsers.StringParser.StringParser.array_handler" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
array_handler(cls, array=None, append=False, dtype='float', shape=None, pre=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L957)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L957?message=Update%20Docs)]
</div>
Returns a handler that uses to_array
  - `dtype`: `Any`
    > 
  - `array`: `Any`
    > 
  - `shape`: `Any`
    > 
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/StringParser/StringParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/StringParser/StringParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/StringParser/StringParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/StringParser/StringParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/StringParser.py#L79?message=Update%20Docs)   
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