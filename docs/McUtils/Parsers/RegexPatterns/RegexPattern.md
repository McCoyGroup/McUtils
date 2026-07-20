## <a id="McUtils.Parsers.RegexPatterns.RegexPattern">RegexPattern</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns.py#L50)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns.py#L50?message=Update%20Docs)]
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
__init__(self, pat, name=None, children=None, parents=None, dtype=None, repetitions=None, key=None, joiner='', join_function=None, wrapper_function=None, suffix=None, prefix=None, parser=None, handler=None, default_value=None, capturing=None, allow_inner_captures=False, escape=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns.py#L58)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns.py#L58?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L199)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L199?message=Update%20Docs)]
</div>
**LLM Docstring**

Return or replace the primitive pattern/wrapper used by this node; setting it invalidates all compiled caches.
  - `pat`: `object`
    > a literal regex fragment or callable wrapper

  - `:returns`: `object`
    > return or replace the primitive pattern/wrapper used by this node; setting it invalidates all compiled caches.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.children" class="docs-object-method">&nbsp;</a> 
```python
@property
children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L228)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L228?message=Update%20Docs)]
</div>

  - `:returns`: `tuple[RegexPattern]`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.child_count" class="docs-object-method">&nbsp;</a> 
```python
@property
child_count(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L236)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L236?message=Update%20Docs)]
</div>

  - `:returns`: `int`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.child_map" class="docs-object-method">&nbsp;</a> 
```python
@property
child_map(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L244)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L244?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L255)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L255?message=Update%20Docs)]
</div>

  - `:returns`: `tuple[RegexPattern]`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.joiner" class="docs-object-method">&nbsp;</a> 
```python
@property
joiner(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L263)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L263?message=Update%20Docs)]
</div>

  - `:returns`: `str`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.join_function" class="docs-object-method">&nbsp;</a> 
```python
@property
join_function(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L287?message=Update%20Docs)]
</div>

  - `:returns`: `function`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.suffix" class="docs-object-method">&nbsp;</a> 
```python
@property
suffix(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L311)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L311?message=Update%20Docs)]
</div>

  - `:returns`: `str | RegexPattern`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.prefix" class="docs-object-method">&nbsp;</a> 
```python
@property
prefix(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L334)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L334?message=Update%20Docs)]
</div>

  - `:returns`: `str | RegexPattern`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.dtype" class="docs-object-method">&nbsp;</a> 
```python
@property
dtype(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L357)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L357?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L412)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L412?message=Update%20Docs)]
</div>
**LLM Docstring**

Report whether repetition metadata is stored as a `(minimum, maximum)` tuple.
  - `:returns`: `bool`
    > `True` when the condition described above holds; otherwise `False`.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.capturing" class="docs-object-method">&nbsp;</a> 
```python
@property
capturing(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L423)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L423?message=Update%20Docs)]
</div>
**LLM Docstring**

Report whether this node captures directly, including the implicit case where a repeating node contains capturing descendants.
  - `cap`: `object`
    > whether this node captures directly

  - `:returns`: `bool`
    > `True` when the condition described above holds; otherwise `False`.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.get_capturing_groups" class="docs-object-method">&nbsp;</a> 
```python
get_capturing_groups(self, allow_inners=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L452)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L452?message=Update%20Docs)]
</div>
We walk down the tree to find the children with capturing groups in them and
then find the outermost RegexPattern for those unless allow_inners is on in which case we pull them all


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.captures" class="docs-object-method">&nbsp;</a> 
```python
@property
captures(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L469)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L469?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L478)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L478?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L497)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L497?message=Update%20Docs)]
</div>
Returns the named children for the pattern
  - `:returns`: `_`
    >


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.combine" class="docs-object-method">&nbsp;</a> 
```python
combine(self, other, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L530)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L530?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L610)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L610?message=Update%20Docs)]
</div>
Applies wrapper function


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.build" class="docs-object-method">&nbsp;</a> 
```python
build(self, joiner=None, prefix=None, suffix=None, recompile=True, no_captures=False, verbose=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L641)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L641?message=Update%20Docs)]
</div>
**LLM Docstring**

Recursively build the regex text for this node, suppressing inner captures when an outer node captures, applying prefix/joiner/suffix and wrapper functions, and caching the normal capturing form.
  - `joiner`: `object`
    > text or a pattern inserted between children

  - `prefix`: `object`
    > text or a pattern prepended to this node

  - `suffix`: `object`
    > text or a pattern appended to this node

  - `recompile`: `object`
    > whether to rebuild instead of reusing cached regex text

  - `no_captures`: `object`
    > whether captures are suppressed throughout this build

  - `verbose`: `object`
    > whether to print intermediate regex construction details

  - `:returns`: `str`
    > The regex source or textual representation constructed by the operation.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.compiled" class="docs-object-method">&nbsp;</a> 
```python
@property
compiled(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L746)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L746?message=Update%20Docs)]
</div>
**LLM Docstring**

