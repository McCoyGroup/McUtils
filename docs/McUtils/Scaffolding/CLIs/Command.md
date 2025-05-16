## <a id="McUtils.Scaffolding.CLIs.Command">Command</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs.py#L14?message=Update%20Docs)]
</div>

A holder for a command that just automates type handling &
that sort of thing







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Scaffolding.CLIs.Command.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name, method): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/Command.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/Command.py#L19?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.CLIs.Command.get_help" class="docs-object-method">&nbsp;</a> 
```python
get_help(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/Command.py#L28)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/Command.py#L28?message=Update%20Docs)]
</div>
Gets single method help string
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.CLIs.Command.get_parse_dict" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
get_parse_dict(*spec): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L91)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L91?message=Update%20Docs)]
</div>
Builds a parse spec to feed into an ArgumentParser later
  - `spec`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.CLIs.Command.get_parse_spec" class="docs-object-method">&nbsp;</a> 
```python
get_parse_spec(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/Command.py#L128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/Command.py#L128?message=Update%20Docs)]
</div>
Gets a parse spec that can be fed to ArgumentParser
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.CLIs.Command.parse" class="docs-object-method">&nbsp;</a> 
```python
parse(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/Command.py#L160)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/Command.py#L160?message=Update%20Docs)]
</div>
Generates a parse spec, builds an ArgumentParser, and parses the arguments
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.CLIs.Command.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/Command.py#L170)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/Command.py#L170?message=Update%20Docs)]
</div>
Parse argv and call bound method
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/CLIs/Command.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/CLIs/Command.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/CLIs/Command.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/CLIs/Command.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs.py#L14?message=Update%20Docs)   
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