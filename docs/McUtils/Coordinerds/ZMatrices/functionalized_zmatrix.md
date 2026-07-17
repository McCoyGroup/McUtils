# <a id="McUtils.Coordinerds.ZMatrices.functionalized_zmatrix">functionalized_zmatrix</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Coordinerds/ZMatrices.py#L1201)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L1201?message=Update%20Docs)]
</div>

```python
functionalized_zmatrix(base_zm, attachments: 'dict|list[list[int], list[int]]' = None, single_atoms: list[int] = None, methyl_positions: list[int] = None, ethyl_positions: list[int] = None, validate=False): 
```
**LLM Docstring**

Build a larger Z-matrix by attaching fragments and optional standard substituent patterns.

`base_zm` and numeric fragment sizes are converted to chain Z-matrices. Each attachment replaces a fragment's negative placeholders with the supplied external references and shifts its local indices. Additional single atoms are attached using available neighboring references; methyl and ethyl positions append fixed three-atom and two-atom patterns. Optional validation is performed after every fragment addition.
  - `base_zm`: `int | Sequence[Sequence[int]]`
    > Existing Z-matrix or atom count for a chain base.
  - `attachments`: `dict | Iterable | None`
    > Mapping or iterable of `(attachment_points, fragment)` pairs.
  - `single_atoms`: `Sequence[int] | None`
    > Existing atom labels at which to append individual atoms.
  - `methyl_positions`: `Sequence[int] | None`
    > Existing atom labels at which to append the implemented three-row methyl pattern.
  - `ethyl_positions`: `Sequence[int] | None`
    > Existing atom labels at which to append the implemented two-row ethyl pattern.
  - `validate`: `bool`
    > Validate the ordering after each explicit fragment attachment.
  - `:returns`: `list[list[int]]`
    > Combined four-column Z-matrix ordering.











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Coordinerds/ZMatrices/functionalized_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Coordinerds/ZMatrices/functionalized_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Coordinerds/ZMatrices/functionalized_zmatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Coordinerds/ZMatrices/functionalized_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Coordinerds/ZMatrices.py#L1201?message=Update%20Docs)   
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