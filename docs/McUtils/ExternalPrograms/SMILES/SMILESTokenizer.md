## <a id="McUtils.ExternalPrograms.SMILES.SMILESTokenizer">SMILESTokenizer</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L1536)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L1536?message=Update%20Docs)]
</div>

Atom-only SMILES tokenizer.

Regular expressions are compiled lazily and cached at the class
level. Each instance controls which bracket metadata fields are
retained.







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
SUPPORTED_METADATA: frozenset
BOND_ORDERS: dict
BOND_STEREOCHEMISTRY: frozenset
UNBRACKETED_ATOMS: frozenset
AROMATIC_ATOMS: frozenset
```
<a id="McUtils.ExternalPrograms.SMILES.SMILESTokenizer.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, *, metadata_fields: 'Collection[str] | None' = None) -> 'None': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES.py#L1594)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L1594?message=Update%20Docs)]
</div>


<a id="McUtils.ExternalPrograms.SMILES.SMILESTokenizer.tokenize" class="docs-object-method">&nbsp;</a> 
```python
tokenize(self, smiles: 'str') -> 'Iterator[SMILESAtom]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESTokenizer.py#L1742)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESTokenizer.py#L1742?message=Update%20Docs)]
</div>
Generate atom tokens in SMILES traversal order.

Non-atom tokens are consumed but not yielded. ``previous`` is
the index of the atom from which the generated atom branches.


<a id="McUtils.ExternalPrograms.SMILES.SMILESTokenizer.annotate" class="docs-object-method">&nbsp;</a> 
```python
annotate(self, smiles: 'str', annotation: 'str', block_size: 'int | list[int]', *, require_all_annotations: 'bool' = True) -> 'Iterator[AnnotatedAtom]': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/SMILES/SMILESTokenizer.py#L1896)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES/SMILESTokenizer.py#L1896?message=Update%20Docs)]
</div>
Add annotation slices and offsets to the base atom stream.
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/SMILES/SMILESTokenizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/SMILES/SMILESTokenizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/SMILES/SMILESTokenizer.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/SMILES/SMILESTokenizer.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/SMILES.py#L1536?message=Update%20Docs)   
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