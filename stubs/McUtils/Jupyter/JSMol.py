import uuid
from .JHTML import HTML
__all__ = ['JSMol']
__reload_hooks__ = ['.JHTML']

class JSMol:

    class Applet(HTML.Div):
        version = '16.3.7.9'
        jsmol_source = f'https://cdn.jsdelivr.net/gh/b3m2a1/jsmol-cdn@{version}/jsmol/JSmol.min.js'
        jmol2_source = f'https://cdn.jsdelivr.net/gh/b3m2a1/jsmol-cdn@{version}/jsmol/js/Jmol2.js'
        unsynced_properties = ['width', 'height']

        @classmethod
        def load_applet_script(cls, id, loader, include_script_interface=False, interface_target='', recording_options=None, target=None):
            ...

        def __init__(self, *model_etc, width=500, height=500, animate=False, vibrate=False, load_script=None, suffix=None, id=None, dynamic_loading=None, include_script_interface=False, recording_options=None, create_applet_loader=None, style=None, autobond=False, **attrs):
            ...

        @property
        def applet_target(self):
            ...

        def prep_load_script(self):
            ...

        def create_applet(self, model_file, include_script_interface=False):
            ...

        def show(self):
            ...