## <a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix">FiniteDifferenceMatrix</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction.py#L668)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction.py#L668?message=Update%20Docs)]
</div>

Defines a matrix that can be applied to a regular grid of values to take a finite difference







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse " id="methods" markdown="1">
 
<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, finite_difference_data, npts=None, mesh_spacing=None, only_core=False, only_center=False, mode='sparse', dtype='float64'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L673)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L673?message=Update%20Docs)]
</div>

  - `finite_difference_data`: `FiniteDifferenceData`
    > 
  - `npts`: `Any`
    > 
  - `mesh_spacing`: `Any`
    > 
  - `only_core`: `Any`
    > 
  - `only_center`: `Any`
    > 
  - `mode`: `Any`
    >


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.weights" class="docs-object-method">&nbsp;</a> 
```python
@property
weights(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L703)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L703?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.order" class="docs-object-method">&nbsp;</a> 
```python
@property
order(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L706)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L706?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.npts" class="docs-object-method">&nbsp;</a> 
```python
@property
npts(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L709)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L709?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.mesh_spacing" class="docs-object-method">&nbsp;</a> 
```python
@property
mesh_spacing(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L717)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L717?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.only_core" class="docs-object-method">&nbsp;</a> 
```python
@property
only_core(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L725)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L725?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.only_center" class="docs-object-method">&nbsp;</a> 
```python
@property
only_center(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L733)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L733?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.mode" class="docs-object-method">&nbsp;</a> 
```python
@property
mode(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L741)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L741?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.dtype" class="docs-object-method">&nbsp;</a> 
```python
@property
dtype(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L749)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L749?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.matrix" class="docs-object-method">&nbsp;</a> 
```python
@property
matrix(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L757)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L757?message=Update%20Docs)]
</div>


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.fd_matrix" class="docs-object-method">&nbsp;</a> 
```python
fd_matrix(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L764)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L764?message=Update%20Docs)]
</div>
Builds a 1D finite difference matrix for a set of boundary weights, central weights, and num of points
Will look like:
b1 b2 b3 ...
w1 w2 w3 ...
0  w1 w2 w3 ...
0  0  w1 w2 w3 ...
...
...
...
.... b3 b2 b1
  - `:returns`: `np.ndarray | sp.csr_matrix`
    > f
d
_
m
a
t
 </div>
</div>




## Examples
## <a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix">FiniteDifferenceMatrix</a>
Defines a matrix that can be applied to a regular grid of values to take a finite difference

### Properties and Methods
<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.__init__" class="docs-object-method">&nbsp;</a>
```python
__init__(self, finite_difference_data, npts=None, mesh_spacing=None, only_core=False, only_center=False, mode='sparse', dtype='float64'): 
```

- `finite_difference_data`: `FiniteDifferenceData`
    >No description...
- `npts`: `Any`
    >No description...
- `mesh_spacing`: `Any`
    >No description...
- `only_core`: `Any`
    >No description...
- `only_center`: `Any`
    >No description...
- `mode`: `Any`
    >No description...

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.weights" class="docs-object-method">&nbsp;</a>
```python
@property
weights(self): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.order" class="docs-object-method">&nbsp;</a>
```python
@property
order(self): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.npts" class="docs-object-method">&nbsp;</a>
```python
@property
npts(self): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.mesh_spacing" class="docs-object-method">&nbsp;</a>
```python
@property
mesh_spacing(self): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.only_core" class="docs-object-method">&nbsp;</a>
```python
@property
only_core(self): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.only_center" class="docs-object-method">&nbsp;</a>
```python
@property
only_center(self): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.mode" class="docs-object-method">&nbsp;</a>
```python
@property
mode(self): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.dtype" class="docs-object-method">&nbsp;</a>
```python
@property
dtype(self): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.matrix" class="docs-object-method">&nbsp;</a>
```python
@property
matrix(self): 
```

<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.fd_matrix" class="docs-object-method">&nbsp;</a>
```python
fd_matrix(self): 
```
Builds a 1D finite difference matrix for a set of boundary weights, central weights, and num of points
        Will look like:
            b1 b2 b3 ...
            w1 w2 w3 ...
            0  w1 w2 w3 ...
            0  0  w1 w2 w3 ...
                 ...
                 ...
                 ...
                    .... b3 b2 b1
- `:returns`: `np.ndarray | sp.csr_matrix`
    >fd_mat

### Examples


___

[Edit Examples](https://github.com/McCoyGroup/References/edit/gh-pages/Documentation/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md) or 
[Create New Examples](https://github.com/McCoyGroup/References/new/gh-pages/?filename=Documentation/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md) <br/>
[Edit Template](https://github.com/McCoyGroup/References/edit/gh-pages/Documentation/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md) or 
[Create New Template](https://github.com/McCoyGroup/References/new/gh-pages/?filename=Documentation/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md) <br/>
[Edit Docstrings](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction.py?message=Update%20Docs)






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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Zachary/Taylor/FiniteDifferenceFunction.py#L668?message=Update%20Docs)   
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