## <a id="McUtils.McUtils.Numputils.GeometricTransformations.AffineTransform.AffineTransform">AffineTransform</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/AffineTransform.py#L17)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/AffineTransform.py#L17?message=Update%20Docs)]
</div>

A simple AffineTranform implementation of the TransformationFunction abstract base class







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.McUtils.Numputils.GeometricTransformations.AffineTransform.AffineTransform.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, tmat, shift=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L23)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L23?message=Update%20Docs)]
</div>
tmat must be a transformation matrix to work properly
  - `shift`: `np.ndarray | None`
    > the shift for the transformation
  - `tmat`: `np.ndarray`
    > the matrix for the linear transformation


<a id="McUtils.McUtils.Numputils.GeometricTransformations.AffineTransform.AffineTransform.transform" class="docs-object-method">&nbsp;</a> 
```python
@property
transform(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L35)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L35?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Numputils.GeometricTransformations.AffineTransform.AffineTransform.inverse" class="docs-object-method">&nbsp;</a> 
```python
@property
inverse(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L39)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L39?message=Update%20Docs)]
</div>
Returns the inverse of the transformation
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Numputils.GeometricTransformations.AffineTransform.AffineTransform.shift" class="docs-object-method">&nbsp;</a> 
```python
@property
shift(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L48)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L48?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Numputils.GeometricTransformations.AffineTransform.AffineTransform.merge" class="docs-object-method">&nbsp;</a> 
```python
merge(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L58)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L58?message=Update%20Docs)]
</div>

  - `other`: `np.ndarray or AffineTransform`
    >


<a id="McUtils.McUtils.Numputils.GeometricTransformations.AffineTransform.AffineTransform.reverse" class="docs-object-method">&nbsp;</a> 
```python
reverse(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L74)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L74?message=Update%20Docs)]
</div>
Inverts the matrix
  - `:returns`: `_`
    >


<a id="McUtils.McUtils.Numputils.GeometricTransformations.AffineTransform.AffineTransform.operate" class="docs-object-method">&nbsp;</a> 
```python
operate(self, coords, shift=True): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L85)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L85?message=Update%20Docs)]
</div>

  - `coords`: `np.ndarry`
    > the array of coordinates passed in


<a id="McUtils.McUtils.Numputils.GeometricTransformations.AffineTransform.AffineTransform.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L120)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.py#L120?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/GeometricTransformations/AffineTransform/AffineTransform.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/GeometricTransformations/AffineTransform.py#L17?message=Update%20Docs)   
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