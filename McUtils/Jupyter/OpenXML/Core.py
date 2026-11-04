"""Declarative Office Open XML elements (namespace-aware, built on JHTML.ContentXML) and generic Open Packaging
Conventions packaging: parts, content types and relationships.
"""

import copy
import io
import posixpath
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass

from ..JHTML import ContentXML

__all__ = [
    "OpenXML",
    "OpenXMLPart",
    "OpenXMLRelationship",
    "OpenXMLPackage",
]


# --------------------------------------------------------------------------------------------- #
#  elements
# --------------------------------------------------------------------------------------------- #

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
from .Vocabulary import register_vocabularies  # circular on purpose: Vocabulary needs OpenXML defined above
register_vocabularies(OpenXML)


# --------------------------------------------------------------------------------------------- #
#  packaging
# --------------------------------------------------------------------------------------------- #

REL_CONTENT_TYPE = "application/vnd.openxmlformats-package.relationships+xml"


def part_name(name):
    name = str(name).lstrip("/")
    if not name or "\\" in name or posixpath.normpath(name) != name or name.startswith("../"):
        raise ValueError("invalid package part name: " + name)
    return name


@dataclass(frozen=True)
class OpenXMLPart:
    name: str
    content_type: str
    data: object

    def to_bytes(self):
        if isinstance(self.data, OpenXML.Element):
            return self.data.to_bytes()
        if isinstance(self.data, str):
            return self.data.encode("utf-8")
        return bytes(self.data)

    def clone(self):
        return type(self)(self.name, self.content_type,
                          self.data.clone() if isinstance(self.data, OpenXML.Element) else self.data)


@dataclass(frozen=True)
class OpenXMLRelationship:
    id: str
    type: str
    target: str
    target_mode: str = None

    def to_presml(self, context=None):
        return OpenXML.rel.Relationship(Id=self.id, Type=self.type, Target=self.target,
                                       TargetMode=self.target_mode)


