# <a id="McUtils.Plots.Colors.prep_color">prep_color</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Colors.py#L1441)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors.py#L1441?message=Update%20Docs)]
</div>

```python
prep_color(base=None, palette=None, blending=None, index=None, lighten=None, saturate=None, modifier=None, shift=False, absolute=False, clip=True, color_space='rgb', modification_space='lab', return_color_code=True, alpha=None, cycle=None): 
```
**LLM Docstring**

Module-level shortcut for `ColorPalette.prep_color`: compose a color from a base
color or palette with optional blending/indexing and saturate/lighten/modify/alpha
transformations.
  - `base`: `Any`
    > an explicit base color
  - `palette`: `Any`
    > a palette to draw from
  - `blending`: `Any`
    > a blend amount
  - `index`: `Any`
    > a palette index
  - `lighten`: `Any`
    > a lighten amount
  - `saturate`: `Any`
    > a saturate amount
  - `modifier`: `Any`
    > a custom modification callback
  - `shift`: `bool`
    > apply modifications additively
  - `absolute`: `bool`
    > set rather than scale the modified channel
  - `clip`: `bool`
    > clip the result
  - `color_space`: `str`
    > the working color space
  - `modification_space`: `str`
    > the modification space
  - `return_color_code`: `bool`
    > return hex codes
  - `alpha`: `Any`
    > an alpha value
  - `cycle`: `Any`
    > cycle the palette when indexing
  - `:returns`: `_`
    > the composed color(s)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Colors/prep_color.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Colors/prep_color.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Colors/prep_color.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Colors/prep_color.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Colors.py#L1441?message=Update%20Docs)   
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