Compile and cache the regex string returned by `build`.
  - `:returns`: `object`
    > The cached compiled regular-expression object.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.add_parent" class="docs-object-method">&nbsp;</a> 
```python
add_parent(self, parent): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L760)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L760?message=Update%20Docs)]
</div>
**LLM Docstring**

Register an ancestor that must be invalidated when this node changes.
  - `parent`: `object`
    > the parent reader or regex node

  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.remove_parent" class="docs-object-method">&nbsp;</a> 
```python
remove_parent(self, parent): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L773)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L773?message=Update%20Docs)]
</div>
**LLM Docstring**

Remove a previously registered ancestor.
  - `parent`: `object`
    > the parent reader or regex node

  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.add_child" class="docs-object-method">&nbsp;</a> 
```python
add_child(self, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L787)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L787?message=Update%20Docs)]
</div>
**LLM Docstring**

Append one child, update named/capturing-descendant flags, and invalidate this node and its ancestors.
  - `child`: `object`
    > the child pattern to add or remove

  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.add_children" class="docs-object-method">&nbsp;</a> 
```python
add_children(self, children): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L804)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L804?message=Update%20Docs)]
</div>
**LLM Docstring**

Append several children, merge their named/capturing-descendant flags, and invalidate caches.
  - `children`: `object`
    > child patterns combined by this node

  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.remove_child" class="docs-object-method">&nbsp;</a> 
```python
remove_child(self, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L821)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L821?message=Update%20Docs)]
</div>
**LLM Docstring**

Remove one child, recompute descendant flags from the remaining children, and invalidate caches.
  - `child`: `object`
    > the child pattern to add or remove

  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.insert_child" class="docs-object-method">&nbsp;</a> 
```python
insert_child(self, index, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L838)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L838?message=Update%20Docs)]
</div>
**LLM Docstring**

Insert a child at a specific position and invalidate cached pattern state.
  - `index`: `object`
    > the insertion position

  - `child`: `object`
    > the child pattern to add or remove

  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.invalidate_cache" class="docs-object-method">&nbsp;</a> 
```python
invalidate_cache(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L857)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L857?message=Update%20Docs)]
</div>
**LLM Docstring**

Clear built-string, compiled-regex, and capturing-group caches, then recursively invalidate all parents.
  - `:returns`: `None`
    > None.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.__copy__" class="docs-object-method">&nbsp;</a> 
```python
__copy__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L880)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L880?message=Update%20Docs)]
</div>
**LLM Docstring**

Make a shallow node copy with an independent child list, no parents, and no built-pattern cache.
  - `:returns`: `object`
    > An independent shallow copy of the regex node.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L898)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L898?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L925)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L925?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L952)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L952?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1024)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1024?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a diagnostic representation containing the key, child count, and primitive pattern.
  - `:returns`: `str`
    > The regex source or textual representation constructed by the operation.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.__str__" class="docs-object-method">&nbsp;</a> 
```python
__str__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1039)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1039?message=Update%20Docs)]
</div>
**LLM Docstring**

Build and return the regex source string.
  - `:returns`: `str`
    > The regex source or textual representation constructed by the operation.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1051)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1051?message=Update%20Docs)]
</div>
**LLM Docstring**

Look up a directly named child by its key.
  - `item`: `object`
    > the child key or array index/slice being accessed

  - `:returns`: `object`
    > The named child or populated array portion selected by the index.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.match" class="docs-object-method">&nbsp;</a> 
```python
match(self, txt, *args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1066)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1066?message=Update%20Docs)]
</div>
**LLM Docstring**

