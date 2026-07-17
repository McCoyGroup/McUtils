## <a id="McUtils.Zachary.Interpolator.CoordinateInterpolator">CoordinateInterpolator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Interpolator.py#L1037)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Interpolator.py#L1037?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Interpolator.py#L1041)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Interpolator.py#L1041?message=Update%20Docs)]
</div>
**LLM Docstring**

Interpolate a path of coordinates parametrized by (normalized) arc length,
delegating the actual interpolation to a base interpolator.
  - `coordinates`: `np.ndarray`
    > the path coordinates
  - `arc_lengths`: `np.ndarray | None`
    > explicit arc-length abcissae (computed if omitted)
  - `distance_function`: `Callable | str | None`
    > the inter-point distance function (or its name)
  - `base_interpolator`: `Any`
    > the interpolator type to use
  - `coordinate_system`: `Any`
    > the coordinate system to interpolate in
  - `interpolator_options`: `Any`
    > extra options for the base interpolator


<a id="McUtils.Zachary.Interpolator.CoordinateInterpolator.euclidean_coordinate_distance" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
euclidean_coordinate_distance(cls, p1, p2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1086)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1086?message=Update%20Docs)]
</div>
**LLM Docstring**

The Euclidean distance between two coordinate frames.
  - `p1`: `Any`
    > the first frame
  - `p2`: `Any`
    > the second frame
  - `:returns`: `float`
    > the distance


<a id="McUtils.Zachary.Interpolator.CoordinateInterpolator.lookup_distance_function" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lookup_distance_function(cls, distance_function): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1101)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1101?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a distance-function name to its implementation.
  - `distance_function`: `str`
    > the name (e.g. `'uniform'`)
  - `:returns`: `Callable`
    > the distance function


<a id="McUtils.Zachary.Interpolator.CoordinateInterpolator.uniform_distance_function" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
uniform_distance_function(cls, coords): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1117)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1117?message=Update%20Docs)]
</div>
**LLM Docstring**

Assign uniformly-spaced abcissae over `[0, 1]` regardless of the actual
inter-point distances.
  - `coords`: `np.ndarray`
    > the path coordinates
  - `:returns`: `np.ndarray`
    > the uniform abcissae


<a id="McUtils.Zachary.Interpolator.CoordinateInterpolator.get_arc_lengths" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_arc_lengths(cls, coordinates: numpy.ndarray, arc_lengths=None, distance_function: 'typing.Callable[[np.ndarray, np.ndarray], float]' = None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L1132)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L1132?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the normalized (`[0, 1]`) arc-length abcissae for a path, either from an
explicit array, a named scheme, or by accumulating a distance function along the
path.
  - `coordinates`: `np.ndarray`
    > the path coordinates
  - `arc_lengths`: `np.ndarray | None`
    > explicit arc lengths (computed if omitted)
  - `distance_function`: `Callable | str | None`
    > the inter-point distance function (or its name)
  - `:returns`: `tuple`
    > `(distance_function, normalized_arc_lengths)`


<a id="McUtils.Zachary.Interpolator.CoordinateInterpolator.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, points, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Interpolator/CoordinateInterpolator.py#L1169)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Interpolator/CoordinateInterpolator.py#L1169?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate the path at the given arc-length parameter(s).
  - `points`: `np.ndarray`
    > the arc-length parameter(s)
  - `etc`: `Any`
    > extra evaluation options
  - `:returns`: `np.ndarray`
    > the interpolated coordinates
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Interpolator.py#L1037?message=Update%20Docs)   
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