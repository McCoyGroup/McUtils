import numpy as np
__all__ = ['MoleculeGraphics']

class MoleculeGraphics:

    def __init__(self, atoms, coords, bonds=None, displacements=None, displacement_range=(-1, 1), displacement_steps=5, name='Molecule', program='Python', comment='', metadata=None, **params):
        ...

    def to_widget(self):
        ...

    def show(self):
        ...

    def _ipython_display_(self):
        ...

    @classmethod
    def _load_nglview(cls):
        ...