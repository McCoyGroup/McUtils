## <a id="McUtils.Devutils.Redirects.DefaultDirectory">DefaultDirectory</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects.py#L298)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects.py#L298?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Devutils.Redirects.DefaultDirectory.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, output_dir=None, chdir=True, **tempdir_opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects.py#L299)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects.py#L299?message=Update%20Docs)]
</div>
**LLM Docstring**

Context manager providing a working directory (a given one, or a fresh temporary
one), optionally `chdir`-ing into it.
  - `output_dir`: `str | None`
    > the directory to use (a temp dir is created if omitted)
  - `chdir`: `bool`
    > change into the directory on enter
  - `tempdir_opts`: `Any`
    > options for the temporary-directory creation


<a id="McUtils.Devutils.Redirects.DefaultDirectory.get_temp_dir" class="docs-object-method">&nbsp;</a> 
```python
get_temp_dir(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/DefaultDirectory.py#L318)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/DefaultDirectory.py#L318?message=Update%20Docs)]
</div>
**LLM Docstring**

Create a `TemporaryDirectory` using the stored options.
  - `:returns`: `_`
    > the temporary directory


<a id="McUtils.Devutils.Redirects.DefaultDirectory.dirname" class="docs-object-method">&nbsp;</a> 
```python
@property
dirname(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/DefaultDirectory.py#L328)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/DefaultDirectory.py#L328?message=Update%20Docs)]
</div>
**LLM Docstring**

The path of the managed directory (or `None` before entering).
  - `:returns`: `str | None`
    > the directory path


<a id="McUtils.Devutils.Redirects.DefaultDirectory.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/DefaultDirectory.py#L345)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/DefaultDirectory.py#L345?message=Update%20Docs)]
</div>
**LLM Docstring**

Establish the directory (creating a temp dir if needed) and optionally `chdir`
into it, returning its path.
  - `:returns`: `str`
    > the directory path


<a id="McUtils.Devutils.Redirects.DefaultDirectory.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/Redirects/DefaultDirectory.py#L366)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects/DefaultDirectory.py#L366?message=Update%20Docs)]
</div>
**LLM Docstring**

Restore the previous working directory and clean up the temporary directory if
one was created.
  - `exc_type`: `Any`
    > the exception type, if any
  - `exc_val`: `Any`
    > the exception value, if any
  - `exc_tb`: `Any`
    > the traceback, if any
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/Redirects/DefaultDirectory.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/Redirects/DefaultDirectory.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/Redirects/DefaultDirectory.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/Redirects/DefaultDirectory.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/Redirects.py#L298?message=Update%20Docs)   
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