# <a id="McUtils.Numputils.Serialization.save_nptar">save_nptar</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Numputils/Serialization.py#L289)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization.py#L289?message=Update%20Docs)]
</div>

```python
save_nptar(file, *args, **kwds) -> 'None': 
```
Save arrays into an uncompressed tar archive of `.npy` members, ready
for memmapped reading via `load_nptar`. Mirrors `np.savez`'s calling
convention: positional args are auto-named 'arr_0', 'arr_1', ...;
keyword args use the given name.

    save_nptar("data.nptar", a=arr1, b=arr2)
    save_nptar("data.nptar", arr1, arr2)   # -> "arr_0", "arr_1"

The tar is written uncompressed and members are NOT padded/aligned
beyond tar's standard 512-byte block boundaries (which `load_nptar`
accounts for via `TarInfo.offset_data`), so every member stays
memmap-able.












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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/Serialization/save_nptar.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/Serialization/save_nptar.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/Serialization/save_nptar.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/Serialization/save_nptar.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Numputils/Serialization.py#L289?message=Update%20Docs)   
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