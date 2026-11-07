"""Portable declarations and reusable components for JavaScript interaction.

``JSVar`` describes an initial value whose live instances exist only in the
browser; it is deliberately independent of Apps' Python ``Var`` synchronizer.
``JSState`` owns a mounted scope, and ``JSBinding`` connects component properties
to that scope. Neither declaration requires IPython or ActiveHTMLWidgets.
Explicit ``VarBridge`` objects in Apps provide the optional widget transport.

This module will grow to encapsulate standard JavaScript interaction components,
including reusable slider interactions currently implemented by ``X3DControls``.
Those components will serve ordinary JHTML and Apps interfaces as well as
Readouts. Scene-specific field resolution remains in the X3D adapter.
"""

import copy
import json
import math
from pathlib import Path
import re
from contextlib import contextmanager
from contextvars import ContextVar
from urllib.parse import urlsplit, urljoin
from urllib.request import urlopen
from functools import lru_cache

__all__ = ["JSVar", "JSState", "JSBinding"]

_runtime_path = ContextVar('mcutils_javascript_path', default='inline')
_offline = ContextVar('mcutils_html_offline', default=False)
_asset_paths = ContextVar('mcutils_html_asset_paths', default=None)


@lru_cache(maxsize=16)
def _fetch_asset(url):
    with urlopen(url, timeout=25) as response:
        return response.read().decode('utf-8')


def _json_value(value):
    """Copy to portable JSON values without retaining a mutable Python payload."""
    def convert(obj):
        if hasattr(obj, "tolist"):
            return obj.tolist()
        if hasattr(obj, "item"):
            return obj.item()
        raise TypeError("JavaScript state requires JSON-serializable values")
    return json.loads(json.dumps(value, default=convert, allow_nan=False))


def _json(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, separators=(",", ":"))


class JSVar:
    """A declaration, not a Python handle to a browser's current value.

    ``initial`` is copied at declaration and serialization time. There is no
    ``value`` property, Python observer list, widget, or implicit kernel bridge.
    Names are local to a ``JSState``; rendering it twice creates fresh instances.
    ``kind`` may be number, integer, string, boolean, array, object, or any.
    Null is accepted only with ``nullable=True`` (the default).
    """
    __slots__ = ("_name", "_initial", "_schema")

    def __init__(self, name, initial=None, *, kind="any", choices=None,
                 min=None, max=None, nullable=True):
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.-]*", name):
            raise ValueError("JSVar names must start with a letter or underscore and contain letters, digits, _, ., or -")
        if kind not in {"any", "number", "integer", "string", "boolean", "array", "object"}:
            raise ValueError("Unknown JSVar kind {!r}".format(kind))
        self._name = name
        self._schema = dict(kind=kind, nullable=bool(nullable))
        if choices is not None:
            self._schema["choices"] = _json_value(list(choices))
        for key, bound in (("min", min), ("max", max)):
            if bound is not None:
                if isinstance(bound, bool) or not isinstance(bound, (int, float)) or not math.isfinite(bound):
                    raise ValueError("JSVar bounds must be finite numbers")
                self._schema[key] = bound
        if min is not None and max is not None and min > max:
            raise ValueError("JSVar min cannot exceed max")
        self._initial = self.validate(initial)

    @property
    def name(self):
        return self._name

    @property
    def initial(self):
        return copy.deepcopy(self._initial)

    def validate(self, value):
        value = _json_value(value)
        schema = self._schema
        if value is None:
            if not schema["nullable"]:
                raise ValueError(self.name + " does not accept null")
            return value
        kind = schema["kind"]
        checks = {
            "any": True,
            "number": isinstance(value, (int, float)) and not isinstance(value, bool),
            "integer": isinstance(value, int) and not isinstance(value, bool),
            "string": isinstance(value, str),
            "boolean": isinstance(value, bool),
            "array": isinstance(value, list),
            "object": isinstance(value, dict),
        }
        if not checks[kind]:
            raise ValueError(self.name + " requires " + kind)
        if "choices" in schema and not any(type(value) is type(choice) and value == choice for choice in schema["choices"]):
            raise ValueError(self.name + " is outside its choices")
        for key in ("min", "max"):
            if key in schema:
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ValueError(self.name + " bounds require a numeric value")
                if (key == "min" and value < schema[key]) or (key == "max" and value > schema[key]):
                    raise ValueError(self.name + " is outside its bounds")
        return value

    def to_dict(self):
        return dict(name=self.name, initial=self.initial, schema=copy.deepcopy(self._schema))


