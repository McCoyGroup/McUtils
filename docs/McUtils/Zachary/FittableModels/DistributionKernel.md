## <a id="McUtils.Zachary.FittableModels.DistributionKernel">DistributionKernel</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels.py#L287)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels.py#L287?message=Update%20Docs)]
</div>

Strategy interface for one mixture component's distribution family.
`params` is always a 2-tuple (location, scale-like) -- what "scale-like"
means is kernel-specific (std, Cauchy scale, von Mises kappa, wrapped
Cauchy rho), but every kernel takes exactly two parameters so they can
be swapped in and out of a model uniformly.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
registry: dict
periodic: bool
params: member_descriptor
```
<a id="McUtils.Zachary.FittableModels.DistributionKernel.register" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
register(cls, name, kernel=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L302)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L302?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.FittableModels.DistributionKernel.resolve" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
resolve(cls, name, *args): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L312)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L312?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.FittableModels.DistributionKernel.log_pdf" class="docs-object-method">&nbsp;</a> 
```python
log_pdf(self, x: 'np.ndarray', params: 'tuple[float, float]') -> 'np.ndarray': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L322)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L322?message=Update%20Docs)]
</div>
Log-density at each point in `x` given this component's params.


<a id="McUtils.Zachary.FittableModels.DistributionKernel.pdf" class="docs-object-method">&nbsp;</a> 
```python
pdf(self, x: 'np.ndarray', params: 'tuple[float, float]') -> 'np.ndarray': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L326)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L326?message=Update%20Docs)]
</div>
Density at each point in `x` given this component's params.


<a id="McUtils.Zachary.FittableModels.DistributionKernel.cdf" class="docs-object-method">&nbsp;</a> 
```python
cdf(self, x: 'np.ndarray', params: 'tuple[float, float]') -> 'np.ndarray': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L330)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L330?message=Update%20Docs)]
</div>
CDF at each point in `x` given this component's params. Always
required (used both for mixture .cdf() and as the fallback root-
finding target when a kernel has no closed-form .ppf).


<a id="McUtils.Zachary.FittableModels.DistributionKernel.ppf" class="docs-object-method">&nbsp;</a> 
```python
ppf(self, q: 'np.ndarray', params: 'tuple[float, float]' = None) -> 'np.ndarray': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L336)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L336?message=Update%20Docs)]
</div>
Closed-form inverse CDF for this *single* kernel (not the overall
mixture, which never has one). Override this in a subclass when
scipy provides one directly (see GaussianKernel/CauchyKernel/etc).
The default raises NotImplementedError, which signals
`MixtureDistribution` to fall back to numeric root-finding against
`cdf` when determining grid bounds for a kernel of this type.


<a id="McUtils.Zachary.FittableModels.DistributionKernel.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L347)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L347?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.FittableModels.DistributionKernel.to_state" class="docs-object-method">&nbsp;</a> 
```python
to_state(self) -> 'dict': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L350)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L350?message=Update%20Docs)]
</div>
Serialize this kernel's identity/config to a plain (JSON-able)
dict. The default assumes no constructor arguments; override
alongside `from_state` if a subclass needs to save extra config.


<a id="McUtils.Zachary.FittableModels.DistributionKernel.from_state" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_state(cls, state: 'dict') -> "'DistributionKernel'": 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L356)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L356?message=Update%20Docs)]
</div>
Reconstruct a kernel instance from a dict produced by
`to_state`. Looks the type up in the kernel registry, so any
`Kernel` subclass works automatically as long as it's been
defined (and decorated with `@_register_kernel`, or otherwise
registered) before this is called.


<a id="McUtils.Zachary.FittableModels.DistributionKernel.new_stats" class="docs-object-method">&nbsp;</a> 
```python
new_stats(self) -> 'dict': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L366)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L366?message=Update%20Docs)]
</div>
Zero-initialized accumulator dict for one EM pass.


<a id="McUtils.Zachary.FittableModels.DistributionKernel.accumulate" class="docs-object-method">&nbsp;</a> 
```python
accumulate(self, stats: 'dict', x: 'np.ndarray', resp: 'np.ndarray', params) -> 'None': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L370)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L370?message=Update%20Docs)]
</div>
Add one chunk's contribution to `stats`, in place.


<a id="McUtils.Zachary.FittableModels.DistributionKernel.finalize" class="docs-object-method">&nbsp;</a> 
```python
finalize(self, stats: 'dict', min_scale: 'float') -> 'tuple[float, float]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L374)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels/DistributionKernel.py#L374?message=Update%20Docs)]
</div>
Compute updated (loc, scale-like) from accumulated `stats`.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/FittableModels/DistributionKernel.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/FittableModels/DistributionKernel.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/FittableModels/DistributionKernel.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/FittableModels/DistributionKernel.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/FittableModels.py#L287?message=Update%20Docs)   
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