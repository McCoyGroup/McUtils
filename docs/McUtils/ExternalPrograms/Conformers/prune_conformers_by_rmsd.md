# <a id="McUtils.ExternalPrograms.Conformers.prune_conformers_by_rmsd">prune_conformers_by_rmsd</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Conformers.py#L985)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Conformers.py#L985?message=Update%20Docs)]
</div>

```python
prune_conformers_by_rmsd(coords, masses=None, rmsd_cutoff: float = 0.025) -> numpy.ndarray[int]: 
```
Deduplicate a list of `Psience.Molecools.Molecule` conformers (same
connectivity, different geometries) by mass-weighted, Eckart-aligned
RMSD. No pre-alignment/embedding step is required -- the optimal
alignment is computed per compared pair by `McUtils.Numputils.eckart_rmsd`.
  - `structs`: `Any`
    > conformers of a single molecule
  - `rmsd_cutoff`: `Any`
    > the (per-atom, mass-weighted) RMSD below which two
    conformers are considered duplicates
  - `:returns`: `_`
    > one representative `Molecule` per RMSD cluster, in their
    original relative order











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Conformers/prune_conformers_by_rmsd.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Conformers/prune_conformers_by_rmsd.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Conformers/prune_conformers_by_rmsd.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Conformers/prune_conformers_by_rmsd.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Conformers.py#L985?message=Update%20Docs)   
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