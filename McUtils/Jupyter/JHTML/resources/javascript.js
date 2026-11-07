/* Portable McUtils state and binding adapters; no widget or notebook dependency. */
(() => {
  'use strict';
  if (globalThis.McUtilsJS) return;
  const entryURL = document.currentScript?.src || null;
  const documentReady = document.readyState === 'loading' ? new Promise(resolve =>
    document.addEventListener('DOMContentLoaded', resolve, {once:true})) : Promise.resolve();
  const scopes = new WeakMap();
  const adapters = new Map();
  const clone = value => JSON.parse(JSON.stringify(value));
  const equal = (a, b) => {
    if (a === b) return true;
    if (!a || !b || typeof a !== 'object' || typeof b !== 'object' || Array.isArray(a) !== Array.isArray(b)) return false;
    const keys = Object.keys(a);
    return keys.length === Object.keys(b).length && keys.every(key => Object.hasOwn(b, key) && equal(a[key], b[key]));
  };
  function portable(value) {
    if (value === null || typeof value === 'string' || typeof value === 'boolean') return;
    if (typeof value === 'number' && Number.isFinite(value)) return;
    if (Array.isArray(value)) { value.forEach(portable); return; }
    if (value && Object.getPrototypeOf(value) === Object.prototype) { Object.values(value).forEach(portable); return; }
    throw new TypeError('JavaScript state requires finite JSON values');
  }
  function validate(value, schema) {
    portable(value);
    if (value === null) {
      if (!schema.nullable) throw new TypeError('Variable does not accept null');
      return;
    }
    const kinds = {any: true, number: typeof value === 'number', integer: Number.isInteger(value),
      string: typeof value === 'string', boolean: typeof value === 'boolean',
      array: Array.isArray(value), object: typeof value === 'object' && !Array.isArray(value)};
    if (!kinds[schema.kind]) throw new TypeError('Variable requires ' + schema.kind);
    if (schema.choices && !schema.choices.some(choice => equal(choice, value))) throw new RangeError('Value is outside its choices');
    for (const bound of ['min', 'max']) if (Object.hasOwn(schema, bound)) {
      if (typeof value !== 'number' || (bound === 'min' ? value < schema[bound] : value > schema[bound])) throw new RangeError('Value is outside its bounds');
    }
  }
  function mount(root) {
    if (scopes.has(root)) return scopes.get(root);
    const config = JSON.parse(root.getAttribute('data-mcjs-state'));
    if (config.version !== 1) throw new Error('Unsupported McUtils JavaScript manifest version');
    const values = new Map(), schemas = new Map(), listeners = new Set(), cleanups = [];
    const bound = new Map();
    let disposed = false, queued = false;
    const changes = new Map();
    function check() { if (disposed) throw new Error('JavaScript state is disposed'); }
    for (const variable of config.variables) {
      if (values.has(variable.name)) throw new Error('Duplicate JavaScript variable: ' + variable.name);
      validate(variable.initial, variable.schema);
      schemas.set(variable.name, variable.schema);
      values.set(variable.name, clone(variable.initial));
    }
    const state = {
      root,
      get(name) { check(); if (!values.has(name)) throw new Error('Unknown variable: ' + name); return clone(values.get(name)); },
      snapshot() { check(); return Object.fromEntries([...values].map(([name, value]) => [name, clone(value)])); },
      set(name, value, origin = null) { return state.patch({[name]: value}, origin); },
      patch(patch, origin = null) {
        check();
        for (const [name, value] of Object.entries(patch)) {
          if (!schemas.has(name)) throw new Error('Unknown variable: ' + name);
          validate(value, schemas.get(name));
        }
        for (const [name, value] of Object.entries(patch)) {
          if (equal(values.get(name), value)) continue;
          values.set(name, clone(value));
          changes.set(name, {name, value: clone(value), origin});
        }
        if (changes.size && !queued) {
          queued = true;
          queueMicrotask(() => {
            queued = false;
            if (disposed) return;
            const batch = [...changes.values()]; changes.clear();
            for (const listener of [...listeners]) listener(batch);
            root.dispatchEvent(new CustomEvent('mcjs:change', {detail: {changes: batch}, bubbles: true}));
          });
        }
        return state;
      },
      subscribe(listener) { check(); listeners.add(listener); return () => listeners.delete(listener); },
      onDispose(callback) { if (disposed) callback(); else cleanups.push(callback); },
      get disposed() { return disposed; },
      dispose() {
        if (disposed) return;
        disposed = true;
        observer.disconnect();
        for (const entry of bound.values()) entry.dispose();
        bound.clear(); listeners.clear(); changes.clear();
        for (const cleanup of cleanups.splice(0).reverse()) {
          try { cleanup(); } catch (error) { console.error(error); }
        }
        scopes.delete(root);
        root.controller = null;
        root.setAttribute('data-mcjs-status', 'disposed');
      }
    };
    scopes.set(root, state);
    root.controller = state;
    function on(target, event, handler, options) {
      target.addEventListener(event, handler, options);
      const remove = () => target.removeEventListener(event, handler, options);
      state.onDispose(remove);
      return remove;
    }
    function attach(element) {
      if (bound.has(element)) return;
      const manifest = JSON.parse(element.getAttribute('data-mcjs-bind'));
      const factory = adapters.get(manifest.adapter);
      if (!factory) throw new Error('Unknown binding adapter: ' + manifest.adapter);
      const removers = [], inputs = new Map();
      const context = {
        element, options: manifest.options,
        get: prop => state.get(manifest.bindings[prop].variable),
        publish(prop, value) {
          const binding = manifest.bindings[prop];
          if (binding && binding.direction !== 'in') state.set(binding.variable, value, element);
        },
        listen(target, event, listener, options) {
          target.addEventListener(event, listener, options);
          removers.push(() => target.removeEventListener(event, listener, options));
        },
        cleanup: callback => removers.push(callback),
        input(prop, setter, {echo = true} = {}) {
          const binding = manifest.bindings[prop];
          if (!binding) return;
          if (!values.has(binding.variable)) throw new Error('Unresolved variable: ' + binding.variable);
          if (binding.direction !== 'out') inputs.set(prop, {setter, echo});
        },
        fail(error) {
          element.setAttribute('data-mcjs-status', 'error');
          element.error = error;
          element.dispatchEvent(new CustomEvent('mcjs:error', {detail: error, bubbles: true}));
        }
      };
      try {
        factory(context);
        const apply = batch => {
          for (const [prop, {setter, echo}] of inputs) {
            const binding = manifest.bindings[prop];
            if (!batch || batch.some(change => change.name === binding.variable && (echo || change.origin !== element))) setter(state.get(binding.variable));
          }
        };
        removers.push(state.subscribe(batch => { try { apply(batch); } catch (error) { context.fail(error); } }));
        apply();
        bound.set(element, {dispose() { for (const remove of removers.splice(0).reverse()) remove(); }});
      } catch (error) {
        for (const remove of removers.reverse()) remove();
        context.fail(error);
        throw error;
      }
    }
    function refresh() {
      if (disposed) return;
      for (const [element, entry] of bound) if (!root.contains(element)) { entry.dispose(); bound.delete(element); }
      const elements = root.matches('[data-mcjs-bind]') ? [root] : [];
      elements.push(...root.querySelectorAll('[data-mcjs-bind]'));
      for (const element of elements) if (element.closest('[data-mcjs-state]') === root) attach(element);
    }
    const observer = new MutationObserver(() => {
      if (!root.isConnected) state.dispose(); else refresh();
    });
    observer.observe(root.ownerDocument.documentElement, {childList: true, subtree: true});
    try {
      if (config.script) new Function('state', 'root', 'on', 'onDispose', config.script)(state, root, on, state.onDispose);
      refresh();
      root.setAttribute('data-mcjs-status', 'ready');
      root.dispatchEvent(new CustomEvent('mcjs:ready', {detail: state, bubbles: true}));
    } catch (error) {
      state.dispose();
      root.setAttribute('data-mcjs-status', 'error');
      root.error = error;
      throw error;
    }
    return state;
  }
  function common(ctx) {
    ctx.input('visible', value => { ctx.element.hidden = !value; });
  }
  adapters.set('dom', ctx => {
    const el = ctx.element;
    common(ctx);
    const optionValue = option => option.hasAttribute('data-mcjs-value') ? JSON.parse(option.getAttribute('data-mcjs-value')) : option.value;
    ctx.input('value', value => {
      if (el.tagName === 'SELECT') {
        for (const option of el.options) option.selected = el.multiple ? (value || []).some(item => equal(item, optionValue(option))) : equal(value, optionValue(option));
      } else el.value = value == null ? '' : String(value);
    });
    ctx.input('checked', value => { el.checked = Boolean(value); });
    ctx.input('text', value => { el.textContent = value == null ? '' : String(value); });
    ctx.input('enabled', value => { el.disabled = !value; });
    const read = () => {
      let value = ['number', 'range'].includes(el.type) ? (el.value === '' ? null : Number(el.value)) : el.value;
      if (el.tagName === 'SELECT') {
        const selected = [...el.selectedOptions].map(optionValue);
        value = el.multiple ? selected : selected[0] ?? null;
      }
      ctx.publish('value', value);
      ctx.publish('checked', Boolean(el.checked));
    };
    ctx.listen(el, 'input', read);
    ctx.listen(el, 'change', read);
  });
  adapters.set('table', ctx => {
    common(ctx);
    const rows = () => [...ctx.element.querySelectorAll('[data-mcjs-key]')];
    ctx.input('selection', value => {
      for (const row of rows()) {
        const selected = equal(JSON.parse(row.getAttribute('data-mcjs-key')), value);
        row.setAttribute('aria-selected', String(selected));
        row.classList.toggle('mcjs-selected', selected);
      }
    });
    const select = event => {
      if (event.type === 'keydown' && !['Enter', ' '].includes(event.key)) return;
      const row = event.target.closest('[data-mcjs-key]');
      if (!row || !ctx.element.contains(row)) return;
      if (event.type === 'keydown') event.preventDefault();
      ctx.publish('selection', JSON.parse(row.getAttribute('data-mcjs-key')));
    };
    ctx.listen(ctx.element, 'click', select);
    ctx.listen(ctx.element, 'keydown', select);
  });
  adapters.set('plotly', ctx => {
    common(ctx);
    const el = ctx.element;
    let active = true, ready = false, dirty = false, rendering = false;
    let data = clone(ctx.options.figure.data || []), layout = clone(ctx.options.figure.layout || {});
    let selection;
    layout.uirevision ??= 'mcutils';
    const keyOf = (trace, point) => (trace.customdata || [])[point];
    function paintSelection() {
      if (selection === undefined) return;
      for (const trace of data) {
        if (!Array.isArray(trace.customdata)) continue;
        trace.selectedpoints = selection === null ? null : trace.customdata.flatMap((key, index) => equal(key, selection) ? [index] : []);
      }
    }
    function schedule() {
      dirty = true;
      if (!ready || rendering || !active) return;
      rendering = true;
      requestAnimationFrame(async () => {
        try {
          if (!active) return;
          dirty = false; paintSelection();
          await globalThis.Plotly.react(el, clone(data), clone(layout), ctx.options.config || {responsive: true});
          if (!active) globalThis.Plotly.purge(el);
        } catch (error) { ctx.fail(error); }
        finally { rendering = false; if (dirty && active) schedule(); }
      });
    }
    ctx.input('selection', value => { selection = value; schedule(); });
    ctx.input('data', value => { data = clone(value); schedule(); });
    ctx.input('layout', value => { layout = {...clone(value), uirevision: value.uirevision ?? 'mcutils'}; schedule(); });
    ctx.cleanup(() => { active = false; if (ready) globalThis.Plotly.purge(el); });
    const mathjax = ctx.options.mathjax ? api.loadScript(ctx.options.mathjax, 'mathjax', () => Boolean(globalThis.MathJax?.startup))
      .then(() => globalThis.MathJax.startup.promise) : Promise.resolve();
    Promise.all([api.loadScript(ctx.options.script, 'plotly', () => Boolean(globalThis.Plotly)), mathjax])
      .then(async () => {
        if (!active) return;
        paintSelection();
        await globalThis.Plotly.newPlot(el, clone(data), clone(layout), ctx.options.config || {responsive: true});
        if (!active) { globalThis.Plotly.purge(el); return; }
        ready = true;
        const click = event => {
          const point = event.points?.[0];
          if (!point) return;
          const key = point.customdata ?? keyOf(data[point.curveNumber] || {}, point.pointNumber);
          if (key !== undefined) ctx.publish('selection', key);
        };
        el.on('plotly_click', click);
        ctx.cleanup(() => el.removeListener('plotly_click', click));
        if (dirty) schedule();
      }).catch(ctx.fail);
  });
  adapters.set('x3d', ctx => {
    common(ctx);
    const el = ctx.element, pending = new Map();
    let controller = null, active = true, timer = null;
    const setters = {mode: 'selectMode', sample: 'selectSample', fraction: 'seek', running: 'setRunning', speed: 'setSpeed', loop: 'setLoop', scale: 'setScale'};
    function apply(prop, value) {
      if (!controller) { pending.set(prop, value); return; }
      const method = setters[prop];
      if (typeof controller[method] !== 'function') throw new Error('X3D controller does not support ' + prop);
      controller[method](value);
    }
    for (const prop of Object.keys(setters)) ctx.input(prop, value => apply(prop, value), {echo:false});
    function find() {
      if (!active) return;
      const candidates = [el, ...el.querySelectorAll('.mcutils-x3d-component')];
      const candidate = ctx.options.controllerId ? candidates.find(node => node.id === ctx.options.controllerId) :
        candidates.find(node => node.controller && (node.controller.selectMode || node.controller.selectSample || node.controller.seek));
      if (!candidate?.controller) {
        if (performance.now() - started > (ctx.options.timeout || 10000)) { ctx.fail(new Error('Timed out waiting for X3D controller')); return; }
        timer = setTimeout(find, 25); return;
      }
      controller = candidate.controller;
      try { for (const [prop, value] of pending) apply(prop, value); pending.clear(); }
      catch (error) { ctx.fail(error); return; }
      const publish = snapshot => {
        if (snapshot.modeIndex !== undefined) ctx.publish('mode', snapshot.modeIndex);
        if (snapshot.sample !== undefined) ctx.publish('sample', snapshot.sample);
        for (const prop of ['fraction', 'running', 'speed', 'loop', 'scale']) if (snapshot[prop] !== undefined) ctx.publish(prop, snapshot[prop]);
      };
      ctx.listen(candidate, 'scanchange', event => publish(event.detail));
      if (typeof controller.onChange === 'function') ctx.cleanup(controller.onChange(publish));
    }
    const started = performance.now();
    timer = setTimeout(find, 0);
    ctx.cleanup(() => { active = false; clearTimeout(timer); });
  });
  const scripts = new Map();
  const stylesheets = new Map();
  const api = {
    version: 1,
    webComponents: true,
    mount,
    state: root => scopes.get(root),
    registerAdapter(name, factory) {
      if (typeof name !== 'string' || !name || typeof factory !== 'function') throw new TypeError('An adapter requires a name and factory');
      adapters.set(name, factory);
    },
    loadStylesheet(url, id) {
      const existing = id && document.getElementById(id);
      if (existing?.tagName === 'STYLE' || existing?.sheet) return Promise.resolve();
      if (stylesheets.has(url)) return stylesheets.get(url);
      const promise = new Promise((resolve,reject) => {
        const link = existing || document.createElement('link');
        link.rel='stylesheet';link.href=url;if(id)link.id=id;
        link.addEventListener('load',resolve,{once:true});
        link.addEventListener('error',()=>reject(new Error('Failed to load stylesheet: '+url)),{once:true});
        if(!existing)document.head.append(link);
      });
      stylesheets.set(url,promise);promise.catch(()=>stylesheets.delete(url));
      return promise;
    },
    ensureNativeStyles(root) {
      const native = element => element.localName?.startsWith('mcui-') && !['mcui-state','mcui-bootstrap'].includes(element.localName);
      if (!entryURL || (!native(root) && ![...root.querySelectorAll('*')].some(native))) return Promise.resolve();
      return api.loadStylesheet(new URL('../../Apps/resources/native.css',entryURL).href,'mcutils-apps-native-css');
    },
    ensureBootstrap(root) {
      if(root.getAttribute('data-mcui-bootstrap-load')==='false')return Promise.resolve();
      const css=root.getAttribute('data-mcui-bootstrap-css');
      const script=root.getAttribute('data-mcui-bootstrap-js');
      if(!globalThis.bootstrap && !script)return Promise.reject(new Error('Bootstrap script must be supplied explicitly'));
      return Promise.all([
        css ? api.loadStylesheet(css,'mcutils-bootstrap-css') : Promise.resolve(),
        api.loadScript(script,'bootstrap',()=>Boolean(globalThis.bootstrap))
      ]);
    },
    loadScript(url, name, present) {
      if (present()) return Promise.resolve();
      if (!url) return Promise.reject(new Error('Missing runtime URL for ' + name));
      if (scripts.has(url)) return scripts.get(url);
      const promise = new Promise((resolve, reject) => {
        const absolute = new URL(url,document.baseURI).href;
        const existing = [...document.scripts].find(script=>script.src === absolute);
        const script = existing || document.createElement('script');
        script.src = url;
        script.addEventListener('load',() => present() ? resolve() : reject(new Error('Runtime did not initialize: ' + name)),{once:true});
        script.addEventListener('error',() => reject(new Error('Failed to load runtime: ' + name)),{once:true});
        if(!existing) document.head.append(script);
      });
      scripts.set(url, promise);
      promise.catch(() => scripts.delete(url));
      return promise;
    }
  };
  globalThis.McUtilsJS = api;
  // The CDN entry point reuses the existing Apps WebComponents and stylesheet
  // from the same pinned repository revision. Inline exports assemble those
  // sources locally, so no nested request is made by an offline document.
  api.ready = entryURL && !globalThis.McUtilsApps ?
    api.loadScript(new URL('../../Apps/resources/native.js',entryURL).href,'mcutils-ui',()=>Boolean(globalThis.McUtilsApps))
      .then(()=>api.ensureNativeStyles(document.body || document.documentElement)) : Promise.resolve();
  api.ready.catch(error=>console.error('McUtils UI runtime failed:',error));

  class McuiState extends HTMLElement {
    constructor() { super();this._generation=0;this._newReady(); }
    _newReady() {
      this.ready=new Promise((resolve,reject)=>{this._resolveReady=resolve;this._rejectReady=reject;});
      this.ready.catch(()=>{});
    }
    connectedCallback() {
      const generation=++this._generation;
      Promise.all([documentReady,api.ready]).then(()=>api.ensureNativeStyles(this))
        .then(()=>this.closest('mcui-bootstrap')?.ready)
        .then(()=>{
          if(generation!==this._generation || !this.isConnected)return;
          this._resolveReady(mount(this));
        }).catch(error=>{
          if(generation!==this._generation)return;
          this.error=error;this.setAttribute('data-mcjs-status','error');this._rejectReady(error);
          this.dispatchEvent(new CustomEvent('mcjs:error',{detail:error,bubbles:true}));
        });
    }
    disconnectedCallback() {
      const generation=++this._generation;
      queueMicrotask(()=>{
        if(generation!==this._generation || this.isConnected)return;
        scopes.get(this)?.dispose();this._resolveReady(null);this._newReady();
      });
    }
  }

  class McuiBootstrap extends HTMLElement {
    connectedCallback() {
      if(this._active)return;
      const generation=this._generation=(this._generation || 0)+1;
      this._active=true;this._instances ||= new Map();
      this.ready=Promise.all([documentReady,api.ready]).then(()=>api.ensureBootstrap(this)).then(()=>{
        if(!this._active || generation!==this._generation)return;
        this.refresh();
        this._observer=new MutationObserver(()=>this.refresh());
        this._observer.observe(this,{childList:true,subtree:true});
      });
      this.ready.catch(error=>{this.error=error;this.dispatchEvent(new CustomEvent('mcjs:error',{detail:error,bubbles:true}));});
    }
    refresh() {
      for(const [element,instance] of this._instances) if(!this.contains(element)) {
        instance.dispose();this._instances.delete(element);
      }
      for(const element of this.querySelectorAll('[data-bs-toggle="tooltip"],[data-bs-toggle="popover"]')) {
        // Notebook handlers own rich widget content and its plugin lifetime.
        if(element.closest('mcui-bootstrap')!==this || element.hasAttribute('data-mcui-widget-plugin'))continue;
        const type=element.getAttribute('data-bs-toggle')==='tooltip'?'Tooltip':'Popover';
        if(globalThis.bootstrap?.[type])this._instances.set(element,bootstrap[type].getOrCreateInstance(element));
      }
    }
    disconnectedCallback() {
      queueMicrotask(()=>{
        if(this.isConnected)return;
        this._active=false;this._generation++;this._observer?.disconnect();
        for(const instance of this._instances?.values() || [])instance.dispose();
        this._instances?.clear();
      });
    }
  }
  if(!customElements.get('mcui-state'))customElements.define('mcui-state',McuiState);
  if(!customElements.get('mcui-bootstrap'))customElements.define('mcui-bootstrap',McuiBootstrap);
})();
