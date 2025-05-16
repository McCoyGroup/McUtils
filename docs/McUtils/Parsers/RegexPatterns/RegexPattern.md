## <a id="McUtils.Parsers.RegexPatterns.RegexPattern">RegexPattern</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns.py#L47)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns.py#L47?message=Update%20Docs)]
</div>

Represents a combinator structure for building more complex regexes

It might be worth working with this combinator structure in a _lazy_ fashion so that we can drill down
into the expression structure... that way we can define a sort-of Regex calculus that we can use to build up higher
order regexes but still be able to recursively inspect subparts?







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Parsers.RegexPatterns.RegexPattern.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, pat, name=None, children=None, parents=None, dtype=None, repetitions=None, key=None, joiner='', join_function=None, wrapper_function=None, suffix=None, prefix=None, parser=None, handler=None, default_value=None, capturing=None, allow_inner_captures=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L55)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L55?message=Update%20Docs)]
</div>

  - `pat`: `str | callable`
    > 
  - `name`: `str`
    > 
  - `dtype`: `Any`
    > 
  - `repetitions`: `Any`
    > 
  - `key`: `Any`
    > 
  - `joiner`: `Any`
    > 
  - `children`: `Any`
    > 
  - `parents`: `Any`
    > 
  - `wrapper_function`: `Any`
    > 
  - `suffix`: `Any`
    > 
  - `prefix`: `Any`
    > 
  - `parser`: `Any`
    > 
  - `handler`: `Any`
    > 
  - `capturing`: `Any`
    > 
  - `allow_inner_captures`: `Any`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.pat" class="docs-object-method">&nbsp;</a> 
```python
@property
pat(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L172)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L172?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.children" class="docs-object-method">&nbsp;</a> 
```python
@property
children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L179)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L179?message=Update%20Docs)]
</div>

  - `:returns`: `tuple[RegexPattern]`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.child_count" class="docs-object-method">&nbsp;</a> 
```python
@property
child_count(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L187)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L187?message=Update%20Docs)]
</div>

  - `:returns`: `int`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.child_map" class="docs-object-method">&nbsp;</a> 
```python
@property
child_map(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L195)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L195?message=Update%20Docs)]
</div>
Returns the map to subregexes for named regex components
  - `:returns`: `Dict[str, RegexPattern]`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.parents" class="docs-object-method">&nbsp;</a> 
```python
@property
parents(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L206)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L206?message=Update%20Docs)]
</div>

  - `:returns`: `tuple[RegexPattern]`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.joiner" class="docs-object-method">&nbsp;</a> 
```python
@property
joiner(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L214)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L214?message=Update%20Docs)]
</div>

  - `:returns`: `str`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.join_function" class="docs-object-method">&nbsp;</a> 
```python
@property
join_function(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L227)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L227?message=Update%20Docs)]
</div>

  - `:returns`: `function`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.suffix" class="docs-object-method">&nbsp;</a> 
```python
@property
suffix(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L240)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L240?message=Update%20Docs)]
</div>

  - `:returns`: `str | RegexPattern`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.prefix" class="docs-object-method">&nbsp;</a> 
```python
@property
prefix(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L252)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L252?message=Update%20Docs)]
</div>

  - `:returns`: `str | RegexPattern`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.dtype" class="docs-object-method">&nbsp;</a> 
```python
@property
dtype(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L264)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L264?message=Update%20Docs)]
</div>
Returns the StructuredType for the matched object

The basic thing we do is build the type from the contained child dtypes
The process effectively works like this:
If there's a single object, we use its dtype no matter what
Otherwise, we add together our type objects one by one, allowing the StructuredType to handle the calculus

After we've built our raw types, we compute the shape on top of these, using the assigned repetitions object
One thing I realize now I failed to do is to include the effects of sub-repetitions... only a single one will
ever get called.
  - `:returns`: `None | StructuredType`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.is_repeating" class="docs-object-method">&nbsp;</a> 
