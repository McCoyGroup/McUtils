## <a id="McUtils.Numputils.GeometricTransformations.GeometricTransformation.GeometricTransformation">GeometricTransformation</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/GeometricTransformations/GeometricTransformation.py#L25)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/GeometricTransformations/GeometricTransformation.py#L25?message=Update%20Docs)]
</div>

The GeometricTransformation class provides a simple, general way to represent a
compound coordinate transformation.
In general, it's basically just a wrapper chaining together a number of TransformationFunctions.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Numputils.GeometricTransformations.GeometricTransformation.GeometricTransformation.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *transforms): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L32)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L32?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.GeometricTransformations.GeometricTransformation.GeometricTransformation.is_affine" class="docs-object-method">&nbsp;</a> 
```python
@property
is_affine(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L39)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L39?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.GeometricTransformations.GeometricTransformation.GeometricTransformation.transformation_function" class="docs-object-method">&nbsp;</a> 
```python
@property
transformation_function(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L42)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L42?message=Update%20Docs)]
</div>

  - `:returns`: `TransformationFunction`
    >


<a id="McUtils.Numputils.GeometricTransformations.GeometricTransformation.GeometricTransformation.transforms" class="docs-object-method">&nbsp;</a> 
```python
@property
transforms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L50)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L50?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.GeometricTransformations.GeometricTransformation.GeometricTransformation.apply" class="docs-object-method">&nbsp;</a> 
```python
apply(self, coords, shift=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L54)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L54?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.GeometricTransformations.GeometricTransformation.GeometricTransformation.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, coords, shift=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L57)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L57?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.GeometricTransformations.GeometricTransformation.GeometricTransformation.condense_transforms" class="docs-object-method">&nbsp;</a> 
```python
condense_transforms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L63)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L63?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.GeometricTransformations.GeometricTransformation.GeometricTransformation.inverse" class="docs-object-method">&nbsp;</a> 
```python
@property
inverse(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L68)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.py#L68?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.GeometricTransformations.GeometricTransformation.GeometricTransformation.parse_transform" class="docs-object-method">&nbsp;</a> 
```python
@staticmethod
parse_transform(tf): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L72)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L72?message=Update%20Docs)]
</div>
Provides a way to "tag" a transformation
  - `tf`: `Any`
    > 
  - `:returns`: `_`
    >
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/GeometricTransformations/GeometricTransformation/GeometricTransformation.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/GeometricTransformations/GeometricTransformation.py#L25?message=Update%20Docs)   
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