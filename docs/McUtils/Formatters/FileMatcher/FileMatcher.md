## <a id="McUtils.Formatters.FileMatcher.FileMatcher">FileMatcher</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/FileMatcher.py#L94)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/FileMatcher.py#L94?message=Update%20Docs)]
</div>

Defines a filter that uses StringMatcher to specifically match files







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Formatters.FileMatcher.FileMatcher.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, match_patterns, negative_match=False, use_basename=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/FileMatcher.py#L99)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/FileMatcher.py#L99?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize `FileMatcher` state from the supplied configuration.
  - `match_patterns`: `object`
    > regex, matcher, predicate, or iterable of match specifications
  - `negative_match`: `object`
    > whether to invert the match result
  - `use_basename`: `object`
    > whether matching is performed only on `os.path.basename(f)`
  - `:returns`: `None`
    > `None`; the operation mutates state, writes output, or raises by design.


<a id="McUtils.Formatters.FileMatcher.FileMatcher.matches" class="docs-object-method">&nbsp;</a> 
```python
matches(self, f): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/FileMatcher/FileMatcher.py#L117)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/FileMatcher/FileMatcher.py#L117?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate the configured matcher against the input and apply optional negation.
  - `f`: `object`
    > string or file path being tested
  - `:returns`: `bool`
    > whether the input satisfies the matcher after optional negation
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/FileMatcher/FileMatcher.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/FileMatcher/FileMatcher.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/FileMatcher/FileMatcher.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/FileMatcher/FileMatcher.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/FileMatcher.py#L94?message=Update%20Docs)   
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