from McUtils.Data import UnitsData
from pysisyphus.calculators.Calculator import Calculator

class PysisyphusTermCalculator(Calculator):

    def __init__(self, term_evaluator, batched_orders=False, distance_units=None, energy_units=None, **kwargs):
        ...

    def get_energy(self, atoms, coords):
        ...

    def get_forces(self, atoms, coords):
        ...

    def get_hessian(self, atoms, coords):
        ...