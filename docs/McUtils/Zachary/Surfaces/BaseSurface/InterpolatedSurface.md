## <a id="McUtils.Zachary.Surfaces.BaseSurface.InterpolatedSurface">InterpolatedSurface</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/BaseSurface.py#L306)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface.py#L306?message=Update%20Docs)]
</div>

A surface that operates by doing an interpolation of passed mesh data







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Surfaces.BaseSurface.InterpolatedSurface.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, xdata, ydata=None, dimension=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/BaseSurface.py#L310)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface.py#L310?message=Update%20Docs)]
</div>
**LLM Docstring**

Build a surface that evaluates by interpolating supplied mesh data.

When only `xdata` is given, its last column is taken as the values.
  - `xdata`: `np.ndarray`
    > the sample points (or points-plus-values)
  - `ydata`: `np.ndarray | None`
    > the sample values
  - `dimension`: `int | None`
    > the input dimensionality (inferred from `xdata`)
  - `opts`: `Any`
    > options forwarded to the interpolator


<a id="McUtils.Zachary.Surfaces.BaseSurface.InterpolatedSurface.evaluate" class="docs-object-method">&nbsp;</a> 
```python
evaluate(self, points, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/BaseSurface/InterpolatedSurface.py#L335)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface/InterpolatedSurface.py#L335?message=Update%20Docs)]
</div>
We delegate all the dirty work to the Interpolator so hopefully that's working...
  - `points`: `Any`
    > 
  - `kwargs`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Zachary.Surfaces.BaseSurface.InterpolatedSurface.minimize" class="docs-object-method">&nbsp;</a> 
```python
minimize(self, initial_guess=None, function_options=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/BaseSurface/InterpolatedSurface.py#L347)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface/InterpolatedSurface.py#L347?message=Update%20Docs)]
</div>
**LLM Docstring**

Minimize the interpolated surface, defaulting the starting point to the
lowest-valued sample.
  - `initial_guess`: `np.ndarray | None`
    > the starting point (defaults to the best sample)
  - `function_options`: `dict | None`
    > options forwarded to the surface evaluation
  - `opts`: `Any`
    > options forwarded to the optimizer
  - `:returns`: `np.ndarray`
    > the minimizing point
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Surfaces/BaseSurface/InterpolatedSurface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Surfaces/BaseSurface/InterpolatedSurface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Surfaces/BaseSurface/InterpolatedSurface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Surfaces/BaseSurface/InterpolatedSurface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/BaseSurface.py#L306?message=Update%20Docs)   
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