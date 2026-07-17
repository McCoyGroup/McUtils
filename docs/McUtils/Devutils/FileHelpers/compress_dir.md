# <a id="McUtils.Devutils.FileHelpers.compress_dir">compress_dir</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers.py#L461)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L461?message=Update%20Docs)]
</div>

```python
compress_dir(config_dir, cache_dir=None, name=None, files=None): 
```
**LLM Docstring**

Create a gzipped tar archive of (some of) a directory's files.
  - `config_dir`: `str`
    > the directory to archive
  - `cache_dir`: `str | None`
    > where to write the archive (defaults to the parent directory)
  - `name`: `str | None`
    > the archive base name (defaults to the directory name)
  - `files`: `Iterable[str] | None`
    > the file names to include (defaults to all)
  - `:returns`: `str`
    > the archive path











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/FileHelpers/compress_dir.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/FileHelpers/compress_dir.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/FileHelpers/compress_dir.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/FileHelpers/compress_dir.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L461?message=Update%20Docs)   
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