## <a id="McUtils.Zachary.FittableModels.MixtureDistribution">MixtureDistribution</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels.py#L718)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels.py#L718?message=Update%20Docs)]
</div>

A k-component mixture distribution with a (possibly heterogeneous)
kernel per component -- the "just the math" parent class. Knows how
to evaluate pdf/cdf, build and use a numeric ppf (inverse CDF), and
save/load that ppf to disk. Doesn't know or care how it was produced;
see `FittedMixtureDistribution` for the subclass that adds that.

Attributes
----------
kernels : list[Kernel], length k
    One kernel instance per component; may be different types (but
    all must agree on `.periodic`).
params : list[tuple[float, float]], length k
    (loc, scale-like) parameters per component, matching
    `kernels[j].param_names`.
weights : np.ndarray, shape (k,)







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.FittableModels.MixtureDistribution.__post_init__" class="docs-object-method">&nbsp;</a> 
```python
__post_init__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L743)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L743?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.FittableModels.MixtureDistribution.k" class="docs-object-method">&nbsp;</a> 
```python
@property
k(self) -> 'int': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L747)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L747?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.FittableModels.MixtureDistribution.periodic" class="docs-object-method">&nbsp;</a> 
```python
@property
periodic(self) -> 'bool': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L751)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L751?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.FittableModels.MixtureDistribution.component_pdfs" class="docs-object-method">&nbsp;</a> 
```python
component_pdfs(self, x): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L755)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L755?message=Update%20Docs)]
</div>
Weighted per-component densities at `x`, shape (*, k). Useful
for plotting each colored component curve individually.


<a id="McUtils.Zachary.FittableModels.MixtureDistribution.pdf" class="docs-object-method">&nbsp;</a> 
```python
pdf(self, x): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L764)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L764?message=Update%20Docs)]
</div>
Mixture density at `x`: sum of weighted per-component densities.


<a id="McUtils.Zachary.FittableModels.MixtureDistribution.component_cdfs" class="docs-object-method">&nbsp;</a> 
```python
component_cdfs(self, x): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L768)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L768?message=Update%20Docs)]
</div>
Weighted per-component CDFs at `x`, shape (*, k).


<a id="McUtils.Zachary.FittableModels.MixtureDistribution.cdf" class="docs-object-method">&nbsp;</a> 
```python
cdf(self, x): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L776)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L776?message=Update%20Docs)]
</div>
Mixture CDF at `x`: sum of weighted per-component CDFs. Always
available in closed form (every kernel supplies `.cdf` via
scipy), even for kernels/mixtures with no closed-form `.ppf`.

Note: for a periodic mixture this is itself periodic --
cdf(x) == cdf(x + 2*pi) exactly, since they're the same physical
angle. That's correct for density/mass questions (and matches
pdf's periodicity), but it is *not* usable as a monotonic
quantile map across a full period -- see `unwrapped_cdf` for
that.


<a id="McUtils.Zachary.FittableModels.MixtureDistribution.unwrapped_cdf" class="docs-object-method">&nbsp;</a> 
```python
unwrapped_cdf(self, x, grid_size=2000, eps=1e-09, rebuild=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L791)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L791?message=Update%20Docs)]
</div>
A monotonically increasing "unwrapped" CDF across one full
period (0 -> 1 as x sweeps from the period's start to its end),
for periodic mixtures. Non-periodic mixtures just delegate to
the ordinary `.cdf()`, which is already monotonic.

Built from the same (q, x) PPF grid used by `.ppf()` (lazily
built on first call, exactly like `.ppf()`), inverted the other
way via interpolation -- i.e. this and `.ppf()` are exact
inverses of each other by construction, which `.cdf()` is not
for a periodic mixture.

This exists for callers that need a proper quantile map spanning
a full period (e.g. truncated-quantile encoding schemes) rather
than the periodic `.cdf()`, which wraps back to its starting
value before reaching 1.


<a id="McUtils.Zachary.FittableModels.MixtureDistribution.ppf" class="docs-object-method">&nbsp;</a> 
```python
ppf(self, q, grid_size=2000, eps=1e-09, rebuild=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L898)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L898?message=Update%20Docs)]
</div>
Inverse CDF, via grid-based linear interpolation over precomputed
(q, x) pairs -- built lazily on first call (or forced with
`rebuild=True`), since a mixture's CDF essentially never has a
closed-form inverse even when every component's CDF does.


<a id="McUtils.Zachary.FittableModels.MixtureDistribution.save_ppf_grid" class="docs-object-method">&nbsp;</a> 
```python
save_ppf_grid(self, path, grid_size=2000, eps=1e-09): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L910)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L910?message=Update%20Docs)]
</div>
Save the ppf grid to an NPZ file: `ppf_grid` (q values),
`ppf_values` (corresponding x values), and `metadata` (a JSON
string describing each component's kernel type, params, and
weight -- enough to fully reconstruct this mixture via
`MixtureDistribution.load_ppf_grid`).


<a id="McUtils.Zachary.FittableModels.MixtureDistribution.load_ppf_grid" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
load_ppf_grid(cls, path) -> "'MixtureDistribution'": 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L937)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L937?message=Update%20Docs)]
</div>
Reconstruct a `MixtureDistribution` (kernels, params, weights,
and the precomputed ppf grid) from a file written by
`save_ppf_grid`. The result supports `.pdf`/`.cdf`/`.ppf`
immediately; `.ppf` uses the loaded grid without recomputing it.


<a id="McUtils.Zachary.FittableModels.MixtureDistribution.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L958)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/MixtureDistribution.py#L958?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.FittableModels.__create_fn__.<locals>.__eq__" class="docs-object-method">&nbsp;</a> 
```python
__eq__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/__create_fn__/<locals>.py#L)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/__create_fn__/<locals>.py#L?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/FittableModels/MixtureDistribution.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/FittableModels/MixtureDistribution.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/FittableModels/MixtureDistribution.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/FittableModels/MixtureDistribution.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels.py#L718?message=Update%20Docs)   
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