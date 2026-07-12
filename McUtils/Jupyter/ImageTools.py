
import uuid
import numpy as np
import re
import functools
import base64
import io
from .. import Devutils as dev
from . import JHTML
from .JHTML import CSS

__all__ = ['DisplayImage']


class DisplayImage:
    def __init__(self, figure, format,
                 plot_range=None, scaling_factor=None,
                 splits=None, postdraw=None,
                 include_save_buttons=False, id=None):
        if isinstance(figure, str):
            self.figure = None
            self._raw_text = figure
        else:
            self.figure = figure
            self._raw_text = None
        self._text = None
        self.plot_range = plot_range
        self.scaling_factor = scaling_factor
        self.splits = splits
        self.postdraw = postdraw
        self.fmt = format
        if id is None:
            id = "rdkit-" + str(uuid.uuid4())[:6]
        self.id = id
        self.include_save_buttons = include_save_buttons

    @classmethod
    def split_string_by_segments(cls, text, split_dict):
        chunk_iter = 0
        chunks = []
        flat_splits = []
        for key, splits in sorted(split_dict.items()):
            for i, p in enumerate(splits):
                flat_splits.append((f"{key}_{i}", p))
        for lab, (start, end) in sorted(flat_splits, key=lambda ks :ks[1][0]):
            chunks.append((None, text[chunk_iter:start]))
            chunks.append((lab, text[start:end]))
            chunk_iter = end
        if chunk_iter > 0 and chunk_iter < len(text):
            chunks.append((None, text[chunk_iter:]))
        return chunks

    @classmethod
    def _path_addition_function(cls, xml_modifier):
        def create_new_element(t):
            uuh = JHTML.HTML.parse(t)
            new_mod = xml_modifier(uuh)
            if not isinstance(new_mod, str):
                new_mod = new_mod.tostring()
            return new_mod

        return create_new_element

    @classmethod
    def _text_addition_function(cls, text, mode='svg', font_options=None, **modifiers):
        if mode == 'text':
            def modify_text_element(parsed_elem):
                opts = parsed_elem.attrs | modifiers
                path: str = opts.pop('d', None)
                path = path.replace("M", "").replace("Q", "").replace("L", "").replace(",", "")
                centroid = np.average(np.array(path.split()).astype(float).reshape(-1, 2), axis=0)
                x, y = centroid
                return JHTML.HTML.XMLElement("text", text, x=f"{x:.1f}", y=f"{y:.1f}", **opts)
        else:
            if font_options is None:
                font_options = {}
            text_path = cls._text_to_path(text, **font_options)

            def modify_text_element(parsed_elem):
                opts = parsed_elem.attrs | modifiers
                path: str = opts.pop('d', None)
                path = path.replace("M", "").replace("Q", "").replace("L", "").replace(",", "")
                verts = np.array(path.split()).astype(float).reshape(-1, 2)
                bbox = (
                    (np.min(verts[:, 0]), np.max(verts[:, 0])),
                    (np.min(verts[:, 1]), np.max(verts[:, 1]))
                )
                d = cls._path_to_svg(text_path, bbox)
                return JHTML.HTML.XMLElement("path", d=d, **opts)
        return cls._path_addition_function(modify_text_element)
    @classmethod
    def _text_to_path(cls, text, **font_opts):
        from matplotlib.textpath import TextPath
        from matplotlib.font_manager import FontProperties
        fp = FontProperties(**font_opts)
        return TextPath((0, 0), text, prop=fp)
    @classmethod
    def _path_to_svg(cls, path,
                     target_bbox: tuple[tuple[float, float], tuple[float, float]],
                     base_height=None,
                     y_flip: bool = True):
        from matplotlib.path import Path
        # Matplotlib path code → SVG command mapping
        _CMD_MAP = {
            Path.MOVETO: "M",
            Path.LINETO: "L",
            Path.CURVE3: "Q",  # quadratic Bézier
            Path.CURVE4: "C",  # cubic Bézier
            Path.CLOSEPOLY: "Z",
        }
        # Number of vertices consumed by each code (including the "current" vertex)
        _VERT_COUNT = {
            Path.MOVETO: 1,
            Path.LINETO: 1,
            Path.CURVE3: 2,  # 1 control + 1 end
            Path.CURVE4: 3,  # 2 controls + 1 end
            Path.CLOSEPOLY: 0,  # vertex is ignored
        }

        verts = np.asarray(path.vertices, dtype=float)
        bbox_init = (
            (np.min(verts[:, 0]), np.max(verts[:, 0])),
            (np.min(verts[:, 1]), np.max(verts[:, 1]))
        )
        dims_init = (
            bbox_init[0][1] - bbox_init[0][0],
            bbox_init[1][1] - bbox_init[1][0],
        )
        codes = path.codes if path.codes is not None else (
                [Path.MOVETO] + [Path.LINETO] * (len(verts) - 1)
        )

        if y_flip:
            h = dims_init[1] if base_height is None else base_height
            verts = verts.copy()
            verts[:, 1] = h - verts[:, 1]

        dims_target = (
            target_bbox[0][1] - target_bbox[0][0],
            target_bbox[1][1] - target_bbox[1][0],
        )
        scaling = max(np.array(dims_target) / np.array(dims_init))

        verts = (
                (verts - np.array([[bbox_init[0][0], bbox_init[1][0]]])) * scaling
                + np.array([[target_bbox[0][0], target_bbox[1][0]]])
        )

        parts = []
        i = 0
        while i < len(codes):
            code = codes[i]

            if code == Path.STOP:
                i += 1
                continue

            cmd = _CMD_MAP.get(code)
            if cmd is None:
                i += 1
                continue

            if code == Path.CLOSEPOLY:
                parts.append("Z")
                i += 1
                continue

            n = _VERT_COUNT[code]
            seg_verts = verts[i: i + n]
            coord_str = " ".join(f"{x:.6g},{y:.6g}" for x, y in seg_verts)
            parts.append(f"{cmd} {coord_str}")
            i += n

        return " ".join(parts)

    multivalue_attrs = {'class'}
    @classmethod
    def _prep_svg_val(cls, attr, old, val):
        # TODO: handle styles
        if attr == 'style':
            if len(old) > 0:
                if isinstance(val, str):
                    val = CSS.parse(val)
                else:
                    val = CSS(**val)
                old = CSS.parse(old)
                val = CSS(**(old.props|val.props)).tostring()
            elif isinstance(val, dict):
                val = CSS(**val).tostring()
        else:
            if isinstance(val, str):
                if attr in cls.multivalue_attrs:
                    if len(old) > 0:
                        val = old + " " + val
            else:
                val = val(old)
        return val
    @classmethod
    def _apply_attr_tf(cls, attr, rest, value):
        if rest[1] == "'":
            val_bits = rest[2:].split("'", 1)  # always `'` from rdkit
            if len(val_bits) == 1:
                old, rest = val_bits
            else:
                old = val_bits[0]
                rest = ""
            val = cls._prep_svg_val(attr, old, value)
            rest = f"='{val}'{rest}"
        else:
            val_bits = rest[1:].split(" ", 1)
            if len(val_bits) == 1:
                old = val_bits[0]
                rest = ""
            else:
                old, rest = val_bits
                rest = " " + rest
            val = cls._prep_svg_val(attr, old, value)
            rest = f'={val}{rest}'
        return rest
    @classmethod
    def _inject_attr(cls, tag, body, attr, value):
        header, csep, rest = tag.partition(attr)
        if len(rest) == 0 or (len(rest) == 1 and rest[0] == "="):
            value = cls._prep_svg_val(attr, "", value)
            header += f" {attr}='{value}'"
        else:
            if (header[-1] == " " or header[-1] == "<") and rest[0] == "=":
                rest = cls._apply_attr_tf(attr, rest, value)
            else:
                if attr +"=" in rest:
                    oh, oc = header, csep
                    header, csep, subrest = rest.partition(attr +"=")
                    header = oh + oc +header
                    csep = attr
                    rest = "= " +subrest
                    if header[-1] == " ":
                        rest = cls._apply_attr_tf(attr, rest, value)
                else:
                    header = header + csep + rest
                    csep = " "
                    rest = f"{attr}='{value}'"

        tag = header + csep + rest
        return tag, body
    @classmethod
    def _find_end_tag(cls, text, tag_start, end_tag1, end_tag2, closer_tag):
        tag_end1 = text.find(end_tag1, tag_start)
        tag_end2 = text.find(end_tag2, tag_start)
        which_int = None
        if tag_end1 < 0:
            if tag_end2 < 0:
                return -1, None
            else:
                tag_end = tag_end2
                which = end_tag2
                which_int = 1
        elif tag_end2 < 0:
            tag_end = tag_end1
            which = end_tag1
            which_int = 0
        elif tag_end1 <= tag_end2:
            tag_end = tag_end1
            which = end_tag1
            which_int = 0
        else:
            tag_end = tag_end2
            which = end_tag2
            which_int = 1
        tag_end = text.find(closer_tag, tag_end + 1)
        if tag_end < 0:
            return -1, None
        tag_end = tag_end + 1
        return tag_end, which
    @classmethod
    def _iter_xml_chunk(cls, text :str):
        end_tag1 = "/>"
        end_tag2 = "</"
        open_tag = "<"
        closer_tag = ">"
        cur_l = -1
        end_l = len(text)
        stack = []
        while cur_l < end_l:
            tag_start = text.find(open_tag, cur_l +1)
            if tag_start < 0:
                break
            cur_l += 1
            tag_end, end_tag = cls._find_end_tag(text, tag_start, end_tag1, end_tag2, closer_tag)
            if tag_end < 0:
                break
            tag_end += len(closer_tag)
            sub_chunk = text[cur_l:tag_end]
            opener_counts = sub_chunk.count(open_tag)
            closer_counts = sub_chunk.count(closer_tag)
            if opener_counts == closer_counts:
                yield sub_chunk
            else:
                for diff in range(closer_counts - opener_counts):
                    tag_start = text.find(closer_tag, tag_start +1)
                    tag_start = text.find(open_tag, tag_start +1)
                    stack.append(tag_start)
                sub_chunk = text[tag_start:tag_end]
                children = [sub_chunk]
                for ts in reversed(stack):
                    te, end_tag = cls._find_end_tag(text, tag_start, end_tag1, end_tag2, closer_tag)
                    if te < 0:
                        raise ValueError("unclosed XML")
                    te += len(closer_tag)
                    children.append((text[ts:tag_start], text[tag_end:te]))
                    tag_start = ts
                    tag_end = te
                yield children
            cur_l += tag_end - cur_l
    @classmethod
    def _tranform_single(cls, t, transformation):
        if len(t.strip()) > 0:
            # we assume no nesting
            tag, sep, body = t.partition(">")
            if tag[-1] == "/":
                tag = tag[:-1]
                sep = "/" + sep
            if "</" not in tag:
                tag, body = transformation(tag, body)
            body = cls._transform_svg(body, transformation)
            t = tag + sep + body
        return t
    @classmethod
    def _transform_svg(cls, text, transformation):
        chunks = []
        for t in cls._iter_xml_chunk(text):
            if isinstance(t, str):
                if len(t.strip()) > 0:
                    t = cls._tranform_single(t, transformation)
            else:
                # only transform top-level element by default
                # requires constructing, TODO: allow nested tfs
                body = t[-1]
                for header, footer in reversed(t[-1]):
                    body = header + body + footer
                t = cls._tranform_single(body, transformation)
            chunks.append(t)
        return "".join(chunks)
    @classmethod
    def add_classes(cls, label, text):
        if label is not None and len(text) > 0:
            label = label.replace("_", "-")
            text =  f"<g class='{label}'>\n{text}</g>"
        return text
    @classmethod
    def _attr_annotation_function(cls, attr, value):
        def annotate(tag, body):
            return cls._inject_attr(tag, body, attr, value)
        return annotate
    default_annotation_pattern = None
    default_annotation_exclude = r'mol-\w+'
    @classmethod
    def _prep_annotation_function(cls, attrs_dict):
        if dev.is_list_like(attrs_dict):
            subfuncs = [
                cls._prep_annotation_function(d)
                for d in attrs_dict
            ]
            def transform(label, text, return_applied=False):
                applied = False
                for f in subfuncs:
                    text, applied = f(label, text, return_applied=True)
                    if applied:
                        break
                if return_applied:
                    return text, applied
                else:
                    return text
        else:
            funcs = []
            if attrs_dict is None:
                attrs_dict = {'classes' :True}
            cls_prep = attrs_dict.pop('classes', None)
            matches = attrs_dict.pop('pattern', None)
            excludes = attrs_dict.pop('exclude', cls.default_annotation_exclude)
            rep = attrs_dict.pop('replacement', None)
            if isinstance(rep, dict):
                text = rep.pop('text')
                rep = cls._text_addition_function(text, **rep)
            for k ,v in attrs_dict.items():
                f = cls._attr_annotation_function(k, v)
                funcs.append(f)
            def transform(label, text, return_applied=False):
                apply_tf = True
                if apply_tf and matches is not None:
                    if isinstance(matches, (str, re.Pattern)):
                        apply_tf = label is not None and bool(re.match(matches, label))
                    else:
                        apply_tf = matches(label)
                if apply_tf and excludes is not None:
                    if isinstance(excludes, (str, re.Pattern)):
                        apply_tf = label is not None and not bool(re.match(excludes, label))
                    else:
                        apply_tf = not excludes(label)
                if apply_tf:
                    if rep is not None:
                        text = rep(text)
                    text = cls._transform_svg(
                        text,
                        lambda tag ,body:functools.reduce(lambda x, y: y(*x), funcs, (tag, body))
                    )
                    if cls_prep is True:
                        k = label
                    elif cls_prep:
                        k = cls_prep(label)
                    else:
                        k = None
                    if k is not None:
                        text = cls.add_classes(k, text)
                if return_applied:
                    return text, apply_tf
                else:
                    return text
        return transform
    @classmethod
    def annotate_text(cls, text, splits, annotation_map=None):
        bits = []
        samp = ""
        if callable(annotation_map):
            function = annotation_map
        else:
            function = cls._prep_annotation_function(annotation_map)
        for label, c in cls.split_string_by_segments(text, splits):
            samp += c
            c = function(label, c)
            bits.append(c)
        return "".join(bits)
    def postprocess(self, text):
        # TODO: set up options dispatch for this
        postdraw = self.postdraw
        if dev.str_is(self.postdraw, 'annotate'):
            postdraw = {'annotate' :{}}
        if postdraw is not None:
            if not callable(postdraw):
                if 'annotate' not in postdraw:
                    annotation_function = postdraw
                else:
                    annotation_function = postdraw['annotate']
                postdraw = functools.partial(self.annotate_text, annotation_map=annotation_function)
            text = postdraw(text, self.splits)
        # print(text)
        # raise Exception(...)
        return text
    @property
    def text(self):
        if self._text is None:
            if self._raw_text is None:
                self.figure.FinishDrawing()
                self._raw_text = self.figure.GetDrawingText()
            self._text = self.postprocess(self._raw_text)
        return self._text

    @classmethod
    def get_svg_script(self, id):
        return f"""
    (function(){{
      let link = document.createElement('a');
      let base_name = '{id}';
      link.download = base_name + '.svg';
      let serializer = new XMLSerializer();
      let svg = document.getElementById('{id}').getElementsByTagName('svg')[0]
      let source = serializer.serializeToString(svg);
      link.href = "data:image/svg+xml;charset=utf-8,"+encodeURIComponent(source);
      link.click();
    }})()"""

    @classmethod
    def get_png_from_svg_script(self, id):
        return f"""
            (function(){{
              let base_name = '{id}';
              let serializer = new XMLSerializer();
              let svg = document.getElementById('{id}').getElementsByTagName('svg')[0]
              let source = serializer.serializeToString(svg);

              // https://stackoverflow.com/a/28226736  
              const svgBlob = new Blob([source], {{type: 'image/svg+xml;charset=utf-8'}});
              const url = window.URL.createObjectURL(svgBlob);

              const image = new Image();
              image.width = svg.width.baseVal.value;
              image.height = svg.height.baseVal.value;
              image.src = url;
              image.onload = function () {{
                const canvas = document.createElement('canvas');
                canvas.width = image.width;
                canvas.height = image.height;

                const ctx = canvas.getContext('2d');
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(image, 0, 0);
                window.URL.revokeObjectURL(url);

                const imgURI = canvas
                  .toDataURL('image/png')
                  .replace('image/png', 'image/octet-stream');

                let link = document.createElement('a');
                link.download = base_name + '.png';
                link.target = '_blank';
                link.href = imgURI;

                link.click()    
              }};
            }})()"""

    @classmethod
    def get_png_script(self, id):
        return f"""
    (function(){{
      let link = document.createElement('a');
      let base_name = '{id}';
      link.download = base_name + '.png';
      link.href = document.getElementById('{id}').getElementsByTagName('img')[0].src
      link.click();
    }})()"""

    def to_widget(self):
        from ..Jupyter.JHTML import HTML
        if self.fmt == 'svg':
            obj = HTML.parse(self.text, namespace='http://www.w3.org/2000/svg')
            if self.include_save_buttons:
                obj = JHTML.Div(
                    obj,
                    JHTML.Div(
                        JHTML.Button("Download SVG", onclick=self.get_svg_script(self.id)),
                        JHTML.Button("Download PNG", onclick=self.get_png_from_svg_script(self.id)),
                        display='flex'
                    ),
                    id=self.id,
                    display='block'
                )
        else:
            b64_url = base64.b64encode(self.text.encode())
            data_url = "data:image/png;base64," + b64_url.decode('utf-8')
            obj = HTML.Image(src=data_url)
            if self.include_save_buttons:
                obj = JHTML.Div(
                    obj,
                    JHTML.Button("Download", onclick=self.get_png_script(self.id)),
                    id=self.id,
                    display='block'
                )
        return obj

    def _ipython_display_(self):
        self.to_widget()._ipython_display_()

    def show(self):
        self.to_widget().display()

    def save(self, file):
        if self.fmt == 'svg':
            with open(file, 'w+') as out:
                out.write(self.text)
        else:
            from PIL import Image
            obj = Image.open(io.BytesIO(self.text))
            obj.save(file, format=self.fmt)