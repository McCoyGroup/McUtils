## <a id="McUtils.ExternalPrograms.ASE.ASEMolecule">ASEMolecule</a> 

<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE.py#L341)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE.py#L341?message=Update%20Docs)]
</div>

A simple interchange format for ASE molecules







<div class="collapsible-section">
 <div class="collapsible-section collapsible-section-header" markdown="1">
## <a class="collapse-link" data-toggle="collapse" href="#methods" markdown="1"> Methods and Properties</a> <a class="float-right" data-toggle="collapse" href="#methods"><i class="fa fa-chevron-down"></i></a>
 </div>
 <div class="collapsible-section collapsible-section-body collapse show" id="methods" markdown="1">
 ```python
default_optimizer: str
convergence_criterion: float
max_steps: int
default_mep: str
```
<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.atoms" class="docs-object-method">&nbsp;</a> 
```python
@property
atoms(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L346)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L346?message=Update%20Docs)]
</div>
**LLM Docstring**

The element symbols of the atoms.
  - `:returns`: `Sequence[str]`
    > the atom symbols


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.coords" class="docs-object-method">&nbsp;</a> 
```python
@property
coords(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L357)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L357?message=Update%20Docs)]
</div>
**LLM Docstring**

The atomic Cartesian coordinates.
  - `:returns`: `np.ndarray`
    > the coordinates


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.charges" class="docs-object-method">&nbsp;</a> 
```python
@property
charges(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L368)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L368?message=Update%20Docs)]
</div>
**LLM Docstring**

The per-atom charges.
  - `:returns`: `np.ndarray`
    > the charges


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.meta" class="docs-object-method">&nbsp;</a> 
```python
@property
meta(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L379)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L379?message=Update%20Docs)]
</div>
**LLM Docstring**

The ASE `Atoms.info` metadata dict.
  - `:returns`: `dict`
    > the metadata


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.copy" class="docs-object-method">&nbsp;</a> 
```python
copy(self): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L391)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L391?message=Update%20Docs)]
</div>
**LLM Docstring**

Return a copy of this molecule, carrying over the calculator and charge.
  - `:returns`: `ASEMolecule`
    > the copied molecule


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.from_atoms" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_atoms(cls, atoms, calculator=None, charge=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L405)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L405?message=Update%20Docs)]
</div>
**LLM Docstring**

Wrap an ASE `Atoms` object, optionally attaching a calculator and charge.
  - `atoms`: `Any`
    > the ASE atoms object
  - `calculator`: `Any`
    > the ASE calculator to attach
  - `charge`: `int | None`
    > the molecular charge
  - `:returns`: `ASEMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.from_coords" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_coords(cls, atoms, coords, charge=None, spin=None, info=None, calculator=None, **etc): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L425)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L425?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `ASEMolecule` from atoms and coordinates, recording charge/spin in the
ASE `info` dict and optionally attaching a calculator.
  - `atoms`: `Sequence[str]`
    > the element symbols
  - `coords`: `np.ndarray`
    > the Cartesian coordinates
  - `charge`: `int | None`
    > the molecular charge
  - `spin`: `int | None`
    > the spin
  - `info`: `dict | None`
    > an initial ASE `info` dict
  - `calculator`: `Any`
    > the ASE calculator to attach
  - `etc`: `Any`
    > extra arguments for the ASE `Atoms` constructor
  - `:returns`: `ASEMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.from_mol" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
from_mol(cls, mol, coord_unit='Angstroms', calculator=None, calculator_options=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L465)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L465?message=Update%20Docs)]
</div>
**LLM Docstring**

Build an `ASEMolecule` from a generic molecule object, converting coordinates to
Angstroms and deriving an ASE calculator from the molecule's energy evaluator
when none is given.
  - `mol`: `Any`
    > the source molecule
  - `coord_unit`: `str`
    > the source coordinate unit
  - `calculator`: `Any`
    > an explicit ASE calculator
  - `calculator_options`: `dict | None`
    > options for building the calculator from the evaluator
  - `:returns`: `ASEMolecule`
    > the wrapped molecule


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.calculate_props" class="docs-object-method">&nbsp;</a> 
```python
calculate_props(self, props, geoms=None, calc=None, extra_calcs=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L524)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L524?message=Update%20Docs)]
</div>
**LLM Docstring**

