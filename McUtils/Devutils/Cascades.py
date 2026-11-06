"""
Property cascades: declare what each stored or derived value of an object depends on, and let setters
invalidate everything downstream of them.

The idiom this replaces is hand-written bookkeeping like::

    @coords.setter
    def coords(self, c):
        self.embedding.coords = c
        self._pg = None                # point group belonged to the old geometry
        self._hamiltonian = None       # ...and so on, wherever someone remembered

A `PropertyCascade` is the dependency graph (``name -> names it depends on``); `cascading_property` is a
`property` whose setter invalidates the dependents of its name; `derived_property` is a lazily computed,
cached value that is cleared whenever anything it depends on changes; `cascading_attribute` is a plain
stored attribute whose assignment cascades. Classes don't inherit anything. Instead each object *explicitly*
owns a `CascadingPropertyManager` under the name ``_cascade_manager`` -- created in ``__init__``, or supplied
by a property if you want it built lazily -- and the descriptors raise a `CascadeManagerError` if it is missing::

    class Thing:
        cascade_dependencies = {'summary': ['a', 'b']}   # extra nodes / edges not tied to a descriptor

        def __init__(self, a):
            self._cascade_manager = CascadingPropertyManager(self, listeners=[print_changes])
            self._a = a

        @cascading_property
        def a(self): return self._a
        @a.setter
        def a(self, v): self._a = v

        energy_evaluator = cascading_attribute()        # plain stored attribute, `_energy_evaluator`

        @derived_property(depends_on=['a', 'energy_evaluator'])
        def energy(self): return self.energy_evaluator(self.a)

    with thing._cascade_manager.batch():                # cascade once, at the end
        thing.a = 1

Nodes are plain names, so values that aren't descriptors (cache keys, manager-held state) can take part
too. Listeners (``f(obj, changed, affected)``) are told which names changed and which dependents were reset,
which is how persistent caches learn that an identifier no longer vouches for a value.
"""

import contextlib, weakref

__all__ = [
    "PropertyCascade",
    "CascadingPropertyManager",
    "CascadeManagerError",
    "cascading_property",
    "cascading_attribute",
    "derived_property"
]


def _same(a, b):
    """Whether assigning `b` over `a` is a no-op: the same object, or values that compare equal to a plain `True`"""
    if a is b:
        return True
    try:
        r = (a == b)
    except Exception:
        return False
    return type(r).__name__ in ('bool', 'bool_') and bool(r)


def _as_names(names):
    if names is None:
        return ()
    if isinstance(names, str):
        return (names,)
    return tuple(names)


