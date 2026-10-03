"""
Data export: the readout as nested arrays/scalars (``to_data``), a flat ``.npz``, pandas
DataFrames or JSON. Values are exactly the ones every other renderer displays (same units,
full precision); unit metadata travels with them.
"""

import json
import os

import numpy as np

from ..Nodes import (ReadoutNode, ReadoutSection, ReadoutText, ReadoutFields, ReadoutTable,
                     ReadoutArray, ReadoutImage, ReadoutScene, ReadoutGallery, Readout)
from .Base import ReadoutRenderer, RenderContext, handles

__all__ = ["DataReadoutRenderer"]


def _jsonable(v):
    if isinstance(v, np.ndarray):
        return v.tolist()
    if isinstance(v, np.generic):
        return v.item()
    if isinstance(v, dict):
        return {k: _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    return v


class DataReadoutRenderer(ReadoutRenderer):
    hook_name = "readout_data"

    def __init__(self, style=None):
        super().__init__(style)

    def render_readout(self, readout):
        """-> ``(values, meta)`` with ``values`` nested by section id and ``meta`` keyed by path."""
        meta = {}
        ctx = RenderContext(path=(), meta=meta)
        values = self._container(readout, ctx)
        root_meta = {"title": readout.title, "units": {k: v for k, v in (readout.units.units if readout.units else {}).items()
                                                        if v is not None}}
        root_meta.update({k: _jsonable(v) for k, v in readout.meta.items()})
        values, self.renames = self._collapse(values)
        meta = {self.rename(k): v for k, v in meta.items()}
        meta[""] = root_meta
        return values, meta

    @staticmethod
    def _collapse(values):
        """Drop single-child levels (``frequencies/table/x`` -> ``frequencies/x``); returns renames."""
        renames = []
        def rec(d, path):
            out = {}
            for k, v in d.items():
                p = path + (k,)
                if isinstance(v, dict):
                    v = rec(v, p)
                    if len(v) == 1:
                        (ck, cv), = v.items()
                        renames.append(("/".join(p + (ck,)), "/".join(p)))
                        v = cv
                out[k] = v
            return out
        return rec(values, ()), renames

    def rename(self, key):
        for old, new in getattr(self, "renames", ()):
            if key == old or key.startswith(old + "/"):
                key = new + key[len(old):]
        return key

    def _container(self, node, ctx):
        out = {}
        for c in node.get_children():
            res = self.render(c, ctx.child(c))
            if res is None:
                continue
            if isinstance(res, dict) and c.kind == "fields" and c.title is None:
                out.update(res)          # untitled field blocks merge into their section
            else:
                out[c.id] = res
        return out

    def _meta(self, ctx, key, value):
        ctx.extra["meta"]["/".join(ctx.path + ((key,) if key else ()))] = value

    @handles(ReadoutSection, ReadoutGallery)
    def render_section(self, node, ctx):
        if node.meta.get("unavailable") or node.meta.get("error"):
            self._meta(ctx, None, {k: node.meta[k] for k in ("unavailable", "error") if k in node.meta})
        return self._container(node, ctx) or None

    @handles(ReadoutFields)
    def render_fields(self, node, ctx):
        vals = node.data.to_arrays()
        path = ctx.path if node.title is not None else ctx.path[:-1]
        for f in node.data:
            if f.name in vals:
                ctx.extra["meta"]["/".join(path + (f.name,))] = f.get_meta()
        return vals

    @handles(ReadoutTable)
    def render_table(self, node, ctx):
        for name, m in node.data.get_meta().items():
            self._meta(ctx, name, m)
        if node.title:
            self._meta(ctx, None, {"title": node.title})
        return node.data.to_arrays()

    @handles(ReadoutArray)
    def render_array(self, node, ctx):
        self._meta(ctx, None, node.data.get_meta())
        return node.data.array

    @handles(ReadoutText, ReadoutImage, ReadoutScene)
    def render_skip(self, node, ctx):
        return None

    # ---- outputs ---------------------------------------------------------------------- #
    def flatten(self, readout, sep="/"):
        values, meta = self.render_readout(readout)
        flat = {}
        def walk(d, prefix):
            for k, v in d.items():
                key = prefix + (k,)
                if isinstance(v, dict):
                    walk(v, key)
                else:
                    flat[sep.join(key)] = v
        walk(values, (readout.id,))
        meta = {(readout.id + (sep + k if k else "")): v for k, v in meta.items()}
        return flat, meta

    def write_npz(self, readout, file):
        flat, meta = self.flatten(readout)
        arrays = {k: np.asarray(v) for k, v in flat.items()}
        bad = [k for k, v in arrays.items() if v.dtype == object]
        if bad:
            raise TypeError(f"can't store object arrays without pickling: {bad}")
        arrays["__meta__"] = np.asarray(json.dumps(_jsonable(meta)))
        np.savez(file, **arrays)
        return file

    def to_pandas(self, readout):
        """``{path: DataFrame}`` for every table and field block."""
        frames = {}
        self.render_readout(readout)   # for the single-child renames
        for path, node in readout.walk():
            key = readout.id + "/" + self.rename("/".join(path[1:]))
            if isinstance(node, ReadoutTable):
                frames[key] = node.data.to_pandas()
            elif isinstance(node, ReadoutFields):
                k = key if node.title is not None else readout.id + "/" + self.rename("/".join(path[1:-1]))
                if k in frames:
                    import pandas as pd
                    frames[k] = pd.concat([frames[k], node.data.to_pandas()])
                else:
                    frames[k] = node.data.to_pandas()
        return frames

    def write_json(self, readout, file=None, indent=2):
        values, meta = self.render_readout(readout)
        doc = {"id": readout.id, "title": readout.title, "data": _jsonable(values),
               "meta": _jsonable(meta)}
        text = json.dumps(doc, indent=indent, ensure_ascii=False)
        if file is None:
            return text
        with open(file, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        return file

    def export_assets(self, readout, directory, skinned=True):
        os.makedirs(directory, exist_ok=True)
        written = {}
        for path, node in readout.walk():
            if isinstance(node, ReadoutScene) and node.get_source() is not None:
                src = node.get_source()
                fname = os.path.join(directory, "__".join(path[1:]) + ".glb")
                with open(fname, "wb") as f:
                    f.write(src.to_glb(skinned=skinned))
                written["/".join(path)] = fname
        return written
