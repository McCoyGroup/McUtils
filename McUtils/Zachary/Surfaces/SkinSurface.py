"""
Edelsbrunner's skin surface of a set of balls,

    H. Edelsbrunner, "Deformable Smooth Surface Design",
    Discrete Comput. Geom. 21, 87-115 (1999),

evaluated exactly from the regular (weighted Delaunay) triangulation of the
balls.

Definition. For balls `b_i = (z_i, w_i = R_i^2)` with power functions
`pi_i(x) = |x - z_i|^2 - w_i`, a convex combination `b = sum_i l_i b_i` is the
ball with `pi_b = sum_i l_i pi_i`, i.e. center `sum_i l_i z_i` and weight
`|z|^2 + sum_i l_i (w_i - |z_i|^2)`. The skin body for a shrink factor
`0 < s < 1` is the union of all such balls shrunk by `sqrt(s)`, and the skin is
its boundary: a C^1 surface, free of self-intersections, made of quadric
patches.

Evaluation. The skin body is `{x : F(x) >= 0}` with

    F(x) = max_{z in conv(z_i)} [ s W(z) - |x - z|^2 ],

where `W(z)` is the weight of the heaviest combination centered at `z` (given
by the lower hull of the lifted points, i.e. the regular triangulation). If the
maximizer lies in the relative interior of a simplex `X` of that triangulation,
with orthocenter `y_X` and orthosphere size `rho2_X`, then writing
`x - y_X = u + v` (`u` parallel to `X`, `v` orthogonal) gives the closed form

    F(x) = s/(1-s) |u|^2 - |v|^2 - s rho2_X ,
    grad F(x) = 2 s/(1-s) u - 2 v ,

valid exactly when `z* = y_X + u/(1-s)` lies in the simplex; this is the
point's mixed cell `mu_X = (1-s) delta_X + s nu_X`. So `F` is the maximum of
that expression over the simplices whose `z*` is feasible. The zero set is a
sphere of radius `sqrt(s) R_i` on vertex cells and a hyperboloid (or, on
tetrahedra, an inverted sphere) elsewhere.

Triangulation. The regular triangulation is built in the balls' own affine
dimension (so planar and linear molecules are handled exactly), certified
(tiling + local regularity, as in `AlphaMol`), and recomputed on slightly
perturbed balls if the certificate fails. Unlike `AlphaMol`, no bounding balls
are added: they would create spurious simplices near the hull, whereas the
skin depends on the real balls alone.

Meshing uses marching tetrahedra on the exact `F` (with a coarse pass that
skips grid cells certified, via the Hessian bound of `F`, not to meet the
skin), then projects the vertices onto `F = 0`, so vertices lie on the skin to
round-off and mesh areas/volumes converge as `O(h^2)` in the grid spacing.
Pointwise normals and curvatures are exact.
"""

import itertools

import numpy as np
import scipy.spatial

from .AlphaMol import AlphaMol

__all__ = [
    "SkinSurface",
    "SkinSurfaceMesh"
]

