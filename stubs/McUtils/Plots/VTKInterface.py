"""
Provides an interface to VTK that implements all necessary components with a matplotlib compatible API
"""
from ..ExternalPrograms import VTKInterface as vtk
__all__ = ['VTKWindow', 'VTKPrimitive', 'VTKGeometricPrimitive', 'VTKSphere', 'VTKDisk', 'VTKCylinder', 'VTKLine', 'VTKObject']

class VTKObject:
    """A general wrapper for _any_ vtk object that provides a more pythonic interface and can be extended to be add     layers of functionality

    :param obj: any kind of low-level vtk object that exposes a Set/Get interface
    :type obj: Any
    """

    def __init__(self, obj):
        ...

    def chain_to(self, src):
        ...

    def __getattr__(self, item):
        ...

    @staticmethod
    def _HTMLColorToRGB(colorString):
        """
        Convert #RRGGBB to a [R, G, B] list.
        :param: colorString a string in the form: #RRGGBB where RR, GG, BB are hexadecimal.
        The elements of the array rgb are unsigned chars (0..255).
        :return: The red, green and blue components as a list.
        """
        ...

    @classmethod
    def color_tuple(cls, c):
        ...

    def _get_prop(self, item, default_prefix='Get'):
        """To simplify the API a bit we add property-like retrievers for a general Get/Set attribute structure"""
        ...

    def get_prop(self, item):
        ...

    def set_prop(self, item, val):
        ...

    def _get_color(self):
        ...

    def _get_background(self):
        ...
    _prop_getters = {'color': _get_color, 'background': _get_background}

    def _set_color(self, c):
        ...

    def _set_background(self, c):
        ...
    _prop_setters = {'color': _set_color, 'background': _set_background}

    def __getitem__(self, item):
        ...

    def __setitem__(self, key, value):
        ...

class VTKRenderer(VTKObject):

    def __init__(self):
        ...

class VTKRenderWindow(VTKObject):

    def __init__(self):
        ...

class VTKRenderWindowInteractor(VTKObject):

    def __init__(self):
        ...

class VTKActor(VTKObject):

    def __init__(self, actor='', name=None):
        ...

class VTKWrapper:
    """Provides something that *looks* like a lower-level actor but is not
    Requires a setter, getter, and a property object
    """

    def __init__(self, get_val, set_val, prop):
        ...

    @property
    def val(self):
        ...

    @val.setter
    def val(self, v):
        ...

    def __getattr__(self, item):
        ...

class VTKTicks:

    def __init__(self, major_ticks, minor_ticks):
        ...

class VTKAxis:

    def __init__(self, lines, title, label):
        ...

    def set_prop(self, c, v):
        ...

    def get_prop(self, c):
        ...

    def __getitem__(self, item):
        ...

    def __setitem__(self, key, value):
        ...

class VTKCubeAxes(VTKActor):

    def __init__(self):
        ...

    @property
    def x_axis(self):
        ...

    @property
    def y_axis(self):
        ...

    @property
    def z_axis(self):
        ...

    @property
    def axes(self):
        ...

    @property
    def color(self):
        ...

    @color.setter
    def color(self, colors):
        ...

class VTKWindow:
    """Handles all communication with a vtkRenderWindow object
    Creates a vtkRenderer and vtkRenderInteractor and the rest of it to manage this

    """

    def __init__(self, title=None, legend=None, window=None, cube=None, use_axes=True, interactor=None, renderer=None, background='white', image_size=(640, 480), viewpoint=(5, 5, 5), focalpoint=(0, 0, 0), scale=(1, 1, 1)):
        ...

    def add_object(self, thing):
        ...

    def _remove_obj(self, thing):
        ...

    def remove_object(self, thing):
        ...

    def clear(self):
        ...

    def close(self):
        ...

    @property
    def window(self):
        ...

    @property
    def interactor(self):
        ...

    def setup_interactor(self):
        ...

    @property
    def renderer(self):
        ...

    def setup_renderer(self):
        ...

    def _not_imped_warning(self, method):
        ...

    def set_size(self, w, h):
        ...

    def set_size_inches(self, wi, hi):
        ...

    def get_size_inches(self):
        ...

    def get_title(self):
        ...

    def set_title(self, title):
        ...

    def get_lims(self):
        ...

    def get_xlim(self):
        ...

    def set_xlim(self, x):
        ...

    def get_ylim(self):
        ...

    def set_ylim(self, y):
        ...

    def get_zlim(self):
        ...

    def set_zlim(self, z):
        ...

    def get_xlabel(self):
        ...

    def set_xlabel(self, lab, **ops):
        ...

    def get_ylabel(self):
        ...

    def set_ylabel(self, lab, **ops):
        ...

    def get_zlabel(self):
        ...

    def set_zlabel(self, lab, **ops):
        ...

    def get_xticks(self):
        ...

    def set_xticks(self, lab):
        ...

    def get_yticks(self):
        ...

    def set_yticks(self, lab):
        ...

    def get_zticks(self):
        ...

    def set_zticks(self, lab):
        ...

    def set_model_matrix(self):
        ...

    def get_xscale(self):
        ...

    def set_xscale(self, lab):
        ...

    def get_yscale(self):
        ...

    def set_yscale(self, lab):
        ...

    def get_zscale(self):
        ...

    def set_zscale(self, lab):
        ...

    def get_legend(self):
        ...

    def set_legend(self, l):
        ...

    def get_facecolor(self):
        ...

    def set_facecolor(self, bg):
        ...

    @property
    def camera(self):
        ...

    @camera.setter
    def camera(self, cam):
        ...

    def set_viewpoint(self, vp):
        ...

    def set_focalpoint(self, fp):
        ...

    def set_background(self, bg):
        ...

    def show(self):
        ...

class VTKPrimitive:

    def __init__(self, get_mapper, name, color=None, parent=None):
        ...

    @property
    def actor(self):
        ...

    @staticmethod
    def _setup_actor(mapper):
        ...

    @staticmethod
    def _setup_mapper(source):
        ...

    def get_actor(self):
        ...

    def get_mapper(self):
        ...

    def plot(self, window):
        ...

class VTKGeometricPrimitive(VTKPrimitive):

    def __init__(self, source, name, **opts):
        ...

    def _get_mapper(self):
        ...

class VTKDisk(VTKGeometricPrimitive):

    def __init__(self, pos, rad, **opts):
        ...

class VTKLine(VTKGeometricPrimitive):

    def __init__(self, pt1, pt2, **opts):
        ...

class VTKCylinder(VTKGeometricPrimitive):

    def __init__(self, pt1, pt2, rad, cylinder_points=24, **opts):
        ...

class VTKSphere(VTKGeometricPrimitive):

    def __init__(self, pos, rad, theta_points=24, phi_points=24, **opts):
        ...