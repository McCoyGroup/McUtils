## <a id="McUtils.Formatters.TeXWriter.TeXTranspiler">TeXTranspiler</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter.py#L1863)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter.py#L1863?message=Update%20Docs)]
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
__init__(self, tex_root, root_dir=None, figure_renaming_function=None, bib_renaming_function=None, strip_comments=True, figures_path=None, figure_merge_function=None, bib_path=None, bib_merge_function=None, bib_cleanup_function=None, citation_renaming_function=None, aliases=None, styles_path=None, parser_options=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter.py#L1864)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter.py#L1864?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize `TeXTranspiler` state from the supplied configuration.
  - `tex_root`: `object`
    > root TeX file
  - `root_dir`: `object`
    > directory used to resolve relative TeX imports
  - `figure_renaming_function`: `object`
    > value consumed as `figure_renaming_function` by the documented formatting path
  - `bib_renaming_function`: `object`
    > value consumed as `bib_renaming_function` by the documented formatting path
  - `strip_comments`: `object`
    > whether comments are removed before parsing
  - `figures_path`: `object`
    > value consumed as `figures_path` by the documented formatting path
  - `figure_merge_function`: `object`
    > value consumed as `figure_merge_function` by the documented formatting path
  - `bib_path`: `object`
    > value consumed as `bib_path` by the documented formatting path
  - `bib_merge_function`: `object`
    > value consumed as `bib_merge_function` by the documented formatting path
  - `bib_cleanup_function`: `object`
    > value consumed as `bib_cleanup_function` by the documented formatting path
  - `citation_renaming_function`: `object`
    > callable used to rename citation keys
  - `aliases`: `object`
    > path-variable substitutions
  - `styles_path`: `object`
    > value consumed as `styles_path` by the documented formatting path
  - `parser_options`: `object`
    > options forwarded to `TeXParser`
  - `:returns`: `None`
    > `None`; the operation mutates state, writes output, or raises by design.


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.figure_counter" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
figure_counter(cls, name_root='Figure', start_at=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1935)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1935?message=Update%20Docs)]
</div>
**LLM Docstring**

Create a stateful renamer that assigns sequential names while preserving each figure extension.
  - `name_root`: `object`
    > prefix for generated figure names
  - `start_at`: `object`
    > first numeric suffix to generate
  - `:returns`: `callable`
    > stateful figure-renaming callable


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.add_bibs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
add_bibs(cls, bib_list): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1954)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1954?message=Update%20Docs)]
</div>
**LLM Docstring**

Concatenate bibliography files into a persistent temporary file and mark it for later deletion.
  - `bib_list`: `object`
    > bibliography files to concatenate
  - `:returns`: `tuple[str, bool]`
    > temporary bibliography path and deletion flag


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.pruned_bib" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
pruned_bib(cls, bib_file_or_filter, cites=None, *, filter=None, **parser_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1976)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1976?message=Update%20Docs)]
</div>
**LLM Docstring**

Filter a BibTeX file in place to entries referenced by the supplied citation map, or return a configured filter closure.
  - `bib_file_or_filter`: `object`
    > bibliography filename or a citation-filter factory argument
  - `cites`: `object`
    > parsed citation map
  - `filter`: `object`
    > additional callable mask over retained index arrays
  - `parser_options`: `dict`
    > additional keyword options forwarded to the underlying formatter or operation
  - `:returns`: `callable | None`
    > configured pruning callable when invoked as a factory, otherwise `None`


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.get_injection_body" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_injection_body(cls, root_dir, node_data: 'TeXImportGraph.ImportNode', body: 'str'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2034)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2034?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve and return the requested derived value from the object’s current configuration.
  - `root_dir`: `object`
    > directory used to resolve relative TeX imports
  - `node_data`: `TeXImportGraph.ImportNode`
    > value consumed as `node_data` by the documented formatting path
  - `body`: `str`
    > content to format or wrap
  - `:returns`: `tuple`
    > source endpoints paired with normalized imported body


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.apply_body_edit" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
apply_body_edit(cls, cur_text, edits, normalization_function=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2064)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2064?message=Update%20Docs)]
</div>
**LLM Docstring**

Apply endpoint-based replacements in source order while accounting for text already consumed from the working buffer.
  - `cur_text`: `object`
    > source text to edit
  - `edits`: `object`
    > endpoint ranges paired with replacement bodies
  - `normalization_function`: `object`
    > callable converting edit records to endpoint/body pairs
  - `:returns`: `str`
    > source text with all replacements applied


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.flatten_import_graph" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
flatten_import_graph(cls, graph: 'dict[str, dict[str, TeXImportGraph.ImportNode]]', root, cache=None, root_dir=None, strip_comments=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2105?message=Update%20Docs)]
</div>
**LLM Docstring**

