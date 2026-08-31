"""
Provides the conversion framework between coordinate systems
"""

from collections import OrderedDict as odict, deque
import os, abc, uuid, numpy as np, weakref
from ...Extensions import ModuleLoader
from ...Numputils import apply_by_coordinates

__all__ = [
    "CoordinateSystemConverters",
    "CoordinateSystemConverter",
    "SimpleCoordinateSystemConverter"
]

__reload_hook__ = ["...Extensions", '.CartesianToZMatrix', '.ZMatrixToCartesian']

######################################################################################################
##
##                    Reload-safe module-level backing store
##
## `CoordinateSystemConverters` gets *redefined* (a brand new class object) every time this module
## is reloaded. If the registry lives as plain class-body attributes (`converters = odict([])`,
## `converter_graph = None`), every reload silently throws the old registry away and starts a new,
## disconnected one -- and anything registered against an older generation of the class (e.g. from a
## package like Psience that wasn't part of the reload and still references old McUtils classes)
## ends up writing into an orphaned dict that nothing queries anymore.
##
## `importlib.reload` re-executes the module body *in the module's existing __dict__*, so a global
## that's only initialized when it doesn't already exist survives reload untouched. That's the
## standard idiom used below to make the registry itself reload-proof, independent of which
## generation of `CoordinateSystemConverters` happens to be asking for it.
######################################################################################################

try:
    _CONVERTER_REGISTRY
except NameError:
    _CONVERTER_REGISTRY = odict()  # (name1, name2) -> converter

try:
    _CONVERTER_GRAPH
except NameError:
    _CONVERTER_GRAPH = None  # ConversionGraph over names, built lazily

try:
    _CONVERTER_OBJECT_CACHE
except NameError:
    # name -> a representative live CoordinateSystem class/instance for that name.
    # Weak-valued so we don't pin arbitrary per-molecule systems in memory forever.
    _CONVERTER_OBJECT_CACHE = weakref.WeakValueDictionary()

try:
    _CONVERTER_NAME_CACHE
except NameError:
    # object -> generated name, for systems that can't hold their own `.name` attribute
    _CONVERTER_NAME_CACHE = weakref.WeakKeyDictionary()

try:
    _CONVERTER_ID_NAME_CACHE
except NameError:
    # id(object) -> generated name, last-resort fallback for objects that aren't weakly
    # referenceable at all (rare; this can leak for the lifetime of the process in that case)
    _CONVERTER_ID_NAME_CACHE = {}

try:
    _CONVERTER_CHAINED_KEYS
except NameError:
    # keys in _CONVERTER_REGISTRY whose value is a ChainedCoordinateSystemConverter, so
    # deregistration can find dead composite entries without scanning the whole registry
    _CONVERTER_CHAINED_KEYS = set()

try:
    _CONVERTER_FINAL_NODES
except NameError:
    # the (small, bounded-by-the-number-of-canonical-types) set of *final* graph nodes.
    # The "alias across compatible systems" pass in `_register` only ever needs to compare
    # against other final nodes -- but the shared conversion graph also holds every fast-path
    # (non-final, typically per-molecule) node, which grows without bound over a long session.
    # Scanning `graph.keys()` directly for that pass means re-scanning the *entire* graph on
    # every single registration that touches a final system, which is O(n) per call and O(n^2)
    # overall as the fast-path population grows. Keeping final nodes in their own set makes
    # that pass O(#final types) per call instead -- effectively constant.
    _CONVERTER_FINAL_NODES = set()

######################################################################################################
##
##                                   CoordinateSystemConverter Class
##
######################################################################################################
class CoordinateSystemConverter(metaclass=abc.ABCMeta):
    """
    A base class for type converters
    """

    converters = None

    @property
    @abc.abstractmethod
    def types(self):
        """The types property of a converter returns the types the converter converts

        """
        pass

    def convert_many(self, coords_list, **kwargs):
        """Converts many coordinates. Used in cases where a CoordinateSet has higher dimension
        than its basis dimension. Should be overridden by a converted to provide efficient conversions
        where necessary.

        :param coords_list: many sets of coords
        :type coords_list: np.ndarray
        :param kwargs:
        :type kwargs:
        """
        return np.array([self.convert(coords, **kwargs) for coords in coords_list])

    @abc.abstractmethod
    def convert(self, coords, **kwargs):
        """The main necessary implementation method for a converter class.
        Provides the actual function that converts the coords set

        :param coords:
        :type coords: np.ndarray
        :param kwargs:
        :type kwargs:
        """
        pass

    def register(self, where=None, check=True, name_format=None, final=None):
        """
        Registers the CoordinateSystemConverter

        :return:
        :rtype:
        """
        if where is None:
            where = self.converters if not isinstance(self.converters, weakref.ref) else self.converters()
            if where is None:
                type(self).converters = weakref.ref(CoordinateSystemConverters)
                where = type(self).converters()
        where.register_converter(*self.types, self, check=check, name_format=name_format, final=final)
    def deregister(self, where=None, check=True):
        """
        Registers the CoordinateSystemConverter

        :return:
        :rtype:
        """
        if where is None:
            where = self.converters if not isinstance(self.converters, weakref.ref) else self.converters()
            if where is None:
                type(self).converters = weakref.ref(CoordinateSystemConverters)
                where = type(self).converters()
        where.deregister_converter(*self.types, self, check=check)

    def __call__(self, coords, **kwargs):
        if coords.ndim > 2: #TODO: make this a more robust check for the future
            return self.convert_many(coords, **kwargs)
        else:
            return self.convert(coords, **kwargs)

