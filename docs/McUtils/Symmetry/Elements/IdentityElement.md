## <a id="McUtils.Symmetry.Elements.IdentityElement">IdentityElement</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements.py#L210)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements.py#L210?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Symmetry.Elements.IdentityElement.get_transformation" class="docs-object-method">&nbsp;</a> 
```python
get_transformation(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/IdentityElement.py#L211)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/IdentityElement.py#L211?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the `3 x 3` Cartesian matrix implementing this symmetry operation.
  - `:returns`: `np.ndarray`
    > The Cartesian transformation matrix.


<a id="McUtils.Symmetry.Elements.IdentityElement.compose" class="docs-object-method">&nbsp;</a> 
```python
compose(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/IdentityElement.py#L221)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/IdentityElement.py#L221?message=Update%20Docs)]
</div>
**LLM Docstring**

Compose this symmetry operation with another, using algebraic simplifications in concrete subclasses when available.
  - `other`: `object`
    > The symmetry element to compare or compose with this element.
  - `:returns`: `SymmetryElement`
    > The simplified or generic composed symmetry element.


<a id="McUtils.Symmetry.Elements.IdentityElement.inverse" class="docs-object-method">&nbsp;</a> 
```python
inverse(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/IdentityElement.py#L233)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/IdentityElement.py#L233?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the symmetry element whose transformation reverses this operation.
  - `:returns`: `SymmetryElement`
    > The inverse symmetry element.


<a id="McUtils.Symmetry.Elements.IdentityElement.transform" class="docs-object-method">&nbsp;</a> 
```python
transform(self, tf): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/IdentityElement.py#L243)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/IdentityElement.py#L243?message=Update%20Docs)]
</div>
**LLM Docstring**

Express the symmetry element in a transformed Cartesian basis.
  - `tf`: `object`
    > A `3 x 3` change-of-basis transformation.
  - `:returns`: `SymmetryElement`
    > A symmetry element with its defining axis transformed by `tf`.


<a id="McUtils.Symmetry.Elements.IdentityElement.plot" class="docs-object-method">&nbsp;</a> 
```python
plot(self, figure, **graphics_options): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Symmetry/Elements/IdentityElement.py#L256)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements/IdentityElement.py#L256?message=Update%20Docs)]
</div>
**LLM Docstring**

Identity elements have no graphical primitive; this stub intentionally performs no action.
  - `figure`: `object`
    > Plotting figure that receives generated graphics primitives.
  - `graphics_options`: `dict`
    > Additional keyword options forwarded to the selected constructor, generator, or plotting backend.
  - `:returns`: `None`
    > No value is returned.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Symmetry/Elements/IdentityElement.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Symmetry/Elements/IdentityElement.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Symmetry/Elements/IdentityElement.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Symmetry/Elements/IdentityElement.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Symmetry/Elements.py#L210?message=Update%20Docs)   
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