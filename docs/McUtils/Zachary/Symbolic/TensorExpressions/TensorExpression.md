## <a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorExpression">TensorExpression</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Symbolic/TensorExpressions.py#L14)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions.py#L14?message=Update%20Docs)]
</div>









<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
ArrayStack: ArrayStack
Term: Term
SumTerm: SumTerm
ScalingTerm: ScalingTerm
ScalarScalingTerm: ScalarScalingTerm
ScalarPowerTerm: ScalarPowerTerm
FlippedTerm: FlippedTerm
AxisShiftTerm: AxisShiftTerm
OuterTerm: OuterTerm
ContractionTerm: ContractionTerm
InverseTerm: InverseTerm
TraceTerm: TraceTerm
DeterminantTerm: DeterminantTerm
VectorNormTerm: VectorNormTerm
ScalarFunctionTerm: ScalarFunctionTerm
ConstantArray: ConstantArray
IdentityMatrix: IdentityMatrix
OuterPowerTerm: OuterPowerTerm
TermVector: TermVector
CoordinateVector: CoordinateVector
CoordinateTerm: CoordinateTerm
PolynomialTerm: PolynomialTerm
```
<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorExpression.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, expr: 'TensorExpression.Term|List', **vars): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Symbolic/TensorExpressions/TensorExpression.py#L15)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions/TensorExpression.py#L15?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorExpression.eval" class="docs-object-method">&nbsp;</a> 
```python
eval(self, subs: dict = None, print_terms=False): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Symbolic/TensorExpressions/TensorExpression.py#L19)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions/TensorExpression.py#L19?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorExpression.primitives" class="docs-object-method">&nbsp;</a> 
```python
@property
primitives(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Symbolic/TensorExpressions/TensorExpression.py#L81)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions/TensorExpression.py#L81?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorExpression.walk" class="docs-object-method">&nbsp;</a> 
```python
walk(self, callback): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Symbolic/TensorExpressions/TensorExpression.py#L86)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions/TensorExpression.py#L86?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorExpression.get_prims" class="docs-object-method">&nbsp;</a> 
```python
get_prims(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Symbolic/TensorExpressions/TensorExpression.py#L98)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions/TensorExpression.py#L98?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Symbolic.TensorExpressions.TensorExpression.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Symbolic/TensorExpressions/TensorExpression.py#L105)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions/TensorExpression.py#L105?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Zachary/Symbolic/TensorExpressions/TensorExpression.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Zachary/Symbolic/TensorExpressions/TensorExpression.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Zachary/Symbolic/TensorExpressions/TensorExpression.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Zachary/Symbolic/TensorExpressions/TensorExpression.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Symbolic/TensorExpressions.py#L14?message=Update%20Docs)   
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