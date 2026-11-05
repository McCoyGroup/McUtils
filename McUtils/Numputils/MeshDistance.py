"""Triangle distance and solid-interior queries on a cached AABB hierarchy."""
import numpy as np
import scipy.spatial

from ..Misc import njit
from .MeshOps import mesh_arrays, mesh_topology, mesh_normals, check_mesh_deformation

__all__ = ['MeshDistanceQuery', 'mesh_signed_distance', 'weld_mesh_vertices']


def weld_mesh_vertices(vertices, faces, tolerance=1.e-10):
    """Merge coincident mesh vertices without changing surface locations.

    The first vertex of each connected tolerance cluster is retained. No holes
    are capped, triangles deleted, or orientations changed.
    """
    vertices, faces = mesh_arrays(vertices, faces)
    if not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError('weld tolerance must be finite and nonnegative')
    if tolerance == 0:
        unique, inverse = np.unique(vertices, axis=0, return_inverse=True)
        return unique, inverse[faces]
    parent = np.arange(len(vertices))
    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index
    for a, b in scipy.spatial.cKDTree(vertices).query_pairs(tolerance, output_type='ndarray'):
        a, b = find(a), find(b)
        parent[max(a, b)] = min(a, b)
    roots = np.array([find(i) for i in range(len(vertices))])
    keep, inverse = np.unique(roots, return_inverse=True)
    return vertices[keep], inverse[faces]


@njit(cache=True)
def _closest_triangle(p, a, b, c):
    # Voronoi-region tests include face interiors, edges, and vertices.
    ab = b - a; ac = c - a; ap = p - a
    d1 = np.dot(ab, ap); d2 = np.dot(ac, ap)
    if d1 <= 0 and d2 <= 0: return a
    bp = p - b; d3 = np.dot(ab, bp); d4 = np.dot(ac, bp)
    if d3 >= 0 and d4 <= d3: return b
    vc = d1*d4 - d3*d2
    if vc <= 0 and d1 >= 0 and d3 <= 0: return a + (d1/(d1-d3))*ab
    cp = p - c; d5 = np.dot(ab, cp); d6 = np.dot(ac, cp)
    if d6 >= 0 and d5 <= d6: return c
    vb = d5*d2 - d1*d6
    if vb <= 0 and d2 >= 0 and d6 <= 0: return a + (d2/(d2-d6))*ac
    va = d3*d6 - d5*d4
    if va <= 0 and d4-d3 >= 0 and d5-d6 >= 0: return b + ((d4-d3)/((d4-d3)+(d5-d6)))*(c-b)
    denominator = va + vb + vc
    return a + (vb/denominator)*ab + (vc/denominator)*ac


@njit(cache=True)
def _box_distance_squared(point, low, high):
    value = 0.
    for j in range(3):
        d = max(low[j] - point[j], 0., point[j] - high[j])
        value += d*d
    return value


@njit(cache=True)
def _distance_queries(points, triangles, low, high, nodes, order):
    distances = np.empty(len(points)); closest = np.empty_like(points)
    triangle_ids = np.empty(len(points), dtype=np.int64)
    stack = np.empty(len(nodes), dtype=np.int64)
    for i in range(len(points)):
        point = points[i]; best = np.inf; best_id = -1
        top = 1; stack[0] = 0
        while top:
            top -= 1; node = stack[top]
            if _box_distance_squared(point, low[node], high[node]) > best: continue
            left, right, start, count = nodes[node]
            if count:
                for k in range(start, start + count):
                    index = order[k]; triangle = triangles[index]
                    q = _closest_triangle(point, triangle[0], triangle[1], triangle[2])
                    difference = q - point; d = np.dot(difference, difference)
                    if d < best:
                        best = d; closest[i] = q; best_id = index
            else:
                dl = _box_distance_squared(point, low[left], high[left])
                dr = _box_distance_squared(point, low[right], high[right])
                if dl < dr:
                    if dr <= best: stack[top] = right; top += 1
                    if dl <= best: stack[top] = left; top += 1
                else:
                    if dl <= best: stack[top] = left; top += 1
                    if dr <= best: stack[top] = right; top += 1
        distances[i] = np.sqrt(best); triangle_ids[i] = best_id
    return distances, closest, triangle_ids


