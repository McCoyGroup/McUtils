## <a id="McUtils.Numputils.Optimization.NudgedElasticBandStepFinder">NudgedElasticBandStepFinder</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L1725)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L1725?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization.py#L1726)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L1726?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Optimization.NudgedElasticBandStepFinder.get_dist" class="docs-object-method">&nbsp;</a> 
```python
get_dist(self, p1, p2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L1744)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L1744?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Optimization.NudgedElasticBandStepFinder.get_tangent" class="docs-object-method">&nbsp;</a> 
```python
get_tangent(self, guess, mask, cur, prev, next): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L1747)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L1747?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Optimization.NudgedElasticBandStepFinder.adjust_jacobian" class="docs-object-method">&nbsp;</a> 
```python
adjust_jacobian(self, jac, guess, mask, cur, prev, next): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L1770)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L1770?message=Update%20Docs)]
</div>


<a id="McUtils.Numputils.Optimization.NudgedElasticBandStepFinder.image_pairwise_contribution" class="docs-object-method">&nbsp;</a> 
```python
image_pairwise_contribution(self, guess, mask, cur, prev, next, order=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L1776)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.py#L1776?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Optimization/NudgedElasticBandStepFinder.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Optimization.py#L1725?message=Update%20Docs)   
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