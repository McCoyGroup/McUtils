"""
Intrinsic volumes (surface area, volume, integrated mean and Gaussian curvature)
of a union of balls, following the AlphaMol construction of

    P. Koehl, A. Akopyan, H. Edelsbrunner,
    "Computing the Volume, Surface Area, Mean, and Gaussian Curvatures of
    Molecules and Their Derivatives", J. Chem. Inf. Model. 63, 973-985 (2023)

and ported from the reference C++ implementation (github.com/pkoehl/AlphaMol,
`Alphacx/alfcx.h`, `Volumes/volumes.h`, `Volumes/tetra.h`,
`Volumes/gauss_corners.h`).

Relative to the `UnionBall` path already in `SphereUnionSurface`, the
differences are

1. The dual complex is extracted from the regular triangulation with the
   standard alpha-shape rules (orthosphere size + attachment test against the
   link of each simplex), computed in closed form and fully vectorized,
   instead of one SLSQP solve per candidate simplex.
2. The measures use the *short*, angle-weighted inclusion-exclusion formula
   (paper eqs. 5, 7, 13, 15): each tetrahedron of the dual complex only
   modifies the weights of its vertices / edges / triangles and contributes the
   Voronoi-partitioned volume of the tetrahedron itself, so no four-ball
   (Gibson-Scheraga quadruple) intersection is ever evaluated. Only 1-, 2- and
   3-ball quantities appear, all of which are simple and numerically stable.
3. Everything is expressed through inter-center distances, so it is
   rotation/translation invariant by construction.

Gradients with respect to the ball centers (paper eqs. 11-19) are provided by
`gradients` / `weighted_gradient`. The curvature terms use the paper's
distance-derivative formulas; the volume and area terms default to the
equivalent Cartesian Voronoi-face formulas of the paper's refs. 60/61, since
the distance-derivative of the tetrahedron Voronoi pieces (eq. 12) loses
accuracy like eps / sin^3 on the sliver tetrahedra that ring systems and
symmetric structures produce.

Degenerate inputs (co-spherical / co-planar weighted points, exact duplicates)
are handled by (i) a tiny deterministic perturbation of the centers and radii
(a floating-point stand-in for AlphaMol's simulation of simplicity), escalated
automatically if Qhull's triangulation fails a tiling + local-regularity
certificate, (ii) four zero-radius "dummy" balls outside the molecule that make
the triangulation full-dimensional for any input (these never enter the dual
complex), and (iii) pruning of balls wholly contained in another ball.
Everything downstream is evaluated on the same (perturbed) geometry the
triangulation was certified for.
"""

import numpy as np
import scipy.spatial

__all__ = [
    "AlphaMol"
]

# vertex pairs of a tetrahedron (a, b, c, d), in AlphaMol's dihedral ordering
# alpha_ab, alpha_ac, alpha_ad, alpha_bc, alpha_bd, alpha_cd
_TET_EDGES = np.array([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]])
# face opposite vertex k
_TET_FACES = np.array([[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]])
# edges of a sorted triangle (a, b, c) -> ab, ac, bc, and the vertex opposite each
_TRI_EDGES = np.array([[0, 1], [0, 2], [1, 2]])
_TRI_OPP = np.array([2, 1, 0])
# symmetric (vertex, vertex) -> tetrahedron edge index lookup
_PAIR_INDEX = -np.ones((4, 4), dtype=int)
for _k, (_i, _j) in enumerate(_TET_EDGES):
    _PAIR_INDEX[_i, _j] = _PAIR_INDEX[_j, _i] = _k


