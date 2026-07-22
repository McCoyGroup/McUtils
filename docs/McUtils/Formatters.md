# <a id="McUtils.Formatters">McUtils.Formatters</a> 
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/__init__.py#L1)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/__init__.py#L1?message=Update%20Docs)]
</div>
    
Defines a set of formatting utilities

### Members
<div class="container alert alert-secondary bg-light">
  <div class="row">
   <div class="col" markdown="1">
[TemplateWriter](Formatters/TemplateWriter/TemplateWriter.md)   
</div>
   <div class="col" markdown="1">
[OptionalTemplate](Formatters/TemplateWriter/OptionalTemplate.md)   
</div>
   <div class="col" markdown="1">
[ObjectWalker](Formatters/TemplateEngine/ObjectWalker/ObjectWalker.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ObjectHandler](Formatters/TemplateEngine/ObjectWalker/ObjectHandler.md)   
</div>
   <div class="col" markdown="1">
[ObjectSpec](Formatters/TemplateEngine/ObjectWalker/ObjectSpec.md)   
</div>
   <div class="col" markdown="1">
[TemplateFormatter](Formatters/TemplateEngine/TemplateEngine/TemplateFormatter.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[FormatDirective](Formatters/TemplateEngine/TemplateEngine/FormatDirective.md)   
</div>
   <div class="col" markdown="1">
[TemplateFormatDirective](Formatters/TemplateEngine/TemplateEngine/TemplateFormatDirective.md)   
</div>
   <div class="col" markdown="1">
[TemplateOps](Formatters/TemplateEngine/TemplateEngine/TemplateOps.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[TemplateEngine](Formatters/TemplateEngine/TemplateEngine/TemplateEngine.md)   
</div>
   <div class="col" markdown="1">
[ResourceLocator](Formatters/TemplateEngine/TemplateEngine/ResourceLocator.md)   
</div>
   <div class="col" markdown="1">
[TemplateResourceExtractor](Formatters/TemplateEngine/TemplateEngine/TemplateResourceExtractor.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[TemplateWalker](Formatters/TemplateEngine/TemplateEngine/TemplateWalker.md)   
</div>
   <div class="col" markdown="1">
[TemplateHandler](Formatters/TemplateEngine/TemplateEngine/TemplateHandler.md)   
</div>
   <div class="col" markdown="1">
[ModuleTemplateHandler](Formatters/TemplateEngine/TemplateEngine/ModuleTemplateHandler.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ClassTemplateHandler](Formatters/TemplateEngine/TemplateEngine/ClassTemplateHandler.md)   
</div>
   <div class="col" markdown="1">
[FunctionTemplateHandler](Formatters/TemplateEngine/TemplateEngine/FunctionTemplateHandler.md)   
</div>
   <div class="col" markdown="1">
[MethodTemplateHandler](Formatters/TemplateEngine/TemplateEngine/MethodTemplateHandler.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[ObjectTemplateHandler](Formatters/TemplateEngine/TemplateEngine/ObjectTemplateHandler.md)   
</div>
   <div class="col" markdown="1">
[IndexTemplateHandler](Formatters/TemplateEngine/TemplateEngine/IndexTemplateHandler.md)   
</div>
   <div class="col" markdown="1">
[TemplateInterfaceEngine](Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceEngine.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[TemplateInterfaceFormatter](Formatters/TemplateEngine/TemplateEngine/TemplateInterfaceFormatter.md)   
</div>
   <div class="col" markdown="1">
[TeX](Formatters/TeXWriter/TeX.md)   
</div>
   <div class="col" markdown="1">
[TeXTranspiler](Formatters/TeXWriter/TeXTranspiler.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[StringMatcher](Formatters/FileMatcher/StringMatcher.md)   
</div>
   <div class="col" markdown="1">
[MatchList](Formatters/FileMatcher/MatchList.md)   
</div>
   <div class="col" markdown="1">
[FileMatcher](Formatters/FileMatcher/FileMatcher.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[TableFormatter](Formatters/TableFormatters/TableFormatter.md)   
</div>
   <div class="col" markdown="1">
[format_tensor_element_table](Formatters/Conveniences/format_tensor_element_table.md)   
</div>
   <div class="col" markdown="1">
[format_symmetric_tensor_elements](Formatters/Conveniences/format_symmetric_tensor_elements.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[format_mode_labels](Formatters/Conveniences/format_mode_labels.md)   
</div>
   <div class="col" markdown="1">
[format_zmatrix](Formatters/Conveniences/format_zmatrix.md)   
</div>
   <div class="col" markdown="1">
[format_state_vector_frequency_table](Formatters/Conveniences/format_state_vector_frequency_table.md)   
</div>
</div>
  <div class="row">
   <div class="col" markdown="1">
[format_radix_value](Formatters/Conveniences/format_radix_value.md)   
</div>
   <div class="col" markdown="1">
[format_elapsed_time](Formatters/Conveniences/format_elapsed_time.md)   
</div>
   <div class="col" markdown="1">
   
</div>
</div>
</div>





## Examples
**LLM Examples**

### Format a hierarchical results table

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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/__init__.py#L1?message=Update%20Docs)   
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