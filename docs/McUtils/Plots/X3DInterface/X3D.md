## <a id="McUtils.Plots.X3DInterface.X3D">X3D</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface.py#L41)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L41?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
defaults: dict
X3DOM_JS: str
X3DOM_CSS: str
include_export_button: bool
include_record_button: bool
```
<a id="McUtils.Plots.X3DInterface.X3D.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *children, id=None, dynamic_loading=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface.py#L46)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L46?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.X3DInterface.X3D.get_export_script" class="docs-object-method">&nbsp;</a> 
```python
get_export_script(self, id): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L59)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L59?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.X3DInterface.X3D.get_record_screen_script" class="docs-object-method">&nbsp;</a> 
```python
get_record_screen_script(self, id, polling_rate=30, recording_duration=2, video_format='video/webm'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L70)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L70?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.X3DInterface.X3D.set_animation_duration_script" class="docs-object-method">&nbsp;</a> 
```python
set_animation_duration_script(self, id): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L108)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L108?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.X3DInterface.X3D.to_widget" class="docs-object-method">&nbsp;</a> 
```python
to_widget(self, dynamic_loading=None, include_export_button=None, include_record_button=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L120)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L120?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.X3DInterface.X3D.to_html" class="docs-object-method">&nbsp;</a> 
```python
to_html(self, *base_elems, header_elems=None, dynamic_loading=False, include_export_button=None, include_record_button=None, **header_info): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L174)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L174?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.X3DInterface.X3D.get_mime_bundle" class="docs-object-method">&nbsp;</a> 
```python
get_mime_bundle(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L202)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L202?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.X3DInterface.X3D.to_x3d" class="docs-object-method">&nbsp;</a> 
```python
to_x3d(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L204)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L204?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.X3DInterface.X3D.display" class="docs-object-method">&nbsp;</a> 
```python
display(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L216)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L216?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.X3DInterface.X3D.show" class="docs-object-method">&nbsp;</a> 
```python
show(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L219)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L219?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.X3DInterface.X3D.dump" class="docs-object-method">&nbsp;</a> 
```python
dump(self, file, write_html=True, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/X3DInterface/X3D.py#L224)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface/X3D.py#L224?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/X3DInterface/X3D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/X3DInterface/X3D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/X3DInterface/X3D.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/X3DInterface/X3D.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/X3DInterface.py#L41?message=Update%20Docs)   
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