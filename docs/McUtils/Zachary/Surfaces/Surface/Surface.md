## <a id="McUtils.Zachary.Surfaces.Surface.Surface">Surface</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/Surface.py#L10)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface.py#L10?message=Update%20Docs)]
</div>

This actually isn't a concrete implementation of BaseSurface.
Instead it's a class that _dispatches_ to an implementation of BaseSurface to do its core evaluations (plus it does shape checking)







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Surfaces.Surface.Surface.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, data, dimension=None, base=None, **metadata): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/Surface.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface.py#L15?message=Update%20Docs)]
</div>

  - `data`: `Any`
    > 
  - `dimension`: `Any`
    > 
  - `base`: `None | Type[BaseSurface]`
    > 
  - `metadata`: `Any`
    >


<a id="McUtils.Zachary.Surfaces.Surface.Surface.data" class="docs-object-method">&nbsp;</a> 
```python
@property
data(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/Surface/Surface.py#L39)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface/Surface.py#L39?message=Update%20Docs)]
</div>
**LLM Docstring**

The backing data of the dispatched base surface.
  - `:returns`: `_`
    > the surface data


<a id="McUtils.Zachary.Surfaces.Surface.Surface.minimize" class="docs-object-method">&nbsp;</a> 
```python
minimize(self, initial_guess=None, function_options=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/Surface/Surface.py#L50)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface/Surface.py#L50?message=Update%20Docs)]
</div>
Provides a uniform interface for minimization, basically just dispatching to the BaseSurface implementation if provided
  - `initial_guess`: `np.ndarray | None`
    > initial starting point for the minimization
  - `function_options`: `None | dict`
    > 
  - `opts`: `Any`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Zachary.Surfaces.Surface.Surface.detect_base" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
detect_base(cls, data, opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L70)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L70?message=Update%20Docs)]
</div>
Infers what type of base surface works for the data that's passed in.
It's _super_ roughly done so...yeah generally better to pass the base class you want explicitly.
But in the absence of that we can do this ?_?

Basic strategy:
    1. look for options that go with specific methods
    2. look at data structures to guess
        i.   gradient as the first data arg + all data args are ndarrays -> Taylor Series
        ii.  callables as second arg -> Linear expansion or Linear fit
        iii. just like...one big array -> Interpolatin
  - `data`: `tuple`
    > 
  - `opts`: `dict`
    > 
  - `:returns`: `_`
    >


<a id="McUtils.Zachary.Surfaces.Surface.Surface.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, gridpoints, **kwargs): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/Surface/Surface.py#L114)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface/Surface.py#L114?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate the surface at the given grid points (dispatching to the base surface).
  - `gridpoints`: `np.ndarray`
    > the points to evaluate at
  - `kwargs`: `Any`
    > extra evaluation options
  - `:returns`: `np.ndarray`
    > the surface values


<a id="McUtils.Zachary.Surfaces.Surface.Surface.center" class="docs-object-method">&nbsp;</a> 
```python
@property
center(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/Surface/Surface.py#L128)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface/Surface.py#L128?message=Update%20Docs)]
</div>
**LLM Docstring**

The expansion center of the base surface (if it has one).
  - `:returns`: `_`
    > the center


<a id="McUtils.Zachary.Surfaces.Surface.Surface.ref" class="docs-object-method">&nbsp;</a> 
```python
@property
ref(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/Surface/Surface.py#L138)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface/Surface.py#L138?message=Update%20Docs)]
</div>
**LLM Docstring**

The reference value of the base surface (if it has one).
  - `:returns`: `_`
    > the reference value


<a id="McUtils.Zachary.Surfaces.Surface.Surface.expansion_tensors" class="docs-object-method">&nbsp;</a> 
```python
@property
expansion_tensors(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Surfaces/Surface/Surface.py#L148)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface/Surface.py#L148?message=Update%20Docs)]
</div>
**LLM Docstring**

The expansion tensors of the base surface (if it has them).
  - `:returns`: `_`
    > the expansion tensors
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Surfaces/Surface/Surface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Surfaces/Surface/Surface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Surfaces/Surface/Surface.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Surfaces/Surface/Surface.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Surfaces/Surface.py#L10?message=Update%20Docs)   
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