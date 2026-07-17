# <a id="McUtils.ExternalPrograms.Pysisyphus.run_pysisyphus">run_pysisyphus</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/Pysisyphus.py#L1151)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Pysisyphus.py#L1151?message=Update%20Docs)]
</div>

```python
run_pysisyphus(energy_evaluator, method, optimizer=None, optimizer_settings=None, max_cycles=None, max_step=None, max_displacement=None, thresh=None, tol=None, use_max_for_error=True, log_file=None, out_dir=None, return_logs=True, patch_logging=True, logger=None, ignore_zero_steps=True, **kwargs): 
```
**LLM Docstring**

Run a full Pysisyphus optimization: resolve the method and optimizer, translate
the McUtils-style convergence/step settings into Pysisyphus options, run the
optimization (with logging patched and a symmetrized-eigh guard), and collect the
output logs.
  - `energy_evaluator`: `Callable`
    > the energy-evaluation callable
  - `method`: `str`
    > the method name (e.g. `'neb'`, `'ts'`, `'optimize'`)
  - `optimizer`: `str | Callable | None`
    > the optimizer name/callable (default chosen from the method)
  - `optimizer_settings`: `dict | None`
    > extra optimizer settings
  - `max_cycles`: `int | None`
    > the maximum optimization cycles
  - `max_step`: `float | None`
    > the maximum step size
  - `max_displacement`: `float | None`
    > an alias for `max_step`
  - `thresh`: `Any`
    > an explicit Pysisyphus convergence threshold preset
  - `tol`: `float | None`
    > the RMS-force convergence tolerance
  - `use_max_for_error`: `bool`
    > converge on the max force rather than the RMS force
  - `log_file`: `Any`
    > a log file
  - `out_dir`: `str | None`
    > the working/output directory
  - `return_logs`: `bool`
    > read and return the output-directory logs
  - `patch_logging`: `bool`
    > patch Pysisyphus logging first
  - `logger`: `Any`
    > a logger to use
  - `ignore_zero_steps`: `bool`
    > swallow Pysisyphus's zero-step-length termination
  - `kwargs`: `Any`
    > extra options forwarded to the method resolver
  - `:returns`: `tuple`
    > `(generator, optimizer, logs)`











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/Pysisyphus/run_pysisyphus.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/Pysisyphus/run_pysisyphus.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/Pysisyphus/run_pysisyphus.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/Pysisyphus/run_pysisyphus.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/Pysisyphus.py#L1151?message=Update%20Docs)   
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