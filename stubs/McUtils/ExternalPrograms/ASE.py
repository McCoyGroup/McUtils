__all__ = ['ASEMolecule', 'ASECalculator']
import sys
import tempfile
import warnings
import numpy as np, io, os
import McUtils.Devutils as dev
from .. import Numputils as nput
from ..Data import AtomData
from .ExternalMolecule import ExternalMolecule
from .ChemToolkits import ASEInterface

class ASEDimerRunner:
    default_optimizer = 'minmode'

    def __init__(self, images, start_idx, displacement_vector, initial_eigenmode_method='displacement', displacement_method='vector', max_num_rot=10, eliminate_guess_nodes=True, reinterpolate=True, **control_options):
        """
        **LLM Docstring**

        Set up an ASE dimer-method transition-state search seeded from a chain of images.

        :param images: the chain of images (`ASEMolecule`s)
        :type images: list
        :param start_idx: the index of the image to start the dimer from
        :type start_idx: int
        :param displacement_vector: the initial dimer orientation
        :type displacement_vector: np.ndarray
        :param initial_eigenmode_method: how to seed the initial eigenmode
        :type initial_eigenmode_method: str
        :param displacement_method: the dimer displacement method
        :type displacement_method: str
        :param max_num_rot: maximum dimer rotations per step
        :type max_num_rot: int
        :param eliminate_guess_nodes: drop the guess node after optimizing
        :type eliminate_guess_nodes: bool
        :param reinterpolate: reinterpolate the path afterward
        :type reinterpolate: bool
        :param control_options: extra ASE `DimerControl` options
        """
        ...

    @classmethod
    def get_ts_guess_points(cls, energies, *, ts_energy_cutoff, ts_min_nodes):
        """
        **LLM Docstring**

        Pick the image indices around the transition state to use for a quadratic fit,
        scanning outward from the energy maximum while the (reactant-referenced) energy
        stays above a cutoff, padding to a minimum node count.

        :param energies: the per-image energies
        :type energies: Sequence[float]
        :param ts_energy_cutoff: fractional energy cutoff (relative to reactant->TS rise)
        :type ts_energy_cutoff: float
        :param ts_min_nodes: minimum number of nodes to keep
        :type ts_min_nodes: int
        :return: the selected image indices
        :rtype: list[int]
        """
        ...

    @classmethod
    def get_dimer_image_guess(cls, base_images, energies=None, distance_metric=None, masses=None, fit_order=2, use_max_for_guess=True, **guess_options):
        """
        **LLM Docstring**

        Guess the transition-state image (or bracketing image pair) along a chain, either
        by taking the energy maximum or by fitting a polynomial to the energy-vs-distance
        profile and locating its peak.

        :param base_images: the chain images
        :type base_images: list
        :param energies: the per-image energies (computed if omitted)
        :type energies: Sequence | None
        :param distance_metric: the inter-image distance metric
        :type distance_metric: Callable | None
        :param masses: the atomic masses (for mass-weighting)
        :type masses: Sequence | None
        :param fit_order: the polynomial fit order
        :type fit_order: int
        :param use_max_for_guess: use the raw energy maximum as the guess
        :type use_max_for_guess: bool
        :param guess_options: options for the guess-point selection
        :return: the TS image index, or the bracketing `(i, i+1)` pair
        :rtype: int | tuple
        """
        ...

    @classmethod
    def from_images(cls, geoms, mol, energies=None, image_guess=None, calc=None, distance_metric=None, masses=None, fit_order=2, ts_energy_cutoff=0.5, ts_min_nodes=3, use_max_for_guess=True, **etc):
        """
        **LLM Docstring**

        Build an `ASEDimerRunner` from a set of geometries, preparing trajectory images
        and guessing the transition-state image when one isn't supplied.

        :param geoms: the geometries along the path
        :type geoms: Sequence
        :param mol: the reference molecule (for preparing images)
        :type mol: ASEMolecule
        :param energies: the per-image energies (computed if omitted)
        :type energies: Sequence | None
        :param image_guess: an explicit TS image index/pair
        :type image_guess: int | tuple | None
        :param calc: the ASE calculator to attach
        :param distance_metric: the inter-image distance metric
        :type distance_metric: Callable | None
        :param masses: the atomic masses
        :type masses: Sequence | None
        :param fit_order: the polynomial fit order
        :type fit_order: int
        :param ts_energy_cutoff: fractional TS energy cutoff
        :type ts_energy_cutoff: float
        :param ts_min_nodes: minimum fit nodes
        :type ts_min_nodes: int
        :param use_max_for_guess: use the raw energy maximum as the guess
        :type use_max_for_guess: bool
        :param etc: extra options for the runner
        :return: the dimer runner
        :rtype: ASEDimerRunner
        """
        ...

    @classmethod
    def from_image_pair(cls, base_images, start, end, **opts):
        """
        **LLM Docstring**

        Build an `ASEDimerRunner` from a bracketing image pair, taking the dimer
        displacement vector as the coordinate difference between them.

        :param base_images: the chain images
        :type base_images: list
        :param start: the starting image index
        :type start: int
        :param end: the bracketing image index
        :type end: int
        :param opts: extra options for the runner
        :return: the dimer runner
        :rtype: ASEDimerRunner
        """
        ...

    def optimize(self, trajectory=None, optimizer=None, logfile=None, maxstep=None, **options):
        """
        **LLM Docstring**

        Run the ASE dimer (min-mode) optimization to converge to a saddle point,
        returning the relaxation object and the resulting image chain.

        :param trajectory: an ASE trajectory to record
        :param optimizer: the dimer translation optimizer (`'minmode'` by default)
        :type optimizer: str | type | None
        :param logfile: a log file/stream
        :param maxstep: the maximum translation step
        :type maxstep: float | None
        :param options: extra options for the optimizer `run`
        :return: `(relaxation, images)`
        :rtype: tuple
        """
        ...

