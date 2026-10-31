"""Presentation backends for Apps. Native presentation uses Web Components.

The facade below is deliberately local to Apps; it does not alter JHTML or the
ActiveHTMLWidget implementation. Existing Bootstrap descriptors are translated
at this boundary, preserving the component and variable/callback APIs.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
from functools import lru_cache
import re
from ..JHTML import JHTML as _JHTML

__all__ = ['AppTheme']

_current = ContextVar('mcutils_app_theme', default='native')
_chosen = ContextVar('mcutils_app_theme_choice', default=None)
_mode = ContextVar('mcutils_app_render_mode', default='widget')
_depth = ContextVar('mcutils_app_render_depth', default=0)


class AppTheme:
    """An Apps presentation backend, independent of per-component color themes.

    Use ``ui_theme='bootstrap'`` on a component/App, or construct/render within
    ``with AppTheme('bootstrap'):``. Native presentation is the default.
    """
    names = ('native', 'bootstrap')
    _apis = {}
    bootstrap_css = 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css'
    bootstrap_js = 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js'

    def __init__(self, name='native'):
        if isinstance(name, AppTheme):
            name = name.name
        if name not in self.names:
            raise ValueError('Unknown Apps UI theme {!r}; expected {}'.format(name, self.names))
        self.name = name
        self._tokens = ContextVar('mcutils_app_theme_tokens_'+str(id(self)),default=())

    @classmethod
    def current(cls):
        return cls(_current.get())

    @classmethod
    def mode(cls):
        return _mode.get()

    @classmethod
    def selected(cls):
        return _chosen.get()

    def __enter__(self):
        self._tokens.set(self._tokens.get()+((_current.set(self.name),_chosen.set(self.name)),))
        return self

    def __exit__(self, *exc):
        stack=self._tokens.get();current,chosen=stack[-1];self._tokens.set(stack[:-1])
        _chosen.reset(chosen);_current.reset(current)

    @classmethod
    @contextmanager
    def rendering(cls, theme=None, mode=None):
        tokens = []
        if theme is not None:
            name=cls(theme).name
            tokens.append((_current,_current.set(name)))
            tokens.append((_chosen,_chosen.set(name)))
        if mode is not None:
            tokens.append((_mode, _mode.set(mode)))
        depth = _depth.get()
        tokens.append((_depth, _depth.set(depth+1)))
        try:
            yield cls.current(), depth == 0
        finally:
            for variable, token in reversed(tokens):
                variable.reset(token)

    def resources(self):
        """Static document dependencies; callers can deduplicate these elements."""
        H = _JHTML.HTML
        if self.name == 'bootstrap':
            return [H.Link(rel='stylesheet', href=self.bootstrap_css), H.Script(src=self.bootstrap_js),
                    H.Script("document.addEventListener('DOMContentLoaded',()=>{for(const el of document.querySelectorAll('[data-bs-toggle=tooltip],[data-bs-toggle=popover]')){const C=el.dataset.bsToggle==='tooltip'?window.bootstrap.Tooltip:window.bootstrap.Popover;C.getOrCreateInstance(el);}});")]
        return [H.Style(self.native_css(), id='mcutils-apps-native-css'),
                H.Script(self.native_script(), id='mcutils-apps-native-js')]

    @staticmethod
    def native_css():
        return Path(__file__).with_name('resources').joinpath('native.css').read_text()

    @staticmethod
    def native_script():
        return Path(__file__).with_name('resources').joinpath('native.js').read_text()

    def initializer(self):
        if self.name == 'native':
            import json
            return ("if(!document.getElementById('mcutils-apps-native-css')){const s=document.createElement('style');"
                    "s.id='mcutils-apps-native-css';s.textContent="+json.dumps(self.native_css())+";document.head.append(s);}\n"
                    +self.native_script()+"\nreturn window.McUtilsApps.mount(widget);")
        import json
        return """const css=%s,js=%s;
