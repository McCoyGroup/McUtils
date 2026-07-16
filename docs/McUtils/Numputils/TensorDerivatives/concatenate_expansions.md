# <a id="McUtils.Numputils.TensorDerivatives.concatenate_expansions">concatenate_expansions</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TensorDerivatives.py#L796)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L796?message=Update%20Docs)]
</div>

```python
concatenate_expansions(a_expansion_or_expansion_list, b_expansion=None, concatenate_values=True): 
```
**LLM Docstring**

Concatenate expansions, either along the value axis or along the derivative
(coordinate) axes.

With a single list argument the expansions are concatenated pairwise. With
`concatenate_values` set the value axis is joined; otherwise the derivative axes
are joined into block-diagonal form. Missing/zero terms are filled with
appropriately shaped zeros.
  - `a_expansion_or_expansion_list`: `list`
    > the first expansion, or a list of expansions
  - `b_expansion`: `list | None`
    > the second expansion (omit to pass a list as the first arg)
  - `concatenate_values`: `bool`
    > join along the value axis (vs. the derivative axes)
  - `:returns`: `list`
    > the concatenated expansion











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TensorDerivatives/concatenate_expansions.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TensorDerivatives/concatenate_expansions.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TensorDerivatives/concatenate_expansions.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TensorDerivatives/concatenate_expansions.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L796?message=Update%20Docs)   
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