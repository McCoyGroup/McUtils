# <a id="McUtils.Numputils.AnalyticDerivs.rot_deriv">rot_deriv</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/AnalyticDerivs.py#L85)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/AnalyticDerivs.py#L85?message=Update%20Docs)]
</div>

```python
rot_deriv(angle, axis, dAngle, dAxis): 
```
Gives a rotational derivative w/r/t some unspecified coordinate
(you have to supply the chain rule terms)
Assumes that axis is a unit vector.
  - `angle`: `float`
    > angle for rotation
  - `axis`: `np.ndarray`
    > axis for rotation
  - `dAngle`: `float`
    > chain rule angle deriv.
  - `dAxis`: `np.ndarray`
    > chain rule axis deriv.
  - `:returns`: `np.ndarray`
    > d
e
r
i
v
a
t
i
v
e
s
 
o
f
 
t
h
e
 
r
o
t
a
t
i
o
n
 
m
a
t
r
i
c
e
s
 
w
i
t
h
 
r
e
s
p
e
c
t
 
t
o
 
b
o
t
h
 
t
h
e
 
a
n
g
l
e
 
a
n
d
 
t
h
e
 
a
x
i
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
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/examples/McUtils/Numputils/AnalyticDerivs/rot_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/examples/McUtils/Numputils/AnalyticDerivs/rot_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/ci/docs/McUtils/Numputils/AnalyticDerivs/rot_deriv.md)/[New](https://github.com/McCoyGroup/McUtils/new/master/?filename=ci/docs/templates/McUtils/Numputils/AnalyticDerivs/rot_deriv.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/AnalyticDerivs.py#L85?message=Update%20Docs)   
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