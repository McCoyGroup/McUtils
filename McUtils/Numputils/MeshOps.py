"""Array-based mesh geometry, incidence, comparison and deformation checks.

Connectivity comparisons require a vertex correspondence. With no supplied
IDs, coincident vertices can be matched geometrically; stable ordered topology
also establishes an index correspondence. Other cases remain unresolved and
must not be interpreted as an analytical-surface topology certificate.
"""
from dataclasses import dataclass
import collections
import math
import numpy as np
import scipy
import scipy.spatial
import scipy.sparse
import scipy.sparse.csgraph
from .VectorOps import *
from . import TransformationMatrices as tmats
from . import Misc as misc
from .Options import Options
from . import CoordOps as _coords
from . import TensorDerivatives as _td

__all__ = [
    'mesh_arrays', 'MeshComparison', 'MeshVertexMap', 'MeshIncidence',
    'map_mesh_vertices', 'canonicalize_mesh_faces', 'mesh_incidence',
    'mesh_topology', 'mesh_topology_report', 'compare_meshes',
    'mesh_normals', 'mesh_vertex_normals', 'mesh_surface_area', 'mesh_volume',
    'check_mesh_deformation', 'cap_mesh_boundary_loop'
]


def mesh_arrays(vertices, faces):
    """Validate triangle geometry and return finite float vertices/integer faces."""
    vertices = np.asarray(vertices, dtype=float)
    if vertices.size == 0:
        vertices = vertices.reshape(0, 3)
    if vertices.ndim != 2 or vertices.shape[1] != 3 or not np.all(np.isfinite(vertices)):
        raise ValueError('vertices must be a finite (n,3) array')
    faces = _mesh_faces(faces)
    if faces.size and faces.max() >= len(vertices):
        raise ValueError('face index is outside the vertex array')
    return vertices, faces


def _mesh_faces(faces):
    faces = np.asarray(faces)
    if faces.size == 0:
        return np.empty((0, 3), dtype=int)
    if faces.ndim != 2 or faces.shape[1] != 3 or not np.issubdtype(faces.dtype, np.integer):
        raise ValueError('faces must be an integer (n,3) triangle array')
    if np.any(faces < 0):
        raise ValueError('negative mesh indices are not supported')
    return faces.astype(np.int64, copy=False)


def _unpack_mesh(mesh):
    if hasattr(mesh, 'verts') and hasattr(mesh, 'inds'):
        return mesh_arrays(mesh.verts, mesh.inds)
    if hasattr(mesh, 'vertices') and hasattr(mesh, 'faces'):
        return mesh_arrays(mesh.vertices, mesh.faces)
    return mesh_arrays(*mesh)


def canonicalize_mesh_faces(faces, vertex_map=None, oriented=False, return_mapping=False):
    """Canonical triangle rows, preserving duplicate multiplicity.

    ``return_mapping`` returns ``(faces, original_row_indices, winding_signs)``.
    Signs are measured relative to sorted vertex IDs. No vertices are welded.
    """
    faces = _mesh_faces(faces)
    if vertex_map is not None:
        mapping = np.asarray(vertex_map, dtype=int)
        if faces.size and faces.max() >= len(mapping):
            raise ValueError('vertex map does not cover all referenced vertices')
        faces = mapping[faces]
    permutation = np.argsort(faces, axis=1, kind='stable')
    canonical = np.take_along_axis(faces, permutation, axis=1)
    inversions = (permutation[:, 0] > permutation[:, 1]).astype(int)
    inversions += permutation[:, 0] > permutation[:, 2]
    inversions += permutation[:, 1] > permutation[:, 2]
    signs = np.where(inversions % 2, -1, 1)
    if oriented:
        canonical = canonical.copy()
        canonical[signs < 0] = canonical[signs < 0][:, [0, 2, 1]]
    order = np.lexsort(canonical.T[::-1])
    return (canonical[order], order, signs[order]) if return_mapping else canonical[order]


@dataclass
class MeshVertexMap:
    ids: tuple
    first: np.ndarray
    second: np.ndarray
    shared: np.ndarray
    added: np.ndarray
    removed: np.ndarray


def map_mesh_vertices(ids0, ids1):
    """Map unique, hashable vertex identities to one common integer pool."""
    sequences = [list(ids0), list(ids1)]
    pool = {}
    maps = []
    for sequence in sequences:
        if any(isinstance(x, (float, np.floating)) and not np.isfinite(x) for x in sequence):
            raise ValueError('vertex IDs must be finite')
        try:
            if len(set(sequence)) != len(sequence):
                raise ValueError('vertex IDs must be unique within each mesh')
            for value in sequence:
                if value not in pool:
                    pool[value] = len(pool)
            maps.append(np.array([pool[x] for x in sequence], dtype=int))
        except TypeError as error:
            raise ValueError('vertex IDs must be hashable') from error
    common = np.intersect1d(*maps)
    return MeshVertexMap(tuple(pool), *maps, common,
                         np.setdiff1d(maps[1], maps[0]), np.setdiff1d(maps[0], maps[1]))


@dataclass
class MeshIncidence:
    edges: np.ndarray
    face_edges: np.ndarray
    edge_counts: np.ndarray
    edge_orientations: np.ndarray
    vertex_faces: object
    edge_faces: object
    used_vertices: np.ndarray
    isolated_vertices: np.ndarray


def mesh_incidence(faces, nvertices=None):
    faces = _mesh_faces(faces)
    minimum = int(faces.max()) + 1 if faces.size else 0
    nvertices = minimum if nvertices is None else int(nvertices)
    if nvertices < minimum:
        raise ValueError('nvertices does not cover face indices')
    directed = faces[:, [[0, 1], [1, 2], [2, 0]]].reshape(-1, 2)
    edges, inverse, counts = np.unique(np.sort(directed, axis=1), axis=0,
                                        return_inverse=True, return_counts=True)
    signs = np.where(directed[:, 0] < directed[:, 1], 1, -1)
    vf = scipy.sparse.coo_matrix((np.ones(faces.size, dtype=int),
        (faces.ravel(), np.repeat(np.arange(len(faces)), 3))), shape=(nvertices, len(faces))).tocsr()
    ef = scipy.sparse.coo_matrix((np.ones(len(inverse), dtype=int),
        (inverse, np.repeat(np.arange(len(faces)), 3))), shape=(len(edges), len(faces))).tocsr()
    used = np.unique(faces)
    return MeshIncidence(edges, inverse.reshape(-1, 3), counts, signs.reshape(-1, 3), vf, ef,
                         used, np.setdiff1d(np.arange(nvertices), used))


def _boundary_paths(edges):
    adjacency = collections.defaultdict(list)
    unused = set()
    for a, b in edges:
        a, b = int(a), int(b)
        adjacency[a].append(b); adjacency[b].append(a)
        unused.add(tuple(sorted((a, b))))
    paths = []
    while unused:
        edge = min(unused)
        ends = [x for x in edge if len(adjacency[x]) != 2]
        start = ends[0] if ends else edge[0]
        path = [start]; current = start
        while True:
            candidates = [n for n in adjacency[current] if tuple(sorted((current, n))) in unused]
            if not candidates:
                break
            nxt = min(candidates)
            unused.remove(tuple(sorted((current, nxt))))
            path.append(nxt); current = nxt
            if current == start or len(adjacency[current]) != 2:
                break
        paths.append(np.array(path, dtype=int))
    return paths


def mesh_topology(faces, nvertices=None):
    """Surface incidence/manifold diagnostics; unused pool vertices are excluded.

    Vertex links distinguish a closed bow-tie from a manifold surface even
    when every edge has incidence two. Equal invariants do not certify isotopy.
    """
    faces = _mesh_faces(faces)
    incidence = mesh_incidence(faces, nvertices)
    edges, counts = incidence.edges, incidence.edge_counts
    canonical = canonicalize_mesh_faces(faces)
    _, duplicate_counts = np.unique(canonical, axis=0, return_counts=True)
    duplicates = canonical[1:][np.all(canonical[1:] == canonical[:-1], axis=1)]
    degenerate = np.flatnonzero(np.any(np.diff(np.sort(faces, axis=1), axis=1) == 0, axis=1))
    boundary = edges[counts == 1]
    nonmanifold = set()
    for vertex in incidence.used_vertices:
        rows = incidence.vertex_faces.indices[incidence.vertex_faces.indptr[vertex]:incidence.vertex_faces.indptr[vertex+1]]
        link = collections.defaultdict(list)
        for row in rows:
            other = faces[row][faces[row] != vertex]
            if len(other) != 2:
                nonmanifold.add(int(vertex)); continue
            a, b = map(int, other)
            link[a].append(b); link[b].append(a)
        if not link:
            nonmanifold.add(int(vertex)); continue
        visited = set(); todo = [next(iter(link))]
        while todo:
            v = todo.pop()
            if v in visited: continue
            visited.add(v); todo.extend(link[v])
        degrees = [len(v) for v in link.values()]
        valid = (all(d == 2 for d in degrees) or
                 (degrees.count(1) == 2 and all(d in (1, 2) for d in degrees)))
        if len(visited) != len(link) or not valid:
            nonmanifold.add(int(vertex))
    if len(incidence.used_vertices):
        remap = np.full(incidence.vertex_faces.shape[0], -1, dtype=int)
        remap[incidence.used_vertices] = np.arange(len(incidence.used_vertices))
        compact = remap[edges]
        graph = scipy.sparse.coo_matrix((np.ones(len(edges)), compact.T),
                                        shape=(len(incidence.used_vertices),)*2).tocsr()
        components, labels = scipy.sparse.csgraph.connected_components(graph, directed=False)
        euler = np.bincount(labels, minlength=components)
        euler -= np.bincount(labels[compact[:, 0]], minlength=components)
        euler += np.bincount(labels[remap[faces[:, 0]]], minlength=components)
    else:
        components, euler = 0, np.empty(0, dtype=int)
    orientation_sums = np.bincount(incidence.face_edges.ravel(),
                                   weights=incidence.edge_orientations.ravel(), minlength=len(edges))
    winding_edges = edges[(counts == 2) & (orientation_sums != 0)]
    paths = _boundary_paths(boundary)
    manifold = not (np.any(counts > 2) or nonmanifold or len(duplicates) or len(degenerate))
    return dict(boundary_edges=boundary, boundary_loops=paths,
        nonmanifold_edges=edges[counts > 2], nonmanifold_vertices=np.array(sorted(nonmanifold), dtype=int),
        duplicate_faces=duplicates, degenerate_faces=degenerate,
        isolated_vertices=incidence.isolated_vertices,
        components=int(components), component_euler=np.sort(euler),
        euler_characteristic=int(euler.sum()),
        n_holes=sum(len(p)>1 and p[0] == p[-1] for p in paths),
        is_manifold=bool(manifold), is_watertight=bool(manifold and not len(boundary)),
        winding_edges=winding_edges, is_consistently_oriented=not len(winding_edges))


