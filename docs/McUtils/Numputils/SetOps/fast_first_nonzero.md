# <a id="McUtils.Numputils.SetOps.fast_first_nonzero">fast_first_nonzero</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/SetOps.py#L978)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/SetOps.py#L978?message=Update%20Docs)]
</div>

```python
fast_first_nonzero(arr, axis=-1): 
```
**LLM Docstring**

Find, for each row, the index of the first nonzero entry along an axis (or
`-1` if the row is all zeros).

Uses a byte-view `argmax` trick for speed, so the input must be an integer
array.
  - `arr`: `np.ndarray`
    > the integer array to scan
  - `axis`: `int`
    > the axis to scan along
  - `:returns`: `np.ndarray`
    > t
h
e
 
f
i
r
s
t
-
n
o
n
z
e
r
o
 
i
n
d
e
x
 
p
e
r
 
r
o
w
 
(
`
-
1
`
 
w
h
e
r
e
 
n
o
n
e
)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/SetOps/fast_first_nonzero.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/SetOps/fast_first_nonzero.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/SetOps/fast_first_nonzero.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/SetOps/fast_first_nonzero.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/SetOps.py#L978?message=Update%20Docs)   
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