class JSBinding:
    """Connect a component property to a JSVar with optional explicit direction.

    ``in`` feeds a component, ``out`` publishes component events, and ``both``
    does both. None uses the adapter's declared default. No Python callable is
    converted into JavaScript by binding serialization.
    """
    def __init__(self, variable, direction=None):
        if not isinstance(variable, JSVar):
            raise TypeError("JSBinding requires a JSVar; use VarBridge for Python Var values")
        if direction not in (None, "in", "out", "both"):
            raise ValueError("binding direction must be in, out, both, or None")
        self.variable, self.direction = variable, direction

    def to_dict(self):
        return dict(variable=self.variable.name, direction=self.direction)


class JSState:
    """A serializable declaration of a browser state scope.

    Use ``state.to_widget(*html)`` to host ordinary HTML, or pass ``state=`` to
    JHTML/Apps/Readout containers. Despite the compatibility method name,
    ``to_widget`` returns plain HTML unless ``mode='widget'`` and bridges are
    explicitly requested. Each render has independent values and subscriptions.

    ``script`` is an optional trusted JavaScript body receiving ``state``,
    ``root``, ``on``, and ``onDispose``. Python callables are rejected. Its
    cleanup uses the same lifetime as the containing interface.

    Scopes serialize as ``mcui-state`` WebComponents. Load the shared UI entry
    point once; its lifecycle mounts and disposes scopes automatically. Full
    HTML/Readout exports collect that library once after the interface.
    ``javascript_path`` accepts ``'inline'`` (the default) or a script URL/path
    to JHTML/resources/javascript.js and its sibling Apps resources. ``offline``
    on an exporter also embeds supported view dependencies such as Plotly.
    """
    _capabilities = {
        "dom": {"value": "both", "checked": "both", "text": "in", "visible": "in", "enabled": "in"},
        "table": {"selection": "both", "visible": "in"},
        "plotly": {"selection": "both", "data": "in", "layout": "in", "visible": "in"},
        "x3d": {"mode": "both", "sample": "both", "fraction": "both", "running": "both",
                "speed": "both", "loop": "both", "scale": "both", "visible": "in"},
    }

    def __init__(self, *variables, bridges=(), script=None, javascript_path=None):
        if len(variables) == 1 and isinstance(variables[0], (list, tuple)):
            variables = tuple(variables[0])
        self.variables = {}
        for variable in variables:
            if not isinstance(variable, JSVar):
                raise TypeError("JSState contains JSVar declarations, not Python Var values")
            if variable.name in self.variables:
                raise ValueError("Duplicate JSVar name: " + variable.name)
            self.variables[variable.name] = variable
        self.bridges = tuple(bridges)
        for bridge in self.bridges:
            if self.variables.get(bridge.js_var.name) is not bridge.js_var:
                raise ValueError("VarBridge target must belong to this JSState")
        if script is not None and not isinstance(script, str):
            raise TypeError("JSState script must be trusted JavaScript source, not a Python callable")
        self.script = script
        self.javascript_path = self.check_javascript_path(javascript_path)

    def __getitem__(self, name):
        return self.variables[name]

    @classmethod
    def register_adapter(cls, name, properties):
        """Declare an extension's properties and default binding directions.

        Its trusted browser module must register the matching factory with
        ``McUtilsJS.registerAdapter(name, factory)`` before bindings mount. A
        JSState's script runs before that initial mount for this purpose.
        """
        if not isinstance(name, str) or not name:
            raise ValueError('A JavaScript adapter name is required')
        properties = dict(properties)
        if any(not isinstance(prop, str) or direction not in ('in','out','both')
               for prop, direction in properties.items()):
            raise ValueError('Adapter properties require names and in/out/both directions')
        if name in cls._capabilities and cls._capabilities[name] != properties:
            raise ValueError('Conflicting JavaScript adapter declaration: ' + name)
        cls._capabilities[name] = properties

    def to_dict(self):
        variables = [variable.to_dict() for variable in self.variables.values()]
        values = {variable["name"]: variable for variable in variables}
        for bridge in self.bridges:
            if bridge.initialize_from == "python":
                values[bridge.js_var.name]["initial"] = bridge.js_var.validate(bridge.python_var.value)
        return dict(version=1, variables=variables, script=self.script)

    @staticmethod
    def check_javascript_path(path):
        if path is None:
            return None
        path = str(path)
        if path == 'inline':
            return path
        parsed = urlsplit(path)
        if not path.strip() or any(ord(char) < 32 for char in path) or parsed.scheme not in ('','http','https','file'):
            raise ValueError('javascript_path must be inline or a script URL/path')
        if parsed.scheme in ('http','https') and not parsed.netloc:
            raise ValueError('javascript_path requires a complete HTTP(S) URL')
        return path

    @classmethod
    def current_javascript_path(cls):
        return 'inline' if _offline.get() else _runtime_path.get()

    @staticmethod
    def is_offline():
        return _offline.get()

    @classmethod
    @contextmanager
    def rendering(cls, javascript_path=None, offline=None, asset_paths=None):
        tokens = []
        if javascript_path is not None:
            tokens.append((_runtime_path,_runtime_path.set(cls.check_javascript_path(javascript_path))))
        if offline is not None:
            tokens.append((_offline,_offline.set(bool(offline))))
        if asset_paths is not None:
            tokens.append((_asset_paths,_asset_paths.set(dict(asset_paths))))
        try:
            yield
        finally:
            for variable, token in reversed(tokens):
                variable.reset(token)

    @staticmethod
    def javascript_source(include_ui=True):
        """The standalone bundle assembled from the existing UI and state sources."""
        source = Path(__file__).with_name('resources').joinpath('javascript.js').read_text()
        if include_ui:
            source = Path(__file__).parent.parent.joinpath('Apps/resources/native.js').read_text() + '\n' + source
        return source

    @staticmethod
    def native_css():
        return Path(__file__).parent.parent.joinpath('Apps/resources/native.css').read_text()

    @classmethod
    def asset_source(cls, name, path):
        path = str((_asset_paths.get() or {}).get(name, path))
        if urlsplit(path).scheme in ('http','https'):
            return _fetch_asset(path)
        if path.startswith('file:'):
            from urllib.request import url2pathname
            path = url2pathname(urlsplit(path).path)
        return Path(path).read_text(encoding='utf-8')

    @staticmethod
    def _script_element(source, **attrs):
        from .HTML import HTML
        return HTML.Script(re.sub(r'</script', r'<\\/script', source, flags=re.I), **attrs)

    @classmethod
    def _walk_elements(cls, elements):
        if isinstance(elements,(list,tuple)):
            for element in elements:
                yield from cls._walk_elements(element)
        else:
            yield elements
            for child in getattr(elements,'elems',()):
                yield from cls._walk_elements(child)

    @classmethod
    def runtime_path(cls, elements=(), javascript_path=None):
        if cls.is_offline():
            return 'inline'
        if javascript_path is not None:
            return cls.check_javascript_path(javascript_path)
        explicit = {getattr(element,'attrs',{}).get('data-mcjs-runtime')
                    for element in cls._walk_elements(elements)} - {None}
        if len(explicit)>1:
            raise ValueError('One interface cannot request multiple JavaScript runtime versions')
        return next(iter(explicit)) if explicit else cls.current_javascript_path()

    @classmethod
    def resource_elements(cls, elements=(), *, javascript_path=None, force=False,
                          native_styles=None, bootstrap=False):
        """Collect one shared UI runtime and optional offline view dependencies.

        The caller owns placement/de-duplication. Scopes contain declarations,
        never bootstrap images or copies of the runtime. Local asset overrides
        use keys plotly, mathjax, x3dom_script, bootstrap_script, and
        bootstrap_stylesheet; remote explicit Bootstrap assets may be read while
        exporting, but the offline result never fetches them in the viewer.
        """
        from .HTML import HTML
        needed, native, plotly, x3d = force, False, False, False
        mathjax = None
        for element in cls._walk_elements(elements):
            tag = str(getattr(element,'tag','')).lower()
            attrs = getattr(element,'attrs',{})
            if tag.startswith('mcui-'):
                needed = True
                native |= tag not in ('mcui-state','mcui-bootstrap')
                bootstrap |= tag == 'mcui-bootstrap' and attrs.get('data-mcui-bootstrap-load')!='false'
            classes = attrs.get('class','')
            classes = classes.split() if isinstance(classes,str) else classes or []
            if any(token.startswith('mcui-') and token not in ('mcui-root','mcui-bootstrap') for token in classes):
                native = needed = True
            x3d |= tag == 'x3d'
            if 'data-mcjs-bind' in attrs:
                binding = json.loads(attrs['data-mcjs-bind'])
                needed = True
                if binding['adapter']=='plotly':
                    plotly = True
                    mathjax = binding['options'].get('mathjax') or mathjax
        native = native if native_styles is None else native_styles
        path = cls.runtime_path(elements,javascript_path)
        resources = []
        if native:
            if path == 'inline':
                resources.append(HTML.Style(cls.native_css(),id='mcutils-apps-native-css'))
            else:
                resources.append(HTML.Link(rel='stylesheet',href=urljoin(path,'../../Apps/resources/native.css'),id='mcutils-apps-native-css'))
        if bootstrap:
            from ..Apps.Themes import AppTheme
            if cls.is_offline():
                css = cls.asset_source('bootstrap_stylesheet',AppTheme.bootstrap_css)
                resources.append(HTML.Style(re.sub(r'</style',r'<\\/style',css,flags=re.I),id='mcutils-bootstrap-css'))
                resources.append(cls._script_element(cls.asset_source('bootstrap_script',AppTheme.bootstrap_js),id='mcutils-bootstrap-js'))
            else:
                resources.extend([HTML.Link(rel='stylesheet',href=AppTheme.bootstrap_css,id='mcutils-bootstrap-css'),
                                  HTML.Script(src=AppTheme.bootstrap_js,id='mcutils-bootstrap-js')])
        if cls.is_offline():
            if plotly:
                if (_asset_paths.get() or {}).get('plotly'):
                    source = cls.asset_source('plotly','')
                else:
                    from plotly.offline import get_plotlyjs
                    source = get_plotlyjs()
                resources.append(cls._script_element(source,id='mcutils-plotly-js'))
            if mathjax:
                resources.append(cls._script_element(cls.asset_source('mathjax',mathjax),id='mcutils-mathjax-js'))
            if x3d:
                source = Path(__file__).parent.parent/'resources/x3dom-full.js'
                resources.append(cls._script_element(cls.asset_source('x3dom_script',source),id='mcutils-x3dom-js'))
        if needed:
            if path == 'inline':
                resources.append(cls._script_element(cls.javascript_source(),id='mcutils-apps-native-js'))
            else:
                resources.append(HTML.Script(src=path,id='mcutils-apps-native-js'))
        return resources

    @staticmethod
    def unique_resources(resources):
        """Keep shared assets once and place the WebComponent entry point last."""
        result, seen = [], set()
        for element in resources:
            if isinstance(element,str):
                key = ('text',element)
            else:
                attrs = getattr(element,'attrs',{})
                key = ('id',attrs['id']) if attrs.get('id') else ('text',element.tostring())
            if key not in seen:
                seen.add(key);result.append(element)
        return sorted(result,key=lambda element: int(not isinstance(element,str) and getattr(element,'attrs',{}).get('id')=='mcutils-apps-native-js'))

    @classmethod
    def runtime_loader(cls, javascript_path=None):
        """A Promise expression used only by the shared ActiveHTMLWidgets API."""
        path = cls.runtime_path(javascript_path=javascript_path)
        if path == 'inline':
            return '(function(){\n'+cls.javascript_source()+"\nreturn Promise.resolve(McUtilsJS.ready).then(()=>McUtilsJS);\n})()"
        return r'''(function(){
if(globalThis.McUtilsJS) return Promise.resolve(McUtilsJS.ready).then(()=>McUtilsJS);
const url=URL;
const loads=globalThis.__mcutilsUIRuntimeLoads ||= new Map();
if(!loads.has(url)) loads.set(url,new Promise((resolve,reject)=>{
  const script=document.createElement('script');script.src=url;
  script.onload=()=>globalThis.McUtilsJS ? Promise.resolve(McUtilsJS.ready).then(()=>resolve(McUtilsJS),reject) : reject(new Error('McUtils UI runtime did not initialize'));
  script.onerror=()=>{loads.delete(url);reject(new Error('Failed to load McUtils UI runtime: '+url));};
  document.head.append(script);
}));
return loads.get(url);
})()'''.replace('URL',_json(path),1)

    @classmethod
    def bind_element(cls, element, bindings, *, adapter="dom", options=None):
        """Attach a portable binding manifest to an existing HTML element."""
        if not bindings and adapter == 'dom':
            return element
        if adapter not in cls._capabilities:
            raise ValueError("Unknown JavaScript adapter: " + adapter)
        config, references = {}, []
        for prop, binding in (bindings or {}).items():
            if prop not in cls._capabilities[adapter]:
                raise ValueError("{} does not support binding {!r}".format(adapter, prop))
            if isinstance(binding, JSVar):
                binding = JSBinding(binding)
            if not isinstance(binding, JSBinding):
                raise TypeError("bind values must be JSVar or JSBinding declarations")
            default = cls._capabilities[adapter][prop]
            direction = binding.direction or default
            if default in ('in', 'out') and direction != default:
                raise ValueError(prop + " is an " + default + "-only property")
            config[prop] = dict(binding.to_dict(), direction=direction)
            references.append(binding.variable)
        manifest = dict(adapter=adapter, bindings=config, options=_json_value(options or {}))
        attrs = dict(element.attrs)
        for key, value in tuple(attrs.items()):
            if isinstance(value, bool):
                if key in ('checked', 'disabled', 'multiple', 'selected', 'hidden'):
                    if value:
                        attrs[key] = key
                    else:
                        del attrs[key]
                else:
                    attrs[key] = str(value).lower()
            elif isinstance(value, (int, float)):
                attrs[key] = str(value)
        attrs["data-mcjs-bind"] = _json(manifest)
        element.attrs = attrs
        element._mcjs_variables = tuple(references)
        return element

    def _validate_elements(self, elements):
        def walk(element):
            if isinstance(element, (list, tuple)):
                for child in element:
                    walk(child)
                return
            attrs = getattr(element, "attrs", {})
            if "data-mcjs-state" in attrs:
                return  # Nested state owns its own names.
            for variable in getattr(element, "_mcjs_variables", ()):
                if self.variables.get(variable.name) is not variable:
                    raise ValueError("Binding references a JSVar outside this JSState: " + variable.name)
            if "data-mcjs-bind" in attrs:
                manifest = json.loads(attrs["data-mcjs-bind"])
                for binding in manifest["bindings"].values():
                    if binding["variable"] not in self.variables:
                        raise ValueError("Unresolved JSVar: " + binding["variable"])
            for child in getattr(element, "elems", ()):
                walk(child)
        walk(elements)

    def to_widget(self, *elements, mode="html", javascript_path=None):
        from ..Apps.Themes import AppTheme
        if mode not in ("html", "widget"):
            raise ValueError("JSState mode must be html or widget")
        self._validate_elements(elements)
        path = self.check_javascript_path(javascript_path) if javascript_path is not None else self.javascript_path
        attrs = {'data-mcjs-state':_json(self.to_dict()),'style':{'display':'contents'}}
        if path is not None:
            attrs['data-mcjs-runtime'] = path
        root = AppTheme.current().component('state',*elements,mode='static' if mode=='html' else 'widget',**attrs)
        if mode == "widget":
            with self.rendering(javascript_path=path):
                if self.bridges:
                    from ..Apps.Variables import VarBridge
                    return VarBridge.mount(self, root)
                return AppTheme.current().decorate(root)
        return root

    @classmethod
    def render_html(cls, *elements, javascript_path=None, offline=False, asset_paths=None):
        from .HTML import HTML
        with cls.rendering(javascript_path=javascript_path,offline=offline,asset_paths=asset_paths):
            resources = cls.unique_resources(cls.resource_elements(elements,javascript_path=javascript_path))
            return HTML.Div(*elements,*resources).tostring()

    def to_html(self, *elements, javascript_path=None, offline=False, asset_paths=None):
        from ..Apps.Themes import AppTheme, _materialize
        with AppTheme.rendering(mode='static',javascript_path=javascript_path,offline=offline,asset_paths=asset_paths) as (theme,_):
            scope = self.to_widget(*_materialize(elements),javascript_path=javascript_path)
            body = theme.component('root',scope,mode='static',cls=['mcui-root','mcui-'+theme.name])
            return self.render_html(body,javascript_path=javascript_path,offline=offline,asset_paths=asset_paths)
