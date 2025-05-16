## <a id="McUtils.Scaffolding.CLIs.CLI">CLI</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs.py#L259)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs.py#L259?message=Update%20Docs)]
</div>

A representation of a command line interface
which layers simple command dispatching on the basic
ArgParse interface







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
extra_commands: dict
```
<a id="McUtils.Scaffolding.CLIs.CLI.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, name, description, *groups, cmd_name=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/CLI.py#L265)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/CLI.py#L265?message=Update%20Docs)]
</div>

  - `name`: `str`
    > 
  - `description`: `str`
    > 
  - `cmd_name`: `str | None`
    > 
  - `groups`: `Type[CommandGroup]`
    >


<a id="McUtils.Scaffolding.CLIs.CLI.parse_group_command" class="docs-object-method">&nbsp;</a> 
```python
parse_group_command(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/CLI.py#L284)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/CLI.py#L284?message=Update%20Docs)]
</div>
Parses a group and command argument (if possible) and prunes `sys.argv`
  - `group`: `Any`
    > 
  - `command`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.CLIs.CLI.get_command" class="docs-object-method">&nbsp;</a> 
```python
get_command(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/CLI.py#L305)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/CLI.py#L305?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.CLIs.CLI.get_group" class="docs-object-method">&nbsp;</a> 
```python
get_group(self, grp): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/CLI.py#L314)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/CLI.py#L314?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.CLIs.CLI.run_command" class="docs-object-method">&nbsp;</a> 
```python
run_command(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/CLI.py#L322)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/CLI.py#L322?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.CLIs.CLI.get_help" class="docs-object-method">&nbsp;</a> 
```python
get_help(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/CLI.py#L332)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/CLI.py#L332?message=Update%20Docs)]
</div>
Gets the help string for the CLI
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.CLIs.CLI.help" class="docs-object-method">&nbsp;</a> 
```python
help(self, print_help=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/CLI.py#L348)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/CLI.py#L348?message=Update%20Docs)]
</div>


<a id="McUtils.Scaffolding.CLIs.CLI.run_parse" class="docs-object-method">&nbsp;</a> 
```python
run_parse(self, parse, unknown): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/CLI.py#L355)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/CLI.py#L355?message=Update%20Docs)]
</div>
Provides a standard entry point to running stuff using the default CLI
  - `parse`: `Any`
    > 
  - `unknown`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.CLIs.CLI.parse_toplevel_args" class="docs-object-method">&nbsp;</a> 
```python
parse_toplevel_args(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/CLI.py#L425)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/CLI.py#L425?message=Update%20Docs)]
</div>
Parses out the top level flags that the program supports
  - `:returns`: `_`
    >


<a id="McUtils.Scaffolding.CLIs.CLI.run" class="docs-object-method">&nbsp;</a> 
```python
run(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Scaffolding/CLIs/CLI.py#L448)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs/CLI.py#L448?message=Update%20Docs)]
</div>
Parses the arguments in `sys.argv` and dispatches to the approriate action.
By default supports interactive sessions, running scripts, and abbreviated tracebacks.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/CLIs/CLI.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/CLIs/CLI.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/CLIs/CLI.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/CLIs/CLI.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Scaffolding/CLIs.py#L259?message=Update%20Docs)   
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