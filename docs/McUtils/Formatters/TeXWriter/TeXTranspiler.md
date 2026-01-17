## <a id="McUtils.Formatters.TeXWriter.TeXTranspiler">TeXTranspiler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter.py#L933)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter.py#L933?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
LabelBlock: LabelBlock
ref_tag_map: dict
ref_label_formats: dict
si_ref_format: str
main_ref_format: str
si_doc_labels: tuple
style_search_paths: list
```
<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, tex_root, root_dir=None, figure_renaming_function=None, bib_renaming_function=None, strip_comments=True, figures_path=None, figure_merge_function=None, bib_path=None, bib_merge_function=None, aliases=None, styles_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter.py#L934)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter.py#L934?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.figure_counter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
figure_counter(cls, name_root='Figure', start_at=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L960)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L960?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.add_bibs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
add_bibs(cls, bib_list): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L967)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L967?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.get_injection_body" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_injection_body(cls, root_dir, node_data: 'TeXImportGraph.ImportNode', body: 'str'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L974)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L974?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.apply_body_edit" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
apply_body_edit(cls, cur_text, edits, normalization_function=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L990)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L990?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.flatten_import_graph" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
flatten_import_graph(cls, graph: 'dict[str, dict[str, TeXImportGraph.ImportNode]]', root, cache=None, root_dir=None, strip_comments=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1017)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1017?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_block" class="docs-object-method">&nbsp;</a> 
```python
remap_block(self, flat_tex, call_head, file_parser, replacement_path=None, renaming_function=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1050)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1050?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_figures" class="docs-object-method">&nbsp;</a> 
```python
remap_figures(self, flat_tex, figures_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1127)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1127?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_bibliography" class="docs-object-method">&nbsp;</a> 
```python
remap_bibliography(self, flat_tex, bib_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1134)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1134?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_style_files" class="docs-object-method">&nbsp;</a> 
```python
remap_style_files(self, flat_tex, styles_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1142)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1142?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.get_call_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_call_list(self, tex_stream, tags) -> 'dict[tuple[int, int], str]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1159)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1159?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.create_label_block_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create_label_block_map(cls, tex_stream, call_tags, block_parser): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1177)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1177?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.create_label_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create_label_map(cls, tex_stream): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1188)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1188?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.create_ref_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create_ref_map(cls, tex_stream): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1211)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1211?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.ref_remapping_label" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
ref_remapping_label(cls, head, label, si_index_map): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1234)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1234?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.figure_table_remapping" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
figure_table_remapping(cls, si_labels: 'dict[str, dict[tuple[int, int], LabelBlock]]', label_function=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1258)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1258?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_refs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
remap_refs(cls, tex_stream, ref_handler, ref_map=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1277)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1277?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.find_si_documents" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
find_si_documents(cls, flat_tex): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1285)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1285?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_si" class="docs-object-method">&nbsp;</a> 
```python
remap_si(self, flat_tex): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1293)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1293?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.create_flat_tex" class="docs-object-method">&nbsp;</a> 
```python
create_flat_tex(self, include_aux=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1314)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1314?message=Update%20Docs)]
</div>


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.transpile" class="docs-object-method">&nbsp;</a> 
```python
transpile(self, target_dir, file_name='main.tex', include_aux=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1391)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L1391?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter.py#L933?message=Update%20Docs)   
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