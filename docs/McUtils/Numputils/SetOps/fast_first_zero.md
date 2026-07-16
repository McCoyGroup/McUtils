# <a id="McUtils.Numputils.SetOps.fast_first_zero">fast_first_zero</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/SetOps.py#L1005)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/SetOps.py#L1005?message=Update%20Docs)]
</div>

```python
fast_first_zero(arr, axis=-1): 
```
**LLM Docstring**

Find, for each row, the index of the first zero entry along an axis (or `-1`
if the row has no zeros).

The integer counterpart of `fast_first_nonzero`, using a byte-view trick.
  - `arr`: `np.ndarray`
    > the integer array to scan
  - `axis`: `int`
    > the axis to scan along
  - `:returns`: `np.ndarray`
    > the first-zero index per row (`-1` where none)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/SetOps/fast_first_zero.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/SetOps/fast_first_zero.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/SetOps/fast_first_zero.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/SetOps/fast_first_zero.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/SetOps.py#L1005?message=Update%20Docs)   
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