# <a id="McUtils.Numputils.VectorOps.apply_by_structures">apply_by_structures</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L1726)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L1726?message=Update%20Docs)]
</div>

```python
apply_by_structures(tf, points, ndim=1, **kwargs): 
```
**LLM Docstring**

Apply a transformation function to each structure in a batch individually.

The leading batch axes are flattened, `tf` is called once per structure, and the
results are restacked. If `tf` returns extra values alongside its primary array,
those are collected and returned separately.
  - `tf`: `Callable`
    > the per-structure transformation function
  - `points`: `np.ndarray`
    > the batched points/structures
  - `ndim`: `int`
    > number of trailing axes belonging to a single structure
  - `kwargs`: `Any`
    > extra keyword arguments forwarded to `tf`
  - `:returns`: `np.ndarray | tuple`
    > the stacked results (plus any extra returns from `tf`)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/apply_by_structures.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/apply_by_structures.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/apply_by_structures.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/apply_by_structures.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L1726?message=Update%20Docs)   
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