def mesh_topology_report(vertices, faces):
    vertices, faces = mesh_arrays(vertices, faces)
    return mesh_topology(faces, len(vertices))


def mesh_normals(vertices, faces, normalize=True, return_norms=False):
    vertices, faces = mesh_arrays(vertices, faces)
    a, b, c = (vertices[faces[:, k]] for k in range(3))
    normals = np.cross(b-a, c-a)
    norms = np.linalg.norm(normals, axis=1)
    if normalize:
        normals = np.divide(normals, norms[:, None], out=np.zeros_like(normals), where=norms[:, None] > 0)
    return (normals, norms) if return_norms else normals


def mesh_vertex_normals(vertices, faces, vertex_normals=None):
    vertices, faces = mesh_arrays(vertices, faces)
    if vertex_normals is None:
        normals = np.zeros_like(vertices)
        face_normals = mesh_normals(vertices, faces, normalize=False)
        for k in range(3): np.add.at(normals, faces[:, k], face_normals)
    else:
        normals = np.asarray(vertex_normals, float)
        if normals.shape != vertices.shape: raise ValueError('vertex normals have the wrong shape')
    lengths = np.linalg.norm(normals, axis=1)
    return np.divide(normals, lengths[:, None], out=np.zeros_like(normals), where=lengths[:, None] > 0)


def mesh_surface_area(vertices, faces, return_components=False):
    terms = mesh_normals(vertices, faces, normalize=False, return_norms=True)[1]/2
    return terms if return_components else terms.sum()


def mesh_volume(vertices, faces, return_components=False, signed=False):
    vertices, faces = mesh_arrays(vertices, faces)
    a, b, c = (vertices[faces[:, k]] for k in range(3))
    terms = np.einsum('ij,ij->i', a, np.cross(b, c))/6
    return terms if return_components else (terms.sum() if signed else abs(terms.sum()))


@dataclass
class MeshComparison:
    vertex_maps: MeshVertexMap
    correspondence: str
    same_connectivity: bool
    common_faces: np.ndarray
    added_faces: np.ndarray
    removed_faces: np.ndarray
    winding_changes: np.ndarray
    topology_before: dict
    topology_after: dict
    max_displacement: object

    @property
    def topology_change_detected(self):
        a, b = self.topology_before, self.topology_after
        if not a['is_manifold'] or not b['is_manifold']:
            return None
        return a['components'] != b['components'] or not np.array_equal(a['component_euler'], b['component_euler'])


def compare_meshes(mesh0, mesh1, *, vertex_ids=None, vertex_map=None, correspondence='auto',
                   atol=1e-8, rtol=1e-7):
    """Compare meshes without conflating reordering, winding and topology.

    Auto correspondence recognizes coincident geometry (including reordered
    vertices) and unchanged indexed connectivity. Otherwise new vertices get
    disjoint IDs and the result says ``unresolved``. Ordered correspondence is
    an explicit assertion that row identity persists despite changed faces.
    """
    a, fa = _unpack_mesh(mesh0); b, fb = _unpack_mesh(mesh1)
    method = correspondence
    if vertex_ids is not None:
        if len(vertex_ids[0]) != len(a) or len(vertex_ids[1]) != len(b):
            raise ValueError('vertex ID counts must match the meshes')
        maps = map_mesh_vertices(*vertex_ids); method = 'ids'
    elif vertex_map is not None:
        mapping = np.asarray(vertex_map, int)
        if mapping.shape != (len(b),) or np.any(mapping < 0) or np.any(mapping >= len(a)) or len(np.unique(mapping)) != len(b):
            raise ValueError('vertex_map must map second-mesh vertices uniquely into the first mesh')
        maps = map_mesh_vertices(np.arange(len(a)), mapping); method = 'explicit'
    else:
        if correspondence not in ('auto', 'ordered'):
            raise ValueError('correspondence must be auto or ordered')
        mapping = None
        if correspondence == 'ordered':
            if len(a) != len(b): raise ValueError('ordered correspondence requires equal vertex counts')
            mapping = np.arange(len(b)); method = 'ordered'
        elif len(a) == len(b):
            if not len(a): mapping = np.empty(0, int); method = 'coincident'
            else:
                distance, candidate = scipy.spatial.cKDTree(a).query(b)
                tolerance = atol + rtol*np.maximum(np.linalg.norm(b, axis=1), np.linalg.norm(a[candidate], axis=1))
                # Coincident duplicate positions are ambiguous, so only accept
                # a unique bijection. Shared row connectivity is handled below.
                if np.all(distance <= tolerance) and len(np.unique(candidate)) == len(a):
                    mapping = candidate; method = 'coincident'
                elif np.array_equal(canonicalize_mesh_faces(fa), canonicalize_mesh_faces(fb)):
                    mapping = np.arange(len(a)); method = 'indexed'
        if mapping is None:
            maps = map_mesh_vertices(np.arange(len(a)), np.arange(len(b)) + len(a)); method = 'unresolved'
        else:
            maps = map_mesh_vertices(np.arange(len(a)), mapping)
    ca, ia, sa = canonicalize_mesh_faces(fa, maps.first, return_mapping=True)
    cb, ib, sb = canonicalize_mesh_faces(fb, maps.second, return_mapping=True)
    # Lists preserve multiplicity; duplicate faces remain defects in the report.
    old = collections.defaultdict(list); new = collections.defaultdict(list)
    for i, row in enumerate(ca): old[tuple(row)].append(i)
    for i, row in enumerate(cb): new[tuple(row)].append(i)
    common, added, removed, flips = [], [], [], []
    for row in sorted(old.keys() | new.keys()):
        left, right = old[row], new[row]; count = min(len(left), len(right))
        common.extend([row]*count); removed.extend([row]*(len(left)-count)); added.extend([row]*(len(right)-count))
        flips.extend(row for x,y in zip(left[:count],right[:count]) if sa[x] != sb[y])
    array = lambda rows: np.asarray(rows, dtype=int).reshape(-1,3)
    displacement = None
    if method != 'unresolved' and len(maps.shared):
        pa = {int(k): v for k,v in zip(maps.first,a)}; pb = {int(k): v for k,v in zip(maps.second,b)}
        displacement = float(max(np.linalg.norm(pa[int(k)]-pb[int(k)]) for k in maps.shared))
    return MeshComparison(maps,method,not added and not removed,array(common),array(added),array(removed),array(flips),
                           mesh_topology(fa,len(a)),mesh_topology(fb,len(b)),displacement)


def check_mesh_deformation(vertices0, vertices1, faces, *, samples=9, check_intersections=True, atol=1e-10):
    """Sampled diagnostics of a specified linear deformation, not a CCD proof.

    Area minima are also located analytically: squared cross-product norm is
    quartic in interpolation time. Optional intersection checks exclude normal
    adjacent face contacts and use bounding boxes before triangle tests.
    """
    a, faces = mesh_arrays(vertices0, faces); b, _ = mesh_arrays(vertices1, faces)
    if a.shape != b.shape: raise ValueError('deformation needs corresponding vertex arrays')
    if int(samples) != samples or samples < 2: raise ValueError('samples must be an integer >= 2')
    tri0, delta = a[faces], (b-a)[faces]
    u, v = tri0[:,1]-tri0[:,0],tri0[:,2]-tri0[:,0]
    du, dv = delta[:,1]-delta[:,0],delta[:,2]-delta[:,0]
    cross = np.stack([np.cross(u,v),np.cross(du,v)+np.cross(u,dv),np.cross(du,dv)],axis=1)
    candidates = set(np.linspace(0,1,int(samples)).tolist()); collapsed = set()
    for i, c in enumerate(cross):
        polynomial = np.zeros(5)
        for k in range(3): polynomial += np.convolve(c[:,k],c[:,k])
        derivative = np.arange(1,5)*polynomial[1:]
        roots = np.polynomial.polynomial.polyroots(np.trim_zeros(derivative,'b')) if np.any(derivative) else []
        local = [0.,1.] + [float(r.real) for r in roots if abs(r.imag)<1e-9 and 0<r.real<1]
        candidates.update(local)
        if min(np.polynomial.polynomial.polyval(t,polynomial) for t in local) <= atol**2:
            collapsed.add(i)
    intersections = []
    for t in sorted(candidates):
        pts = a + t*(b-a)
        if check_intersections:
            tris = pts[faces]; boxes = (tris.min(1),tris.max(1))
            centers=(boxes[0]+boxes[1])/2
            radii=np.linalg.norm((boxes[1]-boxes[0])/2,axis=1)
            pairs=scipy.spatial.cKDTree(centers).query_pairs(2*radii.max()+atol,output_type='ndarray') if len(faces) else np.empty((0,2),int)
            for i,j in pairs:
                if np.any(boxes[1][i]+atol<boxes[0][j]) or np.any(boxes[1][j]+atol<boxes[0][i]):continue
                if np.intersect1d(faces[i],faces[j]).size:continue
                if tri_tri_intersect(tris[i],tris[j],eps=atol):intersections.append((float(t),int(i),int(j)))
    return dict(valid=not collapsed and not intersections,degenerate_faces=np.array(sorted(collapsed),int),
                intersections=intersections,sample_times=np.array(sorted(candidates)),
                continuous_collision_certified=False)


