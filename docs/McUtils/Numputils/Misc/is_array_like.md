# <a id="McUtils.Numputils.Misc.is_array_like">is_array_like</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Misc.py#L90)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Misc.py#L90?message=Update%20Docs)]
</div>

```python
is_array_like(obj, valid_dtypes=None, ndim=None): 
```
**LLM Docstring**

Test whether an object is (or can be coerced into) a numeric-friendly array,
optionally constraining the dtype and/or number of dimensions.

Object-dtype arrays and atomic scalars are rejected; anything else is coerced
with `np.asanyarray` and validated against `valid_dtypes` and `ndim`.
  - `obj`: `Any`
    > the object to test
  - `valid_dtypes`: `Iterable | None`
    > acceptable dtype super-types (any-match)
  - `ndim`: `int | None`
    > required number of dimensions (any if omitted)
  - `:returns`: `bool`
    > whether the object is array-like under the constraints











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Misc/is_array_like.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Misc/is_array_like.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Misc/is_array_like.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Misc/is_array_like.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Misc.py#L90?message=Update%20Docs)   
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