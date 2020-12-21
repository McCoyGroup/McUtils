## <a id="McUtils.McUtils.Zachary.Surfaces.BaseSurface.InterpolatedSurface">InterpolatedSurface</a>
A surface that operates by doing an interpolation of passed mesh data

### Properties and Methods
<a id="McUtils.McUtils.Zachary.Surfaces.BaseSurface.InterpolatedSurface.__init__" class="docs-object-method">&nbsp;</a>
```python
__init__(self, xdata, ydata=None, dimension=None, **opts): 
```

<a id="McUtils.McUtils.Zachary.Surfaces.BaseSurface.InterpolatedSurface.evaluate" class="docs-object-method">&nbsp;</a>
```python
evaluate(self, points, **kwargs): 
```
We delegate all the dirty work to the Interpolator so hopefully that's working...
- `points`: `Any`
    >No description...
- `kwargs`: `Any`
    >No description...
- `:returns`: `_`
    >No description...

<a id="McUtils.McUtils.Zachary.Surfaces.BaseSurface.InterpolatedSurface.minimize" class="docs-object-method">&nbsp;</a>
```python
minimize(self, initial_guess=None, function_options=None, **opts): 
```

### Examples