######################################################################################################
##
##                                   CoordinateSystemConverters Class
##
######################################################################################################
class CoordinateSystemConverters:
    """
    A coordinate converter class. It's a singleton so can't be instantiated.

    Registry keys are, by default, the system objects themselves -- cheap identity-based
    hashing, exactly like the original implementation, with no string work at all. That's fine
    for the overwhelming majority of registrations (typically short-lived, per-molecule
    instances that never need to be looked up across an `importlib.reload` boundary in
    practice, since they get rebuilt from scratch whenever the thing that reload affected --
    e.g. a molecule -- gets rebuilt too).

    Only systems explicitly marked *final* -- via an `is_final_coordinate_system` attribute, or
    by having a `.name` in `cls.final_system_names` -- get resolved to a stable string key
    instead. Those are the small set of canonical, singleton-ish types (`CartesianCoordinates3D`,
    `ZMatrixCoordinateSystem`, etc.) that are actually defined in code subject to reload, and are
    therefore the only ones where object identity is untrustworthy across a reload. Confining the
    string resolution (and the "alias across compatible systems" registration pass, which is the
    expensive part) to just those systems keeps registration/deregistration/lookup for everything
    else at the original O(1)-ish cost.
    """

    # bound to the module-level, reload-persistent objects -- see block above. Every generation of
    # this class shares the same underlying dict/graph.
    converters = _CONVERTER_REGISTRY
    converter_graph = _CONVERTER_GRAPH
    converters_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "Resources",
        "Converters"
    )
    converters_package = ".".join(__name__.split(".")[:-1])
    converter_type = CoordinateSystemConverter

    # used to mint a name for any system that doesn't provide a stable `.name`; override by
    # passing `name_format` through to `register`/`register_converter` if you want something
    # more descriptive than a bare uuid for a particular family of anonymous systems
    default_anonymous_name_format = "AnonymousCoordinateSystem<{uuid}>"

    # fallback allowlist for marking systems "final" by name, for cases where you'd rather not
    # (or can't) add an `is_final_coordinate_system = True` attribute to the class itself.
    # Pre-populated with the built-in canonical types; extend/replace as needed --
    # `CoordinateSystemConverters.final_system_names |= {"MyCustomSingletonSystem"}`.
    final_system_names = frozenset({
        "Cartesian3D", "ZMatrix", "SphericalCoordinates",
        "GenericInternals", "IterativeZMatrix",
    })

    def __init__(self):
        raise NotImplementedError("{} is a singleton".format(type(self)))

    @classmethod
    def get_coordinates(self, coordinate_set):
        """Extracts coordinates from a coordinate_set
        """
        pass

    ##################################################################################################
    ## name resolution
    ##################################################################################################

    @classmethod
    def _get_cached_name(cls, system):
        try:
            return _CONVERTER_NAME_CACHE.get(system)
        except TypeError:
            return _CONVERTER_ID_NAME_CACHE.get(id(system))

    @classmethod
    def _cache_name(cls, system, name):
        try:
            _CONVERTER_NAME_CACHE[system] = name
        except TypeError:
            _CONVERTER_ID_NAME_CACHE[id(system)] = name

    @classmethod
    def _cache_object(cls, name, obj):
        try:
            _CONVERTER_OBJECT_CACHE[name] = obj
        except TypeError:
            # not weakly referenceable (e.g. a bare class in some Python versions); safe to skip,
            # worst case we fall back to the name string itself when reconstructing a chained path
            pass

    @classmethod
    def _is_final(cls, system):
        """
        Whether `system` should be treated as "final" -- i.e. stable/canonical enough that it
        needs a reload-proof string key. Checked, in order: an explicit
        `is_final_coordinate_system` attribute (set this on your canonical classes, e.g.
        `CartesianCoordinates3D.is_final_coordinate_system = True`, to opt in explicitly), then
        membership of `.name` in `cls.final_system_names` as a no-code-changes-needed fallback.
        Everything else is treated as an ordinary, cheaply-object-keyed system.
        """
        flag = getattr(system, 'is_final_coordinate_system', None)
        if flag is not None:
            return bool(flag)
        return getattr(system, 'name', None) in cls.final_system_names

    @classmethod
    def _resolve_key(cls, system, name_format=None, final=None):
        """
        The actual registry key for `system`: the object itself (fast path) unless it's final
        (or `final=True` is forced explicitly), in which case it's resolved to a stable string.
        """
        is_final = cls._is_final(system) if final is None else final
        if not is_final:
            return system
        return cls._resolve_name(system, name_format=name_format)

    @classmethod
    def _resolve_name(cls, system, name_format=None):
        """
        Resolves a stable string identifier for a CoordinateSystem class or instance. Only ever
        called for systems that are "final" (see `_is_final`) -- everything else is keyed by the
        object itself and never pays this cost.

        Uses `.name` when present -- and *only* `.name`. This deliberately does NOT fold in
        `.dimension` or anything else: whether an attribute like `.dimension` is populated (and
        to what) can differ across the different call sites that touch what is logically the
        same system (e.g. a generic class-level registration vs. a bound instance later), which
        would split one logical system into multiple registry keys that never match each other.
        Distinguishing genuinely different systems that happen to share a base name (e.g. two
        differently-shaped `MolecularCartesians`) is expected to be handled by `.name` itself --
        which this codebase already does by minting per-instance names (e.g.
        `MolecularCartesians-<uuid>`) wherever that distinction actually matters.

        Anything with no `.name` at all (`name is None`) gets a uuid-based name minted via
        `name_format` (falling back to `default_anonymous_name_format`), cached against the
        object so repeated lookups of the *same* object are stable for its lifetime.
        """
        base = getattr(system, 'name', None)
        if base:
            return base

        cached = cls._get_cached_name(system)
        if cached is not None:
            return cached

        fmt = name_format or cls.default_anonymous_name_format
        new_name = fmt.format(uuid=uuid.uuid4().hex)

        # best effort: stash the name directly on the object so that even a *different*
        # generation of this class (post-reload) sees the same identifier for it next time
        try:
            system.name = new_name
        except Exception:
            cls._cache_name(system, new_name)

        return new_name

    @classmethod
    def _systems_compatible(cls, a, b):
        try:
            return a.is_compatible(a, b)
        except Exception:
            # never let a stale cross-generation object (e.g. an isinstance check against a
            # class from a different reload generation) blow up registration
            return False

    ##################################################################################################
    ## loading
    ##################################################################################################

    @classmethod
    def _get_converter_file(self, file):
        if os.path.exists(file):
            abspath = file
        else:
            abspath = os.path.join(self.converters_dir, file)
        return abspath

    @classmethod
    def load_converter(cls, converter):

        file = cls._get_converter_file(converter)
        loader = ModuleLoader(cls.converters_dir, cls.converters_package)
        env = loader.load(file)

        try:
            converters = env.__converters__
        except KeyError:
            raise KeyError("converter at {} missing field '{}'".format(file, "converters"))

        for conv in converters:
            cls._register(*conv.types, conv)

    _converters_loaded = False
    @classmethod
    def _preload_converters(cls):
        """
        Preloads Cartesian/ZMatrix converters.
        Maybe will load others in the future.
        :return:
        :rtype:
        """
        global _CONVERTER_GRAPH
        if _CONVERTER_GRAPH is None:
            _CONVERTER_GRAPH = ConversionGraph()
        # `converter_graph` is reset to `_CONVERTER_GRAPH`'s value from *class body definition
        # time* on every reload; re-bind it here so this (possibly new) generation of the class
        # always points at the one persistent graph object.
        cls.converter_graph = _CONVERTER_GRAPH

        if not cls._converters_loaded:
            from .DefaultConverters import __converters__ as converters
            for conv in converters:
                cls._register(*conv.types, conv, move_to_end=True)

            if os.path.exists(cls.converters_dir):
                for file in os.listdir(cls.converters_dir):
                    if os.path.splitext(file)[1] == ".py":
                        cls.load_converter(file)
            cls._converters_loaded = True

    ##################################################################################################
    ## lookup
    ##################################################################################################

    @classmethod
    def get_converter(cls, system1, system2):
        """
        Gets the appropriate converter for two CoordinateSystem objects

        :param system1:
        :type system1: CoordinateSystem
        :param system2:
        :type system2: CoordinateSystem
        :return:
        :rtype:
        """
        conv = system1.get_direct_converter(system2)
        if conv is not None:
            return conv

        conv = system2.get_inverse_converter(system1)
        if conv is not None:
            return conv

        cls._preload_converters()

        k1 = cls._resolve_key(system1)
        k2 = cls._resolve_key(system2)
        if isinstance(k1, str):
            cls._cache_object(k1, system1)
        if isinstance(k2, str):
            cls._cache_object(k2, system2)

        if (k1, k2) in cls.converters:
            key_path = [(k1, k2)]
        else:
            key_path = cls.converter_graph.find_path_bfs(k1, k2)

        if key_path is None:
            raise KeyError(
                "{}: no rules for converting coordinate system {} to {} in {}".format(
                    cls.__name__, system1, system2,
                    ["{}=>{}".format(a, b) for a, b in cls.converters]
                )
            )
        elif len(key_path) == 1:
            return cls.converters[key_path[0]]
        else:
            def _obj_for(key):
                if key == k1:
                    return system1
                if key == k2:
                    return system2
                if isinstance(key, str):
                    return _CONVERTER_OBJECT_CACHE.get(key, key)
                return key  # already a live object -- fast-path key

            conversions = [
                (cls.converters[p], (_obj_for(p[0]), _obj_for(p[1])))
                for p in key_path
            ]
            return ChainedCoordinateSystemConverter((system1, system2), conversions)

    ##################################################################################################
    ## registration
    ##################################################################################################

    @classmethod
    def register_converter(cls, system1, system2, converter, check=True, name_format=None, final=None):
        """
        Registers a converter between two coordinate systems

        :param system1:
        :type system1: CoordinateSystem
        :param system2:
        :type system2: CoordinateSystem
        :param final: force the "final" (string-keyed) treatment on or off for this
            registration, instead of relying on auto-detection via `_is_final`. Pass a single
            bool for both systems, or a `(final1, final2)` pair to set them independently.
        :return:
        :rtype:
        """
        cls._preload_converters()
        if check and not hasattr(converter, 'convert'): #isinstance(converter, cls.converter_type):
            raise TypeError('{}: registered converters should be subclasses of {} <{}> (got {} which inherits from {})'.format(
                cls.__name__,
                cls.converter_type, id(cls.converter_type),
                type(converter),
                ["{} <{}>".format(x, id(x)) for x in type(converter).__bases__]
            ))
        cls._register(system1, system2, converter, name_format=name_format, final=final)

    @classmethod
    def deregister_converter(cls, system1, system2, converter, check=True):
        """
        Registers a converter between two coordinate systems

        :param system1:
        :type system1: CoordinateSystem
        :param system2:
        :type system2: CoordinateSystem
        :return:
        :rtype:
        """
        k1, k2 = cls._resolve_key(system1), cls._resolve_key(system2)
        if cls.converters.get((k1, k2)) is converter:
            del cls.converters[(k1, k2)]
            _CONVERTER_CHAINED_KEYS.discard((k1, k2))
            # only scan the (typically tiny) set of explicitly-registered composite converters,
            # rather than the whole registry, to find any that routed through this edge
            if _CONVERTER_CHAINED_KEYS:
                dead = []
                for k in list(_CONVERTER_CHAINED_KEYS):
                    v = cls.converters.get(k)
                    if v is None:
                        _CONVERTER_CHAINED_KEYS.discard(k)
                        continue
                    if (k1, k2) in getattr(v, 'edges', ()):
                        dead.append(k)
                for k in dead:
                    del cls.converters[k]
                    _CONVERTER_CHAINED_KEYS.discard(k)

    @classmethod
    def _register(cls, system1, system2, converter, move_to_end=False, name_format=None, final=None):
        if final is None:
            final1 = final2 = None
        elif isinstance(final, (tuple, list)):
            final1, final2 = final
        else:
            final1 = final2 = final

        k1 = cls._resolve_key(system1, name_format, final1)
        k2 = cls._resolve_key(system2, name_format, final2)
        is_final1 = isinstance(k1, str)
        is_final2 = isinstance(k2, str)
        if is_final1:
            cls._cache_object(k1, system1)
            _CONVERTER_FINAL_NODES.add(k1)
        if is_final2:
            cls._cache_object(k2, system2)
            _CONVERTER_FINAL_NODES.add(k2)

        cls.converters[(k1, k2)] = converter
        if move_to_end:
            cls.converters.move_to_end((k1, k2))
        if isinstance(converter, ChainedCoordinateSystemConverter):
            _CONVERTER_CHAINED_KEYS.add((k1, k2))

        graph = cls.converter_graph
        graph.add(k1, k2)

        # the "alias across compatible systems" pass only ever compares against *other final*
        # nodes -- scan the small, bounded final-node set, never the full (unboundedly large,
        # fast-path-dominated) graph.
        if not (is_final1 or is_final2):
            return

        for k_name in list(_CONVERTER_FINAL_NODES):
            if k_name in (k1, k2):
                continue
            k_obj = _CONVERTER_OBJECT_CACHE.get(k_name)
            if k_obj is None:
                continue
            if is_final1 and cls._systems_compatible(system1, k_obj):
                cls.converters[(k_name, k2)] = converter
                if move_to_end:
                    cls.converters.move_to_end((k_name, k2))
            elif is_final2 and cls._systems_compatible(system2, k_obj):
                cls.converters[(k1, k_name)] = converter
                if move_to_end:
                    cls.converters.move_to_end((k1, k_name))

