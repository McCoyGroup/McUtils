## <a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction">SymPyFunction</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions.py#L1532)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions.py#L1532?message=Update%20Docs)]
</div>

A function suitable for symbolic manipulation
with derivatives and evlauation







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.get_sympy" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
get_sympy(cls): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L1538)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L1538?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.sympy" class="docs-object-method">&nbsp;</a> 
```python
@property
sympy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1542)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1542?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, expr, vars=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1546)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1546?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.sort_vars" class="docs-object-method">&nbsp;</a> 
```python
sort_vars(self, vars): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1562)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1562?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.merge_vars" class="docs-object-method">&nbsp;</a> 
```python
merge_vars(self, v1, v2): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1564)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1564?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.compile" class="docs-object-method">&nbsp;</a> 
```python
compile(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1569)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1569?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.eval" class="docs-object-method">&nbsp;</a> 
```python
eval(self, r: numpy.ndarray) -> 'np.ndarray': 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1574)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1574?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.deriv" class="docs-object-method">&nbsp;</a> 
```python
deriv(self, *which, order=1): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1585)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1585?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__call__" class="docs-object-method">&nbsp;</a> 
```python
__call__(self, r): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1621)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1621?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__neg__" class="docs-object-method">&nbsp;</a> 
```python
__neg__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1628)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1628?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__mul__" class="docs-object-method">&nbsp;</a> 
```python
__mul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1631)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1631?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__rmul__" class="docs-object-method">&nbsp;</a> 
```python
__rmul__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1638)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1638?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__truediv__" class="docs-object-method">&nbsp;</a> 
```python
__truediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1640)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1640?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__rtruediv__" class="docs-object-method">&nbsp;</a> 
```python
__rtruediv__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1647)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1647?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__add__" class="docs-object-method">&nbsp;</a> 
```python
__add__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1655)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1655?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__radd__" class="docs-object-method">&nbsp;</a> 
```python
__radd__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1662)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1662?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__sub__" class="docs-object-method">&nbsp;</a> 
```python
__sub__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1670)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1670?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__rsub__" class="docs-object-method">&nbsp;</a> 
```python
__rsub__(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1677)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1677?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__pow__" class="docs-object-method">&nbsp;</a> 
```python
__pow__(self, power, modulo=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1685)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1685?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.invert" class="docs-object-method">&nbsp;</a> 
```python
invert(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1693)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1693?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__invert__" class="docs-object-method">&nbsp;</a> 
```python
__invert__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1695)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1695?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1697)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1697?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.compose" class="docs-object-method">&nbsp;</a> 
```python
compose(self, other): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1699)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1699?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.symbols" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
symbols(cls, *syms): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L1710)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L1710?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.exp" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
exp(cls, fn): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L1714)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L1714?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.morse" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
morse(cls, var, de=10, a=1, re=0): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/__init__.py#L1717)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/__init__.py#L1717?message=Update%20Docs)]
</div>


<a id="McUtils.McUtils.Zachary.Symbolic.ElementaryFunctions.SymPyFunction.__repr__" class="docs-object-method">&nbsp;</a> 
```python
__repr__(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1723)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.py#L1723?message=Update%20Docs)]
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Symbolic/ElementaryFunctions/SymPyFunction.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Symbolic/ElementaryFunctions.py#L1532?message=Update%20Docs)   
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