Recursively inline imported TeX files, memoizing results and inserting `None` sentinels to break cycles.
  - `graph`: `dict[str, dict[str, TeXImportGraph.ImportNode]]`
    > import adjacency mapping
  - `root`: `object`
    > current TeX file or resource root
  - `cache`: `object`
    > memoized flattened file bodies
  - `root_dir`: `object`
    > directory used to resolve relative TeX imports
  - `strip_comments`: `object`
    > whether comments are removed before parsing
  - `:returns`: `object`
    > flattened TeX source, optionally paired with auxiliary metadata


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_block" class="docs-object-method">&nbsp;</a> 
```python
remap_block(self, flat_tex, call_head, file_parser, replacement_path=None, renaming_function=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2156)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2156?message=Update%20Docs)]
</div>
**LLM Docstring**

Locate resource commands, extract filenames, optionally rename/repath them, and rewrite the command bodies.
  - `flat_tex`: `object`
    > flattened TeX source or path to it
  - `call_head`: `object`
    > TeX command head to locate
  - `file_parser`: `object`
    > callable extracting resource paths from command text
  - `replacement_path`: `object`
    > new resource directory prefix
  - `renaming_function`: `object`
    > callable mapping original resources to output names
  - `:returns`: `object`
    > rewritten TeX source and any associated mapping metadata


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_figures" class="docs-object-method">&nbsp;</a> 
```python
remap_figures(self, flat_tex, figures_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2287?message=Update%20Docs)]
</div>
**LLM Docstring**

Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.
  - `flat_tex`: `object`
    > flattened TeX source or path to it
  - `figures_path`: `object`
    > value consumed as `figures_path` by the documented formatting path
  - `:returns`: `object`
    > rewritten TeX source and any associated mapping metadata


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_bibliography" class="docs-object-method">&nbsp;</a> 
```python
remap_bibliography(self, flat_tex, bib_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2306)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2306?message=Update%20Docs)]
</div>
**LLM Docstring**

Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.
  - `flat_tex`: `object`
    > flattened TeX source or path to it
  - `bib_path`: `object`
    > value consumed as `bib_path` by the documented formatting path
  - `:returns`: `object`
    > rewritten TeX source and any associated mapping metadata


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_style_files" class="docs-object-method">&nbsp;</a> 
```python
remap_style_files(self, flat_tex, styles_path=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2326)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2326?message=Update%20Docs)]
</div>
**LLM Docstring**

Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.
  - `flat_tex`: `object`
    > flattened TeX source or path to it
  - `styles_path`: `object`
    > value consumed as `styles_path` by the documented formatting path
  - `:returns`: `object`
    > rewritten TeX source and any associated mapping metadata


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.get_call_list" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_call_list(self, tex_stream, tags) -> 'dict[tuple[int, int], str]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2355)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2355?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve and return the requested derived value from the object’s current configuration.
  - `tex_stream`: `object`
    > TeX source string, file, or stream
  - `tags`: `object`
    > command tags to scan
  - `:returns`: `dict`
    > source endpoint ranges mapped to raw TeX calls


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.create_label_block_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create_label_block_map(cls, tex_stream, call_tags, block_parser): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2395)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2395?message=Update%20Docs)]
</div>
**LLM Docstring**

Scan the TeX source for the requested command family and organize parsed blocks by type and source endpoints.
  - `tex_stream`: `object`
    > TeX source string, file, or stream
  - `call_tags`: `object`
    > command tags to scan
  - `block_parser`: `object`
    > callable decomposing a matched command
  - `:returns`: `dict`
    > parsed blocks organized by type and source endpoints


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.create_label_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create_label_map(cls, tex_stream): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2420)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2420?message=Update%20Docs)]
</div>
**LLM Docstring**

Scan the TeX source for the requested command family and organize parsed blocks by type and source endpoints.
  - `tex_stream`: `object`
    > TeX source string, file, or stream
  - `:returns`: `dict`
    > parsed blocks organized by type and source endpoints


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.create_ref_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create_ref_map(cls, tex_stream): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2463)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2463?message=Update%20Docs)]
</div>
**LLM Docstring**

Scan the TeX source for the requested command family and organize parsed blocks by type and source endpoints.
  - `tex_stream`: `object`
    > TeX source string, file, or stream
  - `:returns`: `dict`
    > parsed blocks organized by type and source endpoints


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.create_cite_map" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
create_cite_map(cls, tex_stream): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2499)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2499?message=Update%20Docs)]
</div>
**LLM Docstring**

