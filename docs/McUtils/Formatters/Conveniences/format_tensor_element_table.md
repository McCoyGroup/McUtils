# <a id="McUtils.Formatters.Conveniences.format_tensor_element_table">format_tensor_element_table</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Formatters/Conveniences.py#L16)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/Conveniences.py#L16?message=Update%20Docs)]
</div>

```python
format_tensor_element_table(inds, vals, headers=('Indices', 'Value'), format='{:8.3f}', column_join='|', index_format='{:>5.0f}', **etc): 
```
**LLM Docstring**

Combine transposed index arrays with one or more value columns and format them under spanning headers.
  - `inds`: `object`
    > index arrays identifying tensor elements
  - `vals`: `object`
    > values paired with the index tuples
  - `headers`: `object`
    > optional header rows
  - `format`: `object`
    > numeric value formatter or formatter sequence
  - `column_join`: `object`
    > separator or separator sequence between columns
  - `index_format`: `object`
    > formatter applied to tensor index columns
  - `etc`: `dict`
    > additional keyword options forwarded to the underlying formatter or operation
  - `:returns`: `str`
    > formatted text











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Formatters/Conveniences/format_tensor_element_table.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Formatters/Conveniences/format_tensor_element_table.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Formatters/Conveniences/format_tensor_element_table.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Formatters/Conveniences/format_tensor_element_table.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Formatters/Conveniences.py#L16?message=Update%20Docs)   
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