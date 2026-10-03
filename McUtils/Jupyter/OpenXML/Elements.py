"""Namespace-aware declarative Open XML elements built on JHTML.ContentXML."""

import copy

from ..JHTML import ContentXML

__all__ = ["OpenXML"]


class _Namespace:
    def __init__(self, prefix, uri, types):
        self.prefix, self.uri = prefix, uri
        self.types, self.aliases, self.classes, self.named_classes = {}, {}, {}, {}
        self.public_name = prefix
        if isinstance(types, type):
            types = [(value.tag.split(":")[-1], value) for value in vars(types).values()
                     if isinstance(value, type) and issubclass(value, OpenXML.TagElement)]
        else:
            types = types.items()
        for tag, value in types:
            if isinstance(value, type):
                self.classes.setdefault(tag, value)
                self.named_classes[value.__name__] = value
                aliases = (value.__name__,)
            else:
                aliases = tuple(value)
            self.types[tag] = self.types.get(tag, ()) + aliases
            self.aliases.update({alias: tag for alias in aliases})

    def __getattr__(self, name):
        if name in self.named_classes:
            return self.named_classes[name]
        tag = name if name in self.types else self.aliases.get(name.rstrip("_"))
        if tag is None:
            raise AttributeError(name)
        return self[tag]

    def __getitem__(self, tag):
        if tag not in self.types:
            raise KeyError(tag)
        if tag not in self.classes:
            cls = type(self.types[tag][0] if self.types[tag] else tag,
                       (OpenXML.TagElement,),
                       {"tag": self.prefix + ":" + tag, "__module__": __name__})
            self.classes[tag] = cls
        return self.classes[tag]

    def __dir__(self):
        return sorted(set(self.types) | set(self.aliases))


class OpenXML(ContentXML):
    """Registry of Open XML namespaces and their element constructors.

    Both ``OpenXML.p.sld`` and ``OpenXML.Presentation.Slide`` are available.
    Namespace-qualified attributes can use ``r__embed`` or ``**{'r:embed': ...}``.
    The small built-in vocabulary has explicit, readable element classes.
    Additional types can be registered or expressed with ``OpenXML.Element``.
    """
    namespaces = {}
    namespaces_by_uri = {}
    namespace_uris = {"xml": "http://www.w3.org/XML/1998/namespace"}

    boolean_values = ("0", "1")
    namespace_attributes = ("Requires", "mc:Ignorable", "mc:MustUnderstand")

    @classmethod
    def register_namespace(cls, prefix, uri, types):
        """Register an additional vocabulary; no network access is needed at runtime."""
        if prefix in cls.namespace_uris and cls.namespace_uris[prefix] != uri:
            raise ValueError("namespace prefix already registered: " + prefix)
        if not isinstance(types, type) and not hasattr(types, "items"):
            types = {tag: (tag,) for tag in types}
        namespace = _Namespace(prefix, uri, types)
        cls.namespaces[prefix] = namespace
        cls.namespaces_by_uri[uri] = namespace
        cls.namespace_uris[prefix] = uri
        setattr(cls, prefix, namespace)
        return namespace

    @classmethod
    def register_element(cls, prefix, tag, name=None):
        """Add one bespoke element to an existing namespace vocabulary."""
        namespace = cls.namespaces[prefix]
        name = name or tag
        if tag in namespace.types:
            raise ValueError("element already registered: " + prefix + ":" + tag)
        namespace.types[tag] = (name,)
        namespace.aliases[name] = tag
        return namespace[tag]

    @classmethod
    def get_element_type(cls, tag, namespace=None, attrs=None):
        if tag.startswith("{"):
            uri, local = tag[1:].split("}", 1)
            namespace = cls.namespaces_by_uri.get(uri)
        elif ":" in tag:
            prefix, local = tag.split(":", 1)
            namespace = cls.namespaces.get(prefix)
        else:
            local = tag
            if isinstance(namespace, str):
                namespace = cls.namespaces.get(namespace) or cls.namespaces_by_uri.get(namespace)
        if namespace is None or local not in namespace.types:
            return cls.Element
        if namespace.prefix == "a" and local == "ext" and attrs is not None and {"cx", "cy"}.issubset(attrs):
            return namespace.Extents
        return namespace[local]

    @classmethod
    def get_class_map(cls):
        result = {}
        for ns in cls.namespaces.values():
            for tag in ns.types:
                constructor = ns[tag]
                result[ns.prefix + ":" + tag] = constructor
                result["{" + ns.uri + "}" + tag] = constructor
        return result

    class Element(ContentXML.Element):
        can_be_dynamic = False
        default_prettify = False

        def __init__(self, tag, *elems, **attrs):
            super().__init__(tag, *elems, **attrs)

        def to_presml(self, context=None):
            return self

        def clone(self):
            children = [e.clone() if isinstance(e, OpenXML.Element) else e for e in self.elems]
            attrs = copy.deepcopy(dict(self.attrs))
            node = OpenXML.Element(self.tag, *children, **attrs) if type(self) is OpenXML.Element \
                else type(self)(*children, **attrs)
            node.tag = self.tag
            return node

        def walk(self):
            yield self
            for child in self.elems:
                if isinstance(child, OpenXML.Element):
                    yield from child.walk()

        def find(self, tag):
            return next((e for e in self.walk() if e.local_tag == tag or e.tag == tag), None)

        @property
        def local_tag(self):
            return self.tag.split(":")[-1]

        def to_source(self, name="OpenXML", indent=0):
            """Return executable declarative Python, with no embedded XML strings."""
            if type(self) is OpenXML.Element:
                constructor = name + ".Element"
                arguments = [repr(self.tag)]
            else:
                prefix, tag = type(self).tag.split(":", 1)
                namespace = OpenXML.namespaces[prefix]
                constructor = name + "." + namespace.public_name + "." + type(self).__name__
                arguments = []
            for child in self.elems:
                arguments.append(child.to_source(name, indent + 4)
                                 if isinstance(child, OpenXML.Element) else repr(child))
            if self.attrs:
                arguments.append("**" + repr(dict(self.attrs)))
            if not arguments:
                return constructor + "()"
            if not any("\n" in argument for argument in arguments) and \
                    indent + len(constructor) + sum(map(len, arguments)) < 110:
                return constructor + "(" + ", ".join(arguments) + ")"
            padding = " " * (indent + 4)
            return constructor + "(\n" + ",\n".join(padding + a for a in arguments) + "\n" + " " * indent + ")"

    class TagElement(Element):
        tag = None

        def __init__(self, *elems, **attrs):
            super().__init__(self.tag, *elems, **attrs)


OpenXML.base_element = OpenXML.Element
OpenXML.Element.context = OpenXML
OpenXML.TagElement.context = OpenXML
OpenXML.namespace_uris.update({
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
})
from .Vocabulary import register_vocabularies
register_vocabularies(OpenXML)
