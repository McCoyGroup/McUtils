__all__ = ['JupyterAPIs', 'DefaultOutputWidget']

class JupyterAPIs:
    """
    Provides access to the various Jupyter APIs
    """
    _apis = None

    @classmethod
    def load_api(cls):
        ...

    @classmethod
    def get_shell_api(cls):
        ...

    @classmethod
    def get_shell_instance(cls):
        ...

    @classmethod
    def get_base_api(cls):
        ...

    @classmethod
    def in_jupyter_environment(cls):
        ...

    @classmethod
    def get_display_api(cls):
        ...

    @property
    def display_api(self):
        ...

    @classmethod
    def get_widgets_api(self):
        ...

    @property
    def widgets_api(self):
        ...

    @classmethod
    def get_events_api(self):
        ...

    @property
    def events_api(self):
        ...

class DefaultOutputWidget:
    _output_area_stack = []

    @classmethod
    def _get_output_pane(cls):
        ...

    def __init__(self, obj=None):
        ...

    @classmethod
    def get_default(cls):
        ...

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    def __call__(self, *args, **kwargs):
        ...

class frozendict(dict):

    def __hash__(self):
        ...

    def __setitem__(self, key, value):
        ...