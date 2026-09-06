# <a id="McUtils.Zachary.FittableModels.fit_distribution_mixture_model">fit_distribution_mixture_model</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels.py#L1123)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels.py#L1123?message=Update%20Docs)]
</div>

```python
fit_distribution_mixture_model(data, kernels, weights_init=None, mask_fn=None, vals_key='vals', chunk_size=None, sample_size=None, seed=None, max_iter=100, tol=1e-06, min_scale=1e-06, verbose=False) -> 'FittedMixtureDistribution': 
```
Fit a k-component mixture, with a (possibly different) kernel per
component, to (optionally masked) values in `data`.

Works identically whether `data` is in memory or a chunked,
out-of-core store, and whether `sample_size` is set -- see the module
docstring of the earlier Gaussian-specific version for how `data` /
`chunk_size` are resolved; that mechanism is unchanged here.

Parameters
----------
kernels : list[Kernel], length k
    One kernel instance per component -- e.g.
    `[CauchyKernel(), GaussianKernel(), GaussianKernel()]` for one
    heavy-tailed component and two light-tailed ones. All kernels
    must agree on `periodic` (can't mix linear and circular kernels).
params_init : list[tuple[float, float]], length k
    Initial (loc, scale-like) guess per component, matching each
    kernel's `param_names` (e.g. (mean, std) for Gaussian,
    (loc, scale) for Cauchy, (mean, kappa) for von Mises).
weights_init : array-like, shape (k,), optional
    Initial mixture weights (default: uniform).
min_scale : float
    Regularization floor preventing a component from collapsing onto
    a single point (interpreted per-kernel: a scale/std floor for
    linear kernels, an equivalent concentration cap for periodic
    ones).
(all other parameters as in the Gaussian-only `fit_gaussian_mixture`)

Returns
-------
FittedMixtureDistribution












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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/FittableModels/fit_distribution_mixture_model.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/FittableModels/fit_distribution_mixture_model.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/FittableModels/fit_distribution_mixture_model.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/FittableModels/fit_distribution_mixture_model.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels.py#L1123?message=Update%20Docs)   
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