class OpenXMLPackage:
    """An OPC package independent of presentation, spreadsheet or word semantics."""
    def __init__(self, parts=(), content_types=None):
        if hasattr(parts, "values"):
            parts = parts.values()
        self.parts = {}
        self.content_types = content_types.clone() if content_types is not None else OpenXML.opc.Types(
            OpenXML.opc.Default(Extension="rels", ContentType=REL_CONTENT_TYPE),
            OpenXML.opc.Default(Extension="xml", ContentType="application/xml")
        )
        for part in parts:
            self.add_part(part.name, part.content_type, part.data)

    def __getitem__(self, name):
        return self.parts[part_name(name)]

    def clone(self):
        return type(self)([p.clone() for p in self.parts.values()], self.content_types)

    def content_type(self, name):
        name = part_name(name)
        overrides, defaults = {}, {}
        for element in self.content_types.elems:
            if not isinstance(element, OpenXML.Element):
                continue
            if element.local_tag == "Override":
                overrides[element.attrs["PartName"].lstrip("/")] = element.attrs["ContentType"]
            elif element.local_tag == "Default":
                defaults[element.attrs["Extension"].lower()] = element.attrs["ContentType"]
        return overrides.get(name, defaults.get(name.rsplit(".", 1)[-1].lower()))

    def add_part(self, name, content_type, data):
        name = part_name(name)
        if name == "[Content_Types].xml":
            raise ValueError("content types are managed separately")
        if not content_type:
            raise ValueError("part requires a content type: " + name)
        if self.content_type(name) != content_type:
            self.content_types.elems = [e for e in self.content_types.elems
                                        if not (isinstance(e, OpenXML.Element)
                                                and e.local_tag == "Override"
                                                and e.attrs["PartName"].lstrip("/") == name)]
            self.content_types.append(OpenXML.opc.Override(
                PartName="/" + name, ContentType=content_type))
        part = OpenXMLPart(name, content_type, data)
        self.parts[name] = part
        return part

    def remove_part(self, name):
        name = part_name(name)
        self.parts.pop(name, None)
        self.content_types.elems = [e for e in self.content_types.elems
                                    if not (isinstance(e, OpenXML.Element)
                                            and e.local_tag == "Override"
                                            and e.attrs["PartName"].lstrip("/") == name)]

    @staticmethod
    def relationships_name(source=None):
        if not source:
            return "_rels/.rels"
        source = part_name(source)
        directory, name = posixpath.split(source)
        return posixpath.join(directory, "_rels", name + ".rels")

    @staticmethod
    def relationship_source(name):
        if name == "_rels/.rels":
            return ""
        directory, leaf = posixpath.split(name)
        if posixpath.basename(directory) != "_rels" or not leaf.endswith(".rels"):
            raise ValueError("not a relationships part: " + name)
        return posixpath.join(posixpath.dirname(directory), leaf[:-5])

    @staticmethod
    def resolve_target(source, target):
        if target.startswith("/"):
            return part_name(target)
        return part_name(posixpath.normpath(posixpath.join(posixpath.dirname(source or ""), target)))

    def relationships(self, source=None):
        part = self.parts.get(self.relationships_name(source))
        if part is None:
            return ()
        root = part.data if isinstance(part.data, OpenXML.Element) else OpenXML.parse(part.to_bytes())
        return tuple(OpenXMLRelationship(e.attrs["Id"], e.attrs["Type"], e.attrs["Target"],
                                         e.attrs.get("TargetMode"))
                     for e in root.elems if isinstance(e, OpenXML.Element))

    def add_relationship(self, source, target, relationship_type, id=None, external=False):
        name = self.relationships_name(source)
        existing = self.relationships(source)
        used = {r.id for r in existing}
        target = str(target) if external else posixpath.relpath(part_name(target), posixpath.dirname(source or "") or ".")
        for relation in existing:
            if relation.type == relationship_type and relation.target == target \
                    and relation.target_mode == ("External" if external else None):
                if id is None or id == relation.id:
                    return relation.id
        if id is None:
            i = 1
            while "rId" + str(i) in used:
                i += 1
            id = "rId" + str(i)
        elif id in used:
            raise ValueError("duplicate relationship ID: " + id)
        relation = OpenXMLRelationship(id, relationship_type, target, "External" if external else None)
        root = self.parts[name].data.clone() if name in self.parts else OpenXML.rel.Relationships()
        root.append(relation.to_presml())
        self.add_part(name, REL_CONTENT_TYPE, root)
        return id

    @classmethod
    def from_file(cls, file):
        if isinstance(file, (bytes, bytearray)):
            file = io.BytesIO(file)
        with zipfile.ZipFile(file) as archive:
            manifest = OpenXML.parse(archive.read("[Content_Types].xml"))
            package = cls(content_types=manifest)
            for name in archive.namelist():
                if name == "[Content_Types].xml" or name.endswith("/"):
                    continue
                content_type = package.content_type(name)
                data = archive.read(name)
                # SVGs and other user-created assets retain their exact bytes.
                if name.endswith((".xml", ".rels")):
                    data = OpenXML.parse(data)
                package.add_part(name, content_type, data)
        return package

    def validate(self):
        """Check package types, relationship targets and explicit relationship references.

        This is an OPC integrity check, not Office schema or rendering validation.
        """
        for name, part in self.parts.items():
            if self.content_type(name) != part.content_type:
                raise ValueError("inconsistent content type: " + name)
            if name.endswith(".rels"):
                source = self.relationship_source(name)
                if source and source not in self.parts:
                    raise ValueError("missing relationship source: " + source)
                relations = self.relationships(source)
                if len({r.id for r in relations}) != len(relations):
                    raise ValueError("duplicate relationship IDs: " + name)
                for relation in relations:
                    if relation.target_mode != "External":
                        target = self.resolve_target(source, relation.target)
                        if target not in self.parts:
                            raise ValueError("missing relationship target: " + target)
            elif isinstance(part.data, OpenXML.Element):
                ids = {r.id for r in self.relationships(name)}
                tree = ET.fromstring(part.to_bytes())
                for element in tree.iter():
                    for attr, value in element.attrib.items():
                        if attr.startswith("{" + OpenXML.namespace_uris["r"] + "}") and value not in ids:
                            raise ValueError("missing relationship " + value + " in " + name)
        for element in self.content_types.elems:
            if isinstance(element, OpenXML.Element) and element.local_tag == "Override" \
                    and element.attrs["PartName"].lstrip("/") not in self.parts:
                raise ValueError("content type references absent part: " + element.attrs["PartName"])
        return self

    def write(self, file, validate=True):
        if validate:
            self.validate()
        with zipfile.ZipFile(file, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            def write_part(name, data):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, data)
            # OPC manifests use the default namespace with unprefixed names.
            # Parsed manifests may acquire prefixed Override children when new
            # parts are added; normalize a copy, preserving the stored objects.
            manifest = self.content_types.clone()
            manifest.attrs = dict(manifest.attrs, xmlns=OpenXML.namespace_uris["opc"])
            for element in manifest.walk():
                element.tag = element.local_tag
            write_part("[Content_Types].xml", manifest.to_bytes())
            for name, part in self.parts.items():
                if name.endswith(".rels") and isinstance(part.data, OpenXML.Element):
                    # Relationship parts likewise use the default namespace: LibreOffice (and
                    # other non-Microsoft consumers) reject prefixed `rel:Relationships`.
                    rels = part.data.clone()
                    rels.attrs = dict(rels.attrs, xmlns=OpenXML.namespace_uris["rel"])
                    for element in rels.walk():
                        element.tag = element.local_tag
                    write_part(name, rels.to_bytes())
                else:
                    write_part(name, part.to_bytes())
        return file

    def to_bytes(self, validate=True):
        buffer = io.BytesIO()
        self.write(buffer, validate=validate)
        return buffer.getvalue()
