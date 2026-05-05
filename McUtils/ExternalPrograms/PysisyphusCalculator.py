from McUtils.Data import UnitsData
from pysisyphus.calculators.Calculator import Calculator

class PysisyphusTermCalculator(Calculator):
    def __init__(self,
                 term_evaluator,
                 batched_orders=False,
                 distance_units=None,
                 energy_units=None,
                 **kwargs):
        super().__init__()
        self.evaluator = term_evaluator
        self.batched_orders = batched_orders
        self.distance_units = distance_units
        self.energy_units = energy_units
        self.kwargs = kwargs

    def get_energy(self, atoms, coords):
        if self.distance_units is not None:
            dist_conv = UnitsData.convert("BohrRadius", self.distance_units)
        else:
            dist_conv = 1
        if self.energy_units is not None:
            energy_conv = UnitsData.convert(self.energy_units, "Hartrees")
        else:
            energy_conv = 1
        res = self.evaluator(coords * dist_conv, 0, **self.kwargs)
        if self.batched_orders:
            res = res[0]
        return dict(energy=res * energy_conv)

    def get_forces(self, atoms, coords):
        if self.distance_units is not None:
            dist_conv = UnitsData.convert("BohrRadius", self.distance_units)
        else:
            dist_conv = 1
        if self.energy_units is not None:
            energy_conv = UnitsData.convert(self.energy_units, "Hartrees")
        else:
            energy_conv = 1
        res = self.evaluator(coords, 1, **self.kwargs)
        if self.batched_orders:
            energy, grad = res
        else:
            grad = res
            energy = self.evaluator(res, 0, **self.kwargs)
        return dict(energy=energy * energy_conv, forces=-grad * energy_conv / dist_conv)

    def get_hessian(self, atoms, coords):
        if self.distance_units is not None:
            dist_conv = UnitsData.convert("BohrRadius", self.distance_units)
        else:
            dist_conv = 1
        if self.energy_units is not None:
            energy_conv = UnitsData.convert(self.energy_units, "Hartrees")
        else:
            energy_conv = 1
        res = self.evaluator(coords, 2, **self.kwargs)
        if self.batched_orders:
            energy, grad, hess = res
        else:
            hess = res
            grad = self.evaluator(res, 1, **self.kwargs)
            energy = self.evaluator(res, 0, **self.kwargs)
        return dict(energy=energy * energy_conv,
                    forces=-grad * energy_conv / dist_conv,
                    hessian=hess * energy_conv / dist_conv**2)

