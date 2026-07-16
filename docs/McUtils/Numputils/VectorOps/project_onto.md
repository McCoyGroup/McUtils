# <a id="McUtils.Numputils.VectorOps.project_onto">project_onto</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/VectorOps.py#L2012)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L2012?message=Update%20Docs)]
</div>

```python
project_onto(vecs, basis, ndim=None, orthonormal=False, inverse=None, allow_pinv=False): 
```
**LLM Docstring**

Project vectors onto the span of a basis.
  - `vecs`: `np.ndarray`
    > the vectors to project
  - `basis`: `np.ndarray`
    > the basis to project onto
  - `ndim`: `int | None`
    > number of vector axes (inferred if omitted)
  - `orthonormal`: `bool`
    > whether the basis is orthonormal
  - `inverse`: `np.ndarray | None`
    > explicit basis inverse (optional)
  - `allow_pinv`: `bool`
    > use the pseudoinverse
  - `:returns`: `np.ndarray`
    > t
h
e
 
p
r
o
j
e
c
t
e
d
 
v
e
c
t
o
r
s











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/project_onto.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/project_onto.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/project_onto.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/project_onto.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/VectorOps.py#L2012?message=Update%20Docs)   
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