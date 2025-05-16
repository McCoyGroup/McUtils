## <a id="McUtils.Zachary.Interpolator.CoordinateInterpolator">CoordinateInterpolator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Interpolator.py#L808)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Interpolator.py#L808?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_interpolator_type: IncrementalCartesianCoordinateInterpolation
```
<a id="McUtils.Zachary.Interpolator.CoordinateInterpolator.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, coordinates, arc_lengths=None, distance_function=None, base_interpolator=None, coordinate_system=None, **interpolator_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Interpolator.py#L812)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Interpolator.py#L812?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Interpolator.CoordinateInterpolator.euclidean_coordinate_distance" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
euclidean_coordinate_distance(cls, p1, p2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L841)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L841?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Interpolator.CoordinateInterpolator.lookup_distance_function" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lookup_distance_function(cls, distance_function): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L846)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L846?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Interpolator.CoordinateInterpolator.uniform_distance_function" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
uniform_distance_function(cls, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L852)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L852?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Interpolator.CoordinateInterpolator.get_arc_lengths" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_arc_lengths(cls, coordinates: numpy.ndarray, arc_lengths=None, distance_function: 'typing.Callable[[np.ndarray, np.ndarray], float]' = None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L856)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L856?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Interpolator.CoordinateInterpolator.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, points, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Interpolator/CoordinateInterpolator.py#L877)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Interpolator/CoordinateInterpolator.py#L877?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Interpolator/CoordinateInterpolator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Interpolator/CoordinateInterpolator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Interpolator/CoordinateInterpolator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Interpolator/CoordinateInterpolator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Interpolator.py#L808?message=Update%20Docs)   
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