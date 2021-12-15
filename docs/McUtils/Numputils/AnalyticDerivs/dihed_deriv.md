# <a id="McUtils.Numputils.AnalyticDerivs.dihed_deriv">dihed_deriv</a>

```python
dihed_deriv(coords, i, j, k, l, order=1, zero_thresh=None, zero_point_step_size=0.0001): 
```
Gives the derivative of the dihedral between i, j, k, and l with respect to the Cartesians
    Currently gives what are sometimes called the `psi` angles.
    Can also support more traditional `phi` angles by using a different angle ordering
- `coords`: `np.ndarray`
    >No description...
- `i`: `int | Iterable[int]`
    >No description...
- `j`: `int | Iterable[int]`
    >No description...
- `k`: `int | Iterable[int]`
    >No description...
- `l`: `int | Iterable[int]`
    >No description...
- `:returns`: `np.ndarray`
    >derivatives of the dihedral with respect to atoms i, j, k, and l 




___

[Edit Examples](https://github.com/McCoyGroup/McUtils/edit/edit/ci/examples/ci/docs/McUtils/Numputils/AnalyticDerivs/dihed_deriv.md) or 
[Create New Examples](https://github.com/McCoyGroup/McUtils/new/edit/?filename=ci/examples/ci/docs/McUtils/Numputils/AnalyticDerivs/dihed_deriv.md) <br/>
[Edit Template](https://github.com/McCoyGroup/McUtils/edit/edit/ci/docs/ci/docs/McUtils/Numputils/AnalyticDerivs/dihed_deriv.md) or 
[Create New Template](https://github.com/McCoyGroup/McUtils/new/edit/?filename=ci/docs/templates/ci/docs/McUtils/Numputils/AnalyticDerivs/dihed_deriv.md) <br/>
[Edit Docstrings](https://github.com/McCoyGroup/McUtils/edit/edit/McUtils/Numputils/AnalyticDerivs.py?message=Update%20Docs)