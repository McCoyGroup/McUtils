## <a id="McUtils.Plots.Styling.Styled">Styled</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling.py#L16?message=Update%20Docs)]
</div>

Simple styling class







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Plots.Styling.Styled.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *str, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling.py#L20)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling.py#L20?message=Update%20Docs)]
</div>
**LLM Docstring**

Hold a value together with a dict of styling options.
  - `str`: `Any`
    > the value(s) (optionally a `(value, opts_dict)` pair)
  - `opts`: `Any`
    > styling options


<a id="McUtils.Plots.Styling.Styled.could_be" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
could_be(cls, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L34)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L34?message=Update%20Docs)]
</div>
**LLM Docstring**

Test whether a piece of data is a `(value, opts_dict)` pair that could be a
`Styled`.
  - `data`: `Any`
    > the data to test
  - `:returns`: `bool`
    > whether it looks like a styled value


<a id="McUtils.Plots.Styling.Styled.construct" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
construct(cls, data): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L47)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L47?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a `Styled` from a `(value, opts_dict)` pair.
  - `data`: `Any`
    > the `(value, opts_dict)` pair
  - `:returns`: `Styled`
    > the styled value


<a id="McUtils.Plots.Styling.Styled.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Styling/Styled.py#L59)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling/Styled.py#L59?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a representation showing the value and options.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Styling/Styled.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Styling/Styled.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Styling/Styled.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Styling/Styled.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Styling.py#L16?message=Update%20Docs)   
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