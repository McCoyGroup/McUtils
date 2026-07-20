## <a id="McUtils.Plots.Styling.PlotLegend">PlotLegend</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling.py#L71)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling.py#L71?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
known_styles: set
default_styles: dict
marker_synonyms: dict
```
<a id="McUtils.Plots.Styling.PlotLegend.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, components, **styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling.py#L80)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling.py#L80?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a legend (a list of handle components plus styling options), validating the
styles and filling in defaults.
  - `components`: `Any`
    > the legend handle components (or another `PlotLegend`)
  - `styles`: `Any`
    > legend styling options


<a id="McUtils.Plots.Styling.PlotLegend.check_styles" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
check_styles(cls, styles): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L99)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L99?message=Update%20Docs)]
</div>
**LLM Docstring**

Raise if any style keys aren't among the known legend styles.
  - `styles`: `dict`
    > the styles to check


<a id="McUtils.Plots.Styling.PlotLegend.could_be_legend" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
could_be_legend(cls, bits): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L113)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L113?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether a value could be legend components (an iterable that isn't a bare
scalar/string).
  - `bits`: `Any`
    > the value to test
  - `:returns`: `bool`
    > whether it could be a legend


<a id="McUtils.Plots.Styling.PlotLegend.construct" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct(cls, bits): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L132)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L132?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a `PlotLegend` from components (accepting an existing legend, a
`(components, opts)` pair, or a bare component list), canonicalizing dict-specified
handles.
  - `bits`: `Any`
    > the components (or `(components, opts)` pair)
  - `:returns`: `PlotLegend`
    > the legend


<a id="McUtils.Plots.Styling.PlotLegend.construct_line_marker" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct_line_marker(cls, lw=4, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L153)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L153?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a line legend handle (a matplotlib `Line2D`).
  - `lw`: `float`
    > the line width
  - `opts`: `Any`
    > extra line options
  - `:returns`: `_`
    > the legend handle


<a id="McUtils.Plots.Styling.PlotLegend.construct_dot_marker" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct_dot_marker(cls, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L167)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L167?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a dot/patch legend handle (a matplotlib `Patch`).
  - `opts`: `Any`
    > patch options
  - `:returns`: `_`
    > the legend handle


<a id="McUtils.Plots.Styling.PlotLegend.load_constructors" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_constructors(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L179)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L179?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the mapping of marker names to their legend-handle constructors.
  - `:returns`: `dict`
    > the constructor mapping


<a id="McUtils.Plots.Styling.PlotLegend.canonicalize_bit" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
canonicalize_bit(cls, marker='-', **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L194)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L194?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a single legend handle from a marker spec (resolving marker synonyms and
dispatching to the appropriate constructor).
  - `marker`: `Any`
    > the marker name/synonym (or a constructor callable)
  - `opts`: `Any`
    > handle options
  - `:returns`: `_`
    > the legend handle


<a id="McUtils.Plots.Styling.PlotLegend.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling/PlotLegend.py#L212)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling/PlotLegend.py#L212?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation showing the components and options.
  - `:returns`: `str`
    > the representation
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Styling/PlotLegend.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Styling/PlotLegend.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Styling/PlotLegend.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Styling/PlotLegend.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling.py#L71?message=Update%20Docs)   
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