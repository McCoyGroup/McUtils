"""
This provides a unified interface for handling "surfaces" i.e. functions that map from coordinate space to the real line
The interface provides multiple different modes of surface specification, allowing for Taylor series data,
expansions basis expansions, or analytic representations.
The idea is to provide a unified interface that represents the _concept_ while allowing for flexibility in implementation.
Specific types of surfaces, like PES and dipole surfaces can be layered on top as superclasses and provided their own bespoke importers.
"""
__all__ = ['BaseSurface', 'TaylorSeriesSurface', 'InterpolatedSurface', 'Surface', 'MultiSurface', 'sphere_points', 'SphereUnionSurface', 'SphereUnionSurfaceMesh', 'marching_cubes']
from .BaseSurface import *
from .Surface import *
from .SphereUnionSurface import *
from .MarchingCubesSurface import *