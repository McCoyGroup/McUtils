# <a id="McUtils.Devutils.core.is_interface_like">is_interface_like</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/core.py#L151)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/core.py#L151?message=Update%20Docs)]
</div>

```python
is_interface_like(obj, interface_types, exlusion_types, implementation_attrs): 
```
**LLM Docstring**

General duck-typing test: an object qualifies if it isn't an excluded type and is
either an instance of one of the interface types or has all of the required
implementation attributes.
  - `obj`: `Any`
    > the object to test
  - `interface_types`: `Any`
    > the accepted types (or `None`)
  - `exlusion_types`: `Any`
    > types to reject (or `None`)
  - `implementation_attrs`: `Any`
    > attributes the object must expose (or `None`)
  - `:returns`: `bool`
    > whether the object matches the interface











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/core/is_interface_like.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/core/is_interface_like.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/core/is_interface_like.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/core/is_interface_like.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/core.py#L151?message=Update%20Docs)   
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