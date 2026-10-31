/* McUtils native Web Components. Light DOM belongs to the widget manager. */
(() => {
  'use strict';
  if (customElements.get('mcui-root')) return;

  const views = new WeakMap();
  const query = (root, selector) => {
    try { return selector ? root.querySelector(selector) : null; }
    catch { return null; }
  };
  const controlFrom = (event, selector) => event.target.closest?.(selector);
  const signal = (element, kind, detail) => element.dispatchEvent(new CustomEvent(
    `mcui:${kind}`, {detail, bubbles: true, composed: true}
  ));

  class McuiElement extends HTMLElement {
    static watchChildren = false;

    connectedCallback() {
      if (this._events) return;
      this._events = new AbortController();
      this.connect();
      if (this.constructor.watchChildren) {
        this._observer = new MutationObserver(() => this.requestUpdate());
        this._observer.observe(this, {childList: true, subtree: true});
      }
      // Parsing and widget child views can finish after connectedCallback.
      this.requestUpdate();
    }

    disconnectedCallback() {
      this._events?.abort();
      this._events = null;
      this._observer?.disconnect();
      this._observer = null;
      this.disconnect();
    }

    attributeChangedCallback(name, oldValue, value) {
      if (oldValue !== value && this.isConnected) this.refresh();
    }

    connect() {}
    disconnect() {}
    update() {}

    listen(type, handler, target = this, options = {}) {
      target.addEventListener(type, handler, {...options, signal: this._events.signal});
    }

    requestUpdate() {
      if (this._pending) return;
      this._pending = true;
      queueMicrotask(() => {
        this._pending = false;
        if (this.isConnected) this.refresh();
      });
    }

    refresh() {
      if (this._updating) return;
      this._updating = true;
      try { this.update(); }
      finally { this._updating = false; }
    }

    target(control) {
      const selector = control?.getAttribute('data-mcui-target') || control?.getAttribute('href');
      return query(this, selector) || query(this.getRootNode(), selector);
    }
  }

  // Layout children stay in place: no cloning, reparenting or innerHTML render.
  class McuiRoot extends McuiElement {}
  class McuiGrid extends McuiElement {}
  class McuiFlex extends McuiElement {}
  class McuiPanel extends McuiElement {}
  class McuiPanelHeader extends McuiElement {}
  class McuiPanelBody extends McuiElement {}
  class McuiPanelFooter extends McuiElement {}

  class McuiCollapse extends McuiElement {
    static observedAttributes = ['open'];
    get open() { return this.hasAttribute('open'); }
    set open(value) { this.toggleAttribute('open', Boolean(value)); }
    show() { this.open = true; }
    hide() { this.open = false; }
    toggle() { this.open = !this.open; }

    update() {
      if (!this._initialized) {
        this._initialized = true;
        if (this.classList.contains('mcui-show')) this.open = true;
      }
      const previous = this._openState;
      this._openState = this.open;
      this.classList.toggle('mcui-show', this.open);
      this.setAttribute('aria-hidden', String(!this.open));
      if (previous !== undefined && previous !== this.open) {
        signal(this, 'change', {open: this.open});
      }
    }
  }

  class McuiAccordion extends McuiElement {
    static watchChildren = true;
    static observedAttributes = ['value', 'multiple'];
    get controls() {
      return [...this.querySelectorAll('[data-mcui-toggle="collapse"]')]
        .filter(el => el.closest('mcui-accordion,mcui-opener') === this);
    }
    get panels() { return this.controls.map(el => this.target(el)).filter(Boolean); }
    get value() { return this.panels.find(el => el.open)?.id ?? null; }
    set value(value) {
      if (value == null) this.removeAttribute('value');
      else this.setAttribute('value', value);
      for (const panel of this.panels) panel.open = panel.id === value;
      this.refresh();
    }
    get multiple() { return this.localName === 'mcui-opener' || this.hasAttribute('multiple'); }
    set multiple(value) { this.toggleAttribute('multiple', Boolean(value)); }

    connect() {
      this.listen('click', event => {
        const control = controlFrom(event, '[data-mcui-toggle="collapse"]');
        if (!this.controls.includes(control)) return;
        const panel = this.target(control);
        if (!panel) return;
        event.preventDefault();
        panel.toggle();
      });
      this.listen('mcui:change', event => {
        const panel = event.target;
        if (!this.panels.includes(panel)) return;
        if (panel.open && !this.multiple) {
          for (const other of this.panels) if (other !== panel) other.hide();
          this.setAttribute('value', panel.id);
        } else if (!panel.open && this.getAttribute('value') === panel.id) {
          this.removeAttribute('value');
        }
        this.syncControls();
      });
    }

    syncControls() {
      for (const control of this.controls) {
        const panel = this.target(control);
        if (!panel) continue;
        control.setAttribute('aria-expanded', String(panel.open));
        control.setAttribute('aria-controls', panel.id);
        control.classList.toggle('mcui-collapsed', !panel.open);
      }
    }

    update() {
      const specified = this.getAttribute('value');
      let active = false;
      for (const panel of this.panels) {
        panel.refresh();
        if (specified !== null) panel.open = panel.id === specified;
        if (panel.open && !this.multiple) {
          if (active) panel.hide();
          active = true;
        }
      }
      this.syncControls();
    }
  }
  class McuiOpener extends McuiAccordion {}

  function tabsOwner(control) {
    const list = control.closest('mcui-tab-list');
    return list?.parentElement?.closest('mcui-tabs') || list || control.closest('mcui-tabs');
  }

  class McuiTabs extends McuiElement {
    static watchChildren = true;
    static observedAttributes = ['value'];
    get controls() {
      return [...this.querySelectorAll('[data-mcui-toggle="tab"]')]
        .filter(el => tabsOwner(el) === this);
    }
    get value() { return this.getAttribute('value'); }
    set value(value) {
      if (value == null) this.removeAttribute('value');
      else this.setAttribute('value', value);
    }

    connect() {
      this.listen('click', event => {
        const control = controlFrom(event, '[data-mcui-toggle="tab"]');
        if (!this.controls.includes(control)) return;
        event.preventDefault();
        this.value = this.target(control)?.id;
      });
      this.listen('keydown', event => {
        const control = controlFrom(event, '[data-mcui-toggle="tab"]');
        const controls = this.controls;
        if (!controls.includes(control)) return;
        const vertical = control.closest('[role="tablist"]')?.getAttribute('aria-orientation') === 'vertical';
        const previous = vertical ? 'ArrowUp' : 'ArrowLeft';
        const next = vertical ? 'ArrowDown' : 'ArrowRight';
        if (![previous, next, 'Home', 'End'].includes(event.key)) return;
        let index = controls.indexOf(control);
        index = event.key === 'Home' ? 0 : event.key === 'End' ? controls.length - 1
          : (index + (event.key === previous ? -1 : 1) + controls.length) % controls.length;
        event.preventDefault();
        this.value = this.target(controls[index])?.id;
        controls[index].focus();
      });
    }

    update() {
      const controls = this.controls;
      if (!controls.length) return;
      const selected = controls.find(el => this.target(el)?.id === this.value)
        || controls.find(el => el.classList.contains('mcui-active')) || controls[0];
      const value = this.target(selected)?.id;
      if (!value) return;
      if (this.value !== value) this.value = value;
      for (const control of controls) {
        const pane = this.target(control), active = control === selected;
        control.closest('ul,.mcui-nav')?.setAttribute('role', 'tablist');
        control.setAttribute('role', 'tab');
        control.setAttribute('aria-selected', String(active));
        control.tabIndex = active ? 0 : -1;
        control.classList.toggle('mcui-active', active);
        if (pane) {
          control.setAttribute('aria-controls', pane.id);
          pane.setAttribute('role', 'tabpanel');
          pane.setAttribute('aria-hidden', String(!active));
          if (control.id) pane.setAttribute('aria-labelledby', control.id);
          pane.classList.toggle('mcui-active', active);
          pane.classList.toggle('mcui-show', active);
        }
      }
      const previous = this._selection;
      this._selection = value;
      if (previous !== undefined && previous !== value) signal(this, 'select', {value});
    }
  }
  class McuiTabList extends McuiTabs {}

  class McuiDropdown extends McuiElement {
    static watchChildren = true;
    static observedAttributes = ['open'];
    get open() { return this.hasAttribute('open'); }
    set open(value) { this.toggleAttribute('open', Boolean(value)); }
    get toggleButton() { return this.querySelector('[data-mcui-toggle="dropdown"]'); }
    get menu() { return this.querySelector('.mcui-dropdown-menu'); }
    get items() { return [...this.menu?.querySelectorAll('.mcui-dropdown-item:not([disabled])') || []]; }
    show() { this.open = true; }
    hide() { this.open = false; }
    toggle() { this.open = !this.open; }

    connect() {
      this.listen('click', event => {
        if (event.target.closest('mcui-dropdown') !== this) return;
        if (controlFrom(event, '[data-mcui-toggle="dropdown"]')) {
          event.preventDefault(); this.toggle();
        } else if (controlFrom(event, '.mcui-dropdown-item')) this.hide();
      });
      this.listen('keydown', event => {
        if (event.target.closest('mcui-dropdown') !== this) return;
        if (event.key === 'Escape') {
          this.hide(); this.toggleButton?.focus(); return;
        }
        if (!['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) return;
        if (!this.open) this.show();
        const items = this.items;
        if (!items.length) return;
        let index = items.indexOf(this.ownerDocument.activeElement);
        index = event.key === 'Home' ? 0 : event.key === 'End' ? items.length - 1
          : index < 0 ? (event.key === 'ArrowUp' ? items.length - 1 : 0)
          : (index + (event.key === 'ArrowUp' ? -1 : 1) + items.length) % items.length;
        event.preventDefault(); items[index].focus();
      });
    }

    disconnect() { this._outside?.abort(); this._outside = null; }

    update() {
      this.toggleButton?.setAttribute('aria-haspopup', 'menu');
      this.toggleButton?.setAttribute('aria-expanded', String(this.open));
      this.menu?.setAttribute('role', 'menu');
      this.menu?.classList.toggle('mcui-show', this.open);
      for (const item of this.items) { item.setAttribute('role', 'menuitem'); item.tabIndex = -1; }
      if (this.open && !this._outside) {
        this._outside = new AbortController();
        this.ownerDocument.addEventListener('click', event => {
          if (!this.contains(event.target)) this.hide();
        }, {signal: this._outside.signal});
      } else if (!this.open) this.disconnect();
      if (this._openState !== undefined && this._openState !== this.open) signal(this, 'change', {open: this.open});
      this._openState = this.open;
    }
  }

  class McuiCarousel extends McuiElement {
    static watchChildren = true;
    static observedAttributes = ['index', 'interval', 'paused'];
    get frames() {
      return [...this.querySelectorAll('.mcui-carousel-item')]
        .filter(el => el.closest('mcui-carousel') === this);
    }
    get index() { return Number(this.getAttribute('index') || 0); }
    set index(value) { this.setAttribute('index', String(value)); }
    get paused() { return this.hasAttribute('paused'); }
    set paused(value) { this.toggleAttribute('paused', Boolean(value)); }
    next() { this.index = this.index + 1; }
    previous() { this.index = this.index - 1; }
    pause() { this.paused = true; }
    play() { this.paused = false; }

    connect() {
      this.listen('click', event => {
        const control = controlFrom(event, '[data-mcui-slide],[data-mcui-slide-to]');
        if (!control || control.closest('mcui-carousel') !== this) return;
        event.preventDefault();
        if (control.hasAttribute('data-mcui-slide-to')) this.index = Number(control.getAttribute('data-mcui-slide-to'));
        else if (control.getAttribute('data-mcui-slide') === 'prev') this.previous();
        else this.next();
      });
    }

    disconnect() { clearTimeout(this._timer); this._timer = null; }

    update() {
      this.disconnect();
      const frames = this.frames;
      if (!frames.length) return;
      let index = this.hasAttribute('index') ? this.index : frames.findIndex(el => el.classList.contains('mcui-active'));
      index = Number.isFinite(index) ? ((Math.trunc(index) % frames.length) + frames.length) % frames.length : 0;
      if (this.index !== index || !this.hasAttribute('index')) this.index = index;
      frames.forEach((el, i) => {el.classList.toggle('mcui-active', i === index); el.setAttribute('aria-hidden', String(i !== index));});
      for (const control of this.querySelectorAll('[data-mcui-slide-to]')) {
        control.classList.toggle('mcui-active', Number(control.getAttribute('data-mcui-slide-to')) === index);
      }
      const previous = this._selection;
      this._selection = index;
      if (previous !== undefined && previous !== index) signal(this, 'select', {index});
      const interval = Number(this.getAttribute('interval') || frames[index].getAttribute('data-mcui-interval')
        || this.getAttribute('data-mcui-interval') || 5000);
      if (!this.paused && this.getAttribute('data-mcui-ride') === 'carousel'
          && interval > 0 && interval <= 2147483647 && frames.length > 1) {
        this._timer = setTimeout(() => { if (this.isConnected) this.next(); }, interval);
      }
    }
  }

  class McuiPopup extends McuiElement {
    static observedAttributes = ['open', 'title', 'data-mcui-title', 'data-mcui-content',
      'data-mcui-placement', 'data-mcui-trigger', 'data-mcui-html'];
    get open() { return this.hasAttribute('open'); }
    set open(value) { this.toggleAttribute('open', Boolean(value)); }
    get kind() { return this.localName === 'mcui-tooltip' ? 'tooltip' : 'popover'; }
    get triggers() { return this.getAttribute('data-mcui-trigger') || (this.kind === 'tooltip' ? 'hover focus' : 'click'); }
    show() { this.open = true; }
    hide() { this.open = false; }
    toggle() { this.open = !this.open; }

    connect() {
      this.listen('click', event => {
        if (event.target.closest('mcui-tooltip,mcui-popover') === this && this.triggers.includes('click')) this.toggle();
      });
      for (const [start, end, trigger] of [['pointerover', 'pointerout', 'hover'], ['focusin', 'focusout', 'focus']]) {
        this.listen(start, () => { if (this.triggers.includes(trigger)) this.show(); });
        this.listen(end, event => {
          if (this.triggers.includes(trigger) && !this.contains(event.relatedTarget) && !this._popup?.contains(event.relatedTarget)) this.hide();
        });
      }
      this.listen('keydown', event => { if (event.key === 'Escape') this.hide(); });
    }

    disconnect() { this.clearPopup(); }

    clearPopup() {
      this._generation = (this._generation || 0) + 1;
      for (const view of this._children || []) view.remove();
      this._children = [];
      this._outside?.abort(); this._outside = null;
      this._popup?.remove(); this._popup = null;
      if (this._description) {
        const target = this._descriptionTarget;
        const tokens = (target.getAttribute('aria-describedby') || '').split(/\s+/).filter(id => id && id !== this._description);
        if (tokens.length) target.setAttribute('aria-describedby', tokens.join(' '));
        else target.removeAttribute('aria-describedby');
        this._description = null;
        this._descriptionTarget = null;
      }
    }

    async fillContent(parent, attribute, generation) {
      const view = views.get(this);
      const value = view?.getAttribute?.(attribute) ?? this.getAttribute(attribute) ?? '';
      if (value && typeof value === 'object' && view?.create_child_view) {
        try {
          const child = await view.create_child_view(value);
          if (generation === this._generation && parent.isConnected) {
            this._children.push(child); parent.append(child.el);
          } else child.remove();
        } catch (error) {
          if (generation === this._generation) signal(this, 'error', {message: String(error)});
        }
      } else if (this.getAttribute('data-mcui-html') === 'true') parent.innerHTML = String(value);
      else parent.textContent = String(value);
    }

    update() {
      this.clearPopup();
      if (!this.open || !this.isConnected) return;
      const generation = this._generation;
      const popup = this.ownerDocument.createElement('div');
      this._popup = popup;
      popup.className = `mcui-root mcui-native mcui-${this.kind}`;
      popup.id = 'mcui-popup-' + Math.random().toString(36).slice(2);
      popup.setAttribute('role', this.kind === 'tooltip' ? 'tooltip' : 'dialog');
      this.ownerDocument.body.append(popup);
      if (this.kind === 'popover') {
        const title = this.ownerDocument.createElement('div');
        title.className = 'mcui-popover-header'; popup.append(title);
        this.fillContent(title, 'data-mcui-title', generation);
      }
      const body = this.ownerDocument.createElement('div'); popup.append(body);
      this.fillContent(body, this.kind === 'tooltip' ? 'data-mcui-title' : 'data-mcui-content', generation);
      this._description = popup.id;
      this._descriptionTarget = this.querySelector('button,a[href],input,select,textarea,[tabindex]') || this;
      this._descriptionTarget.setAttribute('aria-describedby', [this._descriptionTarget.getAttribute('aria-describedby'), popup.id].filter(Boolean).join(' '));
      this._outside = new AbortController();
      this.ownerDocument.addEventListener('click', event => {
        if (!this.contains(event.target) && !popup.contains(event.target)) this.hide();
      }, {signal: this._outside.signal});
      this.ownerDocument.addEventListener('keydown', event => { if (event.key === 'Escape') this.hide(); }, {signal: this._outside.signal});
      requestAnimationFrame(() => {
        if (generation !== this._generation || !popup.isConnected) return;
        const r = this.getBoundingClientRect(), p = popup.getBoundingClientRect();
        const placement = this.getAttribute('data-mcui-placement') || 'top';
        let x = r.left + (r.width - p.width) / 2, y = r.top - p.height - 8;
        if (placement === 'bottom') y = r.bottom + 8;
        if (placement === 'left') { x = r.left - p.width - 8; y = r.top; }
        if (placement === 'right') { x = r.right + 8; y = r.top; }
        popup.style.left = Math.max(4, Math.min(innerWidth - p.width - 4, x)) + 'px';
        popup.style.top = Math.max(4, Math.min(innerHeight - p.height - 4, y)) + 'px';
      });
    }
  }
  class McuiTooltip extends McuiPopup {}
  class McuiPopover extends McuiPopup {}

  const elements = {root: McuiRoot, grid: McuiGrid, flex: McuiFlex,
    panel: McuiPanel, 'panel-header': McuiPanelHeader, 'panel-body': McuiPanelBody, 'panel-footer': McuiPanelFooter,
    collapse: McuiCollapse, accordion: McuiAccordion, opener: McuiOpener,
    tabs: McuiTabs, 'tab-list': McuiTabList, dropdown: McuiDropdown, carousel: McuiCarousel,
    tooltip: McuiTooltip, popover: McuiPopover};
  for (const [name, Component] of Object.entries(elements)) customElements.define(`mcui-${name}`, Component);

  // Only the live widget bridge is global. Behaviors use custom-element lifecycles.
  window.McUtilsApps = Object.freeze({elements: Object.freeze(elements),
    mount(view) {
      const element = view.el || view;
      if (view.el) views.set(element, view);
      element.refresh?.();
    },
    dispose(element) { views.delete(element); }
  });
})();
