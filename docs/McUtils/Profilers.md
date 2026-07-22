# <a id="McUtils.Profilers">McUtils.Profilers</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Profilers/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/__init__.py#L1?message=Update%20Docs)]
</div>
    
Tools migrated from `Peeves` for profiling code

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[Timer](Profilers/Timer/Timer.md)   
</div>
   <div class="col" markdown="1">
[BlockProfiler](Profilers/Profiler/BlockProfiler.md)   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>





## Examples

**LLM Examples**

### Time a numerical block

```python
import numpy as np
from McUtils.Profilers import Timer
from McUtils.Numputils import vec_dots

vectors = np.random.default_rng(7).normal(size=(100_000, 3))
with Timer("100k vector norms", rounding=4):
    norms = np.sqrt(vec_dots(vectors, vectors))
print("mean norm:", norms.mean())
```

### Use a timer as a decorator

```python
import numpy as np
from McUtils.Profilers import Timer

@Timer("eigensystem", print_times=3)
def diagonalize(matrix):
    return np.linalg.eigh(matrix)

rng = np.random.default_rng(1)
matrix = rng.normal(size=(300, 300))
matrix = matrix + matrix.T
values, vectors = diagonalize(matrix)
```

### Profile a calculation block

```python
import numpy as np
from McUtils.Profilers import BlockProfiler

with BlockProfiler.profiler("matrix multiplication", mode="deterministic"):
    rng = np.random.default_rng(3)
    left = rng.normal(size=(500, 500))
    right = rng.normal(size=(500, 500))
    product = left @ right
```

### Record explicit laps

```python
import numpy as np
from McUtils.Profilers import Timer

timer = Timer("pipeline")
timer.start()
matrix = np.random.default_rng(2).normal(size=(500, 500))
timer.log()
values = np.linalg.eigvalsh(matrix + matrix.T)
timer.log()
elapsed = timer.stop()
print("lap count:", len(timer.laps), "total:", elapsed)
```

### Select a profiler backend dynamically

```python
from McUtils.Profilers import BlockProfiler

profiler = BlockProfiler.profiler(
    "interpolation workload",
    mode="deterministic",
    print_options={"sort_by": "cumulative"}
)
with profiler:
    values = [sum(i * j for j in range(100)) for i in range(1000)]
```

### Disable profiling without branching

```python
from McUtils.Profilers import BlockProfiler

profiling_enabled = False
with BlockProfiler.profiler("optional profile", mode="deterministic",
                            inactive=not profiling_enabled):
    result = sum(i * i for i in range(1_000_000))
print(result)
```







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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Profilers.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Profilers.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Profilers.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Profilers.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Profilers/__init__.py#L1?message=Update%20Docs)   
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