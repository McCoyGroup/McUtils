## <a id="McUtils.Jupyter.JHTML.JHTML.JHTML">JHTML</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/JHTML.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML.py#L14?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
HTML: HTML
HTMLManager: HTMLManager
CSS: CSS
XML: ContentXML
HTMLWidgets: HTMLWidgets
APIs: JupyterAPIs
DefaultOutputWidget: DefaultOutputWidget
callbacks: dict
widgets: dict
OutputArea: OutputArea
JavascriptAPI: JavascriptAPI
Bootstrap: Bootstrap
Styled: Styled
Compound: Compound
```
<a id="McUtils.Jupyter.JHTML.HTML.HTMLManager.manage_class" class="docs-object-method">&nbsp;</a> 
```python
manage_class(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTML/HTMLManager.py#L353)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTML/HTMLManager.py#L353?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTML.HTMLManager.manage_styles" class="docs-object-method">&nbsp;</a> 
```python
manage_style(styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTML/HTMLManager.py#L368)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTML/HTMLManager.py#L368?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTML.HTMLManager.extract_styles" class="docs-object-method">&nbsp;</a> 
```python
extract_styles(attrs, style_props=None, ignored_styles=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTML/HTMLManager.py#L408)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTML/HTMLManager.py#L408?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTML.HTMLManager.manage_attrs" class="docs-object-method">&nbsp;</a> 
```python
manage_attrs(attrs, sanitize=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTML/HTMLManager.py#L397)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTML/HTMLManager.py#L397?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.load" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load(cls, exec_prefix=None, overwrite=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L33)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L33?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Markdown" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Markdown(cls, text): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L44)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L44?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, context=None, include_bootstrap=False, expose_classes=False, output_pane=True, callbacks=None, widgets=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/JHTML.py#L51)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML.py#L51?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.insert_vars" class="docs-object-method">&nbsp;</a> 
```python
insert_vars(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L76)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L76?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.wrap_callbacks" class="docs-object-method">&nbsp;</a> 
```python
wrap_callbacks(self, c): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L91)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L91?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L106)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L106?message=Update%20Docs)]
</div>
To make writing HTML interactively a bit nicer
  - `:returns`: `_`
    >


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.out" class="docs-object-method">&nbsp;</a> 
```python
@property
out(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L134)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L134?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.prune_vars" class="docs-object-method">&nbsp;</a> 
```python
prune_vars(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L138)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L138?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L147)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML/JHTML.py#L147?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.parse_handlers" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_handlers(cls, handler_string): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L160)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L160?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.parse_widget" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_widget(cls, uuid): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L176)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L176?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.convert" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
convert(cls, etree, strip=True, converter=None, **extra_attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L184)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L184?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.parse" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse(cls, src, event_handlers=None, dynamic=None, track_value=None, strict=True, fallback=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L213)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L213?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Abbr" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Abbr(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Address" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Address(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Anchor" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Anchor(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Anchor" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
A(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Area" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Area(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Article" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Article(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Aside" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Aside(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Audio" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Audio(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.B" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
B(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Base" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Base(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Bdi" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Bdi(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Bdo" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Bdo(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Blockquote" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Blockquote(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Body" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Body(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Bold" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Bold(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Br" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Br(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Button" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Button(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Canvas" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Canvas(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Caption" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Caption(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Cite" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Cite(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Code" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Code(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Col" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Col(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Colgroup" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Colgroup(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Data" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Data(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Datalist" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Datalist(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Dd" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Dd(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Del" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Del(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Details" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Details(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Dfn" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Dfn(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Dialog" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Dialog(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Div" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Div(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Dl" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Dl(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Dt" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Dt(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Em" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Em(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Embed" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Embed(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Fieldset" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Fieldset(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Figcaption" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Figcaption(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Figure" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Figure(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Footer" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Footer(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Form" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Form(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Head" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Head(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Header" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Header(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Heading" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Heading(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Hr" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Hr(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Html" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Html(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Iframe" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Iframe(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Image" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Image(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Img" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Img(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Input" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Input(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Ins" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Ins(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Italic" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Italic(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Italic" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
I(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Kbd" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Kbd(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Label" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Label(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Legend" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Legend(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Link" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Link(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.List" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
List(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.List" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Ul(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.ListItem" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
ListItem(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.ListItem" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Li(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Main" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Main(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Map(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Mark" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Mark(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Meta" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Meta(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Meter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Meter(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Nav" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Nav(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Noscript" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Noscript(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.NumberedList" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
NumberedList(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.NumberedList" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Ol(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Object" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Object(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Optgroup" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Optgroup(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Option" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Option(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Output" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Output(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Param" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Param(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Picture" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Picture(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Pre" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Pre(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Progress" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Progress(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Q" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Q(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Rp" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Rp(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Rt" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Rt(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Ruby" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Ruby(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.S" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
S(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Samp" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Samp(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Script" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Script(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Section" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Section(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Select" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Select(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Small" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Small(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Source" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Source(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Span" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Span(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Strong" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Strong(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Style" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Style(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Sub" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Sub(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.SubHeading" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
SubHeading(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.SubsubHeading" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
SubsubHeading(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.SubsubsubHeading" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
SubsubsubHeading(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.SubHeading5" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
SubHeading5(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.SubHeading6" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
SubHeading6(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Summary" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Summary(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Sup" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Sup(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Svg" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Svg(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Table" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Table(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.TableBody" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
TableBody(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.TableBody" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Tbody(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.TableFooter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
TableFooter(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.TableFooter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Tfoot(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.TableHeader" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
TableHeader(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.TableHeader" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Thead(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.TableHeading" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
TableHeading(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.TableHeading" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Th(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.TableItem" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
TableItem(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.TableItem" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Td(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.TableRow" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
TableRow(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.TableRow" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Tr(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Template" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Template(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Text" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Text(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Text" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
P(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Textarea" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Textarea(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Time" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Time(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Title" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Title(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Track" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Track(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.U" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
U(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Var" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Var(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Video" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Video(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.JHTML.JHTML.Wbr" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
Wbr(jhtml, *elements, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L283)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L283?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/JHTML/JHTML/JHTML.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/JHTML/JHTML/JHTML.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/JHTML/JHTML/JHTML.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/JHTML/JHTML/JHTML.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/JHTML.py#L14?message=Update%20Docs)   
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