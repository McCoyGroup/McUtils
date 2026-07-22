## <a id="McUtils.Symmetry.Elements.RotationElement">RotationElement</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements.py#L368)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements.py#L368?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Symmetry.Elements.RotationElement.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, order, axis, root=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements.py#L369)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements.py#L369?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize the symmetry element, normalizing any supplied axis and reducing equivalent rotation roots when possible.
  - `order`: `object`
    > Order of the rotation or improper rotation.
  - `axis`: `object`
    > Axis vector defining the symmetry operation.
  - `root`: `object`
    > Integer power of the primitive rotation. Defaults to `1`.
  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.Symmetry.Elements.RotationElement.inverse" class="docs-object-method">&nbsp;</a> 
```python
inverse(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/RotationElement.py#L392)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/RotationElement.py#L392?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the symmetry element whose transformation reverses this operation.
  - `:returns`: `SymmetryElement`
    > The inverse symmetry element.


<a id="McUtils.Symmetry.Elements.RotationElement.transform" class="docs-object-method">&nbsp;</a> 
```python
transform(self, tf): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/RotationElement.py#L402)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/RotationElement.py#L402?message=Update%20Docs)]
</div>
**LLM Docstring**

Express the symmetry element in a transformed Cartesian basis.
  - `tf`: `object`
    > A `3 x 3` change-of-basis transformation.
  - `:returns`: `SymmetryElement`
    > A symmetry element with its defining axis transformed by `tf`.


<a id="McUtils.Symmetry.Elements.RotationElement.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/RotationElement.py#L415)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/RotationElement.py#L415?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a diagnostic string describing the symmetry element.
  - `:returns`: `str`
    > The representation string.


<a id="McUtils.Symmetry.Elements.RotationElement.compose" class="docs-object-method">&nbsp;</a> 
```python
compose(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/RotationElement.py#L427)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/RotationElement.py#L427?message=Update%20Docs)]
</div>
**LLM Docstring**

Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.
  - `other`: `object`
    > The symmetry element to compare or compose with this element.
  - `:returns`: `SymmetryElement`
    > The simplified or generic composed symmetry element.


<a id="McUtils.Symmetry.Elements.RotationElement.get_transformation" class="docs-object-method">&nbsp;</a> 
```python
get_transformation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/RotationElement.py#L470)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/RotationElement.py#L470?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the `3 x 3` Cartesian matrix implementing this symmetry operation.
  - `:returns`: `np.ndarray`
    > The Cartesian transformation matrix.


<a id="McUtils.Symmetry.Elements.RotationElement.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, figure, *, origin=None, line_type=None, disk_type=None, color='black', radius=2, spoke_radius=0.3, disk_color='black', disk_transparency=0.8, **graphics_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/RotationElement.py#L481)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/RotationElement.py#L481?message=Update%20Docs)]
</div>
**LLM Docstring**

Add graphical primitives representing this symmetry element to a figure.
  - `figure`: `object`
    > Plotting figure that receives generated graphics primitives.
  - `origin`: `object`
    > Plot origin. Defaults to `None`.
  - `line_type`: `object`
    > Value used as `line_type` by the implementation. Defaults to `None`.
  - `disk_type`: `object`
    > Value used as `disk_type` by the implementation. Defaults to `None`.
  - `color`: `object`
    > Value used as `color` by the implementation. Defaults to `'black'`.
  - `radius`: `object`
    > Value used as `radius` by the implementation. Defaults to `2`.
  - `spoke_radius`: `object`
    > Value used as `spoke_radius` by the implementation. Defaults to `0.3`.
  - `disk_color`: `object`
    > Value used as `disk_color` by the implementation. Defaults to `'black'`.
  - `disk_transparency`: `object`
    > Value used as `disk_transparency` by the implementation. Defaults to `0.8`.
  - `graphics_options`: `dict`
    > Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
  - `:returns`: `object`
    > The plotted primitive or list of plotted primitives.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry/Elements/RotationElement.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry/Elements/RotationElement.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry/Elements/RotationElement.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry/Elements/RotationElement.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements.py#L368?message=Update%20Docs)   
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