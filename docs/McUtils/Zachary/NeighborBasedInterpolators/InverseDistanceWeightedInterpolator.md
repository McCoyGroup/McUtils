## <a id="McUtils.Zachary.NeighborBasedInterpolators.InverseDistanceWeightedInterpolator">InverseDistanceWeightedInterpolator</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators.py#L2924)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators.py#L2924?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.NeighborBasedInterpolators.InverseDistanceWeightedInterpolator.weight_deriv" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
weight_deriv(cls, disp, dists, norm, power, n, gammas_1=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2926)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2926?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the `n`-th-order contribution to the derivative of the inverse-distance
weights with respect to the query point.
  - `disp`: `np.ndarray`
    > the point-to-center displacements
  - `dists`: `np.ndarray`
    > the point-to-center distances
  - `norm`: `np.ndarray`
    > the per-point weight normalization
  - `power`: `float`
    > the inverse-distance power
  - `n`: `int`
    > the derivative order
  - `gammas_1`: `np.ndarray | None`
    > cached lower-order gamma terms
  - `:returns`: `tuple`
    > `(gammas, gradient_contribution)`


<a id="McUtils.Zachary.NeighborBasedInterpolators.InverseDistanceWeightedInterpolator.idw_derivs" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
idw_derivs(cls, deriv_order, disp, dists, norm, power, weights): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L2957)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L2957?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the derivatives (up to `deriv_order`, currently ≤ 2) of the
inverse-distance weights with respect to the query point.
  - `deriv_order`: `int`
    > the highest derivative order
  - `disp`: `np.ndarray`
    > the point-to-center displacements
  - `dists`: `np.ndarray`
    > the point-to-center distances
  - `norm`: `np.ndarray`
    > the weight normalization
  - `power`: `float`
    > the inverse-distance power
  - `weights`: `np.ndarray`
    > the base weights
  - `:returns`: `list`
    > the weight-derivative tensors


<a id="McUtils.Zachary.NeighborBasedInterpolators.InverseDistanceWeightedInterpolator.get_idw_weights" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_idw_weights(cls, pts, dists, disps=None, deriv_order=None, zero_tol=1e-06, power=2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L3014)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L3014?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the normalized inverse-distance weights (and optionally their
derivatives) for each query point, handling exact coincidences with a sample
point specially.
  - `pts`: `np.ndarray`
    > the query points
  - `dists`: `np.ndarray`
    > the point-to-neighbor distances
  - `disps`: `np.ndarray | None`
    > the point-to-neighbor displacements (needed for derivatives)
  - `deriv_order`: `int | None`
    > the highest derivative order (weights only if `None`)
  - `zero_tol`: `float`
    > the coincidence tolerance
  - `power`: `float`
    > the inverse-distance power
  - `:returns`: `np.ndarray | list`
    > the weights (and their derivatives if requested)


<a id="McUtils.Zachary.NeighborBasedInterpolators.InverseDistanceWeightedInterpolator.get_weights" class="docs-object-method">&nbsp;</a> 
```python
get_weights(self, pts, dists, inds, zero_tol=1e-06, power=2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators/InverseDistanceWeightedInterpolator.py#L3074)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators/InverseDistanceWeightedInterpolator.py#L3074?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the inverse-distance weights for a set of query points.
  - `pts`: `np.ndarray`
    > the query points
  - `dists`: `np.ndarray`
    > the point-to-neighbor distances
  - `inds`: `np.ndarray`
    > the neighbor indices
  - `zero_tol`: `float`
    > the coincidence tolerance
  - `power`: `float`
    > the inverse-distance power
  - `:returns`: `np.ndarray`
    > the weights


<a id="McUtils.Zachary.NeighborBasedInterpolators.InverseDistanceWeightedInterpolator.eval" class="docs-object-method">&nbsp;</a> 
```python
eval(self, pts, deriv_order=0, neighbors=None, merge_neighbors=None, reshape_derivatives=True, return_interpolation_data=False, check_in_sample=True, zero_tol=1e-08, return_error=False, use_cache=True, retries=None, max_distance=None, min_distance=None, neighborhood_clustering_radius=None, use_natural_neighbors=False, chunk_size=None, power=2, mode='fast'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/NeighborBasedInterpolators/InverseDistanceWeightedInterpolator.py#L3095)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators/InverseDistanceWeightedInterpolator.py#L3095?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate the inverse-distance-weighted interpolant (and derivatives) at a set of
query points, combining neighbor weights with the stored values and derivatives.
  - `pts`: `np.ndarray`
    > the query points
  - `deriv_order`: `int`
    > the highest derivative order
  - `neighbors`: `int | None`
    > the neighbor count
  - `merge_neighbors`: `int | None`
    > the group-merge threshold
  - `reshape_derivatives`: `bool`
    > return full derivative tensors
  - `return_interpolation_data`: `bool`
    > also return the interpolation data
  - `check_in_sample`: `bool`
    > short-circuit points coinciding with samples
  - `zero_tol`: `float`
    > the coincidence tolerance
  - `return_error`: `bool`
    > also return error estimates
  - `use_cache`: `bool`
    > reuse cached neighborhoods
  - `retries`: `int | None`
    > retries on failure
  - `:returns`: `np.ndarray | list | tuple`
    > the values (and extras as requested)
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/NeighborBasedInterpolators/InverseDistanceWeightedInterpolator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/NeighborBasedInterpolators/InverseDistanceWeightedInterpolator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/NeighborBasedInterpolators/InverseDistanceWeightedInterpolator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/NeighborBasedInterpolators/InverseDistanceWeightedInterpolator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/NeighborBasedInterpolators.py#L2924?message=Update%20Docs)   
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