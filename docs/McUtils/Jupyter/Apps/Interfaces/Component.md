## <a id="McUtils.Jupyter.Apps.Interfaces.Component">Component</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces.py#L115)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces.py#L115?message=Update%20Docs)]
</div>

Provides an abstract base class for an interface element
to allow for the easy construction of interesting interfaces







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Jupyter.Apps.Interfaces.Component.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, dynamic=True, debug_pane=None, **attrs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L120)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L120?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.attrs" class="docs-object-method">&nbsp;</a> 
```python
@property
attrs(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L127)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L127?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.get_attr" class="docs-object-method">&nbsp;</a> 
```python
get_attr(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L134)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L134?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.get_child" class="docs-object-method">&nbsp;</a> 
```python
get_child(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L136)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L136?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.__getitem__" class="docs-object-method">&nbsp;</a> 
```python
__getitem__(self, item): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L140)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L140?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.set_attr" class="docs-object-method">&nbsp;</a> 
```python
set_attr(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L146)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L146?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.update_widget_attr" class="docs-object-method">&nbsp;</a> 
```python
update_widget_attr(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L148)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L148?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.set_child" class="docs-object-method">&nbsp;</a> 
```python
set_child(self, which, new): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L150)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L150?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.update_widget_child" class="docs-object-method">&nbsp;</a> 
```python
update_widget_child(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L154)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L154?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.__setitem__" class="docs-object-method">&nbsp;</a> 
```python
__setitem__(self, key, value): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L156?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.del_attr" class="docs-object-method">&nbsp;</a> 
```python
del_attr(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L166)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L166?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.del_widget_attr" class="docs-object-method">&nbsp;</a> 
```python
del_widget_attr(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L168)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L168?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.del_child" class="docs-object-method">&nbsp;</a> 
```python
del_child(self, which): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L170)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L170?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.del_widget_child" class="docs-object-method">&nbsp;</a> 
```python
del_widget_child(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L174)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L174?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.__delitem__" class="docs-object-method">&nbsp;</a> 
```python
__delitem__(self, key): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L176)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L176?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.insert" class="docs-object-method">&nbsp;</a> 
```python
insert(self, where, new): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L186)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L186?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.append" class="docs-object-method">&nbsp;</a> 
```python
append(self, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L190)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L190?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.insert_child" class="docs-object-method">&nbsp;</a> 
```python
insert_child(self, where, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L193)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L193?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.insert_widget_child" class="docs-object-method">&nbsp;</a> 
```python
insert_widget_child(self, where, child): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L197)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L197?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.add_class" class="docs-object-method">&nbsp;</a> 
```python
add_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L200)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L200?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.add_component_class" class="docs-object-method">&nbsp;</a> 
```python
add_component_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L204)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L204?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.add_widget_class" class="docs-object-method">&nbsp;</a> 
```python
add_widget_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L213)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L213?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.remove_class" class="docs-object-method">&nbsp;</a> 
```python
remove_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L215)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L215?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.remove_component_class" class="docs-object-method">&nbsp;</a> 
```python
remove_component_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L219)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L219?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.remove_widget_class" class="docs-object-method">&nbsp;</a> 
```python
remove_widget_class(self, *cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L230)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L230?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.to_jhtml" class="docs-object-method">&nbsp;</a> 
```python
to_jhtml(self, parent=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L233)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L233?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.to_widget" class="docs-object-method">&nbsp;</a> 
```python
to_widget(self, parent=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L236)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L236?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.mutate" class="docs-object-method">&nbsp;</a> 
```python
mutate(self, fn): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L251)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L251?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.Apps.Interfaces.Component.invalidate_cache" class="docs-object-method">&nbsp;</a> 
```python
invalidate_cache(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/Apps/Interfaces/Component.py#L254)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces/Component.py#L254?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/Apps/Interfaces/Component.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/Apps/Interfaces/Component.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/Apps/Interfaces/Component.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/Apps/Interfaces/Component.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/Apps/Interfaces.py#L115?message=Update%20Docs)   
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