@njit(cache=True)
def _ray_box(point, direction, low, high, tolerance):
    near = 0.; far = np.inf
    for j in range(3):
        t0 = (low[j] - point[j] - tolerance) / direction[j]
        t1 = (high[j] - point[j] + tolerance) / direction[j]
        near = max(near, min(t0, t1)); far = min(far, max(t0, t1))
        if far < near: return False
    return True


@njit(cache=True)
def _winding_at_point(point, triangles):
    angle = 0.
    for triangle in triangles:
        a = triangle[0] - point; b = triangle[1] - point; c = triangle[2] - point
        la = np.sqrt(np.dot(a, a)); lb = np.sqrt(np.dot(b, b)); lc = np.sqrt(np.dot(c, c))
        numerator = np.dot(a, np.cross(b, c))
        denominator = la*lb*lc + np.dot(a,b)*lc + np.dot(b,c)*la + np.dot(c,a)*lb
        angle += 2*np.arctan2(numerator, denominator)
    return angle / (4*np.pi)


@njit(cache=True)
def _inside_queries(points, triangles, low, high, nodes, order, tolerance):
    inside = np.empty(len(points), dtype=np.bool_)
    # Non-axis-aligned deterministic directions; edge/vertex hits are excluded
    # from voting rather than counted twice. Three valid rays form a majority.
    directions = np.array([[1., .3713906764, .5291772109], [.193178, 1., .438731],
                           [.312931, .271828, 1.], [1., -.617831, .239791],
                           [-.381973, 1., -.718281], [.419173, -.318731, 1.],
                           [-1., -.289173, .619381]])
    stack = np.empty(len(nodes), dtype=np.int64)
    fallbacks = 0
    for i in range(len(points)):
        point = points[i]; votes = 0; valid = 0
        if np.any(point < low[0]-tolerance) or np.any(point > high[0]+tolerance):
            inside[i] = False; continue
        for raw_direction in directions:
            direction = raw_direction / np.sqrt(np.sum(raw_direction*raw_direction))
            top = 1; stack[0] = 0; hits = 0; ambiguous = False
            while top and not ambiguous:
                top -= 1; node = stack[top]
                if not _ray_box(point, direction, low[node], high[node], tolerance): continue
                left, right, start, count = nodes[node]
                if count:
                    for k in range(start, start+count):
                        triangle = triangles[order[k]]
                        e1 = triangle[1]-triangle[0]; e2 = triangle[2]-triangle[0]
                        h = np.cross(direction, e2); determinant = np.dot(e1, h)
                        scale = np.sqrt(np.dot(e1,e1)*np.dot(e2,e2))
                        if abs(determinant) <= 1.e-13*scale: continue
                        s = point-triangle[0]; u = np.dot(s,h)/determinant
                        if u < -1.e-11 or u > 1+1.e-11: continue
                        q = np.cross(s,e1); v = np.dot(direction,q)/determinant
                        if v < -1.e-11 or u+v > 1+1.e-11: continue
                        t = np.dot(e2,q)/determinant
                        if t <= tolerance: continue
                        if min(u, v, 1-u-v) <= 1.e-11:
                            ambiguous = True; break
                        hits += 1
                else:
                    stack[top] = left; stack[top+1] = right; top += 2
            if not ambiguous:
                valid += 1; votes += hits % 2
                if valid == 3: break
        if valid < 3:
            inside[i] = abs(_winding_at_point(point, triangles)) > .5; fallbacks += 1
        else:
            inside[i] = votes >= 2
    return inside, fallbacks


