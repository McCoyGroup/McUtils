__all__ = [
    "ASEMolecule",
    "ASECalculator"
]

import sys
import tempfile
import warnings

import numpy as np, io, os
import McUtils.Devutils as dev
from .. import Numputils as nput
from ..Data import AtomData
# from ..Zachary import CoordinateInterpolator

from .ExternalMolecule import ExternalMolecule
from .ChemToolkits import ASEInterface


class ASEDimerRunner:
    default_optimizer = 'minmode'

    def __init__(self,
                 images,
                 start_idx,
                 displacement_vector,
                 initial_eigenmode_method='displacement',
                 displacement_method='vector',
                 max_num_rot=10,
                 eliminate_guess_nodes=True,
                 reinterpolate=True,
                 **control_options):
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

        self.images = images
        self.start_idx = start_idx
        self.displacement_vector = displacement_vector
        self.control_options = dict(
            initial_eigenmode_method=initial_eigenmode_method,
            displacement_method=displacement_method,
            max_num_rot=max_num_rot,
            **control_options
        )
        self.reinterpolate = reinterpolate
        self.eliminate_guess_nodes = eliminate_guess_nodes

    @classmethod
    def get_ts_guess_points(cls,
                            energies,
                            *,
                            ts_energy_cutoff,  # 50% of the height from the reactants to TS
                            ts_min_nodes  # at least 3 nodes for the quadratic fit
                            ):
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
        energies = np.array(energies)

        product = np.argmin(energies)
        ts = np.argmax(energies)
        if product > ts:
            reactant = np.argmin(energies[:ts])
        else:
            reactant = np.argmin(energies[ts:])

        offset_energies = (energies - energies[reactant])  / (energies[ts] - energies[reactant])

        # scan left and right from the TS until we have either gone below the offset or have reached our node cutoff
        left_points = []
        for i in range(ts-1): # scan in reverse
            if offset_energies[ts - i] > ts_energy_cutoff:
                left_points.append(ts - i)
        right_points = []
        for i in range(ts+1, len(energies)):
            if offset_energies[i] > ts_energy_cutoff:
                right_points.append(i)

        all_points = list(reversed(left_points)) + [ts] + right_points
        if len(all_points) < ts_min_nodes:
            pad = (len(all_points) - ts_min_nodes) // 2
            left_pad = min([pad + (len(all_points) - ts_min_nodes) % 2, all_points[0]])
            right_pad = min([pad, len(energies) - all_points[-1]])
            all_points = (
                list(range(all_points[0] - left_pad, all_points[0]))
                + all_points
                + list(range(all_points[-1] + 1, all_points[-1] + right_pad))
            )

        return all_points


    @classmethod
    def get_dimer_image_guess(cls,
                              base_images,
                              energies=None,
                              distance_metric=None,
                              masses=None,
                              fit_order=2,
                              use_max_for_guess=True,
                              **guess_options
                              ):
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
        if energies is None:
            energies = [m.calculate_energy(order=None) for m in base_images]
        energies = np.array(energies)
        if use_max_for_guess:
            ts = np.argmax(energies)
            if ts > 0:
                if ts < len(energies) - 1:
                    if energies[ts + 1] < energies[ts - 1]:
                        ts = ts - 1
                else:
                    ts = len(energies) - 2
            return ts

        points = cls.get_ts_guess_points(energies, **guess_options)
        geoms = np.array([b.coords for b in base_images])
        if distance_metric is None:
            distance_metric = lambda *args, **kwargs: nput.incremental_eckart_rmsd(*args, mass_weighted=True, **kwargs)
        if masses is None:
            symbols = base_images[0].atoms
            masses = [AtomData[a, "Mass"] for a in symbols]
        distances = distance_metric(
            geoms,
            masses=masses,
        )

        distances = nput.vec_rescale(distances)
        coeffs = np.polyfit(distances[points,], energies[points,], fit_order)
        target_poly = np.poly1d(coeffs)
        pd = target_poly.deriv()
        roots = pd.roots
        vals = target_poly(roots)
        ts_pos_guess = roots[np.argmax(vals)]

        # find the two images nearest to this guessed value
        insert_idx = np.searchsorted(distances, ts_pos_guess)

        return insert_idx, insert_idx+1

    @classmethod
    def from_images(cls,
                    geoms,
                    mol,
                    energies=None,
                    image_guess=None,
                    calc=None,
                    distance_metric=None,
                    masses=None,
                    fit_order=2,
                    ts_energy_cutoff=.5,  # 50% of the height from the reactants to TS
                    ts_min_nodes=3,
                    use_max_for_guess=True,
                    **etc):
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

        base_images = mol.prep_trajectory_images(geoms, calc=calc)
        if image_guess is None:
            image_guess = cls.get_dimer_image_guess(base_images,
                                                    energies=energies,
                                                    distance_metric=distance_metric,
                                                    masses=masses,
                                                    fit_order=fit_order,
                                                    ts_energy_cutoff=ts_energy_cutoff,
                                                    ts_min_nodes=ts_min_nodes,
                                                    use_max_for_guess=use_max_for_guess)
        if nput.is_int(image_guess):
            image_guess = [image_guess, image_guess+1]

        return cls.from_image_pair(base_images, *image_guess, **etc)

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
        displacement_vector = base_images[end].coords - base_images[start].coords
        return cls(
            base_images,
            start,
            displacement_vector,
            **opts
        )

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
        import ase.mep as mep
        opts = self.control_options | {k:v for k,v in {
            'logfile': logfile,
            'maximum_translation': maxstep
        }.items() if v is not None}

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with mep.DimerControl(
                    mask=None,
                    **opts
            ) as d_control: # idk why we are using this as a context manager
                d_atoms = mep.MinModeAtoms(self.images[self.start_idx].mol, d_control)
                d_atoms.displace(displacement_vector=self.displacement_vector)

                if optimizer is None:
                    optimizer = self.default_optimizer

                if dev.str_is(optimizer, 'minmode'):
                    optimizer = mep.MinModeTranslate
                else:
                    optimizer = ASEMolecule.lookup_optimizer_type(optimizer)
                # Converge to a saddle point
                dim_rlx = optimizer(d_atoms, logfile=logfile, trajectory=trajectory)
                dim_rlx.run(**options)

        self.images[self.start_idx].mol = d_atoms.atoms
        if self.eliminate_guess_nodes:
            images = self.images[:self.start_idx+1] + self.images[self.start_idx+2:]
        else:
            images = self.images[self.start_idx:]
        # images = list(self.images)
        # images = (
        #         images[:self.start_idx]
        #         + images[self.start_idx].prep_trajectory_images([d_atoms.atoms])
        #         + images[self.start_idx+1:]
        # )
        return dim_rlx, images

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
        return self.mol.symbols
    @property
    def coords(self):
        """
        **LLM Docstring**

        The atomic Cartesian coordinates.

        :return: the coordinates
        :rtype: np.ndarray
        """
        return self.mol.positions
    @property
    def charges(self):
        """
        **LLM Docstring**

        The per-atom charges.

        :return: the charges
        :rtype: np.ndarray
        """
        return self.mol.charges
    @property
    def meta(self):
        """
        **LLM Docstring**

        The ASE `Atoms.info` metadata dict.

        :return: the metadata
        :rtype: dict
        """
        return self.mol.info

    def copy(self):
        """
        **LLM Docstring**

        Return a copy of this molecule, carrying over the calculator and charge.

        :return: the copied molecule
        :rtype: ASEMolecule
        """
        mol = self.mol.copy()
        return self.from_atoms(mol,
                               calculator=self.mol.calc,
                               charge=self.mol.info.get('charge'))

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
        if calculator is not None:
            atoms.calc = calculator
            if charge is not None and hasattr(calculator, 'set_charge'):
                calculator.set_charge(charge)
        return cls(atoms)

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

        if info is None and charge is not None or spin is not None:
            info = {}
        if charge is not None:
            info['charge'] = charge
        if spin is not None:
            info['spin'] = spin

        atoms = ASEInterface.Atoms(
            atoms,
            coords,
            info=info,
            **etc
        )

        return cls.from_atoms(atoms, calculator=calculator, charge=charge)

    @classmethod
    def from_mol(cls, mol, coord_unit="Angstroms", calculator=None, calculator_options=None):
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
        from ..Data import UnitsData

        if calculator is None and mol.energy_evaluator is not None:
            if calculator_options is None:
                calculator_options = {}
            calculator = mol.get_energy_evaluator().to_ase(**calculator_options)

        return cls.from_coords(
            mol.atoms,
            mol.coords * UnitsData.convert(coord_unit, "Angstroms"),
            # bonds=mol.bonds,
            charge=mol.charge,
            calculator=calculator
        )

    # def calculate_gradient(self, geoms=None, force_field_generator=None, force_field_type='mmff'):
    #     if force_field_generator is None:
    #         force_field_generator = self.get_force_field
    #     cur_geom = np.array(self.mol.GetPositions()).reshape(-1, 3)
    #     if geoms is not None:
    #         geoms = np.asanyarray(geoms)
    #         base_shape = geoms.shape[:-2]
    #         geoms = geoms.reshape((-1,) + cur_geom.shape)
    #         vals = np.empty((len(geoms), np.prod(cur_geom.shape, dtype=int)), dtype=float)
    #         try:
    #             for i, g in enumerate(geoms):
    #                 self.mol.SetPositions(g)
    #                 ff = force_field_generator(force_field_type)
    #                 vals[i] = ff.CalcGrad()
    #         finally:
    #             self.mol.SetPositions(cur_geom)
    #         return vals.reshape(base_shape + (-1,))
    #     else:
    #         ff = force_field_generator(force_field_type)
    #         return np.array(ff.CalcGrad()).reshape(-1)

    # def get_calculator(self):
    #     if isinstance(self.calc, MassWeightedCalculator):
    #         return self.calc.copy()
    #     else:
    #         return self.load_class()(self.calc.base_calc)
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
        from ase.calculators.calculator import all_changes
        if calc is None:
            calc = self.mol.calc
        if geoms is None:
            calc.calculate(self.mol, properties=props, system_changes=all_changes)
            base = {
                k:calc.results[k]
                for k in props
            }
            if extra_calcs is not None:
                updates = extra_calcs(self.mol)
                base.update(updates)
            return base
        else:
            cur_geom = self.mol.positions
            geoms = np.asanyarray(geoms)
            base_shape = geoms.shape[:-2]
            geoms = geoms.reshape((-1,) + cur_geom.shape)
            prop_arrays = {}

            try:
                for i, g in enumerate(geoms):
                    self.mol.positions = g
                    calc.calculate(self.mol, properties=props, system_changes=all_changes)
                    for k in props:
                        res = calc.results[k]
                        if k not in prop_arrays:
                            if hasattr(res, 'shape'):
                                shp = res.shape
                            else:
                                shp = ()
                            prop_arrays[k] = np.empty(
                                (len(geoms),) + shp,
                                dtype=type(res) if not hasattr(res, 'dtype') else res.dtype
                            )
                        prop_arrays[k][i] = res
                    if extra_calcs is not None:
                        updates = extra_calcs(self.mol)
                        for k,res in updates.items():
                            if k not in prop_arrays:
                                prop_arrays[k] = np.empty(
                                    (len(geoms),) + res.shape,
                                    dtype=res.dtype
                                )
                            prop_arrays[k][i] = res
            finally:
                self.mol.positions = cur_geom

            return {
                k:r.reshape(base_shape + r.shape[1:])
                for k,r in prop_arrays.items()
            }

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
        if calc is None:
            calc = self.mol.calc
        just_eng = order is None
        if just_eng: order = 0
        props = ['energy']
        if order > 0:
            props.append('forces')
        extra_calcs = None
        if order > 1:
            if hasattr(calc, hessian_func_attr):
                hessian_func = getattr(calc, hessian_func_attr)
                extra_calcs = lambda m:{'hessian':calc.get_hessian(m)}
            else:
                raise ValueError("ASE calculators only need to implement forces")
        if order > 2:
            raise ValueError("ASE calculators don't support 3rd derivatives by default")
        res = self.calculate_props(props, geoms=geoms, calc=calc, extra_calcs=extra_calcs)
        if just_eng:
            if geoms is None:
                return res['energy'].squeeze()
            else:
                return res['energy']

        base_ndim = 0 if geoms is None else np.asarray(geoms).ndim - 2
        ncoord = 3 * len(self.masses)

        ret_tup = (res['energy'],)
        if order > 0:
            ret_tup = ret_tup + (
                -res['forces'].reshape(res['forces'].shape[:base_ndim] + (ncoord,)),
            )
        if order > 1:
            ret_tup = ret_tup + (
                res['hessian'].reshape(res['forces'].shape[:base_ndim] + (ncoord, ncoord)),
            )
        return ret_tup

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
        if isinstance(method, str):
            import ase.optimize as optimize
            if method == 'bfgs':
                method = optimize.BFGS
            elif method == 'lbfgs':
                method = optimize.LBFGS
            elif method == 'bfgs-linesearch':
                method = optimize.BFGSLineSearch
            elif method == 'lbfgs-linesearch':
                method = optimize.LBFGSLineSearch
            else:
                method = getattr(optimize, method)
        return method

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
        if method is None:
            method = self.default_optimizer
        return self.lookup_optimizer_type(method)

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
        if logger is not None:
            logger = dev.Logger.lookup(logger)
            logfile = logger.log_file
            if logfile is None:
                logfile = sys.stdout
        else:
            if quiet:
                logfile = io.StringIO()
            else:
                logfile = sys.stdout
        return logfile
    convergence_criterion = 1e-4
    max_steps = 100
    def optimize_structure(self,
                           geoms=None,
                           calc=None,
                           quiet=True,
                           logfile=None,
                           logger=None,
                           fmax=None,
                           steps=None,
                           method=None,
                           **opts):
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
        BFGS = self.resolve_optimizer(method)

        if logfile is None:
            logfile = self._prep_logger(logger, quiet)

        if calc is None:
            calc = self.mol.calc
        cur_calc = self.mol.calc
        cur_geom = self.mol.positions
        try:
            self.mol.calc = calc
            if geoms is None:
                opt_rea = BFGS(self.mol, logfile=logfile, **opts)
                if fmax is None:
                    fmax = self.convergence_criterion
                if steps is None:
                    steps = self.max_steps
                opt = opt_rea.run(fmax=fmax, steps=steps)
                opt_coords = self.mol.positions
            else:
                cur_geom = self.mol.positions
                geoms = np.asanyarray(geoms)
                base_shape = geoms.shape[:-2]
                geoms = geoms.reshape((-1,) + cur_geom.shape)
                opt = np.empty((len(geoms),), dtype=object)
                opt_coords = np.empty_like(geoms)

                for i, g in enumerate(geoms):
                    self.mol.positions = g
                    opt_rea = BFGS(self.mol, logfile=logfile, **opts)
                    if fmax is None:
                        fmax = self.convergence_criterion
                    if steps is None:
                        steps = self.max_steps
                    opt[i] = opt_rea.run(fmax=fmax, steps=steps)
                    opt_coords[i] = self.mol.positions
                opt = opt.reshape(base_shape)
                opt_coords = opt_coords.reshape(base_shape + opt_coords.shape[1:])
        finally:
            self.mol.calc = cur_calc
            self.mol.positions = cur_geom

        return opt, opt_coords, {}

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
        if mol is None:
            mol = self
        info = mol.mol.info
        if calc is None:
            calc = mol.mol.calc
        return [
            self.from_atoms(g,
                            calculator=calc if g.calc is None else None,
                            charge=info.get('charge')
                            )
                if hasattr(g, 'calc') and not hasattr(g, 'coords') else
            g
                if hasattr(g, 'coords') else
                    self.from_coords(
                        mol.atoms,
                        g,
                        calc=calc,
                        **info
                    )
            for g in geoms
        ]

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
        if method is None:
            method = self.default_optimizer

        if isinstance(method, str):
            import ase.mep as mep
            # mep = ASEInterface.submodule('mep')
            if method == 'neb':
                method = mep.NEB
            elif method == 'dimer':
                method = ASEDimerRunner
            else:
                method = getattr(mep, method)
        return method

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
        if isinstance(method, dict):
            opts = method.copy() | opts
            method = opts.pop('method')

        if optimizer_method is not None:
            opts['method'] = optimizer_method

        method = self.resolve_trajectory_method(method)

        if hasattr(method, 'from_images'):
            traj = method.from_images(geoms, mol=self, calc=calc, **opts)
            images = None
        else:
            images = self.prep_trajectory_images(geoms, calc=calc)
            if not in_place:
                images = [i.copy() for i in images]
            images = [i.mol for i in images]

            if calc is not None:
                for i in images:
                    i.calc = calc

            traj = method(images, **opts)

        return traj, images

    def optimize_trajectory(self,
                            geoms,
                            method,
                            calc=None,
                            quiet=True,
                            logfile=None,
                            logger=None,
                            fmax=None,
                            tol=None,
                            steps=None,
                            optimizer=None,
                            optimizer_method=None,
                            in_place=False,
                            return_coords=True,
                            optimizer_settings=None,
                            **opts):
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
        traj, images = self.prep_trajectory_type(geoms, method, calc=calc,
                                                 in_place=in_place,
                                                 optimizer_method=optimizer_method)
        if logfile is None:
            logfile = self._prep_logger(logger, quiet)

        if fmax is None:
            if tol is not None:
                fmax = tol
            else:
                fmax = self.convergence_criterion
        if steps is None:
            steps = self.max_steps
        if optimizer_settings is None:
            optimizer_settings = {}
        if hasattr(traj, 'optimize'):
            opt, images = traj.optimize(optimizer=optimizer, logfile=logfile, fmax=fmax, steps=steps,
                                        **(optimizer_settings | opts))
        else:
            if fmax is None:
                fmax = self.convergence_criterion
            if steps is None:
                steps = self.max_steps
            optimizer = self.resolve_optimizer(optimizer)
            opt_rea = optimizer(traj, logfile=logfile, **(optimizer_settings | opts))
            opt = opt_rea.run(fmax=fmax, steps=steps)
            images = self.prep_trajectory_images(images)
        if return_coords:
            images = [i.coords for i in images]

        return opt, images, {}


def ASECalculator(
        energy_evaluator,
        charge_evaluator=None,
        dipole_evaluator=None,
        analytic_derivative_order=None,
        charge_derivative_order=None,
        dipole_derivative_order=None,
        **kwargs
):
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
    from .ASECalculator import ASETermCalculator

    return ASETermCalculator(
        energy_evaluator,
        charge_evaluator=charge_evaluator,
        dipole_evaluator=dipole_evaluator,
        analytic_derivative_order=analytic_derivative_order,
        charge_derivative_order=charge_derivative_order,
        dipole_derivative_order=dipole_derivative_order,
        **kwargs
    )