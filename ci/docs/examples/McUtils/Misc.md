# `McUtils.Misc` examples

## Compile a symbolic numerical expression

```python
import numpy as np
from McUtils.Misc import Abstract

x, np_symbol = Abstract.vars("x", "np")
expression = Abstract.Lambda(x)(
    .5 * np_symbol.sum(x * x, axis=-1)
)
energy = expression.compile({"np": np})
points = np.array([[1., 2., 3.], [.5, .5, .5]])
assert np.allclose(energy(points), [7., .375])
```

## Write code that works with or without Numba

```python
import numpy as np
from McUtils.Misc import njit

@njit
def pairwise_distances(points):
    n = len(points)
    distances = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            distances[i, j] = np.sqrt(np.sum((points[i] - points[j])**2))
    return distances

print(pairwise_distances(np.eye(3)))
```

## Track modifications during debugging

```python
from types import SimpleNamespace
from McUtils.Misc import ModificationTracker
from McUtils.Scaffolding import Logger

state = SimpleNamespace(energy=-76.1, iteration=1)
logger = Logger()
tracked = ModificationTracker(state, logger=logger)
tracked.energy = -76.2
tracked.iteration += 1
print("updated state:", state)
```

## Construct and compile a symbolic polynomial

```python
import numpy as np
from McUtils.Misc import Abstract

x = Abstract.var("x")
polynomial = Abstract.Lambda(x)(3 * x**2 - 2 * x + 4)
function = polynomial.compile()
grid = np.linspace(-2, 2, 9)
print(function(grid))
```

## Build a symbolic NumPy reduction

```python
import numpy as np
from McUtils.Misc import Abstract

x, np_symbol = Abstract.vars("x", "np")
rms_expr = Abstract.Lambda(x)(np_symbol.sqrt(np_symbol.mean(x**2)))
rms = rms_expr.compile({"np": np})
print("RMS:", rms(np.array([1., -2., 3.])))
```

## Inspect whether Numba is available

```python
from McUtils.Misc.NumbaTools import NumbaState, load_numba

numba = load_numba()
if numba is None:
    print("Numba unavailable; decorators fall back to Python")
else:
    print("Numba version:", numba.__version__)
print("Numba state:", NumbaState)
```
