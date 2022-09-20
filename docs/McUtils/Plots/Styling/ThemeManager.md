## <a id="McUtils.Plots.Styling.ThemeManager">ThemeManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Styling.py#L100)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Styling.py#L100?message=Update%20Docs)]
</div>

Simple manager class for plugging into themes in a semi-background agnostic way







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
extra_themes: dict
```
<a id="McUtils.Plots.Styling.ThemeManager.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *theme_names, backend=<Backends.MPL: 'matplotlib'>, graphics_styles=None, **extra_styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Styling/ThemeManager.py#L120)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Styling/ThemeManager.py#L120?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Styling.ThemeManager.from_spec" class="docs-object-method">&nbsp;</a> 
```python
from_spec(theme): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Styling/ThemeManager.py#L126)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Styling/ThemeManager.py#L126?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Styling.ThemeManager.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Styling/ThemeManager.py#L149)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Styling/ThemeManager.py#L149?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Styling.ThemeManager.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Styling/ThemeManager.py#L160)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Styling/ThemeManager.py#L160?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Styling.ThemeManager.theme" class="docs-object-method">&nbsp;</a> 
```python
@property
theme(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Styling/ThemeManager.py#L164)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Styling/ThemeManager.py#L164?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Styling.ThemeManager.add_theme" class="docs-object-method">&nbsp;</a> 
```python
add_theme(theme_name, *base_theme, **extra_styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Styling/ThemeManager.py#L171)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Styling/ThemeManager.py#L171?message=Update%20Docs)]
</div>
Adds a theme to the extra themes dict. At some future date we'll
want to make it so that this does a level of validation, too.
  - `theme_name`: `Any`
    > 
  - `base_theme`: `Any`
    > 
  - `extra_styles`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Plots.Styling.ThemeManager.resolve_theme" class="docs-object-method">&nbsp;</a> 
```python
resolve_theme(theme_name, *base_themes, **extra_styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Styling/ThemeManager.py#L186)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Styling/ThemeManager.py#L186?message=Update%20Docs)]
</div>
Resolves a theme so that it only uses strings for built-in styles
  - `:returns`: `_`
    >


<a id="McUtils.Plots.Styling.ThemeManager.validate_theme" class="docs-object-method">&nbsp;</a> 
```python
validate_theme(self, theme_names, theme_styless): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Styling/ThemeManager.py#L232)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Styling/ThemeManager.py#L232?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Styling.ThemeManager.backend_themes" class="docs-object-method">&nbsp;</a> 
```python
@property
backend_themes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Styling/ThemeManager.py#L243)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Styling/ThemeManager.py#L243?message=Update%20Docs)]
</div>


<a id="McUtils.Plots.Styling.ThemeManager.theme_names" class="docs-object-method">&nbsp;</a> 
```python
@property
theme_names(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Plots/Styling/ThemeManager.py#L251)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Styling/ThemeManager.py#L251?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Styling/ThemeManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Styling/ThemeManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Styling/ThemeManager.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Styling/ThemeManager.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Plots/Styling.py#L100?message=Update%20Docs)   
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