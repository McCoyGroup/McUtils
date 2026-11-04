**LLM Examples**

### Format a hierarchical results table

<!-- readout(id="mcutils-formatters-1", isolated=True, display="both") -->
```python
from McUtils.Formatters import TableFormatter

results = {
    "water": {"HF": {"energy": -75.983}, "CCSD(T)": {"energy": -76.241}},
    "ammonia": {"HF": {"energy": -56.195}, "CCSD(T)": {"energy": -56.492}}
}
table = TableFormatter.format_tree(
    results, column_join=" | ",
    data_normalization_function=lambda values: values
)
print(table)
```

### Build a TeX equation

<!-- readout(id="mcutils-formatters-2", isolated=True, display="both") -->
```python
from McUtils.Formatters import TeX

f = TeX.Symbol(TeX.bold("F"))
l = TeX.Symbol(TeX.bold("L"))
omega = TeX.Symbol("omega")
equation = (f * l).Equals(l * omega**2)
block = TeX.Equation(equation, label="eq:normal-modes")
print(block.format_tex())
```

### Render a mixed TeX table

<!-- readout(id="mcutils-formatters-3", isolated=True, display="both") -->
```python
from McUtils.Formatters import TeX

headers = ["Method", "Energy / $E_h$", "Basis"]
rows = [["HF", -75.983, "cc-pVDZ"],
        ["MP2", -76.230, "cc-pVDZ"],
        ["CCSD(T)", -76.241, "cc-pVTZ"]]
table = TeX.Table(headers, rows, caption="Electronic energies",
                  label="tab:energies", number_format="{:.6f}")
print(table.format_tex())
```

### Render a directory of templates

```python
from McUtils.Formatters import TemplateWriter

writer = TemplateWriter(
    template_dir="templates/gaussian",
    output_dir="jobs/water"
)
writer.write_all({"method": "B3LYP", "basis": "6-31G*", "charge": 0})
```

### Select files with composable matchers

<!-- readout(id="mcutils-formatters-5", isolated=True, display="both") -->
```python
from pathlib import Path
from McUtils.Formatters import FileMatcher, StringMatcher

matcher = FileMatcher([StringMatcher([".log", ".fchk"])], use_basename=True)
files = [path for path in Path("calculations").rglob("*")
         if path.is_file() and matcher.matches(str(path))]
print("matched outputs:", files)
```

### Flatten a TeX project

```python
from McUtils.Formatters import TeXTranspiler

transpiler = TeXTranspiler(
    "paper/main.tex",
    figure_renaming_function=TeXTranspiler.figure_counter()
)
body, auxiliary = transpiler.create_flat_tex(include_aux=True)
print("flattened lines:", len(body.splitlines()))
print("auxiliary files:", auxiliary.keys())
```
