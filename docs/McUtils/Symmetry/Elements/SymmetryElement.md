## <a id="McUtils.Symmetry.Elements.SymmetryElement">SymmetryElement</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements.py#L14?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Symmetry.Elements.SymmetryElement.get_transformation" class="docs-object-method">&nbsp;</a> 
```python
get_transformation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/SymmetryElement.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/SymmetryElement.py#L15?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the `3 x 3` Cartesian matrix implementing this symmetry operation.
  - `:returns`: `np.ndarray`
    > The Cartesian transformation matrix.


<a id="McUtils.Symmetry.Elements.SymmetryElement.inverse" class="docs-object-method">&nbsp;</a> 
```python
inverse(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/SymmetryElement.py#L26)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/SymmetryElement.py#L26?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the symmetry element whose transformation reverses this operation.
  - `:returns`: `SymmetryElement`
    > The inverse symmetry element.


<a id="McUtils.Symmetry.Elements.SymmetryElement.__eq__" class="docs-object-method">&nbsp;</a> 
```python
__eq__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/SymmetryElement.py#L37)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/SymmetryElement.py#L37?message=Update%20Docs)]
</div>
**LLM Docstring**

Compare two elements by numerical equality of their transformation matrices.
  - `other`: `object`
    > The symmetry element to compare or compose with this element.
  - `:returns`: `bool`
    > Whether the transformations are numerically equal.


<a id="McUtils.Symmetry.Elements.SymmetryElement.compose" class="docs-object-method">&nbsp;</a> 
```python
compose(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/SymmetryElement.py#L49)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/SymmetryElement.py#L49?message=Update%20Docs)]
</div>
**LLM Docstring**

Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.
  - `other`: `object`
    > The symmetry element to compare or compose with this element.
  - `:returns`: `SymmetryElement`
    > The simplified or generic composed symmetry element.


<a id="McUtils.Symmetry.Elements.SymmetryElement.__matmul__" class="docs-object-method">&nbsp;</a> 
```python
__matmul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/SymmetryElement.py#L62)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/SymmetryElement.py#L62?message=Update%20Docs)]
</div>
**LLM Docstring**

Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.
  - `other`: `object`
    > The symmetry element to compare or compose with this element.
  - `:returns`: `SymmetryElement`
    > The simplified or generic composed symmetry element.


<a id="McUtils.Symmetry.Elements.SymmetryElement.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/SymmetryElement.py#L75)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/SymmetryElement.py#L75?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a diagnostic string describing the symmetry element.
  - `:returns`: `str`
    > The representation string.


<a id="McUtils.Symmetry.Elements.SymmetryElement.from_transformation_matrix" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_transformation_matrix(cls, x, max_rotation_order=60): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L87)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L87?message=Update%20Docs)]
</div>
**LLM Docstring**

Classify a Cartesian matrix and instantiate the corresponding identity, inversion, rotation, reflection, or improper-rotation element.
  - `x`: `object`
    > Value used as `x` by the implementation.
  - `max_rotation_order`: `object`
    > Maximum rotation order considered while classifying a matrix. Defaults to `60`.
  - `:returns`: `SymmetryElement`
    > The classified symmetry element.


<a id="McUtils.Symmetry.Elements.SymmetryElement.transform" class="docs-object-method">&nbsp;</a> 
```python
transform(self, tf): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/SymmetryElement.py#L116)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/SymmetryElement.py#L116?message=Update%20Docs)]
</div>
**LLM Docstring**

Express the symmetry element in a transformed Cartesian basis.
  - `tf`: `object`
    > A `3 x 3` change-of-basis transformation.
  - `:returns`: `SymmetryElement`
    > A symmetry element with its defining axis transformed by `tf`.


<a id="McUtils.Symmetry.Elements.SymmetryElement.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, figure, **graphics_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/SymmetryElement.py#L130)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/SymmetryElement.py#L130?message=Update%20Docs)]
</div>
**LLM Docstring**

Add graphical primitives representing this symmetry element to a figure.
  - `figure`: `object`
    > Plotting figure that receives generated graphics primitives.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry/Elements/SymmetryElement.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry/Elements/SymmetryElement.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry/Elements/SymmetryElement.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry/Elements/SymmetryElement.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements.py#L14?message=Update%20Docs)   
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