"""Static JupyterLab Markdown elements built from McUtils HTML.

The inline styles use literal colors so JupyterLab's Markdown sanitizer can
retain them. ``JupyterMarkdownElement.default_theme`` is the shared palette;
each element class owns its ``theme_styles`` mapping for local customization.

Example::

    from McUtils.Jupyter.JHTML import JCard, JAlert

    JCard("Results", title="Calculation", kind="primary").to_widget().display()
    JAlert("Complete", kind="success").to_copy_button().to_widget().display()
"""

from __future__ import annotations

from .HTML import HTML, HTMLManager

__all__ = [
    "JupyterMarkdownElement", "JRow", "JColumn", "JCard", "JAlert",
    "JBadge", "JButton", "JTable",
]


def _resolve(value):
    if isinstance(value, JupyterMarkdownElement):
        return value.to_widget()
    if isinstance(value, tuple):
        return tuple(_resolve(item) for item in value)
    if isinstance(value, list):
        return [_resolve(item) for item in value]
    if isinstance(value, dict):
        return {key: _resolve(item) for key, item in value.items()}
    return value


class JupyterMarkdownElement:
    """A static HTML element recipe rendered on demand.

    The shared ``default_theme`` maps each ``kind`` to literal colors. Each
    subclass defines its own ``theme_styles`` for the HTML parts it renders.
    """

    registry = {}
    default_theme = {
        "default": {
            "background": "#ffffff", "foreground": "#212529",
            "border": "#dee2e6", "accent": "#6c757d", "on_accent": "#ffffff",
        },
        "primary": {
            "background": "#cce5ff", "foreground": "#004085",
            "border": "#b8daff", "accent": "#007bff", "on_accent": "#ffffff",
        },
        "secondary": {
            "background": "#e2e3e5", "foreground": "#383d41",
            "border": "#d6d8db", "accent": "#6c757d", "on_accent": "#ffffff",
        },
        "info": {
            "background": "#d1ecf1", "foreground": "#0c5460",
            "border": "#bee5eb", "accent": "#17a2b8", "on_accent": "#ffffff",
        },
        "success": {
            "background": "#d4edda", "foreground": "#155724",
            "border": "#c3e6cb", "accent": "#28a745", "on_accent": "#ffffff",
        },
        "warning": {
            "background": "#fff3cd", "foreground": "#856404",
            "border": "#ffeeba", "accent": "#ffc107", "on_accent": "#212529",
        },
        "error": {
            "background": "#f8d7da", "foreground": "#721c24",
            "border": "#f5c6cb", "accent": "#dc3545", "on_accent": "#ffffff",
        },
    }
    theme_styles = {}

    @classmethod
    def register(cls, name, element=None):
        if element is not None:
            cls.registry[name] = element
            return element
        def register(element):
            return cls.register(name, element)
        return register

    @classmethod
    def lookup(cls, name):
        return cls.registry[name] if isinstance(name, str) else name

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def _palette(self, kind):
        try:
            return self.default_theme[kind]
        except KeyError as exc:
            raise ValueError(
                f"kind must be one of {', '.join(self.default_theme)}"
            ) from exc

    def _style(self, part, attrs=None, **theme_values):
        """Combine this class's part style, palette values, and caller styles."""
        style = {**self.theme_styles[part], **theme_values}
        attrs = {} if attrs is None else dict(attrs)
        user_style = attrs.pop("style", None)
        if user_style is not None:
            style.update(HTMLManager.manage_styles(user_style).props)
        return {**attrs, "style": style}

    def _widget_function(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement _widget_function")

    def to_widget(self):
        """Render with this element's bound factory method."""
        widget = self._widget_function(
            *(_resolve(arg) for arg in self.args),
            **{key: _resolve(value) for key, value in self.kwargs.items()},
        )
        widget.wrap_display_element = False
        return widget

    def tostring(self, *, prettify=True, **opts):
        return self.to_widget().tostring(prettify=prettify, **opts)

    def to_copy_button(self, label="Copy", button_type=None, **attrs):
        """Build an output-cell copy button for the pretty HTML source."""
        if button_type is None:
            button_type = JButton
            attrs.setdefault("kind", "secondary")
        return self.to_widget().to_copy_button(
            label, button_type=button_type, prettify=True, **attrs
        )

    def display(self):
        return self.to_widget().display()

    def _ipython_display_(self):
        self.to_widget()._ipython_display_()


@JupyterMarkdownElement.register("row")
class JRow(JupyterMarkdownElement):
    """A wrapping horizontal layout."""

    theme_styles = {
        "container": {"display": "flex", "flex_wrap": "wrap"},
    }

    def _widget_function(self, *children, gap="12px", **attrs):
        return HTML.Div(
            *children,
            **self._style("container", attrs, gap=gap),
        )


@JupyterMarkdownElement.register("column")
class JColumn(JupyterMarkdownElement):
    """A flexible column for use in :class:`JRow`."""

    theme_styles = {
        "container": {"min_width": "0"},
    }

    def _widget_function(self, *children, min_width="180px", **attrs):
        return HTML.Div(
            *children,
            **self._style("container", attrs, flex=f"1 1 {min_width}"),
        )


@JupyterMarkdownElement.register("card")
class JCard(JupyterMarkdownElement):
    """A bordered card whose status colors affect only its title."""

    theme_styles = {
        "container": {"border_radius": "2px", "overflow": "hidden"},
        "title": {"font_weight": "600", "padding": "10px 14px"},
        "body": {"padding": "14px"},
        # Optional per-kind body overrides; the defaults inherit all colors.
        "body_kinds": {},
    }

    def _widget_function(self, *children, title=None, kind="default", **attrs):
        palette = self._palette(kind)
        body_style = {
            **self.theme_styles["body"],
            **self.theme_styles["body_kinds"].get(kind, {}),
        }
        body = HTML.Div(*children, style=body_style)
        if title is None:
            parts = (body,)
        else:
            title_style = {
                **self.theme_styles["title"],
                "border_bottom": f"1px solid {palette['border']}",
            }
            if kind != "default":
                title_style.update(
                    background_color=palette["background"],
                    color=palette["foreground"],
                )
            parts = (HTML.Div(title, style=title_style), body)
        return HTML.Div(
            *parts,
            **self._style(
                "container", attrs,
                border=f"1px solid {self._palette('default')['border']}",
            ),
        )


@JupyterMarkdownElement.register("alert")
class JAlert(JupyterMarkdownElement):
    """A notice using JupyterLab classes where they exist."""

    jupyter_kinds = {
        "info": "alert-info",
        "success": "alert-success",
        "warning": "alert-warning",
        "error": "alert-danger",
    }

    theme_styles = {
        "container": {
            "padding": "10px 14px", "border_radius": "2px",
            "margin_bottom": "1em",
        },
        "jupyter_variant": {},
    }

    def _widget_function(self, *children, kind="info", use_jupyter_styles=True, **attrs):
        palette = self._palette(kind)
        attrs.setdefault("role", "alert")
        if use_jupyter_styles:
            classes = ["alert"]
            jupyter_class = self.jupyter_kinds.get(kind)
            if jupyter_class is not None:
                classes.append(jupyter_class)
            classes.extend(HTMLManager.manage_class(attrs.pop("cls", None)))
            classes.extend(HTMLManager.manage_class(attrs.pop("class", None)))
            attrs["cls"] = list(dict.fromkeys(classes))
            if jupyter_class is not None:
                # JupyterLab supplies the padding, border, radius, and colors.
                return HTML.Div(*children, **attrs)
            # Primary, secondary, and default have no JupyterLab variant.
            return HTML.Div(
                *children,
                **self._style(
                    "jupyter_variant", attrs,
                    background_color=palette["background"],
                    color=palette["foreground"],
                    border_color=palette["border"],
                ),
            )
        return HTML.Div(
            *children,
            **self._style(
                "container", attrs,
                background_color=palette["background"],
                color=palette["foreground"],
                border=f"1px solid {palette['border']}",
                border_left=f"4px solid {palette['accent']}",
            ),
        )


@JupyterMarkdownElement.register("badge")
class JBadge(JupyterMarkdownElement):
    """A compact, solid status label."""

    theme_styles = {
        "container": {
            "display": "inline-block", "padding": "2px 7px",
            "border_radius": "999px", "font_size": "0.85em",
            "font_weight": "600",
        },
    }

    def _widget_function(self, text, kind="info", **attrs):
        palette = self._palette(kind)
        return HTML.Span(
            text,
            **self._style(
                "container", attrs,
                background_color=palette["accent"],
                color=palette["on_accent"],
            ),
        )


@JupyterMarkdownElement.register("button")
class JButton(JupyterMarkdownElement):
    """A static, Bootstrap 4 colored HTML button."""

    theme_styles = {
        "container": {
            "border_radius": "4px", "padding": "6px 12px",
            "cursor": "pointer", "font_weight": "400",
        },
    }

    def _widget_function(self, label, *, kind="primary", **attrs):
        if "on_click" in attrs or "event_handlers" in attrs:
            raise ValueError("JButton is static HTML and does not accept Python callbacks")
        palette = self._palette(kind)
        attrs.setdefault("type", "button")
        return HTML.Button(
            label,
            **self._style(
                "container", attrs,
                background_color=palette["accent"],
                color=palette["on_accent"],
                border=f"1px solid {palette['accent']}",
            ),
        )


@JupyterMarkdownElement.register("table")
class JTable(JupyterMarkdownElement):
    """A table with optional headers and status colored headings."""

    theme_styles = {
        "container": {"width": "100%", "border_collapse": "collapse"},
        "heading": {"padding": "6px 10px", "text_align": "left", "font_weight": "600"},
        "cell": {"padding": "6px 10px", "text_align": "left"},
    }

    def _widget_function(self, rows, *, headers=None, kind="default", **attrs):
        palette = self._palette(kind)
        cell_style = {
            **self.theme_styles["cell"],
            "border_bottom": f"1px solid {palette['border']}",
        }
        table_rows = []
        if headers is not None:
            heading_style = {
                **self.theme_styles["heading"],
                "background_color": palette["background"],
                "color": palette["foreground"],
                "border_bottom": f"1px solid {palette['border']}",
            }
            table_rows.append(HTML.TableRow(*(
                HTML.TableHeading(value, style=heading_style)
                for value in headers
            )))
        table_rows.extend(
            HTML.TableRow(*(
                HTML.TableItem(value, style=cell_style) for value in values
            ))
            for values in rows
        )
        neutral = self._palette("default")
        return HTML.Table(
            *table_rows,
            **self._style(
                "container", attrs,
                color=neutral["foreground"],
                background_color=neutral["background"],
            ),
        )
