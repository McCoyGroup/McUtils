# <a id="McUtils.ExternalPrograms.Conformers.generate_conformer_ensemble">generate_conformer_ensemble</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Conformers.py#L1039)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Conformers.py#L1039?message=Update%20Docs)]
</div>

```python
generate_conformer_ensemble(molecule_generator, smiles: str, *, energy_evaluator=None, optimizer=None, target_num_structs: int = 10, num_pregen: int = None, conf_gen_options: Optional[dict] = None, evaluate_energy: bool = True, preoptimize: bool = True, optimizer_settings: Optional[dict] = None, rmsd_cutoff: Optional[float] = 0.025, preopt_iterations: int = 50, spin: int = 1, verbose: bool = False, **molecule_options) -> list: 
```
The core, single-SMILES "generate -> dedupe -> optimize" routine.

Given one SMILES string, this:

  1. embeds up to `conf_gen_options['numConfs']` (or `target_num_structs`, if
     energies aren't being evaluated) 3D conformers with RDKit's
     ETKDG-family embedder (via `Psience.Molecools.Molecule`),
  2. deduplicates them by mass-weighted, Eckart-aligned RMSD
     (`prune_conformers_by_rmsd`, `rmsd_cutoff`),
  3. optionally pre-optimizes every surviving conformer and re-dedupes,
  4. evaluates each conformer's energy and picks the lowest-`target_num_structs`
     (re-optimizing -- and re-scoring -- that final set if it wasn't
     already fully optimized in step 3), and
  5. returns them as `ConformerRecord`s, most-favorable first.

This function is side-effect free: it never writes to disk, and it
never raises on chemically invalid or unembeddable SMILES -- it returns
an empty list instead, so batch drivers can skip bad entries without
special-casing them.
  - `smiles`: `Any`
    > a single SMILES string
  - `target_num_structs`: `Any`
    > number of final conformers to keep
  - `conf_gen_options`: `Any`
    > passed through to the ETKDG embedder; merged
    over `default_conformer_generator_options` (user options win)
  - `energy_evaluator`: `Any`
    > the `Psience` energy evaluator (name, spec
    dict, or a raw ASE-style calculator object)
  - `evaluate_energy`: `Any`
    > whether to compute energies at all
  - `preoptimize`: `Any`
    > optimize every surviving conformer up front (rather
    than only the final selected set)
  - `optimizer_settings`: `Any`
    > passed to `Molecule.optimize`
  - `rmsd_cutoff`: `Any`
    > RMSD below which two conformers are considered
    duplicates (`None` disables deduplication)
  - `preopt_iterations`: `Any`
    > max iterations for the (cheaper)
    pre-optimization pass
  - `spin`: `Any`
    > passed through to `Molecule.from_string`
  - `verbose`: `Any`
    > print basic progress information
  - `:returns`: `_`
    > the selected conformers as `ConformerRecord`s (empty if the
    SMILES couldn't be parsed, embedded, or optimized)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Conformers/generate_conformer_ensemble.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Conformers/generate_conformer_ensemble.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Conformers/generate_conformer_ensemble.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Conformers/generate_conformer_ensemble.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Conformers.py#L1039?message=Update%20Docs)   
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