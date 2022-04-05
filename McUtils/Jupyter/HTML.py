from xml.etree import ElementTree
import weakref

__all__ = [
    "HTML",
    "CSS"
]

class CSS:
    """
    Defines a holder for CSS properties
    """
    def __init__(self, *selectors, **props):
        self.selectors = selectors
        self.props = self.canonicalize_props(props)
    @classmethod
    def construct(cls,
                  *selectors,
                  background=None,
                  background_attachment=None,
                  background_color=None,
                  background_image=None,
                  background_position=None,
                  background_repeat=None,
                  border=None,
                  border_bottom=None,
                  border_bottom_color=None,
                  border_bottom_style=None,
                  border_bottom_width=None,
                  border_color=None,
                  border_left=None,
                  border_left_color=None,
                  border_left_style=None,
                  border_left_width=None,
                  border_right=None,
                  border_right_color=None,
                  border_right_style=None,
                  border_right_width=None,
                  border_style=None,
                  border_top=None,
                  border_top_color=None,
                  border_top_style=None,
                  border_top_width=None,
                  border_width=None,
                  clear=None,
                  clip=None,
                  color=None,
                  cursor=None,
                  display=None,
                  filter=None,
                  float=None,
                  font=None,
                  font_family=None,
                  font_size=None,
                  font_variant=None,
                  font_weight=None,
                  height=None,
                  left=None,
                  letter_spacing=None,
                  line_height=None,
                  list_style=None,
                  list_style_image=None,
                  list_style_position=None,
                  list_style_type=None,
                  margin=None,
                  margin_bottom=None,
                  margin_left=None,
                  margin_right=None,
                  margin_top=None,
                  overflow=None,
                  padding=None,
                  padding_bottom=None,
                  padding_left=None,
                  padding_right=None,
                  padding_top=None,
                  page_break_after=None,
                  page_break_before=None,
                  position=None,
                  text_align=None,
                  text_decoration=None,
                  text_indent=None,
                  text_transform=None,
                  top=None,
                  vertical_align=None,
                  visibility=None,
                  width=None,
                  z_index=None,
                  **props
                  ):
        """
        Provides a convenience constructor for systems with autocompletions

        :param selectors:
        :type selectors:
        :param background:
        :type background:
        :param background_attachment:
        :type background_attachment:
        :param background_color:
        :type background_color:
        :param background_image:
        :type background_image:
        :param background_position:
        :type background_position:
        :param background_repeat:
        :type background_repeat:
        :param border:
        :type border:
        :param border_bottom:
        :type border_bottom:
        :param border_bottom_color:
        :type border_bottom_color:
        :param border_bottom_style:
        :type border_bottom_style:
        :param border_bottom_width:
        :type border_bottom_width:
        :param border_color:
        :type border_color:
        :param border_left:
        :type border_left:
        :param border_left_color:
        :type border_left_color:
        :param border_left_style:
        :type border_left_style:
        :param border_left_width:
        :type border_left_width:
        :param border_right:
        :type border_right:
        :param border_right_color:
        :type border_right_color:
        :param border_right_style:
        :type border_right_style:
        :param border_right_width:
        :type border_right_width:
        :param border_style:
        :type border_style:
        :param border_top:
        :type border_top:
        :param border_top_color:
        :type border_top_color:
        :param border_top_style:
        :type border_top_style:
        :param border_top_width:
        :type border_top_width:
        :param border_width:
        :type border_width:
        :param clear:
        :type clear:
        :param clip:
        :type clip:
        :param color:
        :type color:
        :param cursor:
        :type cursor:
        :param display:
        :type display:
        :param filter:
        :type filter:
        :param float:
        :type float:
        :param font:
        :type font:
        :param font_family:
        :type font_family:
        :param font_size:
        :type font_size:
        :param font_variant:
        :type font_variant:
        :param font_weight:
        :type font_weight:
        :param height:
        :type height:
        :param left:
        :type left:
        :param letter_spacing:
        :type letter_spacing:
        :param line_height:
        :type line_height:
        :param list_style:
        :type list_style:
        :param list_style_image:
        :type list_style_image:
        :param list_style_position:
        :type list_style_position:
        :param list_style_type:
        :type list_style_type:
        :param margin:
        :type margin:
        :param margin_bottom:
        :type margin_bottom:
        :param margin_left:
        :type margin_left:
        :param margin_right:
        :type margin_right:
        :param margin_top:
        :type margin_top:
        :param overflow:
        :type overflow:
        :param padding:
        :type padding:
        :param padding_bottom:
        :type padding_bottom:
        :param padding_left:
        :type padding_left:
        :param padding_right:
        :type padding_right:
        :param padding_top:
        :type padding_top:
        :param page_break_after:
        :type page_break_after:
        :param page_break_before:
        :type page_break_before:
        :param position:
        :type position:
        :param text_align:
        :type text_align:
        :param text_decoration:
        :type text_decoration:
        :param text_indent:
        :type text_indent:
        :param text_transform:
        :type text_transform:
        :param top:
        :type top:
        :param vertical_align:
        :type vertical_align:
        :param visibility:
        :type visibility:
        :param width:
        :type width:
        :param z_index:
        :type z_index:
        :param props:
        :type props:
        :return:
        :rtype:
        """
        common_props = dict(
            background=background,
            background_attachment=background_attachment,
            background_color=background_color,
            background_image=background_image,
            background_position=background_position,
            background_repeat=background_repeat,
            border=border,
            border_bottom=border_bottom,
            border_bottom_color=border_bottom_color,
            border_bottom_style=border_bottom_style,
            border_bottom_width=border_bottom_width,
            border_color=border_color,
            border_left=border_left,
            border_left_color=border_left_color,
            border_left_style=border_left_style,
            border_left_width=border_left_width,
            border_right=border_right,
            border_right_color=border_right_color,
            border_right_style=border_right_style,
            border_right_width=border_right_width,
            border_style=border_style,
            border_top=border_top,
            border_top_color=border_top_color,
            border_top_style=border_top_style,
            border_top_width=border_top_width,
            border_width=border_width,
            clear=clear,
            clip=clip,
            color=color,
            cursor=cursor,
            display=display,
            filter=filter,
            float=float,
            font=font,
            font_family=font_family,
            font_size=font_size,
            font_variant=font_variant,
            font_weight=font_weight,
            height=height,
            left=left,
            letter_spacing=letter_spacing,
            line_height=line_height,
            list_style=list_style,
            list_style_image=list_style_image,
            list_style_position=list_style_position,
            list_style_type=list_style_type,
            margin=margin,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            overflow=overflow,
            padding=padding,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            page_break_after=page_break_after,
            page_break_before=page_break_before,
            position=position,
            text_align=text_align,
            text_decoration=text_decoration,
            text_indent=text_indent,
            text_transform=text_transform,
            top=top,
            vertical_align=vertical_align,
            visibility=visibility,
            width=width,
            z_index=z_index
        )
        for k, v in common_props.items():
            if v is not None:
                props[k] = v
        return cls(*selectors, **props)
    @classmethod
    def canonicalize_props(cls, props):
        return {k.replace("_", "-"):v for k,v in props.items()}
    @classmethod
    def parse(cls, sty):
        header = sty.split("{", 1)[0]
        if len(header) == len(sty): # inline styles
            chunks = [x.strip() for x in sty.split(";")]
            splits = [x.split(":") for x in chunks if len(x) > 0]
            return cls(**{k.strip(): v.strip() for k, v in splits})
        else:
            splits = [x.split("{") for x in sty.split("}")]
            styles = []
            for key, vals in splits:
                key = [x.strip() for x in key.split(",")]
                chunks = [x.strip() for x in vals.split(";")]
                pairs = [x.split(":") for x in chunks if len(x) > 0]
                styles.append(
                    cls(*key, **{k.strip(): v.strip() for k, v in pairs})
                )
                return styles

    def tostring(self):
        if len(self.selectors) > 0:
            return "{sel} {{\n  {body}\n}}".format(
                sel=",".join(self.selectors),
                body="\n  ".join("{k}:{v};".format(k=k,v=v) for k,v in self.props.items())
            )
        else:
            return " ".join("{k}:{v};".format(k=k,v=v) for k,v in self.props.items())