Evaluate the requested ASE calculator properties for the current geometry, or
for each geometry in a batch, optionally augmenting them with extra computed
values.
  - `props`: `Sequence[str]`
    > the property names to compute
  - `geoms`: `np.ndarray | None`
    > a batch of geometries (or `None` for the current one)
  - `calc`: `Any`
    > the calculator to use (defaults to the attached one)
  - `extra_calcs`: `Callable | None`
    > a callable returning extra properties per structure
  - `:returns`: `dict`
    > the property values (batched to match `geoms`)


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.calculate_energy" class="docs-object-method">&nbsp;</a> 
```python
calculate_energy(self, geoms=None, order=None, calc=None, hessian_func_attr='get_hessian'): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L595)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L595?message=Update%20Docs)]
</div>
**LLM Docstring**

Compute the energy (and optionally the gradient and Hessian) at the current
geometry or over a batch, via the ASE calculator.

Order `0` returns just the energy; order `1` adds the gradient (negated forces);
order `2` additionally requires the calculator to expose a Hessian.
  - `geoms`: `np.ndarray | None`
    > a batch of geometries (or `None` for the current one)
  - `order`: `int | None`
    > the derivative order (`None`/`0`=energy, `1`=gradient, `2`=Hessian)
  - `calc`: `Any`
    > the calculator to use
  - `hessian_func_attr`: `str`
    > the calculator attribute providing the Hessian
  - `:returns`: `float | np.ndarray | tuple`
    > the energy, or a tuple of `(energy, gradient[, hessian])`


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.lookup_optimizer_type" class="docs-object-method">&nbsp;</a> 
```python
@classmethod
lookup_optimizer_type(cls, method): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/classmethod.py#L653)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/classmethod.py#L653?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve an ASE optimizer name to its optimizer class.
  - `method`: `str | type`
    > the optimizer name (`'bfgs'`, `'lbfgs'`, ...) or a class
  - `:returns`: `type`
    > the optimizer class


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.resolve_optimizer" class="docs-object-method">&nbsp;</a> 
```python
resolve_optimizer(self, method): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L680)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L680?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve an optimizer specification to an ASE optimizer class, defaulting to the
class default when none is given.
  - `method`: `str | type | None`
    > the optimizer name/class (or `None` for the default)
  - `:returns`: `type`
    > the optimizer class


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.optimize_structure" class="docs-object-method">&nbsp;</a> 
```python
optimize_structure(self, geoms=None, calc=None, quiet=True, logfile=None, logger=None, fmax=None, steps=None, method=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L723)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L723?message=Update%20Docs)]
</div>
**LLM Docstring**

Optimize the current geometry (or each geometry in a batch) with an ASE
optimizer, returning the optimizer status and optimized coordinates.
  - `geoms`: `np.ndarray | None`
    > a batch of geometries (or `None` for the current one)
  - `calc`: `Any`
    > the calculator to use
  - `quiet`: `bool`
    > suppress optimizer output
  - `logfile`: `Any`
    > an explicit log file/stream
  - `logger`: `Any`
    > a logger to log through
  - `fmax`: `float | None`
    > the force convergence threshold
  - `steps`: `int | None`
    > the maximum optimization steps
  - `method`: `str | type | None`
    > the optimizer name/class
  - `opts`: `Any`
    > extra optimizer options
  - `:returns`: `tuple`
    > `(status, optimized_coords, extra)`


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.prep_trajectory_images" class="docs-object-method">&nbsp;</a> 
```python
prep_trajectory_images(self, geoms, mol=None, calc=None): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L800)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L800?message=Update%20Docs)]
</div>
**LLM Docstring**

Normalize a set of geometries into a list of `ASEMolecule` images, wrapping raw
ASE atoms or coordinate arrays and attaching the calculator as needed.
  - `geoms`: `Sequence`
    > the geometries (ASE atoms, molecules, or coordinate arrays)
  - `mol`: `ASEMolecule | None`
    > the reference molecule (defaults to this one)
  - `calc`: `Any`
    > the calculator to attach
  - `:returns`: `list[ASEMolecule]`
    > the image molecules


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.resolve_trajectory_method" class="docs-object-method">&nbsp;</a> 
```python
resolve_trajectory_method(self, method, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L838)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L838?message=Update%20Docs)]
</div>
**LLM Docstring**

