from .d3 import D3
from ..JHTML.WidgetTools import frozendict
__all__ = ['RendererD3', 'FigureManagerD3', 'FigureCanvasD3', '_BackendD3']
__reload_hook__ = ['..JHTML', '.d3']
import uuid, hashlib, itertools, io, base64, numpy as np
from PIL import Image
import matplotlib as mpl
from matplotlib import font_manager as fm
from matplotlib.backend_bases import _Backend, FigureCanvasBase, FigureManagerBase, RendererBase
from matplotlib.colors import rgb2hex
from matplotlib.path import Path
from matplotlib import _path
from matplotlib.transforms import Affine2D, Affine2DBase

class RendererD3(RendererBase):
    """
    A modification of the base matplotlib SVG renderer to plug into the D3 library work we've done
    """
    _capstyle_d = {'projecting': 'square', 'butt': 'butt', 'round': 'round'}

    @staticmethod
    def _short_float_fmt(x):
        """
        Create a short string representation of a float, which is %f
        formatting with trailing zeros and the decimal point removed.
        """
        ...

    @staticmethod
    def _generate_transform(transform_list):
        ...

    def __init__(self, width, height, basename=None, image_dpi=72, *, metadata=None):
        ...

    def open_group(self, s, gid=None):
        ...

    def close_group(self, s):
        ...

    def write_defs(self):
        ...

    def _make_id(self, type, content):
        ...

    def _make_flip_transform(self, transform):
        ...

    def _get_hatch(self, gc, rgbFace):
        """
        Create a new hatch pattern
        """
        ...

    def _write_hatches(self):
        ...

    def _get_style_dict(self, gc, rgbFace):
        """Generate a style string from the GraphicsContext and rgbFace."""
        ...

    def _get_style(self, gc, rgbFace):
        ...

    def _get_clip_attrs(self, gc):
        ...

    def _write_clips(self):
        ...

    def option_image_nocomposite(self):
        ...

    def _convert_path(self, path, transform=None, clip=None, simplify=None, sketch=None):
        ...

    def draw_path(self, gc, path, transform, rgbFace=None):
        ...

    def draw_markers(self, gc, marker_path, marker_trans, path, trans, rgbFace=None):
        ...

    def draw_path_collection(self, gc, master_transform, paths, all_transforms, offsets, offset_trans, facecolors, edgecolors, linewidths, linestyles, antialiaseds, urls, offset_position):
        ...

    def option_scale_image(self):
        ...

    def get_image_magnification(self):
        ...

    def draw_image(self, gc, x, y, im, transform=None):
        ...

    def _update_glyph_map_defs(self, glyph_map_new):
        """
        Emit definitions for not-yet-defined glyphs, and record them as having
        been defined.
        """
        ...

    def _adjust_char_id(self, char_id):
        ...

    def _draw_text_as_path(self, gc, x, y, s, prop, angle, ismath, mtext=None):
        ...

    def _draw_text_as_text(self, gc, x, y, s, prop, angle, ismath, mtext=None):
        ...
    text_as_path = False

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        ...

    def flipy(self):
        ...

    def get_canvas_width_height(self):
        ...

    def get_text_width_height_descent(self, s, prop, ismath):
        ...

    def get_toplevel(self):
        ...

    def insert_d3(self, root: 'D3.Frame'):
        """
        width='%spt' % str_width,
        height='%spt' % str_height,
        viewBox='0 0 %s %s' % (str_width, str_height),
        xmlns="http://www.w3.org/2000/svg",
        version="1.1",
        attrib={'xmlns:xlink': "http://www.w3.org/1999/xlink"}
        :param root:
        :return:
        """
        ...

class FigureManagerD3(FigureManagerBase):
    """
    Manages a set of D3 canvases by providing a
    """

    def __init__(self, canvas: 'FigureCanvasD3', num):
        ...

    def show(self):
        ...

    def full_screen_toggle(self):
        ...

    def get_window_title(self):
        ...

    def set_window_title(self, title):
        ...

    def resize(self, width, height):
        ...

class FigureCanvasD3(FigureCanvasBase):
    """
    The canvas the figure renders into.  Calls the draw and print fig
    methods, creates the renderers, etc.

    Note: GUI templates will want to connect events for button presses,
    mouse movements and key presses to functions that call the base
    class methods button_press_event, button_release_event,
    motion_notify_event, key_press_event, and key_release_event.  See the
    implementations of the interactive backends for examples.

    Attributes
    ----------
    figure : `~matplotlib.figure.Figure`
        A high-level Figure instance
    """
    manager_class = FigureManagerD3

    def __init__(self, figure=None, manager=None):
        ...

    def draw(self, clear=False):
        """
        Draw the figure using the renderer.

        It is important that this method actually walk the artist tree
        even if not output is produced because this will trigger
        deferred work (like computing limits auto-limits and tick
        values) that users may want access to before saving to disk.
        """
        ...

    @classmethod
    def render_objects(cls, figure, obj):
        ...

@_Backend.export
class _BackendD3(_Backend):
    FigureCanvas = FigureCanvasD3
    FigureManager = FigureManagerD3