class MeshDistanceQuery:
    """Snapshot of a closed, consistently oriented triangle mesh.

    Distances are exact point-to-triangle distances up to floating-point error.
    Sign uses even/odd solid occupancy (negative inside), so globally reversed
    winding is harmless. Nested shells represent cavities under this policy.
    """
    def __init__(self, vertices, faces, *, leaf_size=8, weld_tolerance=1.e-10,
                 check_intersections=True):
        if int(leaf_size) != leaf_size or leaf_size < 1:
            raise ValueError('leaf_size must be a positive integer')
        vertices, faces = weld_mesh_vertices(vertices, faces, weld_tolerance)
        if not len(faces): raise ValueError('a signed-distance mesh must enclose a nonempty solid')
        topology = mesh_topology(faces, len(vertices))
        if not topology['is_watertight'] or not topology['is_consistently_oriented']:
            raise ValueError('signed distance requires a closed, manifold, consistently oriented mesh')
        scale = max(float(np.ptp(vertices, axis=0).max()), np.finfo(float).tiny)
        area2 = mesh_normals(vertices, faces, return_norms=True)[1]
        if np.any(area2 <= np.finfo(float).eps*scale*scale):
            raise ValueError('signed-distance mesh contains degenerate triangles')
        if check_intersections:
            report = check_mesh_deformation(vertices, vertices, faces, samples=2, check_intersections=True,
                                             atol=np.finfo(float).eps*scale*32)
            if report['intersections']:
                raise ValueError('signed-distance mesh contains self-intersections')
        self.vertices, self.faces = vertices.copy(), faces.copy()
        self.triangles = self.vertices[self.faces]
        self.topology = topology
        self.tolerance = 64*np.finfo(float).eps*scale
        lows = self.triangles.min(axis=1); highs = self.triangles.max(axis=1)
        centers = (lows+highs)/2
        bounds0, bounds1, nodes, order = [], [], [], []
        def build(indices):
            index = len(nodes); nodes.append(None)
            bounds0.append(lows[indices].min(axis=0)); bounds1.append(highs[indices].max(axis=0))
            if len(indices) <= leaf_size:
                nodes[index] = [-1, -1, len(order), len(indices)]; order.extend(indices.tolist())
            else:
                axis = np.ptp(centers[indices], axis=0).argmax()
                indices = indices[np.argsort(centers[indices, axis], kind='stable')]
                middle = len(indices)//2
                left = build(indices[:middle]); right = build(indices[middle:])
                nodes[index] = [left, right, 0, 0]
            return index
        build(np.arange(len(faces)))
        self._low, self._high = np.array(bounds0), np.array(bounds1)
        self._nodes, self._order = np.array(nodes, dtype=np.int64), np.array(order, dtype=np.int64)

    @staticmethod
    def _points(points):
        points = np.asarray(points, dtype=float)
        if points.ndim < 1 or points.shape[-1] != 3 or not np.all(np.isfinite(points)):
            raise ValueError('query points must be finite and have final dimension three')
        return points, points.reshape(-1, 3)

    def distance(self, points, *, return_closest=False):
        points, flat = self._points(points)
        distances, closest, ids = _distance_queries(flat, self.triangles, self._low, self._high, self._nodes, self._order)
        shape = points.shape[:-1]
        result = distances.reshape(shape)
        return (result, closest.reshape(points.shape), ids.reshape(shape)) if return_closest else result

    def contains(self, points):
        points, flat = self._points(points)
        inside, _ = _inside_queries(flat, self.triangles, self._low, self._high, self._nodes, self._order, self.tolerance)
        return inside.reshape(points.shape[:-1])

    def signed_distance(self, points):
        distances = self.distance(points)
        signed = np.where(self.contains(points), -distances, distances)
        return np.where(distances <= self.tolerance, 0., signed)


def mesh_signed_distance(points, vertices, faces, **options):
    """Convenience query; reuse MeshDistanceQuery for repeated evaluations."""
    return MeshDistanceQuery(vertices, faces, **options).signed_distance(points)