Resolve a minimum-energy-path method name to its class (`'neb'`, `'dimer'`, or an
`ase.mep` attribute).
  - `method`: `str | type | None`
    > the method name/class
  - `opts`: `Any`
    > unused extra options
  - `:returns`: `type`
    > the trajectory method class


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.prep_trajectory_type" class="docs-object-method">&nbsp;</a> 
```python
prep_trajectory_type(self, geoms, method, calc=None, in_place=False, optimizer_method=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L865)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L865?message=Update%20Docs)]
</div>
**LLM Docstring**

Build the trajectory object for a path method from a set of geometries, either
via the method's `from_images` constructor or by preparing image atoms and
handing them to the method.
  - `geoms`: `Sequence`
    > the geometries along the path
  - `method`: `str | type | dict`
    > the path method (name, class, or options dict)
  - `calc`: `Any`
    > the calculator to attach
  - `in_place`: `bool`
    > modify the images in place rather than copying
  - `optimizer_method`: `str | None`
    > an optimizer method to record in the options
  - `opts`: `Any`
    > extra options for the method
  - `:returns`: `tuple`
    > `(trajectory, images)`


<a id="McUtils.ExternalPrograms.ASE.ASEMolecule.optimize_trajectory" class="docs-object-method">&nbsp;</a> 
```python
optimize_trajectory(self, geoms, method, calc=None, quiet=True, logfile=None, logger=None, fmax=None, tol=None, steps=None, optimizer=None, optimizer_method=None, in_place=False, return_coords=True, optimizer_settings=None, **opts): 
```
<div class="docs-source-link" markdown="1">
[[source](https://github.com/McCoyGroup/McUtils/blob/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L912)/
[edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE/ASEMolecule.py#L912?message=Update%20Docs)]
</div>
**LLM Docstring**

Optimize a reaction path / minimum-energy-path trajectory (NEB, dimer, etc.),
returning the optimizer status and the optimized images (or their coordinates).
  - `geoms`: `Sequence`
    > the geometries along the path
  - `method`: `str | type | dict`
    > the path method
  - `calc`: `Any`
    > the calculator to attach
  - `quiet`: `bool`
    > suppress output
  - `logfile`: `Any`
    > an explicit log file/stream
  - `logger`: `Any`
    > a logger to log through
  - `fmax`: `float | None`
    > the force convergence threshold
  - `tol`: `float | None`
    > an alias for `fmax`
  - `steps`: `int | None`
    > the maximum optimization steps
  - `optimizer`: `str | type | None`
    > the optimizer name/class
  - `optimizer_method`: `str | None`
    > an optimizer method for the trajectory builder
  - `in_place`: `bool`
    > modify images in place
  - `return_coords`: `bool`
    > return image coordinates rather than image objects
  - `optimizer_settings`: `dict | None`
    > extra optimizer settings
  - `opts`: `Any`
    > extra options
  - `:returns`: `tuple`
    > `(status, images_or_coords, extra)`
 </div>
</div>












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
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/examples/McUtils/ExternalPrograms/ASE/ASEMolecule.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/examples/McUtils/ExternalPrograms/ASE/ASEMolecule.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/gh-pages/ci/docs/McUtils/ExternalPrograms/ASE/ASEMolecule.md)/[New](https://github.com/McCoyGroup/McUtils/new/gh-pages/?filename=ci/docs/templates/McUtils/ExternalPrograms/ASE/ASEMolecule.md)   
</div>
   <div class="col" markdown="1">
[Edit](https://github.com/McCoyGroup/McUtils/edit/master/McUtils/ExternalPrograms/ASE.py#L341?message=Update%20Docs)   
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