def cap_mesh_boundary_loop(vertices, loop, new_vertex_id):
    """Centroid fan for a small convex/star-shaped loop; no automatic repair."""
    loop = np.asarray(loop,int)
    if len(loop)>1 and loop[0] == loop[-1]: loop = loop[:-1]
    if len(loop)<3: raise ValueError('a boundary cap needs at least three vertices')
    return np.asarray(vertices)[loop].mean(0),np.column_stack([loop,np.roll(loop,-1),np.full(len(loop),new_vertex_id)])


# Migrated polygon, intersection and mesh-generation routines.
def polygon_normal(vertices, normalize=True):
    """Newell normal, following the polygon's vertex winding."""
    vertices = np.asarray(vertices, float)
    if vertices.ndim < 2 or vertices.shape[-1] != 3 or vertices.shape[-2] < 3:
        raise ValueError('polygon vertices must have shape (..., n>=3, 3)')
    normal = np.cross(vertices, np.roll(vertices, -1, axis=-2)).sum(axis=-2)
    if normalize:
        length = np.linalg.norm(normal, axis=-1, keepdims=True)
        normal = np.divide(normal, length, out=np.zeros_like(normal), where=length > 0)
    return normal


def winding_sign(u, v, axis1=0, axis2=1, return_component=False, zero_threshold=1e-8):
    u = np.asanyarray(u)
    v = np.asanyarray(v)
    z = u[..., axis1] * v[..., axis2] - u[..., axis2] * v[..., axis1]
    if not return_component:
        z = np.asanyarray(z)
        z[np.abs(z) < zero_threshold] = 0
        z = np.sign(z)
    return z


def winding_number(points, polygon, axis1=0, axis2=1, zero_threshold=None):
    pts   = np.asanyarray(points)
    verts = np.asanyarray(polygon)
    v1 = verts
    v2 = np.roll(verts, -1, axis=-2)

    x,  y  = pts[..., axis1],  pts[..., axis2]
    y1, y2 = v1[..., axis2],  v2[..., axis2]
    upward = (y1[..., np.newaxis, :] <= y[..., :, np.newaxis]) & (y2[..., np.newaxis, :] >  y[..., :, np.newaxis])
    downward = (y1[..., np.newaxis, :] >  y[..., :, np.newaxis]) & (y2[..., np.newaxis, :] <= y[..., :, np.newaxis])


    x1, x2 = v1[..., axis1], v2[..., axis1]
    cross = (
        (x2 - x1)[..., np.newaxis, :] * (y[..., :, np.newaxis] - y1[..., np.newaxis, :]) -
        (x[..., :, np.newaxis] - x1[..., np.newaxis, :]) * (y2 - y1)[..., np.newaxis, :]
    )

    if zero_threshold is None:
        zero_threshold = Options.zero_threshold
    w = np.sum(
        upward & (cross > zero_threshold),
         axis=-1
    ) - np.sum(
        downward & (cross < -zero_threshold),
         axis=-1
    )
    return w


def point_in_triangle(p, a, b, c, diffs=None, windings=None, **winding_args):
    #TODO: handle coincident lines
    if windings is not None:
        d1, d2, d3 = windings
    else:
        if diffs is not None:
            a, b, c = diffs
        else:
            a, b, c = a - p, b - p, c - p
        d1 = winding_sign(a, b, **winding_args)
        d2 = winding_sign(b, c, **winding_args)
        d3 = winding_sign(c, a)
    if misc.is_numeric(d1):
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        return not (has_neg and has_pos)
    else:
        d1, d2, d3 = np.asanyarray(d1), np.asanyarray(d2), np.asanyarray(d3)
        has_neg = (d1 < 0) | (d2 < 0) | (d3 < 0)
        has_pos = (d1 > 0) | (d2 > 0) | (d3 > 0)
        return ~(has_neg & has_pos)


def is_polygon_ear(plane_points, indices, i, j, k, diffs=None, windings=None):
    a, b, c = plane_points[i], plane_points[j], plane_points[k]
    # Ear must be a convex vertex (positive cross product = CCW winding)
    if windings is None: # precomputed winding signs
        if diffs is not None:
            if winding_sign(diffs[j, i], diffs[k, i]) <= 0:
                return False
        else:
            if winding_sign(b - a, c - a) <= 0:
                return False
    else:
        if windings[i, j, k] <= 0:
            return False

    # No other vertex may lie inside the candidate ear triangle
    for m, idx in enumerate(indices):
        if idx in (i, j, k):
            continue
        if windings is None:
            if diffs is not None:
                if point_in_triangle(None, None, None, None,
                                     diffs=(diffs[i, idx], diffs[j, idx], diffs[k, idx])):
                    return False
            else:
                if point_in_triangle(plane_points[idx], a, b, c):
                    return False
        else:
            if point_in_triangle(None, None, None, None,
                                 windings=(windings[idx, a, b], windings[idx, b, c], windings[idx, c, a])):
                return False
    return True


def ear_clipping_triangulation(plane_points, indices, diffs=None, windings=None):
    plane_points = np.asanyarray(plane_points)
    n = len(plane_points)

    if diffs is None:
        diffs = plane_points[..., :, np.newaxis, :] - plane_points[..., np.newaxis, :, :]

    if windings is True:
        # compute all winding signs
        raise NotImplementedError("not sure precomputing windings is useful")

    triangles = []
    indices = list(indices)
    for _ in range(n**2):
        ear_found = False
        for i in range(len(indices)):
            prev = indices[(i - 1) % len(indices)]
            curr = indices[i]
            next = indices[(i + 1) % len(indices)]
            if is_polygon_ear(plane_points, indices, prev, curr, next, diffs=diffs, windings=windings):
                triangles.append((prev, curr, next))
                indices.pop(i)
                ear_found = True
                break

        if not ear_found:
            raise ValueError("No ear found — polygon may be self-intersecting or degenerate")

        if len(indices) <= 3:
            break
    else:
        raise ValueError("Ear-clipping failed — polygon may be self-intersecting")

    triangles.append((indices[0], indices[1], indices[2]))
    return triangles


def triangulate_polygon(vertices):
    """Ear-clip a polygon in its Newell plane, retaining its winding."""
    vertices = np.asarray(vertices, float)
    if vertices.ndim != 2 or vertices.shape[1] != 3 or len(vertices) < 3:
        raise ValueError('polygon vertices must have shape (n>=3,3)')
    if len(vertices) == 3:
        return np.arange(3)
    normal = polygon_normal(vertices)
    if not np.any(normal):
        raise ValueError('degenerate polygon has no plane normal')
    reference = np.eye(3)[np.argmin(abs(normal))]
    u = np.cross(reference, normal); u /= np.linalg.norm(u)
    v = np.cross(normal, u)
    plane = np.stack([vertices @ u, vertices @ v], axis=-1)
    return np.asarray(ear_clipping_triangulation(plane, list(range(len(vertices)))), dtype=int)


def tri_tri_intersect(t1: np.ndarray, t2: np.ndarray, eps: float = 1e-9) -> bool:
    """
    Test whether two triangles in 3D intersect.
    t1, t2 : (3, 3) arrays of vertex positions.
    Returns True if they share any point (including edge/vertex touches).
    """
    def plane_of(tv):
        n = np.cross(tv[1] - tv[0], tv[2] - tv[0])
        ln = np.linalg.norm(n)
        if ln < eps:
            return None, None          # degenerate triangle
        n = n / ln
        return n, -np.dot(n, tv[0])   # (normal, offset d)  →  n·x + d = 0

    # ── Step 1: plane rejection ───────────────────────────────────────────────
    n2, d2 = plane_of(t2)
    if n2 is None:
        return False

    sd1 = t1 @ n2 + d2                # signed dists of T1 verts to plane(T2)
    if np.all(sd1 >  eps) or np.all(sd1 < -eps):
        return False                  # T1 strictly on one side of plane(T2)

    n1, d1 = plane_of(t1)
    if n1 is None:
        return False

    sd2 = t2 @ n1 + d1                # signed dists of T2 verts to plane(T1)
    if np.all(sd2 >  eps) or np.all(sd2 < -eps):
        return False                  # T2 strictly on one side of plane(T1)

    # ── Step 2: coplanar case ────────────────────────────────────────────────
    L = np.cross(n1, n2)
    if np.linalg.norm(L) < eps:
        return _coplanar_tri_tri(t1, t2, n1, eps)

    # ── Step 3: compute overlap intervals on L ───────────────────────────────
    # Project vertices onto L (use largest-magnitude axis for numerical stability)
    ax = np.argmax(np.abs(L))

    def interval(tv, sd):
        """Scalar interval [lo, hi] of tv's intersection with L."""
        p = tv[:, ax]
        pts = []
        for i in range(3):
            j = (i + 1) % 3
            si, sj = sd[i], sd[j]
            if abs(si - sj) < eps:
                continue
            if si * sj <= 0:          # edge crosses or touches the other plane
                t = si / (si - sj)
                pts.append(p[i] + t * (p[j] - p[i]))
        # Verts that lie exactly on the plane also count
        pts += [p[i] for i in range(3) if abs(sd[i]) <= eps]
        if len(pts) < 2:
            return None, None
        return min(pts), max(pts)

    lo1, hi1 = interval(t1, sd1)
    lo2, hi2 = interval(t2, sd2)

    if lo1 is None or lo2 is None:
        return False

    return hi1 >= lo2 - eps and hi2 >= lo1 - eps   # intervals overlap?


