# <a id="McUtils.Numputils.TensorDerivatives.orthogonalize_transformations">orthogonalize_transformations</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/TensorDerivatives.py#L986)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L986?message=Update%20Docs)]
</div>

```python
orthogonalize_transformations(transformation_pairs, order=None, orthonormalize=True, assume_prenormalized=True, first_order_projector=True, nonzero_cutoff=None, concatenate=True): 
```
**LLM Docstring**

Orthogonalize a sequence of forward/reverse transformation pairs against one
another, building a combined (block) transformation.

Each successive pair is projected against the accumulated complement projector
(Gram-Schmidt style) and optionally renormalized; the projector is updated after
each step. The per-pair results are optionally concatenated into a single
forward/reverse expansion.
  - `transformation_pairs`: `Iterable[tuple]`
    > the `(forward, reverse)` expansion pairs
  - `order`: `int | None`
    > the derivative order (inferred from the inputs if omitted)
  - `orthonormalize`: `bool`
    > renormalize each projected pair
  - `assume_prenormalized`: `bool`
    > skip the initial renormalization of each pair
  - `first_order_projector`: `bool`
    > use only the leading-order projector
  - `nonzero_cutoff`: `float | None`
    > singular-value cutoff used during renormalization
  - `concatenate`: `bool`
    > concatenate the results into a single transformation
  - `:returns`: `tuple`
    > the orthogonalized `(forward, reverse)` transformations











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/TensorDerivatives/orthogonalize_transformations.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/TensorDerivatives/orthogonalize_transformations.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/TensorDerivatives/orthogonalize_transformations.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/TensorDerivatives/orthogonalize_transformations.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/TensorDerivatives.py#L986?message=Update%20Docs)   
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