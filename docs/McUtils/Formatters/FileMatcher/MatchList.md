## <a id="McUtils.Formatters.FileMatcher.MatchList">MatchList</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/FileMatcher.py#L61)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/FileMatcher.py#L61?message=Update%20Docs)]
</div>

Defines a set of matches that must be matched directly (uses `set` to make this basically a constant time check)







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Formatters.FileMatcher.MatchList.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *matches, negative_match=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/FileMatcher.py#L66)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/FileMatcher.py#L66?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize `MatchList` state from the supplied configuration.
  - `matches`: `tuple`
    > additional positional values forwarded or collected by this operation
  - `negative_match`: `object`
    > whether to invert the match result
  - `:returns`: `None`
    > `None`; the operation mutates state, writes output, or raises by design.


<a id="McUtils.Formatters.FileMatcher.MatchList.test_match" class="docs-object-method">&nbsp;</a> 
```python
test_match(self, f): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/FileMatcher/MatchList.py#L81)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/FileMatcher/MatchList.py#L81?message=Update%20Docs)]
</div>
**LLM Docstring**

Test constant-time membership in the stored literal match set.
  - `f`: `object`
    > string or file path being tested
  - `:returns`: `bool`
    > whether the input is present in the literal match set
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/FileMatcher/MatchList.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/FileMatcher/MatchList.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/FileMatcher/MatchList.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/FileMatcher/MatchList.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/FileMatcher.py#L61?message=Update%20Docs)   
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