def _project_2d(tri, normal):
    """Drop the axis most aligned with the normal → 2D projection."""
    ax = np.argmax(np.abs(normal))
    keep = [i for i in range(3) if i != ax]
    return tri[:, keep]


def _segments_intersect_2d(p1, p2, p3, p4, eps=1e-9) -> bool:
    """Do line segments p1–p2 and p3–p4 intersect?"""
    d1, d2 = p2 - p1, p4 - p3
    cross = d1[0]*d2[1] - d1[1]*d2[0]
    diff  = p3 - p1
    if abs(cross) < eps:           # parallel
        return False
    t = (diff[0]*d2[1] - diff[1]*d2[0]) / cross
    u = (diff[0]*d1[1] - diff[1]*d1[0]) / cross
    return -eps <= t <= 1+eps and -eps <= u <= 1+eps


def _point_in_tri_2d(p, tri2d, eps=1e-9) -> bool:
    """Is point p inside triangle tri2d (2D)?"""

    def sign(a, b, c):
        return (a[0]-c[0])*(b[1]-c[1]) - (b[0]-c[0])*(a[1]-c[1])
    d1 = sign(p, tri2d[0], tri2d[1])
    d2 = sign(p, tri2d[1], tri2d[2])
    d3 = sign(p, tri2d[2], tri2d[0])
    has_neg = (d1 < -eps) or (d2 < -eps) or (d3 < -eps)
    has_pos = (d1 >  eps) or (d2 >  eps) or (d3 >  eps)
    return not (has_neg and has_pos)


def _coplanar_tri_tri(t1, t2, normal, eps=1e-9) -> bool:
    a, b = _project_2d(t1, normal), _project_2d(t2, normal)
    # Edge–edge intersections
    for i in range(3):
        for j in range(3):
            if _segments_intersect_2d(a[i], a[(i+1)%3],
                                       b[j], b[(j+1)%3], eps):
                return True
    # One triangle fully inside the other?
    if _point_in_tri_2d(a[0], b, eps):
        return True
    if _point_in_tri_2d(b[0], a, eps):
        return True
    return False


def triangle_plane_embedding(tris, zero_threshold=None):
    tris = np.asanyarray(tris)
    crosses = vec_crosses(tris[..., 0, :] - tris[..., 1, :], tris[..., 2, :] - tris[..., 1, :])
    crosses, norms = vec_normalize(crosses, return_norms=True)
    if zero_threshold is None:
        zero_threshold = Options
    dead_points = norms < zero_threshold
    shift = -vec_dots(crosses, tris[1])
    return (crosses, shift), dead_points


def check_triangle_plane_offsets(t1, t2, embeddings=None, zero_threshold=None, return_distances=False):
    if embeddings is None:
        embeddings = triangle_plane_embedding(t1)[0], triangle_plane_embedding(t2)[0]
    (n1, d1), (n2, d2) = embeddings

    if zero_threshold is None:
        zero_threshold = Options.zero_threshold

    sd1 = np.reshape(t1 @ n2[..., :, np.newaxis] + d2[..., np.newaxis], d2.shape)
    mask = np.all(sd1 > zero_threshold, axis=-1) | np.all(sd1 < -zero_threshold, axis=-1)

    submask = np.where(mask)
    n1 = n1[submask]
    d1 = d1[submask]
    t2 = t2[submask]

    sd2 = np.reshape(t2 @ n1[..., :, np.newaxis] + d1[..., np.newaxis], d1.shape)
    subsubmask = np.any(sd2 < zero_threshold, axis=-1) & np.any(sd2 > -zero_threshold, axis=-1) # note boolean flip
    s2 = tuple(s[subsubmask] for s in submask)

    if return_distances:
        sd2_full = np.zeros_like(sd1)
        sd2_full[submask] = sd2

    mask[s2] = False
    if return_distances:
        return mask, (sd1, sd2_full)
    else:
        return mask


def check_coplanar_triangle_intersection(t1, t2, embeddings=None, zero_threshold=None,
                                         return_crosses=False):
    if embeddings is None:
        embeddings = triangle_plane_embedding(t1)[0], triangle_plane_embedding(t2)[0]
    (n1, d1), (n2, d2) = embeddings

    base_shape = t1.shape[:-2]
    n1 = n1.reshape((-1,) + n1.shape[-1:])
    t1 = t1.reshape((-1,) + t1.shape[-2:])
    n2 = n2.reshape((-1,) + n2.shape[-1:])
    t2 = t2.reshape((-1,) + t2.shape[-2:])

    crosses = vec_crosses(n1, n2)
    cross_norms = vec_norms(crosses)
    if zero_threshold is None:
        zero_threshold = Options.zero_threshold

    mask = cross_norms < zero_threshold # coplanar, need to check
    check_inds = np.where(mask)

    if len(check_inds[0]) > 0:
        n1 = n1[mask]
        t1 = t1[mask]
        # n2 = n2[mask]
        t2 = t2[mask]

        # fast pseudo-2d projection for checks
        i1 = np.argmax(np.abs(n1), axis=-1)
        submask = np.full(t1.shape, True)
        submask[np.arange(len(t1)), :, i1] = False
        a = t1[submask].reshape(t1.shape[:-1] + (t1.shape[-1] - 1,))
        b = t2[submask].reshape(t2.shape[:-1] + (t2.shape[-1] - 1,))

        # if any segments intersect we can short circuit
        for i in range(3): # 3 points in a triangle
            for j in range(3):
                seg_mask = check_segment_intersection_2d(
                    a[..., i, :], a[..., (i + 1) % 3, :],
                    b[..., j, :], b[..., (j + 1) % 3, :],
                    zero_threshold=zero_threshold
                )
                nsm = ~seg_mask

                a = a[nsm]
                b = b[nsm]
                check_inds = tuple(m[nsm] for m in check_inds)
                if len(check_inds[0]) == 0:
                    break
            if len(check_inds[0]) == 0:
                break

        if len(check_inds[0]) > 0:
            # One triangle fully inside the other?
            contained_mask = point_in_triangle(a[..., 0, :], *np.moveaxis(b, -2, 0), zero_threshold)
            ncm = ~contained_mask
            a = a[ncm]
            b = b[ncm]
            check_inds = tuple(m[ncm] for m in check_inds)

        if len(check_inds[0]) > 0:
            contained_mask = point_in_triangle(b[..., 0, :], *np.moveaxis(a, -2, 0), zero_threshold)
            ncm = ~contained_mask
            check_inds = tuple(m[ncm] for m in check_inds)
            mask[check_inds] = False

    mask = mask.reshape(base_shape)
    if return_crosses:
        return mask, crosses
    else:
        return mask


def get_bounding_boxes(polys, concatentate=False):
    min_vals = np.min(polys, axis=-2)
    max_vals = np.max(polys, axis=-2)

    if concatentate:
        return np.concatenate((min_vals[..., np.newaxis], max_vals[..., np.newaxis]), axis=-1)
    else:
        return min_vals, max_vals


def check_interval_overlaps(bounds_1, bounds_2, include_endpoints=True, zero_threshold=None):
    m1, M1 = bounds_1
    m2, M2 = bounds_2
    m1 = np.asanyarray(m1)
    M1 = np.asanyarray(M1)
    m2 = np.asanyarray(m2)
    M2 = np.asanyarray(M2)

    if zero_threshold is None:
        zero_threshold = Options.zero_threshold
    M1 = M1 + zero_threshold
    M2 = M2 + zero_threshold

    if include_endpoints:
        mask = (M2 >= m1) & (M1 >= m2)
    else:
        mask = (M2 > m1) & (M1 > m2)

    return mask


def check_bbox_intersections(polys1, polys2, zero_threshold=None):
    a, b = np.asarray(polys1), np.asarray(polys2)
    tolerance = Options.zero_threshold if zero_threshold is None else zero_threshold
    return np.all((a.max(axis=-2) + tolerance >= b.min(axis=-2)) &
                  (b.max(axis=-2) + tolerance >= a.min(axis=-2)), axis=-1)


def check_line_intersection(line_1, line_2, zero_threshold=None):
    p1, d1 = line_1
    p2, d2 = line_2
    p1, d1, p2, d2 = np.asanyarray(p1), np.asanyarray(d1), np.asanyarray(p2), np.asanyarray(d2)
    M = np.concatenate([d1[..., np.newaxis, :], -d2[..., np.newaxis, :]])
    rhs = p2 - p1

    (s, t), residuals, rank, _ = np.linalg.lstsq(M, rhs, rcond=None)

    # Lines intersect iff the system is solved exactly
    if len(residuals) == 0:
        residual = np.linalg.norm(M @ np.array([s, t]) - rhs)
    else:
        residual = float(np.sqrt(residuals[0]))

    if zero_threshold is None:
        zero_threshold = Options.zero_threshold
    mask = residual < zero_threshold
    s[~mask] = 0
    t[~mask] = 0

    return mask, s, t


