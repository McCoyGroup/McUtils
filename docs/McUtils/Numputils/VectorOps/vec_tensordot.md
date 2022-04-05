# <a id="McUtils.Numputils.VectorOps.vec_tensordot">vec_tensordot</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/Numputils/VectorOps.py#L342)]
</div>

```python
vec_tensordot(tensa, tensb, axes=2, shared=None): 
```
Defines a version of tensordot that uses matmul to operate over stacks of things
    Basically had to duplicate the code for regular tensordot but then change the final call
- `tensa`: `Any`
    >No description...
- `tensb`: `Any`
    >No description...
- `axes`: `Any`
    >No description...
- `shared`: `int | None`
    >the axes that should be treated as shared (for now just an int)
- `:returns`: `_`
    >No description... 



___

[Edit Examples](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Numputils/VectorOps/vec_tensordot.md) or 
[Create New Examples](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Numputils/VectorOps/vec_tensordot.md) <br/>
[Edit Template](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Numputils/VectorOps/vec_tensordot.md) or 
[Create New Template](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Numputils/VectorOps/vec_tensordot.md) <br/>
[Edit Docstrings](https://github.com/McCoyGroup/McUtils/edit/master/Numputils/VectorOps.py#L342?message=Update%20Docs)