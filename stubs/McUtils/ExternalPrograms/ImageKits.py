"""
Provides support for chemical toolkits
"""
import io
import base64
from .Interface import *
__all__ = ['PILInterface', 'OpenCVInterface']

class PILInterface(ExternalProgramInterface):
    """
    A simple class to support operations that make use of the OpenCV toolkit
    """
    name = 'PIL'
    module = 'PIL'

    @classmethod
    def from_file(cls, file, **opts):
        ...

    @classmethod
    def from_url(cls, url):
        ...

    @classmethod
    def to_url(cls, image, format='png'):
        ...

    @classmethod
    def prep_url_buffer(cls, img_data: str, format=None):
        ...

class OpenCVInterface(ExternalProgramInterface):
    """
    A simple class to support operations that make use of the PIL toolkit
    """
    name = 'OpenCV'
    module = 'cv2'