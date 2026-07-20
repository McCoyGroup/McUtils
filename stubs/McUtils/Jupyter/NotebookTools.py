import os
import re
import json
from .. import Devutils as dev
from .JHTML import JHTML
from ..ExternalPrograms import PILInterface
__all__ = ['NotebookReader']

class NotebookReader:

    def __init__(self, json_or_fp):
        ...

    class NotebookCell:

        def __init__(self, nb: 'NotebookReader', cell_data):
            ...

        @property
        def cell_type(self):
            ...

        @property
        def cell_index(self):
            ...

        def __repr__(self):
            ...

        @property
        def attachments(self):
            ...

        def get_images(self):
            ...

        @property
        def source(self):
            ...

        @property
        def text(self):
            ...

        @classmethod
        def get_cell_header(cls, data):
            ...

        @property
        def cell_header(self):
            ...

        @property
        def html(self):
            ...

        @classmethod
        def prep_attachments(cls, nb, attachment_data):
            ...

    def cell(self, data):
        ...

    def get_mime_image_loader(self, img_type):
        ...

    def get_mime_type_loader(self, mime_type):
        ...

    class CellList:

        def __init__(self, nb: 'NotebookReader', cell_list):
            ...

        def __repr__(self):
            ...

        def __len__(self):
            ...

        def __iter__(self):
            ...

        def __getitem__(self, item):
            ...

        def modify(self, cells=None, *, nb=None):
            ...

        def filter_cells(self, filter):
            ...

        def find_cells_by_type(self, pattern):
            ...

        def _match_header(self, pattern, data):
            ...

        def find_cells_by_header(self, pattern):
            ...

        def find_cells_with_attachments(self, pattern=None):
            ...

        @classmethod
        def prep_regex(self, pattern, flags=None):
            ...

    def cell_list(self, cells=None):
        ...

    def __repr__(self):
        ...

    def load_notebook(self, nb_js):
        ...

    def get_notebook_name(self, nb_js=None):
        ...

    @property
    def file_name(self):
        ...

    @property
    def nb_json(self):
        ...

    @classmethod
    def get_notebook_files(cls, directory='.'):
        ...

    @classmethod
    def sort_by_evaluation_time(cls, file_list, directory='.'):
        ...

    @classmethod
    def active_notebook(cls, directory='.'):
        ...