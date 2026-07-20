"""
Convenience classes for hooking into the matplotlib animation framework
"""
from .Graphics import GraphicsBase, Graphics
__all__ = ['EventHandler', 'Animator']

class EventHandler:

    def __init__(self, figure, on_click=None, on_release=None, on_draw=None, on_key_press=None, on_key_release=None, on_move=None, on_select=None, on_resize=None, on_scroll=None, on_figure_entered=None, on_figure_left=None, on_axes_entered=None, on_axes_left=None):
        """Creates an EventHandler on a Figure that handles most interactivity stuff

        :param figure:
        :type figure: GraphicsBase
        :param on_click:
        :type on_click:
        :param on_release:
        :type on_release:
        :param on_draw:
        :type on_draw:
        :param on_key_press:
        :type on_key_press:
        :param on_key_release:
        :type on_key_release:
        :param on_move:
        :type on_move:
        :param on_select:
        :type on_select:
        :param on_resize:
        :type on_resize:
        :param on_scroll:
        :type on_scroll:
        :param on_figure_entered:
        :type on_figure_entered:
        :param on_figure_left:
        :type on_figure_left:
        :param on_axes_entered:
        :type on_axes_entered:
        :param on_axes_left:
        :type on_axes_left:
        """
        ...

    def bind(self, **handlers):
        ...

    @property
    def handlers(self):
        ...

    class Event:

        def __init__(self, event_handler, handler, filter=None, update=True, name=None):
            ...

        @property
        def data(self):
            ...

        def handle_event(self, event):
            ...

        def __call__(self, *args, **kwargs):
            ...

    def ButtonPressedEvent(self, handler, **kw):
        ...

    def ButtonReleasedEvent(self, handler, **kw):
        ...

    def DrawEvent(self, handler, **kw):
        ...

    def KeyPressedEvent(self, handler, **kw):
        ...

    def KeyReleasedEvent(self, handler, **kw):
        ...

    def MoveEvent(self, handler, **kw):
        ...

    def SelectEvent(self, handler, **kw):
        ...

    def ScrollEvent(self, handler, **kw):
        ...

    def FigureEnterEvent(self, handler, **kw):
        ...

    def FigureLeaveEvent(self, handler, **kw):
        ...

    def AxesEnterEvent(self, handler, **kw):
        ...

    def AxesLeaveEvent(self, handler, **kw):
        ...

class Animator:

    def __init__(self, figure, data_generator, plot_method=None, events=True, update=False, **anim_ops):
        ...

    def _get_plot_method(self, figure, plot_method):
        ...

    @property
    def active(self):
        ...

    @active.setter
    def active(self, val):
        ...

    def start(self):
        ...

    def stop(self):
        ...

    def toggle(self):
        ...

    def show(self):
        ...

    def to_jshtml(self):
        """
        Delegates to the underlying animation
        :return:
        :rtype:
        """
        ...

    def to_html5_video(self):
        """
        Delegates to the underlying animation
        :return:
        :rtype:
        """
        ...

    def as_jupyter_animation(self, mode='javascript'):
        """
        Chains some stuff to make Jupyter animations work
        :return:
        :rtype:
        """
        ...