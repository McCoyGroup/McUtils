## <a id="McUtils.Jupyter.NotebookTools.NotebookWriter">NotebookWriter</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/NotebookTools.py#L276)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/NotebookTools.py#L276?message=Update%20Docs)]
</div>

Converts a block of Markdown text into Jupyter notebook JSON (nbformat v4)
that can be written to disk and opened directly in Jupyter.

Fenced code blocks (e.g. ` ```python ... ``` `) whose language tag is in
`code_languages` become code cells; everything else (including fenced blocks
in other languages, like `bash` or `json`) stays inline in a markdown cell.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
code_fence_pattern: Pattern
default_code_languages: set
default_kernelspecs: dict
```
<a id="McUtils.Jupyter.NotebookTools.NotebookWriter.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, blocks, notebook_directory=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/NotebookTools.py#L295)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/NotebookTools.py#L295?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookWriter.from_markdown" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_markdown(cls, markdown, code_languages=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L299)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L299?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookWriter.make_cell" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
make_cell(cls, cell_type, source): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L321)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L321?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookWriter.to_json" class="docs-object-method">&nbsp;</a> 
```python
to_json(self, kernelspec=None, language='python', language_info=None, nbformat_minor=4): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/NotebookTools/NotebookWriter.py#L333)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/NotebookTools/NotebookWriter.py#L333?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookWriter.write" class="docs-object-method">&nbsp;</a> 
```python
write(self, file, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/NotebookTools/NotebookWriter.py#L351)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/NotebookTools/NotebookWriter.py#L351?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookWriter.get_default_notebook_directory" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_default_notebook_directory(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L356)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L356?message=Update%20Docs)]
</div>
Resolves the `TemporaryDirectory` shared by all `NotebookWriter` instances
that don't specify their own `notebook_directory`, creating it the first
time it's needed.


<a id="McUtils.Jupyter.NotebookTools.NotebookWriter.notebook_directory" class="docs-object-method">&nbsp;</a> 
```python
@property
notebook_directory(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/NotebookTools/NotebookWriter.py#L367)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/NotebookTools/NotebookWriter.py#L367?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.NotebookTools.NotebookWriter.open_temp" class="docs-object-method">&nbsp;</a> 
```python
open_temp(self, port, mode='lab', name=None, host='localhost', scheme='http', token=None, new=0, root_dir=None, notebook_directory=None, browser=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Jupyter/NotebookTools/NotebookWriter.py#L376)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/NotebookTools/NotebookWriter.py#L376?message=Update%20Docs)]
</div>
Writes this notebook into `self.notebook_directory` (a shared temp
directory by default) and opens it against an already-running Jupyter
server via `NotebookReader.open_notebook`.
  - `port`: `Any`
    > the port the running Jupyter server is listening on
  - `mode`: `Any`
    > `"notebook"` or `"lab"`
  - `name`: `Any`
    > file name (without or with `.ipynb`) to write to within
    `self.notebook_directory`; a unique name is generated if omitted
  - `host`: `Any`
    > the host the server is running on
  - `scheme`: `Any`
    > the URL scheme (`"http"`/`"https"`)
  - `token`: `Any`
    > an auth token to append to the URL, if the server requires one
  - `new`: `Any`
    > forwarded to `webbrowser.open`
  - `opts`: `Any`
    > forwarded to `write`/`to_json` (e.g. `kernelspec`, `language`, `language_info`)
  - `:returns`: `_`
    > the URL that was opened
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Jupyter/NotebookTools/NotebookWriter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Jupyter/NotebookTools/NotebookWriter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Jupyter/NotebookTools/NotebookWriter.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Jupyter/NotebookTools/NotebookWriter.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Jupyter/NotebookTools.py#L276?message=Update%20Docs)   
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