def check_segment_intersection(p1, p2, p3, p4, zero_threshold=None):
    p1 = np.asanyarray(p1)
    if p1.ndim == 2:
        return check_segment_intersection_2d(p1, p2, p3, p4, zero_threshold=zero_threshold)
    else:
        p2 = np.asanyarray(p2)
        p3 = np.asanyarray(p3)
        p4 = np.asanyarray(p4)
        line_1 = p1, (p2 - p1)
        line_2 = p3, (p4 - p3)
        mask, s, t = check_line_intersection(line_1, line_2, zero_threshold=zero_threshold)
        d1 = vec_norms(line_1[1][mask])
        d2 = vec_norms(line_2[1][mask])
        mask[mask] = (-zero_threshold < s[mask]) & (s[mask] < d1) & (-zero_threshold < t[mask]) & (t[mask] < d2)
        return mask


def check_segment_intersection_2d(p1, p2, p3, p4, axis1=0, axis2=1, zero_threshold=None):
        p1, p2, p3, p4 = np.asanyarray(p1), np.asanyarray(p2), np.asanyarray(p3), np.asanyarray(p4)

        if zero_threshold is None:
            zero_threshold = Options.zero_threshold
        d1, d2 = p2 - p1, p4 - p3
        cross = d1[..., axis1] * d2[..., axis2] - d1[..., axis2] * d2[..., axis1]
        mask = np.abs(cross) > zero_threshold

        mask_inds = np.where(mask)

        diff = p3[mask] - p1[mask]
        d1 = d1[mask]
        d2 = d2[mask]
        t = (diff[..., axis1] * d2[..., axis2] - diff[..., axis2] * d2[..., axis1])
        u = (diff[..., axis1] * d1[..., axis2] - diff[..., axis2] * d1[..., axis1])

        submask = (
                (-zero_threshold < t ) &  (t < cross * (1 + zero_threshold))
                & (-zero_threshold < u) & (u < cross * (1 + zero_threshold))
        )
        submask = ~submask # TODO: just invert the checks...
        mask_inds = tuple(m[submask] for m in mask_inds)
        mask[mask_inds] = False

        return mask


def _tri_overlap_intervals(p, sd, zero_threshold=None):
    """Scalar intervals [lo, hi] for the triangle intersection points along the normal axis"""
    if zero_threshold is None:
        zero_threshold = Options.zero_threshold

    needs_bounds = np.full(p.shape[:-1], sd)
    min_bounds = np.zeros(p.shape[:-1], dtype=p.dtype)
    max_bounds = np.zeros(p.shape[:-1], dtype=p.dtype)
    for i in range(3): # three points in a triangle
        boundary_mask = np.where(np.abs(sd[..., i]) < zero_threshold)
        if len(boundary_mask[0]) > 0:
            new_mask = needs_bounds[boundary_mask]
            rem_mask = ~new_mask
            new_mask = tuple(bm[new_mask] for bm in boundary_mask)
            min_bounds[new_mask] = p[..., i][boundary_mask]
            max_bounds[new_mask] = p[..., i][boundary_mask]
            if np.any(rem_mask):
                rem_mask = tuple(bm[rem_mask] for bm in boundary_mask)
                min_bounds[rem_mask] = np.min([min_bounds[rem_mask], p[..., i][rem_mask]], axis=0)
                max_bounds[rem_mask] = np.min([max_bounds[rem_mask], p[..., i][rem_mask]], axis=0)
            needs_bounds[boundary_mask] = False

    for i in range(3):
        j = (i + 1) % 3
        si, sj = sd[..., i], sd[..., j]
        ds = si - sj
        edge_mask = (
                np.abs(ds) > zero_threshold
                & (si * sj) <= 0
        )
        edge_mask = np.where(np.abs(sd[..., i]) < zero_threshold)
        if len(edge_mask[0]) > 0: # edge crosses or touches the other plane
            t = si[edge_mask] / ds[edge_mask]
            pi = p[..., i][edge_mask]
            pj = p[..., j][edge_mask]
            new_p = pi + t * (pj - pi)

            new_mask = needs_bounds[edge_mask]
            rem_mask = ~new_mask
            new_new_p = new_p[new_mask]
            rem_new_p = new_p[rem_mask]
            new_mask = tuple(bm[new_mask] for bm in edge_mask)
            min_bounds[new_mask] = new_new_p
            max_bounds[new_mask] = new_new_p
            if np.any(rem_mask):
                rem_mask = tuple(bm[rem_mask] for bm in edge_mask)
                min_bounds[rem_mask] = np.min([min_bounds[rem_mask], rem_new_p], axis=0)
                max_bounds[rem_mask] = np.min([max_bounds[rem_mask], rem_new_p], axis=0)
            needs_bounds[edge_mask] = False

    return needs_bounds, min_bounds, max_bounds


def check_triangle_intersection(tris1, tris2,
                                embeddings=None,
                                check_indices=None,
                                check_direct_product=False,
                                zero_threshold=None):
    tris1 = np.asanyarray(tris1)
    tris2 = np.asanyarray(tris2)
    if embeddings is None:
        embeddings = triangle_plane_embedding(tris1), triangle_plane_embedding(tris2)
    ((e1, d1), mask1), ((e2, d2), mask2) = embeddings
    if check_indices is None and check_direct_product:
        check_indices = np.meshgrid(np.arange(len(tris1)), np.arange(len(tris2)))
    if check_indices is not None:
        i, j = check_indices
        e1 = e1[..., i, :]
        mask1 = mask1[..., i]
        d1 = d1[..., i]
        e2 = e2[..., j, :]
        mask2 = mask2[..., j]
        d2 = d2[..., j]

    full_mask = mask1 & mask2
    submask = np.where(full_mask)
    tris1 = tris1[submask]
    e1 = e1[submask]
    d1 = d1[submask]
    tris2 = tris2[submask]
    e2 = e2[submask]
    d2 = d2[submask]

    if zero_threshold is None:
        zero_threshold = Options.zero_threshold

    ## duplicates later effort
    # bbox_mask = check_bbox_intersections(tris1, tris2, zero_threshold=zero_threshold)
    # s2 = tuple(s[bbox_mask] for s in submask)
    # full_mask[s2] = False
    #
    # nbm = ~bbox_mask
    # submask = tuple(s[nbm] for s in submask)
    # tris1 = tris1[submask]
    # e1 = e1[submask]
    # d1 = d1[submask]
    # tris2 = tris2[submask]
    # e2 = e2[submask]
    # d2 = d2[submask]

    if len(submask[0]) > 0:
        plane_mask, dists = check_triangle_plane_offsets(tris1, tris2,
                                                         embeddings=((e1, d1), (e2, d2)),
                                                         zero_threshold=zero_threshold,
                                                         return_distances=True)
        s2 = tuple(s[plane_mask] for s in submask)
        full_mask[s2] = False

        npm = ~plane_mask
        submask = tuple(s[npm] for s in submask)
        tris1 = tris1[submask]
        e1 = e1[submask]
        d1 = d1[submask]
        tris2 = tris2[submask]
        e2 = e2[submask]
        d2 = d2[submask]

        dists = (dists[0][submask], dists[1][submask])

    if len(submask[0]) > 0:
        coplanar_mask, crosses = check_coplanar_triangle_intersection(tris1, tris2,
                                                                      embeddings=((e1, d1), (e2, d2)),
                                                                      zero_threshold=zero_threshold,
                                                                      return_crosses=True)
        s2 = tuple(s[coplanar_mask] for s in submask)
        full_mask[s2] = False

        npm = ~coplanar_mask
        submask = tuple(s[npm] for s in submask)
        tris1 = tris1[submask]
        # e1 = e1[submask]
        # d1 = d1[submask]
        tris2 = tris2[submask]
        # e2 = e2[submask]
        # d2 = d2[submask]

        crosses = crosses[submask]
        dists = (dists[0][submask], dists[1][submask])

    if len(submask[0]) > 0:
        ax = np.argmax(np.abs(crosses), axis=-1)
        a = np.take_along_axis(tris1, ax, axis=-1)
        b = np.take_along_axis(tris2, ax, axis=-1)

        missing1, lo1, hi1 = _tri_overlap_intervals(a, dists[0])
        missing2, lo2, hi2 = _tri_overlap_intervals(b, dists[1])

        done_mask = missing1 | missing2
        s2 = tuple(s[done_mask] for s in submask)
        full_mask[s2] = False

        rem_mask = ~done_mask
        submask = tuple(s[rem_mask] for s in submask)
        no_intersection = ~check_interval_overlaps(
            (lo1[rem_mask], hi1[rem_mask]),
            (lo2[rem_mask], hi2[rem_mask]),
        )
        submask = tuple(s[no_intersection] for s in submask)
        full_mask[submask] = False

    return full_mask


def fibonacci_sphere(samples):
    if int(samples) != samples or samples < 0:
        raise ValueError('samples must be a nonnegative integer')
    samples = int(samples)
    if samples == 0: return np.empty((0,3))
    if samples == 1: return np.array([[0.,1.,0.]])
    i = np.arange(samples)
    y = 1 - 2*i/(samples-1)
    radius = np.sqrt(np.maximum(0,1-y*y))
    theta = np.pi*(np.sqrt(5)-1)*i
    return np.stack([radius*np.cos(theta), y, radius*np.sin(theta)], axis=-1)


