from __future__ import annotations

import abc
import collections
import uuid
import numpy as np
import os
import json

from .. import Devutils as dev
from ..Jupyter import JHTML, X3DHTML
from .. import Numputils as nput

__all__ = [
    "X3D",
    "X3DScript",
    "X3DComponent",
    "X3DPrimitive",
    "X3DGeometryObject",
    "X3DGeometryGroup",
    "X3DGroup",
    "X3DScene",
    "X3DBackground",
    "X3DMaterial",
    "X3DEnvironment",
    "X3DLight",
    "X3DDirectionalLight",
    "X3DPointLight",
    "X3DSpotLight",
    "X3DLine",
    "X3DSphere",
    "X3DCone",
    "X3DBox",
    "X3DCylinder",
    "X3DCappedCylinder",
    "X3DArrow",
    "X3DTorus",
    "X3DRectangle2D",
    "X3DDisk2D",
    "X3DCircle2D",
    "X3DPolyline2D",
    "X3DTriangleSet",
    "X3DIndexedTriangleSet",
    "X3DIndexedLineSet",
    "X3DSwitch",
    "X3DListAnimator",
    "X3DInterpolatingAnimator"
]

#TODO: cache these resources or put them on a path that is accessible by Jupyter
#      might be pretty simple depending on what resource paths Jupyter naturally exposes

class X3DObject(metaclass=abc.ABCMeta):
    id: str
    @abc.abstractmethod
    def to_x3d(self) -> X3DHTML.X3DElement:
        """
        **LLM Docstring**

        Abstract: render this object to its X3D DOM element.

        :return: the X3D element
        """
        ...

    def get_interpolated_attributes(self):
        """
        **LLM Docstring**

        Return the object's attributes used when building animation frames (its X3D element's attrs).

        :return: the attribute dict
        :rtype: dict
        """
        return self.to_x3d().attrs
    def get_children(self):
        """
        **LLM Docstring**

        Return the object's child objects (none by default).

        :return: the children
        :rtype: list
        """
        return []

    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh unique id for a new object.

        :return: the id
        :rtype: str
        """
        return str(uuid.uuid4())[:6]

    def resolve_prop_attr(self, prop_name):
        """
        **LLM Docstring**

        Map a property name to the X3D attribute name it animates (identity by default).

        :param prop_name: the property name
        :return: the attribute name
        """
        return prop_name
    def prep_animation_values(self, prop_name, values):
        """
        **LLM Docstring**

        Normalize a property's per-frame animation values (e.g. defaulting `transparency` gaps to 0).

        :param prop_name: the property name
        :param values: the per-frame values
        :return: the normalized values
        """
        if prop_name == 'transparency':
            values = [v if v is not None else 0 for v in values]
        return values
    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the id of the DOM node that carries a given animated property (this object by default).

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        return self.id

class X3DScript:
    """Trusted JavaScript body for a browser-side :class:`X3DComponent`.

    The body receives ``component`` and can return a controller object, exposed
    as ``component.root.controller``. Scripts execute in the exported page and
    need no live Python kernel. Application-specific scripts belong to callers.
    """

    def __init__(self, source):
        if not isinstance(source, str):
            raise TypeError("X3DScript source must be a JavaScript string")
        self.source = source


class X3DComponent:
    """HTML controls, JSON data and a script bound to one X3DOM scene.

    Scripts receive ``root``, ``scene``, ``data``, and a ``nodes`` alias mapping.
    ``query(selector)`` searches the controls. ``setField(node_or_alias, name,
    value)`` writes X3D fields, flattening numeric arrays. ``on`` attaches an
    event listener and returns its remover; ``onDispose`` registers cleanup.
    Listeners and cleanup callbacks are disposed when the component or scene is
    removed. Initialization waits for the scene's own runtime to be ready.

    Pass components to ``X3D(..., components=[...])``. They are included in
    ``to_widget()`` and HTML exports; ``to_x3d()`` remains bare scene markup.
    This lifecycle currently supports X3DOM, not X_ITE. Source is trusted code.
    """

    def __init__(self, *elements, script, data=None, nodes=None, id=None,
                 placement='before', timeout=10000, **attrs):
        if len(elements) == 1 and isinstance(elements[0], (tuple, list)):
            elements = tuple(elements[0])
        if isinstance(script, str):
            script = X3DScript(script)
        if not isinstance(script, X3DScript):
            raise TypeError("script must be an X3DScript or JavaScript string")
        if placement not in {'before', 'after'}:
            raise ValueError("component placement must be 'before' or 'after'")
        try:
            timeout_value = float(timeout)
        except (TypeError, ValueError):
            raise ValueError("component timeout must be positive milliseconds") from None
        if isinstance(timeout, (bool, str)) or not np.isfinite(timeout_value) or timeout_value <= 0:
            raise ValueError("component timeout must be positive milliseconds")
        if id is None:
            id = 'x3d-component-' + uuid.uuid4().hex
        self._check_id(id)
        self.elements, self.script = tuple(elements), script
        self.data, self.nodes = data, {} if nodes is None else dict(nodes)
        self.id, self.placement, self.timeout = id, placement, timeout_value
        self.attrs = attrs

    @staticmethod
    def _check_id(value):
        if not isinstance(value, str) or not value or any(c.isspace() for c in value):
            raise ValueError("X3D node ids must be nonempty strings without whitespace")
        return value

    @classmethod
    def _node_id(cls, value):
        if not isinstance(value, str):
            if hasattr(value, 'id'):
                value = value.id
            elif hasattr(value, 'attrs'):
                value = value.attrs.get('id')
        return cls._check_id(value)

    def _configuration(self, scene_id):
        nodes = {}
        for alias, node in self.nodes.items():
            if not isinstance(alias, str) or not alias:
                raise ValueError("component node aliases must be nonempty strings")
            nodes[alias] = self._node_id(node)
        return json.dumps(dict(sceneId=self._check_id(scene_id), data=self.data,
                               nodes=nodes, timeout=self.timeout),
                          default=lambda x: x.tolist() if hasattr(x, 'tolist') else
                              (_ for _ in ()).throw(TypeError("component data must be JSON serializable")),
                          ensure_ascii=True, allow_nan=False)

    def get_bootstrap_script(self, scene_id):
        """An event-handler body that also works for notebook HTML insertion."""
        return r"""
