## <a id="McUtils.Symmetry.Elements.ReflectionElement">ReflectionElement</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements.py#L565)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements.py#L565?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Symmetry.Elements.ReflectionElement.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, axis): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements.py#L566)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements.py#L566?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize the symmetry element, normalizing any supplied axis and reducing equivalent rotation roots when possible.
  - `axis`: `object`
    > Axis vector defining the symmetry operation.
  - `:returns`: `None`
    > No value is returned.


<a id="McUtils.Symmetry.Elements.ReflectionElement.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/ReflectionElement.py#L580)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/ReflectionElement.py#L580?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a diagnostic string describing the symmetry element.
  - `:returns`: `str`
    > The representation string.


<a id="McUtils.Symmetry.Elements.ReflectionElement.get_transformation" class="docs-object-method">&nbsp;</a> 
```python
get_transformation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/ReflectionElement.py#L592)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/ReflectionElement.py#L592?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the `3 x 3` Cartesian matrix implementing this symmetry operation.
  - `:returns`: `np.ndarray`
    > The Cartesian transformation matrix.


<a id="McUtils.Symmetry.Elements.ReflectionElement.inverse" class="docs-object-method">&nbsp;</a> 
```python
inverse(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/ReflectionElement.py#L603)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/ReflectionElement.py#L603?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the symmetry element whose transformation reverses this operation.
  - `:returns`: `SymmetryElement`
    > The inverse symmetry element.


<a id="McUtils.Symmetry.Elements.ReflectionElement.transform" class="docs-object-method">&nbsp;</a> 
```python
transform(self, tf): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/ReflectionElement.py#L613)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/ReflectionElement.py#L613?message=Update%20Docs)]
</div>
**LLM Docstring**

Express the symmetry element in a transformed Cartesian basis.
  - `tf`: `object`
    > A `3 x 3` change-of-basis transformation.
  - `:returns`: `SymmetryElement`
    > A symmetry element with its defining axis transformed by `tf`.


<a id="McUtils.Symmetry.Elements.ReflectionElement.compose" class="docs-object-method">&nbsp;</a> 
```python
compose(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/ReflectionElement.py#L626)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/ReflectionElement.py#L626?message=Update%20Docs)]
</div>
**LLM Docstring**

Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.
  - `other`: `object`
    > The symmetry element to compare or compose with this element.
  - `:returns`: `SymmetryElement`
    > The simplified or generic composed symmetry element.


<a id="McUtils.Symmetry.Elements.ReflectionElement.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, figure, *, origin=None, disk_type=None, color='black', radius=2, disk_transparency=0.8, **graphics_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/ReflectionElement.py#L658)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/ReflectionElement.py#L658?message=Update%20Docs)]
</div>
**LLM Docstring**

Add graphical primitives representing this symmetry element to a figure.
  - `figure`: `object`
    > Plotting figure that receives generated graphics primitives.
  - `origin`: `object`
    > Plot origin. Defaults to `None`.
  - `disk_type`: `object`
    > Value used as `disk_type` by the implementation. Defaults to `None`.
  - `color`: `object`
    > Value used as `color` by the implementation. Defaults to `'black'`.
  - `radius`: `object`
    > Value used as `radius` by the implementation. Defaults to `2`.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry/Elements/ReflectionElement.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry/Elements/ReflectionElement.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry/Elements/ReflectionElement.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry/Elements/ReflectionElement.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements.py#L565?message=Update%20Docs)   
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