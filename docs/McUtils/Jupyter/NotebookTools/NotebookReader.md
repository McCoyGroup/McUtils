## <a id="McUtils.Jupyter.NotebookTools.NotebookReader">NotebookReader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/NotebookTools.py#L11)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/NotebookTools.py#L11?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
NotebookCell: NotebookCell
CellList: CellList
```
<a id="McUtils.Jupyter.NotebookTools.NotebookReader.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, json_or_fp): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/NotebookTools/NotebookReader.py#L12)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/NotebookTools/NotebookReader.py#L12?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookReader.cell" class="docs-object-method">&nbsp;</a> 
```python
cell(self, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/NotebookTools/NotebookReader.py#L69)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/NotebookTools/NotebookReader.py#L69?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookReader.get_mime_image_loader" class="docs-object-method">&nbsp;</a> 
```python
get_mime_image_loader(self, img_type): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/NotebookTools/NotebookReader.py#L71)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/NotebookTools/NotebookReader.py#L71?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookReader.get_mime_type_loader" class="docs-object-method">&nbsp;</a> 
```python
get_mime_type_loader(self, mime_type): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/NotebookTools/NotebookReader.py#L75)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/NotebookTools/NotebookReader.py#L75?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookReader.cell_list" class="docs-object-method">&nbsp;</a> 
```python
cell_list(self, cells=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/NotebookTools/NotebookReader.py#L149)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/NotebookTools/NotebookReader.py#L149?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookReader.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/NotebookTools/NotebookReader.py#L156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/NotebookTools/NotebookReader.py#L156?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookReader.load_notebook" class="docs-object-method">&nbsp;</a> 
```python
load_notebook(self, nb_js): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/NotebookTools/NotebookReader.py#L160)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/NotebookTools/NotebookReader.py#L160?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookReader.get_notebook_name" class="docs-object-method">&nbsp;</a> 
```python
get_notebook_name(self, nb_js=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/NotebookTools/NotebookReader.py#L170)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/NotebookTools/NotebookReader.py#L170?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookReader.file_name" class="docs-object-method">&nbsp;</a> 
```python
@property
file_name(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/NotebookTools/NotebookReader.py#L182)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/NotebookTools/NotebookReader.py#L182?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookReader.nb_json" class="docs-object-method">&nbsp;</a> 
```python
@property
nb_json(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/NotebookTools/NotebookReader.py#L188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/NotebookTools/NotebookReader.py#L188?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookReader.get_notebook_files" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_notebook_files(cls, directory='.'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L195)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L195?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookReader.sort_by_evaluation_time" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
sort_by_evaluation_time(cls, file_list, directory='.'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L201)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L201?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookReader.active_notebook" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
active_notebook(cls, directory='.'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L207)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L207?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/NotebookTools/NotebookReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/NotebookTools/NotebookReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/NotebookTools/NotebookReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/NotebookTools/NotebookReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/NotebookTools.py#L11?message=Update%20Docs)   
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