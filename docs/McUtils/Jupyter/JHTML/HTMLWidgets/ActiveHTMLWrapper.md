## <a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper">ActiveHTMLWrapper</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets.py#L14?message=Update%20Docs)]
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
__init__(self, *elements, tag=None, cls=None, id=None, value=None, style=None, event_handlers=None, inner_html=None, javascript_handles=None, onevents=None, data=None, unsynced_properties=None, debug_pane=None, track_value=None, continuous_update=None, **attributes): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets.py#L18)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets.py#L18?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, *elems, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L215)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L215?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.canonicalize_widget" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_widget(cls, x): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L231)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L231?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.clean_props" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
clean_props(cls, props, to_str=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L260)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L260?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.from_HTML" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_HTML(cls, x: McUtils.Jupyter.JHTML.HTML.HTML.XMLElement, event_handlers=None, debug_pane=None, **props): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L285)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L285?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.load_HTMLElement" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_HTMLElement(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L318)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L318?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.convert_child" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
convert_child(cls, c): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L322)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L322?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.to_html" class="docs-object-method">&nbsp;</a> 
```python
to_html(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L364)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L364?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.find" class="docs-object-method">&nbsp;</a> 
```python
find(self, path, find_mirror=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L393)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L393?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.findall" class="docs-object-method">&nbsp;</a> 
```python
findall(self, path, find_mirror=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L398)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L398?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.iterfind" class="docs-object-method">&nbsp;</a> 
```python
iterfind(self, path, find_mirror=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L403)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L403?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.find_by_id" class="docs-object-method">&nbsp;</a> 
```python
find_by_id(self, id, mode='first', parent=None, find_mirror=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L409)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L409?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.to_widget" class="docs-object-method">&nbsp;</a> 
```python
to_widget(self, parent=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L434)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L434?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L436)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L436?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.display" class="docs-object-method">&nbsp;</a> 
```python
display(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L451)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L451?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.get_mime_bundle" class="docs-object-method">&nbsp;</a> 
```python
get_mime_bundle(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L456)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L456?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.handle_event" class="docs-object-method">&nbsp;</a> 
```python
handle_event(self, e): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L485)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L485?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.link" class="docs-object-method">&nbsp;</a> 
```python
link(self, elem): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L489)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L489?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.tag" class="docs-object-method">&nbsp;</a> 
```python
@property
tag(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L498)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L498?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.id" class="docs-object-method">&nbsp;</a> 
```python
@property
id(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L501)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L501?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.text" class="docs-object-method">&nbsp;</a> 
```python
@property
text(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L510)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L510?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.value" class="docs-object-method">&nbsp;</a> 
```python
@property
value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L520)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L520?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.attrs" class="docs-object-method">&nbsp;</a> 
```python
@property
attrs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L529)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L529?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L554)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L554?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, item, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L559)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L559?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.__delitem__" class="docs-object-method">&nbsp;</a> 
```python
__delitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L564)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L564?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.get_attribute" class="docs-object-method">&nbsp;</a> 
```python
get_attribute(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L569)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L569?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.set_attribute" class="docs-object-method">&nbsp;</a> 
```python
set_attribute(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L590)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L590?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.del_attribute" class="docs-object-method">&nbsp;</a> 
```python
del_attribute(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L616)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L616?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.get_child" class="docs-object-method">&nbsp;</a> 
```python
get_child(self, position, wrapper=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L641)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L641?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.set_child" class="docs-object-method">&nbsp;</a> 
```python
set_child(self, position, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L654)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L654?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.insert" class="docs-object-method">&nbsp;</a> 
```python
insert(self, where, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L666)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L666?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.append" class="docs-object-method">&nbsp;</a> 
```python
append(self, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L685)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L685?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.del_child" class="docs-object-method">&nbsp;</a> 
```python
del_child(self, position): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L687)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L687?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.activate_body" class="docs-object-method">&nbsp;</a> 
```python
activate_body(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L699)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L699?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.elements" class="docs-object-method">&nbsp;</a> 
```python
@property
elements(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L703)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L703?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.children" class="docs-object-method">&nbsp;</a> 
```python
@property
children(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L713)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L713?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.html_string" class="docs-object-method">&nbsp;</a> 
```python
@property
html_string(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L720)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L720?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.html" class="docs-object-method">&nbsp;</a> 
```python
@property
html(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L730)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L730?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.load_HTML" class="docs-object-method">&nbsp;</a> 
```python
load_HTML(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L744)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L744?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.javascript_handles" class="docs-object-method">&nbsp;</a> 
```python
@property
javascript_handles(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L751)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L751?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.class_list" class="docs-object-method">&nbsp;</a> 
```python
@property
class_list(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L774)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L774?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.add_class" class="docs-object-method">&nbsp;</a> 
```python
add_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L781)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L781?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.remove_class" class="docs-object-method">&nbsp;</a> 
```python
remove_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L794)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L794?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.style" class="docs-object-method">&nbsp;</a> 
```python
@property
style(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L808)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L808?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.add_styles" class="docs-object-method">&nbsp;</a> 
```python
add_styles(self, **sty): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L815)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L815?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.remove_styles" class="docs-object-method">&nbsp;</a> 
```python
remove_styles(self, *sty): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L821)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L821?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.data" class="docs-object-method">&nbsp;</a> 
```python
@property
data(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L829)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L829?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.event_handlers" class="docs-object-method">&nbsp;</a> 
```python
@property
event_handlers(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L836)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L836?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.update_events" class="docs-object-method">&nbsp;</a> 
```python
update_events(self, events): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L845)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L845?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.add_event" class="docs-object-method">&nbsp;</a> 
```python
add_event(self, send=True, **events): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L848)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L848?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.remove_event" class="docs-object-method">&nbsp;</a> 
```python
remove_event(self, *events, send=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L876)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L876?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.wait_for_message" class="docs-object-method">&nbsp;</a> 
```python
wait_for_message(self, msg, callback, suppress_others=False, timeout=1, poll_interval=0.05): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L904)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L904?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.call" class="docs-object-method">&nbsp;</a> 
```python
call(self, method, buffers=None, return_message=None, callback=None, timeout=1, poll_interval=0.05, suppress_others=False, **content): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L931)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L931?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.add_javascript" class="docs-object-method">&nbsp;</a> 
```python
add_javascript(self, **methods): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L983)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L983?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.remove_javascript" class="docs-object-method">&nbsp;</a> 
```python
remove_javascript(self, *methods): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L991)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L991?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.trigger" class="docs-object-method">&nbsp;</a> 
```python
trigger(self, method, buffers=None, **content): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1002)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1002?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.onevents" class="docs-object-method">&nbsp;</a> 
```python
@property
onevents(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1004)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1004?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.update_onevents" class="docs-object-method">&nbsp;</a> 
```python
update_onevents(self, events): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1013)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1013?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.on" class="docs-object-method">&nbsp;</a> 
```python
on(self, send=True, **events): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1016)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1016?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.off" class="docs-object-method">&nbsp;</a> 
```python
off(self, *events, send=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1044)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1044?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.track_value" class="docs-object-method">&nbsp;</a> 
```python
@property
track_value(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1057)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1057?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.continuous_update" class="docs-object-method">&nbsp;</a> 
```python
@property
continuous_update(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1063)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets/ActiveHTMLWrapper.py#L1063?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.JHTML.HTMLWidgets.ActiveHTMLWrapper.loader" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
loader(cls, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1080)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1080?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/JHTML/HTMLWidgets.py#L14?message=Update%20Docs)   
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