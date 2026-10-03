"""Declarative Office Open XML vocabularies and generic OPC packaging."""

from .Elements import OpenXML
from .Packaging import OpenXMLPart, OpenXMLRelationship, OpenXMLPackage

__all__ = ["OpenXML", "OpenXMLPart", "OpenXMLRelationship", "OpenXMLPackage"]
