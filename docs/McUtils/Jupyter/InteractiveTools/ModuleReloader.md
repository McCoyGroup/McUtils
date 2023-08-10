## <a id="McUtils.Jupyter.InteractiveTools.ModuleReloader">ModuleReloader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/InteractiveTools.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/InteractiveTools.py#L14?message=Update%20Docs)]
</div>

Reloads a module & recursively descends its 'all' tree
to make sure that all submodules are also reloaded







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
blacklist_keys: list
```
<a id="McUtils.Jupyter.InteractiveTools.ModuleReloader.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, modspec): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/InteractiveTools/ModuleReloader.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/InteractiveTools/ModuleReloader.py#L20?message=Update%20Docs)]
</div>

  - `modspec`: `str | types.ModuleType`
    >


<a id="McUtils.Jupyter.InteractiveTools.ModuleReloader.get_parents" class="docs-object-method">&nbsp;</a> 
```python
get_parents(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/InteractiveTools/ModuleReloader.py#L29)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/InteractiveTools/ModuleReloader.py#L29?message=Update%20Docs)]
</div>
Returns module parents
  - `:returns`: `_`
    >


<a id="McUtils.Jupyter.InteractiveTools.ModuleReloader.get_members" class="docs-object-method">&nbsp;</a> 
```python
get_members(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/InteractiveTools/ModuleReloader.py#L38)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/InteractiveTools/ModuleReloader.py#L38?message=Update%20Docs)]
</div>
Returns module members
  - `:returns`: `_`
    >


<a id="McUtils.Jupyter.InteractiveTools.ModuleReloader.reload_member" class="docs-object-method">&nbsp;</a> 
```python
reload_member(self, member, stack=None, reloaded=None, blacklist=None, reload_parents=True, verbose=False, print_indent=''): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/InteractiveTools/ModuleReloader.py#L55)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/InteractiveTools/ModuleReloader.py#L55?message=Update%20Docs)]
</div>


<a id="McUtils.Jupyter.InteractiveTools.ModuleReloader.reload" class="docs-object-method">&nbsp;</a> 
```python
reload(self, stack=None, reloaded=None, blacklist=None, reload_parents=True, verbose=False, print_indent=''): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Jupyter/InteractiveTools/ModuleReloader.py#L108)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/InteractiveTools/ModuleReloader.py#L108?message=Update%20Docs)]
</div>
Recursively searches for modules to reload and then reloads them.
Uses a cache to break cyclic dependencies of any sort.
This turns out to also be a challenging problem, since we need to basically
load depth-first, while never jumping too far back...
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Jupyter/InteractiveTools/ModuleReloader.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Jupyter/InteractiveTools/ModuleReloader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Jupyter/InteractiveTools/ModuleReloader.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Jupyter/InteractiveTools/ModuleReloader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Jupyter/InteractiveTools.py#L14?message=Update%20Docs)   
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