if(!document.querySelector('link[data-mcutils-bootstrap]')){const s=document.createElement('link');s.rel='stylesheet';s.href=css;s.dataset.mcutilsBootstrap='';document.head.append(s);}
if(!window.__mcutilsBootstrapReady)window.__mcutilsBootstrapReady=window.bootstrap?Promise.resolve(window.bootstrap):new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=js;s.onload=()=>resolve(window.bootstrap);s.onerror=reject;document.head.append(s);});
return window.__mcutilsBootstrapReady.then(b=>{for(const el of widget.el.querySelectorAll('[data-bs-toggle="tooltip"],[data-bs-toggle="popover"]')){const C=el.dataset.bsToggle==='tooltip'?b.Tooltip:b.Popover;C.getOrCreateInstance(el);}});
""" % (json.dumps(self.bootstrap_css), json.dumps(self.bootstrap_js))

    def javascript_api(self):
        if self.name not in self._apis:
            self._apis[self.name] = _JHTML.JavascriptAPI(
                mcui_mount=self.initializer(),
                mcui_refresh="widget.el.refresh?.();",
                mcui_remove="if(window.McUtilsApps)window.McUtilsApps.dispose(widget.el);")
        return self._apis[self.name]

    def decorate(self, element):
        """Notebook mount: retain the rendered child object and its callbacks."""
        return self.component('root', element, mode='widget',
                              cls=['mcui-root', 'mcui-'+self.name],
                              javascript_handles=self.javascript_api(),
                              onevents={'initialize': 'mcui_mount', 'remove': 'mcui_remove'})

    def component(self, name, *elements, mode=None, fallback='Div', **attrs):
        """Construct a native custom element, or its selected theme equivalent.

        Custom elements retain light-DOM children and existing widget models.
        Their browser lifecycle owns behavior; this Python boundary owns markup.
        """
        mode = self.mode() if mode is None else mode
        if self.name == 'bootstrap':
            return getattr(_JHTML.HTML if mode == 'static' else _JHTML, fallback)(*elements, **attrs)
        plain, widget = _component_classes('mcui-'+name)
        if mode == 'static':
            return plain(*elements, **attrs)
        return _JHTML._dispatch(plain, widget, *elements, **attrs)

    _classes = {
        'btn': 'button', 'form-control': 'input', 'form-range': 'range', 'form-select': 'select',
        'form-check-input': 'check', 'form-check': 'check-group', 'form-switch': 'switch',
        'list-group-item-action': 'action', 'navbar-expand': 'navbar-expand',
        'flex-column': 'column', 'd-flex': 'flex', 'd-inline-flex': 'inline-flex',
        'd-inline': 'inline', 'd-inline-block': 'inline-block', 'd-block': 'block', 'd-none': 'hidden',
        'me-auto': 'spacer', 'w-100': 'full-width', 'h-100': 'full-height',
    }
    _known = frozenset(('card card-header card-body card-footer card-img card-img-top '
                        'list-group list-group-flush list-group-item btn-group breadcrumb breadcrumb-item '
                        'progress progress-bar spinner-border spinner-grow navbar navbar-nav nav nav-item nav-link '
                        'nav-tabs tab-content tab-pane active show fade collapse collapsing accordion accordion-item '
                        'accordion-header accordion-button accordion-body accordion-collapse collapsed dropdown '
                        'dropdown-menu dropdown-item dropdown-toggle carousel carousel-inner carousel-item '
                        'carousel-control-prev carousel-control-next carousel-control-prev-icon carousel-control-next-icon '
                        'carousel-indicators pagination page-item page-link modal modal-dialog modal-content '
                        'modal-header modal-body modal-footer offcanvas offcanvas-header offcanvas-body '
                        'offcanvas-start offcanvas-end toast toast-header toast-body toast-container btn-close '
                        'tooltip tooltip-inner popover popover-header popover-body border border-top border-bottom '
                        'border-start border-end rounded overflow-auto text-muted text-center align-items-center '
                        'justify-content-between navbar-dark navbar-light').split())

    def classes(self, classes):
        if self.name == 'bootstrap':
            return classes
        out = []
        for token in _JHTML.manage_class(classes):
            if token in self._classes:
                token = 'mcui-'+self._classes[token]
            elif token in self._known or re.match(r'^(btn|bg|text|border|spinner)-(primary|secondary|success|danger|warning|info|light|dark|border|grow)$', token) or re.match(r'^[mp][setbxy]?-[0-5]$', token):
                token = 'mcui-'+token
            out.append(token)
        return out

    def attrs(self, attrs):
        attrs = dict(attrs)
        if self.name == 'native':
            if 'cls' in attrs:
                attrs['cls'] = self.classes(attrs['cls'])
            if 'class' in attrs:
                attrs['class'] = self.classes(attrs['class'])
            attrs = {re.sub(r'^data[-_]bs[-_]', 'data_mcui_', key): value for key,value in attrs.items()}
        if 'wrapper_attrs' in attrs:
            attrs['wrapper_attrs'] = {key:self.attrs(value) for key,value in attrs['wrapper_attrs'].items()}
        if self.name == 'native' and _mode.get() != 'static' and attrs.get('event_handlers'):
            # ActiveHTML's default event fields omit CustomEvent.detail.
            # Explicit handler dictionaries retain the caller's own field policy.
            attrs['event_handlers'] = {
                event: {'callback':handler, 'fields':['type','detail','target','bubbles','composed'],
                        'propagate':True} if event.startswith('mcui:') and callable(handler) else handler
                for event,handler in attrs['event_handlers'].items()
            }
        # The native backend does not execute Bootstrap-specific plugin hooks.
        # Bootstrap resources are loaded by this module, independent of the
        # ActiveHTMLWidget handler context.
        handles = attrs.get('javascript_handles')
        if isinstance(handles, dict) and any(isinstance(v,str) and 'context.bootstrap' in v for v in handles.values()):
            if self.name == 'bootstrap':
                import json
                loader = ("if(!window.__mcutilsBootstrapReady)window.__mcutilsBootstrapReady=window.bootstrap?Promise.resolve(window.bootstrap):new Promise((resolve,reject)=>{const s=document.createElement('script');s.src="+json.dumps(self.bootstrap_js)+";s.onload=()=>resolve(window.bootstrap);s.onerror=reject;document.head.append(s);});\n")
                attrs['javascript_handles'] = {key:loader+"return window.__mcutilsBootstrapReady.then(()=>{\n"+value.replace('context.bootstrap','window.bootstrap')+"\n});" if isinstance(value,str) else value for key,value in handles.items()}
            else:
                attrs.pop('javascript_handles', None)
                attrs.pop('onevents', None)
        if _mode.get() == 'static':
            if attrs.get('track_value') or attrs.get('trackInput'):
                attrs['disabled']=True
                attrs['data_requires_kernel']='true'
            handlers = attrs.pop('event_handlers', {}) or {}
            for event, handler in handlers.items():
                if isinstance(handler, str):
                    attrs['on'+event] = handler
                elif callable(handler):
                    owner=getattr(handler,'__self__',None)
                    if hasattr(owner,'action') and owner.action is None:continue
                    attrs['data_requires_kernel'] = 'true'
                    if event == 'click':
                        attrs['disabled'] = True
            for key in ('dynamic','track_value','trackInput','continuous_update','javascript_handles','onevents','oninitialize'):
                attrs.pop(key, None)
        return attrs


@lru_cache(maxsize=None)
def _component_classes(tag):
    plain = type(tag.replace('-', '_'), (_JHTML.HTML.TagElement,), {'tag': tag})
    widget = type(tag.replace('-', '_')+'_widget', (_JHTML.HTMLWidgets.WrappedHTMLElement,), {'base': plain})
    return plain, widget


def _materialize(value):
    if isinstance(value, (list,tuple)):
        return type(value)(_materialize(item) for item in value)
    # Resolve components before leaving the theme scope. Do not stringify a
    # live widget: the widget manager must own its DOM and Python callbacks.
    from .Interfaces import Component
    if isinstance(value, Component):
        return value.to_jhtml() if _mode.get() == 'static' else value.to_widget()
    return value


class _ElementFactory:
    def __init__(self, name, bootstrap=False, component=None):
        self.name = name
        self.bootstrap = bootstrap
        self.component = component

    def __call__(self, *elements, **attrs):
        theme = AppTheme.current()
        attrs = theme.attrs(attrs)
        if self.bootstrap and theme.name == 'bootstrap':
            source = getattr(_JHTML.Bootstrap, self.name)
        else:
            name = {'Card':'Div','CardHeader':'Div','CardBody':'Div','CardFooter':'Div',
                    'CardImage':'Img','ButtonGroup':'Div','LinkButton':'Anchor'}.get(self.name,self.name) if self.bootstrap else self.name
            source = getattr(_JHTML.HTML if _mode.get() == 'static' else _JHTML, name)
            if self.bootstrap:
                semantic = {'Card':'card','CardHeader':'card-header','CardBody':'card-body','CardFooter':'card-footer',
                            'Button':'button','ButtonGroup':'btn-group','CloseButton':'btn-close'}.get(self.name)
                if semantic:
                    attrs['cls'] = list(dict.fromkeys(_JHTML.manage_class(attrs.get('cls')) + ['mcui-'+semantic]))
        if self.name == 'Button':attrs.setdefault('type','button')
        elements = tuple(_materialize(item) for item in elements)
        if theme.name == 'native':
            component = self.component
            if component is None:
                classes = set(_JHTML.manage_class(attrs.get('cls')))
                component = next((name for token,name in (
                    ('mcui-card','panel'), ('mcui-card-header','panel-header'),
                    ('mcui-card-body','panel-body'), ('mcui-card-footer','panel-footer'),
                    ('mcui-accordion','accordion'), ('mcui-opener','opener'),
                    ('mcui-dropdown','dropdown'), ('mcui-carousel','carousel'),
                    ('mcui-collapse','collapse')) if token in classes),None)
            if component is not None:
                return theme.component(component, *elements, **attrs)
        return source(*elements, **attrs)


class _BootstrapFacade:
    def __getattr__(self, name):
        if name in ('Class','Variant'):
            return getattr(_JHTML.Bootstrap,name)
        return _ElementFactory(name, bootstrap=True)


class _AppHTMLMeta(type):
    def __getattr__(cls, name):
        if name == 'Bootstrap':
            return _BootstrapFacade()
        if name == 'AppElement':
            return lambda component, fallback='Div': _ElementFactory(fallback, component=component)
        # Constructors are the only intercepted API. Utilities, types and
        # compound-wrapper machinery remain the existing JHTML implementation.
        if name in ('HTML','CSS','XML','SVGContext','HTMLManager','Compound','JavascriptAPI','OutputArea','DefaultOutputWidget','APIs') or name.startswith(('manage_','extract_','parse','load')):
            return getattr(_JHTML,name)
        if hasattr(_JHTML,name) and name[:1].isupper():
            return _ElementFactory(name)
        return getattr(_JHTML,name)


class AppHTML(metaclass=_AppHTMLMeta):
    """Apps-local JHTML constructors, selected by the active AppTheme."""
