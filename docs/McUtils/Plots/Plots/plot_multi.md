# <a id="McUtils.Plots.Plots.plot_multi">plot_multi</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/Plots/Plots.py#L1970)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots.py#L1970?message=Update%20Docs)]
</div>

```python
plot_multi(*plot_specs: dict, figure=None, plot_type_styles=None, default_type='plot', x=None, y=None, z=None, func=None, common_settings=None, **global_settings): 
```
**LLM Docstring**

Build several plots onto a shared figure from a sequence of plot specs, layering
common settings, per-type styles, and global settings, and expanding any
list-valued `func` into multiple curves.
  - `plot_specs`: `Any`
    > the per-plot specification dicts
  - `figure`: `Any`
    > an existing figure to draw onto
  - `plot_type_styles`: `dict | None`
    > per-plot-type default styles
  - `default_type`: `str`
    > the default plot type
  - `x`: `Any`
    > shared x data
  - `y`: `Any`
    > shared y data
  - `z`: `Any`
    > shared z data
  - `func`: `Any`
    > shared function(s) to plot
  - `common_settings`: `dict | None`
    > settings shared across all plots
  - `global_settings`: `Any`
    > settings applied only to the first (figure-creating) plot
  - `:returns`: `Graphics`
    > the shared figure











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/Plots/Plots/plot_multi.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/Plots/Plots/plot_multi.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/Plots/Plots/plot_multi.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/Plots/Plots/plot_multi.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/Plots/Plots.py#L1970?message=Update%20Docs)   
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