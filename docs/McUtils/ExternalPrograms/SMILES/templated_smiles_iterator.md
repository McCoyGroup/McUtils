# <a id="McUtils.ExternalPrograms.SMILES.templated_smiles_iterator">templated_smiles_iterator</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L1962)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L1962?message=Update%20Docs)]
</div>

```python
templated_smiles_iterator(scaffold: 'str', fragments: 'Sequence[str]', active_sites: 'Sequence[int]', chiralities: 'Optional[Sequence[Union[str, Sequence[str]]]]' = None, stereos: 'Optional[dict]' = None, bond_orders: 'Optional[Sequence]' = None, atom_replacements: 'Optional[dict]' = None, attachment_bond_orders: 'Optional[Sequence[Union[int, float]]]' = None, binding_sites: 'Optional[Sequence[int]]' = None, cache: 'Optional[dict]' = None, add_implicit_hydrogens: 'Union[bool, str]' = 'full', remove_sites: 'Union[bool, Sequence[int]]' = False, reorder_from_atom_map: 'bool' = True, return_fragment_indices: 'bool' = False, return_new_bonds: 'bool' = False, filter: 'Optional[Callable[[str, Sequence[int], Sequence[str]], bool]]' = None, quiet: 'bool' = False, smiles_cache: 'set | None' = None, deduplicate: 'bool' = True) -> 'Iterable': 
```
Enumerate a SMILES library by attaching one fragment (with repetition
allowed) from `fragments` onto each of `active_sites` on `scaffold`,
optionally expanded over every combination of `chiralities` at those
sites. Every product is built with a single call to
`McUtils.ExternalPrograms.SMILES.build_templated_smiles`, which is
given every fragment for this combination as its `*replacements`
together with whichever of `atom_replacements`/`bond_orders`/
`chiralities`/`stereos`/`remove_sites` the caller supplied, so a
single library-generation call can do the whole "attach substituents,
then fix up bond orders/atom identities/stereocenters, then strip the
binding-site atom maps" job in one pass, exactly as
`build_templated_smiles` is designed to.

This function only drives the two axes that make sense to expand
combinatorially (which fragment goes where, and which chirality/
stereo winding it's built with); every other `build_templated_smiles`
argument is forwarded verbatim to every product.
  - `scaffold`: `Any`
    > the scaffold SMILES; if it doesn't yet carry the
    atom-map numbers referenced by `active_sites`, pass `binding_sites`
    (raw, 0-indexed atom positions) to have `build_templated_smiles`
    assign them first
  - `fragments`: `Any`
    > candidate fragment SMILES (each should carry a single
    atom-map-numbered attachment atom), drawn from combinatorially
    (with repetition) to fill `active_sites`
  - `active_sites`: `Any`
    > the 0-indexed, atom-map-based attachment sites on
    `scaffold` -- i.e. site `s` attaches to the atom carrying atom-map
    number `s + 1`. Forwarded into each `build_templated_smiles`
    replacement's own `new_bonds=[[site, 0, bond_order]]`.
  - `chiralities`: `Any`
    > for each site, either a single winding ('CW'/'CCW')
    or a list of windings to expand over combinatorially; forwarded to
    `build_templated_smiles`'s `chiralities` (as `{site: winding, ...}`)
    for each combination
  - `stereos`: `Any`
    > forwarded verbatim to `build_templated_smiles`'s
    `stereos`
  - `bond_orders`: `Any`
    > forwarded verbatim to `build_templated_smiles`'s
    `bond_orders`
  - `atom_replacements`: `Any`
    > forwarded verbatim to `build_templated_smiles`'s
    `atom_replacements`
  - `attachment_bond_orders`: `Any`
    > the bond order used to attach each
    fragment (parallel to `active_sites`; defaults to all single bonds)
  - `binding_sites`: `Any`
    > forwarded verbatim to `build_templated_smiles`'s
    own `active_sites` -- raw, 0-indexed atom positions on an
    as-yet-unmapped `scaffold` to assign sequential atom-map numbers
    to, *before* fragment attachment. Distinct from this function's
    own `active_sites`, which always refers to atom-map numbers.
  - `cache`: `Any`
    > an optional shared parse cache (see
    `McUtils.ExternalPrograms.SMILES.parse_smiles_and_atom_map`); a
    fresh one is created and reused across the whole iterator if
    omitted
  - `add_implicit_hydrogens`: `Any`
    > forwarded verbatim to
    `build_templated_smiles`
  - `remove_sites`: `Any`
    > forwarded verbatim to `build_templated_smiles`'s
    `remove_sites` (strip the attachment atom maps from the final
    product)
  - `reorder_from_atom_map`: `Any`
    > forwarded verbatim to
    `build_templated_smiles`
  - `return_fragment_indices`: `Any`
    > forwarded verbatim to
    `build_templated_smiles`; if set, each yielded item is a tuple
    `(smiles, fragments)` rather than a bare string
  - `return_new_bonds`: `Any`
    > forwarded verbatim to `build_templated_smiles`;
    if set (together with `return_fragment_indices`), each yielded item
    is a tuple `(smiles, fragments, new_bonds)`
  - `filter`: `Any`
    > `filter(scaffold, active_sites, frags) -> bool`, applied
    to each raw fragment combination before it's built
  - `:returns`: `_`
    > an iterator of product SMILES strings (or tuples, if
    `return_fragment_indices`/`return_new_bonds` is set)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/SMILES/templated_smiles_iterator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/SMILES/templated_smiles_iterator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/SMILES/templated_smiles_iterator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/SMILES/templated_smiles_iterator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L1962?message=Update%20Docs)   
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