def uv_mapping(uv):
    """
    Map points on [0,1]^2 onto the unit sphere S^2 via the cylindrical
    equal-area (Lambert / "hat-box") projection:

        z   = 2v - 1
        phi = 2*pi*u
        x,y = sqrt(1-z^2)*cos(phi), sqrt(1-z^2)*sin(phi)

    By Archimedes' hat-box theorem, orthogonal projection of the sphere
    onto its circumscribing cylinder is area-preserving, so this map is
    the inverse of that projection: it sends the *uniform* measure on the
    square to the *uniform* (surface-area) measure on the sphere. That
    means a low-discrepancy sequence on the square pushes forward to a
    low-discrepancy-ish sample on the sphere -- no low-discrepancy
    structure is invented in 3D, but no uniformity is lost in translation
    either, since z is uniform in [-1,1] and phi uniform in [0,2*pi)
    are exactly the two conditions that characterize the uniform
    distribution on S^2.

    Parameters
    ----------
    uv : (N,2) array, both columns in [0,1)

    Returns
    -------
    (N,3) array of points on the unit sphere
    """
    u, v = uv[..., 0], uv[..., 1]
    z = 2.0 * v - 1.0
    phi = 2.0 * np.pi * u
    r = np.sqrt(np.clip(1.0 - z * z, 0.0, None))
    return np.moveaxis(np.array([r * np.cos(phi), r * np.sin(phi), z]), 0, -1)


def uv_sphere(polar_samples, azimuthal_samples, return_faces=True):
    n_theta = max(int(polar_samples), 2)
    n_phi = max(int(azimuthal_samples), 3)

    # --- vertex directions (unit sphere) ------------------------------------ #
    theta = np.pi * np.arange(1, n_theta) / n_theta  # interior rings only
    phi = 2 * np.pi * np.arange(n_phi) / n_phi
    st, ct = np.sin(theta), np.cos(theta)
    cp, sp = np.cos(phi), np.sin(phi)
    ring = np.stack([
        np.outer(st, cp),
        np.outer(st, sp),
        np.broadcast_to(ct[:, None], (n_theta - 1, n_phi)),
    ], axis=-1).reshape(-1, 3)
    dirs = np.concatenate([
        [[0.0, 0.0, 1.0]],  # north pole
        ring,
        [[0.0, 0.0, -1.0]],  # south pole
    ], axis=0)

    north, south = 0, len(dirs) - 1

    index_map: np.ndarray[int] = (
            1
            + np.arange(0, n_theta + 1)[:, np.newaxis] * n_phi
            + (np.arange(n_phi + 1)[np.newaxis, :] % n_phi)
    )

    if return_faces:
        faces = np.empty((2 * n_phi + 2 * (n_theta - 2) * n_phi, 3), dtype=int)
        offset, end = 0, n_phi
        # north cap
        faces[offset:end, 0] = north
        faces[offset:end, 1] = index_map[0, :n_phi]
        faces[offset:end, 2] = index_map[0, 1:n_phi+1]
        offset = end
        # quad bands
        i = np.arange(n_theta - 2)
        j = np.arange(n_phi)
        a = index_map[np.ix_(i, j)].reshape(-1)
        b = index_map[np.ix_(i, j + 1)].reshape(-1)
        c = index_map[np.ix_(i + 1, j)].reshape(-1)
        d = index_map[np.ix_(i + 1, j+1)].reshape(-1)
        end = offset + 2 * len(a)
        faces[offset:end:2, 0] = a
        faces[offset:end:2, 1] = b
        faces[offset:end:2, 2] = c
        faces[offset+1:end:2, 0] = b
        faces[offset+1:end:2, 1] = c
        faces[offset+1:end:2, 2] = d
        offset = end
        # south cap
        end = offset + n_phi
        last = n_theta - 1
        faces[offset:end, 0] = south
        j = np.arange(n_phi)
        faces[offset:end, 1] = index_map[last-1, j + 1]
        faces[offset:end, 2] = index_map[last-1, j]

        # orient outward, independent of the construction winding above
        tri = dirs[faces]
        fn = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        flip = np.einsum('ij,ij->i', fn, tri.mean(axis=1)) < 0
        faces[flip] = faces[flip][:, ::-1]

        return dirs, faces
    else:
        return dirs


def uv_cylinder(azimuthal_samples, return_faces=True):
    n_phi = max(int(azimuthal_samples), 3)
    start = np.array([0, 0, 0])
    end = np.array([0, 0, 1])

    phi = 2 * np.pi * np.arange(n_phi) / n_phi
    cp = np.cos(phi)
    sp = np.sin(phi)

    verts = np.zeros((2*n_phi + 2, 3), dtype=float)
    verts[1:n_phi+1, 0] = cp
    verts[1:n_phi+1, 1] = sp
    verts[n_phi+1:2*n_phi+1, 0] = cp
    verts[n_phi+1:2*n_phi+1, 1] = sp
    verts[n_phi+1:2*n_phi+1, 2] = 1 # offset along z
    verts[-1, 2] = 1

    if return_faces:
        faces = np.empty((4*n_phi, 3), dtype=int)

        j = np.arange(n_phi)

        # bottom cap
        cb = 0
        faces[:n_phi, 0] = cb
        faces[:n_phi, 1] = 1 + (j + 1) % n_phi
        faces[:n_phi, 2] = 1 + j

        off = 1
        # barrel
        b0, b1 = off + j, off + (j + 1) % n_phi
        t0, t1 = off + n_phi + j, off + n_phi + (j + 1) % n_phi
        faces[n_phi:3*n_phi:2, 0] = b0
        faces[n_phi:3*n_phi:2, 1] = b1
        faces[n_phi:3*n_phi:2, 2] = t0
        faces[n_phi+1:3*n_phi:2, 0] = b1
        faces[n_phi+1:3*n_phi:2, 1] = t1
        faces[n_phi+1:3*n_phi:2, 2] = t0

        # top cap
        off = n_phi + 1
        ct = off + n_phi
        faces[3*n_phi:, 0] = ct
        faces[3*n_phi:, 1] = off + j
        faces[3*n_phi:, 2] = off + (j + 1) % n_phi

        faces = np.array(faces, dtype=np.int64)
        tri = verts[faces]  # robust outward orientation
        fn = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        flip = np.einsum('ij,ij->i', fn, tri.mean(axis=1) - (start + end) / 2) < 0
        faces[flip] = faces[flip][:, ::-1]
        return verts, faces
    return verts


def uv_cone(azimuthal_samples, top_radius=0, tol=1e-6, return_faces=True):
    cyl_data = uv_cylinder(azimuthal_samples, return_faces=return_faces)
    if not return_faces:
        verts = cyl_data
        faces = None
    else:
        verts, faces = cyl_data

    n_phi = max(int(azimuthal_samples), 3)
    if top_radius < tol:
        verts = np.concatenate([
            verts[:1+n_phi],
            verts[(-1,), :]
        ], axis=0)
        faces = faces[:n_phi]
        top = faces.copy()
        top[:, 0] = len(verts) - 1
        top = top[:, ::-1]
        faces = np.concatenate([faces, top], axis=0)
    else:
        verts[1+n_phi:, :2] *= top_radius

    if return_faces:
        return verts, faces
    else:
        return faces


def uv_box(return_faces=True, allow_normals=False):
    if allow_normals:
        pts = np.array([[0., 0., 0.],
                        [0., 0., 0.],
                        [0., 0., 0.],
                        [0., 0., 1.],
                        [0., 0., 1.],
                        [0., 0., 1.],
                        [0., 1., 0.],
                        [0., 1., 0.],
                        [0., 1., 0.],
                        [0., 1., 1.],
                        [0., 1., 1.],
                        [0., 1., 1.],
                        [1., 0., 0.],
                        [1., 0., 0.],
                        [1., 0., 0.],
                        [1., 0., 1.],
                        [1., 0., 1.],
                        [1., 0., 1.],
                        [1., 1., 0.],
                        [1., 1., 0.],
                        [1., 1., 0.],
                        [1., 1., 1.],
                        [1., 1., 1.],
                        [1., 1., 1.]])
    else:
        pts = np.array([[0., 0., 0.],
                        [0., 0., 1.],
                        [0., 1., 0.],
                        [0., 1., 1.],
                        [1., 0., 0.],
                        [1., 0., 1.],
                        [1., 1., 0.],
                        [1., 1., 1.]])
    if return_faces:
        if allow_normals:
            faces = np.array([[9,  6,   0],
                              [3,  9,   0],
                              [12, 18, 21],
                              [12, 21, 15],
                              [1,  13, 16],
                              [1,  16,  4],
                              [22, 19,  7],
                              [10, 22,  7],
                              [20, 14,  2],
                              [8,  20,  2],
                              [5,  17, 23],
                              [5,  23, 11]])
        else:
            faces = np.array([[3, 2, 0],
                              [1, 3, 0],
                              [4, 6, 7],
                              [4, 7, 5],
                              [0, 4, 5],
                              [0, 5, 1],
                              [7, 6, 2],
                              [3, 7, 2],
                              [6, 4, 0],
                              [2, 6, 0],
                              [1, 5, 7],
                              [1, 7, 3]])
        return pts, faces
    return pts