class HTML:
    """
    A namespace for holding various HTML attributes
    """
    @classmethod
    def expose(cls):
        g = globals()
        for x in cls.__dict__:
            if isinstance(x, type):
                g[x.__name__] = x
    class XMLElement:
        """
        Convenience API for ElementTree
        """

        def __init__(self, tag, *elems, on_update=None, **attrs):
            self.tag = tag
            self._elems = list(elems[0] if len(elems) == 1 and isinstance(elems[0], (list, tuple)) else elems)
            self._elem_view = None
            if 'cls' in attrs:
                attrs['class'] = attrs['cls']
                del attrs['cls']
            self._attrs = attrs
            self._attr_view = None
            self._parents = weakref.WeakSet()
            self._tree_cache = None
            self.on_update = on_update if on_update is not None else lambda *s:None
        @property
        def attrs(self):
            if self._attr_view is None:
                self._attr_view = self._attrs.copy()
            return self._attr_view
        @attrs.setter
        def attrs(self, attrs):
            self._attrs = attrs
            self._attr_view = None
            self._invalidate_cache()
            self.on_update(self, 'attributes', attrs)
        @property
        def elems(self):
            if self._elem_view is None:
                self._elem_view = tuple(self._elems)
            return self._elem_view
        @elems.setter
        def elems(self, elems):
            self._elems = elems
            self._elem_view = None
            self._invalidate_cache()
            self.on_update(self)
            self.on_update(self, 'elements', elems)

        def _invalidate_cache(self):
            if self._tree_cache is not None:
                self._tree_cache = None
                for p in tuple(self._parents):
                    p._invalidate_cache()
                    self._parents.remove(p)
        def __getitem__(self, item):
            if isinstance(item, str):
                return self._attrs[item]
            else:
                return self._elems[item]
        def __setitem__(self, item, value):
            if isinstance(item, str):
                self._attrs[item] = value
                self._attr_view = None
            else:
                self._elems[item] = value
                self._elem_view = None
            self._invalidate_cache()
            self.on_update(self, item, value)

        @property
        def tree(self):
            return self.to_tree()
        def to_tree(self, root=None, parent=None):
            if parent is not None:
                self._parents.add(parent)
            if self._tree_cache is None:
                if root is None:
                    root = ElementTree.Element('root')
                attrs = self.attrs
                _copied = False
                if 'style' in attrs:
                    styles = attrs['style']
                    if hasattr(styles, 'items'):
                        styles = CSS(**styles)
                    if hasattr(styles, 'tostring'):
                        if not _copied:
                            attrs = attrs.copy()
                            _copied = True
                        attrs['style'] = styles.tostring()
                if 'class' in attrs:
                    if not isinstance(attrs['class'], str):
                        if not _copied:
                            attrs = attrs.copy()
                            _copied = True
                        try:
                            iter(attrs['class'])
                        except TypeError:
                            attrs['class'] = str(attrs['class'])
                        else:
                            attrs['class'] = " ".join(str(c) for c in attrs['class'])
                my_el = ElementTree.SubElement(root, self.tag, attrs)
                if all(isinstance(e, str) for e in self.elems):
                    my_el.text = "\n".join(self.elems)
                else:
                    for elem in self.elems:
                        if hasattr(elem, 'to_tree'):
                            elem.to_tree(root=my_el, parent=self)
                        elif hasattr(elem, 'modify'):
                            elem.modify().to_tree(root=my_el, parent=self)
                        elif isinstance(elem, ElementTree.Element):
                            my_el.append(elem)
                        elif isinstance(elem, (str, int, float, CSS)):
                            elem = str(elem)
                            kids = list(my_el)
                            if len(kids) > 0:
                                if kids[-1].tail is None:
                                    kids[-1].tail = elem
                                else:
                                    kids[-1].tail += "\n"+elem
                            else:
                                my_el.text = elem
                        elif hasattr(elem, 'to_widget'):
                            raise ValueError("can't convert {} to pure HTML. It looks like a `JupyterHTMLWrapper` so look for the appropriate `JHTML` subclass.".format(elem))
                        else:
                            raise ValueError("don't know what to do with {}".format(elem))
                self._tree_cache = my_el
            elif root is not None:
                if self._tree_cache not in root:
                    root.append(self._tree_cache)
            return self._tree_cache
        def tostring(self):
            return "\n".join(s.decode() for s in ElementTree.tostringlist(self.to_tree()))
        def __repr__(self):
            return "{}({}, {})".format(type(self).__name__, self.elems, self.attrs)
        def _repr_html_(self):
            return self.tostring()
        def display(self):
            from .HTMLWidgets import JupyterHTMLWrapper
            return JupyterHTMLWrapper.get_display_api().display(JupyterHTMLWrapper.get_display_api().HTML(self.tostring()))
        def make_class_list(self):
            self.attrs['class'] = self.attrs['class'].split()
        def add_class(self, *cls, copy=True):
            return HTML.ClassAdder(self, cls, copy=copy).modify()
        def remove_class(self, *cls, copy=True):
            return HTML.ClassRemover(self, cls, copy=copy).modify()
        def add_styles(self, copy=True, **sty):
            return HTML.StyleAdder(self, copy=copy, **sty).modify()

        def _find_child_node(self, etree):
            from collections import deque
            # BFS to try to find the element that matches
            remaining = deque()
            remaining.append(self)
            while remaining:
                elem = remaining.popleft()
                if isinstance(elem, HTML.ElementModifier):
                    elem = elem.modify()
                if isinstance(elem, HTML.XMLElement):
                    if etree == elem.tree:
                        return elem
                    else:
                        for e in elem.elems:
                            remaining.append(e)

        def find(self, path, find_element=True):
            base = self.tree.find(path)
            if find_element and base is not None:
                new = self._find_child_node(base)
                if new is not None:
                    base = new
            return base
        def findall(self, path, find_element=True):
            bases = self.tree.findall(path)
            if find_element:
                new = []
                for b in bases:
                    newb = self._find_child_node(b)
                    if newb is not None:
                        new.append(newb)
                    else:
                        new.append(b)
                bases = new
            return bases
        def iterfind(self, path, find_element=True):
            bases = self.tree.iterfind(path)
            for b in bases:
                if find_element:
                    newb = self._find_child_node(b)
                    if newb is not None:
                        yield newb
                    else:
                        yield b
                else:
                    yield b
        def find_by_id(self, id, mode='first', parent=None, find_element=True):
            fn = {
                'first':self.find,
                'all':self.findall,
                'iter':self.iterfind
            }[mode]
            sel = ".//*[@id='{id}']{parents}".format(id=id, parents="" if parent is None else ('.'+'.'*parent))
            return fn(sel, find_element=find_element)

        def copy(self):
            import copy
            base = copy.copy(self)
            base.attrs = base.attrs.copy()
            base._tree_cache = None
            base._parents = weakref.WeakSet()
            return base
    class ElementModifier:
        def __init__(self, my_el, copy=False):
            self.el = my_el
            self.needs_copy = copy
            self._parents = None
            self._tree_cache = None
        def modify(self):
            if self.needs_copy:
                el = self.el.copy()
            else:
                el = self.el
            return el
        def tostring(self):
            return self.modify().tostring()
        def _repr_html_(self):
            return self.tostring()
        def copy(self):
            import copy
            new = copy.copy(self)
            new.el = new.el.copy()
        def add_class(self, *cls, copy=True):
            return HTML.ClassAdder(self, cls=cls, copy=copy)
        def remove_class(self, *cls, copy=True):
            return HTML.ClassRemover(self, cls=cls, copy=copy)
        def add_styles(self, copy=True, **sty):
            return HTML.StyleAdder(self, copy=copy, **sty)
    class ClassAdder(ElementModifier):
        cls = None
        def __init__(self, el, cls=None, copy=True):
            if cls is None:
                cls = self.cls
            if isinstance(cls, str):
                cls = cls.split()
            self.cls = cls
            super().__init__(el, copy=copy)
        def modify(self):
            if isinstance(self.el, HTML.ElementModifier):
                el = self.el.modify()
            else:
                if self.needs_copy:
                    el = self.el.copy()
                else:
                    el = self.el
            if 'class' in el.attrs:
                if isinstance(el['class'], str):
                    el.make_class_list()
                class_list = list(el['class'])
                for cls in self.cls:
                    cls = str(cls)
                    if cls not in class_list:
                        class_list.append(cls)
                el['class'] = tuple(class_list)
            else:
                el['class'] = self.cls
            return el
        def __repr__(self):
            return "{}({}, {})".format(type(self).__name__, self.el, self.cls)
    class ClassRemover(ElementModifier):
        cls = None
        def __init__(self, el, cls=None, copy=True):
            if cls is None:
                cls = self.cls
            if isinstance(cls, str):
                cls = cls.split()
            self.cls = cls
            super().__init__(el, copy=copy)
        def modify(self):
            if isinstance(self.el, HTML.ElementModifier):
                el = self.el.modify()
            else:
                if self.needs_copy:
                    el = self.el.copy()
                else:
                    el = self.el
            if 'class' in el.attrs:
                if isinstance(el['class'], str):
                    el.make_class_list()
                class_list = list(el['class'])
                for cls in self.cls:
                    cls = str(cls)
                    try:
                        class_list.remove(cls)
                    except ValueError:
                        pass
                el['class'] = tuple(class_list)
            else:
                el['class'] = self.cls
            return el
        def __repr__(self):
            return "{}({}, {})".format(type(self).__name__, self.el, self.cls)
    class StyleAdder(ElementModifier):
        def __init__(self, el, copy=True, **styles):
            self.styles = styles
            super().__init__(el, copy=copy)
        def modify(self):
            if isinstance(self.el, HTML.ElementModifier):
                el = self.el.modify()
            else:
                if self.needs_copy:
                    el = self.el.copy()
                else:
                    el = self.el

            if 'style' in el.attrs:
                style = el.attrs['style']
                if isinstance(style, str):
                    style = CSS.parse(style)
                else:
                    style = style.copy()
                style.props = dict(style.props, **self.styles)
                el.attrs['style'] = style
            else:
                el.attrs['style'] = CSS(**self.styles)
            return el
        def __repr__(self):
            return "{}({}, {})".format(type(self).__name__, self.el, self.styles)

    class TagElement(XMLElement):
        tag = None
        def __init__(self, *elems, **attrs):
            super().__init__(self.tag, *elems, **attrs)
    class Nav(TagElement): tag='nav'
    class Anchor(TagElement): tag='a'
    class Text(TagElement): tag='p'
    class Div(TagElement): tag='div'
    class Heading(TagElement): tag='h1'
    class SubHeading(TagElement): tag='h2'
    class SubsubHeading(TagElement): tag='h3'
    class SubsubsubHeading(TagElement): tag='h4'
    class Small(TagElement): tag='small'
    class Bold(TagElement): tag='b'
    class Italic(TagElement): tag='i'
    class Image(TagElement): tag='img'
    class ListItem(TagElement): tag='li'
    class BaseList(TagElement):
        def __init__(self, *elems, item_attributes=None, **attrs):
            if item_attributes is None:
                item_attributes = {}
            elems = [HTML.ListItem(x, **item_attributes) if not isinstance(x, HTML.ListItem) else x for x in elems]
            super().__init__(*elems, **attrs)
    class List(BaseList): tag='ul'
    class NumberedList(BaseList): tag='ol'
    class Pre(TagElement): tag='pre'
    class Style(TagElement): tag='style'
    class Script(TagElement): tag='script'
    class Span(TagElement): tag='span'
    class Button(TagElement): tag='button'
    class TableRow(TagElement): tag='tr'
    class TableHeading(TagElement): tag='th'
    class TableItem(TagElement): tag='td'
    class Table(TagElement):
        tag = 'table'
        def __init__(self, *rows, headers=None, **attrs):
            if len(rows) == 1 and isinstance(rows[0], (list, tuple)):
                rows = rows[0]
            rows = [
                HTML.TableRow(
                    [HTML.TableItem(y) if not isinstance(y, HTML.TableItem) else y for y in x]
                ) if not isinstance(x, HTML.TableRow) else x for x in rows
            ]
            if headers is not None:
                rows = [
                    HTML.TableRow([HTML.TableHeading(x) if not isinstance(x, HTML.TableHeading) else x for x in headers])
                ] + rows
            super().__init__(rows, **attrs)

    class Canvas(TagElement): tag='canvas'

    _cls_map = None
    @classmethod
    def get_class_map(cls):
        if cls._cls_map is None:
            cls._cls_map = {}
            for v in cls.__dict__.values():
                if isinstance(v, type) and hasattr(v, 'tag'):
                    cls._cls_map[v.tag] = v
        return cls._cls_map

    @classmethod
    def convert(cls, etree:ElementTree.Element):
        children = [cls.convert(x) for x in etree]
        text = etree.text
        tail = etree.tail

        elems = (
                ([text] if text is not None else [])
                + children
                + (list(tail) if tail is not None else [])
        )

        tag = etree.tag
        map = cls.get_class_map()
        try:
            tag_class = map[tag]
        except KeyError:
            tag_class = lambda *es,**ats:HTML.XMLElement(tag, *es, **ats)

        attrs = {} if etree.attrib is None else etree.attrib

        return tag_class(*elems, **attrs)

    @classmethod
    def parse(cls, str):
        etree = ElementTree.fromstring(str)
        return cls.convert(etree)