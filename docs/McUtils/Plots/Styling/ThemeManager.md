## <a id="McUtils.Plots.Styling.ThemeManager">ThemeManager</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling.py#L260)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling.py#L260?message=Update%20Docs)]
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
__init__(self, *theme_names, backend=None, graphics_styles=None, **extra_styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling.py#L285)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling.py#L285?message=Update%20Docs)]
</div>
**LLM Docstring**

Set up a theme manager that applies named themes (and extra styles) via a graphics
backend's theme context.
  - `theme_names`: `Any`
    > the base theme names
  - `backend`: `Any`
    > the graphics backend (defaults to matplotlib)
  - `graphics_styles`: `dict | None`
    > extra graphics-level styles
  - `extra_styles`: `Any`
    > extra theme properties


<a id="McUtils.Plots.Styling.ThemeManager.parse_theme_spec" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
parse_theme_spec(cls, theme): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L305)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L305?message=Update%20Docs)]
</div>
Normalizes a flexible theme specification (`None`, a name, a properties dict, or
a `(names, properties)` pair) into a `[theme_names, theme_properties]` pair.
  - `theme`: `Any`
    > the theme specification
  - `:returns`: `list`
    > the `[theme_names, theme_properties]` pair


<a id="McUtils.Plots.Styling.ThemeManager.from_spec" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_spec(cls, theme, backend=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L336)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L336?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a `ThemeManager` (or a `NoThemeManager` for `None`) from a flexible theme
specification (a name, a properties dict, or a `(names, properties)` pair).
  - `theme`: `Any`
    > the theme specification
  - `backend`: `Any`
    > the graphics backend
  - `:returns`: `ThemeManager | NoThemeManager`
    > the theme manager


<a id="McUtils.Plots.Styling.ThemeManager.merge_theme_spec" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
merge_theme_spec(cls, theme, **style_overrides): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L353)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L353?message=Update%20Docs)]
</div>
Layers style overrides (e.g. a `palette`, nested under `axes`) onto an existing
theme specification, preserving any base theme names and existing styles.
Handy for exposing a one-off style (like `palette=...`) as a keyword argument
without clobbering the rest of a caller's theme.
  - `theme`: `Any`
    > the base theme specification (`None`, a name, a dict, or a
    `(names, properties)` pair)
  - `style_overrides`: `Any`
    > style properties to deep-merge over the theme's properties
  - `:returns`: `list`
    > the merged `[theme_names, theme_properties]` spec


<a id="McUtils.Plots.Styling.ThemeManager.canonicalize_theme_props" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_theme_props(cls, props): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L381)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L381?message=Update%20Docs)]
</div>
Recursively normalizes theme properties, resolving anywhere a color list can be
given as a named `ColorPalette` instead of an explicit list.
Supports a `palette` shorthand key (expanded into `prop_cycle.color`) and a
`prop_cycle.color` entry given directly as a palette name.
  - `props`: `dict`
    > the theme properties
  - `:returns`: `dict`
    > the canonicalized properties


<a id="McUtils.Plots.Styling.ThemeManager.__enter__" class="docs-object-method">&nbsp;</a> 
```python
__enter__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling/ThemeManager.py#L412)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling/ThemeManager.py#L412?message=Update%20Docs)]
</div>
Enters the theme context: resolves the theme, validates its names against the
backend, canonicalizes its styles (resolving any named `ColorPalette` color
lists), and applies the result via the backend's theme context.
  - `:returns`: `_`
    > the entered theme context


<a id="McUtils.Plots.Styling.ThemeManager.__exit__" class="docs-object-method">&nbsp;</a> 
```python
__exit__(self, exc_type, exc_val, exc_tb): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling/ThemeManager.py#L429)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling/ThemeManager.py#L429?message=Update%20Docs)]
</div>
**LLM Docstring**

Exit the theme context, restoring the previous theme.
  - `exc_type`: `Any`
    > the exception type, if any
  - `exc_val`: `Any`
    > the exception value, if any
  - `exc_tb`: `Any`
    > the traceback, if any


<a id="McUtils.Plots.Styling.ThemeManager.theme" class="docs-object-method">&nbsp;</a> 
```python
@property
theme(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling/ThemeManager.py#L443)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling/ThemeManager.py#L443?message=Update%20Docs)]
</div>
**LLM Docstring**

The resolved theme (names and styles) for this manager.
  - `:returns`: `list`
    > the `[theme_names, styles]` theme


<a id="McUtils.Plots.Styling.ThemeManager.add_theme" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
add_theme(self, theme_name, *base_theme, **extra_styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L454)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L454?message=Update%20Docs)]
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
@classmethod
resolve_theme(self, theme_name, *base_themes, **extra_styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L470)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L470?message=Update%20Docs)]
</div>
Resolves a theme so that it only uses strings for built-in styles.
Composition is a deep merge (via `dev.merge_dicts`), so overriding a nested
style (e.g. `axes={'palette': ...}`) layers onto a base theme's other nested
styles (e.g. `axes.labelsize`) instead of replacing the whole section.
  - `:returns`: `_`
    >


<a id="McUtils.Plots.Styling.ThemeManager.validate_theme" class="docs-object-method">&nbsp;</a> 
```python
validate_theme(self, theme_names, theme_styless): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling/ThemeManager.py#L534)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling/ThemeManager.py#L534?message=Update%20Docs)]
</div>
**LLM Docstring**

Validate the theme names against the backend's supported themes, resolving each
name (or the first supported alternative in a group).
  - `theme_names`: `Any`
    > the theme names (or alternative groups)
  - `theme_styless`: `Any`
    > the theme styles (unused here)
  - `:returns`: `list`
    > the resolved theme names


<a id="McUtils.Plots.Styling.ThemeManager.backend_themes" class="docs-object-method">&nbsp;</a> 
```python
@property
backend_themes(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling/ThemeManager.py#L574)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling/ThemeManager.py#L574?message=Update%20Docs)]
</div>
**LLM Docstring**

The theme names supported by the backend.
  - `:returns`: `tuple`
    > the supported theme names


<a id="McUtils.Plots.Styling.ThemeManager.theme_names" class="docs-object-method">&nbsp;</a> 
```python
@property
theme_names(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling/ThemeManager.py#L586)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling/ThemeManager.py#L586?message=Update%20Docs)]
</div>
**LLM Docstring**

All available theme names (backend themes plus the registered extra themes).
  - `:returns`: `tuple`
    > the theme names
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling.py#L260?message=Update%20Docs)   
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