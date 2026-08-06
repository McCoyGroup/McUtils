## <a id="McUtils.ExternalPrograms.Parsers.QChem.QChemLogReader">QChemLogReader</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Parsers/QChem.py#L12)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/QChem.py#L12?message=Update%20Docs)]
</div>

Implements a stream-based reader for a Q-Chem output (`.out`/`.log`) file.

Parallels `MOLPROLogReader`/`OrcaLogReader`: the block tag/parser table lives in
the companion `QChemLogComponents` module and is resolved lazily by the
`ElectronicStructureLogReader` base. Read data with `parse`, or the convenience
classmethod `read_props`::

    from McUtils.ExternalPrograms.Parsers import QChemLogReader

    data = QChemLogReader.read_props(
        "job.out",
        ["Header", "CartesianCoordinates", "SCFEnergies", "FinalEnergy"]
    )







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
components_name: str
```

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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Parsers/QChem/QChemLogReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Parsers/QChem/QChemLogReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Parsers/QChem/QChemLogReader.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Parsers/QChem/QChemLogReader.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Parsers/QChem.py#L12?message=Update%20Docs)   
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