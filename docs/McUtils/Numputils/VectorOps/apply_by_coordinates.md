# <a id="McUtils.Numputils.VectorOps.apply_by_coordinates">apply_by_coordinates</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L1680)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L1680?message=Update%20Docs)]
</div>

```python
apply_by_coordinates(tf, points, reroll=None, ndim=1, **kwargs): 
```
**LLM Docstring**

Apply a transformation function that expects its inputs split into separate
coordinate arguments.

The trailing `ndim` coordinate axes are rolled to the front so they can be
unpacked as positional arguments to `tf`; the result is rolled back (when it
matches the input layout, or when `reroll` is forced). If `tf` returns extra
values alongside the transformed points, those are passed through.
  - `tf`: `Callable`
    > the transformation function (called as `tf(*coords, **kwargs)`)
  - `points`: `np.ndarray`
    > the points to transform
  - `reroll`: `bool | None`
    > force rolling the coordinate axes back (auto-detected if `None`)
  - `ndim`: `int`
    > number of trailing coordinate axes to split off
  - `kwargs`: `Any`
    > extra keyword arguments forwarded to `tf`
  - `:returns`: `np.ndarray | tuple`
    > the transformed points (plus any extra returns from `tf`)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/apply_by_coordinates.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/apply_by_coordinates.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/apply_by_coordinates.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/apply_by_coordinates.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L1680?message=Update%20Docs)   
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