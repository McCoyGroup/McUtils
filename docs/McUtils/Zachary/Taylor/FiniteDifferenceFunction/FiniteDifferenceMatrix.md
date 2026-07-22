## <a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix">FiniteDifferenceMatrix</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L815)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L815?message=Update%20Docs)]
</div>

Defines a matrix that can be applied to a regular grid of values to take a finite difference







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 
<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.__init__" class="docs-object-method">&nbsp;</a> 
```python
__init__(self, finite_difference_data, npts=None, mesh_spacing=None, only_core=False, only_center=False, mode='sparse', dtype='float64'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L820)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L820?message=Update%20Docs)]
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
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L850)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L850?message=Update%20Docs)]
</div>
**LLM Docstring**

The finite-difference weights backing the matrix.
  - `:returns`: `tuple`
    > the weights


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.order" class="docs-object-method">&nbsp;</a> 
```python
@property
order(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L861)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L861?message=Update%20Docs)]
</div>
**LLM Docstring**

The derivative order.
  - `:returns`: `int`
    > the order


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.npts" class="docs-object-method">&nbsp;</a> 
```python
@property
npts(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L872)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L872?message=Update%20Docs)]
</div>
**LLM Docstring**

The number of grid points the matrix spans. Setting it invalidates the cached
matrix.
  - `:returns`: `int`
    > the number of points


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.mesh_spacing" class="docs-object-method">&nbsp;</a> 
```python
@property
mesh_spacing(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L898)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L898?message=Update%20Docs)]
</div>
**LLM Docstring**

The grid spacing. Setting it invalidates the cached matrix.
  - `:returns`: `float`
    > the mesh spacing


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.only_core" class="docs-object-method">&nbsp;</a> 
```python
@property
only_core(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L922)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L922?message=Update%20Docs)]
</div>
**LLM Docstring**

Whether to build only the core (non-boundary) rows. Setting it invalidates the
cached matrix.
  - `:returns`: `bool`
    > the flag


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.only_center" class="docs-object-method">&nbsp;</a> 
```python
@property
only_center(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L948)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L948?message=Update%20Docs)]
</div>
**LLM Docstring**

Whether to build only the single centered row. Setting it invalidates the cached
matrix.
  - `:returns`: `bool`
    > the flag


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.mode" class="docs-object-method">&nbsp;</a> 
```python
@property
mode(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L974)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L974?message=Update%20Docs)]
</div>
**LLM Docstring**

The storage mode (`'dense'` or `'sparse'`). Setting it invalidates the cached
matrix.
  - `:returns`: `str`
    > the mode


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.dtype" class="docs-object-method">&nbsp;</a> 
```python
@property
dtype(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L1000)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L1000?message=Update%20Docs)]
</div>
**LLM Docstring**

The matrix dtype. Setting it invalidates the cached matrix.
  - `:returns`: `_`
    > the dtype


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.matrix" class="docs-object-method">&nbsp;</a> 
```python
@property
matrix(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L1022)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L1022?message=Update%20Docs)]
</div>
**LLM Docstring**

The finite-difference matrix (built and cached lazily).
  - `:returns`: `np.ndarray | sparse matrix`
    > the matrix


<a id="McUtils.Zachary.Taylor.FiniteDifferenceFunction.FiniteDifferenceMatrix.fd_matrix" class="docs-object-method">&nbsp;</a> 
```python
fd_matrix(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L1037)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.py#L1037?message=Update%20Docs)]
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
    > fd_mat
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Zachary/Taylor/FiniteDifferenceFunction/FiniteDifferenceMatrix.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Zachary/Taylor/FiniteDifferenceFunction.py#L815?message=Update%20Docs)   
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