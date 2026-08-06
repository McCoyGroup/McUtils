# <a id="McUtils.Scaffolding.Serializers.unflatten_tree">unflatten_tree</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Scaffolding/Serializers.py#L2327)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L2327?message=Update%20Docs)]
</div>

```python
unflatten_tree(serial_tree, unprep_tree=True, max_leaf_elements=None, block_pointers=None, prefix_filter=None, jump_table=None, record=None): 
```
Replay traversal markers and per-key shape/value pointers to rebuild
the nested tree and restore list/`None` sentinels.

If `jump_table` and `record` are both given, resumes the walk directly
at that record's span instead of starting from the beginning -- no
need to replay everything before it.
  - `serial_tree`: `Any`
    > flat-tree metadata and arrays. NOT mutated (key_map
                    is read, not popped), so this can be called
                    repeatedly against the same loaded data.
  - `unprep_tree`: `Any`
    > whether numbered list dictionaries should be restored
  - `jump_table`: `Any`
    > optional dict from build_jump_table
  - `record`: `Any`
    > optional path string to jump to (requires jump_table)
  - `:returns`: `_`
    > the reconstructed nested dict











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Scaffolding/Serializers/unflatten_tree.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Scaffolding/Serializers/unflatten_tree.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Scaffolding/Serializers/unflatten_tree.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Scaffolding/Serializers/unflatten_tree.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Scaffolding/Serializers.py#L2327?message=Update%20Docs)   
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