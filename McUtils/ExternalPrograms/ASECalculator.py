from ase.calculators.calculator import Calculator, all_changes

__all__ = [
    'ASETermCalculator'
]

class ASETermCalculator(Calculator):
    def __init__(self,
                 term_evaluator,
                 charge_evaluator=None,
                 dipole_evaluator=None,
                 analytic_derivative_order=None,
                 charge_derivative_order=None,
                 dipole_derivative_order=None,
                 implemented_properties=None,
                 **kwargs):
        super().__init__()
        self.evaluator = term_evaluator
        self.dipole_evaluator = dipole_evaluator
        self.charge_evaluator = charge_evaluator
        if implemented_properties is None:
            implemented_properties = self.resolve_implemented_properties(analytic_derivative_order,
                                                                         charge_evaluator=charge_evaluator,
                                                                         dipole_evaluator=dipole_evaluator,
                                                                         charge_derivative_order=charge_derivative_order,
                                                                         dipole_derivative_order=dipole_derivative_order)
        self.implemented_properties = implemented_properties
        self.kwargs = kwargs

    @classmethod
    def resolve_implemented_properties(cls,
                                       analytic_derivative_order,
                                       charge_evaluator=None,
                                       dipole_evaluator=None,
                                       charge_derivative_order=None,
                                       dipole_derivative_order=None):
        props = []
        if analytic_derivative_order is None:
            props.extend(['energy', 'forces'])
        elif analytic_derivative_order >= 0:
            for i in range(analytic_derivative_order+1):
                if i == 0:
                    props.append('energy')
                elif i == 1:
                    props.append('forces')
                elif i == 2:
                    props.append('hessians')
                else:
                    props.append(f'energy_derivative_{i}')

        if charge_evaluator is not None:
            if charge_derivative_order is None:
                props.extend(['charges'])
            else:
                for i in range(charge_derivative_order+1):
                    if i == 0:
                        props.append('charges')
                    else:
                        props.append(f'charges_derivative_{i}')



        if dipole_evaluator is not None:
            if dipole_derivative_order is None:
                props.extend(['dipole'])
            else:
                for i in range(dipole_derivative_order+1):
                    if i == 0:
                        props.append('dipole')
                    else:
                        props.append(f'dipole_derivative_{i}')

        return props


    def _calc_energy_term(self, atoms, order, **kwargs):
        return self.evaluator(atoms, order, **(self.kwargs | kwargs))
    def _calc_energy(self, atoms, **kwargs):
        return self._calc_energy_term(atoms, 0, **kwargs)
    def _calc_forces(self, atoms, **kwargs):
        return -self._calc_energy_term(atoms, 1, **kwargs)
    def _calc_hessians(self, atoms, **kwargs):
        return self._calc_energy_term(atoms, 2, **kwargs)

    def _calc_dipole_term(self, atoms, order, **kwargs):
        return self.dipole_evaluator(atoms, order, **(self.kwargs | kwargs))
    def _calc_dipole(self, atoms, **kwargs):
        return self._calc_dipole_term(atoms, 0, **kwargs)

    def _calc_charge_term(self, atoms, order, **kwargs):
        return self.charge_evaluator(atoms, order, **(self.kwargs | kwargs))
    def _calc_charges(self, atoms, **kwargs):
        return self._calc_charge_term(atoms, 0, **kwargs)

    def _dispatch_calculate(self, property, atoms):
        if property == 'energy':
            return self._calc_energy(atoms)
        elif property == 'forces':
            return self._calc_forces(atoms)
        elif property in ['hessians', 'energy_derivative_2']:
            return self._calc_hessians(atoms)
        elif property == 'dipole':
            return self._calc_dipole(atoms)
        elif property == 'charges':
            return self._calc_charges(atoms)
        elif property.startswith('energy_derivative_'):
            return self._calc_energy_term(atoms, int(property.split("_", 2)[-1]))
        elif property.startswith('dipole_derivative_'):
            return self._calc_dipole_term(atoms, int(property.split("_", 2)[-1]))
        elif property.startswith('charges_derivative_'):
            return self._calc_charge_term(atoms, int(property.split("_", 2)[-1]))
        else:
            raise ValueError(f"Unknown property {property}")

    def calculate(self, atoms=None, properties=['energy'], system_changes=all_changes):
        super().calculate(atoms, properties, system_changes)

        #TODO: allow reuse of previous props for caching
        results = {}
        for prop in properties:
            results[prop] = self._dispatch_calculate(prop, atoms)

        return results