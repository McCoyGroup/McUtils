"""
Report templates: what a report on a given kind of object should contain, so that a model only has to write what
the template leaves open.

A template with fixed ``sections`` and a single source needs no model to choose content or outline. Templates are
found by `find_report_template`: the registry (by class, along the MRO), then the ``report_template`` attribute of the
source's readout interface (so a package can attach a template without McUtils importing it), then the generic one.
"""

__all__ = ["ReportTemplate", "register_report_template", "find_report_template", "template_menu"]


class ReportTemplate:
    """
    :cvar name: the template's name (recorded in the document's meta)
    :cvar sections: ``[(heading, [section names])]``; empty means there is no fixed outline
    :cvar optional: sections that may be offered to the model on top of the fixed ones
    :cvar locked: source-section names (``"overview"``; ``"normal_modes"`` also covers ``normal_modes.frequencies``) whose
        blocks the model can't edit, move or remove once `apply_template` has built them
    :cvar locked_headings: template headings whose heading block and every block under it are locked the same way
    :cvar captions: whether the model writes captions
    :cvar section_text: whether the model writes section prose
    :cvar summary: whether the model writes a summary
    """
    name = "generic"
    sections = []
    optional = []
    locked = []
    locked_headings = []
    captions = True
    section_text = True
    summary = True

    def applies_to(self, source):
        """Whether this template suits a `ReportSource` (checked after the class lookup)."""
        return True

    def locks(self, heading, section):
        """Whether the readout block for ``section`` built under ``heading`` is locked."""
        return heading in self.locked_headings or any(section == n or section.startswith(n + ".") for n in self.locked)

    def caption_for(self, handle, section, source):
        """A fixed caption for a block (used when the model doesn't write captions), or ``None``."""
        return None

    @property
    def is_fixed(self):
        return bool(self.sections)

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r})"


_TEMPLATES = {}


def register_report_template(target, template=None):
    """Register ``template`` (a `ReportTemplate` subclass) for ``target`` (a class or dotted name). Usable as a decorator."""
    def reg(template):
        key = target if isinstance(target, str) else f"{target.__module__}.{target.__qualname__}"
        _TEMPLATES[key] = template
        return template
    return reg if template is None else reg(template)


def _instance(t):
    return t() if isinstance(t, type) else t


def find_report_template(source):
    """The `ReportTemplate` for a `ReportSource`; the generic template if nothing else applies."""
    for cls in type(source.obj).__mro__:
        full = f"{cls.__module__}.{cls.__qualname__}"
        for key, template in _TEMPLATES.items():
            if full == key or full.endswith("." + key):
                t = _instance(template)
                if t.applies_to(source):
                    return t
    try:
        attached = getattr(source.interface(), "report_template", None)
    except Exception:
        attached = None
    if attached is not None:
        t = _instance(attached)
        if t.applies_to(source):
            return t
    return ReportTemplate()


def template_menu(source):
    """
    What the report template for a `ReportSource` offers, with each section's description and availability:
    ``{name, captions, outline: [{heading, sections: [row]}], optional: [row]}``, where ``row`` is
    ``{name, title, description, available, reason?}``. A part of a section (``normal_modes.frequencies``) takes the
    section's row with ``part`` added. ``outline`` is empty when the template has no fixed outline.
    """
    template = find_report_template(source)
    rows = {r["name"]: r for r in source.sections()}

    def row(name):
        base, _, part = name.partition(".")
        r = rows.get(base)
        if r is None:
            return {"name": name, "title": name, "description": "", "available": False, "reason": "not a section of this source"}
        out = {"name": name, "title": r.get("title") or base, "description": r.get("description") or "",
               "available": bool(r.get("available", True))}
        if part:
            out["part"] = part
        if r.get("reason") and not out["available"]:
            out["reason"] = r["reason"]
        return out

    return {"name": template.name, "captions": bool(template.captions),
            "locked": list(template.locked) + [f"everything under {h!r}" for h in template.locked_headings],
            "outline": [{"heading": h, "sections": [row(n) for n in names]} for h, names in template.sections],
            "optional": [row(n) for n in template.optional]}
