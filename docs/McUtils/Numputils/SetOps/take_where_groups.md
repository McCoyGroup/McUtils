# <a id="McUtils.Numputils.SetOps.take_where_groups">take_where_groups</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/SetOps.py#L931)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/SetOps.py#L931?message=Update%20Docs)]
</div>

```python
take_where_groups(arr, where, presorted=True, return_rows=False): 
```
**LLM Docstring**

Gather the values selected by a multi-axis `where` result and split them into
groups by their leading index.

When the groups are equal-sized (and presorted) the values are simply reshaped;
otherwise they are split at the group boundaries. The group row labels can
optionally be returned alongside.
  - `arr`: `np.ndarray`
    > the array to gather from
  - `where`: `tuple[np.ndarray, ...]`
    > a multi-axis `where`-style index tuple
  - `presorted`: `bool`
    > whether the `where` entries are already grouped/sorted
  - `return_rows`: `bool`
    > also return the group row labels
  - `:returns`: `list | tuple`
    > the grouped values (and rows if requested)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/SetOps/take_where_groups.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/SetOps/take_where_groups.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/SetOps/take_where_groups.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/SetOps/take_where_groups.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/SetOps.py#L931?message=Update%20Docs)   
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