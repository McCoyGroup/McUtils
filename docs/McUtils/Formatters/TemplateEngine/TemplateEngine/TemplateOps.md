## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps">TemplateOps</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Formatters/TemplateEngine/TemplateEngine.py#L30)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine.py#L30?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.loop" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
loop(caller: Callable, *args, joiner='', formatter=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L31)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L31?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.loop_template" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
loop_template(cls, template: str, *args, joiner='', formatter=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L48?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.join" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
join(*args, joiner=' ', formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L57)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L57?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.load" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load(cls, template, formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L62)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L62?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.include" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
include(cls, template, formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L65)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L65?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.apply" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
apply(cls, template, *args, formatter=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L68)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L68?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.nonempty" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
nonempty(cls, data, formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L73)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L73?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.wrap" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
wrap(cls, fn): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L76)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L76?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.cleandoc" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
cleandoc(txt, formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L82)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L82?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.wrap_str" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
wrap_str(obj, formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L85)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L85?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.optional" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
optional(key, default='', formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L92)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L92?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateOps.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateOps.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateOps.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TemplateEngine/TemplateEngine/TemplateOps.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Formatters/TemplateEngine/TemplateEngine.py#L30?message=Update%20Docs)   
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