def orient_mesh_faces_outward(verts, faces, reference):
    """Flip face winding so normals point away from `reference` (a point or per-face array)."""
    tri = verts[faces]
    normals = vec_crosses(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    centroids = tri.mean(axis=1)
    outward = centroids - np.asarray(reference)
    flip = vec_dots(normals, outward) < 0
    faces = faces.copy()
    faces[flip] = faces[flip][:, (0, 2, 1)]
    return faces

def estimate_mesh_vertex_curvatures(verts, inds, vertex_normals=None, method=None, rings=2):
    """
    **LLM Docstring**

    Per-vertex mean and Gaussian curvature estimated from a triangle mesh.

    `'quadric'` (default): at each vertex, least-squares fit of the height
    `w = a u^2 + b u v + c v^2 + d u + e v` of its `rings`-ring neighbours
    over the tangent plane of the vertex normal, and the curvatures of that
    graph at the vertex. Insensitive to triangle shape, so it stays
    accurate on isosurface meshes (irregular, with occasional slivers);
    converges as `O(h^2)` on smooth surfaces. Vertices with fewer than
    five neighbours fall back to `'cotangent'`.

    `'cotangent'`: the discrete operators of Meyer, Desbrun, Schroeder &
    Barr (2003), see `cotangent_vertex_curvatures`; exact Gauss-Bonnet in
    aggregate, but individual vertices are noisy on irregular meshes.

    The sign of the mean curvature follows the vertex normals (given, or
    area-weighted face normals from the triangle winding), so it is
    positive on convex parts of an outward-oriented mesh.

    :param verts: the vertices, shape `(n, 3)`
    :param inds: the triangles, shape `(t, 3)`
    :param vertex_normals: optional per-vertex normals
    :param method: `'quadric'` or `'cotangent'`
    :param rings: neighbourhood size for the quadric fit
    :return: `(mean, gaussian)`
    :rtype: tuple
    """
    verts, inds = mesh_arrays(verts, inds)
    if method is None:
        method = 'quadric'
    if method == 'cotangent':
        return cotangent_mesh_vertex_curvatures(verts, inds, vertex_normals=vertex_normals)
    elif method != 'quadric':
        raise ValueError(f"unknown curvature estimator '{method}'")
    verts = np.asanyarray(verts, dtype=float)
    inds = np.asanyarray(inds, dtype=int)
    n = len(verts)
    e = np.concatenate([inds[:, [0, 1]], inds[:, [1, 2]], inds[:, [2, 0]]])
    A = scipy.sparse.coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n, n)).tocsr()
    A = ((A + A.T) > 0).astype(np.int8)
    N = A.copy()
    for _ in range(rings - 1):
        N = ((N + N @ A) > 0).astype(np.int8)
    N = N.tolil()
    N.setdiag(0)
    N = N.tocsr()
    N.eliminate_zeros()
    vn = mesh_vertex_normals(verts, inds, vertex_normals)
    ax = np.eye(3)[np.argmin(np.abs(vn), axis=1)]
    t1 = np.cross(vn, ax)
    t1 /= np.linalg.norm(t1, axis=1)[:, None]
    t2 = np.cross(vn, t1)
    mean = np.full(n, np.nan)
    gauss = np.full(n, np.nan)
    counts = np.diff(N.indptr)
    for c in np.unique(counts):
        if c < 5:
            continue
        rows = np.flatnonzero(counts == c)
        for start in range(0, len(rows), 20000):
            r = rows[start:start + 20000]
            nb = N.indices[N.indptr[r][:, None] + np.arange(c)[None, :]]
            d = verts[nb] - verts[r][:, None, :]
            u = np.einsum('mkx,mx->mk', d, t1[r])
            v = np.einsum('mkx,mx->mk', d, t2[r])
            w = np.einsum('mkx,mx->mk', d, vn[r])
            M = np.stack([u * u, u * v, v * v, u, v], -1)
            MtM = np.einsum('mki,mkj->mij', M, M)
            Mtw = np.einsum('mki,mk->mi', M, w)
            reg = 1e-14 * np.trace(MtM, axis1=1, axis2=2)[:, None, None] * np.eye(5)
            a, b, cc, dd, ee = np.linalg.solve(MtM + reg, Mtw[..., None])[..., 0].T
            g2 = 1 + dd * dd + ee * ee
            # the surface bends away from an outward normal on convex parts, hence the sign
            mean[r] = -((1 + ee * ee) * 2 * a - 2 * dd * ee * b + (1 + dd * dd) * 2 * cc) / (2 * g2 ** 1.5)
            gauss[r] = (4 * a * cc - b * b) / g2 ** 2
    bad = ~np.isfinite(mean) | ~np.isfinite(gauss)
    if bad.any():
        cm, cg = cotangent_mesh_vertex_curvatures(verts, inds, vertex_normals=vertex_normals)
        mean[bad], gauss[bad] = cm[bad], cg[bad]
    return mean, gauss