(function(image) {
  const root = image.parentElement;
  image.remove();
  if (!root || root.__mcutilsX3DMounted) return;
  root.__mcutilsX3DMounted = true;
  const config = %s;
  let scene = null, wrapper = null, timer = null, disposed = false;
  const removers = [], callbacks = [], started = Date.now();
  root.setAttribute('data-x3d-state', 'loading');
  function dispose() {
    if (disposed) return;
    disposed = true;
    if (timer !== null) clearTimeout(timer);
    observer.disconnect();
    for (const remove of removers.splice(0)) remove();
    for (const callback of callbacks.splice(0).reverse()) {
      try { callback(); } catch (error) { console.error(error); }
    }
    root.controller = null;
    root.setAttribute('data-x3d-state', 'disposed');
  }
  function fail(error) {
    dispose();
    root.error = error;
    root.setAttribute('data-x3d-state', 'error');
    root.dispatchEvent(new CustomEvent('mcutils-x3d-error', {detail: error}));
    console.error('X3D component initialization failed:', error);
  }
  const observer = new MutationObserver(() => {
    if (!root.isConnected || (wrapper && !wrapper.isConnected) || (scene && !scene.isConnected)) dispose();
  });
  observer.observe(document.documentElement, {childList: true, subtree: true});
  function byId(parent, id) {
    if (parent.id === id) return parent;
    for (const node of parent.querySelectorAll('[id]')) {
      if (node.id === id) return node;
    }
    return null;
  }
  function fieldString(value) {
    if (Array.isArray(value) || ArrayBuffer.isView(value)) {
      return Array.from(value, fieldString).join(' ');
    }
    if (typeof value === 'number' && !Number.isFinite(value)) {
      throw new TypeError('X3D fields require finite numbers');
    }
    if (!['string', 'number', 'boolean'].includes(typeof value)) {
      throw new TypeError('X3D fields require strings, numbers, booleans or arrays');
    }
    return String(value);
  }
  function mount() {
    const nodes = Object.create(null);
    for (const [alias, id] of Object.entries(config.nodes)) {
      const node = byId(scene, id);
      if (!node) throw new Error('Missing X3D component node: ' + alias + ' (' + id + ')');
      nodes[alias] = node;
    }
    function resolve(target) {
      if (typeof target === 'string') target = nodes[target] || root.querySelector(target);
      if (!target || typeof target.addEventListener !== 'function') {
        throw new TypeError('Unknown X3D component target');
      }
      return target;
    }
    const component = {
      root, scene, data: config.data, nodes,
      query: selector => root.querySelector(selector),
      setField(target, field, value) {
        if (disposed) throw new Error('X3D component is disposed');
        target = resolve(target);
        if (!scene.contains(target)) throw new Error('X3D field target is outside this scene');
        const serialized = fieldString(value);
        const coordinateField = target.tagName.toLowerCase() === 'coordinateinterpolator' ? field.toLowerCase() : '';
        if (coordinateField === 'key') {
          // Keep key count current for a following keyValue write in the same
          // event handler, before the DOM mutation observer has run.
          const fields = scene.ownerDocument.defaultView.x3dom.fields;
          target.setAttribute(field, serialized);
          target.setFieldValue('key', fields.MFFloat.parse(serialized));
        } else if (coordinateField === 'keyvalue') {
          // X3DOM 1.8.3 stores coordinate frames as nested arrays. Its attribute
          // parser cannot replace those arrays, so use the public field API.
          const fields = scene.ownerDocument.defaultView.x3dom.fields;
          const keyCount = target.getFieldValue('key').length;
          const numbers = serialized.trim().split(/[\s,]+/).map(Number);
          if (numbers.length %% 3 !== 0 || !numbers.every(Number.isFinite)) {
            throw new Error('CoordinateInterpolator keyValue requires complete finite xyz coordinates');
          }
          const coordinates = fields.MFVec3f.parse(serialized);
          if (!keyCount || !coordinates.length || coordinates.length %% keyCount !== 0) {
            throw new Error('CoordinateInterpolator keyValue requires complete coordinate frames for each key');
          }
          const pointCount = coordinates.length / keyCount;
          const frames = Array.from({length: keyCount}, (_, index) =>
            coordinates.slice(index * pointCount, (index + 1) * pointCount));
          target.setAttribute(field, serialized);
          target.setFieldValue('keyValue', frames);
        } else {
          target.setAttribute(field, serialized);
        }
      },
      on(target, event, listener, options) {
        if (disposed) throw new Error('X3D component is disposed');
        target = resolve(target);
        target.addEventListener(event, listener, options);
        let active = true;
        const remove = () => {
          if (active) target.removeEventListener(event, listener, options);
          active = false;
        };
        removers.push(remove);
        return remove;
      },
      onDispose(callback) {
        if (typeof callback !== 'function') throw new TypeError('Expected a cleanup function');
        if (disposed) callback(); else callbacks.push(callback);
      },
      dispose,
      get disposed() { return disposed; }
    };
    const controller = (function(component) {
%s
    })(component);
    if (disposed) return;
    root.controller = controller === undefined ? component : controller;
    root.setAttribute('data-x3d-state', 'ready');
    root.dispatchEvent(new CustomEvent('mcutils-x3d-ready', {detail: root.controller}));
  }
  function wait() {
    if (disposed) return;
    if (!root.isConnected) { dispose(); return; }
    if (!wrapper && root.parentElement) wrapper = byId(root.parentElement, config.sceneId);
    if (wrapper) scene = wrapper.querySelector('x3d');
    if (scene && scene.runtime && scene.runtime.isReady === true) {
      try { mount(); } catch (error) { fail(error); }
    } else if (Date.now() - started >= config.timeout) {
      fail(new Error('Timed out waiting for X3DOM scene ' + config.sceneId));
    } else {
      timer = setTimeout(wait, 25);
    }
  }
  wait();
})(this);
""" % (self._configuration(scene_id), self.script.source)

    def to_widget(self, scene_id):
        attrs = dict(self.attrs)
        attrs.setdefault('cls', 'mcutils-x3d-component')
        return JHTML.Div(
            *self.elements,
            JHTML.Image(src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
                        onload=self.get_bootstrap_script(scene_id),
                        style='display:none;', alt=''),
            id=self.id, can_be_dynamic=False, **attrs
        )


class X3D(X3DObject):
    defaults = dict(
        width=500,
        height=500
    )
    xite_options = dict(
        contentScale="auto",
        antialiased = "true",
        multisampling = "8",
        primitiveQuality = "HIGH",
        update = "auto",
    )
    def to_readout(self, caption=None, **opts):
        """
        **LLM Docstring**

        Build a `Readout` of this scene (`ViewReadout`).

        :param opts: `ReadoutInterface.to_readout` options (``include``, ``exclude``, ``units``, ...)
        :return: the readout
        :rtype: McUtils.Jupyter.Readouts.Readout
        """
        from .Readouts import ViewReadout
        return ViewReadout(self, caption=caption).to_readout(**opts)

    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh `x3d-`-prefixed id.

        :return: the id
        :rtype: str
        """
        return "x3d-" + str(uuid.uuid4())[:6]
    def __init__(self, *children, id=None, dynamic_loading=True,
                 use_xite=False,
                 xite_options=None,
                 x3dom_path=None,
                 x3dom_css_path=None,
                 include_mathjax=False,
                 recording_options=None,
                 include_export_button=False,
                 include_record_button=False,
                 include_view_settings_button=False,
                 preload_scripts=None,
                 onload_scripts=None,
                 components=None,
                 playback=None,
                 **opts):
        """
        **LLM Docstring**

        Set up the top-level X3D scene container: its children, size, resource paths, and
        the optional export/record/view-settings UI and MathJax/loader scripting.

        :param children: the scene's child objects
        :param id: the DOM id (auto-generated if omitted)
        :param dynamic_loading: load the X3DOM runtime dynamically
        :type dynamic_loading: bool
        :param x3dom_path: an override path/URL for the X3DOM JS
        :param x3dom_css_path: an override path/URL for the X3DOM CSS
        :param include_mathjax: include MathJax for text rendering
        :type include_mathjax: bool
        :param recording_options: options for the screen recorder
        :type recording_options: dict | None
        :param include_export_button: include the image-export button
        :type include_export_button: bool
        :param include_record_button: include the screen-record button
        :type include_record_button: bool
        :param include_view_settings_button: include the view-settings button
        :type include_view_settings_button: bool
        :param preload_scripts: scripts to run before the scene loads
        :param onload_scripts: scripts to run once the scene loads
        :param components: scriptable HTML controls bound to this X3DOM scene
        :type components: X3DComponent | iterable[X3DComponent] | None
        :param playback: enable playback controls, disable them, or configure them;
            None uses the native animators' playback settings
        :type playback: bool | dict | None
        :param opts: extra scene options (e.g. width/height)
        """
        if len(children) == 1 and isinstance(children[0], (tuple, list)):
            children = children[0]
        self.children = children
        self.opts = opts
        if id is None:
            id = self.get_new_id()
        self.id = id
        self.dynamic_loading = dynamic_loading
        if recording_options is None:
            recording_options = {}
        self.recording_options = recording_options
        self.include_export_button =include_export_button
        self.include_record_button = include_record_button
        self.include_view_settings_button =include_view_settings_button
        if x3dom_path is not None:
            if dev.str_is(x3dom_path, 'local') and not os.path.isfile('local'):
                # get the relative path
                x3dom_path = 'file://' + os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    'Jupyter', 'resources', 'x3dom-full.js'
                )
            self.X3DOM_JS = x3dom_path
        if x3dom_css_path is not None:
            self.X3DOM_CSS = x3dom_css_path
        if xite_options is None:
            xite_options = self.xite_options
        self.xite_options = xite_options
        self.use_xite = use_xite
        self.include_mathjax = include_mathjax
        self.preload_scripts = preload_scripts
        self.onload_scripts = onload_scripts
        if isinstance(components, X3DComponent):
            components = [components]
        self.components = tuple(() if components is None else components)
        if any(not isinstance(component, X3DComponent) for component in self.components):
            raise TypeError("X3D components must be X3DComponent objects")
        if self.components and use_xite:
            raise NotImplementedError("X3DComponent lifecycle currently requires X3DOM (use_xite=False)")
        if playback is not None and not isinstance(playback, (bool, dict)):
            raise TypeError("playback must be a boolean, a configuration dict, or None")
        if use_xite and (playback is True or isinstance(playback, dict)):
            raise NotImplementedError("X3D playback controls currently require X3DOM")
        self.playback = playback
        self._widg = None
        self._widget_cache = {}

    X_ITE_JS = "https://cdn.jsdelivr.net/npm/x_ite@11.5.11/dist/x_ite.min.js"
    X3DOM_JS = 'https://www.x3dom.org/download/1.8.3/x3dom-full.js'
    X3DOM_CSS = 'https://www.x3dom.org/download/x3dom.css'
    MATHJAX_CDN = 'https://cdn.jsdelivr.net/npm/mathjax@4/tex-svg.js'

    @staticmethod
    def get_playback_controls():
        """Reusable HTML toolbar for the generic X3D playback controller."""
        role = lambda name: {'data-role': 'playback-' + name}
        return JHTML.Div(
            JHTML.Button('Pause', type='button', **role('toggle')),
            JHTML.Button('Restart', type='button', **role('restart')),
            JHTML.Button('Back 1%', type='button', **role('previous')),
            JHTML.Button('Forward 1%', type='button', **role('next')),
            JHTML.Input(type='range', min='0', max='1', step='any', value='0',
                        **dict(role('position'), **{'aria-label': 'Animation position'})),
            JHTML.Output('0%', **role('label')),
            JHTML.Label('Speed ', JHTML.Input(type='number', min='.01', step='.25', value='1',
                        style='width:4.5em;', **role('speed'))),
            JHTML.Label(JHTML.Input(type='checkbox', checked=True, **role('loop')), ' Loop'),
            cls='mcutils-x3d-playback',
            style='display:flex;align-items:center;gap:.5em;flex-wrap:wrap;'
        )

    @staticmethod
    def get_playback_script():
        """A reusable controller factory for any routed X3D fraction animation.

        A browser clock feeds public input fields on existing interpolators and
        sequencers. Native TimeSensors are disabled while controlled, allowing
        seek and speed changes without changing engine-private clock state.
        """
        return r"""
function X3DPlayback(component, options = {}) {
    const scene = component.scene;
    const elements = Array.from(scene.querySelectorAll('*'));
    const named = new Map();
    for (const node of elements) {
        for (const name of [node.id, node.getAttribute('DEF')]) if (name) named.set(name, node);
    }
    const clock = options.clock || component.nodes.clock || elements.find(node => node.tagName.toLowerCase() === 'timesensor');
    if (!clock) throw new Error('X3D playback requires a TimeSensor');
    let targets = options.targets;
    if (!targets) {
        const names = new Set([clock.id, clock.getAttribute('DEF')]);
        targets = elements.filter(node => node.tagName.toLowerCase() === 'route'
            && names.has(node.getAttribute('fromNode')) && node.getAttribute('fromField') === 'fraction_changed')
            .map(route => ({node: named.get(route.getAttribute('toNode')), field: route.getAttribute('toField')}));
    }
    targets = targets.map(target => target && 'node' in target ? target : {node: target, field: 'set_fraction'});
    if (!targets.length || targets.some(target => !target.node || !target.field)) {
        throw new Error('X3D playback requires routed fraction targets');
    }
    const discrete = targets.every(target => /sequencer$/i.test(target.node.tagName));
    const stepSize = Number(options.stepSize ?? .01);
    if (!Number.isFinite(stepSize) || stepSize <= 0 || stepSize > 1) throw new RangeError('Playback step size must lie between 0 and 1');
    const duration = Number(options.duration ?? clock.getAttribute('cycleInterval') ?? 1);
    const speed = Number(options.speed ?? 1);
    const fraction = Number(options.fraction ?? 0);
    if (!Number.isFinite(duration) || duration <= 0) throw new RangeError('Animation duration must be positive');
    if (!Number.isFinite(speed) || speed <= 0) throw new RangeError('Playback speed must be positive');
    if (!Number.isFinite(fraction) || fraction < 0 || fraction > 1) throw new RangeError('Animation fraction must lie between 0 and 1');
    let keys = !discrete ? [] : options.keys || targets.flatMap(target => (target.node.getAttribute('key') || '').trim().split(/[\s,]+/).filter(Boolean).map(Number));
    keys = [...new Set(keys.map(Number).filter(key => Number.isFinite(key) && key >= 0 && key <= 1))].sort((a, b) => a - b);
    if (discrete && !keys.length) {
        const count = Number(clock.getAttribute('data-frame-count'));
        keys = Number.isInteger(count) && count > 1 ? Array.from({length: count}, (_, index) => index / (count - 1)) : [0, 1];
    }
    const clockBoolean = (name, fallback) => {
        const value = clock.getAttribute(name);
        return value === null ? fallback : value.toLowerCase() === 'true';
    };
    const state = {fraction, duration, speed,
        running: options.running ?? clockBoolean('enabled', true),
        loop: options.loop ?? clockBoolean('loop', false)};
    const controls = Object.fromEntries(['toggle', 'restart', 'previous', 'next', 'position', 'speed', 'loop', 'label']
        .map(name => [name, component.query('[data-role="playback-' + name + '"]')]));
    const listeners = new Set();
    let disposed = false, animationFrame = null, lastTime = state.running ? performance.now() : null;
    component.setField(clock, 'enabled', false);
    if (typeof clock.setFieldValue === 'function') clock.setFieldValue('enabled', false);

    function getState() {
        if (!discrete) return {...state};
        let frame = 0;
        keys.forEach((key, index) => { if (key <= state.fraction + 1e-12) frame = index; });
        return {...state, frame};
    }
    function check() { if (disposed) throw new Error('X3D playback is disposed'); }
    function notify() {
        const snapshot = getState();
        if (controls.toggle) controls.toggle.textContent = state.running ? 'Pause' : 'Play';
        if (controls.position) controls.position.value = String(state.fraction);
        if (controls.speed) controls.speed.value = String(state.speed);
        if (controls.loop) controls.loop.checked = state.loop;
        if (controls.previous) controls.previous.textContent = discrete ? 'Previous frame' : 'Back ' + (stepSize * 100) + '%';
        if (controls.next) controls.next.textContent = discrete ? 'Next frame' : 'Forward ' + (stepSize * 100) + '%';
        if (controls.label) controls.label.textContent = (discrete ? (snapshot.frame + 1) + '/' + keys.length + ' · ' : '') + (state.fraction * 100).toFixed(1) + '%';
        for (const listener of listeners) listener(snapshot);
        scene.dispatchEvent(new CustomEvent('x3d-playback-change', {detail: {...snapshot, clock: clock.id || clock.getAttribute('DEF')}}));
    }
    function apply() {
        for (const target of targets) component.setField(target.node, target.field, state.fraction);
        notify();
    }
    function schedule() {
        if (state.running && !disposed && animationFrame === null) animationFrame = requestAnimationFrame(tick);
    }
    function tick(time) {
        animationFrame = null;
        if (disposed || !state.running) return;
        if (lastTime !== null) {
            state.fraction += Math.max(0, time - lastTime) / 1000 * state.speed / duration;
            if (state.fraction >= 1) {
                if (state.loop) state.fraction %= 1;
                else { state.fraction = 1; state.running = false; }
            }
        }
        lastTime = time;
        apply();
        schedule();
    }
    function setRunning(running) {
        check();
        if (Boolean(running) === state.running) return;
        if (running && !state.loop && state.fraction === 1) { state.fraction = 0; apply(); }
        state.running = Boolean(running);
        lastTime = state.running ? performance.now() : null;
        if (!state.running && animationFrame !== null) { cancelAnimationFrame(animationFrame); animationFrame = null; }
        schedule();
        notify();
    }
    function seek(value) {
        check();
        if (!Number.isFinite(value) || value < 0 || value > 1) throw new RangeError('Animation fraction must lie between 0 and 1');
        state.fraction = value;
        lastTime = state.running ? performance.now() : null;
        apply();
    }
    function setSpeed(value) {
        check();
        if (!Number.isFinite(value) || value <= 0) throw new RangeError('Playback speed must be positive');
        state.speed = value;
        lastTime = state.running ? performance.now() : null;
        notify();
    }
    function setLoop(value) { check(); state.loop = Boolean(value); notify(); }
    function step(count = 1) {
        check();
        if (!Number.isInteger(count)) throw new TypeError('Frame step must be an integer');
        if (!count) return;
        setRunning(false);
        if (!discrete) {
            seek(Math.max(0, Math.min(1, state.fraction + count * stepSize)));
            return;
        }
        let index;
        if (count > 0) {
            index = keys.findIndex(key => key > state.fraction + 1e-12);
            if (index < 0) index = keys.length - 1;
            index += count - 1;
        } else {
            index = keys.length - 1;
            while (index > 0 && keys[index] >= state.fraction - 1e-12) index--;
            index += count + 1;
        }
        seek(keys[Math.max(0, Math.min(keys.length - 1, index))]);
    }
    function dispose() {
        if (disposed) return;
        disposed = true;
        state.running = false;
        if (animationFrame !== null) cancelAnimationFrame(animationFrame);
        animationFrame = null;
        listeners.clear();
        clock.setAttribute('enabled', 'false');
    }
    const controller = {play: () => setRunning(true), pause: () => setRunning(false), setRunning,
        restart: () => seek(0), seek, step, setSpeed, setLoop, getState, dispose,
        onChange(listener) {
            check();
            if (typeof listener !== 'function') throw new TypeError('Expected a playback listener');
            listeners.add(listener);
            return () => listeners.delete(listener);
        }};
    if (controls.toggle) component.on(controls.toggle, 'click', () => setRunning(!state.running));
    if (controls.restart) component.on(controls.restart, 'click', controller.restart);
    if (controls.previous) component.on(controls.previous, 'click', () => step(-1));
    if (controls.next) component.on(controls.next, 'click', () => step(1));
    if (controls.position) component.on(controls.position, 'input', () => seek(Number(controls.position.value)));
    if (controls.speed) component.on(controls.speed, 'change', () => setSpeed(Number(controls.speed.value)));
    if (controls.loop) component.on(controls.loop, 'change', () => setLoop(controls.loop.checked));
    component.onDispose(dispose);
    apply();
    schedule();
    return controller;
}
"""

    @staticmethod
    def _walk_scene(element):
        if isinstance(element, (list, tuple)):
            for child in element:
                yield from X3D._walk_scene(child)
        elif hasattr(element, 'tag'):
            yield element
            for child in getattr(element, 'elems', ()):
                yield from X3D._walk_scene(child)

    def _playback_components(self, element):
        if self.use_xite or self.playback is False:
            return []
        controls = []
        for index, node in enumerate(self._walk_scene(element)):
            if str(node.tag).lower() != 'timesensor':
                continue
            attrs = node.attrs
            if self.playback is None and str(attrs.get('data-playback', False)).lower() != 'true':
                continue
            clock_id = attrs.get('id') or attrs.get('DEF') or self.id + '-clock-' + str(index)
            node.attrs = dict(attrs, id=clock_id)
            options = dict(self.playback) if isinstance(self.playback, dict) else {}
            controls.append(X3DComponent(
                self.get_playback_controls(), nodes={'clock': clock_id}, data=options,
                id=clock_id + '-playback', placement='after',
                script=self.get_playback_script() + '\nreturn X3DPlayback(component, {...component.data, clock: component.nodes.clock});'
            ))
        return controls

    def has_playback(self):
        """Whether the scene requests a generic playback toolbar."""
        return not self.use_xite and self.playback is not False and any(
            str(node.tag).lower() == 'timesensor' and (
                self.playback is not None or str(node.attrs.get('data-playback', False)).lower() == 'true'
            ) for node in self._walk_scene(self.to_x3d())
        )

    @classmethod
    def get_export_script(self, id):
        """
        **LLM Docstring**

        Build the JavaScript that exports the scene canvas to a PNG and triggers a download.

        :param id: the scene DOM id
        :type id: str
        :return: the export script
        :rtype: str
        """
        return f"""
(function(){{
  let link = document.createElement('a');
  let base_name = '{id}';
  link.download = base_name + '.png';
  link.href = document.getElementById('{id}').getElementsByTagName('canvas')[0].toDataURL()
  link.click();
}})()
       """

    @classmethod
    def get_ready_check_expression(cls, id):
        """
        **LLM Docstring**

        Build the JavaScript predicate `rasterize` polls (via Playwright's
        `wait_for_function`) to find out whether X3DOM has actually
        started rendering the scene with the given wrapper `id`, instead
        of sleeping a fixed amount of time and hoping it was enough.

        Each `<x3d>` element gets its own `Runtime` object -- attached
        directly to that DOM element as `.runtime`, *not* reachable through
        `x3dom.canvases[...]` -- whose `.isReady` flips `true` on the
        first animation-frame tick once the WebGL backend is set up (right
        before that frame actually renders). Reading it back off the
        element like this, rather than installing our own hook such as a
        custom `x3dom.runtime.ready`, is also what makes this robust to
        `to_widget()`/`to_html()` sometimes emitting the x3dom `<script>`
        tag twice on the same page (harmless for X3DOM itself, but it
        re-runs that script's top-level `var x3dom = {...}` and so would
        silently wipe out any hook installed between the two runs).

        :param id: the scene's wrapper element id (`X3D.id`)
        :type id: str
        :return: the ready-check predicate, as the body of a Playwright
            `wait_for_function` expression
        :rtype: str
        """
        return f"""
    () => {{
      let wrap = document.getElementById('{id}');
      if (!wrap) return false;
      let el = wrap.getElementsByTagName('x3d')[0];
      return !!el && !!el.runtime && el.runtime.isReady === true;
    }}
            """

    @classmethod
    def get_view_settings_script(self, id):
        """
        **LLM Docstring**

        Build the JavaScript that reads the current view matrix and writes it into the view-matrix output field.

        :param id: the scene DOM id
        :type id: str
        :return: the script
        :rtype: str
        """
        return f"""
    (function(){{
        let fig = document.getElementById('{id}');
        let x3d = fig.getElementsByTagName("x3d")[0];
        let vmObj = x3d.runtime.viewMatrix();
        let vmA = [
            [vmObj["_00"], vmObj["_01"], vmObj["_02"], vmObj["_03"]],
            [vmObj["_10"], vmObj["_11"], vmObj["_12"], vmObj["_13"]],
            [vmObj["_20"], vmObj["_21"], vmObj["_22"], vmObj["_23"]],
            [vmObj["_30"], vmObj["_31"], vmObj["_32"], vmObj["_33"]]
        ];
        let out = document.getElementById('{id}-view-matrix');
        out.value = JSON.stringify(vmA, 1);
    }})()
           """

    @classmethod
    def parse_view_matrix(cls, vs):
        """
        **LLM Docstring**

        Convert a serialized X3DOM view matrix into `{position, orientation}` viewpoint
        options (inverting the matrix and extracting the rotation angle/axis).

        :param vs: the view matrix (JSON string or array)
        :return: the viewpoint options
        :rtype: dict
        """
        import json
        if isinstance(vs, str):
            vs = json.loads(vs)
        vm = np.linalg.inv(vs)
        ang, ax = nput.extract_rotation_angle_axis(vm[:3, :3])
        v_pos = vm[:3, -1].tolist()
        v_ort = np.array(list(ax) + [ang]).tolist()
        opts = {"position": v_pos, "orientation": v_ort}
        return opts

    @classmethod
    def get_record_screen_script(self, id, polling_rate=30, recording_duration=2, video_format='video/webm'):
        """
        **LLM Docstring**

        Build the JavaScript that records the scene canvas to a video and triggers a download.

        :param id: the scene DOM id
        :type id: str
        :param polling_rate: the capture frame rate
        :type polling_rate: int
        :param recording_duration: the recording length in seconds
        :type recording_duration: float
        :param video_format: the recording MIME type
        :type video_format: str
        :return: the recording script
        :rtype: str
        """
        return f"""
    (function(){{
        let canvas = document.getElementById('{id}').getElementsByTagName('canvas')[0];
        
        let pollingRate = (typeof canvas.pollingRate === 'undefined') ? {polling_rate} : canvas.pollingRate;
        let videoFormat = (typeof canvas.videoFormat === 'undefined') ? "{video_format}" : canvas.videoFormat;
        let videoExtension = canvas.videoExtension;
        if (typeof canvas.videoExtension === 'undefined') {{
            videoExtension = ''
        }}
        let x3DRecordingStream = canvas.captureStream(pollingRate);
        let mediaRecorder = new MediaRecorder(x3DRecordingStream, {{mimeType: videoFormat}});
        
        mediaRecorder.frames = [];
        mediaRecorder.ondataavailable = function(e) {{
          mediaRecorder.frames.push(e.data);
        }};
        
        mediaRecorder.onstop = function(e) {{
          link = document.createElement('a');
          const base_name = '{id}';
          const blob = mediaRecorder.frames[0];
          link.download = base_name + videoExtension;
          console.log(blob);
          const blobURL = window.URL.createObjectURL(blob);
          link.href = blobURL;
          console.log(blobURL);
          mediaRecorder.frames = [];
          link.click();
        }};
        
        let duration = (typeof canvas.recordingDuration === 'undefined') ? {recording_duration} : canvas.recordingDuration;
        setTimeout(() => {{mediaRecorder.stop()}}, duration * 1000);
        mediaRecorder.start()
    }})()
           """
    @classmethod
    def set_animation_duration_script(self, id):
        """
        **LLM Docstring**

        Build the JavaScript that reads the duration input and stores it on the canvas.

        :param id: the scene DOM id
        :type id: str
        :return: the script
        :rtype: str
        """
        return f"""
    (function(){{
        let canvas = document.getElementById('{id}').getElementsByTagName('canvas')[0];
        let input = document.getElementById('{id}-duration-input');
        
        canvas.recordingDuration = input.value;
    }})()
           """

    @classmethod
    def _create_loader_fragment(cls, i, s):
        """
        **LLM Docstring**

        Build a JavaScript fragment that dynamically injects a preload/onload script or
        library (handling variable capture/restore around the load).

        :param i: the fragment index
        :type i: int
        :param s: the loader spec (a `{lib: callback}` dict, a raw string, or an element)
        :return: the loader fragment
        :rtype: str
        """
        if isinstance(s, dict):
            lib, callback = list(s.items())[0]
            if not isinstance(lib, str):
                var, lib = lib
                if isinstance(var, str):
                    return f'''
try {{
    window._vcontext{i} = {var};
    delete {var};
}} catch (e) {{}}
const frag{i} = document.createElement('script');
frag{i}.src='{lib}';
frag{i}.onload=function() {{window._vcontext{i}; {callback}; var {var} = window._vcontext{i};}};
document.head.append(frag{i});
'''
                else:
                    var, target = var
                    return f'''
try {{
    window._vcontext{i} = {var};
    delete {var};
}} catch (e) {{}}
const frag{i} = document.createElement('script');
frag{i}.src='{lib}';
frag{i}.onload=function() {{let {target} = {var}; {callback}; {var} = window._vcontext{i};}};
document.head.append(frag{i});
'''
            else:
                return f'''
const frag{i} = document.createElement('script');
frag{i}.src='{lib}';
frag{i}.onload=function() {{{callback}}};
document.head.append(frag{i});
'''
        elif isinstance(s, str):
            return f'''(function() {{ {s} }})()'''
        else:
            return f'''const frag{i} = document.createRange().createContextualFragment(`{s.tostring()}`); document.head.appendChild(frag{i});'''

    def get_resource_elements(self):
        """Runtime, styles and preload dependencies for a complete HTML page."""
        elems = [JHTML.Script(src=self.X_ITE_JS)] if self.use_xite else [
            JHTML.Link(rel='stylesheet', href=self.X3DOM_CSS),
            JHTML.Script(src=self.X3DOM_JS)
        ]
        if self.include_mathjax:
            elems.append(JHTML.Script(src=self.MATHJAX_CDN))
        if self.preload_scripts is not None:
            elems.extend(JHTML.Script(s) if isinstance(s, str) else s for s in self.preload_scripts)
        return elems

    def to_widget(self,
                  dynamic_loading=None,
                  include_export_button=None,
                  include_record_button=None,
                  include_view_settings_button=None,
                  include_resources=True
                  ):
        """
        **LLM Docstring**

        Render the scene to an interactive X3DOM widget (cached), wiring up the loader
        scripts and any export/record/view-settings UI.

        :param dynamic_loading: load the runtime dynamically
        :type dynamic_loading: bool | None
        :param include_export_button: include the export button
        :type include_export_button: bool | None
        :param include_record_button: include the record button
        :type include_record_button: bool | None
        :param include_view_settings_button: include the view-settings button
        :type include_view_settings_button: bool | None
        :param include_resources: emit dependencies (false when a document supplies them)
        :type include_resources: bool
        :return: the widget
        """
        if dynamic_loading is None:
            dynamic_loading = self.dynamic_loading
        if include_export_button is None:
            include_export_button = self.include_export_button
        if include_record_button is None:
            include_record_button = self.include_record_button
        if include_view_settings_button is None:
            include_view_settings_button = self.include_view_settings_button
        cache_key = (bool(dynamic_loading), bool(include_export_button), bool(include_record_button),
                     bool(include_view_settings_button), bool(include_resources))
        if cache_key in self._widget_cache:
            self._widg = self._widget_cache[cache_key]
            return self._widg
        id = self.id
        x3d_embed = self.to_x3d()
        components = self.components + tuple(self._playback_components(x3d_embed))

        if not dynamic_loading or not include_resources:
            elems = self.get_resource_elements() if include_resources else []
            base_fig = JHTML.Div(
                *elems,
                x3d_embed,
                id=id,
                width=x3d_embed['width'] if not self.use_xite else x3d_embed.style['width'],
                height=x3d_embed['height'] if not self.use_xite else x3d_embed.style['height'],
                can_be_dynamic=False
            )
        else:
            load_scripts = self.get_resource_elements()
            loader_frags = "\n".join([
                f'''
                const frag{i} = document.createRange().createContextualFragment({json.dumps(load_script.tostring())});
                const elem{i} = frag{i}.firstElementChild;
                const url{i} = elem{i} && (elem{i}.getAttribute('src') || elem{i}.getAttribute('href'));
                const present{i} = url{i} && Array.from(document.querySelectorAll('script[src], link[href]')).some(
                    elem => (elem.getAttribute('src') || elem.getAttribute('href')) === url{i});
                if (!present{i}) document.head.appendChild(frag{i});'''
                for i,load_script in enumerate(load_scripts)
            ])
            if not self.use_xite:
                # A notebook can insert a new scene after X3DOM is already live.
                # reload initializes only new X3D elements and preserves existing ones.
                loader_frags += "\nif (window.x3dom && typeof window.x3dom.reload === 'function') window.x3dom.reload();"
            kill_id = "tmp-"+str(uuid.uuid4())[:10]
            base_fig = JHTML.Figure(
                # JHTML.Link(rel='stylesheet', href=self.X3DOM_CSS),
                x3d_embed,
                JHTML.Image(
                    src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
                    id=kill_id,
                    onload=f"""
                    (function() {{
                        let killElem = document.getElementById('{kill_id}');
                        if (killElem !== null) {{
                            killElem.remove();
                            {loader_frags}
                        }}
                    }})()"""
                    ),
                id=id,
                width=x3d_embed['width'] if not self.use_xite else x3d_embed.style['width'],
                height=x3d_embed['height'] if not self.use_xite else x3d_embed.style['height'],
                can_be_dynamic=False
            )

        elems = [component.to_widget(id) for component in components if component.placement == 'before']
        elems.append(base_fig)
        elems.extend(component.to_widget(id) for component in components if component.placement == 'after')
        if include_export_button:
            elems.append(JHTML.Button("Save Figure", onclick=self.get_export_script(self.id)))
        if include_record_button:
            elems.extend([
                JHTML.Button("Record Animation", onclick=self.get_record_screen_script(self.id, **self.recording_options)),
                JHTML.Input(value=str(self.recording_options.get('recording_duration', 2)),
                            id=self.id+'-duration-input', width="50px", oninput=self.set_animation_duration_script(self.id))
            ])
        if include_view_settings_button:
            elems.append(
                JHTML.Div(
                    [
                        JHTML.Button("Show View Matrix", onclick=self.get_view_settings_script(self.id)),
                        JHTML.Textarea(id=self.id + '-view-matrix')
                    ],
                    display="block"
                )
            )

        if self.onload_scripts is not None and len(self.onload_scripts) > 0:
            loader_frags = "\n".join([
                self._create_loader_fragment(i, load_script)
                for i, load_script in enumerate(self.onload_scripts)
            ])
            kill_id = "tmp-loader-"+str(uuid.uuid4())[:10]
            elems.append(
                JHTML.Image(
                    src='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
                    id=kill_id,
                    onload=f"""
                                (function() {{
                                    let killElem = document.getElementById('{kill_id}');
                                    if (killElem !== null) {{
                                        killElem.remove();
                                        {loader_frags}
                                    }}
                                }})()"""
                )
            )

        if len(elems) > 1:
            self._widg = JHTML.Div(
                *elems
            )
        else:
            self._widg = elems[0]

        self._widget_cache[cache_key] = self._widg
        return self._widg

    def to_html(self, *base_elems, header_elems=None,
                dynamic_loading=False,
                include_export_button=None,
                include_record_button=None,
                **header_info):
        """
        **LLM Docstring**

        Wrap the scene widget in a full HTML document (with the X3DOM CSS/JS in the head).

        :param base_elems: extra body elements
        :param header_elems: extra head elements
        :type header_elems: list | None
        :param dynamic_loading: load the runtime dynamically
        :type dynamic_loading: bool
        :param include_export_button: include the export button
        :type include_export_button: bool | None
        :param include_record_button: include the record button
        :type include_record_button: bool | None
        :param header_info: extra head attributes
        :return: the HTML document
        """
        id = self.id
        x3d_embed = self.to_widget(
            dynamic_loading=dynamic_loading,
            include_export_button=include_export_button,
            include_record_button=include_record_button,
            include_resources=False
        )  # .tostring()

        src = self.get_resource_elements()

        return JHTML.Html(
            JHTML.Head(
                *(header_elems if header_elems is not None else []),
                *src,
                **header_info
            ),
            JHTML.Body(
                *base_elems,
                x3d_embed
            ),
            id=id + '-document'
        )

    def _ipython_display_(self):
        """
        **LLM Docstring**

        Display the scene widget in IPython.
        """
        return self.to_widget()._ipython_display_()
    def get_mime_bundle(self):
        """
        **LLM Docstring**

        Return the scene widget's MIME bundle for rich display.

        :return: the MIME bundle
        :rtype: dict
        """
        return self.to_widget().get_mime_bundle()
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the scene to its `<x3d>` DOM element, formatting the size and rendering each child.
        Loose scene objects are placed inside a Scene so the runtime can initialize them.

        :return: the X3D element
        """
        base_opts = dict(self.defaults, **self.opts)
        for k in ['width', 'height']:
            if k in base_opts:
                v = base_opts[k]
                if nput.is_numeric(v):
                    base_opts[k] = f'{v:.0f}px'
        children = [a.to_x3d() if hasattr(a, 'to_x3d') else a for a in self.children]
        scenes, headers, loose = [], [], []
        for child in children:
            tag = str(getattr(child, 'tag', '')).lower()
            (scenes if tag == 'scene' else headers if tag == 'head' else loose).append(child)
        if not scenes:
            scenes = [X3DScene(*loose).to_x3d()]
        elif loose:
            # Preserve an explicit scene's settings without changing a caller's
            # already rendered element when adding animation drivers or objects.
            scene = scenes[0].copy()
            scene.elems = tuple(scene.elems) + tuple(loose)
            scenes[0] = scene
        elem = X3DHTML.X3D(*headers, *scenes, **base_opts)
        if self.use_xite:
            elem = X3DHTML.X3DCanvas(elem,
                                     width=base_opts['width'],
                                     height=base_opts['height'],
                                     **self.xite_options
                                     )
        return elem
    def display(self):
        """
        **LLM Docstring**

        Display the scene widget.
        """
        return self.to_widget().display()

    def show(self):
        """
        **LLM Docstring**

        Display the scene, enabling dynamic loading when in a Jupyter environment.
        """
        from ..Jupyter.JHTML import JupyterAPIs
        dynamic_loading = JupyterAPIs().in_jupyter_environment()
        self.to_widget(dynamic_loading=dynamic_loading).display()

    def dump(self, file, write_html=True, **opts):
        """
        **LLM Docstring**

        Write the scene to a file, as full HTML or as bare X3D.

        :param file: the destination file
        :param write_html: write full HTML (vs bare X3D)
        :type write_html: bool
        :param opts: extra write options
        :return: the write result
        """
        if write_html:
            html = self.to_html()
        else:
            html = self.to_x3d()
        return html.write(file, **opts)

    def rasterize(self, file, image_format='png', width=None, height=None,
                  device_scale_factor=1,
                  background=None, transparent=None,
                  timeout=15000, executable_path=None, channel=None,
                  browser_args=None, keep_html=False,
                  ready_timeout_action='warn'):
        """
        **LLM Docstring**

        Render this scene to a raster image. This builds the page X3DOM
        needs (the margin reset, the optional background, `to_html`'s own
        CSS/JS embedding) and hands the actual headless-browser work off
        to that page's own `HTML.XMLElement.rasterize` -- the generic
        rasterizer any JHTML element now has -- passing it this scene's
        own X3DOM-specific "is it actually on screen yet" check
        (`get_ready_check_expression`) as its `ready_function`, and the
        rendered `<canvas>` (not the `<x3d>` tag itself, whose own CSS
        layout box is not what you'd expect, or the whole page/viewport)
        as what to screenshot.

        :param file: destination; a path, a writable/bytes-like buffer
            (e.g. `io.BytesIO()`), or `None` to get a new `io.BytesIO` back
        :param image_format: `"png"` or `"jpg"`/`"jpeg"`
        :type image_format: str
        :param width: viewport width; defaults to the scene's own configured width
        :param height: viewport height; defaults to the scene's own configured height
        :param background: an HTML background color to give the page
            before the scene loads (mostly invisible once the scene's own
            canvas covers it; a convenience for callers that already have
            a `facecolor`-style option lying around)
        :param transparent: if truthy, take the screenshot with
            `omit_background=True` so a transparent page background can
            come through as alpha (the WebGL canvas' own pixels are
            unaffected unless the scene itself renders with a transparent
            background)
        :param timeout: milliseconds to wait for the scene-ready signal
            before giving up and capturing whatever is currently rendered
        :type timeout: int
        :param executable_path: forwarded to `resolve_chromium_launch_kwargs`
        :param channel: forwarded to `resolve_chromium_launch_kwargs`
        :param browser_args: extra Chromium command-line flags; defaults to
            `DEFAULT_RASTERIZE_ARGS` (a software-WebGL config that works
            headless without a GPU)
        :param keep_html: if truthy, don't delete the intermediate HTML
            file/directory (useful for debugging what got rendered)
        :type keep_html: bool
        :param ready_timeout_action: `"warn"` (default, via the `warnings`
            module), `"raise"`, or `"ignore"` -- what to do if the
            scene-ready signal doesn't fire within `timeout`
        :type ready_timeout_action: str
        :return: `file` if given (the path or buffer passed in), otherwise
            a new `io.BytesIO` holding the image
        """

        def _px(v):
            if isinstance(v, str):
                v = float(v.rstrip('px').strip())
            return int(round(v))

        if width is None:
            width = self.opts.get('width', self.defaults['width'])
        if height is None:
            height = self.opts.get('height', self.defaults['height'])
        width = _px(width)
        height = _px(height)

        header_elems = [JHTML.Style("html, body { margin:0; padding:0; }")]
        if background is not None:
            header_elems.append(JHTML.Style(f"html, body {{ background:{background}; }}"))

        html = self.to_html(header_elems=header_elems, dynamic_loading=False)

        return html.rasterize(
            file,
            width=width, height=height, device_scale_factor=device_scale_factor,
            ready_function=self.get_ready_check_expression(self.id),
            screenshot_selector=f"#{self.id} canvas",
            image_format=image_format, transparent=transparent, timeout=timeout,
            executable_path=executable_path, channel=channel, browser_args=browser_args,
            keep_html=keep_html, ready_timeout_action=ready_timeout_action,
        )

    def get_children(self):
        """
        **LLM Docstring**

        Return the scene's child objects.

        :return: the children
        :rtype: list
        """
        return self.children

class X3DOptionsSet(X3DObject):
    __props__ = {}

    @classmethod
    def parse_color(cls, color):
        """
        **LLM Docstring**

        Parse a color specification into `(color, transparency)`, resolving named colors /
        hex codes into normalized `[0, 1]` components and splitting off an alpha channel.

        :param color: the color specification
        :return: `(color_components, transparency_or_None)`
        :rtype: tuple
        """
        if isinstance(color, (list, tuple, np.ndarray)) and all(isinstance(c, str) for c in color):
            color = " ".join(color)
        if isinstance(color, str):
            if color == 'transparent':
                color = '#' + 'F'*8
            try:
                _ = [float(s) for s in color.split()]
            except ValueError:
                from .Colors import ColorPalette

                bits = []
                for c in color.split():
                    if c.startswith('#'):
                        c = ColorPalette.parse_rgb_code(c)
                    else:
                        c = np.array(ColorPalette.parse_color_string(c))
                    bit_bits = np.array(c) / 255
                    bits.extend(bit_bits)

            else:
                bits = _
        else:
            bits = color
        if len(bits) > 3:
            color = bits[:-1]
            transparency = bits[-1]
        else:
            color = bits
            transparency = None

        return color, transparency

    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh `x3d-opts-`-prefixed id.

        :return: the id
        :rtype: str
        """
        return "x3d-opts-" + str(uuid.uuid4())[:6]
    def __init__(self, id=None, **attrs):
        """
        **LLM Docstring**

        Hold a set of X3D node attributes under an id.

        :param id: the node id (auto-generated if omitted)
        :param attrs: the node attributes
        """
        if id is None:
            id = self.get_new_id()
        self.id = id
        self.attrs = attrs

    conversion_map = {}
    @classmethod
    def prop_keys(cls):
        """
        **LLM Docstring**

        Return the set of valid property keys (declared props plus conversion-map aliases).

        :return: the valid keys
        :rtype: set
        """
        return (cls.__props__ | cls.conversion_map.keys())
    def prep_attrs(self, attrs:dict):
        """
        **LLM Docstring**

        Canonicalize the node attributes (applying the conversion-map aliases and attaching the id), validating against the declared props.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        :raises ValueError: for invalid attribute keys
        """
        attrs = {
            self.conversion_map.get(k, k):v
            for k,v in attrs.items()
        }
        excess_keys = attrs.keys() - self.__props__
        if len(excess_keys) > 0:
            cls = type(self).__name__
            raise ValueError(f"keys {excess_keys} are invalid keys for {cls}")
        attrs['id'] = self.id
        return attrs

    @classmethod
    def resolve_prop_attr(self, prop_name):
        """
        **LLM Docstring**

        Map a property name to its X3D attribute name via the conversion map.

        :param prop_name: the property name
        :return: the attribute name
        """
        return self.conversion_map.get(prop_name, prop_name)

    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the node id carrying a given property (this node).

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        return self.id

class X3DMaterial(X3DOptionsSet):
    __props__ = {
        "diffuseColor",
        "ambientIntensity",
        "emissiveColor",
        "specularColor",
        "shininess",
        "transparency",
        "baseColorFactor",
        "metallicFactor",
        "roughnessFactor",
        "alphaMode"
        # "metadata"
    }
    conversion_map = {
        "brightness": "ambientIntensity",
        "glow": "emissiveColor",
        "color": "diffuseColor",
        "metal_color": "baseColorFactor",
        "metallic": "metallicFactor",
        "roughness": "roughnessFactor",
        "specularity": "specularColor"
    }
    def prep_attrs(self, attrs:dict):
        """
        **LLM Docstring**

        Canonicalize the material attributes (resolving the color into components/transparency) before rendering.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        if attrs.get('color') is not None:
            new_attrs = attrs.copy()
            color, transparency = self.parse_color(attrs['color'])
            new_attrs['color'] = color
            if transparency is not None:
                new_attrs['transparency'] = transparency
        else:
            new_attrs = attrs
        new_attrs = {k:v for k,v in new_attrs.items() if v is not None}
        return super().prep_attrs(new_attrs)
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the material to its X3D DOM element.

        :return: the X3D element
        """
        attrs = self.prep_attrs(self.attrs)
        if (
                attrs.get('roughnessFactor') is not None
                or attrs.get('metallicFactor') is not None
                or attrs.get('baseColorFactor') is not None
                or attrs.get('emissiveFactor') is not None
        ):
            if 'baseColorFactor' not in attrs and 'diffuseColor' in attrs:
                attrs['baseColorFactor'] = attrs.pop('diffuseColor')
            if 'emissiveFactor' not in attrs and 'emissiveColor' in attrs:
                attrs['emissiveFactor'] = attrs.pop('emissiveColor')
            if 'metallicFactor' not in attrs and 'shininess' in attrs:
                attrs['metallicFactor'] = attrs.pop('shininess') / 100
            if 'transparency' in attrs:
                tp =  attrs.pop('transparency')
                bcf = attrs.get('baseColorFactor')
                if bcf is not None:
                    attrs["baseColorFactor"] = list(bcf)[:3] + [1-tp]
                if "alphaMode" not in attrs:
                    attrs["alphaMode"] = "BLEND"
                if "alphaCutoff" not in attrs:
                    attrs["alphaCutoff"] = 0.1
            mat = X3DHTML.PhysicalMaterial(**attrs)
            return mat
        else:
            return X3DHTML.Material(**attrs)

class X3DTexture(X3DOptionsSet):
    __props__ = {
        "url",
        "image",
        "crossOrigin",
        "hideChildren",
        "metadata",
        "repeatS",
        "repeatT",
        "scale",
        "textureProperties",
        "texture_type"
    }
    conversion_map = {
    }
    # def prep_attrs(self, attrs: dict):
    #     if 'color' in attrs:
    #         new_attrs = attrs.copy()
    #         color, transparency = self.parse_color(attrs['color'])
    #         new_attrs['color'] = color
    #         if transparency is not None:
    #             new_attrs['transparency'] = transparency
    #     else:
    #         new_attrs = attrs
    #     return super().prep_attrs(new_attrs)
    texture_type_mapping = {
        "pixel":X3DHTML.PixelTexture,
        "image":X3DHTML.ImageTexture,
        "movie":X3DHTML.MovieTexture
    }
    movie_types = ['.mp4', '.webm']
    @classmethod
    def infer_texture_type(self, ats):
        """
        **LLM Docstring**

        Infer the texture type (pixel/image/movie) from the supplied attributes.

        :param ats: the texture attributes
        :type ats: dict
        :return: the texture type name
        :rtype: str
        """
        if "image" in ats:
            return "pixel"
        elif "loop" in ats or any(ats['url'].endswith(mt) for mt in self.movie_types):
            return "movie"
        else:
            return "image"
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the texture to its X3D DOM element, dispatching on the (inferred) texture type.

        :return: the X3D element
        """
        ats = self.prep_attrs(self.attrs)
        texture_type = ats.pop('texture_type', None)
        if texture_type is None:
            texture_type = self.infer_texture_type(ats)
        if isinstance(texture_type, str):
            texture_type = self.texture_type_mapping[texture_type]
        texture_type:X3DHTML.Texture|X3DHTML.MovieTexture|X3DHTML.PixelTexture|X3DHTML.ImageTexture
        return texture_type(**ats)

class X3DAppearance(X3DOptionsSet):
    __props__ = {
        "alphaClipThreshold",
        "blendMode",
        "colorMaskMode"
        "depthMode"
        "lineProperties"
        "material"
        "metadata"
        "pointProperties"
        "shaders",
        "sortKey",
        "sortType",
        "texture",
        "textureTransform"
    }
    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh appearance id.

        :return: the id
        :rtype: str
        """
        return "x3d-appearance-" + str(uuid.uuid4())[:6]
    def prep_attrs(self, attrs:dict):
        """
        **LLM Docstring**

        Canonicalize the appearance attributes, splitting the material/texture/line/point sub-properties out into their own nodes.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        material_keys = attrs.keys() & X3DMaterial.prop_keys()
        line_keys = attrs.keys() & X3DLineProperties.prop_keys()
        point_keys = attrs.keys() & X3DPointProperties.prop_keys()

        rem_keys = attrs.keys() - (
            X3DMaterial.prop_keys()
            | X3DLineProperties.prop_keys()
            | X3DPointProperties.prop_keys()
        )
        base_attrs = {k:attrs[k] for k in rem_keys}

        if len(material_keys) > 0:
            base_attrs['material'] = {k:attrs[k] for k in material_keys}

        if len(line_keys) > 0:
            base_attrs['lineProperties'] = {k:attrs[k] for k in line_keys}

        if len(point_keys) > 0:
            base_attrs['pointProperties'] = {k:attrs[k] for k in point_keys}

        if 'id' in base_attrs:
            base_attrs['DEF'] = base_attrs['id']
        return base_attrs
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the appearance to its X3D DOM element (with its material/texture/line/point child nodes).

        :return: the X3D element
        """
        base_attrs = self.prep_attrs(self.attrs)
        if 'id' in base_attrs:
            base_attrs['DEF'] = base_attrs['id']

        comps = []
        line_props = base_attrs.pop('lineProperties', None)
        if line_props is not None:
            if isinstance(line_props, dict):
                line_props = X3DLineProperties(id=self.id+'-lineprops', **line_props)
            if isinstance(line_props, X3DLineProperties):
                line_props = line_props.to_x3d()
            comps.append(line_props)

        point_props = base_attrs.pop('pointProperties', None)
        if point_props is not None:
            if isinstance(point_props, dict):
                point_props = X3DPointProperties(id=self.id+'-pointprops', **point_props)
            if isinstance(point_props, X3DPointProperties):
                point_props = point_props.to_x3d()
            comps.append(point_props)

        texture_props = base_attrs.pop('texture', None)
        if texture_props is not None:
            if isinstance(texture_props, str):
                texture_props = {'url':texture_props}
            if isinstance(texture_props, dict):
                texture_props = X3DTexture(id=self.id+'-texture', **texture_props)
            if isinstance(texture_props, X3DTexture):
                texture_props = texture_props.to_x3d()
            comps.append(texture_props)

        material_props = base_attrs.pop('material', None)
        if material_props is not None:
            if isinstance(material_props, dict):
                material_props = X3DMaterial(id=self.id+'-material', **material_props)
            if isinstance(material_props, X3DMaterial):
                material_props = material_props.to_x3d()
            comps.append(material_props)

        return X3DHTML.Appearance(*comps, **base_attrs)

    @classmethod
    def resolve_prop_attr(self, prop_name):
        """
        **LLM Docstring**

        Map a property name to the appearance sub-node attribute it animates.

        :param prop_name: the property name
        :return: the attribute name
        """
        if prop_name in X3DAppearance.prop_keys():
            return self.conversion_map.get(prop_name, prop_name)
        elif prop_name in X3DLineProperties.prop_keys():
            return X3DLineProperties.conversion_map.get(prop_name, prop_name)
        elif prop_name in X3DLineProperties.prop_keys():
            return X3DLineProperties.conversion_map.get(prop_name, prop_name)
        elif prop_name in X3DMaterial.prop_keys():
            return X3DMaterial.conversion_map.get(prop_name, prop_name)
        else:
            raise ValueError(f"property {prop_name} not known")

    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the id of the appearance sub-node (material/texture/...) carrying a property.

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        if prop_name in X3DAppearance.prop_keys():
            return self.id
        elif prop_name in X3DLineProperties.prop_keys():
            return self.id+'-lineprops'
        elif prop_name in X3DLineProperties.prop_keys():
            return self.id+'-pointprops'
        elif prop_name in X3DMaterial.prop_keys():
            return self.id+'-material'
        else:
            raise ValueError(f"property {prop_name} not known")

class X3DLineProperties(X3DOptionsSet):
    __props__ = {
        "applied",
        "linetype",
        "linewidth",
        "linewidthScaleFactor"
    }
    conversion_map = {
        "line_style":"linetype",
        "line_thickness":"linewidth"
    }
    def prep_attrs(self, attrs:dict):
        """
        **LLM Docstring**

        Canonicalize the line-properties attributes (resolving the color into components/transparency) before rendering.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        attrs = super().prep_attrs(attrs)
        attrs['linewidthScaleFactor'] = attrs.get('linewidthScaleFactor', '1')
        attrs['containerField'] = attrs.get('containerField', 'lineProperties')
        if 'id' in attrs:
            attrs['DEF'] = attrs['id']
        return attrs
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the line properties to its X3D DOM element.

        :return: the X3D element
        """
        return X3DHTML.LineProperties(**self.prep_attrs(self.attrs))

class X3DPointProperties(X3DOptionsSet):
    __props__ = {
        "attenuation",
        "pointSizeMaxValue",
        "pointSizeMinValue",
        "pointSizeScaleFactor"
    }
    conversion_map = {
        "point_size":"pointSizeScaleFactor"
    }
    def prep_attrs(self, attrs:dict):
        """
        **LLM Docstring**

        Canonicalize the point-properties attributes (resolving the color into components/transparency) before rendering.

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        attrs = super().prep_attrs(attrs)
        attrs['containerField'] = attrs.get('containerField', 'pointProperties')
        attrs['pointSizeMaxValue'] = str(
            max([
                float(attrs.get('pointSizeMaxValue', '0')),
                float(attrs.get('pointSizeMinValue', '0')),
                float(attrs.get('pointSizeScaleFactor', '0')),
            ])
        )
        if 'id' in attrs:
            attrs['DEF'] = attrs['id']
        return attrs
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the point properties to its X3D DOM element.

        :return: the X3D element
        """
        return X3DHTML.PointProperties(**self.prep_attrs(self.attrs))

class X3DPrimitive(X3DObject):
    wrapper_class = None
    tag_class = None
    @classmethod
    def get_new_id(cls):
        """
        **LLM Docstring**

        Generate a fresh `x3d-obj-`-prefixed id.

        :return: the id
        :rtype: str
        """
        return "x3d-obj-" + str(uuid.uuid4())[:6]
    def __init__(self, *children, id=None, **opts):
        """
        **LLM Docstring**

        Set up a primitive holding its child objects and options (under an id).

        :param children: the child objects
        :param id: the primitive id (auto-generated if omitted)
        :param opts: the primitive options
        """
        if len(children) == 1 and isinstance(children[0], (tuple, list)):
            children = children[0]
        self.children = children
        if id is None:
            id = self.get_new_id()
        opts['id'] = id
        self.opts = opts
    @property
    def id(self):
        """
        **LLM Docstring**

        The primitive's id.

        :return: the id
        :rtype: str
        """
        return self.opts['id']
    @id.setter
    def id(self, new_id):
        """
        **LLM Docstring**

        The primitive's id.

        :return: the id
        :rtype: str
        """
        self.opts['id'] = new_id
    def split_opts(self, opts:dict):
        """
        **LLM Docstring**

        Split options into the non-appearance options and the material/appearance/line/point options.

        :param opts: the options
        :type opts: dict
        :return: `(object_opts, appearance_opts)`
        :rtype: tuple
        """
        material_keys = opts.keys() & (
            X3DMaterial.prop_keys()
            | X3DAppearance.prop_keys()
            | X3DLineProperties.prop_keys()
            | X3DPointProperties.prop_keys()
        )
        rem_keys = opts.keys() - material_keys
        return {k:opts[k] for k in rem_keys}, {k:opts[k] for k in material_keys}
    def get_appearance(self, appearance_options):
        """
        **LLM Docstring**

        Build the appearance node from the appearance options (or `None` if there are none).

        :param appearance_options: the appearance options
        :type appearance_options: dict
        :return: the appearance element (or `None`)
        """
        if len(appearance_options) > 0:
            return X3DAppearance(id=self.id+"-appearance", **appearance_options).to_x3d()
        else:
            return None
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the primitive to its X3D DOM element, wrapping its children and appearance under the tag/wrapper classes.

        :return: the X3D element
        """
        obj_opts, appearance_opts = self.split_opts(self.opts)
        if 'id' in obj_opts:
            obj_opts['DEF'] = obj_opts['id']
        kids = [k.to_x3d() if hasattr(k, 'to_x3d') else k for k in self.children]
        appearance = self.get_appearance(appearance_opts)
        if self.tag_class is None:
            if appearance is not None:
                kids = [appearance] + kids
            return self.wrapper_class(
                kids,
                **obj_opts
            )
        else:
            core = self.tag_class(kids, **obj_opts)
            appearance = self.get_appearance(appearance_opts)
            if appearance is not None:
                return self.wrapper_class(appearance, core)
            else:
                return core

    @classmethod
    def resolve_prop_attr(self, prop_name):
        """
        **LLM Docstring**

        Map a property name to its attribute, routing appearance properties through the appearance node.

        :param prop_name: the property name
        :return: the attribute name
        """
        if prop_name in (
                X3DMaterial.prop_keys()
                | X3DAppearance.prop_keys()
                | X3DLineProperties.prop_keys()
                | X3DPointProperties.prop_keys()
        ):
            return X3DAppearance.resolve_prop_attr(prop_name)
        #TODO: handle mapping of transform props
        else:
            return prop_name

    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the node id carrying a property, routing appearance properties to the appearance node.

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        if prop_name in (
            X3DMaterial.prop_keys()
            | X3DAppearance.prop_keys()
            | X3DLineProperties.prop_keys()
            | X3DPointProperties.prop_keys()
        ):
            return X3DAppearance(id=self.id + "-appearance").get_prop_node_id(prop_name)
        else:
            return self.id

    def get_children(self):
        """
        **LLM Docstring**

        Return the primitive's child objects.

        :return: the children
        :rtype: list
        """
        return self.children

class X3DBackground(X3DOptionsSet):
    wrapper_class = X3DHTML.Background
    __props__ = {
        'skyColor', 'skyAngle', 'groundColor', 'groundAngle',
        'backUrl', 'bottomUrl', 'frontUrl', 'leftUrl', 'rightUrl', 'topUrl'
    }
    conversion_map = {"color": "skyColor", "ground_color": "groundColor"}
    def prep_attrs(self, attrs: dict):
        attrs = super().prep_attrs(attrs)
        for key in ('skyColor', 'groundColor'):
            color = attrs.get(key)
            if color is None: continue
            if isinstance(color, (list, tuple)) and color and not isinstance(color[0], (int, float, str)):
                # multiple stops -> parse each and flatten to the MFColor string
                attrs[key] = " ".join(" ".join(str(x) for x in self.parse_color(c)[0]) for c in color)
            else:
                color, transparency = self.parse_color(color)
                attrs[key] = color
                if key == 'skyColor' and transparency is not None:
                    attrs['transparency'] = transparency
        if 'id' in attrs:
            attrs['DEF'] = attrs['id']
        return attrs
    def to_x3d(self):
        return X3DHTML.Background(**self.prep_attrs(self.attrs))

class X3DEnvironment(X3DOptionsSet):
    wrapper_class = X3DHTML.Environment
    __props__ = {
        'ambientOcclusionRadius',
        'ambientOcclusionType',
        'frameBufferScale',
        'gammaCorrectionDefault',
        'reflectionIntensity',
        'smallFeatureCulling',
        'smallFeatureThreshold',
        'sortObjects',
        'sortTrans',
        'tessellationDetail'
    }
    def to_x3d(self):
        """
        Render the environment to its X3D DOM element.

        :return: the X3D element
        """
        return X3DHTML.Environment(**self.prep_attrs(self.attrs))

class X3DLight(X3DOptionsSet):
    """
    Base for the `X3DLightNode` family (`DirectionalLight`/`PointLight`/`SpotLight`),
    holding the fields they all share.
    """
    __props__ = {
        'ambientIntensity',
        'color',
        'global',
        'intensity',
        'on'
    }
    conversion_map = {
        'brightness': 'ambientIntensity',
        'enabled': 'on',
        'global_': 'global'
    }
    def prep_attrs(self, attrs: dict):
        """
        Canonicalize the light attributes (resolving `color`; lights have no transparency channel).

        :param attrs: the attributes
        :type attrs: dict
        :return: the canonicalized attributes
        :rtype: dict
        """
        attrs = super().prep_attrs(attrs)
        color = attrs.get('color', None)
        if color is not None:
            attrs['color'] = self.parse_color(color)[0]
        if 'id' in attrs:
            attrs['DEF'] = attrs['id']
        return attrs

class X3DDirectionalLight(X3DLight):
    wrapper_class = X3DHTML.DirectionalLight
    __props__ = X3DLight.__props__ | {'direction'}
    def to_x3d(self):
        """
        Render the light to its X3D DOM element.

        :return: the X3D element
        """
        return X3DHTML.DirectionalLight(**self.prep_attrs(self.attrs))

class X3DPointLight(X3DLight):
    wrapper_class = X3DHTML.PointLight
    __props__ = X3DLight.__props__ | {'attenuation', 'location', 'radius'}
    def to_x3d(self):
        """
        Render the light to its X3D DOM element.

        :return: the X3D element
        """
        return X3DHTML.PointLight(**self.prep_attrs(self.attrs))

class X3DSpotLight(X3DPointLight):
    wrapper_class = X3DHTML.SpotLight
    __props__ = X3DPointLight.__props__ | {'beamWidth', 'cutOffAngle', 'direction'}
    def to_x3d(self):
        """
        Render the light to its X3D DOM element.

        :return: the X3D element
        """
        return X3DHTML.SpotLight(**self.prep_attrs(self.attrs))

class X3DNavigationInfo(X3DOptionsSet):
    wrapper_class = X3DHTML.NavigationInfo
    __props__ = {
        'avatarSize',
        'headlight',
        'speed',
        'transitionTime',
        'transitionType',
        'type',
        'visibilityLimit'
    }
    def to_x3d(self):
        """
        Render the navigation info to its X3D DOM element.

        :return: the X3D element
        """
        return X3DHTML.NavigationInfo(**self.prep_attrs(self.attrs))

class X3DScene(X3DPrimitive):
    wrapper_class = X3DHTML.Scene
    default_light_type = 'directional'
    light_types = {
        'directional': X3DDirectionalLight,
        'point': X3DPointLight,
        'spot': X3DSpotLight
    }
    default_viewpoint = {'viewAll':True}
    camera_sensor_def = "CameraSensor"      # new
    camera_rig_def = "CameraLightRig"       # new
    children: list
    def __init__(self, *children:X3DPrimitive,
                 background=None,
                 environment=True,
                 lighting=None,
                 navigation=None,
                 viewpoint=None, **opts):
        """
        **LLM Docstring**

        Set up a scene primitive with an optional background and viewpoint.

        :param children: the scene's child primitives
        :param background: the background specification
        :param viewpoint: the viewpoint specification
        :param environment: `True`/`False`/`None`, a dict of `Environment` options, or an `X3DEnvironment`
        :param lighting: a list of light specs (dicts with a `type` key resolving via `light_types`, or `X3DLight` instances)
        :param opts: extra scene options
        """
        if viewpoint is None:
            viewpoint = self.default_viewpoint
        elif viewpoint is False:
            viewpoint = {}
        super().__init__(*children, **opts)
        if isinstance(background, dict):
            background = X3DBackground(**background)
        elif background is not None and not isinstance(background, (X3DObject, X3DHTML.X3DElement)):
            background = X3DBackground(color=background)
        if background is not None:
            self.children = [background] + list(self.children)
        if environment is True:
            environment = X3DEnvironment(reflectionIntensity=1.0)
        elif isinstance(environment, dict):
            environment = X3DEnvironment(**environment)
        if environment is not None:
            self.children = [environment] + list(self.children)
        if lighting is not None:
            static_specs, follow_specs = self._split_lighting(lighting)
            new_children = [self.resolve_light(l) for l in static_specs]
            if len(follow_specs) > 0:
                rig_children = [self.resolve_light(l).to_x3d() for l in follow_specs]
                sensor = X3DHTML.ProximitySensor(
                    DEF=self.camera_sensor_def,
                    center=(0, 0, 0),
                    size=(100000, 100000, 100000),
                )
                rig = X3DHTML.Transform(*rig_children, DEF=self.camera_rig_def)
                route = X3DHTML.Route(
                    fromNode=self.camera_sensor_def, fromField="orientation_changed",
                    toNode=self.camera_rig_def, toField="set_rotation",
                )
                new_children = [sensor, rig, route] + new_children
            self.children = new_children + list(self.children)
        if navigation is not None:
            if isinstance(navigation, dict):
                navigation = X3DNavigationInfo(**navigation)
            self.children = [navigation] + list(self.children)
        if len(viewpoint) > 0:
            viewpoint = self.get_view_settings(**viewpoint)
            self.children = [X3DHTML.Viewpoint(**viewpoint)] + list(self.children)

    @classmethod
    def _split_lighting(cls, lighting):
        """
        Split a `lighting` list into (static_specs, follow_specs) by popping each
        dict spec's `follow_view` flag. Already-built X3DObject light instances have
        no flag to inspect and are always treated as static.
        """
        static_specs = []
        follow_specs = []
        for l in lighting:
            if isinstance(l, X3DObject):
                static_specs.append(l)
                continue
            l = dict(l)
            follow_view = l.pop('follow_view', False)
            (follow_specs if follow_view else static_specs).append(l)
        return static_specs, follow_specs
    @classmethod
    def resolve_light(cls, light_spec) -> X3DLight:
        """
        Resolve a lighting spec (a dict keyed by light `type`, defaulting to `default_light_type`,
        or an already-built light object) into an `X3DLight` instance.
        :param light_spec: the lighting spec
        :return: the light
        :rtype: X3DLight
        """
        if isinstance(light_spec, X3DObject):
            return light_spec
        light_spec = dict(light_spec)
        light_type = light_spec.pop('type', cls.default_light_type)
        light_cls = cls.light_types[light_type]
        return light_cls(**light_spec)

    default_up_vector = (0, 1, 0)
    default_right_vector = (1, 0, 0)
    default_view_vector = (0, 0, 1)
    default_view_distance = 10
    @classmethod
    def get_view_settings(cls,
                          up_vector=None, view_vector=None, right_vector=None,
                          view_distance=None,
                          view_center=None,
                          view_matrix=None,
                          view_position=None,
                          return_settings=False,
                          **etc):
        """
        **LLM Docstring**

        Build viewpoint settings (position/orientation/etc.) from a flexible view
        specification.

        :param args: positional view arguments
        :param kwargs: view options
        :return: the viewpoint settings
        :rtype: dict
        """
        # CO = coords0[1] - coords0[0]
        # OH = coords0[5] - coords0[1]
        if view_matrix is None:
            if view_vector is None:
                if (
                    up_vector is not None and right_vector is not None
                ):
                    view_vector = nput.vec_crosses(up_vector, right_vector, normalize=True)
                elif right_vector is not None:
                    view_vector = nput.vec_crosses(cls.default_up_vector, right_vector, normalize=True)
                elif up_vector is not None:
                    view_vector = nput.vec_crosses(up_vector, cls.default_right_vector, normalize=True)

            if view_vector is not None:
                m = nput.rotation_matrix(
                    view_vector,
                    cls.default_view_vector
                )
            else:
                m = np.eye(3)

            if up_vector is None and right_vector is not None:
                if view_vector is None:
                    view_vector = cls.default_view_vector
                up_vector = nput.vec_normalize(
                    nput.vec_crosses(right_vector, view_vector)
                )
            elif up_vector is not None and view_vector is not None:
                up_vector = nput.vec_crosses(
                    view_vector,
                    nput.vec_crosses(view_vector, up_vector),
                    normalize=True
                )
            if up_vector is not None:
                m = m @ nput.rotation_matrix(
                    m.T @ up_vector,
                    cls.default_up_vector
                )
            view_matrix = m

        ang, cross = nput.extract_rotation_angle_axis(view_matrix)
        if view_vector is None:
            view_vector = view_matrix[:, -1]
        if view_position is None:
            if view_distance is None:
                view_distance = cls.default_view_distance
            view_position = view_distance * nput.vec_normalize(np.asanyarray(view_vector))
            if view_center is not None:
                if isinstance(view_center, dict):
                    view_center = view_center['untransformed']
                else:
                    view_center = view_matrix @ np.asanyarray(view_center)
                view_position = view_distance * nput.vec_normalize(
                    view_position + view_center
                )
        else:
            if isinstance(view_position, dict):
                view_position = view_position['untransformed']
            else:
                view_position = view_matrix @ np.asanyarray(view_position)
        if return_settings:
            return dict(
                {
                    'view_angle': ang,
                    'rotation_axis': cross,
                    'view': view_vector,
                    'dist': view_distance,
                    'center': view_center
                },
                **etc
            )
        else:
            return dict(
                {
                    'orientation': list(cross) + [ang],
                    'position': view_position
                },
                **etc
            )

class X3DCoordinate(X3DPrimitive):
    wrapper_class = X3DHTML.Coordinate
    def __init__(self, points, id=None, **etc):
        """
        **LLM Docstring**

        Hold a set of coordinate points as an X3D coordinate node.

        :param points: the coordinate points
        :param id: the node id
        :param etc: extra options
        """
        super().__init__(point=self.prep_points(points), id=id, **etc)
    @classmethod
    def prep_points(cls, points):
        """
        **LLM Docstring**

        Normalize coordinate points into the X3D point format.

        :param points: the points
        :return: the prepared points
        """
        return " ".join(np.asanyarray(np.round(points, 4)).flatten().astype(str))

class X3DColor(X3DPrimitive):
    wrapper_class = X3DHTML.Color
    def __init__(self, colors, id=None, **etc):
        """
        **LLM Docstring**

        Hold a set of per-vertex colors as an X3D color node.

        :param colors: the colors
        :param id: the node id
        :param etc: extra options
        """
        super().__init__(color_list=colors, id=id, **etc)
    def split_opts(self, opts:dict):
        """
        **LLM Docstring**

        Split options for the color node (colors aren't material properties).

        :param opts: the options
        :type opts: dict
        :return: `(object_opts, appearance_opts)`
        :rtype: tuple
        """
        base_opts, appearance_opts = super().split_opts(opts)
        base_opts['color'] = self.prep_color(base_opts.pop('color_list'))
        return base_opts, appearance_opts
    @classmethod
    def prep_color(cls, points):
        """
        **LLM Docstring**

        Normalize color values into the X3D color format.

        :param points: the colors
        :return: the prepared colors
        """
        if isinstance(points, str):
            points = X3DOptionsSet.parse_color(points)[0]
        elif isinstance(points[0], str):
            points = [X3DOptionsSet.parse_color(p)[0] for p in points]
        return " ".join(np.asanyarray(np.round(points, 4)).flatten().astype(str))

class X3DGroup(X3DPrimitive):
    wrapper_class = X3DHTML.Group

class X3DSwitch(X3DPrimitive):
    wrapper_class = X3DHTML.Switch

class X3DGeometryObject(X3DPrimitive):
    wrapper_class = X3DHTML.Shape
    def __init__(self, *args, id=None, **opts):
        """
        **LLM Docstring**

        Set up a geometry object, splitting the material options out and preparing the geometry options.

        :param args: the geometry-defining arguments
        :param id: the object id
        :param opts: the geometry and material options
        """
        geom_opts, self.material_opts = self.split_opts(opts)
        self.geometry_opts = self.prep_geometry_opts(*args, **geom_opts)
        super().__init__(id=id)
    def get_interpolated_attributes(self):
        """
        **LLM Docstring**

        Return the geometry plus material attributes used for animation.

        :return: the attributes
        :rtype: dict
        """
        return dict(self.geometry_opts, **self.material_opts)
    @abc.abstractmethod
    def prep_geometry_opts(self, *args, **opts) -> dict:
        """
        **LLM Docstring**

        Abstract: build the geometry options for this shape from its defining arguments.

        :param args: the shape arguments
        :param opts: extra options
        :return: the geometry options
        :rtype: dict
        """
        ...
    def create_tag_object(self, **core_opts):
        """
        **LLM Docstring**

        Build the core geometry tag element from the core options.

        :param core_opts: the core geometry options
        :return: the geometry element
        """
        if 'id' in core_opts:
            core_opts['DEF'] = core_opts['id']
        return self.tag_class(**core_opts)
    def create_object(self,
                      translation=None,
                      rotation=None,
                      scale=None,
                      normal=None,
                      up_vector=None,
                      bbox_center=None,
                      **core_opts):
        """
        **LLM Docstring**

        Build the geometry element together with its transform (translation/rotation/
        scale), computing the rotation needed to align the shape's up-vector with a
        supplied normal.

        :param translation: the translation
        :param rotation: the base rotation (axis-angle)
        :param scale: the scale
        :param normal: a normal to orient the shape toward
        :param up_vector: the shape's reference up-vector
        :param bbox_center: the bounding-box center
        :param core_opts: the core geometry options
        :return: `(geometry_element, transform_dict_or_None)`
        :rtype: tuple
        """
        core_opts['id'] = core_opts.get('id', self.id)
        core_opts['DEF'] = core_opts["id"]
        base_obj = self.create_tag_object(**core_opts)
        tf = {}
        if normal is not None:
            if up_vector is None:
                up_vector = [0, 0, 1]
            angs, crosses, cn = nput.vec_angles(up_vector, normal, return_crosses=True, return_norms=False, return_cross_norms=True)
            if cn < 1e-6:
                orth = [1, 0, 0]
                if abs(np.dot(up_vector, orth)) < 1e-6:
                    orth = [0, 1, 0]
                crosses = nput.vec_crosses(orth, up_vector, normalize=True)
                if np.dot(normal, up_vector) > 0:
                    angs = 0
                else:
                    angs = np.pi
            if rotation is not None:
                if isinstance(rotation, str):
                    rotation = np.array(rotation.split()).astype(float)
                full_rot = (
                    nput.rotation_matrix(crosses, angs)
                        @ nput.rotation_matrix(rotation[:3], rotation[3])
                )
                angs, crosses = nput.extract_rotation_angle_axis(full_rot)
            rotation = np.concatenate([crosses, [angs]])
        for k,v in [["translation",translation], ["rotation",rotation], ["scale", scale], ['bboxcenter', bbox_center]]:
            if v is not None:
                tf[k] = np.round(v, 4) if not isinstance(v, str) else v
        if len(tf) == 0:
            tf = None
        # base_obj = X3DHTML.Transform(base_obj, translation=translation, rotation=rotation, scale=scale)
        return base_obj, tf
    def get_rotation(self, axis, up_vector=None):
        """
        **LLM Docstring**

        Compute the axis-angle rotation that aligns an up-vector with a target axis (and the axis norm).

        :param axis: the target axis
        :param up_vector: the reference up-vector
        :return: `(axis_angle_rotation, axis_norm)`
        :rtype: tuple
        """
        if up_vector is None:
            up_vector = [0, 1, 0]
        angs, crosses, norms = nput.vec_angles(up_vector, axis, return_crosses=True, return_norms=True)
        # Antiparallel vectors have a zero cross product, but a pi rotation
        # still needs a valid axis. This occurs for the reverse arrowhead.
        antiparallel = (np.linalg.norm(crosses, axis=-1) < 1.e-12) & np.isclose(angs, np.pi)
        if np.any(antiparallel):
            up = np.broadcast_to(np.asarray(up_vector, dtype=float), np.shape(crosses))
            reference = np.eye(3)[np.argmin(np.abs(up), axis=-1)]
            fallback = nput.vec_crosses(up, reference, normalize=True)
            crosses = np.where(np.asarray(antiparallel)[..., np.newaxis], fallback, crosses)
        if nput.is_numeric(angs):
            return np.concatenate([crosses, [angs]]), norms[1]
        else:
            return np.concatenate([crosses, angs[..., np.newaxis]], axis=-1), norms[1]

    transform_props = ("translation", "rotation", "scale", "bboxcenter")
    def get_prop_node_id(self, prop_name):
        """
        **LLM Docstring**

        Return the node id carrying a property, routing transform properties to the transform node.

        :param prop_name: the property name
        :return: the node id
        :rtype: str
        """
        if prop_name in self.transform_props:
            return self.id + "-transform"
        else:
            return super().get_prop_node_id(prop_name)
    def to_x3d(self):
        """
        **LLM Docstring**

        Render the geometry to its X3D DOM element, wrapping it in its appearance and transform.

        :return: the X3D element
        """
        # obj_opts, material_opts = self.split_opts(self.opts)
        # kids = [k.to_x3d() for k in self.children]
        core, tf = self.create_object(**self.geometry_opts)
        appearance = self.get_appearance(self.material_opts)
        if appearance is not None:
            core = self.wrapper_class(appearance, core)
        if tf is not None:
            core = X3DHTML.Transform(core, id=core.id+"-transform", DEF=core.id+"-transform", **tf)
        return core

class X3DGeometryGroup(X3DGeometryObject):
    @abc.abstractmethod
    def prep_geometry_opts(self, *args, **opts) -> list[dict]:
        """
        **LLM Docstring**

        Abstract: build a list of per-instance geometry option dicts for this (possibly batched) shape.

        :param args: the shape arguments
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        ...
    def get_interpolated_attributes(self):
        """
        **LLM Docstring**

        Return the first instance's geometry plus material attributes used for animation.

        :return: the attributes
        :rtype: dict
        """
        return dict(self.geometry_opts[0], **self.material_opts)
    def prep_vecs(self, vecs, nstruct=None):
        """
        **LLM Docstring**

        Broadcast a vector (or `None`) across `nstruct` instances.

        :param vecs: the vector(s) (or `None`)
        :param nstruct: the number of instances
        :type nstruct: int | None
        :return: the per-instance vectors
        :rtype: np.ndarray | list
        """
        if vecs is None:
            return [None] * nstruct
        else:
            vecs = np.asanyarray(vecs)
            if vecs.ndim == 1:
                vecs = vecs[np.newaxis]
            if nstruct is not None:
                vecs = np.broadcast_to(vecs, (nstruct, vecs.shape[-1]))
        return vecs
    def prep_mats(self, mats, nstruct=None):
        """
        **LLM Docstring**

        Broadcast a matrix (or `None`) across `nstruct` instances.

        :param mats: the matrix/matrices (or `None`)
        :param nstruct: the number of instances
        :type nstruct: int | None
        :return: the per-instance matrices
        :rtype: np.ndarray | list
        """
        if mats is None:
            return [None] * nstruct
        else:
            mats = np.asanyarray(mats)
            if mats.ndim == 2:
                mats = mats[np.newaxis]
            if nstruct is not None:
                mats = np.broadcast_to(mats, (nstruct,) + mats.shape[-2:])
            return mats
    def prep_const(self, const, nstruct):
        """
        **LLM Docstring**

        Broadcast a scalar constant (or `None`) across `nstruct` instances.

        :param const: the constant (or `None`)
        :param nstruct: the number of instances
        :type nstruct: int
        :return: the per-instance constants
        :rtype: np.ndarray | list
        """
        if const is None:
            return [None] * nstruct
        else:
            const = np.asanyarray(const)
            if const.ndim == 0:
                const = const[np.newaxis]
            const = np.broadcast_to(const, (nstruct,))
            return const
    def to_x3d(self):
        """
        **LLM Docstring**

        Render every instance to its X3D element (wrapped in appearance/transform), grouping them under a single group node.

        :return: the X3D element
        """
        kids = [self.create_object(**g) for g in self.geometry_opts]
        appearance = self.get_appearance(self.material_opts)
        objs = []
        for i,(o,tf) in enumerate(kids):
            if hasattr(o, 'id'):
                id = o.id
            else:
                try:
                    id = o['id']
                except KeyError:
                    id = None
            if appearance is not None:
                o = self.wrapper_class(appearance, o)
            if tf is not None:
                o = X3DHTML.Transform(o, id=id+"-transform", DEF=id+"-transform", **tf)
            objs.append(o)
        if len(objs) == 1:
            return objs[0]
        else:
            return X3DHTML.Group(objs)

class X3DSphere(X3DGeometryGroup):
    tag_class = X3DHTML.Sphere

    def prep_geometry_opts(self, centers, radius=1, **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for spheres at the given centers.

        :param centers: the sphere centers
        :param radius: the sphere radius/radii
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        centers = self.prep_vecs(centers)
        rads = self.prep_const(radius, centers.shape[0])
        return [{"translation":c, "radius":r, **opts} for c,r in zip(centers, rads)]

class X3DBox(X3DGeometryGroup):
    tag_class = X3DHTML.Box

    def prep_geometry_opts(self, starts, ends, normal=None, rotation=None, **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for boxes spanning the given corner pairs.

        :param starts: the min corners
        :param ends: the max corners
        :param normal: a normal to orient the boxes toward
        :param rotation: a base rotation
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        starts = self.prep_vecs(starts)
        ends = self.prep_vecs(ends)
        if normal is None:
            normal = [0, 1, 0]
        normal = self.prep_vecs(normal, len(starts))
        axes = self.prep_vecs([0, 1, 0], len(starts))
        rots, norms = self.get_rotation(axes, normal)

        rmats = nput.rotation_matrix(rots[:, :3], rots[:, 3])
        sizes = ((ends - starts) @ rmats).reshape(starts.shape)

        if rotation is not None:
            rots = self.prep_vecs(rotation, len(starts))

        return [
            {"translation": s, "rotation": a,
             "size": " ".join(np.round(size, 4).astype(str)) if not isinstance(size, str) else size,
             **opts}
            for s,a,size in zip((starts + ends) / 2, rots, sizes)
        ]

class X3DCylinder(X3DGeometryGroup):
    tag_class = X3DHTML.Cylinder

    @staticmethod
    def _geometry_scale(radius, height, scale=None):
        dimensions = np.array([radius, height, radius], dtype=float)
        if scale is not None:
            if isinstance(scale, str):
                scale = scale.split()
            dimensions = dimensions * np.asarray(scale, dtype=float)
        return dimensions

    def create_object(self, *, radius=1, height=2, scale=None, **opts):
        # Animate a unit cylinder's transform. X3DOM 1.8.3 does not invalidate
        # cylinder GPU positions when its radius reaches zero, leaving the last
        # nonzero mesh visible. Transform.scale handles zero dimensions without
        # changing cached geometry or requiring geometry-field update events.
        return super().create_object(radius=1, height=1,
                scale=self._geometry_scale(radius, height, scale), **opts)

    def get_interpolated_attributes(self):
        attrs = super().get_interpolated_attributes()
        radius = attrs.pop('radius', 1)
        height = attrs.pop('height', 2)
        attrs['scale'] = self._geometry_scale(radius, height, attrs.get('scale'))
        return attrs

    def prep_geometry_opts(self, starts, ends, radius=1, closed=True, top=None, bottom=None, **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for cylinders between the given endpoints.

        :param starts: the start points
        :param ends: the end points
        :param radius: the cylinder radius/radii
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        starts = self.prep_vecs(starts)
        ends = self.prep_vecs(ends)
        radius = self.prep_const(radius, starts.shape[0])
        if closed is True:
            closed = [True, True]
        elif closed is False:
            closed = [False, False]

        closed = self.prep_vecs(closed, starts.shape[0])
        if bottom is None:
            bottom = [c[0] for c in closed]
        bottom = self.prep_const(bottom, starts.shape[0])
        if top is None:
            top = [c[1] for c in closed]
        top = self.prep_const(top, starts.shape[0])


        axes = ends - starts
        rots, norms = self.get_rotation(axes)

        return [
            {"translation":s, "rotation":a, "height":n, "radius":r, 'bottom':b, 'top':t, **opts}
            for s,a,n,r,b,t in zip((starts + ends) / 2, rots, norms, radius, bottom, top)
        ]

class X3DCone(X3DGeometryGroup):
    tag_class = X3DHTML.Cone

    def prep_geometry_opts(self, starts, ends, radius=1, top_radius=None, **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for cones (or truncated cones) between the given endpoints.

        :param starts: the base points
        :param ends: the apex points
        :param radius: the base radius/radii
        :param top_radius: the top radius (for truncated cones)
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        starts = self.prep_vecs(starts)
        ends = self.prep_vecs(ends)
        radius = self.prep_const(radius, starts.shape[0])
        top_radius = self.prep_const(top_radius, starts.shape[0])

        axes = ends - starts
        rots, norms = self.get_rotation(axes)

        return [
            {"translation":s, "rotation":a, "height":n, "bottomRadius":r, "topRadius":t, **opts}
            for s,a,n,r,t in zip((starts + ends) / 2, rots, norms, radius, top_radius)
        ]

class X3DArrow(X3DGroup):

    arrowhead_class = X3DCone
    cylinder_class = X3DCylinder

    def __init__(self,
                 starts, ends,
                 radius=1,
                 top_radius=None,
                 arrowhead_radius=2,
                 arrowhead_radius_mode='scaled',
                 arrowhead_offset=.3,
                 arrowhead_offset_mode='scaled',
                 cylinder_class=None,
                 arrowhead_class=None,
                 double_sided=False,
                 **opts):
        """
        **LLM Docstring**

        Build an arrow between two endpoints, optionally with a head at each end.

        ``double_sided=True`` points both heads outward and trims the shaft at
        both bases. Each head uses the existing radius and offset settings;
        its length is capped at half the span so the heads do not cross.

        :param args: the arrow-defining arguments (endpoints, etc.)
        :param double_sided: place outward-pointing heads at both endpoints
        :type double_sided: bool
        :param opts: styling and geometry options
        """
        if arrowhead_class is None:
            arrowhead_class = self.arrowhead_class
        if cylinder_class is None:
            cylinder_class = self.cylinder_class

        starts, ends = np.broadcast_arrays(np.asarray(starts, dtype=float),
                                           np.asarray(ends, dtype=float))
        arrow_vectors = ends - starts
        norms = nput.vec_norms(arrow_vectors)
        unit_vectors = np.divide(arrow_vectors, np.asarray(norms)[..., np.newaxis],
                                 out=np.zeros_like(arrow_vectors),
                                 where=np.asarray(norms)[..., np.newaxis] != 0)
        arrowhead_offset = np.asarray(arrowhead_offset)
        if arrowhead_offset_mode == 'scaled':
            arrowhead_offset = arrowhead_offset * norms
        if double_sided:
            arrowhead_offset = np.minimum(arrowhead_offset, norms / 2)
        disp_vectors = arrowhead_offset[..., np.newaxis] * unit_vectors
        arrow_starts = ends - disp_vectors
        if arrowhead_radius_mode == 'scaled':
            arrowhead_radius = np.asarray(arrowhead_radius) * np.asarray(radius)
        arrowheads = arrowhead_class(arrow_starts, ends,
                                     radius=arrowhead_radius,
                                     top_radius=top_radius,
                                     **opts)
        if double_sided:
            tail_starts = starts + disp_vectors
            tail_heads = arrowhead_class(tail_starts, starts,
                                         radius=arrowhead_radius,
                                         top_radius=top_radius,
                                         **opts)
            cylinders = cylinder_class(tail_starts, arrow_starts, radius=radius, **opts)
            super().__init__(arrowheads, tail_heads, cylinders)
        else:
            cylinders = cylinder_class(starts, arrow_starts, radius=radius, **opts)
            super().__init__(arrowheads, cylinders)

class X3DCappedCylinder(X3DGroup):

    cap_class = X3DSphere
    cylinder_class = X3DCylinder

    def __init__(self,
                 starts, ends,
                 radius=1,
                 cylinder_class=None,
                 cap_class=None,
                 cap_offset=0,
                 use_caps=(True, True),
                 **opts):
        """
        **LLM Docstring**

        Build a capped cylinder (a cylinder plus end-cap spheres/disks) between two
        endpoints.

        :param args: the cylinder-defining arguments
        :param opts: styling and geometry options
        """
        if cap_class is None:
            cap_class = self.cap_class
        if cylinder_class is None:
            cylinder_class = self.cylinder_class

        if cap_offset != 0:
            raise NotImplementedError("cap offseting not supported yet")

        if use_caps is True: use_caps = [True, True]
        elif use_caps is False: use_caps = [False, False]

        cap_list = []
        if use_caps[0]:
            cap_list.append(cap_class(starts, radius=radius, **opts))
        if use_caps[1]:
            cap_list.append(cap_class(ends, radius=radius, **opts))
        cylinders = cylinder_class(starts, ends, radius=radius, **opts)

        super().__init__(
            *cap_list, cylinders
        )

class X3DText(X3DGeometryGroup):
    tag_class = X3DHTML.Text

    def __init__(self, *args, billboard=True, solid=None, billboard_opts=None, **opts):
        """
        **LLM Docstring**

        Build a text geometry, optionally billboarded to face the camera.

        :param args: the text-defining arguments
        :param billboard: face the camera
        :type billboard: bool
        :param solid: render single-sided
        :param billboard_opts: options for the billboard
        :type billboard_opts: dict | None
        :param opts: extra options
        """
        if solid is None:
            solid = bool(billboard)
        if billboard:
            if billboard_opts is None:
                billboard_opts = {'axisOfRotation':'0 0 0'}
            self.wrapper_class = lambda *x,**y:X3DHTML.Billboard(X3DHTML.Shape(*x, **y), **billboard_opts)
        super().__init__(*args, solid=solid, **opts)
    def create_tag_object(self, font_style=None, **core_opts):
        """
        **LLM Docstring**

        Build the text geometry tag with its font style.

        :param font_style: the font styling
        :type font_style: dict | None
        :param core_opts: the core geometry options
        :return: the text element
        """
        body = []
        if font_style is not None:
            body.append(font_style)
        if 'id' in core_opts:
            core_opts['DEF'] = core_opts['id']
        return self.tag_class(body, **core_opts)
    def prep_geometry_opts(self, centers, text, font_style=None, rotation=None, normal=None, **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for text labels at the given centers.

        :param centers: the label positions
        :param text: the label text
        :param font_style: the font styling
        :param rotation: a base rotation
        :param normal: a normal to orient the text toward
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        centers = self.prep_vecs(centers)
        rotation = self.prep_vecs(rotation, len(centers))
        normal = self.prep_vecs(normal, len(centers))
        text = self.prep_const(text, len(centers))
        if font_style is None:
            font_style = {}
        subfonts =  {o.partition("_")[-1]: v for o, v in opts.items() if o.startswith('font_')}
        for f in subfonts:
            del opts['font_' + f]
        font_style = subfonts | font_style
        if len(font_style) == 0:
            font_style = None
        font_style = [
            X3DHTML.FontStyle(**fs)
                if fs is not None else
            None
            for fs in self.prep_const(font_style, len(centers))
        ]
        return [
            {"translation": c, 'string': t, 'length': len(t), 'font_style':fs, 'rotation':r, 'normal':n, **opts}
            for c, t, fs, r, n in zip(centers, text, font_style, rotation, normal)
        ]

class X3DTorus(X3DGeometryGroup):
    tag_class = X3DHTML.Torus

    def prep_geometry_opts(self, centers, radius=1, inner_radius=None,
                           normal=None, rotation=None, scale=None,
                           angle=None,
                           **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for tori at the given centers.

        :param centers: the torus centers
        :param radius: the outer radius/radii
        :param inner_radius: the inner (tube) radius
        :param opts: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        if angle is not None and angle < 0:
            if rotation is None:
                rotation = [0, 0, 1, 0]
            if isinstance(rotation, str):
                rotation = np.array(rotation.split()).astype(float)
            rotation = list(rotation[:3]) + [rotation[3] + angle]
            angle = abs(angle)
        centers = self.prep_vecs(centers)
        normal = self.prep_vecs(normal, centers.shape[0])
        rotation = self.prep_vecs(rotation, centers.shape[0])
        scale = self.prep_vecs(scale, centers.shape[0])
        radius = self.prep_const(radius, centers.shape[0])
        inner_radius = self.prep_const(inner_radius, centers.shape[0])
        angle = self.prep_const(angle, centers.shape[0])

        return [
            {
                "translation": s, "normal": n, "outerRadius": r,
                "innerRadius": i, 'rotation': rot, 'scale': sc,
                'angle': ang,
                **opts}
            for s, n, rot, sc, r, i, ang in zip(
                centers, normal,
                rotation, scale,
                radius, inner_radius, angle
            )
        ]

class X3DCoordinatesWrapper(X3DGeometryGroup):
    tag_class: X3DHTML.X3DElement
    def create_tag_object(self, *, point, color=None, **etc):
        """
        **LLM Docstring**

        Build the geometry tag wrapping a coordinate (and optional color) node.

        :param point: the coordinate points
        :param color: the per-vertex colors
        :param etc: extra options
        :return: the geometry element
        """
        body = [X3DCoordinate(point, id=self.id+"-coord", DEF=self.id+"-coord").to_x3d()]
        if color is not None:
            body.append(X3DColor(color, id=self.id+'-color', DEF=self.id+"-coord").to_x3d())
        return self.tag_class(body, **etc)
    def prep_geometry_opts(self, point, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for a coordinate-backed geometry.

        :param point: the coordinate points
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        return [
            dict({"translation":"0,0,0", "point":point}, **etc)
        ]

class X3DVertexCoordinatesWrapper(X3DCoordinatesWrapper):
    tag_class: X3DHTML.X3DElement
    def prep_geometry_opts(self, point, vertex_colors=None, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for a vertex-coordinate geometry with optional per-vertex colors.

        :param point: the vertex points
        :param vertex_colors: the per-vertex colors
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        base_dict = super().prep_geometry_opts(point, **etc)
        if vertex_colors is not None:
            if isinstance(vertex_colors[0], str) or nput.is_numeric(vertex_colors[0][0]):
                for bd in base_dict:
                    bd['colorPerVertex'] = bd.get('colorPerVertex', True)
                    bd['color'] = vertex_colors
            else:
                for bd, cc in zip(base_dict, vertex_colors):
                    bd['colorPerVertex'] = bd.get('colorPerVertex', True)
                    bd['color'] = cc
        return base_dict

class X3DIndexedCoordinatesWrapper(X3DCoordinatesWrapper):
    def prep_geometry_opts(self, point, indices, vertex_colors=None, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for an indexed-coordinate geometry.

        :param point: the coordinate points
        :param indices: the connectivity indices
        :param vertex_colors: the per-vertex colors
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        base_dict = dict(
                {
                    'index': " ".join(np.asanyarray(indices).flatten().astype(int).astype(str))
                },
                **super().prep_geometry_opts(point, **etc)[0]
            )
        if vertex_colors is not None:
            base_dict['colorPerVertex'] = True
            base_dict['color'] = vertex_colors
        return [base_dict]

class X3DGeometry2DGroup(X3DGeometryGroup):
    def __init__(self, *args, billboard=False, billboard_opts=None, **opts):
        """
        **LLM Docstring**

        Set up a 2D geometry group, optionally billboarded to face the camera.

        :param args: the geometry-defining arguments
        :param billboard: face the camera
        :type billboard: bool
        :param billboard_opts: billboard options
        :type billboard_opts: dict | None
        :param opts: extra options
        """
        if billboard:
            if billboard_opts is None:
                billboard_opts = {'axisOfRotation':'0 0 0'}
            self.wrapper_class = lambda *x,**y:X3DHTML.Billboard(X3DHTML.Shape(*x, **y), **billboard_opts)
        super().__init__(*args, **opts)
    @classmethod
    def prep_2d_coords(cls, coords):
        """
        **LLM Docstring**

        Normalize coordinates into the 2D geometry point format.

        :param coords: the coordinates
        :return: the prepared 2D coordinates
        """
        coords = np.asanyarray(coords)
        coords = coords.reshape(-1, coords.shape[-1])
        if coords.shape[-1] == 2:
            coords = np.pad(coords, [[0, 0], [0, 1]])
        return coords
    def prep_geometry_opts(self, center, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for a 2D geometry at the given center.

        :param center: the geometry center
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        center = self.prep_2d_coords(center)
        return [
            {
                "translation":c,
                 **etc
            }
            for c in center
        ]

class X3DRectangle2D(X3DGeometry2DGroup):
    tag_class = X3DHTML.Rectangle2D
    def prep_geometry_opts(self, left_endpoints, right_endpoints, normal=None, rotation=None, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for 2D rectangles spanning the given endpoint pairs.

        :param left_endpoints: the min corners
        :param right_endpoints: the max corners
        :param normal: a normal to orient toward
        :param rotation: a base rotation
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        left_endpoints = self.prep_2d_coords(left_endpoints)
        right_endpoints = self.prep_2d_coords(right_endpoints)
        center = (left_endpoints + right_endpoints ) / 2
        base_opts = super().prep_geometry_opts(center, **etc)

        if normal is None and rotation is not None:
            normal = np.array([0, 0, 1])
            rotation = np.asanyarray(rotation)
            if np.asanyarray(rotation).ndim > 1:
                normal = np.repeat(normal[np.newaxis], len(rotation), axis=0)
        if normal is not None:
            embedding_axes = nput.rotation_matrix(normal, [0, 0, 1])
            if rotation is not None:
                rotation = np.asanyarray(rotation)
                embedding_axes = embedding_axes @ nput.rotation_matrix(rotation[..., :3], rotation[..., 3])
            right_endpoints = (right_endpoints - center) @ embedding_axes
            left_endpoints = (left_endpoints - center) @ embedding_axes
        normal = self.prep_vecs(normal, right_endpoints.shape[0])
        rotation = self.prep_vecs(rotation, right_endpoints.shape[0])
        size_x = np.abs(right_endpoints[..., 0] - left_endpoints[..., 0])
        size_y = np.abs(right_endpoints[..., 1] - left_endpoints[..., 1])
        return [
            dict(b, size=[x, y], normal=n, rotation=r)
            for b,x,y,n,r in zip(base_opts, size_x, size_y, normal, rotation)
        ]
class X3DCircle2D(X3DGeometry2DGroup):
    tag_class = X3DHTML.Circle2D
    def prep_geometry_opts(self, centers, radius=1,
                           normal=None, rotation=None, scale=None,
                           angle=None,
                           **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for 2D circles at the given centers.

        :param centers: the circle centers
        :param radius: the radius/radii
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        centers = self.prep_vecs(centers)
        normal = self.prep_vecs(normal, centers.shape[0])
        if angle is not None and angle < 0:
            if rotation is None:
                rotation = [0, 0, 1, 0]
            if isinstance(rotation, str):
                rotation = np.array(rotation.split()).astype(float)
            rotation = list(rotation[:3]) + [rotation[3] + angle]
            angle = abs(angle)
        rotation = self.prep_vecs(rotation, centers.shape[0])
        scale = self.prep_vecs(scale, centers.shape[0])
        radius = self.prep_const(radius, centers.shape[0])
        angle = self.prep_const(angle, centers.shape[0])

        return [
            {
                "translation": s, "normal": n, "radius": r,
                'rotation': rot, 'scale': sc,
                'angle': ang,
                **opts}
            for s, n, rot, sc, r, ang in zip(
                centers, normal,
                rotation, scale,
                radius, angle
            )
        ]

class X3DDisk2D(X3DGeometry2DGroup):
    tag_class = X3DHTML.Disk2D

    def prep_geometry_opts(self, centers, radius=1, inner_radius=None,
                           normal=None, rotation=None, scale=None,
                           angle=None,
                           **opts):
        """
        **LLM Docstring**

        Build the per-instance geometry options for 2D disks (or annuli) at the given centers.

        :param centers: the disk centers
        :param radius: the outer radius/radii
        :param inner_radius: the inner radius (for annuli)
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        centers = self.prep_vecs(centers)
        normal = self.prep_vecs(normal, centers.shape[0])
        if angle is not None and angle < 0:
            if rotation is None:
                rotation = [0, 0, 1, 0]
            if isinstance(rotation, str):
                rotation = np.array(rotation.split()).astype(float)
            rotation = list(rotation[:3]) + [rotation[3] + angle]
            angle = abs(angle)
        rotation = self.prep_vecs(rotation, centers.shape[0])
        scale = self.prep_vecs(scale, centers.shape[0])
        radius = self.prep_const(radius, centers.shape[0])
        inner_radius = self.prep_const(inner_radius, centers.shape[0])
        angle = self.prep_const(angle, centers.shape[0])

        return [
            {
                "translation": s, "normal": n, "outerRadius": r,
                "innerRadius": i, 'rotation': rot, 'scale': sc,
                'angle': ang,
                **opts}
            for s, n, rot, sc, r, i, ang in zip(
                centers, normal,
                rotation, scale,
                radius, inner_radius, angle
            )
        ]
class X3DPolyline2D(X3DGeometry2DGroup):
    tag_class = X3DHTML.Polyline2D

class X3DPointSet(X3DVertexCoordinatesWrapper):
    tag_class = X3DHTML.PointSet
class X3DLine(X3DCoordinatesWrapper):
    tag_class = X3DHTML.LineSet
class X3DTriangleSet(X3DCoordinatesWrapper):
    tag_class = X3DHTML.TriangleSet
class X3DIndexedTriangleSet(X3DIndexedCoordinatesWrapper):
    tag_class = X3DHTML.IndexedTriangleSet
class X3DIndexedLineSet(X3DIndexedCoordinatesWrapper):
    tag_class = X3DHTML.IndexedLineSet
    def prep_geometry_opts(self, point, indices, **etc):
        """
        **LLM Docstring**

        Build the per-instance geometry options for an indexed line set.

        :param point: the coordinate points
        :param indices: the line connectivity indices
        :param etc: extra options
        :return: the per-instance geometry options
        :rtype: list
        """
        opts = super().prep_geometry_opts(point, indices, **etc)
        opts[0]['coordIndex'] = opts[0].pop('index')
        return opts
class X3DIndexedQuadSet(X3DIndexedCoordinatesWrapper):
    tag_class = X3DHTML.IndexedQuadSet
class X3DIndexedFaceSet(X3DIndexedCoordinatesWrapper):
    tag_class = X3DHTML.IndexedFaceSet

class X3DGenericAnimator(X3DGroup):
    def __init__(self, *animation_data, id=None, animation_duration=2, running=True, slider=False, playback=True,
                 **opts):
        """
        **LLM Docstring**

        Build an animator group: the animated objects, a time clock/sequencer, the
        per-property interpolators/sequencers, and playback controls outside the scene.

        :param animation_data: the animation data (interpreted by the subclass)
        :param id: the animator id (auto-generated if omitted)
        :param animation_duration: the loop duration in seconds
        :type animation_duration: float
        :param running: start the animation running
        :type running: bool
        :param slider: legacy alias enabling the playback toolbar and timeline
        :type slider: bool
        :param playback: include general playback controls when embedded in X3D
        :type playback: bool
        :param opts: extra options
        """
        self.uuid = str(uuid.uuid4())
        if id is None:
            id = f"animation-{self.uuid}"

        animated_objects, attributes, nframes = self.get_animation_objects(animation_data, id)
        elements = list(animated_objects)
        driver = self.build_animator_group(attributes,
                                      nframes=nframes,
                                      animation_duration=animation_duration,
                                      running=running,
                                      uuid=self.uuid
                                      )
        driver[0].attrs.update({'data-playback': bool(playback or slider), 'data-frame-count': nframes})
        elements.extend(driver)

        super().__init__(elements, id=id, DEF=id, **opts)

    @classmethod
    @abc.abstractmethod
    def get_animation_objects(cls, animation_data, id) -> tuple[list[X3DObject], dict, int]:
        """
        **LLM Docstring**

        Abstract: build the `(objects, per-property attribute sets, frame count)` for the animation.

        :param animation_data: the animation data
        :param id: the animator id
        :return: `(objects, attribute_sets, nframes)`
        :rtype: tuple
        """
        ...

    @classmethod
    def build_animator_group(cls, attribute_sets, nframes, *, uuid, running=True, animation_duration=2):
        """
        **LLM Docstring**

        Build the animation driver nodes: a time sensor, an integer sequencer keyed to the
        frames, the routing between them, and the per-property animation controls.

        :param attribute_sets: the per-object property attribute sets
        :param nframes: the number of frames
        :type nframes: int
        :param uuid: the animation uuid
        :param running: start running
        :type running: bool
        :param animation_duration: the loop duration in seconds
        :type animation_duration: float
        :return: the driver nodes
        :rtype: list
        """
        key_frames = np.linspace(0, 1, nframes+1)[:-1]
        base = [
            X3DHTML.TimeSensor(id=f'animation-clock-{uuid}', DEF=f'animation-clock-{uuid}',
                               cycleInterval=animation_duration, loop=True,
                               enabled=running),
            X3DHTML.IntegerSequencer(id=f'animation-indexer-{uuid}', DEF=f'animation-indexer-{uuid}',
                                     key=key_frames,
                                     keyValue=np.arange(nframes)),
            X3DHTML.Route(
                fromField='fraction_changed', fromNode=f'animation-clock-{uuid}',
                toField='set_fraction', toNode=f'animation-indexer-{uuid}'
            )
        ]
        controls = sum((
            cls.create_animation_control(name, uuid=uuid, **opts)
            for attributes in attribute_sets
            for name,opts in attributes.items()),
            []
        )
        controls = [c for c in controls if c is not None]
        if not any(str(c.tag).lower() == 'route'
                   and c.attrs.get('fromNode') == f'animation-indexer-{uuid}' for c in controls):
            # Interpolating-only animations have no discrete index consumer.
            base = base[:1]
        return base + controls

    @classmethod
    def resolve_control_type(cls, name, values):
        """
        **LLM Docstring**

        Decide whether a property animates by discrete indexing or by interpolation (from its value sequence).

        :param name: the property name
        :param values: the per-frame values
        :return: `'indexed'` or `'interpolated'`
        :rtype: str
        """
        if np.all(values == np.arange(1, len(values)+1)):
            return 'indexed'
        else:
            return 'interpolated'

    interpolator_map = {
        ('color', 'glow'): X3DHTML.ColorInterpolator,
        ('position', 'translation'): X3DHTML.PositionInterpolator,
        ('point', 'coordinate'): X3DHTML.CoordinateInterpolator,
        ('rotation',): X3DHTML.OrientationInterpolator
    }
    @classmethod
    def resolve_interpolator_type(cls, name, values):
        """
        **LLM Docstring**

        Determine the X3D interpolator class (and frame count) for a property from its
        name and the shape/type of its values.

        :param name: the property name
        :type name: str
        :param values: the per-frame values
        :return: `(interpolator_class, nframes)`
        :rtype: tuple
        :raises ValueError: if the interpolator can't be determined
        """
        nl = name.lower()
        for k,t in cls.interpolator_map.items():
            if any(kl in nl for kl in k):
                interp_type = t
                if issubclass(interp_type, X3DHTML.PositionInterpolator):
                    values = np.asanyarray(values)
                    if values.ndim == 1:
                        nframes = len(values) // 3
                    else:
                        nframes = len(values)
                elif issubclass(interp_type, X3DHTML.OrientationInterpolator):
                    values = np.asanyarray(values)
                    if values.ndim == 1:
                        nframes = len(values) // 4
                    else:
                        nframes = len(values)
                # elif issubclass(interp_type, X3DHTML.CoordinateInterpolator):
                #    ## Ill-defined if flattened
                else:
                    nframes = len(values)
                break
        else:
            values = np.asanyarray(values)
            nframes = len(values)
            if np.issubdtype(values.dtype, np.dtype(str)):
                interp_type = X3DHTML.ColorInterpolator
            elif values.ndim == 1:
                interp_type = X3DHTML.ScalarInterpolator
            elif values.ndim == 2 and values.shape[-1] == 3:
                interp_type = X3DHTML.PositionInterpolator
            elif values.ndim == 3 and values.shape[-1] == 3:
                interp_type = X3DHTML.CoordinateInterpolator
            elif values.ndim == 2 and values.shape[-1] == 4:
                interp_type = X3DHTML.OrientationInterpolator
            else:
                raise ValueError(f"interpolator can't be determined for property {name} with shape {values.shape}")

        return interp_type, nframes

    @classmethod
    def _raf_get_color_array_interpolator(cls,
                                          *,
                                          key,
                                          keyValue,
                                          id,
                                          clockId,
                                          targetId):
        """
        **LLM Docstring**

        Build a `requestAnimationFrame`-driven JavaScript interpolator for animating a
        per-vertex color array (which X3DOM can't interpolate natively).

        :param args: the interpolator-defining arguments
        :param kwargs: interpolator options
        :return: the interpolator nodes/scripts
        """
        key = np.asanyarray(key).tolist()
        keyValue = np.asanyarray(keyValue).tolist()

        key_js = json.dumps(key)
        keyValue_js = json.dumps(keyValue)

        return X3DHTML.Script(f'''
  let keys = {key_js};
  let keyValues = {keyValue_js};
  let numPoints = keyValues[0].length;

  function interpolateColors(f) {{
    let i = 0;
    while (i < keys.length - 2 && f >= keys[i + 1]) {{
      i++;
    }}
    let k0 = keys[i], k1 = keys[i + 1];
    let t = (k1 > k0) ? (f - k0) / (k1 - k0) : 0.0;
    t = Math.max(0.0, Math.min(1.0, t));

    let parts = [];
    for (let p = 0; p < numPoints; p++) {{
      let c0 = keyValues[i][p];
      let c1 = keyValues[i + 1][p];
      parts.push(
        (c0[0] + t * (c1[0] - c0[0])).toFixed(4) + " " +
        (c0[1] + t * (c1[1] - c0[1])).toFixed(4) + " " +
        (c0[2] + t * (c1[2] - c0[2])).toFixed(4)
      );
    }}
    return parts.join(" ");
  }}

  document.addEventListener("DOMContentLoaded", function () {{
    const ts = document.getElementById("{clockId}");
    const colorNode = document.getElementById("{targetId}");
    // cycleInterval read directly off the clock (attribute is a string)
    function getCycleInterval() {{
      const raw = ts.getAttribute("cycleInterval");
      const v = parseFloat(raw);
      return v > 0 ? v : 1.0; // guard against 0/NaN -> avoids divide-by-zero
    }}

    let lastColorString = null;
    let lastElapsed = null;

    function getElapsed() {{
        const node = ts._x3domNode;
        // _vf holds the field values; elapsedTime is maintained there while running
        if (node && node._vf && typeof node._vf.elapsedTime === "number") {{
            return node._vf.elapsedTime;
        }}
        return null;
    }}

    function tick() {{
      // ts.elapsedTime is exposed on the X3DOM node once the runtime is live.
      // Before that it's undefined, so fall back to 0.
      const elapsed = getElapsed()??0;
      if (lastElapsed == elapsed) {{ requestAnimationFrame(tick); return }};
      const cycle = getCycleInterval();

      // fraction in [0,1), looping — matches loop="True"
      const f = (elapsed % cycle) / cycle;

      const colorString = interpolateColors(f);

      // skip the setAttribute when nothing changed (cheap dedupe)
      if (colorString !== lastColorString) {{
        colorNode.setAttribute("color", colorString);
        lastColorString = colorString;
      }}

      requestAnimationFrame(tick);
    }}
    requestAnimationFrame(tick);
  }});
    ''', id=id)

    @classmethod
    def get_color_array_interpolator(cls,
                                     *,
                                     key,
                                     keyValue,
                                     id,
                                     DEF,
                                     clockId,
                                     targetId):
        """
        **LLM Docstring**

        Build the color-array interpolator for animating per-vertex colors across frames.

        :param args: the interpolator-defining arguments
        :param kwargs: interpolator options
        :return: the interpolator nodes
        """
        color_driver_id = id
        driver = X3DHTML.CoordinateInterpolator(key=key, keyValue=keyValue,
                                                id=color_driver_id,
                                                DEF=color_driver_id,
                                                clockId=clockId,
                                                targetId=id+'-update')
        script = JHTML.Script(f"""(function() {{
const driver = document.getElementById("{id}");
const colorNode = document.getElementById("{targetId}");

function getInterpValue() {{
  const node = driver._x3domNode;
  if (node && node._vf && node._vf.value_changed) return node._vf.value_changed;
  return null;
}}

let lastStr = null;
function tick() {{
  requestAnimationFrame(tick);          // always re-arm
  const v = getInterpValue();
  if (!v || v.length === 0) return;

  // v is an array of x3dom SFVec3f objects (have .x/.y/.z) or arrays
  let str;
  if (typeof v[0] === "object" && "x" in v[0]) {{
    str = v.map(c => `${{c.x}} ${{c.y}} ${{c.z}}`).join(" ");
  }} else if (Array.isArray(v[0])) {{
    str = v.map(c => `${{c[0]}} ${{c[1]}} ${{c[2]}}`).join(" ");
  }} else {{
    str = v.join(" ");
  }}
  if (str === lastStr) return;
  colorNode.setAttribute("color", str);
  lastStr = str;
}}

requestAnimationFrame(tick)
// document.addEventListener("DOMContentLoaded", () => requestAnimationFrame(tick));
        }})()""", id=id+"-update")
        return [
            driver,
            script
        ]





    @classmethod
    def prep_interpolator(cls, interpolator_type, name, values, nframes, id, clock_id):
        """
        **LLM Docstring**

        Build the interpolator node (and its routing) for one animated property, keyed to
        the frames and wired to the target node.

        :param interpolator_type: the interpolator class
        :param name: the property name
        :param values: the per-frame values
        :param nframes: the number of frames
        :type nframes: int
        :param id: the target node id
        :param clock_id: the animation clock id
        :return: the interpolator nodes
        :rtype: list
        """
        target_id = id
        convert_values = True
        if interpolator_type == X3DHTML.ColorInterpolator:
            if isinstance(values[0], str) or values[0] is None:
                target_id = id + "-appearance-material"
                values = [
                    X3DOptionsSet.parse_color('black' if c is None else c)[0]
                    for c in values
                ]
            else:
                target_id = id + "-color"
                name = None
                interpolator_type = cls.get_color_array_interpolator
                values = [
                    [X3DOptionsSet.parse_color('black' if c is None else c)[0] for c in vl]
                    for vl in values
                ]
                convert_values = True
        elif interpolator_type == X3DHTML.CoordinateInterpolator:
            target_id = id + "-coord"
        if convert_values and nput.is_numeric_array_like(values):
            values = " ".join(np.round(values, 4).flatten().astype(str))
        key_frames = np.linspace(0, 1, nframes)

        iid = id + "-interpolator-" + cls.get_new_id()
        interp_obj = (
            interpolator_type(key=key_frames, keyValue=values,
                              id=iid,
                              DEF=iid,
                              clockId=f'animation-clock-{clock_id}',
                              targetId=target_id)
                if not hasattr(interpolator_type, 'id') else
            interpolator_type
        )
        return interp_obj, name, target_id

    @classmethod
    def create_animation_control(cls, name, *, id, uuid, type=None, values=None, interpolator_type=None):
        """
        **LLM Docstring**

        Build the animation control (a sequencer or interpolator, plus routing) for one
        property, choosing indexed vs interpolated animation.

        :param name: the property name
        :param id: the target node id
        :param uuid: the animation uuid
        :param type: the control type (inferred if omitted)
        :param values: the per-frame values
        :param interpolator_type: an explicit interpolator class
        :return: the control nodes
        :rtype: list
        """
        if values is None:
            if type is None:
                raise ValueError("`values` or `type` must be passed")
            return [
                X3DHTML.Route(
                    fromField='value_changed' if type == 'indexed' else 'fraction_changed',
                    fromNode=f'animation-indexer-{uuid}' if type == 'indexed' else f'animation-clock-{uuid}',
                    toField="set_"+name, toNode=id
                )
            ]
        else:
            if all(v is None for v in values): return [None]
            # if type is None:
            #     type = self.resolve_control_type(name, values)
            interpolator_type, nframes = cls.resolve_interpolator_type(name, values)
            interp_obj, name, target_id = cls.prep_interpolator(interpolator_type, name, values, nframes, id, uuid)
            if not isinstance(interp_obj, list):
                interp_obj = [interp_obj]
            if hasattr(interp_obj[0], 'id'):
                interp_id = interp_obj[0].id
            else:
                interp_id = interp_obj[0]['id']
            if not isinstance(interp_obj, list):
                interp_obj = [interp_obj]
            objs = interp_obj + [
                    X3DHTML.Route(
                        fromField='fraction_changed',
                        fromNode=f'animation-clock-{uuid}',
                        toField='set_fraction', toNode=interp_id
                    )]
            if name is not None:
                objs.append(X3DHTML.Route(
                    fromField='value_changed',
                    fromNode=interp_id,
                    toField='set_'+name, toNode=target_id
                ))
            return objs

class X3DListAnimator(X3DGenericAnimator):
    @classmethod
    def get_animation_objects(self, frames, id):
        """
        **LLM Docstring**

        Build a frame-switching animation: wrap the frames in an X3D `Switch` and animate
        its `whichChoice` by discrete index.

        :param frames: the per-frame objects
        :param id: the animator id
        :return: `(objects, attribute_sets, nframes)`
        :rtype: tuple
        """
        anim_frames = X3DSwitch(
                *frames,
                id=id+"-switch",
                DEF=id+"-switch",
                whichChoice="0"
            )
        nframes = len(anim_frames.children)
        attributes = [
            {
                'whichChoice':{'type':'indexed', 'id':id+"-switch"}
            }
        ]
        return [anim_frames], attributes, nframes

class X3DInterpolatingAnimator(X3DGenericAnimator):
    @classmethod
    def get_animation_objects(cls, object_attr_sets:dict[X3DObject, dict], id):
        """
        **LLM Docstring**

        Build an interpolating animation from a mapping of objects to their per-property
        frame values, validating a consistent frame count and resolving each property's
        target node.

        :param object_attr_sets: the `{object: {property: per_frame_values}}` mapping
        :type object_attr_sets: dict
        :param id: the animator id
        :return: `(objects, attribute_sets, nframes)`
        :rtype: tuple
        :raises ValueError: if the properties have mismatched frame counts
        """
        if isinstance(object_attr_sets, tuple) and len(object_attr_sets) == 1:
            object_attr_sets = object_attr_sets[0]
        objects = []
        att_set = []
        nframes = None
        for i,(obj,attrs) in enumerate(object_attr_sets.items()):
            objects.append(obj)
            at_list = {}
            for a,v in attrs.items():
                if nframes is None:
                    nframes = len(v)
                else:
                    nf = len(v)
                    if nframes != nf:
                        raise ValueError(f"attribute {a} has different number of frames {nf} than other attributes {nframes}")
                prop = obj.resolve_prop_attr(a)
                node = obj.get_prop_node_id(a)
                at_list[prop] = {
                    'id':node,
                    'values':obj.prep_animation_values(a, v)
                }
            att_set.append(at_list)

        return objects, att_set, nframes

    @classmethod
    def frame_diffs(cls, ref:X3DObject|X3DHTML.X3DElement, test:X3DObject|X3DHTML.X3DElement, *rest:X3DObject|X3DHTML.X3DElement):
        """
        **LLM Docstring**

        Walk several X3D object trees in parallel and find which nodes/attributes differ
        across frames, separating the static nodes from the per-node attribute changes.

        :param ref: the reference (first-frame) tree
        :param test: the second-frame tree
        :param rest: the remaining frames' trees
        :return: `(static_nodes, {node: per_frame_attribute_values})`
        :rtype: tuple
        :raises ValueError: if the trees have mismatched structure
        """
        statics = []
        changes = {}
        queue = collections.deque([(ref, test) + rest])
        # avoid bugs
        del ref
        del test
        while queue:
            trees = queue.pop()
            left = trees[0]
            rights = trees[1:]
            if isinstance(left, X3DObject):
                left_kids = left.get_children()
                right_kids = [right.get_children() for right in rights]
            else:
                left_kids = left.elems
                right_kids = [right.elems for right in rights]

            l = len(left_kids)
            for right,rk in zip(rights, right_kids):
                if l != len(rk):
                    raise ValueError(f"tree nodes have different numbers of children {l} vs {len(rk)} for  {left} and {right}")

            if l > 0:
                all_kids = [left_kids] + right_kids
                queue.extend(zip(*all_kids))

            if isinstance(left, X3DObject):
                left_attrs = left.get_interpolated_attributes()
                right_attrs = [right.get_interpolated_attributes() for right in rights]
            else:
                left_attrs = left.attrs
                right_attrs = [right.attrs for right in rights]

            attr_diffs = {}
            all_keys = {
                k
                for a in [left_attrs] + right_attrs
                for k in a.keys()
            } - {'id', 'def', 'DEF'}
            for k in all_keys:
                v = left_attrs.get(k)
                vals = [v]
                diffed = False
                for a in right_attrs:
                    v2 = a.get(k)
                    vals.append(v2)
                    if not diffed:
                        diffed = (
                                v is None and v2 is not None
                                or v2 is None and v is None
                        )
                        if not diffed:
                            if nput.is_numeric_array_like(v):
                                if not nput.is_numeric_array_like(v2):
                                    diffed = True
                                else:
                                    diffed = not np.allclose(v, v2)
                            elif nput.is_numeric_array_like(2):
                                diffed = True
                            else:
                                diffed = v2 != v
                if diffed:
                    attr_diffs[k] = vals
            if len(attr_diffs) > 0:
                changes[left] = attr_diffs
            elif l == 0:
                statics.append(left)
        return statics, changes

    @classmethod
    def from_frames(cls, frames:list[X3DObject|X3DHTML.X3DElement], **opts):
        """
        **LLM Docstring**

        Build an interpolating animation from a list of frame trees by diffing them:
        static content is kept as-is and only the changing attributes are animated.

        :param frames: the per-frame object trees
        :type frames: list
        :param opts: options for the animator
        :return: the animation (or the single frame if nothing changes)
        """
        static_objects, interpolated_objects = cls.frame_diffs(*frames)
        if len(interpolated_objects) == 0:
            return frames[0]
        else:
            anim = X3DInterpolatingAnimator(interpolated_objects, **opts)
            if len(static_objects) > 0:
                anim = X3DGroup(static_objects + [anim])
            return anim

