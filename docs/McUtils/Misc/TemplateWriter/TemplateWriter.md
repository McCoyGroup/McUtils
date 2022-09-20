## <a id="McUtils.Misc.TemplateWriter.TemplateWriter">TemplateWriter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/TemplateWriter.py#L8)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateWriter.py#L8?message=Update%20Docs)]
</div>

A general class that can take a directory layout and apply template parameters to it
Very unsophisticated but workable







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
ignored_files: list
```
<a id="McUtils.Misc.TemplateWriter.TemplateWriter.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, template_dir, replacements=None, file_filter=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/TemplateWriter/TemplateWriter.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateWriter/TemplateWriter.py#L16?message=Update%20Docs)]
</div>


<a id="McUtils.Misc.TemplateWriter.TemplateWriter.replacements" class="docs-object-method">&nbsp;</a> 
```python
@property
replacements(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/TemplateWriter/TemplateWriter.py#L27)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateWriter/TemplateWriter.py#L27?message=Update%20Docs)]
</div>


<a id="McUtils.Misc.TemplateWriter.TemplateWriter.apply_replacements" class="docs-object-method">&nbsp;</a> 
```python
apply_replacements(self, string): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/TemplateWriter/TemplateWriter.py#L33)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateWriter/TemplateWriter.py#L33?message=Update%20Docs)]
</div>
Applies the defined replacements to the
  - `string`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Misc.TemplateWriter.TemplateWriter.write_file" class="docs-object-method">&nbsp;</a> 
```python
write_file(self, template_file, out_dir, apply_template=True, template_dir=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/TemplateWriter/TemplateWriter.py#L45)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateWriter/TemplateWriter.py#L45?message=Update%20Docs)]
</div>
writes a single _file_ to _dir_ and fills the template from the parameters passed when intializing the class
  - `template_file`: `str`
    > the file to load and write into
  - `out_dir`: `str`
    > the directory to write the file into
  - `apply_template`: `bool`
    > whether to apply the template parameters to the file content or not
  - `:returns`: `_`
    >


<a id="McUtils.Misc.TemplateWriter.TemplateWriter.iterate_write" class="docs-object-method">&nbsp;</a> 
```python
iterate_write(self, out_dir, apply_template=True, src_dir=None, template_dir=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Misc/TemplateWriter/TemplateWriter.py#L80)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateWriter/TemplateWriter.py#L80?message=Update%20Docs)]
</div>
Iterates through the files in the template_dir and writes them out to dir
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Misc/TemplateWriter/TemplateWriter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Misc/TemplateWriter/TemplateWriter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Misc/TemplateWriter/TemplateWriter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Misc/TemplateWriter/TemplateWriter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Misc/TemplateWriter.py#L8?message=Update%20Docs)   
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