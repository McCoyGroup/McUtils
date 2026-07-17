# <a id="McUtils.Devutils.core.destructure_option_spec">destructure_option_spec</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/core.py#L253)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/core.py#L253?message=Update%20Docs)]
</div>

```python
destructure_option_spec(spec, allow_enums=True, method_key='method'): 
```
**LLM Docstring**

Split an option specification into a `(method, options)` pair, accepting bare
values/callables, enum members, dicts (with a method key), and `(method, opts)`
tuples.
  - `spec`: `Any`
    > the option specification
  - `allow_enums`: `bool`
    > treat enum members as methods
  - `method_key`: `str`
    > the dict key holding the method
  - `:returns`: `tuple`
    > `(method, options)` (both `None` if it can't be destructured)











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/core/destructure_option_spec.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/core/destructure_option_spec.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/core/destructure_option_spec.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/core/destructure_option_spec.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/core.py#L253?message=Update%20Docs)   
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