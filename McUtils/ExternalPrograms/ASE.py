

__all__ = [
    "ASEMolecule",
    "ASECalculator"
]

import sys
import tempfile

import numpy as np, io, os
from .. import Numputils as nput

from .ExternalMolecule import ExternalMolecule
from .ChemToolkits import ASEInterface

class ASEMolecule(ExternalMolecule):
    """
    A simple interchange format for ASE molecules
    """

    @property
    def atoms(self):
        return self.mol.symbols
    @property
    def coords(self):
        return self.mol.positions
    @property
    def charges(self):
        return self.mol.charges
    @property
    def meta(self):
        return self.mol.info

    def copy(self):
        mol = self.mol.copy()
        return self.from_atoms(mol,
                               calculator=self.mol.calc,
                               charge=self.mol.info.get('charge'))

    @classmethod
    def from_atoms(cls, atoms, calculator=None, charge=None):
        if calculator is not None:
            atoms.calc = calculator
            if charge is not None and hasattr(calculator, 'set_charge'):
                calculator.set_charge(charge)
        return cls(atoms)

    @classmethod
    def from_coords(cls, atoms, coords, charge=None, spin=None, info=None, calculator=None, **etc):

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
    def from_mol(cls, mol, coord_unit="Angstroms", calculator=None):
        from ..Data import UnitsData

        if calculator is None and mol.energy_evaluator is not None:
            calculator = mol.get_energy_evaluator().to_ase()

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

    default_optimizer = 'bfgs'
    def resolve_optimizer(self, method):
        if method is None:
            method = self.default_optimizer
        if isinstance(method, str):
            optimize = ASEInterface.submodule('optimize')
            if method == 'bfgs':
                method = optimize.BFGS
            elif method == 'bfgs-linesearch':
                method = optimize.BFGSLineSearch
            else:
                method = getattr(optimize, method)
        return method

    convergence_criterion = 1e-4
    max_steps = 100
    def optimize_structure(self,
                           geoms=None,
                           calc=None,
                           quiet=True,
                           logfile=None,
                           fmax=None,
                           steps=None,
                           method=None,
                           **opts):
        BFGS = self.resolve_optimizer(method)

        if logfile is None:
            if quiet:
                logfile = io.StringIO()
            else:
                logfile = sys.stdout

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

    def prep_trajectory_images(self, geoms, calc=None):
        info = self.mol.info
        if calc is None:
            calc = self.mol.calc
        return [
            self.from_atoms(g,
                            calculator=calc if g.calc is None else None,
                            charge=info.get('charge')
                            )
                if hasattr(g, 'calc') and not hasattr(g, 'coords') else
            g
                if hasattr(g, 'coords') else
                    self.from_coords(
                        self.atoms,
                        g,
                        calc=calc,
                        **info
                    )
            for g in geoms
        ]

    default_mep = 'neb'
    def resolve_trajectory_method(self, method, **opts):
        if method is None:
            method = self.default_optimizer

        if isinstance(method, str):
            import ase.mep as mep
            # mep = ASEInterface.submodule('mep')
            if method == 'neb':
                method = mep.NEB
            elif method == 'dimer':
                method = mep.DimerControl
            else:
                method = getattr(mep, method)
        return method

    def prep_trajectory_type(self, geoms, method, calc=None, in_place=False, optimizer_method=None, **opts):
        if isinstance(method, dict):
            opts = method.copy() | opts
            method = opts.pop('method')

        if optimizer_method is not None:
            opts['method'] = optimizer_method

        method = self.resolve_trajectory_method(method)

        images = self.prep_trajectory_images(geoms, calc=calc)
        if not in_place:
            images = [i.copy() for i in images]
        images = [i.mol for i in images]

        if calc is not None:
            for i in images:
                i.calc = calc

        return method(images, **opts), images

    def optimize_trajectory(self,
                            geoms,
                            method,
                            calc=None,
                            quiet=True,
                            logfile=None,
                            fmax=None,
                            steps=None,
                            optimizer=None,
                            optimizer_method=None,
                            in_place=False,
                            return_coords=True,
                            **opts):
        optimizer = self.resolve_optimizer(optimizer)

        traj, images = self.prep_trajectory_type(geoms, method, calc=calc,
                                                 in_place=in_place,
                                                 optimizer_method=optimizer_method)

        if logfile is None:
            if quiet:
                logfile = io.StringIO()
            else:
                logfile = sys.stdout

        opt_rea = optimizer(traj, logfile=logfile, **opts)
        if fmax is None:
            fmax = self.convergence_criterion
        if steps is None:
            steps = self.max_steps
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