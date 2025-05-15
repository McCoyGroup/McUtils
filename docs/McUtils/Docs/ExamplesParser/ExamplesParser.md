## <a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser">ExamplesParser</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser.py#L8)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser.py#L8?message=Update%20Docs)]
</div>

Provides a parser for unit tests to turn them into examples







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
IGNORE_UNHANDLED_STATEMENTS: bool
```
<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, unit_tests): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L13)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L13?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.find_setup" class="docs-object-method">&nbsp;</a> 
```python
find_setup(self, tree_iter): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L22)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L22?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.parse_tests" class="docs-object-method">&nbsp;</a> 
```python
parse_tests(self, tree_iter): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L34)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L34?message=Update%20Docs)]
</div>
Parses out the
  - `tree_iter`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.walk_tree" class="docs-object-method">&nbsp;</a> 
```python
walk_tree(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L62)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L62?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.format_node" class="docs-object-method">&nbsp;</a> 
```python
format_node(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L76)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L76?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.from_file" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_file(cls, tests_file): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L86)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L86?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.class_spec" class="docs-object-method">&nbsp;</a> 
```python
@property
class_spec(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L91)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L91?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.setup" class="docs-object-method">&nbsp;</a> 
```python
@property
setup(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L96)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L96?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.functions" class="docs-object-method">&nbsp;</a> 
```python
@property
functions(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L101)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L101?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.functions_map" class="docs-object-method">&nbsp;</a> 
```python
@property
functions_map(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L106)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L106?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.load_function_map" class="docs-object-method">&nbsp;</a> 
```python
load_function_map(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L112)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L112?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.get_examples_functions" class="docs-object-method">&nbsp;</a> 
```python
get_examples_functions(self, node): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L185)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L185?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Docs.ExamplesParser.ExamplesParser.filter_by_name" class="docs-object-method">&nbsp;</a> 
```python
filter_by_name(self, name): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L194)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser/ExamplesParser.py#L194?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Docs/ExamplesParser/ExamplesParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Docs/ExamplesParser/ExamplesParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Docs/ExamplesParser/ExamplesParser.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Docs/ExamplesParser/ExamplesParser.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Docs/ExamplesParser.py#L8?message=Update%20Docs)   
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