class PropertyCascade:
    """
    The dependency graph behind a cascade. Edges point from a name to the names it depends on; a
    *keyed* dependency is one the dependent's cache key already includes, so a change to it makes the
    dependent's in-memory value stale (it is reset) but not its persistent entries (those are looked up
    under the new key).
    """

    def __init__(self, dependencies=None):
        """
        :param dependencies: ``{name: depends_on}``; `depends_on` is a name or an iterable of names, or a
            dict of `add` arguments (``{'depends_on': ..., 'keyed': ..., 'reset': ...}``)
        """
        self._deps = {}      # name -> {dependency: keyed}
        self._resets = {}    # name -> [slot name | callable]
        self._reverse = None
        if dependencies:
            self.update(dependencies)

    def __contains__(self, name):
        return name in self._deps

    def __iter__(self):
        return iter(self._deps)

    def __len__(self):
        return len(self._deps)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, {k: sorted(v) for k, v in self._deps.items()})

    def add(self, name, depends_on=(), *, keyed=(), reset=None):
        """
        Registers `name` (and its edges). Adding a name again merges the edges.

        :param name: the node
        :param depends_on: names that `name` is computed from
        :param keyed: names `name`'s cache key already includes (also dependencies)
        :param reset: what to do to the instance when `name` is invalidated: a slot (attribute) name that
            is set to `None`, a callable taking the instance, or a list of those
        """
        node = self._deps.setdefault(name, {})
        for d in _as_names(depends_on):
            node[d] = node.get(d, False)
            self._deps.setdefault(d, {})
        for d in _as_names(keyed):
            node[d] = True
            self._deps.setdefault(d, {})
        if reset is not None:
            resets = self._resets.setdefault(name, [])
            for r in (reset if isinstance(reset, (list, tuple)) else [reset]):
                if r not in resets:
                    resets.append(r)
        self._reverse = None
        return self

    def update(self, other):
        """Merges another cascade, or a ``{name: depends_on}`` dict, into this one"""
        if isinstance(other, PropertyCascade):
            for name, deps in other._deps.items():
                self.add(name)
                node = self._deps[name]
                for d, keyed in deps.items():
                    node[d] = node.get(d, False) or keyed
                    self._deps.setdefault(d, {})
            for name, resets in other._resets.items():
                self.add(name, reset=list(resets))
        else:
            for name, spec in dict(other).items():
                if isinstance(spec, dict):
                    self.add(name, **spec)
                else:
                    self.add(name, spec)
        self._reverse = None
        return self

    def copy(self):
        return type(self)().update(self)

    def dependencies(self, name, *, keyed=True):
        """The direct dependencies of `name` (leaving out keyed ones if `keyed=False`)"""
        return frozenset(d for d, k in self._deps.get(name, {}).items() if keyed or not k)

    def ancestors(self, name, *, keyed=True):
        """Everything `name` depends on, transitively (not including `name`)"""
        seen = set()
        stack = [name]
        while stack:
            for d in self.dependencies(stack.pop(), keyed=keyed):
                if d not in seen:
                    seen.add(d)
                    stack.append(d)
        seen.discard(name)
        return frozenset(seen)

    def _reverse_edges(self):
        if self._reverse is None:
            rev = {}
            for name, deps in self._deps.items():
                for d in deps:
                    rev.setdefault(d, []).append(name)
            self._reverse = rev
        return self._reverse

    def dependents(self, *names, include_self=False):
        """
        Everything downstream of `names` (transitively), ordered so that a name comes before the names that
        depend on it. The names themselves are included, first, only with `include_self=True`.
        """
        rev = self._reverse_edges()
        order, seen = [], set()

        def visit(n):
            for m in rev.get(n, ()):
                if m not in seen:
                    seen.add(m)
                    visit(m)
                    order.append(m)

        for n in names:
            visit(n)
        order.reverse()
        order = [n for n in order if n not in names]
        if include_self:
            order = list(dict.fromkeys(names)) + order
        return order

    def is_stale(self, name, changed):
        """
        Whether a persistent value stored under `name` can no longer be trusted given that the names in
        `changed` have changed: something `name` depends on, through a non-keyed edge, changed. (A change
        to `name` itself is an in-memory override and doesn't affect what is stored under it.) A `name`
        the cascade doesn't know is stale after *any* change.
        """
        changed = set(changed)
        if not changed:
            return False
        if name not in self._deps:
            return True
        return bool(changed & self.ancestors(name, keyed=False))

    def resets(self, name):
        return tuple(self._resets.get(name, ()))


class _CascadeNode:
    """Base for the descriptors that register themselves in a class's cascade"""
    name = None
    depends_on = ()
    keyed = ()
    slot = None
    reset = None

    def register(self, cascade, name):
        cascade.add(self.name or name, self.depends_on, keyed=self.keyed, reset=self.reset)

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name
        if self.slot is None:
            self.slot = '_' + self.name


class CascadeManagerError(AttributeError):
    """Raised when a cascading descriptor is used on an object that doesn't own a (matching) `CascadingPropertyManager`"""


def _manager_for(obj, name):
    try:
        manager = obj._cascade_manager
    except AttributeError:
        raise CascadeManagerError(
            "{}.{} is a cascading property but the {} has no `_cascade_manager`; create one with "
            "`self._cascade_manager = CascadingPropertyManager(self)` in `__init__` (or provide it as a property)".format(
                type(obj).__name__, name, type(obj).__name__)
        ) from None
    if manager.obj is not obj:
        raise CascadeManagerError(
            "the `_cascade_manager` of this {} belongs to a different object (was it copied or unpickled?); "
            "create a new `CascadingPropertyManager(self)` for the copy".format(type(obj).__name__)
        )
    return manager


