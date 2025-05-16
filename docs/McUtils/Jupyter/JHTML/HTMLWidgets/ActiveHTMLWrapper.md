## <a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper">ActiveHTMLWrapper</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets.py#L14?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
base: NoneType
LazyLoader: LazyLoader
```
<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *elements, tag=None, cls=None, id=None, value=None, style=None, event_handlers=None, javascript_handles=None, onevents=None, data=None, debug_pane=None, track_value=None, continuous_update=None, **attributes): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L18)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L18?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, *elems, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L207)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L207?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.canonicalize_widget" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_widget(cls, x): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L223)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L223?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.from_HTML" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_HTML(cls, x: McUtils.Jupyter.JHTML.HTML.HTML.XMLElement, event_handlers=None, debug_pane=None, **props): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L247)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L247?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.load_HTMLElement" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_HTMLElement(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L271)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L271?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.convert_child" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
convert_child(cls, c): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L275)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L275?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.to_html" class="docs-object-method">&nbsp;</a> 
```python
to_html(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L317)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L317?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.find" class="docs-object-method">&nbsp;</a> 
```python
find(self, path, find_mirror=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L346)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L346?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.findall" class="docs-object-method">&nbsp;</a> 
```python
findall(self, path, find_mirror=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L351)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L351?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.iterfind" class="docs-object-method">&nbsp;</a> 
```python
iterfind(self, path, find_mirror=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L356)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L356?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.find_by_id" class="docs-object-method">&nbsp;</a> 
```python
find_by_id(self, id, mode='first', parent=None, find_mirror=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L362)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L362?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.to_widget" class="docs-object-method">&nbsp;</a> 
```python
to_widget(self, parent=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L387)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L387?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L389)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L389?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.display" class="docs-object-method">&nbsp;</a> 
```python
display(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L404)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L404?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.get_mime_bundle" class="docs-object-method">&nbsp;</a> 
```python
get_mime_bundle(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L409)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L409?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.handle_event" class="docs-object-method">&nbsp;</a> 
```python
handle_event(self, e): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L438)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L438?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.link" class="docs-object-method">&nbsp;</a> 
```python
link(self, elem): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L442)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L442?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.tag" class="docs-object-method">&nbsp;</a> 
```python
@property
tag(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L451)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L451?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.id" class="docs-object-method">&nbsp;</a> 
```python
@property
id(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L454)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L454?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.text" class="docs-object-method">&nbsp;</a> 
```python
@property
text(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L463)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L463?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.value" class="docs-object-method">&nbsp;</a> 
```python
@property
value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L473)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L473?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.attrs" class="docs-object-method">&nbsp;</a> 
```python
@property
attrs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L482)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L482?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L507)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L507?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, item, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L512)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L512?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.__delitem__" class="docs-object-method">&nbsp;</a> 
```python
__delitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L517)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L517?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.get_attribute" class="docs-object-method">&nbsp;</a> 
```python
get_attribute(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L522)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L522?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.set_attribute" class="docs-object-method">&nbsp;</a> 
```python
set_attribute(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L543)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L543?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.del_attribute" class="docs-object-method">&nbsp;</a> 
```python
del_attribute(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L569)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L569?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.get_child" class="docs-object-method">&nbsp;</a> 
```python
get_child(self, position, wrapper=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L594)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L594?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.set_child" class="docs-object-method">&nbsp;</a> 
```python
set_child(self, position, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L607)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L607?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.insert" class="docs-object-method">&nbsp;</a> 
```python
insert(self, where, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L619)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L619?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.append" class="docs-object-method">&nbsp;</a> 
```python
append(self, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L638)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L638?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.del_child" class="docs-object-method">&nbsp;</a> 
```python
del_child(self, position): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L640)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L640?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.activate_body" class="docs-object-method">&nbsp;</a> 
```python
activate_body(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L652)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L652?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.elements" class="docs-object-method">&nbsp;</a> 
```python
@property
elements(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L656)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L656?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.children" class="docs-object-method">&nbsp;</a> 
```python
@property
children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L666)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L666?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.html_string" class="docs-object-method">&nbsp;</a> 
```python
@property
html_string(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L673)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L673?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.html" class="docs-object-method">&nbsp;</a> 
```python
@property
html(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L683)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L683?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.load_HTML" class="docs-object-method">&nbsp;</a> 
```python
load_HTML(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L697)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L697?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.javascript_handles" class="docs-object-method">&nbsp;</a> 
```python
@property
javascript_handles(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L704)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L704?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.class_list" class="docs-object-method">&nbsp;</a> 
```python
@property
class_list(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L727)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L727?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.add_class" class="docs-object-method">&nbsp;</a> 
```python
add_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L734)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L734?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.remove_class" class="docs-object-method">&nbsp;</a> 
```python
remove_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L747)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L747?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.style" class="docs-object-method">&nbsp;</a> 
```python
@property
style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L761)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L761?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.add_styles" class="docs-object-method">&nbsp;</a> 
```python
add_styles(self, **sty): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L768)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L768?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.remove_styles" class="docs-object-method">&nbsp;</a> 
```python
remove_styles(self, *sty): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L774)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L774?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.data" class="docs-object-method">&nbsp;</a> 
```python
@property
data(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L782)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L782?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.event_handlers" class="docs-object-method">&nbsp;</a> 
```python
@property
event_handlers(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L789)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L789?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.update_events" class="docs-object-method">&nbsp;</a> 
```python
update_events(self, events): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L798)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L798?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.add_event" class="docs-object-method">&nbsp;</a> 
```python
add_event(self, send=True, **events): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L801)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L801?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.remove_event" class="docs-object-method">&nbsp;</a> 
```python
remove_event(self, *events, send=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L829)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L829?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.wait_for_message" class="docs-object-method">&nbsp;</a> 
```python
wait_for_message(self, msg, callback, suppress_others=False, timeout=1, poll_interval=0.05): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L857)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L857?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.call" class="docs-object-method">&nbsp;</a> 
```python
call(self, method, buffers=None, return_message=None, callback=None, timeout=1, poll_interval=0.05, suppress_others=False, **content): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L884)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L884?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.add_javascript" class="docs-object-method">&nbsp;</a> 
```python
add_javascript(self, **methods): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L936)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L936?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.remove_javascript" class="docs-object-method">&nbsp;</a> 
```python
remove_javascript(self, *methods): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L944)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L944?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.trigger" class="docs-object-method">&nbsp;</a> 
```python
trigger(self, method, buffers=None, **content): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L955)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L955?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.onevents" class="docs-object-method">&nbsp;</a> 
```python
@property
onevents(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L957)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L957?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.update_onevents" class="docs-object-method">&nbsp;</a> 
```python
update_onevents(self, events): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L966)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L966?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.on" class="docs-object-method">&nbsp;</a> 
```python
on(self, send=True, **events): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L969)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L969?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.off" class="docs-object-method">&nbsp;</a> 
```python
off(self, *events, send=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L997)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L997?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.track_value" class="docs-object-method">&nbsp;</a> 
```python
@property
track_value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1010)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1010?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.continuous_update" class="docs-object-method">&nbsp;</a> 
```python
@property
continuous_update(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1016)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1016?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.loader" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
loader(cls, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L1033)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L1033?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/JHTML/HTMLWidgets.py#L14?message=Update%20Docs)   
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