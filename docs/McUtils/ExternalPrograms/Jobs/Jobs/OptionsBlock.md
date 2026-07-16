## <a id="McUtils.ExternalPrograms.Jobs.Jobs.OptionsBlock">OptionsBlock</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs.py#L83)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs.py#L83?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
require_value: NoneType
```
<a id="McUtils.ExternalPrograms.Jobs.Jobs.OptionsBlock.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, canonicalize_opts=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs.py#L86)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs.py#L86?message=Update%20Docs)]
</div>
**LLM Docstring**

Store the block options, canonicalizing their names against the block's known
properties/aliases unless disabled.
  - `canonicalize_opts`: `bool`
    > canonicalize and validate the option names
  - `opts`: `Any`
    > the block options


<a id="McUtils.ExternalPrograms.Jobs.Jobs.OptionsBlock.get_props" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_props(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L102)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L102?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the tuple of option names this block accepts.
  - `:returns`: `tuple`
    > the accepted property names


<a id="McUtils.ExternalPrograms.Jobs.Jobs.OptionsBlock.get_aliases" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_aliases(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L113)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L113?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the mapping of canonical option names to their accepted aliases.
  - `:returns`: `dict`
    > the alias mapping


<a id="McUtils.ExternalPrograms.Jobs.Jobs.OptionsBlock.get_canonical_opts_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_canonical_opts_map(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L124)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L124?message=Update%20Docs)]
</div>
**LLM Docstring**

Return (and cache) the lower-case-to-canonical mapping of the block's property
names.
  - `:returns`: `dict`
    > the canonicalization mapping


<a id="McUtils.ExternalPrograms.Jobs.Jobs.OptionsBlock.get_props_set" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_props_set(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L141)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L141?message=Update%20Docs)]
</div>
**LLM Docstring**

Return (and cache) the set of accepted property names, for fast membership
checks.
  - `:returns`: `set`
    > the set of accepted properties


<a id="McUtils.ExternalPrograms.Jobs.Jobs.OptionsBlock.get_inverse_alias_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_inverse_alias_map(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L156?message=Update%20Docs)]
</div>
**LLM Docstring**

Return (and cache) the lower-case-alias-to-canonical-name mapping.
  - `:returns`: `dict`
    > the inverse alias mapping


<a id="McUtils.ExternalPrograms.Jobs.Jobs.OptionsBlock.check_canon" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
check_canon(cls, opt, val): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L175)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L175?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether an option belongs to this block, returning its canonical name.

Honors `require_value`: options that require a value (or require none) are
rejected when the supplied value doesn't match.
  - `opt`: `str`
    > the option name
  - `val`: `Any`
    > the option value
  - `:returns`: `tuple[bool, str]`
    > `(belongs_to_block, canonical_name)`


<a id="McUtils.ExternalPrograms.Jobs.Jobs.OptionsBlock.canonicalize_opt_name" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_opt_name(cls, opt): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L204)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L204?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve an option name to its canonical form via the alias and canonicalization
maps.
  - `opt`: `str`
    > the option name
  - `:returns`: `str`
    > the canonical option name


<a id="McUtils.ExternalPrograms.Jobs.Jobs.OptionsBlock.check_opts" class="docs-object-method">&nbsp;</a> 
```python
check_opts(self, opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Jobs/Jobs/OptionsBlock.py#L220)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs/OptionsBlock.py#L220?message=Update%20Docs)]
</div>
**LLM Docstring**

Canonicalize and validate a set of options, raising on unknown or duplicated
names.
  - `opts`: `dict`
    > the raw options
  - `:returns`: `dict`
    > the canonicalized options


<a id="McUtils.ExternalPrograms.Jobs.Jobs.OptionsBlock.prep_opts" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
prep_opts(cls, opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L253)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L253?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize an option value into the canonical `[positional_list, keyword_dict]`
form.

Accepts `True` (no options), a bare string, a mapping, or an existing
`[list, dict]` pair.
  - `opts`: `Any`
    > the option value to normalize
  - `:returns`: `list`
    > `[positional_options, keyword_options]`
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Jobs/Jobs/OptionsBlock.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Jobs/Jobs/OptionsBlock.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Jobs/Jobs/OptionsBlock.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Jobs/Jobs/OptionsBlock.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Jobs/Jobs.py#L83?message=Update%20Docs)   
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