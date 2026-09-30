"""
Draft: keyframed animation support for the `mesh3D` backend (`Mesh3DFigure`),
with export to an animated glTF 2.0 (`.glb`/`.gltf`) that PowerPoint can play.

Mirrors the X3D design in `X3DInterface`:

  * `X3DInterpolatingAnimator.frame_diffs`  ->  `Mesh3DAnimation.frame_diffs`
    (walk the frames in parallel, split static meshes from changing ones)
  * `X3DInterpolatingAnimator` (Position/Orientation/CoordinateInterpolator)
        ->  glTF node `translation`/`rotation`/`scale` channels ('rigid' tracks)
            or mesh morph-target `weights` channels ('morph' tracks)
  * `X3DListAnimator` (Switch + IntegerSequencer)
        ->  one node per frame with STEP-interpolated `scale` 0/1 ('list' mode)

Each changing mesh is first tried as a rigid-body + axis-scale motion of its
frame-0 geometry (exact for atom spheres and bond cylinders, which is what the
molecule plotters emit). glTF node TRS animation is the most widely supported
animation type (PowerPoint, Windows 3D Viewer, Blender, three.js), so that is
preferred. Anything that is not affine falls back to morph targets.

Skinned export
--------------
Some players (notably PowerPoint) only play *skeletal* (skinned) glTF
animation and ignore node-TRS and morph-target channels. ``skinned=True``
re-expresses the same keyframes as a skeleton: every animated piece gets a
joint that carries exactly the TRS keyframes the node export would have used,
and the piece's vertices are bound to that joint with weight 1. Static meshes
are bound to the (unanimated) root joint, 'list' frames become joints whose
scale is switched 0/1, and non-rigid ('morph') pieces fall back to one
translation-only joint per vertex (exact, but joint-heavy).

Usage:

    anim = mol.animate_mode(3, backend='mesh3D')     # -> Mesh3DAnimation
    anim.savefig('mode3.glb')                          # animated, loops
    anim.savefig('mode3_ppt.glb', skinned=True)        # skeletal version for PowerPoint
    anim.show()                                        # X3D preview in Jupyter
"""

import dataclasses
import json
import warnings
import numpy as np

__all__ = ["Mesh3DAnimation"]


def _backends(obj=None):
    from . import Backends
    return Backends


@dataclasses.dataclass
class _MeshTrack:
    kind: str                       # 'rigid' | 'morph'
    mesh: object                    # MeshInformation (local coords for 'rigid')
    translations: np.ndarray = None # (nframes, 3)
    rotations: np.ndarray = None    # (nframes, 4) glTF xyzw quaternions
    scales: np.ndarray = None       # (nframes, 3)
    targets: list = None            # [(nverts, 3)] position deltas vs frame 0
    normal_targets: list = None