Match the compiled pattern only at the beginning of the input.
  - `txt`: `object`
    > the input text or text block to parse

  - `args`: `tuple`
    > positional arguments forwarded to the wrapped callable

  - `:returns`: `object`
    > match the compiled pattern only at the beginning of the input.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.fullmatch" class="docs-object-method">&nbsp;</a> 
```python
fullmatch(self, txt, *args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1082)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1082?message=Update%20Docs)]
</div>
**LLM Docstring**

Require the compiled pattern to match the complete input.
  - `txt`: `object`
    > the input text or text block to parse

  - `args`: `tuple`
    > positional arguments forwarded to the wrapped callable

  - `:returns`: `object`
    > require the compiled pattern to match the complete input.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.search" class="docs-object-method">&nbsp;</a> 
```python
search(self, txt, *args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1098)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1098?message=Update%20Docs)]
</div>
**LLM Docstring**

Find the first occurrence of the compiled pattern in the input.
  - `txt`: `object`
    > the input text or text block to parse

  - `args`: `tuple`
    > positional arguments forwarded to the wrapped callable

  - `:returns`: `object`
    > find the first occurrence of the compiled pattern in the input.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.findall" class="docs-object-method">&nbsp;</a> 
```python
findall(self, txt, *args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1114)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1114?message=Update%20Docs)]
</div>
**LLM Docstring**

Return all non-overlapping matches of the compiled pattern.
  - `txt`: `object`
    > the input text or text block to parse

  - `args`: `tuple`
    > positional arguments forwarded to the wrapped callable

  - `:returns`: `object`
    > return all non-overlapping matches of the compiled pattern.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.finditer" class="docs-object-method">&nbsp;</a> 
```python
finditer(self, txt, *args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1130?message=Update%20Docs)]
</div>
**LLM Docstring**

Iterate over match objects for all non-overlapping matches.
  - `txt`: `object`
    > the input text or text block to parse

  - `args`: `tuple`
    > positional arguments forwarded to the wrapped callable

  - `:returns`: `object`
    > An iterator yielding the records described above.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.sub" class="docs-object-method">&nbsp;</a> 
```python
sub(self, rep, txt, *args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1146)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1146?message=Update%20Docs)]
</div>
**LLM Docstring**

Replace matches using `re.sub`.
  - `rep`: `object`
    > the replacement string or callable

  - `txt`: `object`
    > the input text or text block to parse

  - `args`: `tuple`
    > positional arguments forwarded to the wrapped callable

  - `:returns`: `object`
    > replace matches using `re.sub`.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.subn" class="docs-object-method">&nbsp;</a> 
```python
subn(self, rep, txt, *args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1165)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1165?message=Update%20Docs)]
</div>
**LLM Docstring**

Replace matches and return both the resulting text and replacement count.
  - `rep`: `object`
    > the replacement string or callable

  - `txt`: `object`
    > the input text or text block to parse

  - `args`: `tuple`
    > positional arguments forwarded to the wrapped callable

  - `:returns`: `object`
    > replace matches and return both the resulting text and replacement count.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.replace" class="docs-object-method">&nbsp;</a> 
```python
replace(self, txt, replacement, *args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1184)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1184?message=Update%20Docs)]
</div>
**LLM Docstring**

Replace matches with a supplied replacement string or callable.
  - `txt`: `object`
    > the input text or text block to parse

  - `replacement`: `object`
    > the replacement string or callable

  - `args`: `tuple`
    > positional arguments forwarded to the wrapped callable

  - `:returns`: `object`
    > replace matches with a supplied replacement string or callable.


<a id="McUtils.Parsers.RegexPatterns.RegexPattern.remove" class="docs-object-method">&nbsp;</a> 
```python
remove(self, txt, *args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1203)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns/RegexPattern.py#L1203?message=Update%20Docs)]
</div>
**LLM Docstring**

Delete every match by replacing it with an empty string.
  - `txt`: `object`
    > the input text or text block to parse

  - `args`: `tuple`
    > positional arguments forwarded to the wrapped callable

  - `:returns`: `object`
    > delete every match by replacing it with an empty string.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Parsers/RegexPatterns.py#L50?message=Update%20Docs)   
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