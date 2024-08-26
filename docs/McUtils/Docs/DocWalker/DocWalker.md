## <a id="McUtils.Docs.DocWalker.DocWalker">DocWalker</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Docs/DocWalker.py#L961)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Docs/DocWalker.py#L961?message=Update%20Docs)]
</div>

A class that walks a module structure, generating `.md` files for every class inside it as well as for global functions,
and a Markdown index file.

Takes a set of objects & writers and walks through the objects, generating files on the way.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
module_handler: ModuleWriter
class_handler: ClassWriter
function_handler: FunctionWriter
method_handler: MethodWriter
object_handler: ObjectWriter
index_handler: IndexWriter
spec: DocSpec
```
<a id="McUtils.Docs.DocWalker.DocWalker.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, out=None, engine=None, verbose=True, template_locator=None, examples_directory=None, tests_directory=None, **extra_fields): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Docs/DocWalker/DocWalker.py#L979)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Docs/DocWalker/DocWalker.py#L979?message=Update%20Docs)]
</div>

  - `objects`: `Iterable[Any]`
    > the objects to write out
  - `out`: `None | str`
    > the directory in which to write the files (`None` means `sys.stdout`)
  - `ignore_paths`: `None | Iterable[str]`
    > a set of paths not to write (passed to the objects)


<a id="McUtils.Docs.DocWalker.DocWalker.get_engine" class="docs-object-method">&nbsp;</a> 
```python
get_engine(self, locator): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Docs/DocWalker/DocWalker.py#L1005)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Docs/DocWalker/DocWalker.py#L1005?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.DocWalker.DocWalker.get_examples_loader" class="docs-object-method">&nbsp;</a> 
```python
get_examples_loader(self, examples_directory): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Docs/DocWalker/DocWalker.py#L1011)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Docs/DocWalker/DocWalker.py#L1011?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.DocWalker.DocWalker.get_tests_loader" class="docs-object-method">&nbsp;</a> 
```python
get_tests_loader(self, tests_directory): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Docs/DocWalker/DocWalker.py#L1016)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Docs/DocWalker/DocWalker.py#L1016?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.DocWalker.DocWalker.get_handler" class="docs-object-method">&nbsp;</a> 
```python
get_handler(self, *args, examples_loader=None, tests_loader=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Docs/DocWalker/DocWalker.py#L1021)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Docs/DocWalker/DocWalker.py#L1021?message=Update%20Docs)]
</div>


<a id="McUtils.Docs.DocWalker.DocWalker.visit_root" class="docs-object-method">&nbsp;</a> 
```python
visit_root(self, o, tests_directory=None, examples_directory=None, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Docs/DocWalker/DocWalker.py#L1029)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Docs/DocWalker/DocWalker.py#L1029?message=Update%20Docs)]
</div>
 </div>
</div>



<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#Details-03acfa" markdown="1"> Details</a> <a class="float-right" data-toggle="collapse" href="#Details-03acfa"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="Details-03acfa" markdown="1">
 A `DocWalker` object is a light subclass of a `TemplateWalker`, but specialized for documentation & with specialized handlers
 </div>
</div>








## See Also
[`DocBuilder`](../DocsBuilder/DocBuilder.md)<span>&nbsp;&#9642;&nbsp;</span>[`ModuleWriter`](ModuleWriter.md)<span>&nbsp;&#9642;&nbsp;</span>[`ClassWriter`](ClassWriter.md)<span>&nbsp;&#9642;&nbsp;</span>[`FunctionWriter`](FunctionWriter.md)<span>&nbsp;&#9642;&nbsp;</span>[`MethodWriter`](MethodWriter.md)<span>&nbsp;&#9642;&nbsp;</span>[`ObjectWriter`](ObjectWriter.md)<span>&nbsp;&#9642;&nbsp;</span>[`IndexWriter`](IndexWriter.md)

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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Docs/DocWalker/DocWalker.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Docs/DocWalker/DocWalker.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Docs/DocWalker/DocWalker.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Docs/DocWalker/DocWalker.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Docs/DocWalker.py#L961?message=Update%20Docs)   
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