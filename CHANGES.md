# Changelog

## 1.8.0

Changes since 1.7.5.2.

### Added

- Structured readouts for molecular data, electronic-structure results, jobs, optimizations, logs, archives and profiling, with HTML/Jupyter, text, data and PowerPoint output.
- PowerPoint/OpenXML authoring and animated 3D mesh exports to glTF, including skeletal animation.
- NWChem and Psi4 job builders, dependency reporting, and job submission through local and SLURM execution engines; expanded Gaussian log tools.
- Multipole expansions and electrostatic derivatives, generalized symmetric/Hermitian eigensolvers, and Gaussian polynomial integration.
- AlphaMol molecular surface measures and gradients, smooth skin surfaces and mesh curvature tools.
- Shared-memory array trees and reusable line-indexed JSONL/NPZL data suppliers.
- String-method optimization for reaction paths.

### Changed

- Improved directed and layered graph layouts, multigraph handling, molecular alignment and plot styling.
- Reduced eager permutation generation in unique-partition calculations.
- Eigensystem derivatives support complex Hermitian matrices and reject degenerate eigenvalues when matrix derivatives are nonzero.

### Fixed

- Tensor derivative contractions, broadcasting, matrix inverses and coordinate-frame handling.
- Batched optimization, line searches, quasi-Newton updates and reaction-path reparameterization.
- Conformer hydrogen tags, InChI and stereochemical metadata preservation, cube-file orbital headers and stale coordinate-conversion paths.
- Shared-memory lifecycle handling and HTML/XML, SVG and X3D serialization and rendering regressions.

[Full diff](https://github.com/McCoyGroup/McUtils/compare/v1.7.5.2...87b30b6674857b0364bdc9fb6cd2819ea696fa41)
