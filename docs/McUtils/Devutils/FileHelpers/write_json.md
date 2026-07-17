# <a id="McUtils.Devutils.FileHelpers.write_json">write_json</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Devutils/FileHelpers.py#L176)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L176?message=Update%20Docs)]
</div>

```python
write_json(file, data, writer=None, mode='w+', encoder=None, **opts): 
```
**LLM Docstring**

Serialize data to a file as JSON, separating `open` options from dumper options
and supporting a custom encoder class or default function.
  - `file`: `Any`
    > the file path or stream
  - `data`: `Any`
    > the data to serialize
  - `writer`: `Callable | None`
    > the JSON writer (defaults to `json.dump`)
  - `mode`: `str`
    > the open mode
  - `encoder`: `Any`
    > a JSON encoder class or default-serializer function
  - `opts`: `Any`
    > mixed `open` and dumper options
  - `:returns`: `_`
    > the writer's result











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Devutils/FileHelpers/write_json.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Devutils/FileHelpers/write_json.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Devutils/FileHelpers/write_json.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Devutils/FileHelpers/write_json.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Devutils/FileHelpers.py#L176?message=Update%20Docs)   
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