def cotangent_mesh_vertex_curvatures(verts, inds, vertex_normals=None):
    """
    **LLM Docstring**

    Discrete per-vertex mean and Gaussian curvature of a triangle mesh
    (Meyer et al. 2003): mixed Voronoi areas `A_i`,
    `K_i = (2 pi - sum of angles at i) / A_i` (`pi` instead of `2 pi` on
    boundary vertices), and `H_i = -(Delta x)_i . n_i / 2` with the
    cotangent Laplacian `Delta x`. The sign of `H` follows the vertex
    normals (given, or area-weighted face normals from the triangle
    winding), so it is positive on convex parts of an outward-oriented mesh.

    :param verts: the vertices, shape `(n, 3)`
    :param inds: the triangles, shape `(t, 3)`
    :param vertex_normals: optional per-vertex normals used for the sign of `H`
    :return: `(mean, gaussian)`
    :rtype: tuple
    """
    verts, inds = mesh_arrays(verts, inds)
    verts = np.asanyarray(verts, dtype=float)
    inds = np.asanyarray(inds, dtype=int)
    n = len(verts)
    P = verts[inds]                                        # (t, 3 corners, 3)
    # edge opposite corner k runs between the other two corners
    e = np.stack([P[:, 2] - P[:, 1], P[:, 0] - P[:, 2], P[:, 1] - P[:, 0]], axis=1)
    l2 = np.einsum('tkx,tkx->tk', e, e)
    cr = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0])
    dbl = np.linalg.norm(cr, axis=-1)                      # twice the triangle area
    # interior angle and cotangent at each corner
    a_vec = [(P[:, (k + 1) % 3] - P[:, k], P[:, (k + 2) % 3] - P[:, k]) for k in range(3)]
    dots = np.stack([np.einsum('tx,tx->t', u, v) for u, v in a_vec], axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        cot = dots / dbl[:, None]
        ang = np.arctan2(dbl[:, None], dots)
    cot = np.nan_to_num(cot)
    # mixed Voronoi areas
    area = dbl / 2
    vor = np.stack([
        (l2[:, (k + 1) % 3] * cot[:, (k + 1) % 3] + l2[:, (k + 2) % 3] * cot[:, (k + 2) % 3]) / 8
        for k in range(3)
    ], axis=1)
    obtuse = ang > np.pi / 2
    any_obtuse = obtuse.any(axis=1)
    mixed = np.where(any_obtuse[:, None], np.where(obtuse, area[:, None] / 2, area[:, None] / 4), vor)
    A = np.zeros(n)
    np.add.at(A, inds.ravel(), mixed.ravel())
    # angle deficit (boundary vertices: pi)
    angsum = np.zeros(n)
    np.add.at(angsum, inds.ravel(), np.nan_to_num(ang).ravel())
    edges = np.sort(np.concatenate([inds[:, [0, 1]], inds[:, [1, 2]], inds[:, [2, 0]]]), axis=1)
    ue, cnt = np.unique(edges, axis=0, return_counts=True)
    boundary = np.zeros(n, dtype=bool)
    boundary[ue[cnt == 1].ravel()] = True
    full = np.where(boundary, np.pi, 2 * np.pi)
    # cotangent Laplacian: sum over the edges (i, j) of (cot a + cot b)(x_j - x_i) / (2 A_i)
    lap = np.zeros((n, 3))
    for k in range(3):
        i, j = inds[:, (k + 1) % 3], inds[:, (k + 2) % 3]   # the edge opposite corner k
        w = cot[:, k][:, None] * (verts[j] - verts[i])
        np.add.at(lap, i, w)
        np.add.at(lap, j, -w)
    vn = mesh_vertex_normals(verts, inds, vertex_normals)
    with np.errstate(invalid='ignore', divide='ignore'):
        lap = lap / (2 * A)[:, None]
        mean = -0.5 * np.einsum('ij,ij->i', lap, vn)
        gauss = (full - angsum) / A
    return mean, gauss


def mesh_normal_derivatives(verts, inds, order=1, *, cache=None):
    """
    **LLM Docstring**

    Compute the derivatives (up to `order`) of each triangle's normal with respect to
    its vertex coordinates.

    :param order: the derivative order
    :type order: int
    :return: the per-order normal-derivative tensors
    :rtype: list
    """
    verts, inds = mesh_arrays(verts, inds)
    if len(inds) == 0:
        expansion = [np.zeros((0,) + (3*len(verts),)*m + (3,)) for m in range(order+1)]
        return expansion
    i_list, j_list, k_list = inds.T
    terms = [
        _coords.normal_deriv(verts, i, j, k, order=order,
                          cache=cache) #TODO: handle the broadcasting properly in `normal_deriv`
        for i, j, k in zip(i_list, j_list, k_list)
    ]
    return [np.array(e) for e in zip(*terms)]


def mesh_area_derivatives(verts, inds, order=1, return_components=False, *, cache=None):
    """
    **LLM Docstring**

    Compute the derivatives (up to `order`) of each triangle's area with respect to
    its vertex coordinates, via the Heron expansion of its edge lengths.

    :param order: the derivative order
    :type order: int
    :param return_components: return the per-triangle derivatives rather than their sum
    :type return_components: bool
    :return: the per-order area-derivative tensors
    :rtype: list
    """
    verts, inds = mesh_arrays(verts, inds)
    if len(inds) == 0:
        expansion = [np.zeros((0,) + (3*len(verts),)*m + ()) for m in range(order+1)]
        return expansion if return_components else [value.sum(axis=0) for value in expansion]
    i_list, j_list, k_list = inds.T
    terms = []
    for i, j, k in zip(i_list, j_list, k_list):
        n_a = _coords.dist_deriv(verts, i, j, order=order, cache=cache)
        n_b = _coords.dist_deriv(verts, j, k, order=order, cache=cache)
        n_c = _coords.dist_deriv(verts, k, i, order=order, cache=cache)
        # no reason to handle a bunch of zeros
        subterms = [np.zeros_like(a) for a in n_a]

        # deriv contribs look like (n_verts*3, ...)
        # reshape each term and subsample only relevant portions
        indices = np.concatenate([np.arange(3) + 3*i, np.arange(3) + 3*j, np.arange(3) + 3*k], axis=0)
        n_a = [n[np.ix_(*[indices] * m)] if m > 0 else n for m,n in enumerate(n_a)]
        n_b = [n[np.ix_(*[indices] * m)] if m > 0 else n for m,n in enumerate(n_b)]
        n_c = [n[np.ix_(*[indices] * m)] if m > 0 else n for m,n in enumerate(n_c)]

        s = _td.scale_expansion(_td.add_expansions(n_a, n_b, n_c), 1/2)
        da, db, dc = (
                         _td.subtract_expansions(s, n_a),
                         _td.subtract_expansions(s, n_b),
                         _td.subtract_expansions(s, n_c)
        )
        tri_term = _td.scalarprod_deriv(
            _td.scalarprod_deriv(
                _td.scalarprod_deriv(s, da, order),
                db, order
            ),
            dc, order
        )
        tris = _td.scalarpow_deriv(tri_term, 1/2, order)

        subterms[0] = tris[0]
        for m,(t,s) in enumerate(zip(subterms, tris)):
            if m == 0:
                continue
            else:
                t[np.ix_(*[indices] * m)] = s
        terms.append(subterms)

    tris = [np.array(e) for e in zip(*terms)]
    if return_components:
        return tris
    else:
        return [np.sum(t, axis=0) for t in tris]


def mesh_centroid_derivatives(verts, inds, order=1, return_components=False, *, cache=None):
    """
    **LLM Docstring**

    Compute the derivatives (up to `order`) of each triangle's centroid with respect
    to its vertex coordinates.

    :param order: the derivative order
    :type order: int
    :param return_components: accepted for interface parity
    :type return_components: bool
    :return: the per-order centroid-derivative tensors
    :rtype: list
    """
    verts, inds = mesh_arrays(verts, inds)
    i, j, k = inds.T
    # a scaled diagonal (3*n_verts, n_tris, 3)
    centroids = np.mean(verts[inds], axis=-2)
    expansion = [centroids]
    if order > 0:
        dx = np.zeros((len(i), 3*len(verts), 3))
        n = np.arange(len(i))
        for a in range(3):
            dx[n, i*3+a, a] = 1/3
            dx[n, j*3+a, a] = 1/3
            dx[n, k*3+a, a] = 1/3
        expansion.append(dx)
    for m in range(2, order+1):
        dx = np.zeros((len(i),) + (3*len(verts),) * m + (3,))
        expansion.append(dx)
    return expansion


def mesh_volume_derivatives(verts, inds, order=1, return_components=False,
                       normal_order=None,
                       area_order=None,
                       centroid_order=None, *, cache=None):
    """
    **LLM Docstring**

    Compute the derivatives (up to `order`) of the enclosed volume with respect to
    the vertex coordinates, combining the area, centroid, and normal derivatives via
    the divergence theorem.

    :param order: the derivative order
    :type order: int
    :param return_components: return the per-triangle derivatives rather than their sum
    :type return_components: bool
    :param normal_order: override the order for the normal derivatives
    :type normal_order: int | None
    :param area_order: override the order for the area derivatives
    :type area_order: int | None
    :param centroid_order: override the order for the centroid derivatives
    :type centroid_order: int | None
    :return: the per-order volume-derivative tensors
    :rtype: list
    """
    verts, inds = mesh_arrays(verts, inds)
    if len(inds) == 0:
        expansion = [np.zeros((0,) + (3*len(verts),)*m + ()) for m in range(order+1)]
        return expansion if return_components else [value.sum(axis=0) for value in expansion]
    # from ...Profilers import Timer
    # with Timer('normals'):
    nd = mesh_normal_derivatives(verts, inds, cache=cache, order=order if normal_order is None else normal_order)
    # with Timer('areas'):
    ad = mesh_area_derivatives(verts, inds, cache=cache, order=order if area_order is None else area_order, return_components=True)
    # with Timer('centroid'):
    cd = mesh_centroid_derivatives(verts, inds, cache=cache, order=order if centroid_order is None else centroid_order)

    # with Timer('mult'):
    #TODO: subsample this so only relevant tris are manipulated at once
    terms = _td.scale_expansion(
        _td.scalarprod_deriv(ad,
                              _td.tensordot_deriv(cd, nd, order=order, axes=[-1, -1], shared=1),
                              order=order),
        1/3
    )

    if return_components:
        return terms
    else:
        total = [np.sum(t, axis=0) for t in terms]
        sign = 1 if total[0] >= 0 else -1
        return [sign*t for t in total]


def align_mesh_boundary_loops(verts, A, B):
    """
    Find the best starting offset and traversal direction for loop `B` so
    that walking it lines up with walking loop `A`, using a short
    lookahead to score both candidate directions. Two loops bounding the
    same seam are typically traced in opposite directions (each patch's
    boundary is oriented outward via its own triangles), so this often
    picks the reversed direction -- that's expected, not a bug.
    """
    pa = verts[A]
    best = None
    for reverse in (False, True):
        Bc = B[::-1] if reverse else B
        pb = verts[Bc]
        tree = scipy.spatial.cKDTree(pb)
        _, idx0 = tree.query(pa[0])
        look = min(5, len(A) - 1, len(Bc) - 1)
        cost = 0.0
        for k in range(1, look + 1):
            cost += np.linalg.norm(pa[k % len(A)] - pb[(idx0 + k) % len(Bc)])
        if best is None or cost < best[0]:
            best = (cost, Bc, idx0)

    _, Bc, idx0 = best
    Bc = np.roll(Bc, -idx0)
    return A, Bc


def zipper_mesh_boundary_loops(verts, A, B):
    """
    Bridge two aligned, closed vertex loops with a ring of nA + nB
    triangles, at each step advancing whichever loop yields the shorter
    connecting edge. Standard "loft between two curves" construction, used
    here as a closed ring instead of an open strip.
    """
    nA, nB = len(A), len(B)
    i = j = 0
    tris = []
    while i < nA or j < nB:
        a_cur, a_next = A[i % nA], A[(i + 1) % nA]
        b_cur, b_next = B[j % nB], B[(j + 1) % nB]
        if j >= nB:
            tris.append((a_cur, a_next, b_cur))
            i += 1
        elif i >= nA:
            tris.append((a_cur, b_cur, b_next))
            j += 1
        else:
            d1 = np.linalg.norm(verts[a_next] - verts[b_cur])
            d2 = np.linalg.norm(verts[a_cur] - verts[b_next])
            if d1 <= d2:
                tris.append((a_cur, a_next, b_cur))
                i += 1
            else:
                tris.append((a_cur, b_cur, b_next))
                j += 1
    return tris


def stitch_mesh_boundary_loops(verts, loopA, loopB):
    """
    **LLM Docstring**

    Stitch two boundary loops together with a ring of triangles, after aligning and
    orienting them.

    :param verts: the mesh vertices
    :type verts: np.ndarray
    :param loopA: the first boundary loop (vertex indices)
    :type loopA: np.ndarray
    :param loopB: the second boundary loop
    :type loopB: np.ndarray
    :return: the new bridging triangles
    :rtype: list
    """
    A = np.asarray(loopA[:-1])
    B = np.asarray(loopB[:-1])
    A, B = align_mesh_boundary_loops(verts, A, B)
    return zipper_mesh_boundary_loops(verts, A, B)

__all__ += ['polygon_normal', 'winding_sign', 'winding_number', 'point_in_triangle', 'is_polygon_ear', 'ear_clipping_triangulation', 'triangulate_polygon', 'tri_tri_intersect', 'triangle_plane_embedding', 'check_triangle_plane_offsets', 'check_coplanar_triangle_intersection', 'get_bounding_boxes', 'check_interval_overlaps', 'check_bbox_intersections', 'check_line_intersection', 'check_segment_intersection', 'check_segment_intersection_2d', 'check_triangle_intersection', 'fibonacci_sphere', 'uv_mapping', 'uv_sphere', 'uv_cylinder', 'uv_cone', 'uv_box', 'orient_mesh_faces_outward', 'align_mesh_boundary_loops', 'zipper_mesh_boundary_loops', 'stitch_mesh_boundary_loops']
__all__ += ['estimate_mesh_vertex_curvatures', 'cotangent_mesh_vertex_curvatures', 'mesh_normal_derivatives', 'mesh_area_derivatives', 'mesh_centroid_derivatives', 'mesh_volume_derivatives']