class ConversionGraph:
    """
    Pulled from the UnitGraph stuff. Operates purely on hashable, value-comparable node keys
    (strings, in this codebase) -- no identity comparisons, so it doesn't care whether the
    objects a name was resolved from have since been redefined by a reload.
    """

    def __init__(self, stuff_to_update=()):
        self._graph = {}
        self.update(stuff_to_update)

    def __contains__(self, item):
        return item in self._graph

    def add(self, node, connection):
        self._graph.setdefault(node, set()).add(connection)
        self._graph.setdefault(connection, set())

    def keys(self):
        return self._graph.keys()

    def update(self, iterable):
        for connection in iterable:
            self.add(*connection)

    def find_path_bfs(self, start, end):
        # true BFS (FIFO via popleft) over value-comparable keys. The original implementation
        # compared nodes with `is`/`is not`, which only "worked" because it was operating on a
        # small set of module-level singleton classes; it silently breaks for arbitrary strings
        # (uuid-based names in particular are essentially never interned).
        if start not in self._graph or end not in self._graph:
            return None
        if start == end:
            return []

        q = deque()
        q.append(start)
        parents = {start: None}
        while q:
            cur = q.popleft()
            if cur == end:
                break
            for k in self._graph[cur]:
                if k in parents:
                    continue
                parents[k] = cur
                q.append(k)

        if end not in parents:
            return None

        path = []
        cur = end
        while cur != start:
            nxt = parents[cur]
            path.append((nxt, cur))
            cur = nxt
        return list(reversed(path))

