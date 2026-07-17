# <a id="McUtils.ExternalPrograms.ASE.ASECalculator">ASECalculator</a>
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE.py#L996)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE.py#L996?message=Update%20Docs)]
</div>

```python
ASECalculator(energy_evaluator, charge_evaluator=None, dipole_evaluator=None, analytic_derivative_order=None, charge_derivative_order=None, dipole_derivative_order=None, **kwargs): 
```
**LLM Docstring**

Build an ASE-compatible calculator that evaluates energies (and optionally
charges/dipoles) from the supplied McUtils evaluators.
  - `energy_evaluator`: `Callable`
    > the energy-evaluation callable
  - `charge_evaluator`: `Callable | None`
    > an optional charge evaluator
  - `dipole_evaluator`: `Callable | None`
    > an optional dipole evaluator
  - `analytic_derivative_order`: `int | None`
    > highest analytic energy-derivative order
  - `charge_derivative_order`: `int | None`
    > highest analytic charge-derivative order
  - `dipole_derivative_order`: `int | None`
    > highest analytic dipole-derivative order
  - `kwargs`: `Any`
    > extra options for the calculator
  - `:returns`: `ASETermCalculator`
    > the ASE calculator











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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ASE/ASECalculator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ASE/ASECalculator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ASE/ASECalculator.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ASE/ASECalculator.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE.py#L996?message=Update%20Docs)   
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