class AlphaMol:
    """
    **LLM Docstring**

    The AlphaMol dual complex of a union of balls, together with its four
    intrinsic measures and their per-ball decompositions.

    Construction is lazy: the regular triangulation and dual complex are built
    on first access and cached, so a single `AlphaMol` can serve every measure.

    ```python
    am = AlphaMol(coords, radii)
    am.volume, am.surface_area, am.mean_curvature, am.gaussian_curvature
    am.ball_volumes                               # per-ball contributions
    am.weighted_measures(volume=-p, surface_area=sigma)   # eq. 2 / 17
    am.volume_gradient                            # (n, 3), d V / d centers
    am.weighted_gradient(volume=-p, surface_area=sigma)   # eq. 19
    ```

    Mean curvature follows the paper's convention, `M = int (k1 + k2)/2 dA`
    over the smooth patches, with each concave crease contributing
    `-(1/2) phi L` (`phi` the angle between the sphere normals, `L` its exposed
    length), so a sphere gives `4 pi r`. Gaussian curvature totals `2 pi chi`
    of the boundary.

    Volume and area are C^1 in the centers everywhere; the curvature measures
    are not differentiable at exactly degenerate configurations (e.g. four
    spheres through a common point, as in a perfectly regular ring), so their
    gradients there are one-sided values that depend on how the degeneracy is
    resolved.
    """

    default_perturbation = 1e-9
    fallback_perturbations = (1e-8, 1e-7, 1e-6)
    default_dummy_distance = 3.0

    def __init__(self, centers, radii, *,
                 perturbation=None,
                 seed=1729,
                 prune_contained=True,
                 containment_tolerance=1e-10,
                 dummy_distance=None,
                 joggle=False):
        """
        **LLM Docstring**

        :param centers: ball centers, shape `(n, 3)`
        :type centers: np.ndarray
        :param radii: ball radii, shape `(n,)`
        :type radii: np.ndarray
        :param perturbation: relative size of the deterministic perturbation of
            centers and radii used to put the weighted points in general
            position; it is escalated through `fallback_perturbations` if the
            triangulation fails its certificate. `0` requests none (exact
            input), with the same fallback.
        :type perturbation: float | None
        :param seed: RNG seed for that perturbation (results are deterministic)
        :type seed: int
        :param prune_contained: drop balls wholly contained in another ball (and
            exact duplicates) before triangulating
        :type prune_contained: bool
        :param containment_tolerance: relative tolerance for that pruning
        :type containment_tolerance: float
        :param dummy_distance: distance (in units of the molecule's extent) of
            the four zero-radius bounding balls
        :type dummy_distance: float | None
        :param joggle: additionally pass Qhull's `QJ` option
        :type joggle: bool
        """
        centers = np.asarray(centers, dtype=float)
        radii = np.asarray(radii, dtype=float)
        if centers.ndim != 2 or centers.shape[1] != 3:
            raise ValueError("centers must have shape (n, 3)")
        if radii.shape != (len(centers),):
            raise ValueError("radii must have shape (n,)")
        if not (np.all(np.isfinite(centers)) and np.all(np.isfinite(radii))):
            raise ValueError("centers and radii must be finite")
        if np.any(radii < 0):
            raise ValueError("radii must be non-negative")
        self.centers = centers
        self.radii = radii
        self.perturbation = self.default_perturbation if perturbation is None else perturbation
        self.seed = seed
        self.prune_contained = prune_contained
        self.containment_tolerance = containment_tolerance
        self.dummy_distance = self.default_dummy_distance if dummy_distance is None else dummy_distance
        self.joggle = joggle
        self._complex = None
        self._measures = None
        self._derivative_cache = None
        self._face_cache = None

    # ------------------------------------------------------------------
    # preprocessing
    # ------------------------------------------------------------------
    @classmethod
    def contained_ball_mask(cls, centers, radii, tolerance=0):
        """
        **LLM Docstring**

        Mask of balls that survive removal of every ball wholly contained in
        another ball (exact duplicates keep their lowest index). Uses a KD-tree
        so only pairs closer than `max(r) - min(r)` are examined.

        :param centers: ball centers
        :param radii: ball radii
        :param tolerance: absolute length tolerance for the containment test
        :return: boolean keep-mask
        :rtype: np.ndarray
        """
        n = len(radii)
        keep = radii > 0
        if n < 2:
            return keep
        reach = float(np.max(radii) - np.min(radii)) + tolerance
        tree = scipy.spatial.cKDTree(centers)
        pairs = tree.query_pairs(reach, output_type='ndarray')
        if len(pairs) == 0:
            return keep
        i, j = pairs[:, 0], pairs[:, 1]
        d = np.linalg.norm(centers[i] - centers[j], axis=1)
        i_in_j = d + radii[i] <= radii[j] + tolerance
        j_in_i = d + radii[j] <= radii[i] + tolerance
        # ties (identical balls) drop the larger index
        drop_i = i_in_j & ~(j_in_i & (i < j))
        drop_j = j_in_i & ~drop_i
        keep[i[drop_i]] = False
        keep[j[drop_j]] = False
        return keep

    # ------------------------------------------------------------------
    # regular triangulation + dual complex
    # ------------------------------------------------------------------
    @staticmethod
    def _orthospheres(P, R2, S):
        """
        **LLM Docstring**

        Batched orthocenters `y` (the point of equal power in the affine hull of
        each simplex) and squared orthoradii `rho2 = |y - z_i|^2 - r_i^2` for the
        simplices `S` (shape `(m, k+1)`), all of the same dimension `k >= 1`.

        :return: `(y, rho2)`
        """
        z0 = P[S[:, 0]]
        E = P[S[:, 1:]] - z0[:, None, :]
        # 2 e_j . d = |e_j|^2 - r_j^2 + r_0^2, with d = y - z_0 in span(e_j)
        b = 0.5 * (np.einsum('mix,mix->mi', E, E) - R2[S[:, 1:]] + R2[S[:, 0]][:, None])
        with np.errstate(all='ignore'):
            if E.shape[1] == 3:
                # square system: solve it directly -- going through the Gram
                # matrix would square the condition number of sliver tetrahedra
                try:
                    d = np.linalg.solve(E, b[..., None])[..., 0]
                except np.linalg.LinAlgError:
                    d = np.einsum('mij,mj->mi', np.linalg.pinv(E), b)
            else:
                # d = Q R^-T b from E^T = Q R (well conditioned for thin triangles too)
                Q, Rq = np.linalg.qr(np.swapaxes(E, 1, 2))
                try:
                    lam = np.linalg.solve(np.swapaxes(Rq, 1, 2), b[..., None])[..., 0]
                except np.linalg.LinAlgError:
                    lam = np.einsum('mij,mj->mi', np.linalg.pinv(np.swapaxes(Rq, 1, 2)), b)
                d = np.einsum('mxi,mi->mx', Q, lam)
            rho2 = np.einsum('mx,mx->m', d, d) - R2[S[:, 0]]
        rho2[~np.isfinite(rho2)] = np.inf
        return z0 + d, rho2

    @classmethod
    def _triangulation_defects(cls, Pa, R2, dummies, T, tolerance=1e-13):
        """
        Two cheap certificates that `T` is a valid regular triangulation of the
        (normalized) weighted points: the tetrahedra tile the dummy
        tetrahedron exactly (no overlaps / inverted cells), and every interior
        triangle is locally regular (the vertex across it is not in conflict
        with the orthosphere). Qhull's `Qt` output can violate both when it
        merges nearly co-hyperplanar lifted facets.
        """
        X = Pa[T]
        vol = np.abs(np.einsum('ij,ij->i', np.cross(X[:, 1] - X[:, 0], X[:, 2] - X[:, 0]), X[:, 3] - X[:, 0])) / 6
        D = dummies
        hull_vol = abs(np.dot(np.cross(D[1] - D[0], D[2] - D[0]), D[3] - D[0])) / 6
        tiling_error = abs(vol.sum() - hull_vol) / hull_vol
        faces = np.sort(T[:, _TET_FACES].reshape(-1, 3), axis=1)
        _, inv = np.unique(faces, axis=0, return_inverse=True)
        inv = inv.reshape(-1)
        order = np.argsort(inv, kind='stable')
        iv = inv[order]
        pair = np.flatnonzero(iv[1:] == iv[:-1])
        t1 = order[pair] // 4
        o2 = T.reshape(-1)[order[pair + 1]]
        # power of o2 w.r.t. the orthosphere of t1, minus its size, is
        # det(M) / orient(t1) with M = [x_i - x_o, h_i - h_o]; testing the sign
        # of det(M) * orient(t1) avoids dividing by a sliver's tiny volume
        h = np.einsum('ij,ij->i', Pa, Pa) - R2
        Xt = Pa[T[t1]]
        M = np.concatenate([Xt - Pa[o2][:, None, :], (h[T[t1]] - h[o2][:, None])[..., None]], axis=-1)
        orient = np.linalg.det(Xt[:, 1:] - Xt[:, :1])
        detM = np.linalg.det(M)
        norms = np.prod(np.linalg.norm(M, axis=-1), axis=-1)
        conflict = np.sign(orient) * detM / np.where(norms > 0, norms, 1)
        worst = -float(np.min(conflict, initial=0))
        return tiling_error > tolerance or worst > tolerance, (tiling_error, worst)

    @classmethod
    def _regular_triangulation(cls, Pa, R2, dummies, joggle=False):
        """
        Regular (weighted Delaunay) triangulation from the lower hull of the
        lifted points `(x, |x|^2 - r^2)`, validated with
        `_triangulation_defects`.

        :return: `(T, diagnostics)`, with `T = None` when the certificate fails
        """
        lifted = np.column_stack([Pa, np.einsum('ij,ij->i', Pa, Pa) - R2])
        opts = 'Qt Qx QbB QJ' if joggle else 'Qt Qx QbB'
        try:
            hull = scipy.spatial.ConvexHull(lifted, qhull_options=opts)
        except scipy.spatial.QhullError as exc:
            return None, str(exc).splitlines()[0]
        eq = hull.equations
        lower = eq[:, 3] < -1e-12 * np.linalg.norm(eq[:, :4], axis=1)
        T = np.sort(hull.simplices[lower], axis=1)
        bad, diag = cls._triangulation_defects(Pa, R2, dummies, T)
        return (None if bad else T), diag

    def _build_complex(self):
        centers, radii = self.centers, self.radii
        n = len(radii)
        extent = float(np.max(np.ptp(centers, axis=0))) if n > 1 else 0.0
        scale = max(extent, float(np.max(radii)) if n else 0.0, 1e-300)

        keep = np.ones(n, dtype=bool) & (radii > 0)
        if self.prune_contained and n > 0:
            keep = self.contained_ball_mask(centers, radii, self.containment_tolerance * scale)
        live = np.flatnonzero(keep)
        nl = len(live)

        cx = {'live': live, 'scale': scale, 'n': n}
        if nl == 0:
            cx.update(empty=True)
            return cx

        shift = centers[live].mean(axis=0)
        P0 = (centers[live] - shift) / scale
        R0 = radii[live] / scale
        # four zero-radius balls far outside everything: the lifted point set is
        # then always full-dimensional, and these never enter the dual complex
        span = max(float(np.max(np.linalg.norm(P0, axis=1))) + float(np.max(R0)), 1.0)
        dummies = self.dummy_distance * span * np.array(
            [[1., 1., 1.], [1., -1., -1.], [-1., 1., -1.], [-1., -1., 1.]]
        )
        is_dummy = np.arange(nl + 4) >= nl

        # Qhull's output is certified (`_triangulation_defects`); if it fails on
        # (near-)degenerate input, retry on a slightly perturbed copy of the
        # balls -- a floating-point stand-in for AlphaMol's simulation of
        # simplicity. Everything downstream (dual complex, measures,
        # gradients) is then evaluated on that same perturbed geometry, so the
        # combinatorics and the geometry always agree.
        levels = [self.perturbation] + [p for p in self.fallback_perturbations if p > self.perturbation]
        rng = np.random.default_rng(self.seed)
        dP = rng.uniform(-1, 1, P0.shape)
        dR = rng.uniform(-1, 1, R0.shape)
        T = None
        for pert in levels:
            P = P0 + pert * dP
            R = R0 * (1 + pert * dR)
            Pa = np.concatenate([P, dummies])
            R2 = np.concatenate([R ** 2, np.zeros(4)])
            T, diag = self._regular_triangulation(Pa, R2, dummies, joggle=self.joggle)
            if T is not None:
                break
        if T is None:
            raise ValueError(
                "could not build a valid regular triangulation (tiling / regularity defects {}); "
                "check for non-finite or wildly scaled input".format(diag)
            )
        cx['perturbation'] = pert
        m = len(T)

        # --- faces (each with its <= 2 cofaces) ---
        F_all = T[:, _TET_FACES].reshape(-1, 3)
        F, finv = np.unique(F_all, axis=0, return_inverse=True)
        finv = finv.reshape(-1)
        tet_faces = finv.reshape(m, 4)
        cof_face = finv
        cof_opp = T.reshape(-1)
        # --- edges (each with the third vertex of every face containing it) ---
        E_all = F[:, _TRI_EDGES].reshape(-1, 2)
        E, einv = np.unique(E_all, axis=0, return_inverse=True)
        einv = einv.reshape(-1)
        face_edges = einv.reshape(len(F), 3)
        link_edge = einv
        link_opp = F[:, _TRI_OPP].reshape(-1)
        # tetrahedron edge ids in (ab, ac, ad, bc, bd, cd) order
        f_abc, f_abd, f_bcd = face_edges[tet_faces[:, 3]], face_edges[tet_faces[:, 2]], face_edges[tet_faces[:, 0]]
        tet_edges = np.column_stack([f_abc[:, 0], f_abc[:, 1], f_abd[:, 1], f_abc[:, 2], f_abd[:, 2], f_bcd[:, 2]])

        # --- sizes / attachment ---
        def sizes(S):
            rho2 = np.full(len(S), np.inf)
            real = ~np.any(is_dummy[S], axis=1)
            y = np.zeros((len(S), 3))
            if real.any():
                y[real], rho2[real] = self._orthospheres(Pa, R2, S[real])
            return y, rho2

        def attached(y, rho2, owner, opp, count):
            ok = ~is_dummy[opp] & np.isfinite(rho2[owner])
            owner, opp = owner[ok], opp[ok]
            pw = np.einsum('mx,mx->m', y[owner] - Pa[opp], y[owner] - Pa[opp]) - R2[opp]
            att = np.zeros(count, dtype=bool)
            att[owner[pw < rho2[owner]]] = True
            return att

        _, rho2_t = sizes(T)
        tetK = rho2_t < 0
        # Voronoi vertices of *every* tetrahedron (dummy ones included) bound the
        # Voronoi faces used by the Cartesian volume/area gradients
        with np.errstate(all='ignore'):
            y_t_all, _ = self._orthospheres(Pa, R2, T)
        # the (at most two) cofaces of each triangle
        order = np.argsort(cof_face, kind='stable')
        cf = cof_face[order]
        first = np.r_[True, cf[1:] != cf[:-1]]
        face_tets = -np.ones((len(F), 2), dtype=int)
        face_tets[cf[first], 0] = order[first] // 4
        face_tets[cf[~first], 1] = order[~first] // 4

        y_f, rho2_f = sizes(F)
        faceK = (rho2_f < 0) & ~attached(y_f, rho2_f, cof_face, cof_opp, len(F))
        faceK[tet_faces[tetK].reshape(-1)] = True

        y_e, rho2_e = sizes(E)
        edgeK = (rho2_e < 0) & ~attached(y_e, rho2_e, link_edge, link_opp, len(E))
        edgeK[face_edges[faceK].reshape(-1)] = True

        in_tri = np.zeros(nl + 4, dtype=bool)
        in_tri[T.reshape(-1)] = True
        vi = np.concatenate([E[:, 0], E[:, 1]])
        vq = np.concatenate([E[:, 1], E[:, 0]])
        ok = ~is_dummy[vi] & ~is_dummy[vq]
        vi, vq = vi[ok], vq[ok]
        v_att = np.zeros(nl + 4, dtype=bool)
        v_att[vi[np.sum((Pa[vi] - Pa[vq]) ** 2, axis=1) - R2[vq] < -R2[vi]]] = True
        vertK = in_tri & ~is_dummy & (R2 > 0) & ~v_att
        vertK[E[edgeK].reshape(-1)] = True
        vertK = vertK[:nl]

        cx.update(
            empty=False,
            P=P, R=R,
            tetrahedra=T[tetK], tet_edges=tet_edges[tetK], tet_faces=tet_faces[tetK],
            triangles=F, triangle_edges=face_edges, triangle_mask=faceK,
            edges=E, edge_mask=edgeK,
            vertex_mask=vertK,
            all_points=Pa, all_R2=R2, is_dummy=is_dummy,
            voronoi_vertices=y_t_all, face_tets=face_tets,
            link_edge=link_edge, link_opp=link_opp, link_face=np.repeat(np.arange(len(F)), 3),
            edge_centers=y_e, edge_rho2=rho2_e,
            n_delaunay_tetrahedra=int(np.sum(~np.any(is_dummy[T], axis=1)))
        )
        return cx

    @property
    def dual_complex(self):
        """
        **LLM Docstring**

        The dual (alpha = 0) complex, keyed by dimension, as arrays of
        *original* ball indices: `{0: (nv,), 1: (ne, 2), 2: (nf, 3), 3: (nt, 4)}`.
        """
        cx = self._get_complex()
        if cx['empty']:
            return {0: np.zeros(0, int), 1: np.zeros((0, 2), int),
                    2: np.zeros((0, 3), int), 3: np.zeros((0, 4), int)}
        live = cx['live']
        return {
            0: live[np.flatnonzero(cx['vertex_mask'])],
            1: live[cx['edges'][cx['edge_mask']]],
            2: live[cx['triangles'][cx['triangle_mask']]],
            3: live[cx['tetrahedra']],
        }

    def _get_complex(self):
        if self._complex is None:
            self._complex = self._build_complex()
        return self._complex

    # ------------------------------------------------------------------
    # geometric kernels (vectorized ports of AlphaMol's Volumes/*.h)
    # ------------------------------------------------------------------
    @staticmethod
    def _plane_dist(ra2, rb2, rab2):
        # fraction of |AB| between B and the radical plane of A and B
        return 0.5 - (ra2 - rb2) / (2 * rab2)

    @staticmethod
    def tetra_dihedrals(r12sq, r13sq, r14sq, r23sq, r24sq, r34sq, volume=None):
        """
        **LLM Docstring**

        Dihedral angles of tetrahedra from squared edge lengths (Cayley-Menger
        minors, Yang & Zeng), ordered `alpha12, alpha13, alpha14, alpha23,
        alpha24, alpha34` (the angle *around* each edge).

        Unlike the reference code, the sines are obtained from
        `sin(alpha_ij) = 3 V L_ij / (2 A_f A_g)` rather than `sin(acos(cos))`,
        which keeps near-flat (sliver) tetrahedra -- common for co-planar
        rings -- finite; pass `volume` (computed from coordinates) when
        available, otherwise it comes from the Cayley-Menger determinant.

        :return: `(angle / 2 pi, cos, sin)`, each of shape `(..., 6)`
        """
        val234 = r34sq - r23sq - r24sq
        val134 = r34sq - r14sq - r13sq
        val124 = r24sq - r12sq - r14sq
        val123 = r23sq - r12sq - r13sq
        with np.errstate(all='ignore'):
            v4 = 1 / np.sqrt(np.abs(val234 * val234 - 4 * r23sq * r24sq))
            v3 = 1 / np.sqrt(np.abs(val134 * val134 - 4 * r13sq * r14sq))
            v2 = 1 / np.sqrt(np.abs(val124 * val124 - 4 * r12sq * r14sq))
            v1 = 1 / np.sqrt(np.abs(val123 * val123 - 4 * r12sq * r13sq))
        det12 = -2 * r12sq * val134 - val123 * val124
        det13 = -2 * r13sq * val124 - val123 * val134
        det14 = -2 * r14sq * val123 - val124 * val134
        val213 = r13sq - r12sq - r23sq
        val214 = r14sq - r12sq - r24sq
        val312 = r12sq - r13sq - r23sq
        val314 = r14sq - r13sq - r34sq
        val324 = r24sq - r23sq - r34sq
        det23 = -2 * r23sq * val214 - val213 * val234
        det24 = -2 * r24sq * val213 - val214 * val234
        det34 = -2 * r34sq * val312 - val314 * val324
        cos = np.stack([
            det12 * v1 * v2, det13 * v1 * v3, det14 * v2 * v3,
            det23 * v1 * v4, det24 * v2 * v4, det34 * v3 * v4
        ], axis=-1)
        cos = np.clip(cos, -1, 1)
        if volume is None:
            v1_ = r23sq - r12sq - r13sq
            v2_ = r24sq - r12sq - r14sq
            v3_ = r34sq - r13sq - r14sq
            det5 = (8 * r12sq * r13sq * r14sq - 2 * v1_ * v2_ * v3_
                    - 2 * r12sq * v3_ * v3_ - 2 * r13sq * v2_ * v2_ - 2 * r14sq * v1_ * v1_)
            volume = np.sqrt(np.maximum(det5, 0) / 288)
        L = np.sqrt(np.stack([r12sq, r13sq, r14sq, r23sq, r24sq, r34sq], axis=-1))
        f = np.stack([v1 * v2, v1 * v3, v2 * v3, v1 * v4, v2 * v4, v3 * v4], axis=-1)
        sin = np.clip(24 * np.asarray(volume)[..., None] * L * f, 0, 1)
        ang = np.arctan2(sin, cos)
        return ang / (2 * np.pi), cos, sin

    @classmethod
    def tetra_voronoi(cls, ra2, rb2, rc2, rd2, rab2, rac2, rad2, rbc2, rbd2, rcd2, cos_ang, sin_ang):
        """
        **LLM Docstring**

        Volumes of the tetrahedron `(a, b, c, d)` restricted to the power cells
        of each of its four balls (the `vol F_ijkl` of paper eq. 7); they sum to
        the tetrahedron volume. Port of AlphaMol `tetra_Voronoi`.

        :return: `(vola, volb, volc, vold)`
        """
        rab, rac, rad = np.sqrt(rab2), np.sqrt(rac2), np.sqrt(rad2)
        rbc, rbd, rcd = np.sqrt(rbc2), np.sqrt(rbd2), np.sqrt(rcd2)
        pd = cls._plane_dist
        v1, v2, v3 = pd(ra2, rb2, rab2) * rab, pd(ra2, rc2, rac2) * rac, pd(ra2, rd2, rad2) * rad
        v4, v5, v6 = pd(rb2, rc2, rbc2) * rbc, pd(rb2, rd2, rbd2) * rbd, pd(rc2, rd2, rcd2) * rcd
        v1b, v2b, v3b = rab - v1, rac - v2, rad - v3
        v4b, v5b, v6b = rbc - v4, rbd - v5, rcd - v6

        def c3(a, b, c, x, y, z):  # dihedral cosines around 12, 13, 23 of (A, B, C, P)
            return cls.tetra_dihedrals(a, b, c, x, y, z)[1][..., [0, 1, 3]]

        abc = c3(rab2, rac2, ra2, rbc2, rb2, rc2)
        abd = c3(rab2, rad2, ra2, rbd2, rb2, rd2)
        acd = c3(rac2, rad2, ra2, rcd2, rc2, rd2)
        bcd = c3(rbc2, rbd2, rb2, rcd2, rc2, rd2)
        cos_abc, cos_acb, cos_bca = abc[..., 0], abc[..., 1], abc[..., 2]
        cos_abd, cos_adb, cos_bda = abd[..., 0], abd[..., 1], abd[..., 2]
        cos_acd, cos_adc, cos_cda = acd[..., 0], acd[..., 1], acd[..., 2]
        cos_bcd, cos_bdc, cos_cdb = bcd[..., 0], bcd[..., 1], bcd[..., 2]

        rho_ab2, rho_ac2, rho_ad2 = ra2 - v1b ** 2, ra2 - v2b ** 2, ra2 - v3b ** 2
        rho_bc2, rho_bd2, rho_cd2 = rb2 - v4b ** 2, rb2 - v5b ** 2, rc2 - v6b ** 2
        with np.errstate(all='ignore'):
            invsin = 1 / sin_ang
        cotan = cos_ang * invsin

        def cap(rho2, c1, c2, k):
            return -rho2 * (c1 * c1 + c2 * c2) * cotan[..., k] + 2 * rho2 * c1 * c2 * invsin[..., k]

        err = np.seterr(all='ignore')
        cap_ab = cap(rho_ab2, cos_abc, cos_abd, 0)
        cap_ac = cap(rho_ac2, cos_acb, cos_acd, 1)
        cap_ad = cap(rho_ad2, cos_adb, cos_adc, 2)
        cap_bc = cap(rho_bc2, cos_bca, cos_bcd, 3)
        cap_bd = cap(rho_bd2, cos_bda, cos_bdc, 4)
        cap_cd = cap(rho_cd2, cos_cda, cos_cdb, 5)

        vola = (v1b * cap_ab + v2b * cap_ac + v3b * cap_ad) / 6
        volb = (v1 * cap_ab + v4b * cap_bc + v5b * cap_bd) / 6
        volc = (v2 * cap_ac + v4 * cap_bc + v6b * cap_cd) / 6
        vold = (v3 * cap_ad + v5 * cap_bd + v6 * cap_cd) / 6
        np.seterr(**err)
        # an exactly flat tetrahedron (only possible with `perturbation=0`) has
        # zero-volume Voronoi pieces; the 0/0 above is resolved to that limit
        flat = ~(sin_ang > 0).all(axis=-1)
        return tuple(np.where(flat, 0, v) for v in (vola, volb, volc, vold))

    @classmethod
    def twosphere(cls, ra, rb, rab2):
        """
        **LLM Docstring**

        Per-ball pieces of a two-ball intersection (port of `twosphere_info`):
        cap areas and cone-truncated cap volumes of each ball on its side of the
        radical plane, the radius `r` of the intersection circle, the angle
        `phi` between the sphere normals along it, and `l = cos(a) + cos(b)`
        (the Gaussian-curvature arc term).

        :return: `(surfa, surfb, vola, volb, r, phi, l)`
        """
        ra2, rb2 = ra * ra, rb * rb
        rab = np.sqrt(rab2)
        lam = cls._plane_dist(ra2, rb2, rab2)
        valb = lam * rab
        vala = rab - valb
        surfa = 2 * np.pi * ra * (ra - vala)
        surfb = 2 * np.pi * rb * (rb - valb)
        Aab = np.pi * (ra2 - vala * vala)
        vola = (ra * surfa - vala * Aab) / 3
        volb = (rb * surfb - valb * Aab) / 3
        r = np.sqrt(np.maximum(ra2 - vala * vala, 0))
        phi = np.arccos(np.clip((ra2 + rb2 - rab2) / (2 * ra * rb), -1, 1))
        l = vala / ra + valb / rb
        return surfa, surfb, vola, volb, r, phi, l

    @classmethod
    def threesphere(cls, ra, rb, rc, rab2, rac2, rbc2, abcp_volume=None):
        """
        **LLM Docstring**

        Per-ball pieces of a three-ball intersection (port of
        `threesphere_dvol`, values only): the spherical-polygon areas and
        corresponding cone volumes of each ball within the triple intersection,
        plus the normalized dihedral angles of the tetrahedron `(A, B, C, P)`
        (`P` a triple point) around AB, AC and BC used for the edge `sigma`
        weights.

        :return: `(surf, vol, seg_angles)`, `surf`/`vol` of shape `(m, 3)`
        """
        ra2, rb2, rc2 = ra * ra, rb * rb, rc * rc
        rab, rac, rbc = np.sqrt(rab2), np.sqrt(rac2), np.sqrt(rbc2)
        pd = cls._plane_dist
        l1, l2, l3 = pd(ra2, rb2, rab2), pd(ra2, rc2, rac2), pd(rb2, rc2, rbc2)
        val1, val2, val3 = l1 * rab, l2 * rac, l3 * rbc
        val1b, val2b, val3b = rab - val1, rac - val2, rbc - val3

        angle, cosine, sine = cls.tetra_dihedrals(rab2, rac2, ra2, rbc2, rb2, rc2, volume=abcp_volume)
        ab, ac, ap, bc, bp, cp = [angle[..., k] for k in range(6)]
        tp = 2 * np.pi
        surfa = tp * ra * (ra * (1 - 2 * ap) - 2 * ab * val1b - 2 * ac * val2b)
        surfb = tp * rb * (rb * (1 - 2 * bp) - 2 * ab * val1 - 2 * bc * val3b)
        surfc = tp * rc * (rc * (1 - 2 * cp) - 2 * ac * val2 - 2 * bc * val3)

        rho_ab2 = ra2 - val1b * val1b
        rho_ac2 = ra2 - val2b * val2b
        rho_bc2 = rb2 - val3b * val3b
        s_abc = rho_ab2 * (tp * ab - sine[..., 0] * cosine[..., 0])
        s_acb = rho_ac2 * (tp * ac - sine[..., 1] * cosine[..., 1])
        s_bca = rho_bc2 * (tp * bc - sine[..., 3] * cosine[..., 3])
        vola = (ra * surfa - val1b * s_abc - val2b * s_acb) / 3
        volb = (rb * surfb - val1 * s_abc - val3b * s_bca) / 3
        volc = (rc * surfc - val2 * s_acb - val3 * s_bca) / 3
        return (
            np.stack([surfa, surfb, surfc], axis=-1),
            np.stack([vola, volb, volc], axis=-1),
            np.stack([ab, ac, bc], axis=-1)
        )

    @staticmethod
    def _atan2(y, x):
        # atan2 that also accepts complex (complex-step) arguments; the branch
        # is chosen from the real parts
        yr, xr = np.real(y), np.real(x)
        with np.errstate(all='ignore'):
            use_x = np.abs(xr) >= np.abs(yr)
            t1 = np.arctan(y / np.where(use_x, x, 1)) + np.where(xr < 0, np.where(yr >= 0, np.pi, -np.pi), 0)
            t2 = np.where(yr >= 0, np.pi / 2, -np.pi / 2) - np.arctan(x / np.where(use_x, 1, y))
        return np.where(use_x, t1, t2)

    @classmethod
    def _gauss_corner_shares(cls, ra, rb, rc, rab, rac, rbc):
        """
        The corner term of three spheres split among them (the `g_ijk` of paper
        eq. 15, AlphaMol `threesphere_dgauss`): the spherical triangle spanned by
        the sphere normals `N_a, N_b, N_c` at a triple point, cut by its
        circumcenter `C` into three isosceles pieces, each shared equally by its
        two base vertices.

        AlphaMol evaluates these pieces from `cos^2` of half arc lengths through
        `sqrt(4abc - (a+b+c-1)^2)`, which loses half the digits (and makes the
        derivative blow up) whenever a piece is nearly flat -- i.e. whenever the
        normal triangle is nearly right-angled, as for any three atoms of a
        regular ring. Here the triple point is built in a local frame from the
        distances and every piece is a signed Van Oosterom-Strackee solid
        angle, which is smooth through those configurations. Written with
        complex-safe operations so `threesphere_gauss_derivatives` can
        differentiate it by complex step.

        :return: shares of shape `(m, 3)`
        """
        err = np.seterr(all='ignore')
        sqrt = np.sqrt
        # local frame: A = 0, B = (rab, 0, 0), C = (xc, yc, 0), P = (xp, yp, zp)
        xc = (rab * rab + rac * rac - rbc * rbc) / (2 * rab)
        yc = sqrt(rac * rac - xc * xc)
        xp = (rab * rab + ra * ra - rb * rb) / (2 * rab)
        yp = (rac * rac + ra * ra - rc * rc - 2 * xp * xc) / (2 * yc)
        zp = sqrt(ra * ra - xp * xp - yp * yp)
        zero = 0 * xp
        P = np.stack([xp, yp, zp], -1)
        Na = P / ra[..., None]
        Nb = (P - np.stack([rab, zero, zero], -1)) / rb[..., None]
        Nc = (P - np.stack([xc, yc, zero], -1)) / rc[..., None]
        dot = lambda x, y: np.sum(x * y, axis=-1)
        cross = lambda x, y: np.stack([
            x[..., 1] * y[..., 2] - x[..., 2] * y[..., 1],
            x[..., 2] * y[..., 0] - x[..., 0] * y[..., 2],
            x[..., 0] * y[..., 1] - x[..., 1] * y[..., 0],
        ], -1)
        Cc = cross(Nb - Na, Nc - Na)
        Cc = Cc / sqrt(dot(Cc, Cc))[..., None]
        Cc = Cc * np.where(np.real(dot(Cc, Na)) < 0, -1, 1)[..., None]

        def omega(X, Y, Z):
            num = dot(X, cross(Y, Z))
            den = 1 + dot(X, Y) + dot(Y, Z) + dot(Z, X)
            return 2 * cls._atan2(num, den)

        o_ab, o_bc, o_ca = omega(Na, Nb, Cc), omega(Nb, Nc, Cc), omega(Nc, Na, Cc)
        orient = np.where(np.real(dot(Na, cross(Nb, Nc))) < 0, -1, 1)
        np.seterr(**err)
        return 0.5 * orient[..., None] * np.stack([o_ab + o_ca, o_ab + o_bc, o_bc + o_ca], -1)

    @classmethod
    def threesphere_gauss(cls, ra, rb, rc, rab2, rac2, rbc2):
        """
        **LLM Docstring**

        Contributions of the corners of a three-ball intersection to the
        integrated Gaussian curvature, split among the three balls (values of
        AlphaMol `threesphere_dgauss`, evaluated with `_gauss_corner_shares`).

        :return: array of shape `(m, 3)`
        """
        return cls._gauss_corner_shares(ra, rb, rc, np.sqrt(rab2), np.sqrt(rac2), np.sqrt(rbc2))

    # ------------------------------------------------------------------
    # derivative kernels (paper eqs. 11, 12, 14, 16; SI parts B-D)
    #
    # Every quantity is a function of inter-center distances only, so all
    # derivatives here are with respect to edge *lengths*; `gradients`
    # converts to Cartesian derivatives via eq. 19.
    # ------------------------------------------------------------------
    # faces of each tetrahedron dihedral: the angle around edge `a` is the
    # angle between faces `_DIH_FACES[a]` (face k = the face opposite vertex k)
    _DIH_FACES = np.array([[2, 3], [1, 3], [1, 2], [0, 3], [0, 2], [0, 1]])
    # the three edges (in 12, 13, 14, 23, 24, 34 order) of the face opposite vertex k
    _FACE_SIDES = np.array([[3, 4, 5], [1, 2, 5], [0, 2, 4], [0, 1, 3]])

    @classmethod
    def tetra_dihedral_derivatives(cls, r12sq, r13sq, r14sq, r23sq, r24sq, r34sq, volume=None):
        """
        **LLM Docstring**

        Dihedral angles of tetrahedra and their derivatives with respect to
        the six edge lengths (port of AlphaMol `tetra_dihed_der`, rearranged so
        that the cosine derivative is formed first and never divided by a
        cosine: `dcos = v_i v_j dnum - cos (dM_i / 2M_i + dM_j / 2M_j)`,
        `dtheta = -dcos / sin`, with the sliver-stable `sin` of
        `tetra_dihedrals`).

        :return: `(angle / 2 pi, cos, sin, dtheta)`, `dtheta[..., a, l] = d theta_a / d r_l`
            in radians per length, edges ordered `12, 13, 14, 23, 24, 34`
        """
        ang, cos, sin = cls.tetra_dihedrals(r12sq, r13sq, r14sq, r23sq, r24sq, r34sq, volume=volume)
        r2 = np.stack([r12sq, r13sq, r14sq, r23sq, r24sq, r34sq], axis=-1)
        r12, r13, r14, r23, r24, r34 = [r2[..., k] for k in range(6)]
        val234 = r34 - r23 - r24
        val134 = r34 - r14 - r13
        val124 = r24 - r12 - r14
        val123 = r23 - r12 - r13
        val213 = r13 - r12 - r23
        val214 = r14 - r12 - r24
        val312 = r12 - r13 - r23
        val314 = r14 - r13 - r34
        val324 = r24 - r23 - r34
        minor = np.stack([
            val234 * val234 - 4 * r23 * r24,
            val134 * val134 - 4 * r13 * r14,
            val124 * val124 - 4 * r12 * r14,
            val123 * val123 - 4 * r12 * r13,
        ], axis=-1)
        # d det_a / d r_l^2 (AlphaMol's `dnum`, rows reordered to alpha12..alpha34)
        dnum = np.stack([
            np.stack([-2 * val134 + val123 + val124, 2 * r12 + val124, 2 * r12 + val123, -val124, -val123, -2 * r12], -1),
            np.stack([2 * r13 + val134, -2 * val124 + val123 + val134, 2 * r13 + val123, -val134, -2 * r13, -val123], -1),
            np.stack([2 * r14 + val134, 2 * r14 + val124, -2 * val123 + val124 + val134, -2 * r14, -val134, -val124], -1),
            np.stack([2 * r23 + val234, -val234, -2 * r23, -2 * val214 + val213 + val234, 2 * r23 + val213, -val213], -1),
            np.stack([2 * r24 + val234, -2 * r24, -val234, 2 * r24 + val214, -2 * val213 + val214 + val234, -val214], -1),
            np.stack([-2 * r34, 2 * r34 + val324, -val324, 2 * r34 + val314, -val314, -2 * val312 + val314 + val324], -1),
        ], axis=-2)
        # (1/2) d minor_k / d r_l^2: for a face with squared sides (s, t, u), minor = s^2+t^2+u^2-2(st+tu+us)
        hdminor = np.zeros(r2.shape[:-1] + (4, 6))
        for k, sides in enumerate(cls._FACE_SIDES):
            for s in sides:
                others = [o for o in sides if o != s]
                hdminor[..., k, s] = r2[..., s] - r2[..., others[0]] - r2[..., others[1]]
        with np.errstate(all='ignore'):
            v = 1 / np.sqrt(np.abs(minor))
            fi, fj = cls._DIH_FACES[:, 0], cls._DIH_FACES[:, 1]
            dcos = (
                    (v[..., fi] * v[..., fj])[..., None] * dnum
                    - cos[..., None] * (hdminor[..., fi, :] / minor[..., fi, None]
                                        + hdminor[..., fj, :] / minor[..., fj, None])
            )
            dcos = dcos * 2 * np.sqrt(r2)[..., None, :]   # d/d(r^2) -> d/dr
            dtheta = -dcos / sin[..., None]
        dtheta = np.where(np.isfinite(dtheta), dtheta, 0)
        return ang, cos, sin, dtheta, dcos

    @classmethod
    def tetra_voronoi_derivatives(cls, R2, r2, cos_ang, sin_ang, dtheta):
        """
        **LLM Docstring**

        Voronoi-split tetrahedron volumes (`tetra_voronoi`) and their
        derivatives with respect to the six edge lengths (port of AlphaMol
        `tetra_Voronoi_der`, written as one loop over the six edges instead of
        six unrolled blocks).

        :param R2: squared radii, shape `(m, 4)`
        :param r2: squared edge lengths, shape `(m, 6)`, order `ab, ac, ad, bc, bd, cd`
        :param cos_ang: tetrahedron dihedral cosines `(m, 6)`
        :param sin_ang: tetrahedron dihedral sines `(m, 6)`
        :param dtheta: tetrahedron dihedral derivatives `(m, 6, 6)`
        :return: `(vol, dvol)` of shapes `(m, 4)` and `(m, 4, 6)`
        """
        m = len(r2)
        L = np.sqrt(r2)
        vol = np.zeros((m, 4))
        dvol = np.zeros((m, 4, 6))
        with np.errstate(all='ignore'):
            invsin = 1 / sin_ang
            cotan = cos_ang * invsin
            for e, (x, y) in enumerate(_TET_EDGES):
                z, w = [k for k in range(4) if k not in (x, y)]
                exz, eyz = _PAIR_INDEX[x, z], _PAIR_INDEX[y, z]
                exw, eyw = _PAIR_INDEX[x, w], _PAIR_INDEX[y, w]
                lam = cls._plane_dist(R2[:, x], R2[:, y], r2[:, e])
                hy = lam * L[:, e]          # distance y -> radical plane
                hx = L[:, e] - hy           # distance x -> radical plane
                rho2 = R2[:, x] - hx * hx
                # dihedral cosines around xy in (x, y, z, P_xyz) and (x, y, w, P_xyw)
                cz, dcz = cls._tripoint_cos(R2[:, x], R2[:, y], R2[:, z], r2[:, e], r2[:, exz], r2[:, eyz])
                cw, dcw = cls._tripoint_cos(R2[:, x], R2[:, y], R2[:, w], r2[:, e], r2[:, exw], r2[:, eyw])
                c1, c2 = cz[:, 0], cw[:, 0]
                val = -(c1 * c1 + c2 * c2) * cotan[:, e] + 2 * c1 * c2 * invsin[:, e]
                cap = rho2 * val
                # d(c1), d(c2) over the six tetrahedron edges
                dc1 = np.zeros((m, 6))
                dc2 = np.zeros((m, 6))
                for col, ei in zip(range(3), (e, exz, eyz)):
                    dc1[:, ei] += dcz[:, 0, col]
                for col, ei in zip(range(3), (e, exw, eyw)):
                    dc2[:, ei] += dcw[:, 0, col]
                dcot = -dtheta[:, e, :] * (1 + cotan[:, e, None] ** 2)
                dinv = -dtheta[:, e, :] * (cotan[:, e] * invsin[:, e])[:, None]
                dval = (
                        -2 * (c1[:, None] * dc1 + c2[:, None] * dc2) * cotan[:, e, None]
                        - (c1 * c1 + c2 * c2)[:, None] * dcot
                        + 2 * (dc1 * c2[:, None] + c1[:, None] * dc2) * invsin[:, e, None]
                        + 2 * (c1 * c2)[:, None] * dinv
                )
                dcap = rho2[:, None] * dval
                dcap[:, e] += -2 * hx * lam * val    # d rho2 / d r_e = -2 hx (d hx / d r_e), d hx / d r_e = lam
                vol[:, x] += hx * cap / 6
                vol[:, y] += hy * cap / 6
                dvol[:, x] += hx[:, None] * dcap / 6
                dvol[:, y] += hy[:, None] * dcap / 6
                dvol[:, x, e] += lam * cap / 6
                dvol[:, y, e] += (1 - lam) * cap / 6
        flat = ~(sin_ang > 0).all(axis=-1)
        vol = np.where(flat[:, None], 0, vol)
        dvol = np.where(flat[:, None, None] | ~np.isfinite(dvol), 0, dvol)
        return vol, dvol

    @classmethod
    def _tripoint_cos(cls, ra2, rb2, rc2, rab2, rac2, rbc2):
        # dihedral cosines around AB, AC, BC of (A, B, C, P), P a triple point,
        # and their derivatives w.r.t. (r_ab, r_ac, r_bc)
        _, cos, _, _, dcos = cls.tetra_dihedral_derivatives(rab2, rac2, ra2, rbc2, rb2, rc2,
                                                            volume=np.ones_like(rab2))
        sel = [0, 1, 3]
        return cos[:, sel], dcos[:, sel][:, :, sel]

    @classmethod
    def twosphere_derivatives(cls, ra, rb, rab2):
        """
        **LLM Docstring**

        Derivatives of the `twosphere` quantities with respect to the center
        distance (port of `twosphere_dinfo`).

        :return: `(dsurfa, dsurfb, dvola, dvolb, dr, dphi, dl)`
        """
        ra2, rb2 = ra * ra, rb * rb
        rab = np.sqrt(rab2)
        lam = cls._plane_dist(ra2, rb2, rab2)
        vala = rab - lam * rab
        Aab = np.pi * (ra2 - vala * vala)
        r = np.sqrt(np.maximum(ra2 - vala * vala, 0))
        cosine = np.clip((ra2 + rb2 - rab2) / (2 * ra * rb), -1, 1)
        with np.errstate(all='ignore'):
            dr = -vala * lam / r
            dphi = rab / (ra * rb * np.sqrt(1 - cosine * cosine))
        return (
            -2 * np.pi * ra * lam,
            2 * np.pi * rb * (lam - 1),
            -Aab * lam,
            Aab * lam - Aab,
            np.where(np.isfinite(dr), dr, 0),
            np.where(np.isfinite(dphi), dphi, 0),
            lam / ra + (1 - lam) / rb
        )

    @classmethod
    def threesphere_derivatives(cls, ra, rb, rc, rab2, rac2, rbc2, abcp_volume=None):
        """
        **LLM Docstring**

        `threesphere` together with the derivatives of its per-ball areas,
        volumes and the three segment angles with respect to `(r_ab, r_ac, r_bc)`
        (port of the derivative branch of `threesphere_dvol`).

        :return: `(surf, vol, seg, dsurf, dvol, dseg)`; `dsurf[:, k, l]` is the
            derivative of ball k's term w.r.t. edge l, `dseg` is in radians
        """
        ra2, rb2, rc2 = ra * ra, rb * rb, rc * rc
        rab, rac, rbc = np.sqrt(rab2), np.sqrt(rac2), np.sqrt(rbc2)
        R = np.stack([ra, rb, rc], -1)
        pd = cls._plane_dist
        l1, l2, l3 = pd(ra2, rb2, rab2), pd(ra2, rc2, rac2), pd(rb2, rc2, rbc2)
        val1, val2, val3 = l1 * rab, l2 * rac, l3 * rbc
        val1b, val2b, val3b = rab - val1, rac - val2, rbc - val3

        angle, cosine, sine, dth, _ = cls.tetra_dihedral_derivatives(
            rab2, rac2, ra2, rbc2, rb2, rc2, volume=abcp_volume
        )
        dth = dth[:, :, [0, 1, 3]]            # w.r.t. (ab, ac, bc)
        f = angle                              # fractions: ab, ac, ap, bc, bp, cp
        df = dth / (2 * np.pi)
        m = len(ra)
        tp = 2 * np.pi
        # (h, fraction index, edge column, d h / d edge) for the two arcs on each ball
        arcs = {
            0: ((val1b, 0, 0, l1), (val2b, 1, 1, l2)),
            1: ((val1, 0, 0, 1 - l1), (val3b, 3, 2, l3)),
            2: ((val2, 1, 1, 1 - l2), (val3, 3, 2, 1 - l3)),
        }
        corner = {0: 2, 1: 4, 2: 5}
        surf = np.zeros((m, 3))
        dsurf = np.zeros((m, 3, 3))
        for k in range(3):
            rk = R[:, k]
            s = rk * (1 - 2 * f[:, corner[k]])
            ds = -2 * rk[:, None] * df[:, corner[k], :]
            for h, fi, col, dh in arcs[k]:
                s = s - 2 * f[:, fi] * h
                ds = ds - 2 * df[:, fi, :] * h[:, None]
                ds[:, col] -= 2 * f[:, fi] * dh
            surf[:, k] = tp * rk * s
            dsurf[:, k] = tp * rk[:, None] * ds

        # cone pieces s_e = rho_e^2 (theta_e - sin cos) for e = ab, ac, bc
        seg_idx = [0, 1, 3]
        rho2 = np.stack([ra2 - val1b ** 2, ra2 - val2b ** 2, rb2 - val3b ** 2], -1)
        drho2 = np.stack([-2 * val1b * l1, -2 * val2b * l2, -2 * val3b * l3], -1)   # w.r.t. own edge
        th = tp * f[:, seg_idx]
        sn, cs = sine[:, seg_idx], cosine[:, seg_idx]
        sc = rho2 * (th - sn * cs)
        dsc = (2 * rho2 * sn * sn)[:, :, None] * dth[:, seg_idx, :]
        for e in range(3):
            dsc[:, e, e] += drho2[:, e] * (th[:, e] - sn[:, e] * cs[:, e])
        # ball k volume = (r_k surf_k - sum_{arcs} h * s_e) / 3
        vol = np.zeros((m, 3))
        dvol = np.zeros((m, 3, 3))
        for k in range(3):
            v = R[:, k] * surf[:, k]
            dv = R[:, k, None] * dsurf[:, k]
            for h, fi, col, dh in arcs[k]:
                e = col
                v = v - h * sc[:, e]
                dv = dv - h[:, None] * dsc[:, e]
                dv[:, col] -= dh * sc[:, e]
            vol[:, k] = v / 3
            dvol[:, k] = dv / 3
        seg = f[:, seg_idx]
        dseg = dth[:, seg_idx, :]
        return surf, vol, seg, dsurf, dvol, dseg

    @classmethod
    def threesphere_gauss_derivatives(cls, ra, rb, rc, rab2, rac2, rbc2, step=1e-30):
        """
        **LLM Docstring**

        `threesphere_gauss` and its derivatives with respect to
        `(r_ab, r_ac, r_bc)`, by complex-step differentiation of
        `_gauss_corner_shares` (exact to machine precision; no subtractive
        cancellation, so it inherits that function's stability near
        right-angled normal triangles, where AlphaMol's closed-form derivative
        is singular).

        :return: `(g, dg)` of shapes `(m, 3)` and `(m, 3, 3)`
        """
        L = np.sqrt(np.stack([rab2, rac2, rbc2], -1)).astype(complex)
        g = np.real(cls._gauss_corner_shares(ra, rb, rc, *np.real(L).T))
        dg = np.zeros(g.shape + (3,))
        for l in range(3):
            Lc = L.copy()
            Lc[:, l] += 1j * step
            dg[:, :, l] = np.imag(cls._gauss_corner_shares(ra.astype(complex), rb.astype(complex),
                                                           rc.astype(complex), *Lc.T)) / step
        dg = np.where(np.isfinite(dg), dg, 0)
        return g, dg

    # ------------------------------------------------------------------
    # measures
    # ------------------------------------------------------------------
    def _compute_measures(self):
        cx = self._get_complex()
        n = cx['n']
        out = {k: np.zeros(n) for k in ('surface_area', 'volume', 'mean_curvature', 'gaussian_curvature')}
        if cx['empty']:
            return out
        P, R = cx['P'], cx['R']
        nl = len(R)
        R2 = R * R
        E, edgeK = cx['edges'], cx['edge_mask']
        F, faceK, face_edges = cx['triangles'], cx['triangle_mask'], cx['triangle_edges']
        T, tet_edges, tet_faces = cx['tetrahedra'], cx['tet_edges'], cx['tet_faces']

        surf = np.zeros(nl)
        vol = np.zeros(nl)
        mean = np.zeros(nl)
        gauss = np.zeros(nl)
        v_gamma = np.ones(nl)
        e_gamma = np.ones(len(E))
        e_sigma = np.ones(len(E))

        def d2(i, j):
            return np.sum((P[i] - P[j]) ** 2, axis=-1)

        # --- tetrahedra: Voronoi-split tetrahedron volume + angle weights ---
        if len(T):
            a, b, c, d = T.T
            rab2, rac2, rad2 = d2(a, b), d2(a, c), d2(a, d)
            rbc2, rbd2, rcd2 = d2(b, c), d2(b, d), d2(c, d)
            tvol = np.abs(np.einsum('ij,ij->i', np.cross(P[b] - P[a], P[c] - P[a]), P[d] - P[a])) / 6
            ang, cos, sin = self.tetra_dihedrals(rab2, rac2, rad2, rbc2, rbd2, rcd2, volume=tvol)
            vols = self.tetra_voronoi(R2[a], R2[b], R2[c], R2[d],
                                      rab2, rac2, rad2, rbc2, rbd2, rcd2, cos, sin)
            for idx, v in zip((a, b, c, d), vols):
                np.add.at(vol, idx, v)
            for idx, ks in zip((a, b, c, d), ([0, 1, 2], [0, 3, 4], [1, 3, 5], [2, 4, 5])):
                np.add.at(v_gamma, idx, -(np.sum(ang[:, ks], axis=1) / 2 - 0.25))
            np.add.at(e_gamma, tet_edges.reshape(-1), -ang.reshape(-1))
            np.add.at(e_sigma, tet_edges.reshape(-1), -ang.reshape(-1))

        # --- triangles: coefficient 1 - (#cofaces in K) / 2 ---
        f_cof = np.zeros(len(F))
        if len(T):
            np.add.at(f_cof, tet_faces.reshape(-1), 1)
        f_coef = np.where(faceK, 1 - 0.5 * f_cof, 0)
        fk = np.flatnonzero(f_coef != 0)
        if len(fk):
            a, b, c = F[fk].T
            coef = f_coef[fk]
            rab2, rac2, rbc2 = d2(a, b), d2(a, c), d2(b, c)
            _, rho2_f = self._orthospheres(P, R2, F[fk])
            area_f = 0.5 * np.linalg.norm(np.cross(P[b] - P[a], P[c] - P[a]), axis=1)
            abcp = area_f * np.sqrt(np.maximum(-rho2_f, 0)) / 3
            fs, fv, seg = self.threesphere(R[a], R[b], R[c], rab2, rac2, rbc2, abcp_volume=abcp)
            fg = self.threesphere_gauss(R[a], R[b], R[c], rab2, rac2, rbc2)
            for k, idx in enumerate((a, b, c)):
                np.add.at(surf, idx, coef * fs[:, k])
                np.add.at(vol, idx, coef * fv[:, k])
                np.add.at(gauss, idx, 2 * coef * fg[:, k])
                np.add.at(e_sigma, face_edges[fk, k], -2 * coef * seg[:, k])

        # --- edges ---
        # every edge of the complex (AlphaMol skips |gamma| < 1e-10, which also
        # drops the sigma terms of nearly-buried edges next to slivers)
        ek = np.flatnonzero(edgeK)
        if len(ek):
            a, b = E[ek].T
            g, s = e_gamma[ek], e_sigma[ek]
            sa, sb, va, vb, r, phi, l = self.twosphere(R[a], R[b], d2(a, b))
            np.add.at(surf, a, -g * sa)
            np.add.at(surf, b, -g * sb)
            np.add.at(vol, a, -g * va)
            np.add.at(vol, b, -g * vb)
            for idx in (a, b):
                # paper eq. 13: -(pi/2) sigma_ij phi_ij r_ij to each ball
                np.add.at(mean, idx, -0.5 * np.pi * s * r * phi)
                np.add.at(gauss, idx, -np.pi * s * l)

        # --- vertices ---
        vk = cx['vertex_mask']
        g = np.where(vk, v_gamma, 0)
        surf += g * 4 * np.pi * R2
        vol += g * 4 / 3 * np.pi * R2 * R
        mean += np.where(vk, surf / R, 0)
        gauss += np.where(vk, surf / R2, 0)

        # NB: AlphaMol's C++ code subtracts pi*sigma*r*phi from *each* ball, i.e.
        # twice eq. 13; the factor of 1/2 above matches eq. 13 and the additivity
        # of M (M(ball) = 4 pi r, convex edges +L phi / 2, concave -L phi / 2)

        s = cx['scale']
        live = cx['live']
        out['surface_area'][live] = surf * s ** 2
        out['volume'][live] = vol * s ** 3
        out['mean_curvature'][live] = mean * s
        out['gaussian_curvature'][live] = gauss
        return out

    @property
    def ball_measures(self):
        """
        **LLM Docstring**

        Per-ball contributions to each measure (unweighted), keyed by
        `'surface_area'`, `'volume'`, `'mean_curvature'`,
        `'gaussian_curvature'`; each array has one entry per *input* ball
        (pruned balls contribute 0).
        """
        if self._measures is None:
            self._measures = self._compute_measures()
        return self._measures

    @property
    def ball_surface_areas(self):
        return self.ball_measures['surface_area']
    @property
    def ball_volumes(self):
        return self.ball_measures['volume']
    @property
    def ball_mean_curvatures(self):
        return self.ball_measures['mean_curvature']
    @property
    def ball_gaussian_curvatures(self):
        return self.ball_measures['gaussian_curvature']

    @property
    def surface_area(self):
        return float(np.sum(self.ball_surface_areas))
    @property
    def volume(self):
        return float(np.sum(self.ball_volumes))
    @property
    def mean_curvature(self):
        return float(np.sum(self.ball_mean_curvatures))
    @property
    def gaussian_curvature(self):
        return float(np.sum(self.ball_gaussian_curvatures))

    def measures(self):
        """
        **LLM Docstring**

        :return: the four total intrinsic measures
        :rtype: dict
        """
        return {k: float(np.sum(v)) for k, v in self.ball_measures.items()}

    def weighted_measures(self, volume=None, surface_area=None, mean_curvature=None, gaussian_curvature=None,
                          return_components=False):
        """
        **LLM Docstring**

        The weighted combination `sum_i a_i V_i + b_i A_i + c_i M_i + d_i G_i`
        (paper eq. 17; with scalar weights `-p, sigma, k1, k2` this is the
        morphometric nonpolar solvation energy of eq. 2).

        :param volume: scalar or per-ball weights `a_i`
        :param surface_area: scalar or per-ball weights `b_i`
        :param mean_curvature: scalar or per-ball weights `c_i`
        :param gaussian_curvature: scalar or per-ball weights `d_i`
        :param return_components: return the per-ball totals instead of the sum
        :return: the weighted total (or per-ball array)
        """
        bm = self.ball_measures
        total = np.zeros(len(self.radii))
        for key, w in (('volume', volume), ('surface_area', surface_area),
                       ('mean_curvature', mean_curvature), ('gaussian_curvature', gaussian_curvature)):
            if w is not None:
                total = total + np.asarray(w, dtype=float) * bm[key]
        return total if return_components else float(np.sum(total))

    # ------------------------------------------------------------------
    # gradients
    # ------------------------------------------------------------------
    def _derivative_data(self):
        """
        Evaluate every derivative kernel once on the dual complex; the
        (linear-in-weights) assembly in `_edge_derivatives` reuses it.
        """
        if self._derivative_cache is not None:
            return self._derivative_cache
        cx = self._get_complex()
        if cx['empty']:
            self._derivative_cache = {'empty': True}
            return self._derivative_cache
        P, R = cx['P'], cx['R']
        R2 = R * R
        E, edgeK = cx['edges'], cx['edge_mask']
        F, faceK, face_edges = cx['triangles'], cx['triangle_mask'], cx['triangle_edges']
        T, tet_edges, tet_faces = cx['tetrahedra'], cx['tet_edges'], cx['tet_faces']
        d2 = lambda i, j: np.sum((P[i] - P[j]) ** 2, axis=-1)
        data = {'empty': False}

        # --- edge (two-ball) quantities on every edge of the dual complex ---
        nE = len(E)
        ek = np.flatnonzero(edgeK)
        a, b = E[ek].T
        tw = self.twosphere(R[a], R[b], d2(a, b))
        dtw = self.twosphere_derivatives(R[a], R[b], d2(a, b))
        edge_q = {}
        for name, val in zip(('sa', 'sb', 'va', 'vb', 'r', 'phi', 'l'), tw):
            arr = np.zeros(nE); arr[ek] = val; edge_q[name] = arr
        for name, val in zip(('dsa', 'dsb', 'dva', 'dvb', 'dr', 'dphi', 'dl'), dtw):
            arr = np.zeros(nE); arr[ek] = val; edge_q[name] = arr
        data['edge'] = edge_q

        # --- edge weights (recomputed exactly as in `_compute_measures`) ---
        e_gamma = np.ones(nE)
        e_sigma = np.ones(nE)

        if len(T):
            ta, tb, tc, td = T.T
            r2 = np.stack([d2(ta, tb), d2(ta, tc), d2(ta, td), d2(tb, tc), d2(tb, td), d2(tc, td)], -1)
            tvol = np.abs(np.einsum('ij,ij->i', np.cross(P[tb] - P[ta], P[tc] - P[ta]), P[td] - P[ta])) / 6
            ang, cos, sin, dth, _ = self.tetra_dihedral_derivatives(*r2.T, volume=tvol)
            np.add.at(e_gamma, tet_edges.reshape(-1), -ang.reshape(-1))
            np.add.at(e_sigma, tet_edges.reshape(-1), -ang.reshape(-1))
            data['tet'] = {'dtheta': dth, 'r2': r2, 'cos': cos, 'sin': sin, 'dF': None}

        f_cof = np.zeros(len(F))
        if len(T):
            np.add.at(f_cof, tet_faces.reshape(-1), 1)
        f_coef = np.where(faceK, 1 - 0.5 * f_cof, 0)
        fk = np.flatnonzero(f_coef != 0)
        if len(fk):
            fa, fb, fc = F[fk].T
            rab2, rac2, rbc2 = d2(fa, fb), d2(fa, fc), d2(fb, fc)
            _, rho2_f = self._orthospheres(P, R2, F[fk])
            area_f = 0.5 * np.linalg.norm(np.cross(P[fb] - P[fa], P[fc] - P[fa]), axis=1)
            abcp = area_f * np.sqrt(np.maximum(-rho2_f, 0)) / 3
            _, _, seg, dsurf, dvol, dseg = self.threesphere_derivatives(
                R[fa], R[fb], R[fc], rab2, rac2, rbc2, abcp_volume=abcp)
            _, dg = self.threesphere_gauss_derivatives(R[fa], R[fb], R[fc], rab2, rac2, rbc2)
            coef = f_coef[fk]
            for k in range(3):
                np.add.at(e_sigma, face_edges[fk, k], -2 * coef * seg[:, k])
            data['face'] = {'idx': fk, 'coef': coef, 'dsurf': dsurf, 'dvol': dvol, 'dseg': dseg, 'dg': dg}

        data['e_gamma'] = np.where(edgeK, e_gamma, 0)
        data['edge_mask'] = edgeK
        data['e_sigma'] = e_sigma
        self._derivative_cache = data
        return data

    def _edge_derivatives(self, ws, wv, wm, wg):
        """
        d W / d r_e for every edge of the triangulation, where (in normalized
        units, per live ball)

            W = sum_i ws_i A_i + wv_i V_i  +  [mean-curvature arc terms, weights wm]
                + [Gaussian arc + corner terms, weights wg]

        The sphere-patch parts of M and G are surface areas weighted by 1/r and
        1/r^2, so callers fold those into `ws`.
        """
        cx = self._get_complex()
        data = self._derivative_data()
        E, R = cx['edges'], cx['R']
        R2 = R * R
        dE = np.zeros(len(E))
        q = data['edge']
        ea, eb = E[:, 0], E[:, 1]
        ea_ = np.minimum(ea, len(R) - 1)   # dummy endpoints only occur on edges outside K,
        eb_ = np.minimum(eb, len(R) - 1)   # where every edge quantity is zero anyway
        wsum_m = wm[ea_] + wm[eb_]
        wsum_g = wg[ea_] + wg[eb_]
        # two-ball quantity entering each edge's gamma-weighted term
        Q = ws[ea_] * q['sa'] + ws[eb_] * q['sb'] + wv[ea_] * q['va'] + wv[eb_] * q['vb']
        # mean / Gauss arc factors multiplying d sigma
        Km = 0.5 * np.pi * wsum_m * q['r'] * q['phi']
        Kg = np.pi * wsum_g * q['l']

        if 'tet' in data:
            T, te = cx['tetrahedra'], cx['tet_edges']
            td = data['tet']
            dth = td['dtheta']
            if td['dF'] is None and np.any(wv != 0):
                # Voronoi pieces are only needed for the intrinsic volume path
                _, td['dF'] = self.tetra_voronoi_derivatives(R2[T], td['r2'], td['cos'], td['sin'], dth)
            dF = td['dF']
            # vertex weights: d gamma_x = -(1/4 pi) sum_{edges at x} d theta
            for x, ks in enumerate(([0, 1, 2], [0, 3, 4], [1, 3, 5], [2, 4, 5])):
                i = T[:, x]
                big = ws[i] * 4 * np.pi * R2[i] + wv[i] * 4 / 3 * np.pi * R2[i] * R[i]
                dgam = -np.sum(dth[:, ks, :], axis=1) / (4 * np.pi)
                np.add.at(dE, te.reshape(-1), (big[:, None] * dgam).reshape(-1))
                # Voronoi pieces of the tetrahedron
                if dF is not None:
                    np.add.at(dE, te.reshape(-1), (wv[i][:, None] * dF[:, x, :]).reshape(-1))
            # edge gamma / sigma: d gamma_e = d sigma_e = -d theta_e / 2 pi
            coefs = Q[te] + Km[te] + Kg[te]                         # (mt, 6) per dihedral
            contrib = np.einsum('ma,mal->ml', coefs, dth) / (2 * np.pi)
            np.add.at(dE, te.reshape(-1), contrib.reshape(-1))

        if 'face' in data:
            fd = data['face']
            fk, coef = fd['idx'], fd['coef']
            fe = cx['triangle_edges'][fk]
            idx = cx['triangles'][fk]
            w_s, w_v, w_g = ws[idx], wv[idx], wg[idx]
            direct = (np.einsum('mk,mkl->ml', w_s, fd['dsurf'])
                      + np.einsum('mk,mkl->ml', w_v, fd['dvol'])
                      + 2 * np.einsum('mk,mkl->ml', w_g, fd['dg']))
            # d sigma_e = -2 c d seg_e / 2 pi  (dseg in radians)
            arc = np.einsum('me,mel->ml', Km[fe] + Kg[fe], fd['dseg']) / np.pi
            np.add.at(dE, fe.reshape(-1), (coef[:, None] * (direct + arc)).reshape(-1))

        g, s = data['e_gamma'], data['e_sigma']
        dE += -g * (ws[ea_] * q['dsa'] + ws[eb_] * q['dsb'] + wv[ea_] * q['dva'] + wv[eb_] * q['dvb'])
        on = data['edge_mask']
        dE += -0.5 * np.pi * wsum_m * s * (q['r'] * q['dphi'] + q['phi'] * q['dr']) * on
        dE += -np.pi * wsum_g * s * q['dl'] * on
        return dE

    # ------------------------------------------------------------------
    # Cartesian volume / area gradients (the paper's refs. 60, 61)
    #
    # For a ball i and a neighbour j sharing Voronoi face F_ij, with D_ij the
    # disk cut from the balls by the radical plane and C_ij its boundary circle,
    #
    #   dV_i/dz_j = -(1/l_ij)             int_{F_ij ∩ D_ij} (x - z_j) dA
    #   dA_i/dz_j = -(r_i/(l_ij rho_ij))  int_{F_ij ∩ C_ij} (x - z_j) ds
    #
    # and dX_i/dz_i follows from translation invariance. The face region and
    # its exposed arcs are built in the radical plane from the half-planes
    # {pi_a <= pi_k} of the link of each edge (arcs) and the Voronoi edges
    # dual to its triangles (chords). Unlike the intrinsic formula for the
    # volume, nothing here divides by a tetrahedron's sine, so sliver
    # tetrahedra (co-planar / co-circular rings, symmetric structures) stay
    # well conditioned.
    # ------------------------------------------------------------------
    def _face_geometry(self):
        if self._face_cache is not None:
            return self._face_cache
        cx = self._get_complex()
        P, R2, dummy = cx['all_points'], cx['all_R2'], cx['is_dummy']
        E = cx['edges']
        ek = np.flatnonzero(cx['edge_mask'] & (cx['edge_rho2'] < 0))
        ne = len(ek)
        a, b = E[ek].T
        L = np.linalg.norm(P[b] - P[a], axis=1)
        u = (P[b] - P[a]) / L[:, None]
        ax = np.eye(3)[np.argmin(np.abs(u), axis=1)]
        p = np.cross(u, ax)
        p /= np.linalg.norm(p, axis=1)[:, None]
        q = np.cross(u, p)
        yc = cx['edge_centers'][ek]
        rho = np.sqrt(-cx['edge_rho2'][ek])

        # --- constraints from the link of each edge ---
        row = -np.ones(len(E), dtype=int)
        row[ek] = np.arange(ne)
        le, lk, lf = cx['link_edge'], cx['link_opp'], cx['link_face']
        sel = (row[le] >= 0) & ~dummy[lk]
        er, k, f = row[le[sel]], lk[sel], lf[sel]
        v = 2 * (P[k] - P[a[er]])
        nx = np.einsum('ij,ij->i', v, p[er])
        ny = np.einsum('ij,ij->i', v, q[er])
        pw = lambda x, i: np.sum((x - P[i]) ** 2, axis=1) - R2[i]
        dpow = pw(yc[er], k) - pw(yc[er], a[er])      # constraint: n . x <= dpow (x from disk center)
        nn = np.hypot(nx, ny)
        tiny = nn <= 1e-14 * (1 + np.abs(dpow))
        with np.errstate(all='ignore'):
            delta = np.where(tiny, np.where(dpow >= 0, np.inf, -np.inf), dpow / nn)
            nhx, nhy = np.where(tiny, 1.0, nx / nn), np.where(tiny, 0.0, ny / nn)
        rr = rho[er]

        # --- exposed arcs: complement of the union of removed angular intervals ---
        tp = 2 * np.pi
        alpha = np.arccos(np.clip(delta / rr, -1, 1))          # 0: no cut, pi: all removed
        beta = np.arctan2(nhy, nhx)
        lo = np.mod(beta - alpha, tp)
        hi = lo + 2 * alpha
        full = alpha >= np.pi
        lo, hi = np.where(full, 0, lo), np.where(full, tp, hi)
        cut = alpha > 0
        wrap = cut & (hi > tp)
        s_lo = np.concatenate([lo[cut], np.zeros(wrap.sum())])
        s_hi = np.concatenate([np.minimum(hi[cut], tp), hi[wrap] - tp])
        s_er = np.concatenate([er[cut], er[wrap]])
        counts = np.bincount(s_er, minlength=ne)
        width = int(counts.max(initial=0)) + 1                  # >= 1 padding column per row
        S = np.full((ne, width), tp)
        H = np.full((ne, width), tp)
        o = np.argsort(s_er, kind='stable')
        starts = np.r_[0, np.cumsum(counts)[:-1]]
        pos = np.arange(len(o)) - starts[s_er[o]]
        S[s_er[o], pos] = s_lo[o]
        H[s_er[o], pos] = s_hi[o]
        srt = np.argsort(S, axis=1)
        S = np.take_along_axis(S, srt, 1)
        H = np.take_along_axis(H, srt, 1)
        run = np.maximum.accumulate(H, axis=1)
        prev = np.concatenate([np.zeros((ne, 1)), run[:, :-1]], axis=1)
        g0, g1 = prev, np.maximum(S, prev)                      # gaps [g0, g1]
        dphi = g1 - g0
        ds = np.sin(g1) - np.sin(g0)
        dc = np.cos(g0) - np.cos(g1)
        arc_len = rho * dphi.sum(1)
        arc_mom = rho[:, None] ** 2 * np.stack([ds.sum(1), dc.sum(1)], -1)
        area = 0.5 * rho ** 2 * dphi.sum(1)
        mom = (rho ** 3 / 3)[:, None] * np.stack([ds.sum(1), dc.sum(1)], -1)

        # --- chords: Voronoi edges dual to the triangles around each edge ---
        ft = cx['face_tets'][f]
        ok = np.all(ft >= 0, axis=1)
        yv = cx['voronoi_vertices']
        d3 = -nhy[:, None] * p[er] + nhx[:, None] * q[er]
        t1 = np.einsum('ij,ij->i', yv[np.maximum(ft[:, 0], 0)] - yc[er], d3)
        t2 = np.einsum('ij,ij->i', yv[np.maximum(ft[:, 1], 0)] - yc[er], d3)
        with np.errstate(invalid='ignore'):
            Hh = np.sqrt(np.maximum(rr ** 2 - delta ** 2, 0))
        clo = np.maximum(np.minimum(t1, t2), -Hh)
        chi = np.minimum(np.maximum(t1, t2), Hh)
        good = ok & np.isfinite(delta) & (chi > clo)
        dl = np.where(good, delta, 0)
        piece = np.where(good, 0.5 * dl * (chi - clo), 0)
        cm = (2 * dl[:, None] * np.stack([nhx, nhy], -1)
              + np.where(good, clo + chi, 0)[:, None] * np.stack([-nhy, nhx], -1)) / 3
        np.add.at(area, er, piece)
        np.add.at(mom, er, piece[:, None] * cm)

        to3 = lambda m2: m2[:, :1] * p + m2[:, 1:] * q
        self._face_cache = {
            'edges': ek, 'a': a, 'b': b, 'length': L, 'rho': rho, 'center': yc,
            'area': area, 'moment': to3(mom),                 # int (x - center) dA
            'arc_length': arc_len, 'arc_moment': to3(arc_mom)  # int (x - center) ds
        }
        return self._face_cache

    def _cartesian_gradient(self, wv, ws):
        """
        Gradient (normalized units, live balls) of `sum_i wv_i V_i + ws_i A_i`
        from the Voronoi-face formulas above.
        """
        cx = self._get_complex()
        fg = self._face_geometry()
        nl = len(cx['R'])
        P = cx['all_points']
        R = cx['R']
        a, b, L, rho, yc = fg['a'], fg['b'], fg['length'], fg['rho'], fg['center']
        g = np.zeros((nl, 3))

        def add(w_own, own, other, M0, M1):
            # d X_own / d z_other = -w (M1 + M0 (center - z_other)) ; opposite on z_own
            t = -w_own[:, None] * (M1 + M0[:, None] * (yc - P[other]))
            np.add.at(g, other, t)
            np.add.at(g, own, -t)

        Av, Mv = fg['area'] / L, fg['moment'] / L[:, None]
        add(wv[a], a, b, Av, Mv)
        add(wv[b], b, a, Av, Mv)
        ca = R[a] / (L * rho)
        cb = R[b] / (L * rho)
        add(ws[a] * ca, a, b, fg['arc_length'], fg['arc_moment'])
        add(ws[b] * cb, b, a, fg['arc_length'], fg['arc_moment'])
        return g

    def _edge_to_cartesian(self, dE):
        cx = self._get_complex()
        P = cx['P']
        E = cx['edges']
        nl = len(cx['R'])
        keep = (dE != 0) & (E[:, 1] < nl)
        a, b = E[keep].T
        u = P[a] - P[b]
        u = u / np.linalg.norm(u, axis=1)[:, None]
        g = np.zeros((nl, 3))
        np.add.at(g, a, dE[keep, None] * u)
        np.add.at(g, b, -dE[keep, None] * u)
        return g

    def _live_weights(self, w):
        cx = self._get_complex()
        nl = len(cx['R'])
        if w is None:
            return np.zeros(nl)
        w = np.broadcast_to(np.asarray(w, dtype=float), (cx['n'],))
        return np.asarray(w)[cx['live']]

    def gradients(self, weights=None, method='cartesian'):
        """
        **LLM Docstring**

        Cartesian gradients of the four total measures with respect to the ball
        centers (paper eqs. 11, 12, 14, 16 combined with eq. 19), at fixed radii.

        :param weights: optional per-ball weights applied to every measure, i.e.
            the gradient of `sum_i w_i X_i` for each measure `X`
        :param method: `'cartesian'` or `'intrinsic'`, see `weighted_gradient`
        :return: dict of `(n, 3)` arrays keyed like `measures()`
        :rtype: dict
        """
        w = np.ones(len(self.radii)) if weights is None else weights
        return {
            k: self.weighted_gradient(method=method, **{k: w})
            for k in ('surface_area', 'volume', 'mean_curvature', 'gaussian_curvature')
        }

    def weighted_gradient(self, volume=None, surface_area=None, mean_curvature=None, gaussian_curvature=None,
                          method='cartesian'):
        """
        **LLM Docstring**

        Gradient of `weighted_measures` (eq. 17) with respect to the ball
        centers -- eq. 19, e.g. the nonpolar solvation force
        `-weighted_gradient(volume=-p, surface_area=sigma, mean_curvature=k1, gaussian_curvature=k2)`.

        :param method: how the volume and area parts are differentiated:
            `'cartesian'` (default) uses the Voronoi-face formulas of refs. 60/61
            (`dV_i/dz_j` from face areas and centroids, `dA_i/dz_j` from exposed
            arcs), which stay accurate for near-degenerate (co-planar / co-circular)
            structures; `'intrinsic'` uses the paper's distance-derivative
            formulas (eqs. 11, 12 + 19) throughout, which lose accuracy as
            ~eps / sin^3 on sliver tetrahedra. The curvature parts always use
            eqs. 14 and 16.
        :return: `(n, 3)` gradient (zero rows for pruned balls)
        :rtype: np.ndarray
        """
        cx = self._get_complex()
        out = np.zeros((cx['n'], 3))
        if cx['empty']:
            return out
        R = cx['R']
        s = cx['scale']
        z = np.zeros(len(R))
        wv = self._live_weights(volume)
        ws = self._live_weights(surface_area)
        wm = self._live_weights(mean_curvature)
        wg = self._live_weights(gaussian_curvature)
        # each measure in its own units: d(A)/dz ~ s, dV ~ s^2, dM ~ 1, dG ~ 1/s
        g = np.zeros((len(R), 3))
        # the sphere-patch parts of M and G are areas weighted by 1/r and 1/r^2
        ws_all = s * ws + wm / R + wg / (s * R ** 2)
        if method == 'cartesian':
            g += s ** 2 * self._cartesian_gradient(wv, z) + self._cartesian_gradient(z, ws_all)
            dE = np.zeros(len(cx['edges']))
        elif method == 'intrinsic':
            dE = (self._edge_derivatives(ws_all, z, z, z)
                  + s ** 2 * self._edge_derivatives(z, wv, z, z))
        else:
            raise ValueError(f"unknown gradient method '{method}'")
        # arc (and, for G, corner) terms: eqs. 14 and 16
        if mean_curvature is not None:
            dE = dE + self._edge_derivatives(z, z, wm, z)
        if gaussian_curvature is not None:
            dE = dE + self._edge_derivatives(z, z, z, wg) / s
        g += self._edge_to_cartesian(dE)
        out[cx['live']] = g
        return out

    @property
    def surface_area_gradient(self):
        return self.weighted_gradient(surface_area=1)
    @property
    def volume_gradient(self):
        return self.weighted_gradient(volume=1)
    @property
    def mean_curvature_gradient(self):
        return self.weighted_gradient(mean_curvature=1)
    @property
    def gaussian_curvature_gradient(self):
        return self.weighted_gradient(gaussian_curvature=1)