class CascadingPropertyManager:
    """
    The runtime half of a property cascade, owned explicitly by the object whose properties cascade and stored
    on it as ``_cascade_manager``. It holds the object's `PropertyCascade` graph (built once per class from the
    cascading descriptors and an optional class attribute ``cascade_dependencies``, merged along the MRO),
    applies resets, and tells listeners what changed::

        self._cascade_manager = CascadingPropertyManager(self, listeners=[notify])

    It keeps only a weak reference to its object. A copied object must be given a manager of its own (the
    descriptors raise `CascadeManagerError` otherwise), and an unpickled manager is unattached.
    """
    _graphs = weakref.WeakKeyDictionary()

    def __init__(self, obj=None, listeners=()):
        """
        :param obj: the object that owns this manager
        :param listeners: functions ``f(obj, changed, affected)`` called after every cascade
        """
        self._owner = None if obj is None else weakref.ref(obj)
        self._batch = None
        self._muted = False
        self._listeners = list(listeners)

    @classmethod
    def graph_for(cls, type_):
        """The merged `PropertyCascade` for a class (cached)"""
        graph = cls._graphs.get(type_)
        if graph is None:
            graph = PropertyCascade()
            for base in reversed(type_.__mro__):
                for name, attr in vars(base).items():
                    if isinstance(attr, _CascadeNode):
                        attr.register(graph, name)
                table = vars(base).get('cascade_dependencies')
                if table is not None:
                    graph.update(table)
            cls._graphs[type_] = graph
        return graph

    @property
    def obj(self):
        return None if self._owner is None else self._owner()

    @property
    def graph(self):
        return self.graph_for(type(self.obj))

    def __reduce__(self):
        return (type(self), ())  # an unattached manager; `of` re-binds it to whatever object ends up holding it

    # graph queries, so `obj.cascade.is_stale(...)` style access reads naturally
    def __contains__(self, name):
        return name in self.graph

    def dependents(self, *names, **kw):
        return self.graph.dependents(*names, **kw)

    def is_stale(self, name, changed):
        return self.graph.is_stale(name, changed)

    def changed(self, *names):
        """
        Declares that the stored values `names` have changed: every dependent is reset, then listeners are
        told. Called by the cascading descriptors, or by hand after a mutation they can't see.

        :return: the affected (downstream) names
        """
        if self._batch is not None:
            self._batch.update(names)
            return []
        obj = self.obj
        graph = self.graph
        affected = graph.dependents(*names)
        for n in affected:
            for r in graph.resets(n):
                if callable(r):
                    r(obj)
                else:
                    setattr(obj, r, None)
        if not self._muted:
            for listener in tuple(self._listeners):
                listener(obj, tuple(names), tuple(affected))
        return affected

    @contextlib.contextmanager
    def batch(self):
        """Collects the changes made inside the block and cascades them once, at the end"""
        if self._batch is not None:
            yield
            return
        self._batch = set()
        try:
            yield
        finally:
            names, self._batch = self._batch, None
            if names:
                self.changed(*sorted(names))

    @contextlib.contextmanager
    def suspended(self):
        """Makes the changes inside the block silent (for constructors and loaders that seed state)"""
        saved = self._batch
        self._batch = set()
        try:
            yield
        finally:
            self._batch = saved

    @contextlib.contextmanager
    def muted(self):
        """
        Inside the block dependents are still reset but listeners aren't told. For storing a value that was
        *computed* from the object's current state (a derivative tensor, a loaded result): its dependents
        should be rebuilt, but nothing a persistent cache vouches for has changed.
        """
        saved = self._muted
        self._muted = True
        try:
            yield
        finally:
            self._muted = saved

    def add_listener(self, listener):
        """Registers ``listener(obj, changed, affected)`` on this instance, called after every cascade"""
        self._listeners.append(listener)