class ASEMolecule(ExternalMolecule):
    """
    A simple interchange format for ASE molecules
    """

    @property
    def atoms(self):
        """
        **LLM Docstring**

        The element symbols of the atoms.

        :return: the atom symbols
        :rtype: Sequence[str]
        """
        ...

    @property
    def coords(self):
        """
        **LLM Docstring**

        The atomic Cartesian coordinates.

        :return: the coordinates
        :rtype: np.ndarray
        """
        ...

    @property
    def charges(self):
        """
        **LLM Docstring**

        The per-atom charges.

        :return: the charges
        :rtype: np.ndarray
        """
        ...

    @property
    def meta(self):
        """
        **LLM Docstring**

        The ASE `Atoms.info` metadata dict.

        :return: the metadata
        :rtype: dict
        """
        ...

    def copy(self):
        """
        **LLM Docstring**

        Return a copy of this molecule, carrying over the calculator and charge.

        :return: the copied molecule
        :rtype: ASEMolecule
        """
        ...

    @classmethod
    def from_atoms(cls, atoms, calculator=None, charge=None):
        """
        **LLM Docstring**

        Wrap an ASE `Atoms` object, optionally attaching a calculator and charge.

        :param atoms: the ASE atoms object
        :param calculator: the ASE calculator to attach
        :param charge: the molecular charge
        :type charge: int | None
        :return: the wrapped molecule
        :rtype: ASEMolecule
        """
        ...

    @classmethod
    def from_coords(cls, atoms, coords, charge=None, spin=None, info=None, calculator=None, **etc):
        """
        **LLM Docstring**

        Build an `ASEMolecule` from atoms and coordinates, recording charge/spin in the
        ASE `info` dict and optionally attaching a calculator.

        :param atoms: the element symbols
        :type atoms: Sequence[str]
        :param coords: the Cartesian coordinates
        :type coords: np.ndarray
        :param charge: the molecular charge
        :type charge: int | None
        :param spin: the spin
        :type spin: int | None
        :param info: an initial ASE `info` dict
        :type info: dict | None
        :param calculator: the ASE calculator to attach
        :param etc: extra arguments for the ASE `Atoms` constructor
        :return: the wrapped molecule
        :rtype: ASEMolecule
        """
        ...

    @classmethod
    def from_mol(cls, mol, coord_unit='Angstroms', calculator=None, calculator_options=None):
        """
        **LLM Docstring**

        Build an `ASEMolecule` from a generic molecule object, converting coordinates to
        Angstroms and deriving an ASE calculator from the molecule's energy evaluator
        when none is given.

        :param mol: the source molecule
        :param coord_unit: the source coordinate unit
        :type coord_unit: str
        :param calculator: an explicit ASE calculator
        :param calculator_options: options for building the calculator from the evaluator
        :type calculator_options: dict | None
        :return: the wrapped molecule
        :rtype: ASEMolecule
        """
        ...

    def calculate_props(self, props, geoms=None, calc=None, extra_calcs=None):
        """
        **LLM Docstring**

        Evaluate the requested ASE calculator properties for the current geometry, or
        for each geometry in a batch, optionally augmenting them with extra computed
        values.

        :param props: the property names to compute
        :type props: Sequence[str]
        :param geoms: a batch of geometries (or `None` for the current one)
        :type geoms: np.ndarray | None
        :param calc: the calculator to use (defaults to the attached one)
        :param extra_calcs: a callable returning extra properties per structure
        :type extra_calcs: Callable | None
        :return: the property values (batched to match `geoms`)
        :rtype: dict
        """
        ...

    def calculate_energy(self, geoms=None, order=None, calc=None, hessian_func_attr='get_hessian'):
        """
        **LLM Docstring**

        Compute the energy (and optionally the gradient and Hessian) at the current
        geometry or over a batch, via the ASE calculator.

        Order `0` returns just the energy; order `1` adds the gradient (negated forces);
        order `2` additionally requires the calculator to expose a Hessian.

        :param geoms: a batch of geometries (or `None` for the current one)
        :type geoms: np.ndarray | None
        :param order: the derivative order (`None`/`0`=energy, `1`=gradient, `2`=Hessian)
        :type order: int | None
        :param calc: the calculator to use
        :param hessian_func_attr: the calculator attribute providing the Hessian
        :type hessian_func_attr: str
        :return: the energy, or a tuple of `(energy, gradient[, hessian])`
        :rtype: float | np.ndarray | tuple
        :raises ValueError: for order > 2, or order 2 without Hessian support
        """
        ...

    @classmethod
    def lookup_optimizer_type(cls, method):
        """
        **LLM Docstring**

        Resolve an ASE optimizer name to its optimizer class.

        :param method: the optimizer name (`'bfgs'`, `'lbfgs'`, ...) or a class
        :type method: str | type
        :return: the optimizer class
        :rtype: type
        """
        ...
    default_optimizer = 'bfgs'

    def resolve_optimizer(self, method):
        """
        **LLM Docstring**

        Resolve an optimizer specification to an ASE optimizer class, defaulting to the
        class default when none is given.

        :param method: the optimizer name/class (or `None` for the default)
        :type method: str | type | None
        :return: the optimizer class
        :rtype: type
        """
        ...

    @staticmethod
    def _prep_logger(logger, quiet):
        """
        **LLM Docstring**

        Resolve the log target for an optimization: a logger's log file, standard out, or
        a throwaway buffer when quiet.

        :param logger: a logger to draw the log file from
        :param quiet: suppress output to a buffer when no logger is given
        :type quiet: bool
        :return: the log file/stream
        :rtype: object
        """
        ...
    convergence_criterion = 0.0001
    max_steps = 100

    def optimize_structure(self, geoms=None, calc=None, quiet=True, logfile=None, logger=None, fmax=None, steps=None, method=None, **opts):
        """
        **LLM Docstring**

        Optimize the current geometry (or each geometry in a batch) with an ASE
        optimizer, returning the optimizer status and optimized coordinates.

        :param geoms: a batch of geometries (or `None` for the current one)
        :type geoms: np.ndarray | None
        :param calc: the calculator to use
        :param quiet: suppress optimizer output
        :type quiet: bool
        :param logfile: an explicit log file/stream
        :param logger: a logger to log through
        :param fmax: the force convergence threshold
        :type fmax: float | None
        :param steps: the maximum optimization steps
        :type steps: int | None
        :param method: the optimizer name/class
        :type method: str | type | None
        :param opts: extra optimizer options
        :return: `(status, optimized_coords, extra)`
        :rtype: tuple
        """
        ...

    def prep_trajectory_images(self, geoms, mol=None, calc=None):
        """
        **LLM Docstring**

        Normalize a set of geometries into a list of `ASEMolecule` images, wrapping raw
        ASE atoms or coordinate arrays and attaching the calculator as needed.

        :param geoms: the geometries (ASE atoms, molecules, or coordinate arrays)
        :type geoms: Sequence
        :param mol: the reference molecule (defaults to this one)
        :type mol: ASEMolecule | None
        :param calc: the calculator to attach
        :return: the image molecules
        :rtype: list[ASEMolecule]
        """
        ...
    default_mep = 'neb'

    def resolve_trajectory_method(self, method, **opts):
        """
        **LLM Docstring**

        Resolve a minimum-energy-path method name to its class (`'neb'`, `'dimer'`, or an
        `ase.mep` attribute).

        :param method: the method name/class
        :type method: str | type | None
        :param opts: unused extra options
        :return: the trajectory method class
        :rtype: type
        """
        ...

    def prep_trajectory_type(self, geoms, method, calc=None, in_place=False, optimizer_method=None, **opts):
        """
        **LLM Docstring**

        Build the trajectory object for a path method from a set of geometries, either
        via the method's `from_images` constructor or by preparing image atoms and
        handing them to the method.

        :param geoms: the geometries along the path
        :type geoms: Sequence
        :param method: the path method (name, class, or options dict)
        :type method: str | type | dict
        :param calc: the calculator to attach
        :param in_place: modify the images in place rather than copying
        :type in_place: bool
        :param optimizer_method: an optimizer method to record in the options
        :type optimizer_method: str | None
        :param opts: extra options for the method
        :return: `(trajectory, images)`
        :rtype: tuple
        """
        ...

    def optimize_trajectory(self, geoms, method, calc=None, quiet=True, logfile=None, logger=None, fmax=None, tol=None, steps=None, optimizer=None, optimizer_method=None, in_place=False, return_coords=True, optimizer_settings=None, **opts):
        """
        **LLM Docstring**

        Optimize a reaction path / minimum-energy-path trajectory (NEB, dimer, etc.),
        returning the optimizer status and the optimized images (or their coordinates).

        :param geoms: the geometries along the path
        :type geoms: Sequence
        :param method: the path method
        :type method: str | type | dict
        :param calc: the calculator to attach
        :param quiet: suppress output
        :type quiet: bool
        :param logfile: an explicit log file/stream
        :param logger: a logger to log through
        :param fmax: the force convergence threshold
        :type fmax: float | None
        :param tol: an alias for `fmax`
        :type tol: float | None
        :param steps: the maximum optimization steps
        :type steps: int | None
        :param optimizer: the optimizer name/class
        :type optimizer: str | type | None
        :param optimizer_method: an optimizer method for the trajectory builder
        :type optimizer_method: str | None
        :param in_place: modify images in place
        :type in_place: bool
        :param return_coords: return image coordinates rather than image objects
        :type return_coords: bool
        :param optimizer_settings: extra optimizer settings
        :type optimizer_settings: dict | None
        :param opts: extra options
        :return: `(status, images_or_coords, extra)`
        :rtype: tuple
        """
        ...

def ASECalculator(energy_evaluator, charge_evaluator=None, dipole_evaluator=None, analytic_derivative_order=None, charge_derivative_order=None, dipole_derivative_order=None, **kwargs):
    """
    **LLM Docstring**

    Build an ASE-compatible calculator that evaluates energies (and optionally
    charges/dipoles) from the supplied McUtils evaluators.

    :param energy_evaluator: the energy-evaluation callable
    :type energy_evaluator: Callable
    :param charge_evaluator: an optional charge evaluator
    :type charge_evaluator: Callable | None
    :param dipole_evaluator: an optional dipole evaluator
    :type dipole_evaluator: Callable | None
    :param analytic_derivative_order: highest analytic energy-derivative order
    :type analytic_derivative_order: int | None
    :param charge_derivative_order: highest analytic charge-derivative order
    :type charge_derivative_order: int | None
    :param dipole_derivative_order: highest analytic dipole-derivative order
    :type dipole_derivative_order: int | None
    :param kwargs: extra options for the calculator
    :return: the ASE calculator
    :rtype: ASETermCalculator
    """
    ...