```python
@property
is_repeating(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L319)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L319?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.capturing" class="docs-object-method">&nbsp;</a> 
```python
@property
capturing(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L322)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L322?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.get_capturing_groups" class="docs-object-method">&nbsp;</a> 
```python
get_capturing_groups(self, allow_inners=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L329)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L329?message=Update%20Docs)]
</div>
We walk down the tree to find the children with capturing groups in them and
then find the outermost RegexPattern for those unless allow_inners is on in which case we pull them all


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.captures" class="docs-object-method">&nbsp;</a> 
```python
@property
captures(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L346)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L346?message=Update%20Docs)]
</div>
Subtly different from capturing n that it will tell us if we need to use the group in post-processing, essentially
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.capturing_groups" class="docs-object-method">&nbsp;</a> 
```python
@property
capturing_groups(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L355)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L355?message=Update%20Docs)]
</div>
Returns the capturing children for the pattern
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.named_groups" class="docs-object-method">&nbsp;</a> 
```python
@property
named_groups(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L374)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L374?message=Update%20Docs)]
</div>
Returns the named children for the pattern
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.combine" class="docs-object-method">&nbsp;</a> 
```python
combine(self, other, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L407)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L407?message=Update%20Docs)]
</div>
Combines self and other
  - `other`: `RegexPattern | str`
    > 
  - `:returns`: `str | callable`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.wrap" class="docs-object-method">&nbsp;</a> 
```python
wrap(self, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L429)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L429?message=Update%20Docs)]
</div>
Applies wrapper function


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.build" class="docs-object-method">&nbsp;</a> 
```python
build(self, joiner=None, prefix=None, suffix=None, recompile=True, no_captures=False, verbose=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L443)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L443?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.compiled" class="docs-object-method">&nbsp;</a> 
```python
@property
compiled(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L522)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L522?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.add_parent" class="docs-object-method">&nbsp;</a> 
```python
add_parent(self, parent): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L528)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L528?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.remove_parent" class="docs-object-method">&nbsp;</a> 
```python
remove_parent(self, parent): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L530)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L530?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.add_child" class="docs-object-method">&nbsp;</a> 
```python
add_child(self, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L533)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L533?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.add_children" class="docs-object-method">&nbsp;</a> 
```python
add_children(self, children): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L539)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L539?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.remove_child" class="docs-object-method">&nbsp;</a> 
```python
remove_child(self, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L545)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L545?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.insert_child" class="docs-object-method">&nbsp;</a> 
```python
insert_child(self, index, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L551)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L551?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.invalidate_cache" class="docs-object-method">&nbsp;</a> 
```python
invalidate_cache(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L556)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L556?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.__copy__" class="docs-object-method">&nbsp;</a> 
```python
__copy__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L571)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L571?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L581)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L581?message=Update%20Docs)]
</div>
Combines self and other
  - `other`: `RegexPattern`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.__radd__" class="docs-object-method">&nbsp;</a> 
```python
__radd__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L597)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L597?message=Update%20Docs)]
</div>
Combines self and other
  - `other`: `RegexPattern`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, other, *args, name=None, dtype=None, repetitions=None, key=None, joiner=None, join_function=None, wrap_function=None, suffix=None, prefix=None, multiline=None, parser=None, handler=None, capturing=None, default=None, allow_inner_captures=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L613)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L613?message=Update%20Docs)]
</div>
Wraps self around other
  - `other`: `RegexPattern`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L685)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L685?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.__str__" class="docs-object-method">&nbsp;</a> 
```python
__str__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L692)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L692?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L696)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L696?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.match" class="docs-object-method">&nbsp;</a> 
```python
match(self, txt): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L700)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L700?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.search" class="docs-object-method">&nbsp;</a> 
```python
search(self, txt): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L702)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L702?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.findall" class="docs-object-method">&nbsp;</a> 
```python
findall(self, txt): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L704)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L704?message=Update%20Docs)]
</div>


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.finditer" class="docs-object-method">&nbsp;</a> 
```python
finditer(self, txt): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Parsers/RegexPatterns/RegexPattern.py#L706)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns/RegexPattern.py#L706?message=Update%20Docs)]
</div>
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Parsers/RegexPatterns/RegexPattern.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Parsers/RegexPatterns/RegexPattern.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Parsers/RegexPatterns/RegexPattern.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Parsers/RegexPatterns/RegexPattern.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Parsers/RegexPatterns.py#L47?message=Update%20Docs)   
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