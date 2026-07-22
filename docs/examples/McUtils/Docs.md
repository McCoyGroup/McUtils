**LLM Examples**

### Display rich API documentation in Jupyter

```python
from McUtils.Docs import jdoc
from McUtils.Zachary import FiniteDifferenceDerivative

documentation = jdoc(
    FiniteDifferenceDerivative,
    max_depth=2,
    verbose=False
)
documentation.display()
```

### Extract examples from a test module

```python
from McUtils.Docs import ExamplesParser

examples = ExamplesParser.from_file("ci/tests/ZacharyTests.py")
names = list(examples.functions)
finite_difference_examples = [name for name in names if "Deriv" in name]
print("all documented functions:", len(names))
print("finite-difference examples:", finite_difference_examples)
```

### Build package stubs and summaries

```python
from McUtils.Docs import StubSummaryBuilder

builder = StubSummaryBuilder(
    root_src_dir="McUtils",
    out_dir="stubs"
)
summary = builder.generate_all("McUtils")
print("stub bytes:", summary["stub_size"])
print("summary bytes:", summary["summary_size"])
```

### Render static HTML documentation

```python
from McUtils.Docs import static_doc
from McUtils.Combinatorics import UniquePermutations

html = static_doc(
    UniquePermutations, max_depth=2,
    title="Unique permutation API", return_string=True
)
print("generated HTML characters:", len(html))
```

### Walk an object hierarchy

```python
from McUtils.Docs import DocWalker
from McUtils import Numputils

walker = DocWalker(description="Numerical utility API")
documentation = walker.visit_root(Numputils, max_depth=1)
print(documentation)
```

### Build a documentation site

```python
from McUtils.Docs import DocBuilder

builder = DocBuilder(
    root=".", target="build/docs", readme="README.md",
    packages=[{"id": "McUtils", "tests_root": "ci/tests"}],
    config={"title": "McUtils API", "path": "McUtils"}
)
builder.build()
```
