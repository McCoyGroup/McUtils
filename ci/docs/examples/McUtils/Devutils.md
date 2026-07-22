# LLM Examples

## Route options to the functions that accept them

```python
from McUtils.Devutils import OptionsSet

def optimize(*, method, tolerance=1e-8, max_iterations=100):
    return method, tolerance, max_iterations

options = OptionsSet(method="BFGS", tolerance=1e-10,
                     max_iterations=250, checkpoint="opt.json")
accepted, remaining = options.split(optimize)
print("optimizer options:", accepted)
print("workflow options:", remaining)
```

## Validate a nested configuration

```python
from McUtils.Devutils import Schema

schema = Schema(
    {"method": "str"},
    {"resources": {"cores": "int", "queue": {"type": "str",
                                                "enum": ["short", "long"]}}}
)
config = {"method": "CCSD(T)", "resources": {"cores": 16, "queue": "long"}}
assert schema.validate(config)
```

## Safely write and read JSON

```python
from McUtils.Devutils import write_json, read_json, file_hash

configuration = {"method": "B3LYP", "basis": "6-31G*", "charge": 0}
write_json("calculation.json", configuration, indent=2)
restored = read_json("calculation.json")
assert restored == configuration
print("configuration hash:", file_hash("calculation.json"))
```

## Use explicit default sentinels

```python
from McUtils.Devutils import default, is_default

def choose_backend(backend=default):
    if is_default(backend):
        backend = "numpy"
    return backend

print(choose_backend(), choose_backend("numba"))
```

## Capture output through a logger

```python
import sys
from McUtils.Devutils import Logger, StreamRedirect

logger = Logger(log_file="captured.log")
with logger.block(tag="capturing"):
    print("optimization started")
    ...
    print("energy = -76.2413")
```

## Hash a reproducible input directory

```python
from McUtils.Devutils import directory_hash, files_hash

input_hash = directory_hash("calculation", files=["input.gjf", "config.json"])
explicit_hash = files_hash(["calculation/input.gjf", "calculation/config.json"])
print("directory hash:", input_hash)
print("explicit hash:", explicit_hash)
```
