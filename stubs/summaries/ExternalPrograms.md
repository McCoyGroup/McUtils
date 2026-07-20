### `ASE.py`
  - **class `ASEDimerRunner`**
    - `__init__(images, start_idx, displacement_vector, initial_eigenmode_method='displacement', displacement_method='vector', max_num_rot=10, eliminate_guess_nodes=True, reinterpolate=True, **control_options)`
    - `get_ts_guess_points(energies, *, ts_energy_cutoff, ts_min_nodes)` — Pick the image indices around the transition state to use for a quadratic fit,
    - `get_dimer_image_guess(base_images, energies=None, distance_metric=None, masses=None, fit_order=2, use_max_for_guess=True, **guess_options)` — Guess the transition-state image (or bracketing image pair) along a chain, either
    - `from_images(geoms, mol, energies=None, image_guess=None, calc=None, distance_metric=None, masses=None, fit_order=2, ts_energy_cutoff=0.5, ts_min_nodes=3, use_max_for_guess=True, **etc)` — Build an `ASEDimerRunner` from a set of geometries, preparing trajectory images
    - `from_image_pair(base_images, start, end, **opts)` — Build an `ASEDimerRunner` from a bracketing image pair, taking the dimer
    - `optimize(trajectory=None, optimizer=None, logfile=None, maxstep=None, **options)` — Run the ASE dimer (min-mode) optimization to converge to a saddle point,
  - **class `ASEMolecule`** (ExternalMolecule)
    > A simple interchange format for ASE molecules
    - `atoms()` — The element symbols of the atoms.
    - `coords()` — **LLM Docstring**
    - `charges()` — **LLM Docstring**
    - `meta()` — **LLM Docstring**
    - `copy()` — Return a copy of this molecule, carrying over the calculator and charge.
    - `from_atoms(atoms, calculator=None, charge=None)` — Wrap an ASE `Atoms` object, optionally attaching a calculator and charge.
    - `from_coords(atoms, coords, charge=None, spin=None, info=None, calculator=None, **etc)` — Build an `ASEMolecule` from atoms and coordinates, recording charge/spin in the
    - `from_mol(mol, coord_unit='Angstroms', calculator=None, calculator_options=None)` — Build an `ASEMolecule` from a generic molecule object, converting coordinates to
    - `calculate_props(props, geoms=None, calc=None, extra_calcs=None)` — Evaluate the requested ASE calculator properties for the current geometry, or
    - `calculate_energy(geoms=None, order=None, calc=None, hessian_func_attr='get_hessian')` — Compute the energy (and optionally the gradient and Hessian) at the current
    - `lookup_optimizer_type(method)` — Resolve an ASE optimizer name to its optimizer class.
    - `resolve_optimizer(method)` — Resolve an optimizer specification to an ASE optimizer class, defaulting to the
    - `optimize_structure(geoms=None, calc=None, quiet=True, logfile=None, logger=None, fmax=None, steps=None, method=None, **opts)` — Optimize the current geometry (or each geometry in a batch) with an ASE
    - `prep_trajectory_images(geoms, mol=None, calc=None)` — Normalize a set of geometries into a list of `ASEMolecule` images, wrapping raw
    - `resolve_trajectory_method(method, **opts)` — Resolve a minimum-energy-path method name to its class (`'neb'`, `'dimer'`, or an
    - `prep_trajectory_type(geoms, method, calc=None, in_place=False, optimizer_method=None, **opts)` — Build the trajectory object for a path method from a set of geometries, either
    - `optimize_trajectory(geoms, method, calc=None, quiet=True, logfile=None, logger=None, fmax=None, tol=None, steps=None, optimizer=None, optimizer_method=None, in_place=False, return_coords=True, optimizer_settings=None, **opts)` — Optimize a reaction path / minimum-energy-path trajectory (NEB, dimer, etc.),
- `ASECalculator(energy_evaluator, charge_evaluator=None, dipole_evaluator=None, analytic_derivative_order=None, charge_derivative_order=None, dipole_derivative_order=None, **kwargs)` — Build an ASE-compatible calculator that evaluates energies (and optionally

### `ASECalculator.py`
  - **class `ASETermCalculator`** (Calculator)
    - `__init__(term_evaluator, charge_evaluator=None, dipole_evaluator=None, analytic_derivative_order=None, charge_derivative_order=None, dipole_derivative_order=None, implemented_properties=None, **kwargs)`
    - `resolve_implemented_properties(analytic_derivative_order, charge_evaluator=None, dipole_evaluator=None, charge_derivative_order=None, dipole_derivative_order=None)`
    - `calculate(atoms=None, properties=['energy'], system_changes=all_changes)`

### `ChemToolkits.py` — Provides support for chemical toolkits
  - **class `OpenBabelInterface`** (ExternalProgramInterface)
    > A simple class to support operations that make use of the OpenBabel toolkit (which is installed with anaconda)
  - **class `PybelInterface`** (ExternalProgramInterface)
    > A simple class to support operations that make use of the OpenBabel toolkit (which is installed with anaconda)
  - **class `RDKitInterface`** (ExternalProgramInterface)
  - **class `ASEInterface`** (ExternalProgramInterface)
    - `Atoms(symbols=None, positions=None, numbers=None, masses=None, charges=None, **etc)`
  - **class `OpenChemistryInterface`**
  - **class `PySCFInterface`**
  - **class `CCLibInterface`**

### `ChemicalResourceAPIs.py`
  - **class `ChemSpiderAPI`** (WebAPIConnection)
    > It is better in general to just use the ChemSpiderPy package, but this works for now
    - `__init__(token=None, request_delay_time=None, **opts)`
    - `get_chemspider_apikey(token)` — Resolve the ChemSpider API key, falling back to the `CHEM_SPIDER_APIKEY`
    - `filter()` — The `filter` sub-API (asynchronous compound-search queries).
    - `records()` — The `records` sub-API (compound record lookups).
    - `lookups()` — **LLM Docstring**
    - `tool()` — **LLM Docstring**
    - `handle_filter_query(query_id, count=1, start=0, **polling_opts)` — Fetch a page of results for a completed filter query.
    - `apply_filter_query(filter_path, retries=None, timeout=None, request_delay_time=None, **opts)` — Submit a filter query and return its results, raising if the API doesn't return a
    - `get_info(ids, fields=None, **opts)` — Fetch the requested fields for a batch of compound record ids.
    - `get_compounds_by_name(name, return_ids=False, fields=None, **opts)` — Look up compounds by name (via a cached name filter query), returning either the
  - **class `PubChemAPI`** (WebAPIConnection)
    > It is better in general to just use the ChemSpiderPy package, but this works for now
    - `__init__(request_delay_time=None, **opts)`
    - `compound()` — **LLM Docstring**
    - `name()` — The `compound/name` sub-API (lookups by compound name).
    - **class `Compound`**
      - `__init__(cid, **opts)`
      - `from_identifiers(data)` — Build a `Compound` from a PubChem property record, pulling the `CID` out as the
    - `get_property_list()` — Return (and cache) the mapping of case-folded property names to their canonical
    - `get_compounds_by_name(name, fields=None, subfield='json', limit=10, query=None, wrap=True, **opts)` — Look up compounds by name via the PubChem name endpoint (with result caching),

### `Containers.py`
  - **class `ContainerLauncher`**
    - `__init__(cli_binary, container_spec, *args, bind_sources=None, container_process=None, process_kwargs=None, **kwargs)`
    - `setup_bind_sources(targets, copy_source=True, resolve_module_names=True)`
    - `prep_binds(binds)`
    - `prep_envs(envs)`
    - `map_option_name(key)`
    - `format_job_args(kwargs)`
    - `prep_core_kwargs(kwargs)`
    - `get_launch_command_from_components(binary, spec, launch_kwargs, proc_args, proc_kwargs)`
    - `get_launch_command()`
    - `launch_container(stdout=True, stderr=True, text=True, **subprocess_kwargs)`
    - `launch(**subprocess_kwargs)`
    - `terminate()`
    - `run(text=True, **subprocess_kwargs)`
  - **class `DockerLauncher`** (ContainerLauncher)
    - `__init__(container_spec, *args, cli_binary='docker', mode='run', **kwargs)`
    - `prep_binds(binds)`
    - `prep_envs(envs)`
    - `launch_option_names()`
    - `prep_core_kwargs(kwargs)`
    - `get_launch_command_from_components(binary, spec, launch_kwargs, proc_args, proc_kwargs)`
  - **class `PodmanLauncher`** (DockerLauncher)
    - `__init__(container_spec, *args, cli_binary='podman', **kwargs)`
  - **class `SingularityLauncher`** (ContainerLauncher)
    - `__init__(container_spec, *args, mode='run', cli_binary='singularity', **kwargs)`
    - `prep_binds(binds)`
    - `prep_envs(envs)`
    - `prep_core_kwargs(kwargs)`
    - `get_launch_command_from_components(binary, spec, launch_kwargs, proc_args, proc_kwargs)`
  - **class `CharliecloudLauncher`** (ContainerLauncher)
    - `__init__(container_spec, *args, cli_binary='ch-run', **kwargs)`
    - `prep_binds(binds)`
    - `prep_envs(envs)`
    - `prep_core_kwargs(kwargs)`
    - `get_launch_command_from_components(binary, spec, launch_kwargs, proc_args, proc_kwargs)`

### `CubeProp.py`
  - **class `CubePropEvaluator`**
    - `__init__(origin, axes, steps, values, base_data=None, **opts)`
    - `from_file(file, **interpolation_opts)` — Build a `CubePropEvaluator` by parsing a cube file.
    - `element_volume()` — The volume of one grid cell (the absolute determinant of the axis vectors),
    - `coords_from_grid(origin, axes, steps)` — Build the Cartesian coordinates of every grid point from the origin, axis
    - `grid_coords()` — The Cartesian coordinates of every grid point (computed lazily).
    - `get_value_interpolator(steps, values, **interpolation_options)` — Build an interpolator over the grid values in (integer) grid-index space.
    - `interpolator()` — The value interpolator over the grid (built lazily).
    - `inverse_axes()` — The inverse of the grid axis matrix (computed lazily), used to map Cartesian
    - `embed_points(points)` — Map Cartesian points into (fractional) grid-index coordinates.
    - `unembed_points(points)` — Map (fractional) grid-index coordinates back into Cartesian space.
    - `evaluate(points)` — Interpolate the grid property at arbitrary Cartesian points.
    - `get_isosurface(isoval, **opts)` — Extract an isosurface at the given value via marching cubes, transformed back

### `ExecutionEngine.py`
  - **class `ExecutionStatus`** (enum.Enum)
  - **class `ExecutionFuture`**
    - `__init__(poll_time=None)`
    - `join(timeout=None)` — Poll `get_status` until the job leaves the unknown, pending, or running states, raising `TimeoutErr…
    - `get_result()` — Abstract interface for retrieving a completed job result.
    - `get_status()` — Abstract interface for querying the current execution state.
  - **class `JoinableExecutionFuture`** (ExecutionFuture)
    - `await_result(timeout=None)` — Abstract blocking hook for backends that expose a native result-wait operation.
    - `join(timeout=None)` — Wait for completion through the backend-specific `await_result` operation instead of status polling.
  - **class `ExecutionQueue`**
    - `__init__(futures)`
    - `join(timeout=None)` — Join each future sequentially while deducting elapsed time from a shared timeout budget.
  - **class `ExecutionEngine`**
    - `register(name, engine=None)` — Register an execution-engine class by name, or return a decorator that performs the registration.
    - `resolve(name, **opts)` — Construct the engine class registered under `name` with the supplied options.
    - `__init__(**opts)`
    - `submit_job(**kwargs)` — Abstract interface for submitting one job and returning its future.
    - `submit_jobs(jobs, **kwargs)` — Submit a sequence of job-option dictionaries, overlay shared options on each entry, and return an `…
    - `startup()` — No-op lifecycle hook intended for engines that must acquire backend resources.
    - `shutdown()` — No-op lifecycle hook intended for engines that must release backend resources.
  - **class `FileBackedExecutionFuture`** (ExecutionFuture)
    - `__init__(watch_dir=None, poll_time=None, results_file=None, status_file=None)`
    - `get_result()` — Read and decode the configured result JSON file from the watch directory or current path.
    - `get_status()` — Read the configured status JSON file and convert its `status` field to `ExecutionStatus`; return `U…
  - **class `ManagedJobQueueExecutionFuture`** (FileBackedExecutionFuture)
    - `__init__(job_id, queue_manager, watch_dir=None, results_file=None, status_file=None, poll_time=None)`
    - `get_status()` — Query the queue manager for the scheduler state and translate it through `queue_status_map`.
  - **class `ManagedJobQueueExecutionEngine`** (ExecutionEngine)
    - `__init__(queue_manager, **opts)`
    - `prep_future_opts(watch_dir=None, results_file=None, status_file=None, poll_time=None, **kwargs)` — Separate file-watching and polling options for the future from the remaining scheduler submission o…
    - `submit_job(*, watch_dir=None, poll_time=None, results_file=None, status_file=None, **kwargs)` — Submit the scheduler options through the queue manager and construct a future for the returned job…
  - **class `SLURMExecutionFuture`** (ManagedJobQueueExecutionFuture)
    - `get_status()` — Query SLURM state, but interpret a previously visible running/completed/error job that has disappea…
  - **class `SLURMExecutionEngine`** (ManagedJobQueueExecutionEngine)
    - `__init__(**opts)`
    - `prep_future_opts(*, sbatch_file, watch_dir=None, chdir=None, **kwargs)` — Derive the watch directory from `chdir` or the sbatch-file directory, then split future options fro…
    - `submit_job(sbatch_file, *, watch_dir=None, poll_time=None, results_file=None, status_file=None, **kwargs)` — Submit an sbatch file, unpack the returned SLURM job id, and create an SLURM-aware execution future.
  - **class `ProcessExecutionFuture`** (JoinableExecutionFuture)
    - `__init__(base_obj, **ignored)`
    - `await_result(timeout=None)` — Call the wrapped result object’s blocking `get` once and cache the returned value.
    - `get_result()` — Return the cached asynchronous result, or `None` before it has been awaited.
    - `get_status()` — Use the wrapped result’s `successful` method to distinguish running, completed, and failed states.
  - **class `ProcessGeneratorExecutionEngine`** (ExecutionEngine)
    - `__init__(proc_gen, **opts)`
    - `submit_job(method, **kwargs)` — Submit `method` with keyword arguments through `apply_async` and wrap the asynchronous result.
    - `startup()` — Enter the process-generator context when the engine becomes active.
    - `shutdown()` — Exit the process-generator context when the engine is deactivated.

### `ExternalMolecule.py`
  - **class `ExternalMolecule`**
    > Defines a common interface so that a programs can define one interface and not need to
    > adjust for every new type of chemistry package they want to support.
    > Not all properties need to be well-defined on every type of molecule, but this defines the core interface
    > that _must_ be implemented
    - `__init__(external_mol)`
    - `atoms()`
    - `coords()`
    - `masses()`
    - `bonds()`
    - `charges()`
    - `from_coords(atoms, coords, **etc)`
    - `from_mol(atoms, coords, **etc)`
    - `show()`

### `ImageKits.py` — Provides support for chemical toolkits
  - **class `PILInterface`** (ExternalProgramInterface)
    > A simple class to support operations that make use of the OpenCV toolkit
    - `from_file(file, **opts)`
    - `from_url(url)`
    - `to_url(image, format='png')`
    - `prep_url_buffer(img_data, format=None)`
  - **class `OpenCVInterface`** (ExternalProgramInterface)
    > A simple class to support operations that make use of the PIL toolkit

### `Interface.py` — Provides a uniform interface for potentially installed external programs
  - **class `ExternalProgramInterface`**
    - `try_load_lib()`
    - `get_lib()`
    - `load_library()`
    - `method(name)`
    - `submodule(submodule)`
    - `lib()`

### `ManagedJobQueues.py`
  - **class `ManagedJobQueueJobStatus`** (enum.Enum)
  - **class `ManagedJobQueueSubmissionHandler`**
    - `map_option_name(key)` — Convert a Python-style option name to a GNU-style `--kebab-case` command-line flag.
    - `format_job_args(**kwargs)` — Flatten keyword options into command-line arguments: true emits a flag, false omits it, and other n…
    - `get_job_command(*args, **opts)` — Assemble the queue submission command from the configured executable, formatted options, and positi…
    - `parse_job_id(res)` — Abstract parser for extracting a scheduler job identifier from submission stdout.
    - `prep_job_kwargs(**kwargs)` — Default submission hook that contributes no positional arguments and passes keyword arguments throu…
    - `create_job_process(**opts)` — Prepare and run the scheduler submission command, reject nonzero or stderr-producing executions, an…
  - **class `ManagedJobQueueInformationHandler`**
    - `get_job_info_command()` — Return the command specification used to query scheduler job information.
    - `run_job_info_cmd()` — Run the scheduler information command with captured text output and raise `IOError` on stderr or a…
    - `parse_raw_job_info(stdout)` — Abstract parser that converts scheduler stdout into raw per-job dictionaries.
    - `parse_job_info(stdout)` — Clean every field of every raw scheduler record, including state normalization.
    - `get_all_job_info()` — Run the scheduler query and index the parsed job records by their `id` field.
  - **class `ManagedJobQueueHandler`**
    - `__init__(information_handler, submission_handler)`
    - `get_job_info()` — Return all current job records from the information handler.
    - `get_job_status(job_id)` — Look up a job record and return its `status` field.
    - `submit_job(**kwargs)` — Forward scheduler options to the submission handler and return its submission result.
  - **class `SLURMSubmissionHandler`** (ManagedJobQueueSubmissionHandler)
    - `prep_job_kwargs(*, sbatch_file, **etc)` — Move `sbatch_file` into the positional argument list expected by `sbatch`.
    - `parse_job_id(res)` — Extract the numeric job id from SLURM’s `Submitted batch job N` response.
  - **class `SLURMInformationHandler`** (ManagedJobQueueInformationHandler)
    - `prep_job_kwargs(*, sbatch_script, **kwargs)` — Return an sbatch script as the sole positional argument and preserve the remaining keyword options.
    - `get_job_info_command(sacct_error=False)` — Build a user-scoped `sacct` query, or an `squeue` fallback command when `sacct_error` is true.
    - `parse_raw_job_info(stdout)` — Slice fixed-width SLURM output lines according to `FMT_SPECS` and return one dictionary per line.
    - `run_job_info_cmd()` — Run the normal SLURM accounting query and fall back to `squeue` when the first command fails.
  - **class `SLURMHandler`** (ManagedJobQueueHandler)
    - `__init__()`
    - `get_job_status(job_id)` — Return the normalized `state` field for a SLURM job record.
- `sbatch_python_script(script, chdir=None, **sbatch_kwargs)` — Submit an existing script with `sbatch`; the `chdir` parameter is currently unused.
- `serialize_python_job(func, *args, serializer='json', deserializer=None, serialization_mode=None, template='run_sbatch_python.py', path_modifications=None, script_file='run_{job_name}_{id}.py', job_name=None, id=None, state_string=None, post_processor='print', cleanup=False, function_args=None, function_kwargs=None, **kwargs)` — Serialize function arguments, pickle and base64-encode the callable and optional post-processor, su…
- `get_active_environment()` — Collect active Conda, virtual-environment, Singularity, container-argument, and environment-script…
- `sbatch_python_job(func, *args, sbatch_kwargs=None, job_name=None, id=None, script=None, environment=None, cleanup=False, post_processor='print', **kwargs)` — Build a generated Python runner and an `SBatchJob`, merging SLURM defaults, propagating the active…

### `OpenBabel.py`
  - **class `OBMolecule`** (ExternalMolecule)
    > A simple interchange format for OB molecules
    - `__init__(obmol, charge=None)`
    - `pbmol()` — The Pybel wrapper around the underlying `OBMol` (built lazily).
    - `get_api()` — **LLM Docstring**
    - `atoms()` — The atomic numbers of the atoms, in order.
    - `bonds()` — The bonds as `[begin_atom, end_atom, order]` triples (0-indexed atoms).
    - `coords()` — The atomic Cartesian coordinates.
    - `set_coords(coords)` — Write new Cartesian coordinates onto the molecule's atoms.
    - `coords(coords)` — The atomic Cartesian coordinates.
    - `atom_iter()` — Return an iterator over the molecule's OpenBabel atoms.
    - `from_obmol(obmol, charge=None, guess_bonds=False)` — Wrap an `OBMol` as an `OBMolecule`, optionally perceiving connectivity and bond
    - `get_obmol_from_conversion(data, fmt=None, add_implicit_hydrogens=False, target_fmt='mol2')` — Read an `OBMol` from a string by converting from the input format to an
    - `get_obmol_from_gen3d(data, fmt=None, add_implicit_hydrogens=False, method='gen3D', target='best')` — Read an `OBMol` from a string and generate a 3D structure for it via OpenBabel's
    - `from_string(data, fmt=None, conformer_generator=None, add_implicit_hydrogens=False, charge=None, guess_bonds=False, **confgen_opts)` — Build an `OBMolecule` from a molecule string, choosing between plain conversion
    - `from_file(file, fmt=None, target_fmt='mol2', add_implicit_hydrogens=False, charge=None, guess_bonds=False)` — Build an `OBMolecule` from a file, inferring the format from the extension when
    - `to_file(file, fmt=None, base_fmt='mol2')` — Write the molecule to a file, inferring the output format from the extension
    - `to_string(fmt, base_fmt='mol2')` — Serialize the molecule to a string in the requested format.
    - `from_coords(atoms, coords, bonds=None, add_implicit_hydrogens=False, charge=None, guess_bonds=False)` — Build an `OBMolecule` from atoms, coordinates, and (optional) bonds.
    - `from_mol(mol, coord_unit='Angstroms', guess_bonds=False)` — Build an `OBMolecule` from a generic molecule object, converting its coordinates
    - `copy()` — Return a copy of this molecule (copying the underlying `OBMol` and charge).
    - `remove_hydrogens(copy=True)` — Remove the molecule's hydrogens (on a copy by default).
    - `make_2d(copy=True)` — Generate a 2D depiction of the molecule (on a copy by default), falling back to
    - `draw(fmt='svg', remove_hydrogens=True, plot_range=None, postdraw=None, scaling_factor=None, splits=None, include_save_buttons=False, use_smiles=False, use_coords=False)` — Render the molecule to an image (SVG/PNG), optionally from its SMILES or its own

### `Pysisyphus.py`
- `suppress_logging(level=logging.CRITICAL)` — Temporarily disables logging for a specific block of code.
- `patch_pysis_logging()` — Monkey-patch Pysisyphus's logging setup so it doesn't install its own file
- `PysisCalculator(energy_evaluator, batched_orders=False, distance_units=None, energy_units=None, **kwargs)` — Build a Pysisyphus-compatible calculator that evaluates energies (and
- `register_method(name, method=None)` — Register a path/optimization method resolver by name (usable directly or as a
- `resolve_cos_method(*, images, cos_class, energy_evaluator=None, out_dir=None, logger=None, fixed_images=None, **opts)` — Build a Pysisyphus chain-of-states object of the given class, ensuring every
- `resolve_gsm(*, images, calc_getter=None, energy_evaluator=None, max_nodes=None, energies=None, distance_metric=None, masses=None, fit_order=2, peak_cutoff=0.5, min_nodes=3, **opts)` — Resolve a growing-string-method chain-of-states object, splitting the images into
- `resolve_chain_of_states(*, images, energy_evaluator=None, **opts)` — :param energy_evaluator: an energy evaluator to build calculators from
- `resolve_freezing_string(*, images, calc_getter=None, energy_evaluator=None, **opts)` — :param calc_getter: a factory for per-image calculators
- `resolve_zta(*, images, energy_evaluator=None, **opts)` — Resolve a zero-temperature-string (SimpleZTS) chain-of-states object.
- `resolve_neb(*, images, energy_evaluator=None, **opts)` — :param energy_evaluator: an energy evaluator to build calculators from
- `resolve_optimize(*, geom, energy_evaluator=None, out_dir=None, **opts)` — Resolve a single-geometry optimization target, ensuring it has a calculator and
- `resolve_ts(*, images, energy_evaluator=None, energies=None, image_guess=None, distance_metric=None, masses=None, fit_order=2, peak_cutoff=0.5, min_nodes=3, climb=True, logger=None, out_dir=None, use_max_for_guess=True, eliminate_guess_nodes=True, **opts)` — Resolve a climbing-image transition-state target: guess the TS image along the
- `get_dimer_image_guess(base_images, energies=None, distance_metric=None, masses=None, *, fit_order=2, peak_cutoff, min_nodes=3, use_max_for_guess=False)` — Guess the transition-state image along a chain, either by the raw energy maximum
- `resolve_dimer(*, images, energy_evaluator=None, energies=None, image_guess=None, distance_metric=None, masses=None, fit_order=2, peak_cutoff=0.5, min_nodes=3, displacement_vector=None, climb=True, logger=None, out_dir=None, use_max_for_guess=True, eliminate_guess_nodes=True, fixed_images=None, **opts)` — Resolve a dimer-method transition-state target: guess the TS image, seed the
- `resolve_pysis_method(method_name, logger=None, **opts)` — Resolve a method name (honoring aliases) to its registered resolver and build the
- `register_optimizer(name, method=None)` — Register a Pysisyphus optimizer resolver by name (usable directly or as a
- `resolve_generic_optimizer(name)` — Build a resolver for a Pysisyphus optimizer looked up by name from the
- `resolve_string_optimizer(traj, **opts)` — Instantiate Pysisyphus's `StringOptimizer` for a trajectory, marking it as a
- `resolve_lbfgs_optimizer(traj, **opts)` — Instantiate Pysisyphus's `LBFGS` optimizer for a trajectory.
- `resolve_lrfo_optimizer(traj, **opts)` — Instantiate Pysisyphus's `RFOptimizer` (rational-function optimization) for a
- `resolve_plbfgs_optimizer(traj, **opts)` — Instantiate Pysisyphus's `PreconLBFGS` (preconditioned L-BFGS) optimizer for a
- `resolve_bfgs_optimizer(traj, **opts)` — Instantiate Pysisyphus's `BFGS` optimizer for a trajectory.
- `resolve_rsprfo_optimizer(traj, **opts)` — Instantiate Pysisyphus's `RSPRFOptimizer` (restricted-step partitioned RFO
- `resolve_rsirfo_optimizer(traj, **opts)` — :param traj: the trajectory/geometry to optimize
- `resolve_trim_optimizer(traj, **opts)` — Instantiate Pysisyphus's `TRIM` transition-state optimizer for a trajectory.
- `resolve_fire_optimizer(traj, **opts)` — Instantiate Pysisyphus's `FIRE` optimizer for a trajectory.
- `resolve_cubic_newton_optimizer(traj, **opts)` — Instantiate the registered Pysisyphus optimizer for a trajectory.
- `resolve_cubic_newton_optimizer(traj, **opts)` — Instantiate the registered Pysisyphus optimizer for a trajectory.
- `resolve_cubic_newton_optimizer(traj, **opts)` — Instantiate the registered Pysisyphus optimizer for a trajectory.
  - **class `PysisyphusLogger`**
    - `__init__(log_file=None)`
    - `log(log_level, *args, **opts)` — Log a message at the given level.
    - `debug(*args, **opts)` — **LLM Docstring**
    - `error(*args, **opts)` — **LLM Docstring**
- `resolve_pysis_optimizer(optimizer, method_name, generator, logger=None, **opts)` — Resolve and instantiate the optimizer for a method: pick the default optimizer
- `parse_trj(file)` — Parse an XYZ trajectory (`.trj`) file into its geometries.
- `run_pysisyphus(energy_evaluator, method, optimizer=None, optimizer_settings=None, max_cycles=None, max_step=None, max_displacement=None, thresh=None, tol=None, use_max_for_error=True, log_file=None, out_dir=None, return_logs=True, patch_logging=True, logger=None, ignore_zero_steps=True, **kwargs)` — Run a full Pysisyphus optimization: resolve the method and optimizer, translate
- `register_interpolator(name, method=None)` — Register a path interpolator resolver by name (usable directly or as a
- `resolve_idpp(geoms, **opts)` — Build a Pysisyphus IDPP (image-dependent pair potential) interpolator.
- `resolve_linear(geoms, **opts)` — **LLM Docstring**
- `resolve_redund(geoms, **opts)` — **LLM Docstring**
- `resolve_pysis_interpolator(interpolator, traj, logger=None, **opts)` — Resolve an interpolator name to its resolver and build the interpolator for a
- `prep_pysis_images(atoms, geometry, coord_type='cartesian', coord_kwargs=None, **opts)` — Build Pysisyphus `Geometry` objects from atoms and one or more coordinate sets,
- `pysis_interpolate(geoms, interpolator, **opts)` — Interpolate a path between endpoint geometries using a Pysisyphus interpolator,

### `PysisyphusCalculator.py`
  - **class `PysisyphusTermCalculator`** (Calculator)
    - `__init__(term_evaluator, batched_orders=False, distance_units=None, energy_units=None, **kwargs)`
    - `get_energy(atoms, coords)`
    - `get_forces(atoms, coords)`
    - `get_hessian(atoms, coords)`

### `QM9.py`
  - **class `QM9`**
    - `__init__(qm9_data)`
    - `build_qm9(qm9_dir, pattern='*.xyz', target='qm9.npz')` — Build a packed QM9 `.npz` dataset from a directory of extended-XYZ files,
    - `load_qm9(qm9_file)` — Load a packed QM9 `.npz` dataset, memory-mapped.
    - `smiles_query(pattern, start_at=0, upto=None, track_failures=False, quiet=True, **parser_options)` — Find the dataset entries whose SMILES match a SMARTS pattern, optionally tracking
    - `load_data(index, props=None)` — Load the requested properties for a single dataset entry.
    - `data_iter(props=None, start_at=None, upto=None)` — Iterate over the dataset entries, yielding the requested properties for each.

### `RDKit.py`
  - **class `RDMolecule`** (ExternalMolecule)
    > A simple interchange format for RDKit molecules
    - `__init__(rdconf, charge=None)`
    - `rdmol()` — The underlying RDKit `Mol` object (recovered from the conformer if needed).
    - `atoms()` — The element symbols of the atoms, in order.
    - `bonds()` — The bonds as `[begin_atom, end_atom, order]` triples.
    - `coords()` — The atomic Cartesian coordinates (Angstroms).
    - `coords(coords)` — The atomic Cartesian coordinates (Angstroms).
    - `rings()` — The atom-index tuples of the rings found by RDKit's ring perception.
    - `meta()` — The molecule's RDKit properties as a dict.
    - `copy()` — Return a copy of this molecule, carrying over the current conformer and charge.
    - `charges()` — The per-atom Gasteiger partial charges (computed on access).
    - `formal_charges()` — **LLM Docstring**
    - **class `NullContext`**
    - `quiet_errors(verbose=False)` — Return a context manager that suppresses RDKit's C++ log output, unless
    - `chem_api()` — **LLM Docstring**
    - `guess_rdmol_bonds(rdmol, charge=None, determine_orders=True, in_place=False)` — Perceive the bonds (and, optionally, bond orders) of a mol from its atomic
    - `from_rdmol(rdmol, conf_id=0, charge=None, guess_bonds=False, sanitize=True, add_implicit_hydrogens=False, sanitize_ops=None, allow_generate_conformers=False, num_confs=1, optimize=False, take_min=True, force_field_type='mmff')` — Build an `RDMolecule` from an RDKit mol, adding hydrogens and optionally guessing
    - `resolve_bond_type(t)` — Map a numeric bond order to the corresponding RDKit `BondType` (handling the
    - `from_coords(atoms, coords, bonds=None, charge=None, formal_charges=None, guess_bonds=None, add_implicit_hydrogens=False, implicit_hydrogen_method=None, distance_matrix_tol=0.05, num_confs=None, optimize=False, take_min=None, force_field_type='mmff', confgen_opts=None, sanitize=False, **opts)` — Build an `RDMolecule` from atoms, coordinates, and (optional) bonds, optionally
    - `from_mol(mol, coord_unit='Angstroms', guess_bonds=None)` — Build an `RDMolecule` from a generic molecule object, converting its coordinates
    - `from_sdf(sdf_string, which=0)` — Build an `RDMolecule` from an SDF file path or string.
    - `get_confgen_opts(version='v3', use_experimental_torsion_angle_prefs=True, use_basic_knowledge=True, **opts)` — Build an RDKit ETKDG conformer-generation parameter object of the requested
    - `parse_smiles(smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, add_implicit_hydrogens=None, reorder_from_atom_map=False, replacements=None, quiet=False, **opts)` — Parse a SMILES (or CXSMILES) string into an RDKit mol, with control over
    - `from_smiles(smiles, sanitize=False, parse_name=True, allow_cxsmiles=True, strict_cxsmiles=True, remove_hydrogens=False, replacements=None, add_implicit_hydrogens=False, call_add_hydrogens=True, conf_id=None, num_confs=None, optimize=False, take_min=True, force_field_type='mmff', reorder_from_atom_map=True, confgen_opts=None, check_tag=True, coords=None, conf_tag=None, **opts)` — Build an `RDMolecule` from a SMILES string (or file), embedding a conformer
    - `from_base_mol(mol, conf_id=None, num_confs=None, optimize=False, take_min=None, force_field_type='mmff', confgen_opts=None, **mol_opts)` — Build an `RDMolecule` from an RDKit mol, using an existing conformer when
    - `generate_conformers_for_mol(mol, *, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', add_implicit_hydrogens=False, distance_constraints=None, initial_coordinates=None, fragment_placement_method=None, fragments=None, embedding_mol=None, verbose=False, **opts)` — Generate one or more conformers for a mol via RDKit's ETKDG embedding,
    - `from_no_conformer_molecule(mol, *, conf_id=None, num_confs=1, optimize=False, take_min=True, force_field_type='mmff', add_implicit_hydrogens=False, confgen_opts=None, **etc)` — Generate conformer(s) for a mol that has none, then wrap the result(s) as
    - `to_smiles(remove_hydrogens=None, remove_implicit_hydrogens=None, include_tag=False, canonical=False, compute_stereo=False, remove_stereo=False, preserve_atom_order=False, binary=False, coords=None, mol=None, **opts)` — Serialize the molecule to a SMILES string, with options for hydrogen/stereo
    - `find_substructure(query)` — Return all substructure matches of a SMARTS query in the molecule.
    - `apply_smarts_to_mol(mol, pattern, remove_hydrogens=True, readd_hydrogens=True)` — Apply a SMARTS reaction transform to a mol, running the reaction and
    - `apply_smarts(tf)` — Apply a SMARTS reaction transform to this molecule, returning the products as
    - `take_mol_fragment(mol, inds, conf_id=None)` — Build a sub-mol from the given atom indices (with the bonds among them),
    - `break_bonds(bonds, add_dummies=False, reguess_bonds=True, return_fragments=False)` — Break the given bonds and return the resulting (fragmented) molecule, carrying
    - `fragment_rdmol(mol, inds)` — Build a sub-mol from the given atom indices and the bonds among them.
    - `fragment_rdmol_on_bonds(mol, bonds, addDummies=True)` — Fragment a mol by breaking the given bonds, returning a mapping from each
    - `get_atom_neighbors(i, n=1, mol=None, graph=None)` — Return the labels of the atoms within `n` bonds of a given atom.
    - `draw(figure=None, background=None, remove_atom_numbers=None, remove_hydrogens=True, display_atom_numbers=False, format='svg', drawer=None, coords=None, use_coords=False, align_2d=None, view_settings=None, plot_range=None, atom_labels=None, bond_labels=None, blend_mixed_bonds=True, highlight_atoms=None, highlight_bonds=None, highlight_atom_colors=None, highlight_bond_colors=None, highlight_atom_radii=None, highlight_bond_radii=None, highlight_bond_width_multiplier=None, atom_radii=None, bond_radius=None, allow_radius_rescaling=True, draw_coords=None, highlight_rings=None, label_offset=1, conf_id=None, include_save_buttons=False, no_free_type=None, postdraw=None, return_splits=None, radius_to_range_scaling=None, **draw_opts)` — Draw the molecule in 2D (SVG/PNG), with extensive control over hydrogen removal,
    - `plot(conf_id=None, image_size=(450, 450), **opts)` — Display an interactive 3D rendering of the molecule (via RDKit's IPython 3D
    - `conformer_smiles_tag(coords=None, graph=None, zmatrix=None, encoder=None, byte_size=None, byte_encoding=None, binary=False, include_zmatrix=False)` — Encode the molecule's 3D geometry into a compact string tag (a Z-matrix of the
    - `conformer_from_smiles_tag(tag, graph, decoder=None, byte_size=None, byte_encoding=None, zmatrix=None)` — Decode a conformer tag back into Cartesian coordinates, using the molecular graph
    - `get_mol_edge_graph(mol)` — Build an `EdgeGraph` of a mol's atom/bond connectivity.
    - `get_edge_graph(mol=None)` — Build an `EdgeGraph` of this molecule's connectivity (or of a supplied mol).
    - `from_molblock(molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts)` — Build an `RDMolecule` from a MDL molblock/`.mol` file or string.
    - `from_mrv(molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts)` — Build an `RDMolecule` from a Marvin `.mrv` file or string.
    - `from_xyz(molblock, add_implicit_hydrogens=False, guess_bonds=True, **mol_opts)` — Build an `RDMolecule` from an XYZ file or string (perceiving bonds by default).
    - `from_mol2(molblock, add_implicit_hydrogens=False, sanitize=False, remove_hydrogens=False, **mol_opts)` — Build an `RDMolecule` from a Tripos `.mol2` file or string.
    - `from_cdxml(molblock, add_implicit_hydrogens=True, **mol_opts)` — Build an `RDMolecule` from a ChemDraw `.cdxml` file or string.
    - `from_pdb(molblock, add_implicit_hydrogens=True, **mol_opts)` — Build an `RDMolecule` from a PDB file or string.
    - `from_png(molblock, add_implicit_hydrogens=False, **mol_opts)` — Build an `RDMolecule` from an RDKit-metadata-bearing PNG file or string.
    - `from_fasta(molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts)` — Build an `RDMolecule` from a FASTA sequence (generating a conformer by default).
    - `from_inchi(molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts)` — Build an `RDMolecule` from an InChI string (generating a conformer by default).
    - `from_helm(molblock, add_implicit_hydrogens=True, allow_generate_conformers=True, **mol_opts)` — Build an `RDMolecule` from a HELM (macromolecule) string (generating a conformer
    - `to_xyz(filename=None, conf_id=None, **opts)` — Serialize the molecule to XYZ (returned as a string, or written to a file).
    - `to_molblock(filename=None, conf_id=None, **opts)` — Serialize the molecule to an MDL molblock (returned as a string, or written to a
    - `to_mrv(filename=None, conf_id=None, **opts)` — Serialize the molecule to Marvin MRV (returned as a string, or written to a
    - `to_pdb(filename=None, conf_id=None, **opts)` — Serialize the molecule to PDB (returned as a string, or written to a file).
    - `to_cml(filename=None, **opts)` — Serialize the molecule to CML (returned as a string, or written to a file).
    - `to_sdf(filename=None, **opts)` — Serialize the molecule to SDF (returned as a string, or written to a file).
    - `allchem_api()` — **LLM Docstring**
    - `get_force_field_type(ff_type)` — Resolve a force-field name to the RDKit `(force_field_getter, property_generator)`
    - `get_force_field(force_field_type='mmff', conf=None, mol=None, conf_id=None, **extra_props)` — Build an RDKit force-field object for a conformer, computing any needed
    - `evaluate_charges(coords, model='gasteiger')` — Compute the per-atom partial charges for a set of coordinates (currently only
    - `calculate_energy(geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None)` — Compute the force-field energy of the current geometry, or of each geometry in a
    - `calculate_gradient(geoms=None, force_field_generator=None, force_field_type='mmff', conf_id=None)` — Compute the force-field energy gradient of the current geometry, or of each
    - `calculate_hessian(force_field_generator=None, force_field_type='mmff', stencil=5, mesh_spacing=0.01, **fd_opts)` — Compute the force-field Hessian at the current geometry by finite-differencing
    - `get_optimizer_params(maxAttempts=1000, useExpTorsionAnglePrefs=True, useBasicKnowledge=True, **etc)` — Build an RDKit ETKDGv3 parameter object for structure optimization/embedding.
    - `optimize_structure(geoms=None, force_field_type='mmff', optimizer=None, maxIters=1000, **opts)` — Force-field optimize the current geometry, or each geometry in a batch, returning
    - `show()` — Display an interactive 3D rendering of the current conformer (via RDKit's

### `Runner.py`
  - **class `ExternalProgramRunner`**
    - `__init__(binary, parser=None, prefix=None, suffix=None, delete=True, **runtime_opts)`
    - **class `_write_dir`**
      - `__init__(dir=None, dir_prefix=None, dir_suffix=None, delete=True)`
    - `prep_dir(dir)` — Placeholder hook for subclasses to populate a working directory before launching the external progr…
    - `subprocess_run(binary, input_file, **subprocess_opts)` — Run `binary input_file`, resolving a local binary to an absolute path before calling `subprocess.ru…
    - `run_job(binary, job, dir=None, dir_prefix=None, dir_suffix=None, mode='w', runner=None, prep_dir=None, prep_job=None, prep_results=None, return_auxiliary_files=True, prefix=None, suffix=None, delete=True, raise_errors=True, **subprocess_opts)` — Materialize a job in a named temporary input file, execute the external binary in the work director…
    - `run(job, dir=None, dir_prefix=None, dir_suffix=None, mode=None, runner=None, prep_dir=None, prep_job=None, prep_results=None, return_auxiliary_files=None, prefix=None, suffix=None, delete=None, raise_errors=None, **job_opts)` — Merge per-call overrides with the runner defaults and invoke `run_job` using this instance’s binary…

### `SMILES.py`
  - **class `SMILESSupplier`**
    - `__init__(smiles_file, line_indices=None, name=None, size=int(1000.0), split_idx=0, split_char=None, line_parser=None)`
    - `from_name(name)` — Build a supplier for one of the known SMILES databases (e.g.
    - `to_mp_state()` — Serialize the minimal state needed to rebuild this supplier in a worker process.
    - `from_mp_state(state, line_indices=None, **extra)` — Rebuild a supplier from the state produced by `to_mp_state`, optionally with a
    - `find_smi(n, block_size=None)` — Seek to and read the `n`-th entry (extending the line index if needed),
    - `consume_iter(start_at=None, upto=None)` — Iterate over the SMILES entries from `start_at` up to `upto` (or the end),
    - `create_line_index(upto=None, return_index=True)` — Scan the file to build (or extend) the byte-offset index, up to `upto` entries or
    - `save_line_index(file, line_index)` — Save a byte-offset index to a `.npy` file, down-casting it to the smallest
- `consume_smiles_supplier(supplier, consumer, pool=None, start_at=None, upto=None, initializer=None)` — Apply a consumer function to the SMILES entries of a supplier, optionally in
- `smarts_matcher(pattern, error_value=None, sanitize=True, **parser_options)` — Build a matcher callable that tests whether a SMILES string contains a given
- `match_smiles_supplier(supplier, matcher, pool=None, start_at=None, upto=None, quiet=True, out_file=None, initializer=None)` — Match every SMILES entry in a supplier against a SMARTS pattern (or matcher),

### `Subprocesses.py`
- `env_proc_call(*args, executable=None, text=True, env=None, shell=False, **subprocess_run_kwargs)` — Run a command with an environment-specific executable directory prepended to `PATH`; string command…
- `env_pip(*args)` — Invoke `env_proc_call` with `pip` as the command.

### `Toolkits3D.py`
  - **class `Open3DInterface`** (ExternalProgramInterface)
    > A simple class to support operations that make use of the OpenCV toolkit

### `Visualizers.py`
  - **class `VPythonInterface`** (ExternalProgramInterface)
    > A simple class to support operations that make use of the VPython visualization toolkit
  - **class `VTKInterface`** (ExternalProgramInterface)
    > A simple class to support operations that make use of the VPython visualization toolkit
    - `graphics_object(obj)`
    - `named_colors()`

### `WebAPI.py`
  - **class `WebAPIError`** (IOError)
  - **class `WebRequestHandler`**
    - `resolve_handler(handler)`
    - `request(method, url, json=None, handler=None, **params)`
    - `requests_request(method, url, **params)`
    - `urllib3_request(method, url, **params)`
    - `default_request(method, url, data=None, headers=None, origin_req_host=None, unverifiable=False, json=None, **params)`
    - `handle_response(resp, headers)`
    - `read_response(resp, decode=True)`
  - **class `APIAuthentication`**
    - `prep_request(url_params, **kwargs)`
    - `resolve_auth(auth_data)`
    - `get_auth_dispatch()`
    - `dispatch_auth(opts)`
  - **class `NoAuth`** (APIAuthentication)
    - `prep_request(url_params, **kwargs)`
  - **class `HeaderValueAuth`** (APIAuthentication)
    - `__init__(header, value)`
    - `prep_request(url_params, headers=None, **kwargs)`
  - **class `BasicAuth`** (APIAuthentication)
    > Does any site still use this???
    - `__init__(username, password)`
    - `prep_request(url_params, headers=None, **kwargs)`
  - **class `BearerTokenAuth`** (APIAuthentication)
    - `__init__(token, encoded=True)`
    - `prep_request(url_params, headers=None, **kwargs)`
  - **class `WebAPIConnection`**
    > Base class for super simple web api interactions, use something better designed in general
    - `__init__(auth_info, history_length=None, log_requests=False, request_delay_time=None)`
    - `prep_headers(headers, content_type=None, return_type=None)`
    - `do_request(method, root, *path, query=None, headers=None, content_type=None, return_type=None, handler=None, delay_time=None, json=None, data=None, **urllib3_request_kwargs)`
    - `get(root, *path, query=None, **urllib3_request_kwargs)`
    - `post(root, *path, query=None, **urllib3_request_kwargs)`
    - `delete(root, *path, query=None, **urllib3_request_kwargs)`
    - `get_endpoint_params(root, path, query=None, base=None, fragment=None)`
    - `get_subapi(extension)`
  - **class `WebSubAPIConnection`** (WebAPIConnection)
    - `__init__(path_extension, root_api)`
  - **class `WebResourceManager`** (ResourceManager)
    - `__init__(*, request_handler=None, **opts)`
    - `get_resource_filename(name)`
    - `download_link(link)`
  - **class `ReleaseZIPManager`** (WebResourceManager)
    - `parse_semver(version_string)`
    - `make_semver(version)`
    - `parse_name_version(filename)`
    - `list_resources()`
    - `save_resource(loc, val)`
  - **class `GitHubReleaseManager`** (WebAPIConnection)
    - `__init__(token=None, request_delay_time=None, release_manager=None, **opts)`
    - `list_repos(owner)`
    - `list_releases(owner, repo)`
    - `latest_release(owner, repo)`
    - `update_existing_releases()`
    - `format_repo_key(owner, name)`
    - `resolve_resource_url(v)`
    - `get_release_list(owner, name, update=None)`

### `Jobs/CREST.py`
  - **class `CRESTOptionsBlock`** (OptionsBlock)
    - `load_json()` — Load (and cache) the CREST options specification from the bundled JSON file.
    - `get_props()` — Return the accepted option names for this block, read from its section of the
  - **class `CRESTProcessBlock`** (CRESTOptionsBlock)
    - `format_export()` — Format the process/environment options as shell `export` lines.
    - `get_params()` — Return the `command_line` parameter carrying the `export` commands (or an empty
  - **class `CRESTCommandLineBlock`** (CRESTOptionsBlock)
    - `get_props()` — Return the accepted command-line options, adding the `chrg` (charge) flag.
    - `format_command_line()` — Format the CREST command-line flags (`--flag` / `--flag value`), inlining a few
    - `get_params()` — Return the `command_line` parameter carrying the formatted CREST flags (or an
  - **class `CRESTPathsBlock`** (OptionsBlock)
  - **class `CRESTSystemBlock`** (SystemBlock)
    - `format_coordinate_block()` — Format the molecule as an XYZ block (atom count, blank comment line, then the
    - `get_params()` — Return the molecule-specification template parameters (the XYZ coordinate
  - **class `CRESTJob`** (ExternalProgramJob)
    - `__init__(*strs, path='crest', input_file='geom.xyz', log_file='confgen.log', **opts)`
    - `get_block_types()` — Return the ordered CREST block types.
    - `load_template()` — Return the path to the CREST job (shell-script) template.

### `Jobs/Gaussian.py`
  - **class `GaussianOptionsBlock`** (OptionsBlock)
    - `load_json()` — Load (and cache) the Gaussian options specification from the bundled JSON file.
    - `get_props()` — Return the accepted option names for this block, read from its section of the
    - `check_subopts(key, opt_list, opt_dict=None, ignore_missing=False)` — Validate the sub-options passed to a Gaussian keyword against the values allowed
    - `format_opts(opt_list, opt_dict=None, wrap=False)` — Format a keyword's sub-options into Gaussian's `opt` or `key=val` /
    - `format_base_params(opts=None)` — Format this block's options into a list of `keyword` / `keyword=value` strings,
  - **class `GaussianLinkBlock`** (GaussianOptionsBlock)
    - `get_params()` — Format the Link0 (`%`-prefixed) commands into the `link0` template parameter.
  - **class `GaussianLOTBlock`** (GaussianOptionsBlock)
    - `get_props()` — Return the accepted level-of-theory options, adding `basis_set` and
    - `get_basis_set_map()` — Return the lower-case-to-canonical mapping of the known basis-set names.
    - `get_params()` — Format the level-of-theory line (`#method(opts)/basis`), pulling the basis set
  - **class `GaussianRouteBlock`** (GaussianOptionsBlock)
    - `special_param_dispatch()` — Mapping from route keywords needing special handling to their handler methods.
    - `handle_freq(opts)` — Special-case the `freq` route keyword, splitting out the anharmonic/normal mode
    - `get_params()` — Format the route section, applying any special-keyword handlers and wrapping the
  - **class `GaussianSystemBlock`** (SystemBlock)
    - `format_vars_block(vars, float_fmt='{:11.8f}', joiner=None)` — Format a set of variables/constants into `name value` (or `name=value`) lines.
    - `format_coordinate_block()` — Format the molecule specification: the charge/multiplicity line, the Cartesian
    - `get_params()` — Return the molecule-specification template parameters (the coordinate block and,
  - **class `GaussianRestBlock`** (GaussianOptionsBlock)
    - `load_json()` — Treat every remaining `{...}` placeholder in the job template as an accepted
  - **class `GaussianJob`** (ExternalProgramJob)
    - `__init__(*strs, **opts)`
    - `get_extra_keys()` — Return the set of `{...}` placeholder names present in the job template.
    - `get_block_types()` — Return the ordered Gaussian block types.
    - `load_template()` — Return the path to the Gaussian job template.
    - `get_params()` — Assemble the job parameters, appending a trailing blank line to every section

### `Jobs/Jobs.py`
  - **class `JobBlockBase`**
    - `get_template()` — Abstract: return the template string this block fills in.
    - `get_params()` — Abstract: return the `{template_key: value}` mapping used to fill the template.
    - `format()` — Render the block by filling its template with its parameters (recursively
  - **class `JobBlock`** (JobBlockBase)
    - `__init__(**opts)`
    - `get_template()` — **LLM Docstring**
    - `get_params()` — Return the block options as template parameters, formatting any value that
  - **class `OptionsBlock`** (JobBlock)
    - `__init__(canonicalize_opts=True, **opts)`
    - `get_props()` — Return the tuple of option names this block accepts.
    - `get_aliases()` — Return the mapping of canonical option names to their accepted aliases.
    - `get_canonical_opts_map()` — Return (and cache) the lower-case-to-canonical mapping of the block's property
    - `get_props_set()` — Return (and cache) the set of accepted property names, for fast membership
    - `get_inverse_alias_map()` — Return (and cache) the lower-case-alias-to-canonical-name mapping.
    - `check_canon(opt, val)` — Test whether an option belongs to this block, returning its canonical name.
    - `canonicalize_opt_name(opt)` — Resolve an option name to its canonical form via the alias and canonicalization
    - `check_opts(opts)` — Canonicalize and validate a set of options, raising on unknown or duplicated
    - `prep_opts(opts)` — Normalize an option value into the canonical `[positional_list, keyword_dict]`
  - **class `SystemBlock`** (OptionsBlock)
    - `fmt_carts(atoms, carts, float_fmt='{:11.8f}')` — Format a set of atoms and Cartesian coordinates into aligned columns.
    - `fmt_zmat(atoms, zmat, ordering=None, float_fmt='{:11.8f}')` — Format a Z-matrix (connectivity ordering plus internal-coordinate values) into
    - `fmt_orca_zmat(atoms, zmat, ordering=None, float_fmt='{:11.8f}')` — Format a Z-matrix in ORCA's column order (all reference-atom indices, then all
    - `format_bonds_block()` — Format the block's explicit bond list (pairs, optionally with a bond order) into
  - **class `ExternalProgramJob`**
    - `__init__(**opts)`
    - `get_block_types()` — Abstract: return the ordered list of `OptionsBlock` types making up this job.
    - `load_template()` — Abstract: return the top-level job template.
    - `populate_blocks(opts)` — Route each supplied option into the first block that recognizes it, raising if
    - `get_params()` — Build every block's parameters and merge them into a single template-parameter
    - `format()` — Render the full job input file by filling the job template with the merged block
    - `write(file, mode='w')` — Write the formatted job to a file (path or open stream).

### `Jobs/Orca.py`
  - **class `OrcaOptionsBlock`** (OptionsBlock)
    - `load_json()` — Load (and cache) the ORCA options specification from the bundled JSON file.
    - `get_props()` — Return the accepted option names for this block, read from its section of the
  - **class `OrcaKeywordsBlock`** (OrcaOptionsBlock)
    - `__init__(keywords=None, **rest)`
    - `load_basis_sets()` — Return (and cache) the lower-case-to-canonical mapping of known basis-set names.
    - `get_props()` — Return the accepted keywords, combining `keywords`, the JSON-derived list, and
    - `canonicalize_basis_set(k)` — Resolve a basis-set name to its canonical spelling.
    - `get_params()` — Format the simple-keyword line (the `!`-prefixed keyword list).
  - **class `OrcaGlobalsBlock`** (OrcaKeywordsBlock)
    - `load_basis_sets()` — Return an empty basis-set mapping (basis sets are not globals).
    - `get_props()` — Return the accepted globals option names (the keywords list without the leading
    - `get_params()` — Format the global (`%`-prefixed) settings block.
  - **class `OrcaMethodsBlock`** (OrcaOptionsBlock)
    - `__init__(opts=None, **rest)`
    - `format_options_block(header, opts)` — Format a single `%header ...
    - `get_props()` — Return the accepted method-block names, plus the catch-all `opts` key.
    - `get_params()` — Format all of the requested `%...end` method blocks into the `methods`
  - **class `OrcaSystemBlock`** (SystemBlock)
    - `format_coordinate_block()` — Format the ORCA coordinate block (`*xyz`/`*gzmt charge mult ...
    - `get_params()` — Return the molecule-specification template parameters (the coordinate block and,
  - **class `OrcaJob`** (ExternalProgramJob)
    - `__init__(*strs, basis_set=None, level_of_theory=None, **opts)`
    - `get_block_types()` — Return the ordered ORCA block types.
    - `load_template()` — Return the path to the ORCA job template.

### `Jobs/SBatch.py` — Provides minimal utilities for making slurm stuff nicer
  - **class `SBatchJob`**
    > Provides a simple interface to formatting SLURM
    > files so that they can be submitted to `sbatch`.
    > The hope is that this can be subclassed codify
    > options for different HPC paritions and whatnot.
    - `__init__(description=None, job_name=None, account=None, partition=None, mem=None, nodes=None, ntasks_per_node=None, chdir=None, output=None, steps=(), precall=None, environment=None, **opts)`
    - `clean_opts(opts)` — Makes sure opt names are clean.
    - `format_opt_block()` — Formats block of options
    - `format()` — Formats an SBATCH file from the held options
    - `write(file, output_dir=None, mode='w+', **kwargs)` — Write the formatted SLURM script to a file, optionally within a working
    - `run(file=None, output_dir=None, sbatch_function='sbatch', delete=True, text=True, capture_output=True, *args, **kwargs)` — Write the SLURM script and submit it with `sbatch` (via `subprocess.run`),

### `Parsers/CIFParser.py`
  - **class `CIFSymmetriesArray`**
    - `__init__(key, symmetry_list)`
    - `transformation()` — The (cached) affine transformation matrices for the held symmetry operations.
  - **class `CIFParser`** (FileLineByLineReader)
    - `__init__(file, fields=None, **kw)`
    - `check_tag(line, depth=0, active_tag=None, label=None, history=None)` — Classify a CIF line for the line-by-line reader: block starts (`data_`, `loop_`,
    - `get_block_handlers()` — Return the mapping of CIF field name to the handler that converts its raw text
    - `resolve_handler(label)` — Pick the handler for a field, falling back to the integer handler for fields
    - `handle_block(label, block_data, join=True, depth=0)` — Convert a parsed CIF block into typed data: apply a field handler when there is
    - `parse(target_fields=None)` — Parse the CIF file into a list of block dicts, optionally restricting to a set of
  - **class `CIFConverter`**
    - `__init__(parsed_cif)`
    - `cell_properties()` — The unit-cell properties (all `cell_*` fields), merged into one dict.
    - `atom_properties()` — The atom-site properties (all `atom_*` fields), merged into one dict.
    - `symmetry_properties()` — The symmetry properties (all `symmetry_*` fields), merged into one dict.
    - `prep_property_dict(res)` — Flatten a list of per-block property dicts into a single merged dict.
    - `find(item, strict=True, cache=False)` — Find the first value matching a field name (exact or, when `strict` is off, by
    - `find_all(item, strict=True, cache=False)` — Find every value matching a field name (exact or, when `strict` is off, by
    - `atoms()` — The atom coordinates built from the atom and symmetry properties (applying the
    - `construct_base_atom_coords(property_dict)` — Build the base (asymmetric-unit) atom structure from a property dict: element
    - `construct_atom_coords(atom_properties, symmetry_properties)` — Build the full atom structure by applying the crystallographic symmetry

### `Parsers/Crest.py`
  - **class `CRESTOptLogParser`** (FileStreamReader)
    - `__init__(file, **kwargs)`
    - `parse_struct(data)` — Parse one optimization-step block into its energy, atom labels, and coordinates.
    - `get_next_block()` — Read the next optimization-step block (delimited by `=` and `Etot`), or `None` at
    - `parse()` — Parse every optimization step in the log into a list of coordinate records.
  - **class `CRESTConfgenLogParser`** (ElectronicStructureLogReader)
    - `parse(keys=None, num=None, reset=False)` — Parse the conformer-generation log for the requested component keys (defaulting
  - **class `CRESTParser`**
    > Real access pattern: CRESTParser.<AttrName> (7 class attributes, e.g. CRESTParser.opt_log_file == 'crestopt.log'). Collapsed into a dict below purely for compactness -- do not index it as a dict in real code:
    - `__init__(parse_dir, opt_log_file=None, confgen_log_file=None, ensemble_energies_file=None, conformers_file=None, conformers_best_file=None, rotamers_file=None)`
    - `parse_optimized_structures()` — Parse the optimization-log file into its sequence of structures.
    - `parse_ensemble_enegies()` — Load the ensemble-energies file as a numeric array.
    - `parse_conformers(conformers_file=None)` — Parse a conformers XYZ file into atoms, per-conformer energies, and coordinates.
    - `parse_best_conformers()` — :return: the parsed `(atoms, energies, coords)`
    - `parse_rotamers(rotamers_file=None)` — Parse a rotamers XYZ file into atoms, energies, weights, and coordinates.
    - `parse_log()` — **LLM Docstring**

### `Parsers/CubeParser.py`
  - **class `CubeFileParser`** (FileLineByLineReader)
    - `__init__(file, **kw)`
    - `check_tag(line, depth=0, active_tag=None, label=None, history=None)` — Drive the sequential cube-file parse: emit the header, grid, atoms, and values
    - `handle_block(label, block_data, join=True, depth=0)` — Convert each parsed cube block (`header`, `grid`, `atoms`, `values`) into its
    - `parse()` — Parse the whole cube file, merging the block results into a single

### `Parsers/FChkDerivatives.py` — Lazy class for holding force constants and higher derivative tensors pulled from the Gaussian log f…
  - **class `FchkForceConstants`**
    > Holder class for force constants coming out of an fchk file.
    > Allows us to construct the force constant matrix in lazy fashion if we want.
    - `__init__(fcs, num_atoms=None, reader=None)`
    - `n()` — The number of atoms, inferred from the data length if not supplied.
    - `shape()` — The shape of the full force-constant matrix, `(3n, 3n)`.
    - `array()` — The full, symmetrized `(3n, 3n)` force-constant matrix reconstructed from the
  - **class `FchkForceDerivatives`**
    > Holder class for force constant derivatives coming out of an fchk file
    - `__init__(derivs, num_atoms=None, num_modes=None, reader=None)`
    - `n()` — The number of atoms, inferred from the data length if not supplied.
    - `num_modes()` — The number of modes, inferred from the data length if not supplied.
    - `third_derivs()` — **LLM Docstring**
    - `fourth_derivs()` — **LLM Docstring**
    - `third_deriv_array()` — The third derivatives as a full `(m, 3n, 3n)` tensor, symmetrized from the
    - `fourth_deriv_array()` — The fourth derivatives as a sparse tensor built from the diagonal elements
  - **class `FchkDipoleDerivatives`**
    > Holder class for dipole derivatives coming out of an fchk file
    - `__init__(derivs, num_atoms=None, reader=None)`
    - `n()` — The number of atoms, inferred from the data length (`3 * 3n` values) if not
    - `shape()` — The shape of the dipole-derivative array, `(3n, 3)`.
    - `array()` — The dipole derivatives reshaped to `(3n, 3)`.
  - **class `FchkDipoleHigherDerivatives`**
    > Holder class for dipole derivatives coming out of an fchk file
    - `__init__(derivs, num_atoms=None, num_modes=None, reader=None)`
    - `num_modes()` — The number of modes, inferred from the data length if not supplied.
    - `n()` — The number of atoms, inferred from the data length if not supplied.
    - `shape()` — The shape of one derivative block, `(m, 3n, 3)`.
    - `second_deriv_array()` — The second dipole derivatives (`d^2 mu / dQ dx`) reshaped to `(m, 3n, 3)`.
    - `third_deriv_array()` — The third dipole derivatives (`d^3 mu / dQ^2 dx`) as a `(m, m, 3n, 3)` tensor,
  - **class `FchkDipoleNumDerivatives`**
    > Holder class for numerical derivatives coming out of an fchk file.
    > Gaussian returns first and second derivatives
    - `__init__(derivs, num_atoms=None, num_modes=None, reader=None)`
    - `num_modes()` — The number of modes, inferred from the data length if not supplied.
    - `shape()` — The shape of one derivative block, `(m, 3)`.
    - `first_derivatives()` — The first numerical dipole derivatives, reshaped to `(m, 3)`.
    - `second_derivatives()` — The second numerical dipole derivatives, reshaped to `(m, 3)`.

### `Parsers/GaussianFChkComponents.py` — Defines components of an .fchk file that are already known and parseable
- `get_names(atom_ints, reader=None)`
- `reformat(coords, reader=None)`
- `parse_pol(pol_array, tril=np.tril_indices(3), reader=None)`
- `parse_hyper_pol(pol_array, tril=np.tril_indices(3), reader=None)`
- `parse_pol_derivs(pol_array, tril=np.tril_indices(3), reader=None)`
- `parse_pol_num_derivs(pol_array, tril=np.tril_indices(3), reader=None)`
- `split_vib_modes(mcoeffs, reader=None)` — Pulls the mode vectors from the coeffs
- `split_vib_e2(e2, reader=None)` — Pulls the vibrational data out of the file

### `Parsers/GaussianImporter.py` — Implements an importer for Gaussian output formats
  - **class `GaussianLogReaderException`** (FileStreamReaderException)
    > A class for holding exceptions that occur in the course of reading from a log file
  - **class `GaussianLogReader`** (FileStreamReader)
    > Implements a stream based reader for a Gaussian .log file.
    > This is inherits from the `FileStreamReader` base, and takes a two pronged approach to getting data.
    > First, a block is found in a log file based on a pair of tags.
    > Next, a function (usually based on a `StringParser`) is applied to this data to convert it into a usable data format.
    > The goal is to move toward wrapping all returned data in a `QuantityArray` so as to include data type information, too.
    > *(truncated — see stub for full docstring)*
    - `parse(keys=None, num=None, reset=False)` — The main function we'll actually use.
    - `get_default_keys()` — Tries to get the default keys one might be expected to want depending on the type of job as determi…
    - `read_props(file, keys)` — Convenience classmethod: open `file`, parse the requested keys, and return the
  - **class `GaussianFChkReaderException`** (FileStreamReaderException)
  - **class `GaussianFChkReader`** (FileStreamReader)
    > Implements a stream based reader for a Gaussian .fchk file. Pretty generall I think. Should be robust-ish.
    > One place to change things up is convenient parsers for specific commonly pulled parts of the fchk
    - `__init__(file, **kwargs)`
    - `read_header()` — Reads the header and skips the stream to where we want to be
    - `get_next_block_params()` — Pulls the tag of the next block, the type, the number of bytes it'll be,
    - `get_block(name=None, dtype=None, byte_count=None, value=None)` — Pulls the next block by first pulling the block tag
    - `skip_block(name=None, dtype=None, byte_count=None, value=None)` — Skips the next block
    - `num_atoms()` — The number of atoms in the file, parsed (and cached) from the `Number of atoms`
    - `parse(keys=None, default='raise')` — Parse the requested blocks out of the `.fchk` file (or every block when no keys
    - `read_props(file, keys)` — Convenience classmethod: open `file`, parse the requested keys, and return the

### `Parsers/GaussianLogComponents.py` — This lists the types of readers and things available to the GaussianLogReader
- `header_parser(header)`
- `parser(zmat)`
- `cartesian_coordinates_parser(strs, label_pattern=label_pattern)`
- `header_cartesian_parser(carts)`
- `parser(strs)`
- `parser(pars)` — Parses a optimizatioon parameters block
- `parser(charges)` — Parses a Mulliken charges block
- `parser(moms)` — Parses a multipole moments block
- `parser(moms)` — Parses a multipole moments block
- `convert_D_number(a, **kw)`
- `parser(mom)` — Parses dipole block, but only saves the dipole of the optimized structure
- `parser(block)` — Parses the scan summary block
- `parser(pars)` — Parses the scan summary block and returns only the energies
- `parse_scf_energies(energy_blocks)`
- `parse_scf_block_coordinate_energies(energy_blocks)`
- `parser(pars)` — Parses the X matrix block and returns stuff --> huge pain in the ass function
- `parser(block, start=tag_start)`
- `parse_aimd_coords(blocks)`
- `convert_D_number(a, **kw)`
- `parse_grad(block)`
- `parse_weird_mat(pars)` — Parses the Hessian matrix block and returns stuff --> huge pain in the ass function
- `convert_D_number_block(a, **kw)`
- `parse_aimd_values_blocks(blocks)`
- `parser(blocks)`
- `parse_force_list(strs)`
- `parse_hessian_list(hessias)`
- `parse_cubic_mat(pars, label_pattern=label_pattern)` — Parses the Hessian matrix block and returns stuff --> huge pain in the ass function
- `parse_cubics_list(hessias)`
- `parse_quartics_list(hessias)`
- `parse_nms_modes(label, symmetries, freqs, masses, fcs, ir_ints, _, disps)`
- `parse_nms_block(block)`
- `parse(blocks)`
- `parse_excited_states(blocks)`
- `parse_coriolis(blocks)`
- `parse_quadratics(blocks)`
- `parse_cubics(blocks)`
- `parse_quartics(blocks)`
- `skip_report_header(stuff)`
- `parse_reports(blocks, endline_pattern=RegexPattern([Newline, Whitespace]), num_pattern=num_pattern, numblock_pattern=Repeating(num_pattern, suffix=Optional(',')))`
- `tag_validator(block)`

### `Parsers/MOLPRO.py`
  - **class `MOLPROLogReader`** (ElectronicStructureLogReader)

### `Parsers/Orca.py`
  - **class `OrcaLogReader`** (ElectronicStructureLogReader)
  - **class `OrcaHessReader`** (FileStreamReader)
    - `__init__(file, **kwargs)`
    - `get_special_handlers()` — Return the mapping of block tags that need a dedicated parser to that parser.
    - `handle_orca_block(tag, data)` — Dispatch a `.hess` block to the appropriate parser, choosing by tag: a special
    - `parse_matrix(data, col_blocks=5, data_pattern=None)` — Parse an ORCA block-formatted matrix (a header giving the dimensions followed by
    - `parse_array(data, data_pattern=None)` — Parse an ORCA block whose header gives a length followed by that many numeric
    - `parse_atoms(data)` — Parse the atoms block into element labels, masses, and coordinates.
    - `get_next_block()` — Read the next `$tag ...
    - `parse(tags=None, excludes=None)` — Parse the `.hess` file into a dict of tag to parsed block, optionally restricting

### `Parsers/Parsers.py`
  - **class `ElectronicStructureLogReader`** (FileStreamReader)
    > Implements a stream based reader for a generic electronic structure .log file.
    > This is inherits from the `FileStreamReader` base, and takes a two pronged approach to getting data.
    > First, a block is found in a log file based on a pair of tags.
    > Next, a function (usually based on a `StringParser`) is applied to this data to convert it into a usable data format.
    > The goal is to move toward wrapping all returned data in a `QuantityArray` so as to include data type information, too.
    - `load_components()` — Import (and cache) the module registering this reader's parse components (the
    - `registered_components()` — The mapping of component name to its block specification (tags, parser, mode),
    - `default_keys()` — The default set of component keys to parse, taken from the loaded components
    - `default_ordering()` — The default parse ordering for the components, taken from the loaded components
    - `parse(keys, num=None, reset=False)` — The main function we'll actually use.
    - `read_props(file, keys)` — Convenience classmethod: open `file`, parse the requested keys, and return the

### `Parsers/LogComponents/CRESTLogComponents.py` — This lists the types of readers and things available to the GaussianLogReader
- `parse_command_line(inp_str)` — Pass the matched block through unchanged (the command-line / calculation-info
- `parse_command_line(inp_str)` — Pass the matched block through unchanged (the command-line / calculation-info
- `cartesian_coordinates_parser(cart)` — Parse a CREST Cartesian-coordinates block into atom labels and coordinates.
- `parse_opt_info(opt_block)` — Pass the final-optimization-info block through unchanged.
- `parse_ensemble_info(opt_block)` — Parse the final ensemble-information block into the per-conformer energies

### `Parsers/LogComponents/MOLPROLogComponents.py` — This lists the types of readers and things available to the GaussianLogReader
- `strip_recursive(at_list)` — Recursively strip whitespace (and leading integer labels) from every string in a
- `cartesian_coordinates_parser(strs)` — Parse a MOLPRO Cartesian-coordinates block into atom labels and coordinates.
- `normal_modes_parser(strs)` — Parse a MOLPRO normal-modes block into per-structure frequencies and mode
- `quadratic_terms_parser(qts)` — Parse the MOLPRO quadratic force-constant terms into their mode index and value
- `cubic_terms_parser(qts)` — Parse the MOLPRO cubic force-constant terms into their mode-index triples and
- `quartic_terms_parser(qts)` — Parse the MOLPRO quartic force-constant terms into their mode-index quadruples

### `Parsers/LogComponents/OrcaLogComponents.py` — This lists the types of readers and things available to the GaussianLogReader
- `strip_recursive(at_list)` — Recursively strip whitespace from every string in a nested list.
- `cartesian_coordinates_parser(strs)` — Parse an ORCA Cartesian-coordinates block into atom labels and coordinates.
- `cartesian_au_coordinates_parser(strs)` — Parse an ORCA atomic-units Cartesian-coordinates block into atom labels, masses,
- `freqs_parser(freq_str)` — Parse an ORCA vibrational-frequencies block into a flat frequency array.
- `parse_orca_matrix(orca_mat)` — Parse an ORCA column-blocked matrix printout into a dense array, dropping the

### `Servers/EvaluationServer.py`
  - **class `EvaluationHandler`** (NodeCommHandler)
    - `get_evaluators()`
    - `wrap_evaluator(name, evaluation_function)`
    - `get_methods()`
  - **class `EvaluationClient`** (NodeCommClient)
    - `call(evaluator, coords, filename=None, **kwargs)`

### `Servers/GitServer.py`
  - **class `GitClient`** (ShellCommHandler)
    - `get_methods()`
    - `do_git(args, kwargs)`

### `Servers/NodeCommServer.py` — A simple handler interprocess communication on HPC systems
- `check_kill_process(w_pid, cur_pid)`
- `listen_for_proc(w_pid, cur_pid, polling_time=5)`
- `setup_parent_terminated_listener(PARENT_PID, CURRENT_PID)`
- `infer_mode(connection)`
  - **class `NodeCommTCPServer`** (socketserver.TCPServer)
  - **class `NodeCommClient`**
    - `__init__(connection, timeout=10)`
    - `prep_command_env()`
    - `communicate(command, args, kwargs)`
    - `print_response(response)`
    - `call(command, *args, **kwargs)`
  - **class `NodeCommHandler`** (socketserver.StreamRequestHandler)
    - `handle()`
    - `handle_json_request(message)`
    - `setup_env(env)`
    - `method_dispatch()`
    - `dispatch_request(request, env)`
    - `get_methods()`
    - `get_valid_port(git_port, min_port=4000, max_port=65535)`
    - `get_default_connection(port=None, hostname='localhost', session_var='SESSION_ID')`
    - `serialize_connection(connection, mode)` — Build a JSON-serializable dict describing the connection.
    - `write_connection_file(connection_file, connection, mode)` — Write the connection details out as JSON for clients to consume.
    - `read_connection_file(connection_file)` — Read connection details written by `start_server` and return a
    - `start_server(connection=None, port=None, connection_file=None)`
    - `parse_kwargs(extra)` — Convert leftover ``--`` tokens into a kwargs dict.
    - `build_arg_parser()`
    - `resolve_connection(socket=None, host='localhost', port=None)` — Pick a connection spec from CLI options.
    - `main(argv=None)`
    - `resolve_roots(base, roots=None, allowed_domains=None)`
    - `create_server_package(hostpath, package_name=None, overwrite=False, dependency_paths=None)`
    - **class `MultiprocessingServerContext`**
      - `__init__(proc, timeout=3)`
    - `start_multiprocessing_server(connection=None, port=None, timeout=3, connection_file=None)`
    - `client_request(*args, client_class=None, connection=None, connection_file=None)`
  - **class `ShellCommHandler`** (NodeCommHandler)
    - `subprocess_response(command, args)`
    - `kwargs_to_cli(kwargs)` — Convert a kwargs dict into GNU/sbatch-style CLI flags.
    - `method_dispatch()`
    - `change_pwd(args, kwargs)`
    - `get_pwd(args, kwargs)`
    - `setup_env(env)`
    - `get_subprocess_call_list()`
    - `get_methods()`
- `setup_server(handler_class, connection=None, port=None, ppid=None, hostname=None, connection_file=None)`
- `handle_command_line(handler_class, client_class, connection=None, port=None, ppid=None, hostname=None, connection_file=None)`

### `Servers/SLURMServer.py`
  - **class `SLURMClient`** (ShellCommHandler)
    - `get_methods()`
    - `do_sbatch(args, kwargs)`