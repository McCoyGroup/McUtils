## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.FormatDirective">FormatDirective</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L272)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L272?message=Update%20Docs)]
</div>

Base class for directives -- shouldn't be an enum really...







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.FormatDirective.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name, callback=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L276)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L276?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize an enum directive with its template key and normalized callback.
  - `name`: `Any`
    > an explicit display name
  - `callback`: `Any`
    > the function receiving each generated comprehension result

  - `:returns`: `None`
    > `None`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.FormatDirective.extend" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
extend(cls, *others): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L342)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L342?message=Update%20Docs)]
</div>
**LLM Docstring**

Create a new directive enumeration containing members from this class and additional enumerations.
  - `others`: `Any`
    > additional directive enumerations to merge

  - `:returns`: `Any`
    > A new `FormatDirective` enumeration containing the merged members.


<a id="enum.Enum.__new__" class="docs-object-method">&nbsp;</a> 
```python
__new__(cls, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/enum/Enum.py#L670)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/enum/Enum.py#L670?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/FormatDirective.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/FormatDirective.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/TemplateEngine/FormatDirective.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/TemplateEngine/FormatDirective.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L272?message=Update%20Docs)   
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