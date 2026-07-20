from nbconvert.preprocessors.extractoutput import *

class MarkdownImageExtractor(ExtractOutputPreprocessor):
    """
    Extracts all of the outputs from the notebook file.  The extracted
    outputs are returned in the 'resources' dictionary.
    """

    def __init__(self, *args, prefix='', **kwargs):
        ...

    def reencode_data(self, mime_type, data):
        ...

    def save_attachement(self, filename, attachement, index, cell, resources, cell_index):
        ...

    def preprocess_cell(self, cell, resources, cell_index):
        ...