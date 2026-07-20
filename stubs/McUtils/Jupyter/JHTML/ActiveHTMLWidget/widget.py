from ipywidgets import Widget, DOMWidget, register, widget_serialization, CallbackDispatcher
from traitlets import Unicode, Bool, Instance, Dict, List
from ipywidgets.widgets.trait_types import TypedTuple
from ._frontend import module_name, module_version

@register
class HTMLElement(DOMWidget):
    """
    Represents an HTML element that can be interacted with
    and configured richly, in contrast to the limited interactions
    available in most core Jupyter widgets
    """
    _model_name = Unicode('ActiveHTMLModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('ActiveHTMLView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    tagName = Unicode('div').tag(sync=True)
    classList = List().tag(sync=True)
    styleDict = Dict().tag(sync=True)
    unsyncedProps = List().tag(sync=True)
    elementAttributes = Dict().tag(sync=True, **widget_serialization)
    innerHTML = Unicode('').tag(sync=True)
    textContent = Unicode('').tag(sync=True)
    children = TypedTuple(trait=Instance(Widget)).tag(sync=True, **widget_serialization)
    id = Unicode('').tag(sync=True)
    value = Unicode('').tag(sync=True)
    exportData = Dict().tag(sync=True, **widget_serialization)
    trackInput = Bool(False).tag(sync=True)
    continuousUpdate = Bool(True).tag(sync=True)
    eventPropertiesDict = Dict().tag(sync=True)
    jsHandlers = Dict().tag(sync=True)
    jsAPI = Instance(Widget, allow_none=True).tag(sync=True, **widget_serialization)
    onevents = Dict().tag(sync=True)
    _debugPrint = Bool(False).tag(sync=True)

    def __init__(self, **kwargs):
        ...

    def _handle(self, _, msg, __):
        ...

    def bind_callback(self, callback, remove=False):
        """Register a callback to execute when a DOM event occurs.
        The callback will be called with one argument, an dict whose keys
        depend on the type of event.
        Parameters
        ----------
        remove: bool (optional)
            Set to true to remove the callback from the list of callbacks.
        """
        ...

    def reset_callbacks(self):
        """Remove any previously defined callback."""
        ...

    def __repr__(self):
        ...
    _here = __file__

    @classmethod
    def jupyterlab_install(self, exec_prefix=None, overwrite=False):
        """
        Attempts to do a basic installation for JupterLab
        :return:
        :rtype:
        """
        ...

    @classmethod
    def jupyternb_install(self, exec_prefix=None, overwrite=False):
        """
        Attempts to do a basic installation for JupterLab
        :return:
        :rtype:
        """
        ...

    def trigger(self, event, content=None, buffers=None):
        ...

    def call(self, method, content=None, buffers=None):
        ...