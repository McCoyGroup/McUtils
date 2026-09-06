# <a id="McUtils.ExternalPrograms.ConformerLibrary">McUtils.ExternalPrograms.ConformerLibrary</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ConformerLibrary.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary.py#L1?message=Update%20Docs)]
</div>
    
Provides `ConformerLibrary`, a small, backend-agnostic reader for
conformer ensembles stored as `(smi, coord)` pairs, one entry per
molecule.

The actual storage format is delegated to a `ConformerLibraryBackend`
adaptor (`backend`, always the library's first constructor argument).
The default `NumpyTreeArchiveBackend` reads/writes the "everything in
one tree" format built with `NumpyTreeArchive.from_tree` (see that
class's docstring), e.g.

    samp = TestManager.test_data('a2bbb-substances.smi')
    conf_lib = {}
    for i in [33, 68, 77]:
        smi = SMILESSupplier(samp).find_smi(i)
        confs, engs = generate_conformer_ensemble(Molecule.from_string, smi)
        conf_lib[str(i)] = {'smi': smi, 'coord': [c.coords for c in confs]}

    lib = ConformerLibrary(conf_lib)
    lib.save("conformers.npz")
    lib = ConformerLibrary.from_nparchive("conformers.npz")

`SMILESDatabaseBackend`, `QM9Backend`, and `GEOMBackend` adapt the same
`(smi, coord)`-pair interface onto a `SMILESSupplier`-backed `.smi`/
`.lismi` database, a packed `QM9` dataset, or a `GEOMLoader` archive,
respectively -- so the same `ConformerLibrary` interface works whether
conformers live in a purpose-built archive or are read straight out of
one of those external formats.

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[ConformerLibrary](ConformerLibrary/ConformerLibrary.md)   
</div>
   <div class="col" markdown="1">
   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>













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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ConformerLibrary.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ConformerLibrary.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ConformerLibrary.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ConformerLibrary.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ConformerLibrary.py#L1?message=Update%20Docs)   
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