class Mesh3DAnimation:
    """
    A keyframed animation assembled from parallel per-frame lists of
    `MeshInformation` (what `Mesh3DAxes.draw_*` returns), exportable to glTF.
    """

    rigid_tolerance = 1e-6
    skinned_export = False          # default for `to_gltf`/`savefig` when `skinned` isn't passed
    max_morph_joints = 20000        # guard for the per-vertex fallback in skinned export

    def __init__(self, frames, figure=None, mode=None, animation_duration=2.0,
                 background=None, name="animation", **ignored_opts):
        """
        :param frames: one (possibly nested) list of `MeshInformation` per frame
        :param figure: the `Mesh3DFigure` that produced the frames (for materials/background)
        :param mode: None/'auto' (rigid where exact, else morph), 'rigid', 'morph', or 'list'
        :param animation_duration: loop length in seconds (same meaning as the X3D animators)
        """
        self.frames = [self._flatten(f) for f in frames]
        self.nframes = len(self.frames)
        if self.nframes == 0:
            raise ValueError("no frames to animate")
        self.figure = figure
        self.duration = float(animation_duration)
        self.name = name
        if background is None:
            background = getattr(figure, 'background', 'white')
        self.background = background
        self.mode = 'auto' if mode is None else mode
        self.static, self.tracks, self.list_mode = self.frame_diffs(self.frames, self.mode)

    # ------------------------------------------------------------------ #
    #  frame analysis
    # ------------------------------------------------------------------ #
    @classmethod
    def _flatten(cls, frame):
        out = []
        if frame is None:
            return out
        if hasattr(frame, 'vertices') and hasattr(frame, 'faces'):   # MeshInformation (duck-typed)
            return [frame]
        if hasattr(frame, 'to_mesh_list'):          # a Mesh3DAxes / figure-ish
            return list(frame.to_mesh_list())
        if hasattr(frame, 'meshes'):
            return list(frame.meshes)
        for f in frame:
            out.extend(cls._flatten(f))
        return out

    @classmethod
    def _same_topology(cls, meshes):
        m0 = meshes[0]
        for m in meshes[1:]:
            if m.vertices.shape != m0.vertices.shape or m.mode != m0.mode:
                return False
            if (m.faces is None) != (m0.faces is None):
                return False
            if m.faces is not None and not np.array_equal(m.faces, m0.faces):
                return False
        return True

    @classmethod
    def frame_diffs(cls, frames, mode='auto'):
        """
        Walk the frames in parallel (like `X3DInterpolatingAnimator.frame_diffs`).

        :return: `(static_meshes, tracks, list_mode)`
        """
        if mode == 'list':
            return [], [], True
        n = len(frames[0])
        if any(len(f) != n for f in frames):
            if mode in ('rigid', 'morph'):
                raise ValueError("frames have different numbers of meshes; use mode='list'")
            return [], [], True
        static, tracks = [], []
        for i in range(n):
            meshes = [f[i] for f in frames]
            if not cls._same_topology(meshes):
                if mode in ('rigid', 'morph'):
                    raise ValueError(f"mesh {i} changes topology between frames; use mode='list'")
                return [], [], True
            v0 = meshes[0].vertices
            if all(np.allclose(m.vertices, v0) for m in meshes[1:]):
                static.append(meshes[0])
                continue
            track = None
            if mode in ('auto', 'rigid'):
                track = cls.fit_rigid_track(meshes, tol=cls.rigid_tolerance)
                if track is None and mode == 'rigid':
                    raise ValueError(f"mesh {i} ({meshes[0].name}) is not a rigid+scale motion")
            if track is None:
                track = cls.fit_morph_track(meshes)
            tracks.append(track)
        return static, tracks, False

    @staticmethod
    def _quat_xyzw(R):
        """Rotation matrix -> unit quaternion in glTF (x, y, z, w) order."""
        m = R
        tr = np.trace(m)
        if tr > 0:
            s = 2.0 * np.sqrt(tr + 1.0)
            w = 0.25 * s
            x = (m[2, 1] - m[1, 2]) / s
            y = (m[0, 2] - m[2, 0]) / s
            z = (m[1, 0] - m[0, 1]) / s
        elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
            s = 2.0 * np.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2])
            w = (m[2, 1] - m[1, 2]) / s
            x = 0.25 * s
            y = (m[0, 1] + m[1, 0]) / s
            z = (m[0, 2] + m[2, 0]) / s
        elif m[1, 1] > m[2, 2]:
            s = 2.0 * np.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2])
            w = (m[0, 2] - m[2, 0]) / s
            x = (m[0, 1] + m[1, 0]) / s
            y = 0.25 * s
            z = (m[1, 2] + m[2, 1]) / s
        else:
            s = 2.0 * np.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1])
            w = (m[1, 0] - m[0, 1]) / s
            x = (m[0, 2] + m[2, 0]) / s
            y = (m[1, 2] + m[2, 1]) / s
            z = 0.25 * s
        q = np.array([x, y, z, w])
        return q / np.linalg.norm(q)

    @classmethod
    def fit_rigid_track(cls, meshes, tol=1e-6):
        """
        Try to write every frame as  V_k = R_k S_k L + t_k  with L the frame-0 mesh
        in a fixed local basis B, R_k a proper rotation and S_k diagonal (glTF node TRS).

        Returns None if the motion isn't of that form (-> morph fallback).
        """
        V0 = meshes[0].vertices
        c0 = V0.mean(axis=0)
        X = V0 - c0
        scale = max(1.0, float(np.abs(X).max()))
        if np.linalg.matrix_rank(X, tol=tol * scale) < 3:
            return None      # flat/degenerate mesh: affine map not unique

        # world-space affine maps A_k with (V_k - c_k) = X A_k^T
        As, cs = [], []
        for m in meshes:
            c = m.vertices.mean(axis=0)
            Y = m.vertices - c
            At, *_ = np.linalg.lstsq(X, Y, rcond=None)
            if np.sqrt(np.mean((X @ At - Y) ** 2)) > tol * scale:
                return None
            As.append(At.T)
            cs.append(c)

        # a single local basis in which every stretch is diagonal
        G = sum(A.T @ A for A in As)
        _, B = np.linalg.eigh(G)
        if np.linalg.det(B) < 0:
            B[:, 0] *= -1

        trans, rots, scls = [], [], []
        prev_q = None
        for A, c in zip(As, cs):
            M = A @ B                          # local -> world linear part
            U, s, Wt = np.linalg.svd(M)
            R = U @ Wt
            if np.linalg.det(R) < 0:
                return None
            P = Wt.T @ np.diag(s) @ Wt         # M = R P
            off = P - np.diag(np.diag(P))
            if np.abs(off).max() > 1e3 * tol * max(1.0, np.abs(P).max()):
                return None
            q = cls._quat_xyzw(R)
            if prev_q is not None and np.dot(q, prev_q) < 0:
                q = -q                         # keep quaternion path continuous
            prev_q = q
            trans.append(c)
            rots.append(q)
            scls.append(np.diag(P))

        m0 = meshes[0]
        local = dataclasses.replace(
            m0,
            vertices=X @ B,
            normals=None if m0.normals is None else np.asarray(m0.normals) @ B
        )
        return _MeshTrack('rigid', local,
                          translations=np.array(trans),
                          rotations=np.array(rots),
                          scales=np.array(scls))

    @classmethod
    def fit_morph_track(cls, meshes):
        """Frame 0 is the base mesh; frames 1..n-1 become morph targets (position deltas)."""
        m0 = meshes[0]
        targets = [m.vertices - m0.vertices for m in meshes[1:]]
        normal_targets = None
        if m0.normals is not None and all(m.normals is not None for m in meshes):
            normal_targets = [np.asarray(m.normals) - np.asarray(m0.normals) for m in meshes[1:]]
        return _MeshTrack('morph', m0, targets=targets, normal_targets=normal_targets)

    # ------------------------------------------------------------------ #
    #  glTF export
    # ------------------------------------------------------------------ #
    def _append_material(self, gltf, g, mat):
        fig_cls = type(self.figure) if self.figure is not None else _backends().Mesh3DFigure
        return fig_cls._append_material(gltf, g, mat)

    def to_gltf(self, skinned=None):
        """
        :param skinned: write skeletal (skinned) animation instead of node-TRS /
            morph-target channels (defaults to `skinned_export`)
        """
        if skinned is None:
            skinned = self.skinned_export
        if skinned:
            return self.to_skinned_gltf()
        g = _backends(self.figure).MeshAPIManager.gltf()
        gltf = g.GLTF2()
        gltf.scenes = [g.Scene(nodes=[])]
        gltf.scene = 0
        blob = bytearray()

        def accessor(array, type, comp=g.FLOAT, target=None, minmax=False):
            array = np.ascontiguousarray(array)
            data = array.tobytes()
            blob.extend(b'\x00' * ((4 - len(blob) % 4) % 4))
            offset = len(blob)
            blob.extend(data)
            bv = g.BufferView(buffer=0, byteOffset=offset, byteLength=len(data))
            if target is not None:
                bv.target = target
            gltf.bufferViews.append(bv)
            count = array.size if type == "SCALAR" else len(array)
            acc = g.Accessor(bufferView=len(gltf.bufferViews) - 1, componentType=comp,
                             count=count, type=type)
            if minmax:
                if type == "SCALAR":
                    acc.max, acc.min = [float(array.max())], [float(array.min())]
                else:
                    acc.max, acc.min = array.max(axis=0).tolist(), array.min(axis=0).tolist()
            gltf.accessors.append(acc)
            return len(gltf.accessors) - 1

        def add_mesh(m, name, targets=None, normal_targets=None):
            mat = self._append_material(gltf, g, m.material or {})
            attrs = g.Attributes(POSITION=accessor(m.vertices.astype(np.float32), "VEC3",
                                                   target=g.ARRAY_BUFFER, minmax=True))
            if m.normals is not None and len(m.normals) == len(m.vertices):
                attrs.NORMAL = accessor(np.asarray(m.normals, np.float32), "VEC3", target=g.ARRAY_BUFFER)
            idx = None
            if m.faces is not None and len(m.faces):
                idx = accessor(m.faces.astype(np.uint32).ravel(), "SCALAR",
                               comp=g.UNSIGNED_INT, target=g.ELEMENT_ARRAY_BUFFER)
            prim = g.Primitive(attributes=attrs, indices=idx, material=mat,
                               mode={'triangles': 4, 'lines': 1, 'points': 0}[m.mode])
            weights = None
            if targets:
                prim.targets = []
                for k, dv in enumerate(targets):
                    ta = g.Attributes(POSITION=accessor(np.asarray(dv, np.float32), "VEC3",
                                                        target=g.ARRAY_BUFFER, minmax=True))
                    if normal_targets is not None:
                        ta.NORMAL = accessor(np.asarray(normal_targets[k], np.float32), "VEC3",
                                             target=g.ARRAY_BUFFER)
                    prim.targets.append(ta)
                weights = [0.0] * len(targets)
            gltf.meshes.append(g.Mesh(primitives=[prim], name=name, weights=weights))
            return len(gltf.meshes) - 1

        def add_node(parent=None, **kw):
            gltf.nodes.append(g.Node(**kw))
            ni = len(gltf.nodes) - 1
            if parent is None:
                gltf.scenes[0].nodes.append(ni)
            else:
                gltf.nodes[parent].children = (gltf.nodes[parent].children or []) + [ni]
            return ni

        channels, samplers = [], []

        def add_channel(node, path, times_acc, values, type, interpolation="LINEAR"):
            out = accessor(np.asarray(values, np.float32), type)
            samplers.append(g.AnimationSampler(input=times_acc, output=out, interpolation=interpolation))
            channels.append(g.AnimationChannel(sampler=len(samplers) - 1,
                                               target=g.AnimationChannelTarget(node=node, path=path)))

        root = add_node(name=self.name)
        n = self.nframes

        if self.list_mode:
            # X3DListAnimator analogue: one node per frame, only one visible at a time
            # n frames each shown for duration/n; the extra key at t=duration holds the
            # last frame so the clip length matches `animation_duration` when looping
            times = np.linspace(0, self.duration, n + 1).astype(np.float32)
            t_acc = accessor(times, "SCALAR", minmax=True)
            for k, frame in enumerate(self.frames):
                fn = add_node(root, name=f"frame-{k}", scale=[1.0, 1.0, 1.0] if k == 0 else [0.0, 0.0, 0.0])
                for j, m in enumerate(frame):
                    add_node(fn, mesh=add_mesh(m, m.name or f"mesh-{k}-{j}"), name=m.name or f"mesh-{k}-{j}")
                vis = np.zeros((n + 1, 3))
                vis[k] = 1.0
                if k == n - 1:
                    vis[n] = 1.0
                add_channel(fn, "scale", t_acc, vis, "VEC3", interpolation="STEP")
        else:
            # X3DInterpolatingAnimator analogue: keys spread over [0, duration]
            times = np.linspace(0, self.duration, n).astype(np.float32)
            t_acc = accessor(times, "SCALAR", minmax=True)
            for j, m in enumerate(self.static):
                nm = m.name or f"static-{j}"
                add_node(root, mesh=add_mesh(m, nm), name=nm)
            for j, tr in enumerate(self.tracks):
                nm = (tr.mesh.name or "mesh") + f"-{j}"
                if tr.kind == 'rigid':
                    ni = add_node(root, mesh=add_mesh(tr.mesh, nm), name=nm,
                                  translation=tr.translations[0].tolist(),
                                  rotation=tr.rotations[0].tolist(),
                                  scale=tr.scales[0].tolist())
                    add_channel(ni, "translation", t_acc, tr.translations, "VEC3")
                    add_channel(ni, "rotation", t_acc, tr.rotations, "VEC4")
                    if not np.allclose(tr.scales, tr.scales[0]):
                        add_channel(ni, "scale", t_acc, tr.scales, "VEC3")
                else:
                    ni = add_node(root, mesh=add_mesh(tr.mesh, nm, tr.targets, tr.normal_targets), name=nm)
                    w = np.zeros((n, n - 1))
                    w[np.arange(1, n), np.arange(n - 1)] = 1.0   # frame k -> one-hot target k-1
                    add_channel(ni, "weights", t_acc, w.ravel(), "SCALAR")

        if channels:
            gltf.animations = [g.Animation(name=self.name, channels=channels, samplers=samplers)]
        gltf.buffers = [g.Buffer(byteLength=len(blob))]
        gltf.set_binary_blob(bytes(blob))
        return gltf

    # ------------------------------------------------------------------ #
    #  skinned (skeletal) glTF export
    # ------------------------------------------------------------------ #
    @staticmethod
    def _quat_matrix(q):
        x, y, z, w = q
        return np.array([
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]
        ])

    @classmethod
    def _trs_matrix(cls, t=None, q=None, s=None):
        M = np.eye(4)
        L = np.eye(3)
        if q is not None:
            L = cls._quat_matrix(q)
        if s is not None:
            L = L * np.asarray(s)[np.newaxis, :]
        M[:3, :3] = L
        if t is not None:
            M[:3, 3] = t
        return M

    @staticmethod
    def _material_key(mesh):
        def norm(v):
            if v is None or isinstance(v, (str, bool)):
                return v
            return np.round(np.asarray(v, dtype=float), 6).tolist()
        mat = mesh.material or {}
        return json.dumps(
            [mesh.mode, mesh.normals is not None, sorted((k, norm(v)) for k, v in mat.items())],
            default=str
        )

    def to_skinned_gltf(self):
        """
        Write the animation as a single skinned mesh driven by a skeleton.

        Joint `j` carries the same TRS keyframes that the node export gives the
        corresponding node, and its inverse bind matrix is the inverse of its rest
        (frame-0) transform, so with vertices bound in frame-0 world coordinates the
        skinned result reproduces the node-TRS animation exactly.
        """
        g = _backends(self.figure).MeshAPIManager.gltf()
        gltf = g.GLTF2()
        gltf.scenes = [g.Scene(nodes=[])]
        gltf.scene = 0
        blob = bytearray()

        def accessor(array, type, comp=g.FLOAT, target=None, minmax=False):
            array = np.ascontiguousarray(array)
            data = array.tobytes()
            blob.extend(b'\x00' * ((4 - len(blob) % 4) % 4))
            offset = len(blob)
            blob.extend(data)
            bv = g.BufferView(buffer=0, byteOffset=offset, byteLength=len(data))
            if target is not None:
                bv.target = target
            gltf.bufferViews.append(bv)
            count = array.size if type == "SCALAR" else len(array)
            acc = g.Accessor(bufferView=len(gltf.bufferViews) - 1, componentType=comp,
                             count=count, type=type)
            if minmax:
                if type == "SCALAR":
                    acc.max, acc.min = [float(array.max())], [float(array.min())]
                else:
                    acc.max, acc.min = array.max(axis=0).tolist(), array.min(axis=0).tolist()
            gltf.accessors.append(acc)
            return len(gltf.accessors) - 1

        n = self.nframes
        # joint specs: (name, rest (t, q, s), {path: values}); joint 0 is the static root
        joints = [("root", (None, None, None), {})]
        pieces = []  # (mesh, bind_vertices, bind_normals, per-vertex joint ids)

        def add_joint(name, rest, channels):
            joints.append((name, rest, channels))
            return len(joints) - 1

        if self.list_mode:
            times = np.linspace(0, self.duration, n + 1)
            interpolation = "STEP"
            for k, frame in enumerate(self.frames):
                vis = np.zeros((n + 1, 3))
                vis[k] = 1.0
                if k == n - 1:
                    vis[n] = 1.0
                # rest scale stays 1 so the inverse bind matrix is invertible
                j = add_joint(f"frame-{k}", (None, None, [1.0, 1.0, 1.0]), {"scale": vis})
                for m in frame:
                    pieces.append((m, m.vertices, m.normals, np.full(len(m.vertices), j)))
        else:
            times = np.linspace(0, self.duration, n)
            interpolation = "LINEAR"
            for m in self.static:
                pieces.append((m, m.vertices, m.normals, np.zeros(len(m.vertices), dtype=int)))
            for i, tr in enumerate(self.tracks):
                nm = (tr.mesh.name or "mesh") + f"-{i}"
                if tr.kind == 'rigid':
                    t0, q0, s0 = tr.translations[0], tr.rotations[0], tr.scales[0]
                    channels = {"translation": tr.translations, "rotation": tr.rotations}
                    if not np.allclose(tr.scales, tr.scales[0]):
                        channels["scale"] = tr.scales
                    j = add_joint(nm, (t0, q0, s0), channels)
                    R0 = self._quat_matrix(q0)
                    V = (tr.mesh.vertices * s0) @ R0.T + t0          # frame-0 world coordinates
                    N = None
                    if tr.mesh.normals is not None:
                        N = (np.asarray(tr.mesh.normals) / s0) @ R0.T   # inverse-transpose of R S
                        N /= np.maximum(np.linalg.norm(N, axis=-1, keepdims=True), 1e-12)
                    pieces.append((tr.mesh, V, N, np.full(len(V), j)))
                else:
                    # exact fallback: one translation-only joint per vertex
                    V0 = tr.mesh.vertices
                    traj = np.stack([V0] + [V0 + d for d in tr.targets], axis=1)   # (nverts, nframes, 3)
                    if len(joints) + len(V0) > self.max_morph_joints:
                        raise ValueError(
                            f"skinned export of non-rigid mesh {nm} needs {len(V0)} joints "
                            f"(limit `max_morph_joints`={self.max_morph_joints})"
                        )
                    warnings.warn(f"{nm} isn't a rigid motion; skinning it with {len(V0)} per-vertex joints")
                    ids = np.array([
                        add_joint(f"{nm}-v{v}", (V0[v], None, None), {"translation": traj[v]})
                        for v in range(len(V0))
                    ])
                    # normals can't follow a per-vertex skeleton; let the viewer shade flat
                    pieces.append((dataclasses.replace(tr.mesh, normals=None), V0, None, ids))

        # --- skeleton nodes: root joint with every other joint as a direct child --- #
        joint_nodes = []
        for name, (t, q, s), _ in joints:
            node = g.Node(name=f"joint-{name}")
            if t is not None:
                node.translation = np.asarray(t, dtype=float).tolist()
            if q is not None:
                node.rotation = np.asarray(q, dtype=float).tolist()
            if s is not None:
                node.scale = np.asarray(s, dtype=float).tolist()
            gltf.nodes.append(node)
            joint_nodes.append(len(gltf.nodes) - 1)
        root_node = joint_nodes[0]
        gltf.nodes[root_node].children = joint_nodes[1:]
        gltf.scenes[0].nodes.append(root_node)

        ibms = np.array([
            np.linalg.inv(self._trs_matrix(*rest)).T.reshape(-1)   # glTF matrices are column-major
            for _, rest, _ in joints
        ], dtype=np.float32)
        gltf.skins = [g.Skin(inverseBindMatrices=accessor(ibms, "MAT4"),
                             joints=joint_nodes, skeleton=root_node, name=self.name)]

        # --- one skinned mesh, one primitive per material --- #
        groups = {}
        for m, V, N, ids in pieces:
            groups.setdefault(self._material_key(m), []).append((m, V, N, ids))
        joint_comp = g.UNSIGNED_BYTE if len(joints) <= 256 else g.UNSIGNED_SHORT
        joint_dtype = np.uint8 if len(joints) <= 256 else np.uint16
        prims = []
        for key, members in groups.items():
            m0 = members[0][0]
            verts, norms, faces, jids, off = [], [], [], [], 0
            for m, V, N, ids in members:
                verts.append(V)
                norms.append(N)
                jids.append(ids)
                if m.faces is not None and len(m.faces):
                    faces.append(m.faces + off)
                off += len(V)
            V = np.concatenate(verts).astype(np.float32)
            J = np.zeros((len(V), 4), dtype=joint_dtype)
            J[:, 0] = np.concatenate(jids)
            Wt = np.zeros((len(V), 4), dtype=np.float32)
            Wt[:, 0] = 1.0
            attrs = g.Attributes(
                POSITION=accessor(V, "VEC3", target=g.ARRAY_BUFFER, minmax=True),
                JOINTS_0=accessor(J, "VEC4", comp=joint_comp, target=g.ARRAY_BUFFER),
                WEIGHTS_0=accessor(Wt, "VEC4", target=g.ARRAY_BUFFER),
            )
            if all(N is not None for N in norms):
                attrs.NORMAL = accessor(np.concatenate(norms).astype(np.float32), "VEC3", target=g.ARRAY_BUFFER)
            idx = None
            if faces:
                idx = accessor(np.concatenate(faces).astype(np.uint32).ravel(), "SCALAR",
                               comp=g.UNSIGNED_INT, target=g.ELEMENT_ARRAY_BUFFER)
            prims.append(g.Primitive(
                attributes=attrs, indices=idx,
                material=self._append_material(gltf, g, m0.material or {}),
                mode={'triangles': 4, 'lines': 1, 'points': 0}[m0.mode]
            ))
        gltf.meshes.append(g.Mesh(primitives=prims, name=self.name))
        # a skinned mesh node's own transform is ignored, so keep it untransformed at the root
        gltf.nodes.append(g.Node(mesh=0, skin=0, name=self.name + "-mesh"))
        gltf.scenes[0].nodes.append(len(gltf.nodes) - 1)

        # --- animation on the joints --- #
        channels, samplers = [], []
        if n > 1:
            t_acc = accessor(times.astype(np.float32), "SCALAR", minmax=True)
            types = {"translation": "VEC3", "rotation": "VEC4", "scale": "VEC3"}
            for (name, rest, chans), node in zip(joints, joint_nodes):
                for path, values in chans.items():
                    out = accessor(np.asarray(values, np.float32), types[path])
                    samplers.append(g.AnimationSampler(input=t_acc, output=out, interpolation=interpolation))
                    channels.append(g.AnimationChannel(sampler=len(samplers) - 1,
                                                       target=g.AnimationChannelTarget(node=node, path=path)))
        if channels:
            gltf.animations = [g.Animation(name=self.name, channels=channels, samplers=samplers)]
        gltf.buffers = [g.Buffer(byteLength=len(blob))]
        gltf.set_binary_blob(bytes(blob))
        return gltf

    def savefig(self, file, format=None, skinned=None, **opts):
        fmt = (format or (str(file).rsplit('.', 1)[-1] if isinstance(file, str) else 'glb')).lower()
        if fmt not in ('glb', 'gltf'):
            raise ValueError(f"animated export only supports glb/gltf, not {fmt}")
        gltf = self.to_gltf(skinned=skinned)
        if isinstance(file, str):
            if fmt == 'gltf':
                gltf.convert_buffers(_backends(self.figure).MeshAPIManager.gltf().BufferFormat.DATAURI)
            gltf.save(file)
            return file
        file.write(b"".join(gltf.save_to_bytes()))
        return file

    # ------------------------------------------------------------------ #
    #  X3D preview (reuses X3DFigure.animate_frames -> X3DInterpolatingAnimator)
    # ------------------------------------------------------------------ #
    @staticmethod
    def _unshare_for_x3d(mesh):
        """
        X3DOM can't animate flat-shaded geometry: with `normalPerVertex="false"` it
        expands the indexed triangles into per-face vertices when the shape is first
        built, and later `set_point` events (from the CoordinateInterpolator) are
        written into that expanded buffer with the wrong layout, so the shape
        collapses into slivers/lines or disappears. `Mesh3DFigure.to_x3d` emits
        `normalPerVertex="false"` for every mesh without normals (e.g. the bond
        cylinders, which are drawn without normals on purpose so the caps stay
        sharp).

        Instead, give each triangle its own three vertices and attach face normals.
        The shape is then written with per-vertex normals, which X3DOM animates
        correctly, and because no vertex is shared between faces it still looks
        flat-shaded.
        """
        if mesh.normals is not None or mesh.mode != 'triangles' or mesh.faces is None or not len(mesh.faces):
            return mesh
        tris = mesh.vertices[mesh.faces]                           # (nfaces, 3, 3)
        fn = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
        fn /= np.maximum(np.linalg.norm(fn, axis=-1, keepdims=True), 1e-12)
        return dataclasses.replace(
            mesh,
            vertices=tris.reshape(-1, 3),
            faces=np.arange(3 * len(tris)).reshape(-1, 3),
            normals=np.repeat(fn, 3, axis=0)
        )

    def to_x3d(self, **animation_opts):
        fig_cls = type(self.figure) if self.figure is not None else _backends().Mesh3DFigure
        figs = []
        for frame in self.frames:
            tmp = fig_cls(background=self.background)
            tmp.create_axes()
            tmp.axes[0].meshes = [self._unshare_for_x3d(m) for m in frame]
            figs.append(tmp.to_x3d())         # Graphics3D on the X3D backend
        children = [f.figure.axes[0].children for f in figs]
        animation_opts.setdefault('animation_duration', self.duration)
        mode = 'list' if self.list_mode else None
        return figs[0].figure.animate_frames(children, mode=mode, **animation_opts)

    def show(self):
        return self.to_x3d().show()

    def _ipython_display_(self):
        return self.show()