class cascading_property(property, _CascadeNode):
    """
    A `property` whose setter (and deleter) cascade: once the setter body has run, the dependents of the
    property's name are reset. Used as a decorator, with or without arguments::

        @cascading_property
        def coords(self): ...
        @coords.setter
        def coords(self, c): ...

        @cascading_property(depends_on=['embedding'])
        def masses(self): ...

    With `always=False`, assigning a value equal to the one the property already holds doesn't cascade.
    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None, *,
                 depends_on=(), keyed=(), reset=None, name=None, always=True):
        super().__init__(fget, fset, fdel, doc)
        self.name = name
        self.depends_on = _as_names(depends_on)
        self.keyed = _as_names(keyed)
        self.reset = reset
        self.always = always
        self.slot = None
        self._fget, self._fset, self._fdel, self._doc = fget, fset, fdel, doc
        if doc is None and fget is not None:
            self.__doc__ = fget.__doc__

    def __call__(self, fget):
        return self.getter(fget)

    def _clone(self, fget, fset, fdel):
        new = type(self)(fget, fset, fdel, self._doc, depends_on=self.depends_on, keyed=self.keyed,
                         reset=self.reset, name=self.name, always=self.always)
        if fget is not None and self._doc is None:
            new.__doc__ = fget.__doc__
        return new

    def getter(self, fget):
        return self._clone(fget, self._fset, self._fdel)

    def setter(self, fset):
        return self._clone(self._fget, fset, self._fdel)

    def deleter(self, fdel):
        return self._clone(self._fget, self._fset, fdel)

    def __set_name__(self, owner, name):
        _CascadeNode.__set_name__(self, owner, name)

    def __set__(self, obj, value):
        if self._fset is None:
            raise AttributeError("can't set attribute '{}'".format(self.name))
        if not self.always:
            try:
                if self._fget is not None and _same(self._fget(obj), value):
                    return
            except Exception:
                pass
        super().__set__(obj, value)
        _manager_for(obj, self.name).changed(self.name)

    def __delete__(self, obj):
        super().__delete__(obj)
        _manager_for(obj, self.name).changed(self.name)


class cascading_attribute(_CascadeNode):
    """
    A plain stored attribute (kept in ``_<name>``) whose assignment cascades. `coerce` is applied to assigned
    values; `default` is returned until a value is set. Assigning a value equal to the one already held doesn't cascade.
    The backing slot can be seeded directly (``self._energy_evaluator = x``) where a constructor shouldn't cascade.
    """

    def __init__(self, default=None, *, depends_on=(), keyed=(), reset=None, coerce=None, name=None, doc=None, slot=None):
        self.default = default
        self.depends_on = _as_names(depends_on)
        self.keyed = _as_names(keyed)
        self.reset = reset
        self.coerce = coerce
        self.name = name
        self.slot = slot
        self.__doc__ = doc

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.slot, self.default)

    def __set__(self, obj, value):
        if self.coerce is not None:
            value = self.coerce(value)
        old = obj.__dict__.get(self.slot, self.default)
        obj.__dict__[self.slot] = value
        if not _same(old, value):
            _manager_for(obj, self.name).changed(self.name)


class derived_property(_CascadeNode):
    """
    A value computed on first access, kept in ``_<name>``, and cleared when anything it depends on changes
    (``None`` means "not computed"). Assigning a value seeds it (assigning `None` clears it) without
    cascading, so a constructor argument or a loaded result can stand in for the computation; `settable=False`
    makes it read-only. Used as a decorator, with or without arguments::

        @derived_property(depends_on=['coords', 'masses'])
        def point_group(self): ...
    """

    def __init__(self, fget=None, *, depends_on=(), keyed=(), reset=None, name=None, slot=None, settable=True, doc=None):
        self.fget = fget
        self.depends_on = _as_names(depends_on)
        self.keyed = _as_names(keyed)
        self.reset = reset
        self.name = name
        self.slot = slot
        self.settable = settable
        self.__doc__ = doc if doc is not None else getattr(fget, '__doc__', None)

    def __call__(self, fget):
        self.fget = fget
        if self.__doc__ is None:
            self.__doc__ = fget.__doc__
        return self

    def register(self, cascade, name):
        # the slot is part of its own reset, so invalidating the name clears the value
        extra = [] if self.reset is None else (list(self.reset) if isinstance(self.reset, (list, tuple)) else [self.reset])
        cascade.add(self.name or name, self.depends_on, keyed=self.keyed, reset=[self.slot] + extra)

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        val = obj.__dict__.get(self.slot)
        if val is None:
            val = self.fget(obj)
            if val is not None:
                obj.__dict__[self.slot] = val
        return val

    def __set__(self, obj, value):
        if not self.settable:
            raise AttributeError("can't set attribute '{}'".format(self.name))
        obj.__dict__[self.slot] = value
