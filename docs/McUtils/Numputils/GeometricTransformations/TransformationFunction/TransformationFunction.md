## <a id="McUtils.Numputils.GeometricTransformations.TransformationFunction.TransformationFunction">TransformationFunction</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/TransformationFunction.py#L13)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/TransformationFunction.py#L13?message=Update%20Docs)]
</div>

The TransformationFunction class is an abstract class
It provides the scaffolding for representing a single transformation operation







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Numputils.GeometricTransformations.TransformationFunction.TransformationFunction.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/TransformationFunction.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/TransformationFunction.py#L19?message=Update%20Docs)]
</div>
Initializes a transformation function based on the transfdata
  - `transfdata`: `Any`
    >


<a id="McUtils.Numputils.GeometricTransformations.TransformationFunction.TransformationFunction.inverse" class="docs-object-method">&nbsp;</a> 
```python
@property
inverse(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/TransformationFunction/TransformationFunction.py#L27)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/TransformationFunction/TransformationFunction.py#L27?message=Update%20Docs)]
</div>
Returns the inverse of the transformation
  - `:returns`: `_`
    >


<a id="McUtils.Numputils.GeometricTransformations.TransformationFunction.TransformationFunction.merge" class="docs-object-method">&nbsp;</a> 
```python
merge(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/TransformationFunction/TransformationFunction.py#L36)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/TransformationFunction/TransformationFunction.py#L36?message=Update%20Docs)]
</div>
Tries to merge with another TransformationFunction
  - `other`: `TransformationFunction`
    > a TransformationFunction to try to merge with
  - `:returns`: `TransformationFunction`
    > t
f
u
n
c


<a id="McUtils.Numputils.GeometricTransformations.TransformationFunction.TransformationFunction.operate" class="docs-object-method">&nbsp;</a> 
```python
operate(self, coords, shift=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/TransformationFunction/TransformationFunction.py#L47)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/TransformationFunction/TransformationFunction.py#L47?message=Update%20Docs)]
</div>
Operates on the coords. *Must* be able to deal with a list of coordinates, optimally in an efficient manner
  - `coords`: `np.ndarry`
    > the list of coordinates to apply the transformation to
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/GeometricTransformations/TransformationFunction/TransformationFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/GeometricTransformations/TransformationFunction/TransformationFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/GeometricTransformations/TransformationFunction/TransformationFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/GeometricTransformations/TransformationFunction/TransformationFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/TransformationFunction.py#L13?message=Update%20Docs)   
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