## <a id="McUtils.Docs.DocWalker.MethodWriter">MethodWriter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/DocWalker.py#L1182)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker.py#L1182?message=Update%20Docs)]
</div>

Writes class methods to file
(distinct from functions since not expected to exist solo)







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
template: str
```
<a id="McUtils.Docs.DocWalker.MethodWriter.get_template_params" class="docs-object-method">&nbsp;</a> 
```python
get_template_params(self, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/DocWalker/MethodWriter.py#L1190)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker/MethodWriter.py#L1190?message=Update%20Docs)]
</div>
**LLM Docstring**

Collects method template parameters after unwrapping class, static, and property descriptors.

The original descriptor is restored even if metadata extraction fails.
  - `kwargs`: `Any`
    > options forwarded to the function writer
  - `:returns`: `dict`
    > the method template parameters including decorator text


<a id="McUtils.Docs.DocWalker.MethodWriter.get_signature" class="docs-object-method">&nbsp;</a> 
```python
get_signature(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/DocWalker/MethodWriter.py#L1225)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker/MethodWriter.py#L1225?message=Update%20Docs)]
</div>
**LLM Docstring**

Returns the handled method signature, falling back to `(self)` for non-inspectable properties.
  - `:returns`: `str`
    > the stringified method signature


<a id="McUtils.Docs.DocWalker.MethodWriter.identifier" class="docs-object-method">&nbsp;</a> 
```python
@property
identifier(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/DocWalker/MethodWriter.py#L1239)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker/MethodWriter.py#L1239?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolves the method identifier, constructing property identifiers from their parent class.
  - `:returns`: `str`
    > the fully qualified method identifier
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/DocWalker/MethodWriter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/DocWalker/MethodWriter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/DocWalker/MethodWriter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/DocWalker/MethodWriter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/DocWalker.py#L1182?message=Update%20Docs)   
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