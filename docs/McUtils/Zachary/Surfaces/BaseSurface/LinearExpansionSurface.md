## <a id="McUtils.Zachary.Surfaces.BaseSurface.LinearExpansionSurface">LinearExpansionSurface</a>
A surface with an evaluator built off of an expansion in some user specified basis

### Properties and Methods
<a id="McUtils.Zachary.Surfaces.BaseSurface.LinearExpansionSurface.__init__" class="docs-object-method">&nbsp;</a>
```python
__init__(self, coefficients, basis=None, dimension=None): 
```

- `coefficients`: `np.ndarray`
    >the expansion coefficients in the basis
- `basis`: `Iterable[function] | None`
    >a basis of functions to use (defaults to power series)

<a id="McUtils.Zachary.Surfaces.BaseSurface.LinearExpansionSurface.evaluate" class="docs-object-method">&nbsp;</a>
```python
evaluate(self, points, **kwargs): 
```
First we just apply the basis to the gridpoints, then we dot this into the coeffs
- `points`: `Any`
    >No description...
- `kwargs`: `Any`
    >No description...
- `:returns`: `_`
    >No description...





___

[Edit Examples](https://github.com/McCoyGroup/McUtils/edit/edit/ci/examples/ci/docs/McUtils/Zachary/Surfaces/BaseSurface/LinearExpansionSurface.md) or 
[Create New Examples](https://github.com/McCoyGroup/McUtils/new/edit/?filename=ci/examples/ci/docs/McUtils/Zachary/Surfaces/BaseSurface/LinearExpansionSurface.md) <br/>
[Edit Template](https://github.com/McCoyGroup/McUtils/edit/edit/ci/docs/ci/docs/McUtils/Zachary/Surfaces/BaseSurface/LinearExpansionSurface.md) or 
[Create New Template](https://github.com/McCoyGroup/McUtils/new/edit/?filename=ci/docs/templates/ci/docs/McUtils/Zachary/Surfaces/BaseSurface/LinearExpansionSurface.md) <br/>
[Edit Docstrings](https://github.com/McCoyGroup/McUtils/edit/edit/McUtils/Zachary/Surfaces/BaseSurface.py?message=Update%20Docs)