# Freudenthal (Kuhn) split of the unit cube into 6 tetrahedra: each follows a
# monotone path from corner (0,0,0) to (1,1,1); the split is conforming across
# neighbouring cubes, so the extracted surface is watertight.
_KUHN = np.array([
    [[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
    [[0, 0, 0], [1, 0, 0], [1, 0, 1], [1, 1, 1]],
    [[0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 1, 1]],
    [[0, 0, 0], [0, 1, 0], [0, 1, 1], [1, 1, 1]],
    [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1]],
    [[0, 0, 0], [0, 0, 1], [0, 1, 1], [1, 1, 1]],
])
_TET_EDGES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
# for a single inside (or outside) corner k: the three edges from k
_ONE = {0: (0, 1, 2), 1: (0, 3, 4), 2: (1, 3, 5), 3: (2, 4, 5)}
# for two inside corners (a, b): the four crossing edges, in cyclic order
_TWO = {
    (0, 1): (1, 2, 4, 3), (0, 2): (0, 2, 5, 3), (0, 3): (0, 1, 5, 4),
    (1, 2): (0, 4, 5, 1), (1, 3): (0, 3, 5, 2), (2, 3): (1, 3, 4, 2),
}


class SkinSurfaceMesh:
    """
    **LLM Docstring**

    A triangulation of a skin surface: vertices on the surface (after
    projection), outward-oriented triangles, exact vertex normals, and the
    index of the skin patch (simplex of the regular triangulation) each vertex
    lies on.
    """

    def __init__(self, verts, tris, normals=None, patches=None, skin=None, spacing=None):
        self.verts = np.asarray(verts)
        self.tris = np.asarray(tris)
        self.normals = normals
        self.patches = patches
        self.skin = skin
        self.spacing = spacing

    def surface_area(self):
        """
        **LLM Docstring**

        :return: the total area of the triangles
        :rtype: float
        """
        a, b, c = (self.verts[self.tris[:, k]] for k in range(3))
        return float(0.5 * np.sum(np.linalg.norm(np.cross(b - a, c - a), axis=1)))

    def volume(self):
        """
        **LLM Docstring**

        :return: the enclosed volume (divergence theorem; the triangles are
            outward oriented)
        :rtype: float
        """
        a, b, c = (self.verts[self.tris[:, k]] for k in range(3))
        return float(np.sum(np.einsum('ij,ij->i', a, np.cross(b, c))) / 6)

    def euler_characteristic(self):
        """
        **LLM Docstring**

        :return: `V - E + F` of the mesh (2 per closed genus-0 component)
        :rtype: int
        """
        e = np.sort(np.concatenate([self.tris[:, [0, 1]], self.tris[:, [1, 2]], self.tris[:, [2, 0]]]), axis=1)
        n_e = len(np.unique(e, axis=0))
        n_v = len(np.unique(self.tris))
        return int(n_v - n_e + len(self.tris))

    def vertex_curvatures(self):
        """
        **LLM Docstring**

        Exact mean and Gaussian curvature of the skin at the mesh vertices
        (cached).

        :rtype: dict
        """
        if getattr(self, '_curvatures', None) is None:
            if self.skin is None:
                raise ValueError("no skin surface attached to compute exact curvatures from")
            mean, gauss = self.skin.curvatures(self.verts, band=self.spacing if self.spacing else 1.0)
            self._curvatures = {'mean': mean, 'gaussian': gauss}
        return self._curvatures

    def to_surface_mesh(self, store_curvatures=True):
        """
        **LLM Docstring**

        Convert to a `SphereUnionSurfaceMesh`, for its plotting and mesh
        derivative tools.

        :param store_curvatures: store the exact skin curvatures at the
            vertices on the mesh (used by `SphereUnionSurfaceMesh.plot(curvature=...)`
            and `vertex_curvatures`); otherwise the mesh estimates them itself
        :type store_curvatures: bool
        :rtype: SphereUnionSurfaceMesh
        """
        from .SphereUnionSurface import SphereUnionSurfaceMesh
        skin = self.skin
        curv = self.vertex_curvatures() if (store_curvatures and skin is not None and len(self.verts)) else None
        return SphereUnionSurfaceMesh(
            self.verts, self.tris,
            vertex_normals=self.normals,
            centers=None if skin is None else skin.centers,
            radii=None if skin is None else skin.radii,
            curvatures=curv
        )


class SkinSurface:
    """
    **LLM Docstring**

    The skin surface of a union of balls (Edelsbrunner 1999), evaluated
    exactly from the regular triangulation. Every combination ball lies in the
    union of the generating balls, so the skin body does too.

    ```python
    skin = SkinSurface(coords, vdw_radii, shrink=0.5)   # convex caps on the vdW spheres
    F, grad = skin.skin_function(points, return_gradient=True)   # F >= 0 inside
    pts, nrm = skin.project(points)                      # nearest-ish points on the skin
    mesh = skin.triangulate(spacing=0.25)                # watertight, vertices on the skin
    mesh.surface_area(), mesh.volume()
    ```

    By default (`radii_type='convex'`) the given radii are those of the convex
    spherical caps, so the skin's sphere patches coincide with those spheres
    (for molecules: the van der Waals spheres) and the generating balls have
    radii `r_i / sqrt(s)`. With `radii_type='balls'` the given radii are the
    generating balls themselves and the caps have radii `sqrt(s) R_i`.
    """

    default_shrink = 0.5
    default_perturbation = 1e-9
    fallback_perturbations = (1e-8, 1e-7, 1e-6)

    def __init__(self, centers, radii, shrink=None, *, radii_type='convex',
                 perturbation=None, seed=1729):
        """
        **LLM Docstring**

        :param centers: ball centers, shape `(n, 3)`
        :type centers: np.ndarray
        :param radii: radii, shape `(n,)` (see `radii_type`)
        :type radii: np.ndarray
        :param shrink: the shrink factor `s`, `0 < s < 1`; smaller values give
            wider, smoother blends between the spheres
        :type shrink: float | None
        :param radii_type: `'convex'` (radii of the convex caps) or `'balls'`
            (radii of the generating balls)
        :type radii_type: str
        :param perturbation: relative size of the deterministic perturbation
            that puts the balls in general position (escalated automatically if
            the triangulation fails its certificate); see `AlphaMol`
        :type perturbation: float | None
        :param seed: seed for that perturbation
        :type seed: int
        """
        centers = np.asarray(centers, dtype=float)
        radii = np.asarray(radii, dtype=float)
        if centers.ndim != 2 or centers.shape[1] != 3:
            raise ValueError("centers must have shape (n, 3)")
        if radii.shape != (len(centers),):
            raise ValueError("radii must have shape (n,)")
        if len(radii) == 0:
            raise ValueError("need at least one ball")
        if not (np.all(np.isfinite(centers)) and np.all(np.isfinite(radii))) or np.any(radii <= 0):
            raise ValueError("centers must be finite and radii positive")
        s = self.default_shrink if shrink is None else float(shrink)
        if not 0 < s < 1:
            raise ValueError("shrink must lie strictly between 0 and 1")
        if radii_type == 'convex':
            ball_radii = radii / np.sqrt(s)
        elif radii_type == 'balls':
            ball_radii = radii
        else:
            raise ValueError(f"unknown radii_type '{radii_type}'")
        self.centers = centers
        self.radii = radii
        self.shrink = s
        self.radii_type = radii_type
        self.ball_radii = ball_radii
        self.perturbation = self.default_perturbation if perturbation is None else perturbation
        self.seed = seed
        self._simplices = None
        self._mesh_cache = {}

    # ------------------------------------------------------------------
    # triangulation and per-simplex patch data
    # ------------------------------------------------------------------
    @staticmethod
    def _lower_hull(Q, h):
        """
        Lower hull of the lifted points `(Q, h)` in `d + 1` dimensions
        (`Q` has shape `(n, d)`), i.e. the regular triangulation of the
        weighted points with `h = |q|^2 - w`. Returns the top simplices, or
        `None` if Qhull fails.
        """
        n, d = Q.shape
        if n <= d + 1:
            return np.arange(n)[None, :]
        lifted = np.column_stack([Q, h])
        try:
            hull = scipy.spatial.ConvexHull(lifted, qhull_options='Qt Qx QbB' if d >= 2 else 'Qt QbB')
        except scipy.spatial.QhullError:
            return None
        eq = hull.equations
        lower = eq[:, d] < -1e-12 * np.linalg.norm(eq[:, :d + 1], axis=1)
        return np.sort(hull.simplices[lower], axis=1)

    @staticmethod
    def _triangulation_defects(Q, h, T, tolerance=1e-13):
        """
        Certificate for a regular triangulation `T` of `Q` (any dimension
        `d >= 1`): the simplices tile the convex hull of their vertices, and
        across every interior facet the opposite vertex is not in conflict
        with the neighbouring simplex's orthosphere (sign of
        `det[x_i - x_o, h_i - h_o] * orient`, which never divides by a
        sliver's volume).
        """
        n, d = Q.shape
        if len(T) == 1:
            return False
        X = Q[T]
        E = X[:, 1:] - X[:, :1]
        orient = np.linalg.det(E)
        vol = np.abs(orient).sum() / np.prod(np.arange(1, d + 1))
        used = np.unique(T)
        try:
            if d == 1:
                hull_vol = float(np.ptp(Q[used, 0]))
            else:
                hull_vol = scipy.spatial.ConvexHull(Q[used]).volume
        except scipy.spatial.QhullError:
            return True
        if abs(vol - hull_vol) > tolerance * 1e3 * max(hull_vol, 1e-300):
            return True
        # interior facets
        facets = np.concatenate([np.delete(T, k, axis=1) for k in range(d + 1)])
        opp = np.concatenate([T[:, k] for k in range(d + 1)])
        owner = np.tile(np.arange(len(T)), d + 1)
        _, inv = np.unique(facets, axis=0, return_inverse=True)
        inv = inv.reshape(-1)
        order = np.argsort(inv, kind='stable')
        iv = inv[order]
        pair = np.flatnonzero(iv[1:] == iv[:-1])
        t1, o2 = owner[order[pair]], opp[order[pair + 1]]
        Xt = Q[T[t1]]
        M = np.concatenate([Xt - Q[o2][:, None, :], (h[T[t1]] - h[o2][:, None])[..., None]], axis=-1)
        detM = np.linalg.det(M)
        norms = np.prod(np.linalg.norm(M, axis=-1), axis=-1)
        # det(M) / orient = (-1)^(d+1) (power of the vertex - orthosphere size)
        conflict = (-1) ** (d + 1) * np.sign(orient[t1]) * detM / np.where(norms > 0, norms, 1)
        return bool(np.min(conflict, initial=0) < -tolerance)

    def _triangulate_balls(self):
        """
        Regular triangulation of the (non-duplicate) balls in their own affine
        dimension `d` (a planar molecule gives a 2D triangulation, a linear one
        a 1D one), certified and, if needed, re-computed on slightly perturbed
        balls. No bounding balls are used: they would add spurious simplices
        near the hull, and the skin is defined by the real balls alone.

        :return: `(live, P, R, top, d)` -- input indices kept, (projected)
            centers, radii, top-dimensional simplices, affine dimension
        """
        centers, R = self.centers, self.ball_radii
        _, first = np.unique(np.column_stack([centers, R]), axis=0, return_index=True)
        live = np.sort(first)
        P0, R0 = centers[live], R[live]
        nl = len(live)
        shift = P0.mean(axis=0)
        extent = float(np.max(np.ptp(P0, axis=0))) if nl > 1 else 0.0
        scale = max(extent, float(np.max(R0)), 1e-300)
        Pn, Rn = (P0 - shift) / scale, R0 / scale
        # affine dimension; co-planar / co-linear sets (to 1e-8 of the extent)
        # are triangulated in their own plane / line
        if nl > 1:
            _, sv, Vt = np.linalg.svd(Pn, full_matrices=False)
            d = int(np.sum(sv > 1e-8 * max(sv[0], 1e-300)))
        else:
            d, Vt = 0, np.eye(3)
        if d == 0:
            return live, P0, R0, np.zeros((1, 1), dtype=int), 0
        axes = Vt[:d]
        Q0 = Pn @ axes.T
        rng = np.random.default_rng(self.seed)
        dQ, dR = rng.uniform(-1, 1, Q0.shape), rng.uniform(-1, 1, Rn.shape)
        levels = [self.perturbation] + [p for p in self.fallback_perturbations if p > self.perturbation]
        for pert in levels:
            Q = Q0 + pert * dQ
            Rp = Rn * (1 + pert * dR)
            h = np.einsum('ij,ij->i', Q, Q) - Rp ** 2
            T = self._lower_hull(Q, h)
            if T is None or self._triangulation_defects(Q, h, T):
                continue
            P = (Q @ axes) * scale + shift
            return live, P, Rp * scale, T, d
        raise ValueError("could not build a valid regular triangulation of the balls")

    def _build_simplices(self):
        live, P, R, top, dim = self._triangulate_balls()
        R2 = R ** 2
        s = self.shrink
        # all faces of the top simplices, by dimension
        faces = {}
        for k in range(dim + 1):
            sub = np.concatenate([top[:, list(c)] for c in itertools.combinations(range(dim + 1), k + 1)])
            faces[k] = np.unique(np.sort(sub, axis=1), axis=0)
        faces[0] = faces[0] if len(faces[0]) else np.zeros((0, 1), dtype=int)
        # Voronoi vertices bound the Voronoi cells of interior simplices; cells
        # of simplices on the boundary of the triangulation (and all cells when
        # the balls are co-planar or co-linear) are unbounded
        bounded_top = dim == 3
        if bounded_top:
            with np.errstate(all='ignore'):
                YT, _ = AlphaMol._orthospheres(P, R2, top)
            bfacets = np.concatenate([np.delete(top, k, axis=1) for k in range(4)])
            u, cnt = np.unique(np.sort(bfacets, axis=1), axis=0, return_counts=True)
            boundary = u[cnt == 1]
            boundary_keys = {}
            for k in range(3):
                sub = np.concatenate([boundary[:, list(c)] for c in itertools.combinations(range(3), k + 1)])
                boundary_keys[k] = np.unique(np.sort(sub, axis=1), axis=0)

        def rows_in(A, B):
            # mask of rows of A present in B
            if len(B) == 0:
                return np.zeros(len(A), dtype=bool)
            _, inv = np.unique(np.concatenate([A, B]), axis=0, return_inverse=True)
            inv = inv.reshape(-1)
            return np.isin(inv[:len(A)], inv[len(A):])

        groups = []
        for k in range(dim + 1):
            S = faces[k]
            m = len(S)
            if m == 0:
                continue
            if k == 0:
                y = P[S[:, 0]]
                rho2 = -R2[S[:, 0]]
            else:
                y, rho2 = AlphaMol._orthospheres(P, R2, S)
            z0 = P[S[:, 0]]
            basis = np.zeros((m, 3, 3))
            bary = np.zeros((m, 3, 3))
            if k > 0:
                E = P[S[:, 1:]] - z0[:, None, :]                       # (m, k, 3)
                Qm, Rq = np.linalg.qr(np.swapaxes(E, 1, 2))            # E^T = Q Rq
                basis[:, :k, :] = np.swapaxes(Qm, 1, 2)
                # barycentric coordinates 1..k of z in aff(X): l = Rq^-1 Q^T (z - z0)
                bary[:, :k, :] = np.einsum('mij,mxj->mix', np.linalg.inv(Rq), Qm)
            wmax = np.max(R2[S], axis=1)
            Dy = np.max(np.linalg.norm(P[S] - y[:, None, :], axis=-1), axis=1)
            cen = P[S].mean(axis=1)
            circ = np.max(np.linalg.norm(P[S] - cen[:, None, :], axis=-1), axis=1)
            # bounding ball of the mixed cell (1-s) delta_X + s nu_X; lets
            # `_evaluate` touch only points whose mixed cell can be X's
            mix_c, mix_r = cen.copy(), np.full(m, np.inf)
            if bounded_top:
                subs = np.concatenate([top[:, list(c)] for c in itertools.combinations(range(4), k + 1)])
                owner_t = np.tile(np.arange(len(top)), len(subs) // len(top))
                subs = np.sort(subs, axis=1)
                _, inv = np.unique(np.concatenate([S, subs]), axis=0, return_inverse=True)
                inv = inv.reshape(-1)
                slot = -np.ones(inv.max() + 1, dtype=int)
                slot[inv[:m]] = np.arange(m)
                sid = slot[inv[m:]]
                vlo = np.full((m, 3), np.inf)
                vhi = np.full((m, 3), -np.inf)
                np.minimum.at(vlo, sid, YT[owner_t])
                np.maximum.at(vhi, sid, YT[owner_t])
                interior = np.all(np.isfinite(vlo), axis=1)
                if k < 3:
                    interior &= ~rows_in(S, boundary_keys[k])
                nu_c = 0.5 * (vlo + vhi)
                nu_r = 0.5 * np.linalg.norm(vhi - vlo, axis=1)
                mix_c = np.where(interior[:, None], (1 - s) * cen + s * nu_c, cen)
                mix_r = np.where(interior, (1 - s) * circ + s * nu_r, np.inf)
            verts = -np.ones((m, 4), dtype=int)
            verts[:, :k + 1] = live[S]
            groups.append(dict(dim=np.full(m, k), verts=verts, y=y, rho2=rho2, z0=z0,
                               basis=basis, bary=bary, wmax=wmax, centroid=cen, circ=circ,
                               mix_c=mix_c, mix_r=mix_r, Dy=Dy))
        cat = lambda key: np.concatenate([g[key] for g in groups])
        self._simplices = {key: cat(key) for key in
                           ('dim', 'verts', 'y', 'rho2', 'z0', 'basis', 'bary', 'wmax', 'centroid', 'circ',
                            'mix_c', 'mix_r', 'Dy')}
        self._simplices['points'] = P
        self._simplices['affine_dimension'] = dim
        return self._simplices

    @property
    def simplices(self):
        """
        **LLM Docstring**

        Per-patch data: every simplex of the regular triangulation among the
        (non-duplicate) balls, with its dimension, vertices (input indices,
        padded with -1), orthocenter `y`, orthosphere size `rho2`, and an
        orthonormal basis of its direction space.
        """
        if self._simplices is None:
            self._build_simplices()
        return self._simplices

    def patch_counts(self):
        """
        **LLM Docstring**

        :return: number of skin patch types present: `'sphere'` (vertex
            cells), `'edge'`, `'triangle'` (hyperboloid patches) and
            `'tetrahedron'` (inverted spheres)
        :rtype: dict
        """
        sx = self.simplices
        dims = sx['dim']
        return {name: int(np.sum(dims == k)) for k, name in enumerate(('sphere', 'edge', 'triangle', 'tetrahedron'))}

    # ------------------------------------------------------------------
    # the skin function
    # ------------------------------------------------------------------
    def _pair_values(self, x, idx):
        # closed-form F, grad F and mixed-cell feasibility for (point, simplex) pairs
        sx = self.simplices
        s = self.shrink
        c = s / (1 - s)
        n = len(idx)
        k = sx['dim'][idx]
        d = x - sx['y'][idx]
        F = np.empty(n)
        grad = np.empty((n, 3))
        feasible = np.ones(n, dtype=bool)
        rho2 = sx['rho2'][idx]
        tol = 1e-10
        # vertex cells: sphere of radius sqrt(s) R
        m0 = k == 0
        F[m0] = -np.einsum('ij,ij->i', d[m0], d[m0]) - s * rho2[m0]
        grad[m0] = -2 * d[m0]
        # tetrahedron cells: u = d, v = 0
        m3 = k == 3
        if m3.any():
            i3 = idx[m3]
            F[m3] = c * np.einsum('ij,ij->i', d[m3], d[m3]) - s * rho2[m3]
            grad[m3] = 2 * c * d[m3]
            zs = sx['y'][i3] + d[m3] / (1 - s) - sx['z0'][i3]
            lam = np.einsum('mij,mj->mi', sx['bary'][i3], zs)
            feasible[m3] = np.all(lam >= -tol, axis=1) & (lam.sum(1) <= 1 + tol)
        # edge and triangle cells: split d along / across the simplex
        m12 = ~(m0 | m3)
        if m12.any():
            i12 = idx[m12]
            kk = k[m12]
            B = sx['basis'][i12][:, :2]                                  # rows beyond k are zero
            dd = d[m12]
            u = np.einsum('mix,mi->mx', B, np.einsum('mij,mj->mi', B, dd))
            v = dd - u
            F[m12] = c * np.einsum('ij,ij->i', u, u) - np.einsum('ij,ij->i', v, v) - s * rho2[m12]
            grad[m12] = 2 * c * u - 2 * v
            zs = sx['y'][i12] + u / (1 - s) - sx['z0'][i12]
            lam = np.einsum('mij,mj->mi', sx['bary'][i12][:, :2], zs)
            lam[:, 1] = np.where(kk >= 2, lam[:, 1], 0)
            feasible[m12] = np.all(lam >= -tol, axis=1) & (lam.sum(1) <= 1 + tol)
        return F, grad, feasible

    def _query_balls(self, band):
        """
        Per simplex X, two balls that every point governed by X (for the
        purposes of the skin) lies in: its mixed cell's bounding ball (exact
        for all points, finite for interior simplices) and the ball
        `|x - y_X|^2 <= (1-s) D_X^2 - s rho2_X + eps`, which holds whenever
        `F(x) >= -eps` (`D_X` the largest vertex distance from `y_X`, and
        `eps = 2 band sqrt(s w_max) + band^2`, i.e. points within `band` of
        the skin). The smaller one is queried and the other used as a filter.
        """
        sx = self.simplices
        s = self.shrink
        r1 = sx['mix_r'] * (1 + 1e-9) + 1e-9 * float(np.max(self.ball_radii))
        eps = 2 * band * np.sqrt(s * sx['wmax']) + band * band
        r3 = np.sqrt(np.maximum((1 - s) * sx['Dy'] ** 2 - s * sx['rho2'] + eps, 0)) * (1 + 1e-9)
        use1 = r1 <= r3
        qc = np.where(use1[:, None], sx['mix_c'], sx['y'])
        qr = np.where(use1, r1, r3)
        oc = np.where(use1[:, None], sx['y'], sx['mix_c'])
        orr = np.where(use1, r3, r1)
        return qc, qr, oc, orr

    def _evaluate(self, points, band, chunk=2_000_000):
        points = np.asarray(points, dtype=float)
        shape = points.shape[:-1]
        X = points.reshape(-1, 3)
        n = len(X)
        F = np.full(n, -np.inf)
        G = np.zeros((n, 3))
        owner = -np.ones(n, dtype=int)
        if n == 0:
            return F.reshape(shape), G.reshape(shape + (3,)), owner.reshape(shape)
        qc, qr, oc, orr = self._query_balls(band)
        tree = scipy.spatial.cKDTree(X)
        m = len(qr)
        start = 0
        step = min(m, 4096)
        while start < m:
            # simplices in batches so the candidate-pair arrays stay bounded
            while True:
                sl = slice(start, min(start + step, m))
                hits = tree.query_ball_point(qc[sl], qr[sl], return_sorted=False)
                lens = np.fromiter((len(h) for h in hits), dtype=int, count=len(hits))
                if lens.sum() <= chunk or step == 1:
                    break
                step = max(1, step // 2)
            if lens.sum():
                pts = np.concatenate([h for h in hits if len(h)]).astype(int)
                sim = np.repeat(np.arange(sl.start, sl.stop), lens)
                dx = X[pts] - oc[sim]
                keep = np.einsum('ij,ij->i', dx, dx) <= orr[sim] ** 2
                pts, sim = pts[keep], sim[keep]
                f, g, ok = self._pair_values(X[pts], sim)
                f = np.where(ok, f, -np.inf)
                # per-point maximum over the candidate simplices
                np.maximum.at(F, pts, f)
                win = (f == F[pts]) & ok
                G[pts[win]] = g[win]
                owner[pts[win]] = sim[win]
            start = sl.stop
        return F.reshape(shape), G.reshape(shape + (3,)), owner.reshape(shape)

    def skin_function(self, points, return_gradient=False, return_patches=False, band=1.0):
        """
        **LLM Docstring**

        The skin function `F` (positive inside the skin body, zero on the
        skin). Values are exact for every point within `band` of the skin (and,
        in the interior of the triangulation, everywhere); farther points get
        a value that is only guaranteed to be negative (`-inf` if no patch is
        nearby).

        :param points: query points, shape `(..., 3)`
        :param return_gradient: also return `grad F`
        :param return_patches: also return the index (into `simplices`) of the
            patch whose mixed cell contains each point
        :param band: exactness margin, in length units
        :return: `F` (and optionally the gradient and patch indices)
        """
        F, G, owner = self._evaluate(points, band)
        out = [F]
        if return_gradient:
            out.append(G)
        if return_patches:
            out.append(owner)
        return out[0] if len(out) == 1 else tuple(out)

    def contains(self, points, band=1.0):
        """
        **LLM Docstring**

        :return: boolean mask of points inside the skin body
        """
        return self.skin_function(points, band=band) >= 0

    def normals(self, points, band=1.0):
        """
        **LLM Docstring**

        :return: outward unit normals of the level sets of `F` at `points`
            (on the skin: its outward normal)
        """
        _, G = self.skin_function(points, return_gradient=True, band=band)
        with np.errstate(invalid='ignore', divide='ignore'):
            return -G / np.linalg.norm(G, axis=-1)[..., None]

    def _patch_hessians(self, owner):
        sx = self.simplices
        s = self.shrink
        B = sx['basis'][np.maximum(owner, 0)]
        PL = np.einsum('mix,miy->mxy', B, B)
        return 2 * (s / (1 - s)) * PL - 2 * (np.eye(3)[None] - PL)

    def project(self, points, max_iter=30, tol=1e-12, band=1.0, return_patches=False):
        """
        **LLM Docstring**

        Project points onto the skin along the gradient of `F`. Within one
        patch `F` is an exact quadratic, so each step solves
        `F(x + t g/|g|) = 0` in closed form; a step that lands in another
        patch is simply re-evaluated there (`F` is C^1), so points near the
        surface converge in two or three evaluations.

        :param points: starting points, shape `(..., 3)`
        :param tol: stop when `|F| < tol * R^2`
        :param band: initial exactness margin; enlarged automatically for
            points too far from the skin to be evaluated
        :return: `(points_on_skin, outward_normals)` (and patch indices)
        """
        x = np.array(points, dtype=float).reshape(-1, 3)
        # far points: grow the evaluation band until every point is resolved
        far = np.ones(len(x), dtype=bool)
        b = band
        for _ in range(8):
            F, _, _ = self._evaluate(x[far], b)
            far[np.flatnonzero(far)[np.isfinite(F)]] = False
            if not far.any():
                break
            b *= 4
        band = b
        n = len(x)
        scale2 = float(np.max(self.radii)) ** 2
        Fx = np.full(n, np.inf)
        Gx = np.zeros((n, 3))
        own = -np.ones(n, dtype=int)
        active = np.ones(n, dtype=bool)
        cap = float(np.min(self.radii)) * (1 if self.radii_type == 'convex' else np.sqrt(self.shrink))
        for _ in range(max_iter):
            idx = np.flatnonzero(active)
            if len(idx) == 0:
                break
            F, G, o = self._evaluate(x[idx], band)
            Fx[idx], Gx[idx], own[idx] = F, G, o
            done = ~np.isfinite(F) | (np.abs(F) < tol * scale2)
            active[idx[done]] = False
            go = ~done
            if not go.any():
                break
            F, G, o, ii = F[go], G[go], o[go], idx[go]
            gn = np.linalg.norm(G, axis=1)
            ghat = G / np.maximum(gn, 1e-300)[:, None]
            a = np.einsum('mi,mij,mj->m', ghat, self._patch_hessians(o), ghat)
            # root of F + gn t + a t^2 / 2 nearest to t = 0 (stable form)
            disc = gn * gn - 2 * a * F
            with np.errstate(invalid='ignore', divide='ignore'):
                t = np.where(disc >= 0, -2 * F / (gn + np.sqrt(np.maximum(disc, 0))), -F / gn)
            t = np.clip(np.nan_to_num(t), -cap, cap)
            x[ii] += t[:, None] * ghat
        with np.errstate(invalid='ignore', divide='ignore'):
            nrm = -Gx / np.linalg.norm(Gx, axis=1)[:, None]
        shape = np.shape(points)
        out = (x.reshape(shape), nrm.reshape(shape))
        return out + (own.reshape(shape[:-1]),) if return_patches else out

    def curvatures(self, points, band=1.0):
        """
        **LLM Docstring**

        Mean (`(k1 + k2)/2`, positive on convex caps) and Gaussian curvature of
        the level set of `F` through each point; exact on the skin, where each
        patch is a quadric with constant Hessian
        `2 [s/(1-s) P_parallel - P_perp]`.

        :return: `(mean, gaussian)`
        """
        F, G, owner = self._evaluate(np.asarray(points, dtype=float).reshape(-1, 3), band)
        # f = -F increases outward: grad f = -G, Hess f = -Hess F
        H = -self._patch_hessians(owner)
        g = -G
        gn = np.linalg.norm(g, axis=1)
        tr = np.trace(H, axis1=1, axis2=2)
        gHg = np.einsum('mi,mij,mj->m', g, H, g)
        adj = self._adjugate(H)
        with np.errstate(invalid='ignore', divide='ignore'):
            mean = (gn ** 2 * tr - gHg) / (2 * gn ** 3)
            gauss = np.einsum('mi,mij,mj->m', g, adj, g) / gn ** 4
        shape = np.shape(points)[:-1]
        return mean.reshape(shape), gauss.reshape(shape)

    @staticmethod
    def _adjugate(H):
        a = H
        c = np.empty_like(a)
        c[:, 0, 0] = a[:, 1, 1] * a[:, 2, 2] - a[:, 1, 2] * a[:, 2, 1]
        c[:, 0, 1] = a[:, 0, 2] * a[:, 2, 1] - a[:, 0, 1] * a[:, 2, 2]
        c[:, 0, 2] = a[:, 0, 1] * a[:, 1, 2] - a[:, 0, 2] * a[:, 1, 1]
        c[:, 1, 0] = a[:, 1, 2] * a[:, 2, 0] - a[:, 1, 0] * a[:, 2, 2]
        c[:, 1, 1] = a[:, 0, 0] * a[:, 2, 2] - a[:, 0, 2] * a[:, 2, 0]
        c[:, 1, 2] = a[:, 0, 2] * a[:, 1, 0] - a[:, 0, 0] * a[:, 1, 2]
        c[:, 2, 0] = a[:, 1, 0] * a[:, 2, 1] - a[:, 1, 1] * a[:, 2, 0]
        c[:, 2, 1] = a[:, 0, 1] * a[:, 2, 0] - a[:, 0, 0] * a[:, 2, 1]
        c[:, 2, 2] = a[:, 0, 0] * a[:, 1, 1] - a[:, 0, 1] * a[:, 1, 0]
        return c

    # ------------------------------------------------------------------
    # meshing
    # ------------------------------------------------------------------
    def bounding_box(self, padding=None):
        """
        **LLM Docstring**

        :return: `(lo, hi)` corners of a box containing the skin body (the
            union of the shrunk balls lies inside the union of the balls)
        """
        pad = 0 if padding is None else padding
        R = self.ball_radii
        return (np.min(self.centers - R[:, None], axis=0) - pad,
                np.max(self.centers + R[:, None], axis=0) + pad)

    @staticmethod
    def marching_tetrahedra(values, origin, spacing):
        """
        **LLM Docstring**

        Vectorized marching tetrahedra (Kuhn split of every grid cube) for the
        level set `values = 0`, with `values > 0` inside. Returns a
        watertight mesh whose triangles are oriented outward.

        :param values: grid values, shape `(nx, ny, nz)`
        :param origin: coordinates of grid node `(0, 0, 0)`
        :param spacing: grid spacing (scalar or per axis)
        :return: `(verts, tris)`
        """
        values = np.asarray(values, dtype=float)
        nx, ny, nz = values.shape
        spacing = np.broadcast_to(np.asarray(spacing, dtype=float), (3,))
        origin = np.asarray(origin, dtype=float)
        inside = values > 0
        # cubes with a sign change anywhere
        cube = np.stack([inside[i:nx - 1 + i, j:ny - 1 + j, k:nz - 1 + k]
                         for i in (0, 1) for j in (0, 1) for k in (0, 1)], -1)
        mixed = np.flatnonzero((cube.any(-1) & ~cube.all(-1)).ravel())
        if len(mixed) == 0:
            return np.zeros((0, 3)), np.zeros((0, 3), dtype=int)
        cidx = np.stack(np.unravel_index(mixed, (nx - 1, ny - 1, nz - 1)), -1)   # (c, 3)
        corners = cidx[:, None, None, :] + _KUHN[None]                           # (c, 6, 4, 3)
        corners = corners.reshape(-1, 4, 3)
        node = np.ravel_multi_index(corners.reshape(-1, 3).T, (nx, ny, nz)).reshape(-1, 4)
        val = values.ravel()[node]
        ins = val > 0
        cnt = ins.sum(1)
        tris_nodes = []    # list of (m, 3, 2) arrays of edge endpoints (global node ids)
        orient_in = []     # (m, 3) coordinates of mean inside corner
        orient_out = []
        coords = lambda nd: origin + np.stack(np.unravel_index(nd, (nx, ny, nz)), -1) * spacing

        def emit(sel, edge_lists):
            for el in edge_lists:
                ends = np.stack([node[sel][:, list(_TET_EDGES[e])] for e in el], 1)   # (m, 3, 2)
                tris_nodes.append(ends)
                w_in = ins[sel][:, :, None]
                pts = coords(node[sel].ravel()).reshape(-1, 4, 3)
                orient_in.append((pts * w_in).sum(1) / np.maximum(w_in.sum(1), 1))
                orient_out.append((pts * ~w_in).sum(1) / np.maximum((~w_in).sum(1), 1))

        for k in range(4):
            one_in = (cnt == 1) & ins[:, k]
            one_out = (cnt == 3) & ~ins[:, k]
            for sel in (one_in, one_out):
                if sel.any():
                    emit(sel, [_ONE[k]])
        for (a, b), (e0, e1, e2, e3) in _TWO.items():
            sel = (cnt == 2) & ins[:, a] & ins[:, b]
            if sel.any():
                emit(sel, [(e0, e1, e2), (e0, e2, e3)])
        ends = np.concatenate(tris_nodes)                                         # (t, 3, 2)
        c_in, c_out = np.concatenate(orient_in), np.concatenate(orient_out)
        # one mesh vertex per crossed grid edge
        key = np.sort(ends, axis=-1)
        flat = key.reshape(-1, 2)
        uniq, inv = np.unique(flat[:, 0] * (nx * ny * nz) + flat[:, 1], return_inverse=True)
        a_nd, b_nd = uniq // (nx * ny * nz), uniq % (nx * ny * nz)
        va, vb = values.ravel()[a_nd], values.ravel()[b_nd]
        t = va / (va - vb)
        verts = coords(a_nd) + t[:, None] * (coords(b_nd) - coords(a_nd))
        tris = inv.reshape(-1, 3)
        # orient each triangle so its normal points from the inside corners out
        p0, p1, p2 = verts[tris[:, 0]], verts[tris[:, 1]], verts[tris[:, 2]]
        nrm = np.cross(p1 - p0, p2 - p0)
        flip = np.einsum('ij,ij->i', nrm, c_out - c_in) < 0
        tris[flip] = tris[flip][:, [0, 2, 1]]
        # drop triangles degenerated by coincident vertices
        ok = (tris[:, 0] != tris[:, 1]) & (tris[:, 1] != tris[:, 2]) & (tris[:, 0] != tris[:, 2])
        return verts, tris[ok]

    def _hessian_bound(self):
        s = self.shrink
        return 2 * max(1.0, s / (1 - s))

    def grid_values(self, lo, spacing, shape, coarsening=4):
        """
        **LLM Docstring**

        Exact skin-function values on the regular grid
        `lo + spacing * (i, j, k)` wherever the skin can cross a grid cell,
        using a coarse pass to skip cells certified to contain no zero:
        `F` is C^1 with Hessian norm at most `H = 2 max(1, s/(1-s))`, so a
        coarse corner with `|F| > |grad F| d + H d^2 / 2` (`d` the coarse cell
        diagonal) rules out a crossing anywhere in its cell. Skipped nodes get
        `+1` / `-1` according to the side they are on.

        :return: array of shape `shape`
        """
        shape = tuple(int(n) for n in shape)
        k = max(1, int(coarsening))
        nc = [(n - 1) // k + 2 for n in shape]                  # coarse nodes covering the fine grid
        H = k * spacing
        d = H * np.sqrt(3)
        axes = [lo[i] + H * np.arange(nc[i]) for i in range(3)]
        cg = np.stack(np.meshgrid(*axes, indexing='ij'), -1)
        Fc, Gc, _ = self._evaluate(cg, band=1.5 * d + spacing)
        with np.errstate(invalid='ignore'):
            certain = ~np.isfinite(Fc) | (np.abs(Fc) > np.linalg.norm(Gc, axis=-1) * d + 0.5 * self._hessian_bound() * d * d)
        sign_c = np.where(np.isfinite(Fc) & (Fc > 0), 1.0, -1.0)
        # a coarse cell needs refinement unless one of its corners certifies it
        cert_cell = np.zeros([n - 1 for n in nc], dtype=bool)
        sign_cell = np.zeros([n - 1 for n in nc])
        for a in (0, 1):
            for b in (0, 1):
                for c in (0, 1):
                    sl = (slice(a, nc[0] - 1 + a), slice(b, nc[1] - 1 + b), slice(c, nc[2] - 1 + c))
                    newly = certain[sl] & ~cert_cell
                    sign_cell[newly] = sign_c[sl][newly]
                    cert_cell |= certain[sl]
        # fine grid: fill from certified coarse cells, evaluate the rest exactly
        up = lambda arr: np.repeat(np.repeat(np.repeat(arr, k, 0), k, 1), k, 2)
        big = [(n - 1) * k for n in nc]
        vals = np.zeros(big)
        vals[:] = up(sign_cell)
        need_cell = up(~cert_cell)
        vals = np.pad(vals, ((0, 1), (0, 1), (0, 1)), mode='edge')
        need = np.pad(need_cell, ((0, 1), (0, 1), (0, 1)), mode='constant')
        # nodes on the far faces of refined cells too
        need[1:] |= need[:-1].copy(); need[:, 1:] |= need[:, :-1].copy(); need[:, :, 1:] |= need[:, :, :-1].copy()
        vals = np.ascontiguousarray(vals[:shape[0], :shape[1], :shape[2]])
        need = need[:shape[0], :shape[1], :shape[2]]
        idx = np.flatnonzero(need)
        if len(idx):
            pts = lo + spacing * np.stack(np.unravel_index(idx, shape), -1)
            F, _, _ = self._evaluate(pts, band=3 * spacing)
            vals.reshape(-1)[idx] = np.where(np.isfinite(F), F, -1.0)
        return vals

    def triangulate(self, spacing=0.25, project=True, coarsening=4):
        """
        **LLM Docstring**

        Triangulate the skin: evaluate `F` exactly on a grid (skipping cells
        certified not to meet the skin), extract the zero set by marching
        tetrahedra, then (by default) Newton-project the vertices onto the
        skin and attach exact normals.

        :param spacing: grid spacing, in length units
        :param project: project the vertices onto `F = 0`
        :param coarsening: coarse-to-fine factor for skipping empty cells (1 disables it)
        :return: the mesh
        :rtype: SkinSurfaceMesh
        """
        key = (float(spacing), bool(project))
        if key in self._mesh_cache:
            return self._mesh_cache[key]
        lo, hi = self.bounding_box(padding=2 * spacing)
        n = np.ceil((hi - lo) / spacing).astype(int) + 1
        F = self.grid_values(lo, spacing, n, coarsening=coarsening)
        verts, tris = self.marching_tetrahedra(F, lo, spacing)
        patches = None
        normals = None
        if len(verts):
            if project:
                verts, normals, patches = self.project(verts, band=spacing, return_patches=True)
            else:
                normals = self.normals(verts, band=spacing)
        mesh = SkinSurfaceMesh(verts, tris, normals=normals, patches=patches, skin=self, spacing=spacing)
        self._mesh_cache[key] = mesh
        return mesh

    def surface_area(self, spacing=0.25):
        """
        **LLM Docstring**

        Skin area from the projected mesh (error `O(spacing^2)`).
        """
        return self.triangulate(spacing=spacing).surface_area()

    def volume(self, spacing=0.25):
        """
        **LLM Docstring**

        Volume enclosed by the skin, from the projected mesh (error `O(spacing^2)`).
        """
        return self.triangulate(spacing=spacing).volume()
