## <a id="McUtils.Formatters.TeXWriter.TeXTranspiler">TeXTranspiler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter.py#L929)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter.py#L929?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
style_search_paths: list
```
<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, tex_root, root_dir=None, figure_renaming_function=None, bib_renaming_function=None, strip_comments=True, figures_path=None, figure_merge_function=None, bib_path=None, bib_merge_function=None, aliases=None, styles_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter.py#L930)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter.py#L930?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.figure_counter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
figure_counter(cls, name_root='Figure', start_at=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L956)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L956?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.add_bibs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
add_bibs(cls, bib_list): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L963)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L963?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.get_injection_body" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_injection_body(cls, root_dir, node_data: 'TeXImportGraph.ImportNode', body: 'str'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L970)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L970?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.apply_body_edit" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
apply_body_edit(cls, cur_text, edits, normalization_function=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L986)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L986?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.flatten_import_graph" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
flatten_import_graph(cls, graph: 'dict[str, dict[str, TeXImportGraph.ImportNode]]', root, cache=None, root_dir=None, strip_comments=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1011)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1011?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_block" class="docs-object-method">&nbsp;</a> 
```python
remap_block(self, flat_tex, call_head, file_parser, replacement_path=None, renaming_function=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1044)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1044?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_figures" class="docs-object-method">&nbsp;</a> 
```python
remap_figures(self, flat_tex, figures_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1121)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1121?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_bibliography" class="docs-object-method">&nbsp;</a> 
```python
remap_bibliography(self, flat_tex, bib_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1128?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_style_files" class="docs-object-method">&nbsp;</a> 
```python
remap_style_files(self, flat_tex, styles_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1136)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1136?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.create_flat_tex" class="docs-object-method">&nbsp;</a> 
```python
create_flat_tex(self, include_aux=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1152)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1152?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.transpile" class="docs-object-method">&nbsp;</a> 
```python
transpile(self, target_dir, file_name='main.tex', include_aux=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1226)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1226?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/TeXWriter/TeXTranspiler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/TeXWriter/TeXTranspiler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/TeXWriter/TeXTranspiler.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/TeXWriter/TeXTranspiler.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter.py#L929?message=Update%20Docs)   
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