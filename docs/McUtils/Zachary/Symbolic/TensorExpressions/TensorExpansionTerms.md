## <a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorExpansionTerms">TensorExpansionTerms</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Symbolic/TensorExpressions.py#L1524)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions.py#L1524?message=Update%20Docs)]
</div>

A friend of DumbTensor which exists
to not only make the tensor algebra suck less but also
to make it automated by making use of some simple rules
for expressing derivatives specifically in the context of
doing the coordinate transformations we need to do.
Everything here is 1 indexed since that's how I did the OG math







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
QXTerm: QXTerm
XVTerm: XVTerm
QXVTerm: QXVTerm
BasicContractionTerm: BasicContractionTerm
```
<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorExpansionTerms.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, qx_terms, xv_terms, qxv_terms=None, base_qx=None, base_xv=None, q_name='Q', v_name='V'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.py#L1533)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.py#L1533?message=Update%20Docs)]
</div>

  - `qx_terms`: `Iterable[np.ndarray]`
    > 
  - `xv_terms`: `Iterable[np.ndarray]`
    >


<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorExpansionTerms.QX" class="docs-object-method">&nbsp;</a> 
```python
QX(self, n): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.py#L1550)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.py#L1550?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorExpansionTerms.XV" class="docs-object-method">&nbsp;</a> 
```python
XV(self, m): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.py#L1552)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.py#L1552?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorExpansionTerms.QXV" class="docs-object-method">&nbsp;</a> 
```python
QXV(self, n, m): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.py#L1554)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.py#L1554?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Symbolic/TensorExpressions/TensorExpansionTerms.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions.py#L1524?message=Update%20Docs)   
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