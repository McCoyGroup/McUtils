import uuid
import numpy as np
import re
import functools
import base64
import io
from .. import Devutils as dev
from . import JHTML
from .JHTML import CSS
__all__ = ['DisplayImage']

class DisplayImage:

    def __init__(self, figure, format, plot_range=None, scaling_factor=None, splits=None, postdraw=None, include_save_buttons=False, id=None):
        ...

    @classmethod
    def split_string_by_segments(cls, text, split_dict):
        ...

    @classmethod
    def _path_addition_function(cls, xml_modifier):
        ...

    @classmethod
    def _text_addition_function(cls, text, mode='svg', font_options=None, **modifiers):
        ...

    @classmethod
    def _text_to_path(cls, text, **font_opts):
        ...

    @classmethod
    def _path_to_svg(cls, path, target_bbox: tuple[tuple[float, float], tuple[float, float]], base_height=None, y_flip: bool=True):
        ...
    multivalue_attrs = {'class'}

    @classmethod
    def _prep_svg_val(cls, attr, old, val):
        ...

    @classmethod
    def _apply_attr_tf(cls, attr, rest, value):
        ...

    @classmethod
    def _inject_attr(cls, tag, body, attr, value):
        ...

    @classmethod
    def _find_end_tag(cls, text, tag_start, end_tag1, end_tag2, closer_tag):
        ...

    @classmethod
    def _iter_xml_chunk(cls, text: str):
        ...

    @classmethod
    def _tranform_single(cls, t, transformation):
        ...

    @classmethod
    def _transform_svg(cls, text, transformation):
        ...

    @classmethod
    def add_classes(cls, label, text):
        ...

    @classmethod
    def _attr_annotation_function(cls, attr, value):
        ...
    default_annotation_pattern = None
    default_annotation_exclude = 'mol-\\w+'

    @classmethod
    def _prep_annotation_function(cls, attrs_dict):
        ...

    @classmethod
    def annotate_text(cls, text, splits, annotation_map=None):
        ...

    def postprocess(self, text):
        ...

    @property
    def text(self):
        ...

    @classmethod
    def get_svg_script(self, id):
        ...

    @classmethod
    def get_png_from_svg_script(self, id):
        ...

    @classmethod
    def get_png_script(self, id):
        ...

    def to_widget(self):
        ...

    def _ipython_display_(self):
        ...

    def show(self):
        ...

    def save(self, file):
        ...