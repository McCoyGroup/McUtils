## <a id="McUtils.Numputils.Optimization.NudgedElasticBandStepFinder">NudgedElasticBandStepFinder</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L3839)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L3839?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Numputils.Optimization.NudgedElasticBandStepFinder.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, func, jacobian, hessian=None, spring_constants=0.1, distance_function=None, step_finder='gradient-descent', logger=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L3840)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L3840?message=Update%20Docs)]
</div>
**LLM Docstring**

Initialize a nudged-elastic-band (NEB) step finder with spring couplings between
neighbouring images.
  - `func`: `Callable`
    > the per-image objective
  - `jacobian`: `Callable`
    > the per-image gradient
  - `hessian`: `Callable | None`
    > the per-image Hessian
  - `spring_constants`: `float | np.ndarray`
    > spring constant(s) between images
  - `distance_function`: `Callable | None`
    > optional custom inter-image distance
  - `step_finder`: `str`
    > the base per-image method
  - `logger`: `object | None`
    > optional logger
  - `opts`: `Any`
    > extra options for the base step finder


<a id="McUtils.Numputils.Optimization.NudgedElasticBandStepFinder.get_dist" class="docs-object-method">&nbsp;</a> 
```python
get_dist(self, p1, p2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L3880)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L3880?message=Update%20Docs)]
</div>
**LLM Docstring**

Return the Euclidean distance between two image geometries.
  - `p1`: `np.ndarray`
    > the first geometry
  - `p2`: `np.ndarray`
    > the second geometry
  - `:returns`: `np.ndarray`
    > the distance


<a id="McUtils.Numputils.Optimization.NudgedElasticBandStepFinder.get_tangent" class="docs-object-method">&nbsp;</a> 
```python
get_tangent(self, guess, mask, cur, prev, next): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L3895)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L3895?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the (normalized) NEB path tangent at an image, using the energy-weighted
tangent scheme based on the neighbouring image energies.
  - `guess`: `np.ndarray`
    > the full chain
  - `mask`: `np.ndarray`
    > active-member indices
  - `cur`: `int`
    > current image index
  - `prev`: `int`
    > previous image index
  - `next`: `int`
    > next image index
  - `:returns`: `np.ndarray`
    > the unit path tangent


<a id="McUtils.Numputils.Optimization.NudgedElasticBandStepFinder.adjust_jacobian" class="docs-object-method">&nbsp;</a> 
```python
adjust_jacobian(self, jac, guess, mask, cur, prev, next): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L3937)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L3937?message=Update%20Docs)]
</div>
**LLM Docstring**

Project the tangential component out of the per-image gradient (the NEB
nudging), caching the current path tangent.
  - `jac`: `np.ndarray`
    > the base gradient
  - `guess`: `np.ndarray`
    > the full chain
  - `mask`: `np.ndarray`
    > active-member indices
  - `cur`: `int`
    > current image index
  - `prev`: `int | None`
    > previous image index
  - `next`: `int | None`
    > next image index
  - `:returns`: `np.ndarray`
    > the nudged gradient


<a id="McUtils.Numputils.Optimization.NudgedElasticBandStepFinder.climbing_node_step" class="docs-object-method">&nbsp;</a> 
```python
climbing_node_step(self, guess, mask, gradient_modifer=None, projector=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L3967)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L3967?message=Update%20Docs)]
</div>
**LLM Docstring**

Take a climbing-image step: invert the tangential force component so the image
climbs toward the saddle along the path.
  - `guess`: `np.ndarray`
    > the climbing-image parameters
  - `mask`: `np.ndarray`
    > active-member indices
  - `gradient_modifer`: `Callable | None`
    > optional gradient transformation
  - `projector`: `np.ndarray | None`
    > optional projector
  - `:returns`: `tuple`
    > `(step, gradient)`


<a id="McUtils.Numputils.Optimization.NudgedElasticBandStepFinder.image_pairwise_contribution" class="docs-object-method">&nbsp;</a> 
```python
image_pairwise_contribution(self, guess, mask, cur, prev, next, order=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L4010)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L4010?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the NEB spring contribution to the objective/gradient/Hessian from the
difference of the distances to the two neighbouring images.
  - `guess`: `np.ndarray`
    > the full chain
  - `mask`: `np.ndarray`
    > active-member indices
  - `cur`: `int`
    > current image index
  - `prev`: `int | None`
    > previous image index
  - `next`: `int | None`
    > next image index
  - `order`: `int`
    > derivative order (`0`=value, `1`=gradient, `2`=Hessian)
  - `:returns`: `np.ndarray | int`
    > the spring contribution
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L3839?message=Update%20Docs)   
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