## <a id="McUtils.Jupyter.ImageTools.DisplayImage">DisplayImage</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/ImageTools.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/ImageTools.py#L15?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
multivalue_attrs: set
default_annotation_pattern: NoneType
default_annotation_exclude: str
```
<a id="McUtils.Jupyter.ImageTools.DisplayImage.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, figure, format, plot_range=None, scaling_factor=None, splits=None, postdraw=None, include_save_buttons=False, id=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/ImageTools.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/ImageTools.py#L16?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.ImageTools.DisplayImage.split_string_by_segments" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
split_string_by_segments(cls, text, split_dict): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L37)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L37?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.ImageTools.DisplayImage.add_classes" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
add_classes(cls, label, text): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L343)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L343?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.ImageTools.DisplayImage.annotate_text" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
annotate_text(cls, text, splits, annotation_map=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L419)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L419?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.ImageTools.DisplayImage.postprocess" class="docs-object-method">&nbsp;</a> 
```python
postprocess(self, text): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/ImageTools/DisplayImage.py#L432)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/ImageTools/DisplayImage.py#L432?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.ImageTools.DisplayImage.text" class="docs-object-method">&nbsp;</a> 
```python
@property
text(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/ImageTools/DisplayImage.py#L448)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/ImageTools/DisplayImage.py#L448?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.ImageTools.DisplayImage.get_svg_script" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_svg_script(self, id): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L457)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L457?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.ImageTools.DisplayImage.get_png_from_svg_script" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_png_from_svg_script(self, id): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L471)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L471?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.ImageTools.DisplayImage.get_png_script" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_png_script(self, id): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L511)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L511?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.ImageTools.DisplayImage.to_widget" class="docs-object-method">&nbsp;</a> 
```python
to_widget(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/ImageTools/DisplayImage.py#L522)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/ImageTools/DisplayImage.py#L522?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.ImageTools.DisplayImage.show" class="docs-object-method">&nbsp;</a> 
```python
show(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/ImageTools/DisplayImage.py#L553)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/ImageTools/DisplayImage.py#L553?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.ImageTools.DisplayImage.save" class="docs-object-method">&nbsp;</a> 
```python
save(self, file): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/ImageTools/DisplayImage.py#L556)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/ImageTools/DisplayImage.py#L556?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/ImageTools/DisplayImage.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/ImageTools/DisplayImage.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/ImageTools/DisplayImage.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/ImageTools/DisplayImage.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/ImageTools.py#L15?message=Update%20Docs)   
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