class SimpleCoordinateSystemConverter(CoordinateSystemConverter):
    def __init__(self, types, conversion, **opts):
        super().__init__(**opts)
        self._types = types
        self.conversion = conversion
    @property
    def types(self):
        return self._types
    def convert(self, coords, **kw):
        return self.conversion(coords, **kw)
    def convert_many(self, coords, **kw):
        return self.convert(coords, **kw)
class ChainedCoordinateSystemConverter(CoordinateSystemConverter):

    def __init__(self, types, conversions, **opts):
        super().__init__(**opts)
        self._types = types
        conversions = self.prep_conversions(conversions)
        self.intermediates = {k[1] for k in (p for f, p in conversions)}
        self.edges = {p for f, p in conversions}
        self.conversions = conversions
    @classmethod
    def prep_conversions(cls, conv_list):
        conversions = []
        for f,p in conv_list:
            if isinstance(f, ChainedCoordinateSystemConverter):
                conversions.extend(f.conversions)
            else:
                conversions.append((f,p))
        return conversions
    @property
    def types(self):
        return self._types
    def convert(self, crds, **kwargs):
        cur = crds
        for f, p in self.conversions:
            if hasattr(p[0], 'convert_coords') and not isinstance(p[0], type):
                cur = p[0].convert_coords(cur, p[1], converter=f, **kwargs)
            else:
                cur = f(cur, **kwargs)
            if isinstance(cur, tuple):
                cur, kwargs = cur
            else:
                kwargs = {}
        return cur, kwargs
    def convert_many(self, coords, **kw):
        return self.convert(coords, **kw)

CoordinateSystemConverter.converters = weakref.ref(CoordinateSystemConverters)
