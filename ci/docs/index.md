# McUtils [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mccoygroup/binder-mcutils/master?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252Fmccoygroup%252FMcUtils%26urlpath%3Dlab%252Ftree%252FMcUtils%252Fbinder%252Findex.ipynb%26branch%3Dmaster)

McUtils is a set of utilities written by the McCoy group for the McCoy group to handle common things we do, like pulling data from electronic structure calculations, doing unit conversions, interpolating functions, making attractive plots, getting finite difference derivatives, performing fast, vectorized operations, etc.

We're working on [documenting the package](https://mccoygroup.github.io/References/Documentation/McUtils.html), but writing good documentation takes more time than writing good code.
Docs for the actively edited, unstable branch can be found [here](https://mccoygroup.github.io/McUtils).

McUtils is a suite of mostly independent Python packages developed by the
[McCoy Group](https://mccoygroup.github.io/) to support scientific computing,
computational chemistry, and research-software development. It grew out of
repeated needs across the group's projects: extracting data from electronic
structure calculations, converting molecular coordinate systems, performing
vectorized numerical operations, differentiating and interpolating functions,
building plots and notebook interfaces, and managing reproducible calculations.

The packages share a namespace and occasionally build on one another—especially
on `Numputils` and `Devutils`—but most can be used independently. McUtils also
provides much of the lower-level infrastructure used by
[`Psience`](https://github.com/McCoyGroup/Psience).

### Installation & Requirements

The easiest way to install is via `pip`, as

```lang-shell
pip install mccoygroup-mcutils
```

This should install all dependencies. 
The major requirement is that Python 3.9+ is required due to use of features in the `types` module.
For safety, it is best to install this in a [virtual environment](https://docs.python.org/3.8/tutorial/venv.html), which we can make like

```lang-shell
python3.9 -m pip venv mcenv
```

and activate like

```lang-shell
. mcenv/bin/activate
```

the most up-to-date development version can be installed with

```bash
python -m pip install git+https://github.com/McCoyGroup/McUtils.git
```

or to use it in a [container](https://www.docker.com/) or [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) or some other place where we can control the environment.

The core required dependencies are `numpy`, `scipy`, `h5py`, `numba`, and `matplotlib`.

Some integrations have additional dependencies, mainly `jupyter`, `ipywidgets`,
`rdkit`, `ase`, and `mpi4py`

#### Jupyter Integrations

If you want to get all of the nice `JHTML` features for working in Jupyter, you'll then need to run

```python
from McUtils.Jupyter import JHTML
JHTML.load()
```

and then reload the browser window when prompted.

## Package guide

### Scientific and numerical tools

#### [`McUtils.Numputils`](https://mccoygroup.github.io/McUtils/McUtils/Numputils.html)

`Numputils` collects low-level, reusable numerical operations that are awkward
to express efficiently with NumPy alone. It is the numerical foundation for
many of the other McUtils packages.

Key functionality includes vector and coordinate operations; molecular geometry
calculations; Euler angles, rotation matrices, and affine transformations;
coordinate frames and embedding; sparse arrays and set operations; tensor
derivative transformations; numerical optimization; permutation operations; and
Lebedev quadrature grids for spheres and unions of spheres.

```python
import numpy as np
from McUtils.Numputils import vec_crosses, vec_dots, vec_norms, vec_normalize, pts_angles

# Build a local frame from three atoms in a molecular geometry.
oxygen, hydrogen_1, hydrogen_2 = np.array([
    [0.000, 0.000, 0.000], [0.958, 0.000, 0.000], [-0.240, 0.927, 0.000]
])
# direct vectorized embedding calculations
oh_1, oh_2 = hydrogen_1 - oxygen, hydrogen_2 - oxygen
normal = vec_crosses(oh_1, oh_2)
angle = np.arccos(vec_dots(oh_1, oh_2) / (vec_norms(oh_1) * vec_norms(oh_2)))
angle = np.degrees(angle)
print(f"H-O-H angle: {angle:.2f} degrees; plane normal: {normal}")
# a much more convenient way
angle_2, normal_2 = pts_angles(hydrogen_1, oxygen, hydrogen_2)
angle_2 = np.degrees(angle_2)
print(f"H-O-H angle: {angle_2:.2f} degrees; plane normal: {normal_2}")
```

#### [`McUtils.Zachary`](https://mccoygroup.github.io/McUtils/McUtils/Zachary.html)

`Zachary` provides the higher-order numerical machinery used when plain array
operations are not enough. It is aimed at derivatives, expansions, fitting,
interpolation, and structured numerical representations.

It includes arbitrary-order finite-difference derivatives, Taylor and function
expansions, differentiable function composition, polynomial utilities, lazy and
sparse tensors, regular- and unstructured-grid interpolation, coordinate-path
interpolation, fitted models, multidimensional meshes, and surface construction
including marching cubes and unions of spheres.

```python
import numpy as np
from McUtils.Zachary import TensorExpression

# Construct ||q|| symbolically, then obtain its gradient and Hessian.
q = TensorExpression.CoordinateVector(3, name="coordinates")
radius = TensorExpression.VectorNormTerm(q)
point = np.array([1.0, 2.0, 2.0])
value = TensorExpression(radius, coordinates=point).eval()
gradient = TensorExpression(radius.dQ(), coordinates=point).eval()
hessian = TensorExpression(radius.dQ().dQ(), coordinates=point).eval()
print("radius:", value, "gradient:", gradient, "Hessian eigenvalues:", np.linalg.eigvalsh(hessian))
```

Finite-difference derivatives can be generated lazily and queried only to the
order required:

```python
import numpy as np
from McUtils.Zachary import FiniteDifferenceDerivative

def morse_potential(r, de=0.20, a=1.5, re=1.0):
    return de * (1 - np.exp(-a * (r - re))) ** 2

derivatives = FiniteDifferenceDerivative(morse_potential, stencil=7)(
    np.array([1.0]), mesh_spacing=0.005
)
gradient = derivatives[0]
force_constant = derivatives[0, 0]
print(f"equilibrium gradient: {gradient:.3e}")
print(f"harmonic force constant: {force_constant:.6f}")
```

`SphereUnionSurface` can construct and visualize a solvent-excluded surface
from atomic coordinates and van der Waals radii:

```python
import numpy as np
from McUtils.Data import UnitsData
from McUtils.ExternalPrograms import RDMolecule
from McUtils.Zachary import SphereUnionSurface

mol = RDMolecule.from_smiles("C(C)(C)(C)COOC(c1ccccc1)", add_implicit_hydrogens=True)
angstrom_to_bohr = UnitsData.convert("Angstroms", "BohrRadius")
atoms = mol.atoms
coords = mol.coords * angstrom_to_bohr
surface = SphereUnionSurface.from_xyz(atoms, coords, samples=250)
mesh = surface.get_triangulation(
    method="isosurface", 
    probe_type="ses",
    probe_radius=1.4 * angstrom_to_bohr,
    grid_samples=60
)
print(f"SES area: {mesh.surface_area() / angstrom_to_bohr**2:.2f} Å²")
figure = surface.plot()
figure = mesh.plot(figure=figure)
figure.show()
```

#### [`McUtils.Coordinerds`](https://mccoygroup.github.io/McUtils/McUtils/Coordinerds.html)

`Coordinerds` gives molecular coordinates an explicit, extensible type system.
Its `CoordinateSet` is an `ndarray` subclass that tracks its `CoordinateSystem`,
allowing normal NumPy workflows while retaining the information needed for
coordinate conversion.

The package supports Cartesian, spherical, Z-matrix, generic internal, redundant
internal, and composite coordinate systems; converter registration; analytic
and numerical conversion derivatives; internal-coordinate generation and
pruning; molecular embedding; and iterative conversion back to Cartesian
coordinates.

```python
import numpy as np
from McUtils.Coordinerds import CoordinateSet, CartesianCoordinates3D, ZMatrixCoordinates

water = CoordinateSet([
    [0.0, 0.0, 0.0], [0.96, 0.0, 0.0], [-0.24, 0.93, 0.0]
], system=CartesianCoordinates3D)
ordering = [[0, -1, -1, -1], [1, 0, -1, -1], [2, 0, 1, -1]]
internals = water.convert(ZMatrixCoordinates, ordering=ordering)
rebuilt = internals.convert(CartesianCoordinates3D)
distance = np.linalg.norm(water[1] - water[0])
angle = np.degrees(internals[1, 1])
print(f"O-H distance: {distance:.3f}; H-O-H angle: {angle:.2f}")
assert np.allclose(water, rebuilt)
```

#### [`McUtils.Combinatorics`](https://mccoygroup.github.io/McUtils/McUtils/Combinatorics.html)

`Combinatorics` supports the structured discrete spaces that arise in basis-set
and perturbative calculations. It emphasizes efficient enumeration and indexing
so that large combinatorial objects do not need to be searched naively.

The API covers integer partitions, unique permutations, Lehmer codes,
permutation equivalence classes, symmetric-group spaces, lattice paths, direct
sums, Young tableaux, binomial and Stirling numbers, prime factorizations, stable
factorial ratios, and Halton and Sobol sequences.

```python
import numpy as np
from McUtils.Combinatorics import IntegerPartitioner, UniquePermutations

# Enumerate and index every distinct distribution of four quanta over three modes.
_, partitions = IntegerPartitioner.partitions(4, pad=True, return_lens=True, max_len=3)
states = []
for partition in partitions:
    states.extend(UniquePermutations(partition).permutations())
states = np.unique(np.asarray(states), axis=0)
space = UniquePermutations([2, 1, 1])
indices = space.index_permutations(space.permutations())
assert np.array_equal(space.permutations_from_indices(indices), space.permutations())
```

#### [`McUtils.Graphs`](https://mccoygroup.github.io/McUtils/McUtils/Graphs.html)

`Graphs` provides lightweight graph and tree structures for scientific data
without requiring a full graph-analysis framework. It includes edge-based
graphs, graph traversal and neighborhood operations, tree manipulation, and
basic graph-layout support.

```python
from McUtils.Graphs import EdgeGraph

# Represent ethanol as a labeled molecular graph.
labels = ["C", "C", "O", "H", "H", "H", "H", "H", "H"]
edges = [(0, 1), (1, 2), (0, 3), (0, 4), (0, 5),
         (1, 6), (1, 7), (2, 8)]
ethanol = EdgeGraph(labels, edges)
print("fragments:", ethanol.get_fragments(return_labels=True))
print("C-C-O path:", ethanol.get_path(0, 2))
print("graph centroid:", ethanol.get_centroid())
heavy_atoms = ethanol.take([0, 1, 2])
assert heavy_atoms.get_path(0, 2) == (0, 1, 2)
```

#### [`McUtils.Symmetry`](https://mccoygroup.github.io/McUtils/McUtils/Symmetry.html)

`Symmetry` supplies basic molecular point-group analysis. It represents symmetry
elements and rotors, works with point groups and character data, identifies the
symmetry of molecular structures, and provides tools for symmetrizing
coordinates.

```python
import numpy as np
from McUtils.Symmetry import CharacterTable

c2v = CharacterTable.point_group("Cv", 2)
water = np.array([
    [0.000, 0.000, 0.126],
    [1.437, 0.000, -0.999],
    [-1.437, 0.000, -0.999]
])
reduction = c2v.coordinate_mode_reduction(water)
print(c2v.format())
print("Cartesian representation by irrep:", np.rint(reduction).astype(int))
assert np.allclose(reduction, [2, 0, 1, 0])
```

#### [`McUtils.Data`](https://mccoygroup.github.io/McUtils/McUtils/Data.html)

`Data` wraps frequently used scientific reference data in consistent, lazily
loaded interfaces. It includes atomic and bond properties, physical constants
and unit conversion, named colors, potential and wavefunction data containers,
and arrays that retain their physical units.

```python
from McUtils.Data import AtomData, UnitsData

# Convert a computed O-H harmonic frequency and inspect isotope masses.
frequency_hartree = 0.0167
frequency_cm = frequency_hartree * UnitsData.convert("Hartrees", "Wavenumbers")
m_h = AtomData["Hydrogen", "Mass"]
m_d = AtomData["Deuterium", "Mass"]
m_o = AtomData["Oxygen", "Mass"]
reduced_mass_oh = m_h * m_o / (m_h + m_o)
reduced_mass_od = m_d * m_o / (m_d + m_o)
isotope_shift = (reduced_mass_oh / reduced_mass_od) ** 0.5
print(f"OH: {frequency_cm:.1f} cm^-1; estimated OD: {frequency_cm * isotope_shift:.1f} cm^-1")
```

### Chemistry and external programs

#### [`McUtils.ExternalPrograms`](https://mccoygroup.github.io/McUtils/McUtils/ExternalPrograms.html)

`ExternalPrograms` provides a common layer over chemistry programs, toolkits,
file formats, web resources, and compute environments. Its purpose is to keep
program-specific details out of scientific workflows and make optional tools
discoverable at runtime.

It includes job generation and execution for Gaussian, ORCA, CREST, and Slurm;
readers for Gaussian, ORCA, MOLPRO, CREST, CIF, cube, and formatted-checkpoint
data; adapters for RDKit, ASE, Open Babel, and Pysisyphus; SMILES and 3-D
molecular utilities; chemical-resource web APIs; subprocess and container
execution; managed job queues; and lightweight services for remote or HPC
evaluation.

```python
from McUtils.ExternalPrograms import SLURMExecutionEngine, ExecutionStatus

# The execution layer can swap local processes for Slurm without changing callers.
engine = SLURMExecutionEngine()
future = engine.submit_job(
    "frequency.sbatch",
    watch_dir="frequency-job",
    results_file="results.json",
    poll_time=5
)
print("submitted:", future.job_id, "status:", future.get_status())
if future.get_status() is ExecutionStatus.COMPLETED:
    print(future.get_result())
```

RDKit integration supports conformer generation, force-field optimization,
coordinate manipulation, and interactive 3-D visualization:

```python
import numpy as np
from McUtils.ExternalPrograms import RDMolecule

# RDKit is optional; generate an MMFF-optimized butane conformer ensemble.
conformers = RDMolecule.from_smiles(
    "C(C)(C)(C)COOC(c1ccccc1)", add_implicit_hydrogens=True,
    num_confs=5, 
    optimize=True,
    take_min=False
)
energies = np.array([conf.calculate_energy() for conf in conformers])
best = conformers[np.argmin(energies)].copy()
best.coords = best.coords - best.coords.mean(axis=0)  # recenter the conformer
print("relative energies:", energies - energies.min())
viewer = best.draw(image_size=(600, 400), use_coords=True)
viewer.show()
```

The program-specific parsers also provide a compact route from a completed CREST
run to an ensemble ready for analysis:

```python
import numpy as np
from McUtils.ExternalPrograms import CRESTParser

crest = CRESTParser("crest-run")
ensemble = crest.parse_conformers()
atoms, energies, coordinates = ensemble.atoms, ensemble.energies, ensemble.coords
order = np.argsort(energies)
energies = energies[order] - energies[order[0]]
coordinates = coordinates[order]
print(f"loaded {len(coordinates)} conformers of {len(atoms)} atoms")
print("lowest relative energies:", energies[:5])
best_geometry = coordinates[0]
```

#### [`McUtils.GaussianInterface`](https://mccoygroup.github.io/McUtils/McUtils/GaussianInterface.html)

`GaussianInterface` is a compatibility-oriented entry point for importing
Gaussian results. It exposes log- and formatted-checkpoint readers together with
helpers for extracting energies, geometries, normal modes, force constants, and
higher derivative tensors. New program-neutral work generally belongs in
`ExternalPrograms`, where the underlying Gaussian implementation now lives.

```python
from McUtils.GaussianInterface import GaussianLogReader

with GaussianLogReader("frequency.log") as reader:
    parsed = reader.parse([
        "StandardCartesianCoordinates",
        "DipoleMoments",
        "NormalModes",
        "ScanEnergies"
    ])
atoms, geometries = parsed["StandardCartesianCoordinates"]
dipoles = parsed["DipoleMoments"]
print(f"read {len(geometries)} geometries for {len(atoms)} atoms")
print("final dipole:", dipoles[-1])
```

#### [`McUtils.Parsers`](https://mccoygroup.github.io/McUtils/McUtils/Parsers.html)

`Parsers` is a standalone toolkit for turning large or irregular text files into
structured Python and NumPy data. It combines efficient file streaming with a
composable regular-expression language and declarative structured types.

Use it to locate blocks without loading an entire file, build regex patterns as
Python objects, convert matches into typed or multidimensional arrays, and parse
common XYZ and TeX structures. These components underpin much of the electronic
structure parsing in `ExternalPrograms`.

```python
from McUtils.Parsers import RegexPattern, Repeating, Capturing
from McUtils.Parsers import Number, Whitespace, Optional, StringParser

# Parse a Gaussian-style line into a numeric array without hand-written regex.
eigenvalues = RegexPattern(
    ("Eigenvalues --", Repeating(Capturing(Number), suffix=Optional(Whitespace))),
    joiner=Whitespace
)
parser = StringParser(eigenvalues)
line = "Eigenvalues --  -0.1423  0.0781  0.2114"
values = parser.parse(line)
print("orbital energies:", values)
```

### Visualization and interactive computing

#### [`McUtils.Plots`](https://mccoygroup.github.io/McUtils/McUtils/Plots.html)

`Plots` is a high-level plotting framework built primarily on Matplotlib and
inspired by Mathematica's `Graphics` model. It separates data, graphical
primitives, styling, and display properties so plots can be composed and
restyled consistently.

The package provides 2-D and 3-D graphics, graphics grids, common plot types,
legends and axes management, geometric primitives, themes and color utilities,
images and animations, SVG and scene serialization, and experimental X3D and
VTK backends.

```python
import numpy as np
from McUtils.Plots import Plot, ScatterPlot

x = np.linspace(0, 2 * np.pi, 40)
observations = np.sin(x) + np.random.default_rng(4).normal(0, 0.08, x.shape)
plot = Plot(x, np.sin(x), plot_label="model", plot_style={"color": "navy"})
ScatterPlot(
    x, observations, figure=plot,
    plot_label="measurements",
    plot_style={"color": "crimson", "s": 18}
)
plot.axes_labels = ["phase / rad", "signal"]
plot.plot_label = "Model and measurements"
plot.show()
```

#### [`McUtils.Jupyter`](https://mccoygroup.github.io/McUtils/McUtils/Jupyter.html)

`Jupyter` supports rich, programmatic notebook interfaces. Its `JHTML` layer
represents HTML and Bootstrap components as Python objects and can connect them
to interactive widgets without requiring a separate front-end application.

Additional tools cover reusable controls and app variables, notebook and script
execution, notebook export, image handling, JavaScript and D3 integration,
X3D/JSmol/NGL molecular visualization, and interactive molecule graphics.

```python
from McUtils.Jupyter import JHTML

table = [["Method", "Energy / Eh"], ["HF", -75.983], ["CCSD(T)", -76.241]]
panel = JHTML.Bootstrap.Card(
    JHTML.Bootstrap.Table(table, cls=["table-striped", "table-hover"]),
    header="Water calculation"
)
layout = JHTML.Div(
    JHTML.HTML.Header("Electronic-structure summary"),
    panel,
    JHTML.HTML.P("Values update as calculations finish."),
    cls="container p-3"
)
layout.display()
```

### Software and workflow infrastructure

#### [`McUtils.Scaffolding`](https://mccoygroup.github.io/McUtils/McUtils/Scaffolding.html)

`Scaffolding` contains the operational pieces needed to turn a scientific
calculation into a reliable application or job. The components are designed to
be adopted independently rather than forcing a single application framework.

It provides structured logging, caches, file-backed configurations, serializers,
checkpointing, object persistence and reconstruction, job directories and
runtime state, and helpers for building command-line interfaces.

```python
import numpy as np
from McUtils.Numputils import SparseArray
from McUtils.Scaffolding import PseudoPickler

# Serialize a McUtils sparse object into a reloadable, implementation-neutral form.
hessian = SparseArray.from_diag([0.41, 0.83, 1.26, 1.72])
serializer = PseudoPickler()
payload = serializer.serialize(hessian)
restored = serializer.deserialize(payload)
assert np.allclose(restored.asarray(), hessian.asarray())
print("protocol:", payload["pseudopickle_protocol"], "shape:", restored.shape)
```

#### [`McUtils.Parallelizers`](https://mccoygroup.github.io/McUtils/McUtils/Parallelizers.html)

`Parallelizers` presents a common interface for serial execution,
`multiprocessing`, and MPI. Scientific functions can accept a `parallelizer`
without containing backend-specific branches, while the serial implementation
provides the same contract for debugging and small calculations.

The package also includes parallel task runners, synchronized execution helpers,
and wrappers around `multiprocessing.shared_memory` for sharing NumPy data
without unnecessary copies.

```python
import numpy as np
from McUtils.Parallelizers import SerialNonParallelizer

# The same function can receive an MPI or multiprocessing backend later.
def block_energy(points, *, parallelizer=None):
    return np.sum(points * points)

geometries = np.arange(36.0).reshape(4, 3, 3)
parallelizer = SerialNonParallelizer()
energies = parallelizer.map(
    block_energy, geometries,
    extra_kwargs={"parallelizer": parallelizer}, aggregate=True
)
print("batch energies:", energies)
```

#### [`McUtils.Extensions`](https://mccoygroup.github.io/McUtils/McUtils/Extensions.html)

`Extensions` makes compiled scientific code easier to load and call from Python.
It can discover and build native modules, describe Python/C argument signatures,
locate and manage shared libraries, and expose dynamically loaded functions
through a small foreign-function interface.

```python
import numpy as np
from McUtils.Extensions import FunctionSignature, Argument, ArrayType, RealType, IntType

gradient_signature = FunctionSignature(
    "evaluate_gradient",
    Argument("natoms", IntType),
    Argument("coordinates", ArrayType(RealType, ctypes_spec="double")),
    Argument("gradient", ArrayType(RealType, ctypes_spec="double")),
    return_type=None
)
coordinates = np.zeros((3, 3))
prepared = gradient_signature.prep_args(
    (), {"natoms": 3, "coordinates": coordinates, "gradient": np.empty_like(coordinates)}
)
print(gradient_signature.cpp_signature)
print("prepared coordinate shape:", prepared[1].shape)
```

#### [`McUtils.Formatters`](https://mccoygroup.github.io/McUtils/McUtils/Formatters.html)

`Formatters` handles repeatable generation of text, source, and document-like
outputs. It includes file and string template engines, recursive object walkers,
template-directory writers, TeX construction helpers, plain-text tables, file
matching, and convenient formatting functions.

```python
from McUtils.Formatters import TeX

# Assemble a typeset normal-mode eigenvalue equation from expression objects.
f = TeX.Symbol(TeX.bold("F"))
l = TeX.Symbol(TeX.bold("L"))
omega = TeX.Symbol("omega")
equation = (f * l).Equals(l * (omega ** 2))
document = TeX.Equation(
    equation,
    label="eq:normal-modes"
)
print(document.format_tex())
```

#### [`McUtils.Docs`](https://mccoygroup.github.io/McUtils/McUtils/Docs.html)

`Docs` turns live Python objects and source trees into browsable documentation.
It can walk modules and their children, render interactive or static HTML API
pages, extract embedded examples, build documentation sites, and generate the
compact API stubs and summaries used to document McUtils itself.

```python
from McUtils.Docs import jdoc, ExamplesParser
from McUtils.Zachary import FiniteDifferenceDerivative
from IPython.display import display

# Extract test-backed examples and open rich API documentation in a notebook.
examples = ExamplesParser.from_file("ci/tests/ZacharyTests.py")
finite_difference_examples = [
    name for name in examples.functions
    if "Deriv" in name or "FiniteDifference" in name
]
print("available examples:", finite_difference_examples)
documentation = jdoc(FiniteDifferenceDerivative, max_depth=2)
display(documentation)
```

#### [`McUtils.Devutils`](https://mccoygroup.github.io/McUtils/McUtils/Devutils.html)

`Devutils` collects small abstractions used throughout the suite to keep common
Python plumbing out of scientific code. These include option-set and default
management, lightweight schema validation, file helpers, logging adapters,
output redirection, and explicit singleton sentinels for values such as
“automatic” or “not provided.”

```python
from McUtils.Devutils import OptionsSet, is_dict_like, is_list_like

def run_calculation(*, method, basis="cc-pVDZ", charge=0):
    return method, basis, charge

options = OptionsSet(method="CCSD(T)", basis="aug-cc-pVTZ", charge=0, memory="8GB")
accepted, extra = options.split(run_calculation)
assert is_dict_like(accepted) and is_dict_like(extra)
assert not is_list_like(accepted)
print("call options:", accepted)
print("options for another layer:", extra)
```

#### [`McUtils.Iterators`](https://mccoygroup.github.io/McUtils/McUtils/Iterators.html)

`Iterators` provides compact helpers for consuming and chunking iterables,
splitting and grouping values, flattening nested data, transposing and
interleaving iterators, removing duplicates, and traversing Cartesian products.
These utilities are useful for streaming scientific datasets and expressing
nested iteration without repeating bookkeeping code.

```python
from McUtils.Iterators import chunked, counts, delete_duplicates, flatten

# Turn a nested stream of calculation records into coherent work batches.
records = [[("water", -76.1), ("water", -76.2)],
           [("ammonia", -56.2), ("methane", -40.4), ("methane", -40.5)]]
records = list(flatten(records, atomic_types=(tuple,)))
batch_sizes = counts(record[0] for record in records)
batches = list(chunked(records, 2))
systems = list(delete_duplicates(record[0] for record in records))
print("counts:", batch_sizes)
print("unique systems:", systems)
print("submission batches:", batches)
```

#### [`McUtils.Profilers`](https://mccoygroup.github.io/McUtils/McUtils/Profilers.html)

`Profilers` supplies lightweight timing and profiling tools for investigating
scientific workloads. It includes reusable timers, context-managed timing, and
profiling wrappers that can report where a calculation spends its time.

```python
from McUtils.Profilers import Timer
from McUtils.Numputils import vec_dots
import numpy as np

rng = np.random.default_rng(7)
vectors = rng.normal(size=(100_000, 3))
with Timer("100k vector dot products", rounding=4) as timer:
    norms_squared = vec_dots(vectors, vectors)
timer.start()
normalized = vectors / np.sqrt(norms_squared[:, None])
normalization_time = timer.stop()
print(f"normalization alone: {normalization_time:.4f} seconds")
assert np.allclose(np.linalg.norm(normalized, axis=1), 1)
```

#### [`McUtils.Misc`](https://mccoygroup.github.io/McUtils/McUtils/Misc.html)

`Misc` is the home for focused helpers that do not warrant a larger package. It
currently includes debugging utilities, general decorators, optional-Numba
compatibility decorators, and lightweight symbolic-expression support.

```python
import numpy as np
from McUtils.Misc import Abstract

x, np_symbol = Abstract.vars("x", "np")
potential = Abstract.Lambda(x)(
    0.5 * np_symbol.sum(x * x, axis=-1)
)
energy = potential.compile({"np": np})
points = np.array([[1.0, 2.0, 3.0], [0.5, 0.5, 0.5]])
values = energy(points)
print("harmonic energies:", values)
assert np.allclose(values, [7.0, 0.375])
print("generated AST:", potential.to_eval_expr())
```

### Contributing

If you'd like to help out with this, we'd love contributions.
The easiest way to get started with it is to try it out.
When you find bugs, please [report them](https://github.com/McCoyGroup/McUtils/issues/new?title=Bug%20Found:&labels=bug). 
If there are things you'd like added [let us know](https://github.com/McCoyGroup/McUtils/issues/new?title=Feature%20Request:&labels=enhancement), and we'll try to help you get the context you need to add them yourself.
One of the biggest places where people can help out, though, is in improving the quality of the documentation.
As you try things out, add them as examples, either to the [main page](https://mccoygroup.github.io/References/Documentation/McUtils.html#examples) or to a [child page](https://mccoygroup.github.io/References/Documentation/McUtils/Plots/Plots/Plot.html#examples).
You can also edit the docstrings in the code to add context, explanation, argument types, return types, etc.

Contributions are welcome. The easiest way to begin is to use McUtils in a real
workflow and report what is unclear or broken:

- [Report a bug](https://github.com/McCoyGroup/McUtils/issues/new?title=Bug%20Found:&labels=bug)
- [Request a feature](https://github.com/McCoyGroup/McUtils/issues/new?title=Feature%20Request:&labels=enhancement)

Documentation improvements are especially valuable. Examples, conceptual
explanations, type information, and clearer docstrings all make the broad API
easier to discover. When changing code, please add or update tests under
`ci/tests` and keep public docstrings current.

## License and citation

McUtils is distributed under the [MIT License](LICENSE.txt). Citation metadata is
provided in [`CITATION.cff`](CITATION.cff).

#### API Reference

- [McUtils](McUtils.md)



### Help Us Out!

The easiest way to help us out is to _give feedback_.
Each page _should_ support examples, but unfortunately most do not, simply because writing that kind of thing by hand is time consuming.
If you see a page without examples and you want some, let us know!
To do that, just open and [issue on GitHub]((https://github.com/McCoyGroup/McUtils/issues/new?title=Documentation%20Improvement%20Needed)).
You can use the `Feedback` button at the bottom of each page to do so.

If you want to be a bit more proactive, feel free to provide examples and docstrings yourself! 
There are links at the bottom of each page to edit the examples, templates, and docstrings for that page.
Just create a new one if needed or edit the old one, commit your changes, and `Peeves` will rebuild the site
which what you've added.
It is a huge, huge help, so please take advantage of the opportunity if you're looking for ways to get involved.