Scan the TeX source for the requested command family and organize parsed blocks by type and source endpoints.
  - `tex_stream`: `object`
    > TeX source string, file, or stream
  - `:returns`: `dict`
    > parsed blocks organized by type and source endpoints


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_citation_set" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
remap_citation_set(cls, tex_stream, ref_handler, cite_map=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2514)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2514?message=Update%20Docs)]
</div>
**LLM Docstring**

Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.
  - `tex_stream`: `object`
    > TeX source string, file, or stream
  - `ref_handler`: `object`
    > callable producing endpoint-to-replacement edits
  - `cite_map`: `object`
    > precomputed citation map
  - `:returns`: `object`
    > rewritten TeX source and any associated mapping metadata


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_citations" class="docs-object-method">&nbsp;</a> 
```python
remap_citations(self, flat_tex, si_tex: 'dict[str, str]' = None, citation_renaming_function=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2553)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2553?message=Update%20Docs)]
</div>
**LLM Docstring**

Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.
  - `flat_tex`: `object`
    > flattened TeX source or path to it
  - `si_tex`: `dict[str, str]`
    > supplementary-document source mapping
  - `citation_renaming_function`: `object`
    > callable used to rename citation keys
  - `:returns`: `object`
    > rewritten TeX source and any associated mapping metadata


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.ref_remapping_label" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
ref_remapping_label(cls, head, label, si_index_map): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2595)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2595?message=Update%20Docs)]
</div>
**LLM Docstring**

Convert references to supplementary labels into explicit display text while leaving main-document references as TeX refs.
  - `head`: `object`
    > TeX command head
  - `label`: `object`
    > parsed reference label
  - `si_index_map`: `object`
    > mapping of supplementary labels to one-based display indices
  - `:returns`: `str | None`
    > replacement display text, or `None` when no supplementary reference is present


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.figure_table_remapping" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
figure_table_remapping(cls, si_labels: 'dict[str, dict[tuple[int, int], LabelBlock]]', label_function=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2633)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2633?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a closure that rewrites references using stable supplementary figure/table/equation indices.
  - `si_labels`: `dict[str, dict[tuple[int, int], LabelBlock]]`
    > labels extracted from supplementary documents
  - `label_function`: `object`
    > callable converting a reference block to replacement text
  - `:returns`: `callable`
    > reference-map handler closure


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_refs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
remap_refs(cls, tex_stream, ref_handler, ref_map=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2674)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2674?message=Update%20Docs)]
</div>
**LLM Docstring**

Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.
  - `tex_stream`: `object`
    > TeX source string, file, or stream
  - `ref_handler`: `object`
    > callable producing endpoint-to-replacement edits
  - `ref_map`: `object`
    > precomputed reference map
  - `:returns`: `object`
    > rewritten TeX source and any associated mapping metadata


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.find_si_documents" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
find_si_documents(cls, flat_tex): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2696)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2696?message=Update%20Docs)]
</div>
**LLM Docstring**

Find external supplementary-document commands and map document names to their source endpoint ranges.
  - `flat_tex`: `object`
    > flattened TeX source or path to it
  - `:returns`: `dict`
    > supplementary document names mapped to source endpoints


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.remap_si" class="docs-object-method">&nbsp;</a> 
```python
remap_si(self, flat_tex): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2714)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2714?message=Update%20Docs)]
</div>
**LLM Docstring**

Rewrite the corresponding TeX resource or reference commands and return the updated source together with mapping metadata where applicable.
  - `flat_tex`: `object`
    > flattened TeX source or path to it
  - `:returns`: `object`
    > rewritten TeX source and any associated mapping metadata


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.create_flat_tex" class="docs-object-method">&nbsp;</a> 
```python
create_flat_tex(self, include_aux=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2745)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2745?message=Update%20Docs)]
</div>
**LLM Docstring**

Flatten imports and optionally remap styles, figures, bibliography, supplementary documents, and citations into an auxiliary manifest.
  - `include_aux`: `object`
    > whether resource remapping metadata is returned
  - `:returns`: `object`
    > flattened TeX source, optionally paired with auxiliary metadata


<a id="McUtils.Formatters.TeXWriter.TeXTranspiler.transpile" class="docs-object-method">&nbsp;</a> 
```python
transpile(self, target_dir, file_name='main.tex', include_si=True, include_aux=True, allow_missing_styles=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2862)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter/TeXTranspiler.py#L2862?message=Update%20Docs)]
</div>
**LLM Docstring**

Flatten the document, copy remapped auxiliary resources and supplementary files, and write the final root TeX file.
  - `target_dir`: `object`
    > output directory for the transpiled document
  - `file_name`: `object`
    > name of the generated root TeX file
  - `include_si`: `object`
    > whether flattened supplementary documents are written
  - `include_aux`: `object`
    > whether resource remapping metadata is returned
  - `allow_missing_styles`: `object`
    > whether unavailable class/style files may be skipped
  - `:returns`: `str`
    > the output directory path
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/TeXWriter.py#L1863?message=Update%20Docs)   
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