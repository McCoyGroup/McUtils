## <a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps">TemplateOps</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L30)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L30?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L31)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L31?message=Update%20Docs)]
</div>
**LLM Docstring**

Call a template operation over synchronized positional and keyword iterables and optionally join the results.
  - `caller`: `typing.Callable`
    > the callable applied to each synchronized argument group
  - `joiner`: `Any`
    > the string used to combine generated values, or `None` to keep a list
  - `formatter`: `Any`
    > the active template formatter
  - `args`: `Any`
    > positional arguments forwarded to the wrapped callable
  - `kwargs`: `Any`
    > keyword arguments forwarded to the wrapped callable

  - `:returns`: `Any`
    > A joined string when `joiner` is not `None`; otherwise the list of callback results.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.loop_template" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
loop_template(cls, template: str, *args, joiner='', formatter=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L67)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L67?message=Update%20Docs)]
</div>
**LLM Docstring**

Format a string template over synchronized iterables using `loop`.
  - `template`: `str`
    > the template name, template text, or template callable
  - `joiner`: `Any`
    > the string used to combine generated values, or `None` to keep a list
  - `formatter`: `Any`
    > the active template formatter
  - `args`: `Any`
    > positional arguments forwarded to the wrapped callable
  - `kwargs`: `Any`
    > keyword arguments forwarded to the wrapped callable

  - `:returns`: `Any`
    > The rendered iterations joined by `joiner`, or the list of rendered values when `joiner` is `None`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.join" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
join(*args, joiner=' ', formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L95)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L95?message=Update%20Docs)]
</div>
**LLM Docstring**

Join a sequence of strings, accepting either separate values or one non-string iterable.
  - `joiner`: `Any`
    > the string used to combine generated values, or `None` to keep a list
  - `formatter`: `Any`
    > the active template formatter
  - `args`: `Any`
    > positional arguments forwarded to the wrapped callable

  - `:returns`: `Any`
    > The input strings combined with `joiner`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.load" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load(cls, template, formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L115?message=Update%20Docs)]
</div>
**LLM Docstring**

Load a named template through the active formatter.
  - `template`: `Any`
    > the template name, template text, or template callable
  - `formatter`: `Any`
    > the active template formatter

  - `:returns`: `Any`
    > The template content returned by the formatter.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.include" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
include(cls, template, formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L131)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L131?message=Update%20Docs)]
</div>
**LLM Docstring**

Load and immediately render another template using the current format parameters.
  - `template`: `Any`
    > the template name, template text, or template callable
  - `formatter`: `Any`
    > the active template formatter

  - `:returns`: `Any`
    > The included template rendered with the current parameter scope.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.apply" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
apply(cls, template, *args, formatter=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L147)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L147?message=Update%20Docs)]
</div>
**LLM Docstring**

Render a template with explicit arguments through the active formatter.
  - `template`: `Any`
    > the template name, template text, or template callable
  - `formatter`: `Any`
    > the active template formatter
  - `args`: `Any`
    > positional arguments forwarded to the wrapped callable
  - `kwargs`: `Any`
    > keyword arguments forwarded to the wrapped callable

  - `:returns`: `Any`
    > The rendered template string.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.nonempty" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
nonempty(cls, data, formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L169?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether a value is non-`None` and has positive length.
  - `data`: `Any`
    > the value or collection being tested
  - `formatter`: `Any`
    > the active template formatter

  - `:returns`: `Any`
    > `True` when `data` is non-`None` and nonempty; otherwise `False`.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.wrap" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
wrap(cls, fn): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L185)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L185?message=Update%20Docs)]
</div>
**LLM Docstring**

Adapt a callable so it accepts and ignores the formatter keyword injected into directives.
  - `fn`: `Any`
    > the callable to wrap

  - `:returns`: `Any`
    > A wrapper callable that ignores the injected formatter keyword.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.cleandoc" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
cleandoc(txt, formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L217)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L217?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize indentation and surrounding whitespace in documentation text.
  - `txt`: `Any`
    > the text to normalize
  - `formatter`: `Any`
    > the active template formatter

  - `:returns`: `Any`
    > The cleaned documentation text.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.wrap_str" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
wrap_str(obj, formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L233)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L233?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert an object to an escaped string literal, using triple quotes for multiline text.
  - `obj`: `Any`
    > the object to inspect or dispatch
  - `formatter`: `Any`
    > the active template formatter

  - `:returns`: `Any`
    > An escaped single-line or triple-quoted string representation.


<a id="McUtils.Formatters.TemplateEngine.TemplateEngine.TemplateOps.optional" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
optional(key, default='', formatter=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/staticmethod.py#L253)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/staticmethod.py#L253?message=Update%20Docs)]
</div>
**LLM Docstring**

Retrieve an optional formatting parameter with a fallback value.
  - `key`: `Any`
    > the lookup, assignment, or formatting key
  - `default`: `Any`
    > fallback callable or value used when no match is found
  - `formatter`: `Any`
    > the active template formatter

  - `:returns`: `Any`
    > The current parameter value for `key`, or `default` when it is absent.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TemplateEngine/TemplateEngine.py#L30?message=Update%20Docs)   
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