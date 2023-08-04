## <a id="McUtils.Zachary.Interpolator.Extrapolator">Extrapolator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator.py#L497)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator.py#L497?message=Update%20Docs)]
</div>

A general purpose that takes your data and just extrapolates it.
This currently only exists in template format.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Interpolator.Extrapolator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, extrapolation_function, warning=False, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator/Extrapolator.py#L502)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator/Extrapolator.py#L502?message=Update%20Docs)]
</div>

  - `extrapolation_function`: `None | function | Callable | Interpolator`
    > the function to handle extrapolation off the interpolation grid
  - `warning`: `bool`
    > whether to emit a message warning about extrapolation occurring
  - `opts`: `Any`
    > the options to feed into the extrapolator call


<a id="McUtils.Zachary.Interpolator.Extrapolator.derivative" class="docs-object-method">&nbsp;</a> 
```python
derivative(self, n): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator/Extrapolator.py#L519)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator/Extrapolator.py#L519?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Interpolator.Extrapolator.find_extrapolated_points" class="docs-object-method">&nbsp;</a> 
```python
find_extrapolated_points(self, gps, vals, extrap_value=nan): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator/Extrapolator.py#L525)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator/Extrapolator.py#L525?message=Update%20Docs)]
</div>
Currently super rough heuristics to determine at which points we need to extrapolate
  - `gps`: `Any`
    > 
  - `vals`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Zachary.Interpolator.Extrapolator.apply" class="docs-object-method">&nbsp;</a> 
```python
apply(self, gps, vals, extrap_value=nan): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator/Extrapolator.py#L546)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator/Extrapolator.py#L546?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Interpolator.Extrapolator.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, *args, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Interpolator/Extrapolator.py#L554)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator/Extrapolator.py#L554?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Interpolator/Extrapolator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Interpolator/Extrapolator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Interpolator/Extrapolator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Interpolator/Extrapolator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Interpolator.py#L497?message=Update%20Docs)   
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