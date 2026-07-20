from ase.calculators.calculator import Calculator, all_changes
__all__ = ['ASETermCalculator']

class ASETermCalculator(Calculator):

    def __init__(self, term_evaluator, charge_evaluator=None, dipole_evaluator=None, analytic_derivative_order=None, charge_derivative_order=None, dipole_derivative_order=None, implemented_properties=None, **kwargs):
        ...

    @classmethod
    def resolve_implemented_properties(cls, analytic_derivative_order, charge_evaluator=None, dipole_evaluator=None, charge_derivative_order=None, dipole_derivative_order=None):
        ...

    def _calc_energy_term(self, atoms, order, **kwargs):
        ...

    def _calc_energy(self, atoms, **kwargs):
        ...

    def _calc_forces(self, atoms, **kwargs):
        ...

    def _calc_hessians(self, atoms, **kwargs):
        ...

    def _calc_dipole_term(self, atoms, order, **kwargs):
        ...

    def _calc_dipole(self, atoms, **kwargs):
        ...

    def _calc_charge_term(self, atoms, order, **kwargs):
        ...

    def _calc_charges(self, atoms, **kwargs):
        ...

    def _dispatch_calculate(self, property, atoms):
        ...

    def calculate(self, atoms=None, properties=['energy'], system_changes=all_changes):
        ...