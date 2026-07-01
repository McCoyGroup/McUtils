import collections
import itertools

import numpy as np
import scipy.spatial
import scipy.spatial as spat
import scipy.sparse
from ... import Devutils as dev
from ... import Numputils as nput
from ...Data import AtomData, UnitsData
from ...ExternalPrograms import Open3DInterface as o3d

__all__ = [
    "SphereUnionSurface",
    "SphereUnionSurfaceMesh"
]

# class TriangleMesh:
#
#     ...

class SphereUnionSurface:

    default_samples = 50
    default_scaling = 1
    default_expansion = 0
    default_tolerance = 1e-3
    def __init__(self, centers, radii, scaling=None, expansion=None,
                 samples=None,
                 density=None,
                 tolerance=None,
                 add_intersection_circles=False,
                 **generator_options):
        self.centers = np.asanyarray(centers)
        self.radii = np.asanyarray(radii)
        if samples is None:
            samples = self.default_samples
        self.samples = samples
        self.density = density
        self.add_intersection_circles = add_intersection_circles
        if scaling is None:
            scaling = self.default_scaling
        self.scaling = scaling
        if expansion is None:
            expansion = self.default_expansion
        if tolerance is None:
            tolerance = self.default_tolerance
        self.tolerance = tolerance
        self.expansion = expansion
        self._sample_points = None
        self._sample_data = None
        self.generator_options = generator_options

    @classmethod
    def from_xyz(cls,
                 atoms, positions,
                 scaling=None, expansion=None, samples=None,
                 tolerance=None,
                 radius_property='IconRadius',
                 distance_units='BohrRadius'):
        radii = np.array([
            AtomData[a, radius_property] * UnitsData.convert("Angstroms", distance_units)
            for a in atoms
        ])

        return cls(positions, radii,
                   samples=samples, scaling=scaling, expansion=expansion,
                   tolerance=tolerance
                   )

    @property
    def sampling_points(self):
        if self._sample_points is None:
            self._sample_data = self.generate_points(preserve_origins=True, **self.generator_options)
            self._sample_points = np.concatenate(self._sample_data, axis=0)
        return self._sample_points
    @sampling_points.setter
    def sampling_points(self, pts):
        if pts is not None: pts = np.asanyarray(pts)
        self._sample_points = pts
    @property
    def atom_sampling_points(self):
        if self._sample_data is None:
            self._sample_data = self.generate_points(preserve_origins=True, **self.generator_options)
            self._sample_points = np.concatenate(self._sample_data, axis=0)
        return self._sample_data

    @classmethod
    def nearest_centers(cls, pts, centers, return_normals=False):
        center_vecs = pts[:, np.newaxis, :] - centers[np.newaxis, :, :]
        center_dm = np.linalg.norm(center_vecs, axis=-1)
        np.fill_diagonal(center_dm, 1e6)
        nearest_centers = np.argmin(center_dm, axis=1)
        if return_normals:
            norms = center_dm[np.arange(len(pts)), nearest_centers]
            return nearest_centers, (norms, center_vecs[np.arange(len(pts)), nearest_centers, :] / norms[:, np.newaxis])
        return nearest_centers

    @classmethod
    def sphere_project(cls, pts, centers, radii):
        center_vecs = pts[:, np.newaxis, :] - centers[np.newaxis, :, :]
        center_dm = np.linalg.norm(center_vecs, axis=-1)
        np.fill_diagonal(center_dm, 1e6)
        nearest_centers = np.argmin(center_dm, axis=1)
        sel = (np.arange(len(pts)), nearest_centers)
        scaling = radii[nearest_centers] / center_dm[sel]
        pts = centers[nearest_centers, :] + center_vecs[sel] * scaling[:, np.newaxis]

        return pts

    @classmethod
    def sphere_boundary_pruning(
            cls,
            pts,
            centers,
            # radii,
            min_component=None,
            # max_iterations=15
    ):
        center_vecs = pts[:, np.newaxis, :] - centers[np.newaxis, :, :]
        center_dm = np.linalg.norm(center_vecs, axis=-1)
        np.fill_diagonal(center_dm, 1e6)
        nearest_centers = np.argmin(center_dm, axis=1)

        center_inds, subgroups = nput.group_by(pts, nearest_centers)[0]
        subgroups = list(subgroups)
        if min_component is None:
            primary_comps = []
            for group in subgroups:
                dm = nput.distance_matrix(group)
                np.fill_diagonal(dm, 1e6)
                min_vals = np.min(dm, axis=1)
                vals, bins = np.histogram(min_vals, bins=len(group)//5)
                i = np.argmax(vals)
                primary_comps.append(
                    (bins[i] + bins[i + 1]) / 2
                )
            min_component = np.min(primary_comps) #* .5
        for n,(c, group) in enumerate(zip(center_inds, subgroups)):
            dm = nput.distance_matrix(group)
            np.fill_diagonal(dm, 1e6)
            min_vals = np.min(dm, axis=1)
            print("!", np.sort(min_vals))
            for m,(k, group2) in enumerate(zip(center_inds[n+1:], subgroups[n+1:])):
                dists = np.linalg.norm(group2[:, np.newaxis, :] - group[np.newaxis, :, :], axis=-1)
                dist_cutoff = np.where(np.min(dists, axis=1) < min_component)
                if len(dist_cutoff) > 0 or len(dist_cutoff[0]) > 0:
                    subgroups[n+1+m] = np.delete(group2, dist_cutoff[0], axis=0)

        return np.concatenate(subgroups, axis=0)

    @classmethod
    def point_cloud_repulsion(
            cls,
            pts,
            centers,
            radii,
            min_displacement_cutoff=1e-3,
            stochastic_factor=.0001,
            force_constant=.001,
            power=-3,
            max_iterations=15
    ):
        rows, cols = np.triu_indices(len(pts), k=1)
        n = len(pts)
        for i in range(max_iterations):
            d_vecs = pts[rows, :] - pts[cols, :]
            norms = np.linalg.norm(d_vecs, axis=-1)
            forces = force_constant * np.power(norms, power)
            if np.all(forces < min_displacement_cutoff): break
            force_vecs = d_vecs * forces[:, np.newaxis]
            d_mat = np.zeros((n, n, 3))
            d_mat[rows, cols] = force_vecs
            d_mat[cols, rows] = force_vecs
            disps = np.sum(d_mat, axis=1)

            disps = disps + stochastic_factor * nput.vec_normalize(np.random.normal(size=disps.shape))

            center_vecs = pts[:, np.newaxis, :] - centers[np.newaxis, :, :]
            center_dm = np.linalg.norm(center_vecs, axis=-1)
            np.fill_diagonal(center_dm, 1e6)
            nearest_centers = np.argmin(center_dm, axis=1)
            sel = (np.arange(len(pts)), nearest_centers)
            proj_vecs = (center_vecs[sel] / center_dm[sel][:, np.newaxis])
            eye = nput.identity_tensors((len(pts),), 3)
            proj = eye - proj_vecs[:, :, np.newaxis] * proj_vecs[:, np.newaxis, :]
            pts = pts + (proj @ disps[:, :, np.newaxis]).reshape(disps.shape)

            pts = cls.sphere_project(pts, centers, radii)

        return pts

    @classmethod
    def adjust_point_cloud_density(self,
                                   pts,
                                   centers=None,
                                   radii=None,
                                   min_component=None,
                                   min_component_bins=30,
                                   min_component_scaling=.7,
                                   # max_component=None,
                                   same_point_cutoff=1e-6,
                                   max_iterations=15):
        if len(pts) == 1: return pts

        if centers is not None and radii is None or radii is not None and centers is None:
            raise ValueError("to constrain points, need both centers and radii")
        elif centers is not None:
            centers = np.asanyarray(centers)
            radii = np.asanyarray(radii)

        if max_iterations > 0:
            dm = nput.distance_matrix(pts)
            # rows, cols = np.triu_indices_from(dm, k=1)
            max_dist = np.max(dm) * 100
            np.fill_diagonal(dm, max_dist)
            min_pos = np.argmin(dm, axis=1)
            min_vals = dm[np.arange(len(dm)), min_pos]
            if min_component is None:
                vals, bins = np.histogram(min_vals, bins=min_component_bins)
                i = np.argmax(vals)
                min_component = min_component_scaling * (bins[i] + bins[i+1]) / 2

            for i in range(max_iterations):
                small_mask = min_vals < min_component
                bad_pos = np.where(small_mask)

                # if max_component is not None:
                #     big_mask = min_vals > max_component
                #     big_pos = np.where(big_mask)
                # else:
                #     big_mask = None
                #     big_pos = None

                small_done = len(bad_pos) == 0 or len(bad_pos[0]) == 0
                big_done = True
                # big_done = big_mask is None or (len(big_pos) == 0 or len(big_pos[0]) == 0 or len(pts) == 1)
                if (
                        len(pts) == 1
                        or (small_done and big_done)
                ):
                    break

                bad_vals = min_vals[bad_pos]
                dropped_points = np.where(bad_vals < same_point_cutoff)

                bad_rows = bad_pos[0]
                bad_cols = min_pos[bad_pos]
                _, r_pos = np.unique(bad_rows, return_index=True)
                _, c_pos = np.unique(bad_cols[r_pos], return_index=True)
                # only treat each point once per iteration by first dropping dupes
                # and then ensuring terms that appear in the rows don't appear in the cols
                bad_pos = bad_rows[r_pos[c_pos]]

                if len(dropped_points) > 0 and len(dropped_points[0]) > 0:
                    drop_rows = dropped_points[0]
                    drop_cols = min_pos[dropped_points]
                    drop_mask = drop_cols > drop_rows
                    # drop_rows = drop_rows[drop_mask]
                    drop_cols = drop_cols[drop_mask]
                    bad_pos = np.concatenate([drop_cols, bad_pos])

                bad_rows = bad_pos
                bad_cols = min_pos[bad_pos]

                merge_pos = np.unique(np.concatenate([bad_rows, bad_cols]))
                rem_pos = np.setdiff1d(np.arange(len(pts)), merge_pos)
                # dm = dm[np.ix_(rem_pos, rem_pos)]
                min_vals = min_vals[rem_pos,]
                inv_map = np.argsort(np.concatenate([rem_pos, merge_pos]))
                min_pos = inv_map[min_pos][rem_pos,]
                bad_mask = min_pos >= len(rem_pos)
                min_vals[bad_mask] = max_dist
                min_pos[bad_mask] = -1
                rem_pts = pts[rem_pos,]
                new_pts = (pts[bad_rows] + pts[bad_cols]) / 2 # average point positions

                if centers is not None and radii is not None:
                    d_vecs = new_pts[:, np.newaxis, :] - centers[np.newaxis, :, :]
                    center_dm = np.linalg.norm(d_vecs, axis=-1)
                    np.fill_diagonal(center_dm, max_dist)
                    nearest_centers = np.argmin(center_dm, axis=1)
                    sel = (np.arange(len(new_pts)), nearest_centers)
                    scaling = radii[nearest_centers] / center_dm[sel]
                    new_pts = centers[nearest_centers, :] + d_vecs[sel] * scaling[:, np.newaxis]
                # renormalize to distance to nearest center is unchanged


                if len(new_pts) > 1:
                    new_new_dists = nput.distance_matrix(new_pts)
                    np.fill_diagonal(new_new_dists, max_dist)
                    new_min_pos = np.argmin(new_new_dists, axis=1)
                    new_min_vals = new_new_dists[np.arange(len(new_new_dists)), new_min_pos]
                    dropped_points = np.where(new_min_vals < same_point_cutoff)
                    if len(dropped_points) > 0 and len(dropped_points[0]) > 0:
                        drop_rows = dropped_points[0]
                        drop_cols = new_min_pos[dropped_points]
                        drop_mask = drop_cols > drop_rows
                        # drop_rows = drop_rows[drop_mask]
                        drop_cols = drop_cols[drop_mask]
                        rem_new_pts = np.setdiff1d(np.arange(len(new_pts)), drop_cols)
                        new_pts = new_pts[rem_new_pts,]
                        new_min_vals = new_min_vals[rem_new_pts,]
                        new_min_pos = new_min_pos[rem_new_pts,]
                else:
                    new_min_vals = None
                    new_min_pos = None

                new_rem_dists = np.linalg.norm(rem_pts[:, np.newaxis, :] - new_pts[np.newaxis, :, :], axis=-1)
                new_rem_pos = np.argmin(new_rem_dists, axis=1)
                new_rem_mins = new_rem_dists[np.arange(len(new_rem_dists)), new_rem_pos]
                dropped_points = np.where(new_rem_mins < same_point_cutoff)
                if len(dropped_points) > 0 and len(dropped_points[0]) > 0:
                    drop_rows = dropped_points[0]
                    drop_cols = new_rem_pos[dropped_points]
                    drop_mask = drop_cols > drop_rows
                    # drop_rows = drop_rows[drop_mask]
                    drop_cols = drop_cols[drop_mask]
                    rem_new_pts = np.setdiff1d(np.arange(len(new_pts)), drop_cols)
                    new_pts = new_pts[rem_new_pts,]
                    new_min_vals = new_min_vals[rem_new_pts,]
                    new_rem_dists = np.linalg.norm(rem_pts[:, np.newaxis, :] - new_pts[np.newaxis, :, :], axis=-1)
                    new_rem_pos = np.argmin(new_rem_dists, axis=1)
                    new_rem_mins = new_rem_dists[np.arange(len(new_rem_dists)), new_rem_pos]

                min_mask = min_vals > new_rem_mins
                min_vals[min_mask] = new_rem_mins[min_mask]
                min_pos[min_mask] = new_rem_pos[min_mask]

                new_new_pos = np.argmin(new_rem_dists, axis=0)
                new_new_mins = new_rem_dists[new_new_pos, np.arange(new_rem_dists.shape[1])]
                if new_min_vals is None:
                    new_min_vals = new_new_mins
                    new_min_pos = new_new_pos
                else:
                    min_mask = new_min_vals > new_new_mins
                    new_min_vals[min_mask] = new_new_mins[min_mask]
                    new_min_pos[min_mask] = new_new_pos[min_mask]

                pts = np.concatenate([rem_pts, new_pts], axis=0)
                min_vals = np.concatenate([min_vals, new_min_vals])
                min_pos = np.concatenate([min_pos, new_min_pos])

        return pts

    @classmethod
    def get_exterior_points(cls, points, centers, radii, tolerance:float=0,
                            vertex_map=None,
                            intersection_point_mask=None,
                            intersection_point_tolerance=None,
                            return_components=False):
        points = np.asanyarray(points)
        centers = np.asanyarray(centers)
        radii = np.asanyarray(radii)

        dvs = np.linalg.norm(
            points[:, np.newaxis, :] - centers[np.newaxis, :, :],
            axis=-1
        )

        comps = dvs * (1+tolerance) >= radii[np.newaxis]
        if intersection_point_mask is not None and intersection_point_tolerance is not None:
            comps[intersection_point_mask,] = dvs[intersection_point_mask,] * (1 + intersection_point_tolerance) >= radii[np.newaxis]

        if vertex_map is not None:
            if vertex_map.ndim == 1:
                comps[np.arange(len(vertex_map)), vertex_map] = True
            else:
                for vm in np.moveaxis(vertex_map, -1, 0):
                    comps[np.arange(len(vertex_map)), vm] = True
        if return_components:
            return comps
        else:
            return np.all(comps, axis=1)

    @classmethod
    def get_interior_points(cls, points, centers, radii, tolerance: float = 0, return_components=False):
        points = np.asanyarray(points)
        centers = np.asanyarray(centers)
        radii = np.asanyarray(radii)

        dvs = np.linalg.norm(
            points[:, np.newaxis, :] - centers[np.newaxis, :, :],
            axis=-1
        )

        comps = dvs * (1 - tolerance) <= radii[np.newaxis]
        if return_components:
            return comps
        else:
            return np.any(comps, axis=1)

    @classmethod
    def get_surface_points(cls,
                           centers,
                           radii,
                           samples=50,
                           density=None,
                           scaling=1,
                           expansion=0,
                           preserve_origins=False,
                           circle_samples=None,
                           min_circle_samples=.1,
                           add_intersection_circles=False,
                           intersection_radius_scaling=1,
                           intersection_boundary_clipping_threshold=None,
                           return_intersection_point_mask=False,
                           extend_intersection_points=True,
                           intersection_point_tolerance=None,
                           clear_circle_neighbors=True,
                           neighborhood_tolerance='auto', # percentage of radius
                           tolerance=0,
                           prune=True
                           ):
        centers = np.asanyarray(centers)
        radii:np.array[float] = np.asanyarray(radii) * scaling + expansion

        if density is not None:
            areas = 4*np.pi*radii ** 2
            samples = np.ceil(density * areas).astype(int)
        base_points = cls.sphere_points(
            centers,
            radii,
            samples
        )
        if nput.is_int(samples):
            samples = [samples] * centers.shape[-1]

        base_point_masks = [
            np.full(b.shape[:-1], True)
            for b in base_points
        ]

        d_avgs = []
        for b in base_points:
            dms = nput.distance_matrix(b)
            np.fill_diagonal(dms, np.max(dms))
            d_avgs.append(np.average(np.min(dms, axis=0)))

        if add_intersection_circles:
            for i,j in itertools.combinations(range(len(centers)), 2):
                r_ij = np.linalg.norm(centers[i] - centers[j])
                if r_ij < (radii[i] + radii[j]):
                    circ = cls.sphere_double_intersection_circle(
                        [centers[i], centers[j]],
                        np.array([radii[i], radii[j]]),
                        dist=r_ij)

                    # project points onto the intersection circle, anything
                    # close to the boundary gets pushed onto the boundary
                    circ_pts = circ.center[np.newaxis] + circ.radius * nput.vec_normalize(
                        nput.project_out(base_points[i][:samples[i]] - circ.center[np.newaxis], circ.normal[:, np.newaxis])
                    )
                    circ_dists = nput.vec_norms(base_points[i][:samples[i]] - circ_pts)

                    # any point within tolerance gets pushed onto the intersection
                    thresh = intersection_boundary_clipping_threshold
                    if thresh is None:
                        thresh = neighborhood_tolerance
                    if dev.str_is(thresh, 'auto'):
                        thresh = {
                            'distance_scaling':1,
                            'radius_cutoff':.25,
                            'interior_padding':.25
                        }
                    if isinstance(thresh, dict):
                        sc = thresh.get('distance_scaling', 1)
                        isc = thresh.get('interior_padding', .25)
                        cutoff = thresh.get('radius_cutoff', .25)
                        thresh = np.clip(
                            d_avgs[i] * sc * (
                                1 + isc*(1 - cls.get_exterior_points(base_points[i][:samples[i]], centers, radii, tolerance=tolerance))
                            ),
                            0,
                            radii[i] * cutoff
                        )
                    else:
                        thresh = thresh * radii[i]
                    mask = circ_dists < thresh
                    # make sure points aren't now occluded
                    mask[mask] &= cls.get_exterior_points(circ_pts[mask], centers, radii, tolerance=tolerance)
                    idx = np.where(mask)
                    if len(idx[0]) > 0:
                        base_points[i][idx] = circ_pts[idx]

                    circ_pts = circ.center[np.newaxis] + circ.radius * nput.vec_normalize(
                        nput.project_out(base_points[j][:samples[j]] - circ.center[np.newaxis], circ.normal[:, np.newaxis])
                    )
                    circ_dists = nput.vec_norms(base_points[j][:samples[j]] - circ_pts)

                    # any point within tolerance gets pushed onto the intersection
                    thresh = intersection_boundary_clipping_threshold
                    if thresh is None:
                        thresh = neighborhood_tolerance
                    if dev.str_is(thresh, 'auto'):
                        thresh = {
                            'distance_scaling': 1,
                            'radius_cutoff': .25,
                            'interior_padding': .25
                        }
                    if isinstance(thresh, dict):
                        sc = thresh.get('distance_scaling', 1)
                        isc = thresh.get('interior_padding', .25)
                        cutoff = thresh.get('radius_cutoff', .25)
                        thresh = np.clip(
                            d_avgs[j] * sc * (
                                    1 + isc * (1 - cls.get_exterior_points(base_points[j][:samples[j]], centers, radii,
                                                                           tolerance=tolerance))
                            ),
                            0,
                            radii[j] * cutoff
                        )
                    else:
                        thresh = thresh * radii[j]
                    mask = circ_dists < thresh
                    mask[mask] &= cls.get_exterior_points(circ_pts[mask], centers, radii, tolerance=tolerance)
                    idx = np.where(mask)
                    if len(idx[0]) > 0:
                        base_points[j][idx] = circ_pts[idx]

                    if extend_intersection_points:

                        samps = circle_samples
                        if samps is None:
                            if min_circle_samples < 1:
                                min_circle_samples = int(samples * min_circle_samples)
                            dtot = 2 * np.pi * circ.radius
                            davg = d_avgs[i]
                            targ = 1 + 2 * (dtot // davg)
                            samps = int(max([targ, min_circle_samples]))
                        thetas = np.linspace(0, 2 * np.pi, samps + 1)[:-1]
                        base_circ = np.moveaxis(
                            np.array([np.cos(thetas), np.sin(thetas), np.zeros(thetas.shape)]),
                            0, -1
                        ) * circ.radius * intersection_radius_scaling

                        pts = base_circ @ nput.rotation_matrix([0, 0, 1], circ.normal) + circ.center[np.newaxis]
                        mask = cls.get_exterior_points(pts, centers, radii, tolerance=tolerance+1e-3)
                        if not np.any(mask): continue
                        pts = pts[mask,]
                        # if clear_circle_neighbors:
                        #     if len(base_points[i]) > samps:
                        #         circ_dists = np.linalg.norm(pts[:, np.newaxis, :] - base_points[i][samps:][np.newaxis, :, :], axis=-1)
                        #         nt = neighborhood_tolerance * radii[i]
                        #         mask = np.all(circ_dists >= nt, axis=-1)
                        #         pts = pts[mask,]
                        #
                        #     if len(base_points[j]) > samps:
                        #         circ_dists = np.linalg.norm(pts[:, np.newaxis, :] - base_points[j][samps:][np.newaxis, :, :], axis=-1)
                        #         nt = neighborhood_tolerance * radii[j]
                        #         mask = np.all(circ_dists >= nt, axis=-1)
                        #         pts = pts[mask,]

                        if not isinstance(base_points, list):
                            base_points = list(base_points)
                        base_points[i] = np.concatenate([base_points[i], pts], axis=0)
                        if clear_circle_neighbors:
                            circ_dists = np.linalg.norm(base_points[i][:samples[i]][:, np.newaxis, :] - pts[np.newaxis, :, :], axis=-1)
                            nt = neighborhood_tolerance
                            if dev.str_is(nt, 'auto'):
                                nt = {
                                    'distance_scaling': 1,
                                    'radius_cutoff': .25,
                                    'interior_padding': .25
                                }
                            if isinstance(nt, dict):
                                nt = d_avgs[i] * nt.get('radius_cutoff', .25)
                            else:
                                nt = nt * radii[i]
                            base_point_masks[i] &= np.all(circ_dists >= nt, axis=-1)

                            circ_dists = np.linalg.norm(base_points[j][:samples[j]][:, np.newaxis, :] - pts[np.newaxis, :, :], axis=-1)
                            nt = neighborhood_tolerance
                            if dev.str_is(nt, 'auto'):
                                nt = {
                                    'distance_scaling': 1,
                                    'radius_cutoff': .25,
                                    'interior_padding': .25
                                }
                            if isinstance(nt, dict):
                                nt = d_avgs[j] * nt.get('radius_cutoff', .25)
                            else:
                                nt = nt * radii[j]
                            base_point_masks[j] &= np.all(circ_dists >= nt, axis=-1)

                        if preserve_origins:
                            base_points[j] = np.concatenate([base_points[j], pts], axis=0)

        if add_intersection_circles and extend_intersection_points:
            intsection_point_masks = []
            _ = []
            for bm,pt in zip(base_point_masks,base_points):
                ip_mask = np.full(len(bm), False)
                if len(bm) < len(pt):
                    submask = np.full(len(pt) - len(bm), True)
                    ip_mask = np.concatenate([ip_mask, submask], axis=0)
                    bm = np.concatenate([bm, submask], axis=0)
                    pt = pt[bm]
                    ip_mask = ip_mask[bm]
                    intsection_point_masks.append(ip_mask)
                else:
                    pt = pt[bm]
                _.append(pt)
            base_points = _
        else:
            intsection_point_masks = None

        if prune:
            if not preserve_origins:
                base_points = np.concatenate(base_points, axis=0)
                if intsection_point_masks is not None:
                    intsection_point_masks = np.concatenate(intsection_point_masks, axis=0)
                else:
                    intsection_point_masks = None
                mask = cls.get_exterior_points(base_points, centers, radii,
                                               intersection_point_mask=intsection_point_masks,
                                               intersection_point_tolerance=intersection_point_tolerance,
                                               tolerance=tolerance)

                if return_intersection_point_mask:
                    return base_points[mask,], intsection_point_masks[mask,]
                else:
                    return base_points[mask,]
            else:
                subpoints = []
                ip_masks = []
                if intsection_point_masks is None:
                    intsection_point_masks = [None] * len(base_points)
                for bp,ipm in zip(base_points, intsection_point_masks):
                    mask = cls.get_exterior_points(bp, centers, radii,
                                                   intersection_point_mask=ipm,
                                                   intersection_point_tolerance=intersection_point_tolerance,
                                                   tolerance=tolerance)
                    subpoints.append(bp[mask,])
                    if ipm is not None:
                        ip_masks.append(ipm[mask,])
                if len(ip_masks) == 0:
                    ip_masks = None

                if return_intersection_point_mask:
                    return subpoints, ip_masks
                else:
                    return subpoints
        else:
            if not preserve_origins:
                if return_intersection_point_mask:
                    if intsection_point_masks is not None:
                        intsection_point_masks = np.concatenate(intsection_point_masks, axis=0)
                    return np.concatenate(base_points, axis=0), intsection_point_masks
                else:
                    return np.concatenate(base_points, axis=0)
            else:
                if return_intersection_point_mask:
                    return base_points, intsection_point_masks
                else:
                    return base_points

    def generate_points(self, scaling=None, expansion=None,
                        samples=None,
                        density=None,
                        preserve_origins=False, tolerance=None, prune=True,
                        add_intersection_circles=None, **etc
                        ):
        if samples is None: samples = self.samples
        if density is None: density = self.density
        if scaling is None: scaling = self.scaling
        if expansion is None: expansion = self.expansion
        if tolerance is None: tolerance = self.tolerance
        if add_intersection_circles is None: add_intersection_circles = self.add_intersection_circles

        return self.get_surface_points(
            self.centers,
            self.radii,
            scaling=scaling,
            expansion=expansion,
            samples=samples,
            density=density,
            preserve_origins=preserve_origins,
            add_intersection_circles=add_intersection_circles,
            tolerance=tolerance,
            prune=prune,
            **etc
        )


    def generate_mesh(self,
                      points=None,
                      normals=None,
                      scaling=None, expansion=None, samples=None,
                      method='poisson',
                      depth=5,
                      **reconstruction_settings):

        if points is None:
            if scaling is None and expansion is None and samples is None:
                points = self.sampling_points
            else:
                points = self.generate_points(scaling=scaling, expansion=expansion, samples=samples)
        if method == 'poisson':
            if normals is None:
                if isinstance(points, list):
                    normal_list = []
                    for c,p in zip(self.centers, points):
                        normal_list.append(nput.vec_normalize(p - c[np.newaxis]))
                    normals = np.concatenate(normal_list)
                else:
                    _, (_, normals) = self.nearest_centers(points, self.centers, return_normals=True)
            geom = o3d.submodule('geometry')
            pcd = geom.PointCloud()
            pcd.points = o3d.submodule('utility').Vector3dVector(np.asanyarray(points).view(np.ndarray))
            pcd.normals = o3d.submodule('utility').Vector3dVector(np.asanyarray(normals).view(np.ndarray))
            mesh, densities = geom.TriangleMesh.create_from_point_cloud_poisson(
                pcd,
                depth=depth,
                **reconstruction_settings
            )
        else:
            raise NotImplementedError("only Open3D Poisson currently supported")

        return SphereUnionSurfaceMesh.from_o3d(mesh, densities, surf=self)
        # return np.array(mesh.vertices), np.array(mesh.triangles)

    @classmethod
    def sphere_points(cls, centers, radii, samples, generator=None, shells=None):
        centers = np.asanyarray(centers)
        radii = np.asanyarray(radii)

        base_shape = centers.shape[:-2]
        centers = centers.reshape((-1,) + centers.shape[-2:])
        radii = radii.reshape(-1, radii.shape[-1])

        if generator is None:
            generator = cls.fibonacci_sphere
        if nput.is_int(samples):
            base_points = generator(samples)[np.newaxis, np.newaxis]
        else:
            samples = np.asanyarray(samples)
            if samples.ndim == 1:
                base_points = [
                    generator(n)
                    for n in samples
                ]
                if len(samples) == centers.shape[-2]:
                    base_points = [base_points] * centers.shape[0]
                else:
                    base_points = [bp[np.newaxis, :, :] for bp in base_points]
            else:
                samples = samples.reshape(-1, centers.shape[-2])
                base_points = [
                    [
                        generator(n)
                        for n in subsamp
                    ]
                    for subsamp in samples
                ]

        if shells is None:
            if isinstance(base_points, np.ndarray):
                sphere_points = centers[:, :, np.newaxis, :] + base_points * radii[:, :, np.newaxis, np.newaxis]
            else:
                sphere_points = []
                for cc,rr,pp in zip(centers, radii, base_points):
                    sp = [
                        c[np.newaxis, :] + p * r
                        for c,r,p in zip(cc, rr, pp)
                    ]
                    sphere_points.append(sp)
        else:
            if nput.is_int(shells):
                shells = np.linspace(0, 1, shells+1)[1:] ** (1/3) # uniformly w/in distributed in volume
            shells = np.asanyarray(shells)
            all_rads = radii[:, :, np.newaxis] * shells[np.newaxis, np.newaxis, :]
            sphere_points = centers[:, :, np.newaxis, np.newaxis, :] + base_points * all_rads[:, :, :, np.newaxis, np.newaxis]
            sphere_points = sphere_points.reshape(sphere_points.shape[:2] + (-1,) + sphere_points.shape[-1:])
        if isinstance(sphere_points, np.ndarray):
            return sphere_points.reshape(base_shape + sphere_points.shape[-3:])
        else:
            subarrays = np.full((len(sphere_points),), None, dtype=object)
            for i,s in enumerate(sphere_points):
                subarrays[i] = s
            subarrays = subarrays.reshape(base_shape)
            return subarrays.tolist()

    @classmethod
    def fibonacci_sphere(cls, samples):
        phi = np.pi * (np.sqrt(5.) - 1.)  # golden angle in radians
        samps = np.arange(samples)
        y = 1 - (samps / float(samples - 1)) * 2  # y goes from 1 to -1
        radius = np.sqrt(1 - y * y)  # radius at y
        theta = phi * samps  # golden angle increment
        x = np.cos(theta) * radius
        z = np.sin(theta) * radius

        return np.array([x, y, z]).T

    def get_bbox(self):
        return np.array([
            np.min(self.centers - self.radii[:, np.newaxis], axis=0),
            np.max(self.centers + self.radii[:, np.newaxis], axis=0)
            ])

    def ses_scalar_field(self, grid_pts, atomic_centers, radii, probe_radius):
        """
        For each grid point, compute the SES scalar field:
          f(x) = max_i( R_i - ||x - c_i|| ) + probe_radius
        The SES isosurface is f(x) = probe_radius,
        equivalently: max_i(radii_i - dist_i) = 0
        """
        inflated_R = radii + probe_radius
        diff = grid_pts[:, None, :] - atomic_centers[None, :, :]  # (G, n, 3)
        dist = np.linalg.norm(diff, axis=-1)  # (G, n)
        return (inflated_R[None, :] - dist).max(axis=1)  # (G,)

    def get_surface_function(self, probe_radius=None, distance_function=None):
        centers = np.asanyarray(self.centers)
        radii = np.asanyarray(self.radii)

        if distance_function is None:
            distance_function = lambda r: np.exp(-r)
        if probe_radius is None:
            probe_radius = 0
        def surface(points, probe_radius=probe_radius):
            points = np.asanyarray(points)
            base_shape = points.shape[:-1]
            points = points.reshape((-1,) + points.shape[-1:])
            dvs = np.linalg.norm(
                points[:, np.newaxis, :] - centers[np.newaxis, :, :],
                axis=-1
            ) - (radii[np.newaxis, :] + probe_radius)
            dists = np.min(dvs, axis=-1)
            return distance_function(dists).reshape(base_shape)
        return surface

    default_triangulation_method = 'hull-union'
    def get_triangulation(self,
                          occlusion_type='auto',
                          deduplicate_points=None,
                          point_gen_options=None,
                          add_intersection_circles=True,
                          extend_intersection_points=False,
                          method=None,
                          bbox_scaling=1.2,
                          grid_samples=20,
                          probe_radius=None,
                          **surface_opts):
        if method is None:
            method = self.default_triangulation_method
        if method == 'hull-union':
            if point_gen_options is None:
                point_gen_options = {'add_intersection_circles':add_intersection_circles}
            add_intersection_circles = point_gen_options.get('add_intersection_circles', add_intersection_circles)
            point_gen_options['add_intersection_circles'] = add_intersection_circles
            if dev.str_is(occlusion_type, 'auto'):
                occlusion_type = 'partial' if not add_intersection_circles else 'complete'
            if deduplicate_points is None:
                deduplicate_points = add_intersection_circles
            pts, masks = self.generate_points(preserve_origins=True, prune=False,
                                              return_intersection_point_mask=True,
                                              extend_intersection_points=extend_intersection_points,
                                              **point_gen_options)
            return SphereUnionSurfaceMesh.from_subclouds(
                pts,
                centers=self.centers,
                radii=self.radii,
                occlusion_type=occlusion_type,
                deduplicate_points=deduplicate_points,
                intersection_point_mask=masks,
                **surface_opts
            )
        elif method == 'isosurface':
            from .MarchingCubesSurface import marching_cubes
            surface_function = self.get_surface_function(probe_radius=probe_radius)
            bbox = self.get_bbox()
            if probe_radius is not None:
                bbox[0] -= probe_radius
                bbox[1] += probe_radius
            bbox = bbox * bbox_scaling
            if nput.is_int(grid_samples):
                grid_samples = [grid_samples] * 3
            meshes = np.meshgrid(*[np.linspace(bm, bM, s) for bm,bM,s in zip(*bbox, grid_samples)], indexing='ij')
            values = surface_function(np.moveaxis(meshes, 0, -1))
            def unembed_points(points):
                x,y,z = np.moveaxis(points, 0, -1)
                return np.moveaxis([
                                   nput.vec_rescale(x, [bbox[0][0], bbox[1][0]], [0, grid_samples[0]]),
                                   nput.vec_rescale(y, [bbox[0][1], bbox[1][1]], [0, grid_samples[1]]),
                                   nput.vec_rescale(z, [bbox[0][2], bbox[1][2]], [0, grid_samples[2]]),
                    ], 0, -1)
            return marching_cubes(values,
                                  1,
                                  transformation=unembed_points,
                                  **surface_opts)
        else:
            raise ValueError(f"unknown method {method}")

    @classmethod
    def sampling_point_surface_area(cls,
                                    centers,
                                    radii,
                                    points=None,
                                    exterior_test=None,
                                    point_generator=None,
                                    generator_args=None,
                                    center_surface_areas=None,
                                    **test_args
                                    ):
        if points is None:
            if generator_args is None:
                generator_args = {}
            if point_generator is None:
                point_generator = cls.sphere_points
            points = point_generator(
                centers,
                radii,
                **generator_args
            )
        if exterior_test is None:
            exterior_test = cls.get_exterior_points

        if center_surface_areas is None:
            center_surface_areas = 4 * np.pi * radii**2

        a = 0
        for ca, center_points in zip(center_surface_areas, points):
            mask = exterior_test(center_points, centers, radii, **test_args)
            a += ca * np.sum(mask).astype(int) / len(mask)

        return a

    @classmethod
    def _monte_carlo_volume(cls, points, centers, radii, interior_test=None, center_volumes=None, **test_args):
        if interior_test is None:
            interior_test = cls.get_interior_points

        v = 0
        if center_volumes is None:
            center_volumes = 4/3 * np.pi * radii ** 3
        for cv, points in zip(center_volumes, points):
            mask = interior_test(points, centers, radii, return_components=True, **test_args)
            mask_sums = np.sum(mask, axis=1)
            perc_inc = np.average(1 / mask_sums)
            v += perc_inc * cv
        return v

    @classmethod
    def sampling_point_volume(cls,
                              centers,
                              radii,
                              points=None,
                              interior_test=None,
                              point_generator=None,
                              generator_args=None,
                              center_volumes=None,
                              shells=50,
                              **test_args
                              ):
        if points is None:
            if generator_args is None:
                generator_args = {}
            if point_generator is None:
                point_generator = cls.sphere_points
            points = point_generator(
                centers,
                radii,
                shells=shells,
                **generator_args
            )
        if interior_test is None:
            interior_test = cls.get_interior_points

        if center_volumes is None:
            center_volumes = 4/3 * np.pi * radii ** 3

        return cls._monte_carlo_volume(points, centers, radii,
                                       interior_test=interior_test, center_volumes=center_volumes, **test_args)

    @classmethod
    def random_sphere_sampling(cls, center, radius, samples=500, seed=None, rng=None):
        if rng is None:
            if seed is not None:
                rng = np.random.default_rng(seed)
            else:
                rng = np.random
        subrads = (rng.uniform(0, 1, size=samples) ** (1/3)) * radius
        vecs = nput.vec_normalize(rng.normal(size=(samples, 3)))
        return vecs * subrads[:, np.newaxis] + center[np.newaxis, :]

    @classmethod
    def volume_union_mc(cls, centers, radii, n_samples=100000, seed=None):
        centers = np.asanyarray(centers, dtype=float)
        radii = np.asanyarray(radii, dtype=float)
        if seed is not None:
            rng = np.random.default_rng(seed)
        else:
            rng = None

        points = [
            cls.random_sphere_sampling(c, r, n_samples, rng=rng)
            for c, r in zip(centers, radii)
        ]
        return cls._monte_carlo_volume(points, centers, radii)

    @classmethod
    def volume_voxel(cls, centers, radii, resolution=200):
        lo = (centers - radii[:, None]).min(axis=0)
        hi = (centers + radii[:, None]).max(axis=0)

        # Build grid
        axes = [np.linspace(lo[k], hi[k], resolution) for k in range(3)]
        gx, gy, gz = np.meshgrid(*axes, indexing='ij')
        grid = np.stack([gx, gy, gz], axis=-1)  # (R, R, R, 3)

        inside = np.zeros(grid.shape[:3], dtype=bool)
        for c, r in zip(centers, radii):
            dist2 = ((grid - c) ** 2).sum(axis=-1)
            inside |= dist2 <= r ** 2

        voxel_vol = np.prod((hi - lo) / (resolution - 1))
        return np.sum(inside) * voxel_vol

    @classmethod
    def _trip_q(self, a, b, c, alpha, beta, gamma, e):
        return a * (
            b**2 + c**2 - a**2
            + beta**2 + gamma**2 - 2*alpha**2
            + e*(b**2 - c**2)
        )
    @classmethod
    def _trip_e(self, a, r2, r3):
        return (r2**2 - r3**2) / a**2
    @classmethod
    def _trip_w(self, a, b, c, alpha, beta, gamma):
        A = alpha**2
        B = beta**2
        C = gamma**2
        a = a**2
        b = b**2
        c = c**2
        d = np.linalg.det([
            [0, 1, 1, 1, 1],
            [1, 0, C, B, A],
            [1, C, 0, a, b],
            [1, B, a, 0, c],
            [1, A, b, c, 0],
        ])
        if d > 0:
            return np.sqrt(1 / 2 * d)
        else:
            return d
    @classmethod
    def _trip_s(self, beta, a, c, q1, q3, e1, e3, w):
        ae = a*(1+e1)
        ce = c*(1-e3)
        t1 = np.arctan(ae*w / (beta*q1) )
        t2 = np.arctan(ce*w / (beta*q3) )
        t3 = np.arctan(2*w / q1)
        t4 = np.arctan(2*w / q3)
        s1 = t1 + t2
        if s1 < 0:
            s1 = np.pi + s1
        elif s1 > np.pi:
            s1 = s1 - np.pi
        if t3 < 0:
            t3 = np.pi + t3
        elif t3 > np.pi:
            t3 = t3 - np.pi
        if t4 < 0:
            t4 = np.pi + t4
        elif t4 > np.pi:
            t4 = t4 - np.pi
        return 2*(beta**2) * s1 - beta*(
            ae*t3
            + ce*t4
        )
    @classmethod
    def _trip_t(cls, a, b, c):
        return (a+b+c)*(-a + b + c)*(a-b+c)*(a+b-c)
    @classmethod
    def _trip_p(cls, a, b, c, r1, r2, r3, t):
        A = (b ** 2 - c ** 2 + r2 ** 2 - r3 ** 2) ** 2
        t_abg = np.sqrt(cls._trip_t(a, r2, r3))
        pp = (A + (t + t_abg) ** 2) / (4 * a ** 2) - r1 ** 2
        pm = (A + (t - t_abg) ** 2) / (4 * a ** 2) - r1 ** 2
        # if pp > 0 and pm < 0:
        #     raise ValueError("?", pp, pm)
        return pp, pm
    @classmethod
    def sphere_triple_intersection_area(cls, a, b, c, r1, r2, r3):
        # https://www.tandfonline.com/doi/pdf/10.1080/00268978800100453
        # https://www-tandfonline-com/doi/epdf/10.1080/00268978700102951
        w = cls._trip_w(a, b, c, r1, r2, r3)
        # if abs(w) < 1e-8:
        #     return 0
        if w < -1e-8:
            t2 = cls._trip_t(a, b, c)
            if t2 < 0: return (), 0 # no intersection
            t = np.sqrt(t2)
            p1p, p1m = cls._trip_p(a, b, c, r1, r2, r3, t)
            p2p, p2m = cls._trip_p(b, a, c, r2, r3, r1, t)
            p3p, p3m = cls._trip_p(c, a, b, r3, r1, r2, t)

            if p1p > 0 and p2p > 0 and p3p > 0:
                p1, p2, p3 = p1m, p2m, p3m
            else:
                p1, p2, p3 = p1p, p2p, p3p

            if p1 > 0 and p2 > 0 and p3 > 0:
                return (), 0
            if p1 <= 0 and p2 > 0 and p3 > 0:
                # _, area = cls.sphere_double_intersection_area(a, r2, r3)
                return (1, 2), None
            if p1 > 0 and p2 <= 0 and p3 > 0:
                # _, area = cls.sphere_double_intersection_area(b, r1, r3)
                return (0, 2), None
            if p1 > 0 and p2 > 0 and p3 <= 0:
                # _, area = cls.sphere_double_intersection_area(c, r1, r2)
                return (0, 1), None
            if p1 <= 0 and p2 <= 0 and p3 > 0:
                return (2,), None#-cls.sphere_area(r3)
            if p1 <= 0 and p2 > 0 and p3 <= 0:
                return (1,), None#-cls.sphere_area(r2)
            if p1 > 0 and p2 <= 0 and p3 <= 0:
                return (0,), None#-cls.sphere_area(r1)
            else:
                raise ValueError((p1 > 0,  p2 > 0,  p3 > 0),
                                 p1, p2, p3)
                raise ValueError("don't know what to do here")

        e1 = cls._trip_e(a, r2, r3) #(r2**2 - r3**2) / a**2
        e2 = cls._trip_e(b, r3, r1) #(r3**2 - r1**2) / b**2
        e3 = cls._trip_e(c, r1, r2) #(r1**2 - r2**2) / c**2

        q1 = cls._trip_q(a, b, c, r1, r2, r3, e1)
        q2 = cls._trip_q(b, c, a, r2, r3, r1, e2)
        q3 = cls._trip_q(c, a, b, r3, r1, r2, e3)

        A1 = cls._trip_s(r1, c, b, q3, q2, e3, e2, w)
        A2 = cls._trip_s(r2, a, c, q1, q3, e1, e3, w)
        A3 = cls._trip_s(r3, b, a, q2, q1, e2, e1, w)


        return None, A1 + A2 + A3

    IntersectionCircle = collections.namedtuple("IntersectionCircle",
                                                ["center", "normal", "radius"]
                                                )
    @classmethod
    def sphere_double_intersection_circle(cls, centers, radii, dist=None):
        d = centers[1] - centers[0]
        a = dist
        u, a = nput.vec_normalize(d, norms=dist, return_norms=True)

        r, R = radii**2
        x = (a**2 - R + r) / (2 * a)
        r = np.sqrt(r - x**2)
        return cls.IntersectionCircle(centers[0] + u*x, u, r)
    @classmethod
    def sphere_triple_intersection_point(cls, centers, radii, dists=None):
        # we assume it has been checked that the three spheres intersect using the determinant
        # above

        #TODO: vectorize for multiple sets of intersections
        #TODO: move into Numputils for axis system finding
        dxy = centers[1:] - centers[(0,)]
        (x, y), norms = nput.vec_normalize(dxy, norms=dists, return_norms=True)
        cxy = np.dot(y, x)
        #TODO: handle colinearity
        y = (y - cxy*x) / np.sqrt(1-cxy**2) # norm known analytically
        z = nput.vec_crosses(x, y)# normalized by construction
        axes = np.array([x, y, z])

        #TODO: rederive these w.r.t cos terms and norms...
        cxy = np.dot(x, dxy[1])
        cyy = np.dot(y, dxy[1])

        R1, R2, R3 = radii**2
        n_x, n_y = norms
        RX = n_x**2
        I, J = cxy**2, cyy**2
        X = (R1 - R2 + RX) / (2*n_x)
        Y = (R1 - R3 - 2*cxy*X + I + J) / (2*cyy)
        Z = np.sqrt(R1 - X**2 - Y**2)

        return [
            centers[0] + np.dot([X, Y, Z], axes),
            centers[0] + np.dot([X, Y, -Z], axes),
        ]

    @classmethod
    def get_intersections(cls, centers, radii):
        dm = nput.distance_matrix(centers)
        nc = len(centers)
        intersects = np.full((nc, nc), True)
        intersection_disks = []
        for i, j in itertools.combinations(range(nc), 2):
            if radii[i] + radii[j] > dm[i, j]:
                intersects[i, j] = True
                intersection_disks.append(
                    cls.sphere_double_intersection_circle(
                        centers[(i, j),],
                        radii[(i, j),],
                        dist=dm[i, j]
                    )
                )
        intersection_points = []
        for i, j, k in itertools.combinations(range(nc), 3):
            if all(intersects[p] for p in itertools.combinations((i, j, k), 2)):
                w = cls._trip_w(
                    dm[j, k], dm[i, k], dm[i, j],
                    radii[i], radii[j], radii[k]
                )
                if w > 0:
                    intersection_points.append(
                        cls.sphere_triple_intersection_point(
                            centers[(i, j, k),],
                            radii[(i, j, k),],
                            dists=(dm[i, j], dm[i, k])
                        )
                    )

        return intersection_points, intersection_disks

    @classmethod
    def sphere_double_intersection_area(cls, a, r1, r2):
        t1 = r1 + r2 - a
        t2 = r1 - r2 + a
        t3 = -r1 + r2 + a
        if t1 > 0 and t2 > 0 and t3 > 0:
            return None, np.pi * (
                    2 * (r1**2 + r2**2)
                    - (r1 + r2) * a
                    - (r2 - r1)*(r2**2 - r1**2)/a
            )
        elif t1 < 0:
            return (), 0
        elif t2 < 0:
            return (0,), cls.sphere_area(r1)
        else:
            return (1,), cls.sphere_area(r2)

    @classmethod
    def _quad_w(cls, a, b, c, f, g, h):
        A = a ** 2
        B = b ** 2
        C = c ** 2
        F = f ** 2
        G = g ** 2
        H = h ** 2
        d = np.linalg.det([
            [0, 1, 1, 1, 1],
            [1, 0, H, G, F],
            [1, H, 0, A, B],
            [1, G, A, 0, C],
            [1, F, B, C, 0],
        ])
        if d < 0:
            return d
        else:
            return np.sqrt(1 / 2 * d)
    @classmethod
    def _quad_s(cls, a, b, c, f, g, h):
        return a * (
                b**2 + c**2 - a**2 + g**2 + h**2
                - 2*f**2 + (g**2 - h**2)*(b**2 - c**2)/a**2
        )
    @classmethod
    def _quad_term(cls, a, beta, gamma, W2, s1):
        t = np.arctan(W2 / s1)
        if t < 0:
            t = t + np.pi
        elif t > np.pi:
            t = t - np.pi
        return a*(beta + gamma)*(1 + ((beta - gamma)**2) /a**2) * t
    @classmethod
    def triangle_area(cls, a, b, c):
        s = (a + b + c) /2
        area = np.sqrt(s*(s-a)*(s-b)*(s-c))
        return area
    @classmethod
    def sphere_quadruple_intersection_area(cls,
                                           a, b, c, f, g, h,
                                           # 23, 12, 13, 14, 24, 34
                                           r1, r2, r3, r4,
                                           A123, A124, A134, A234,
                                           I4, I3, I2, I1
                                           ):


        W2 = 2*cls._quad_w(a, b, c, f, g, h)

        # if W2 < 0:
        ia4, ib4 = I4
        ia3, ib3 = I3
        ia2, ib2 = I2
        ia1, ib1 = I1

        test_bits = (int(ia4), int(ib4), int(ia3), int(ib3), int(ia2), int(ib2), int(ia1), int(ib1))

        # clean_tests = [
        #     ((1, 0) if s1 == 0 else (0, 1))
        #     + ((1, 0) if s2 == 0 else (0, 1))
        #     + ((1, 0) if s3 == 0 else (0, 1))
        #     + ((1, 0) if s4 == 0 else (0, 1))
        #     for s1, s2, s3, s4 in itertools.product(range(2), range(2), range(2), range(2))
        # ]
        clean_tests = {
            (1, 0, 1, 0, 1, 0, 1, 0),
            (1, 0, 1, 0, 1, 0, 0, 1),
            (1, 0, 1, 0, 0, 1, 1, 0),
            (1, 0, 1, 0, 0, 1, 0, 1),
            (1, 0, 0, 1, 1, 0, 1, 0),
            (1, 0, 0, 1, 1, 0, 0, 1),
            (1, 0, 0, 1, 0, 1, 1, 0),
            (1, 0, 0, 1, 0, 1, 0, 1),
            (0, 1, 1, 0, 1, 0, 1, 0),
            (0, 1, 1, 0, 1, 0, 0, 1),
            (0, 1, 1, 0, 0, 1, 1, 0),
            (0, 1, 1, 0, 0, 1, 0, 1),
            (0, 1, 0, 1, 1, 0, 1, 0),
            (0, 1, 0, 1, 1, 0, 0, 1),
            (0, 1, 0, 1, 0, 1, 1, 0),
            (0, 1, 0, 1, 0, 1, 0, 1)
        }

        # print(test_bits)

        if test_bits == (1, 1, 0, 0, 0, 0, 0, 0):
            # _, area = cls.sphere_triple_intersection_area(a, b, c, r1, r2, r3)
            return (0, 1, 2), None
        elif test_bits == (0, 0, 1, 1, 0, 0, 0, 0):
            # _, area = cls.sphere_triple_intersection_area(g, f, c, r1, r2, r4)
            return (0, 1, 3), None
        elif test_bits == (0, 0, 0, 0, 1, 1, 0, 0):
            # _, area = cls.sphere_triple_intersection_area(h, f, b, r1, r3, r4)
            return (0, 2, 3), None
        elif test_bits == (0, 0, 0, 0, 0, 0, 1, 1):
            # _, area = cls.sphere_triple_intersection_area(h, g, a, r2, r3, r4)
            return (1, 2, 3), None
        elif test_bits == (1, 1, 1, 1, 0, 0, 0, 0):
            # _, area = cls.sphere_double_intersection_area(c, r1, r2)
            return (0, 1), None
        elif test_bits == (1, 1, 0, 0, 1, 1, 0, 0):
            # _, area = cls.sphere_double_intersection_area(b, r1, r3)
            return (0, 2), None
        elif test_bits == (0, 0, 1, 1, 1, 1, 0, 0):
            # _, area = cls.sphere_double_intersection_area(f, r1, r4)
            return (0, 3), None
        elif test_bits == (1, 1, 0, 0, 0, 0, 1, 1):
            # _, area = cls.sphere_double_intersection_area(a, r2, r3)
            return (1, 2), None
        elif test_bits == (0, 0, 1, 1, 0, 0, 1, 1):
            # _, area = cls.sphere_double_intersection_area(g, r2, r4)
            return (1, 3), None
        elif test_bits == (0, 0, 0, 0, 1, 1, 1, 1):
            # _, area = cls.sphere_double_intersection_area(h, r3, r4)
            return (2, 3), None
        elif test_bits == (1, 1, 1, 1, 1, 1, 0, 0):
            return (0,), None#cls.sphere_area(r1)
        elif test_bits == (1, 1, 1, 1, 0, 0, 1, 1):
            return (1,), None#cls.sphere_area(r2)
        elif test_bits == (1, 1, 0, 0, 1, 1, 1, 1):
            return (2,), None#cls.sphere_area(r3)
        elif test_bits == (0, 0, 1, 1, 1, 1, 1, 1):
            return (3,), None#cls.sphere_area(r4)
        elif test_bits == (1, 1, 1, 1, 1, 1, 1, 1):
            # if W2 < 0:
            T123 = cls.triangle_area(r1, r2, r3)
            T124 = cls.triangle_area(r1, r2, r4)
            T134 = cls.triangle_area(r1, r3, r4)
            T234 = cls.triangle_area(r2, r3, r4)
            test_vec = np.array([T123, T124, T134, T234])

            if (
                    abs(np.dot([1, 1, -1, -1], test_vec)) < 1e-6
                    or abs(np.dot([1, -1, 1, -1], test_vec)) < 1e-6
                    or abs(np.dot([1, -1, -1, 1], test_vec)) < 1e-6
            ):
                A, B, C, F, G, H = np.array([a, b, c, f, g, h])**2
                # need to find triangles
                if (A - (B + C)) > 1e-6:
                    # 1 --c-- 2
                    # | b   g |
                    # 3 --h-- 4
                    # _, area = cls.sphere_double_intersection_area(a, r2, r3)
                    return (1, 2), None
                elif (B - (A + C)) > 1e-6:
                    # 2 --c-- 1
                    # | a   g |
                    # 3 --h-- 4
                    # _, area = cls.sphere_double_intersection_area(b, r1, r3)
                    return (0, 2), None
                elif (C - (A + B)) > 1e-6:
                    # 3 --b-- 1
                    # | a   f |
                    # 2 --g-- 4
                    # _, area = cls.sphere_double_intersection_area(c, r1, r2)
                    return (0, 1), None
                elif (F - (G + H)) > 1e-6:
                    # 3 --b-- 1
                    # | h   c |
                    # 4 --f-- 2
                    # f is a diagonal
                    # _, area = cls.sphere_double_intersection_area(f, r1, r4)
                    return (0, 3), None
                # elif (G - (F + H)) > 1e-6:
                #     # g is a diagonal
                #     _, area = cls.sphere_double_intersection_area(g, r2, r4)
                #     return (1, 3), area
                else:
                    raise ValueError("no set of diagonals works...")
            elif abs(np.dot([1, 1, 1, -1], test_vec)) < 1e-6:
                raise NotImplementedError(...)
            else:
                raise ValueError("no set of areas works...")
        elif test_bits not in clean_tests:
            raise ValueError(test_bits)

        if W2 <= 0:
            raise ValueError(...)

        s1 = cls._quad_s(a, b, c, f, g, h)
        s2 = cls._quad_s(b, c, a, g, h, f)
        # s22 = b * (
        #         c ** 2 + a ** 2 - b ** 2 + h ** 2 + f ** 2
        #         - 2 * g ** 2 + (h ** 2 - f ** 2) * (c ** 2 - a ** 2) / b ** 2
        # )
        # if s2 != s22:
        #     raise ValueError(...)
        s3 = cls._quad_s(c, a, b, h, f, g)
        # si = c * (
        #         a ** 2 + b ** 2 - c ** 2 + f ** 2 + g ** 2
        #         - 2 * h ** 2 + (f ** 2 - g ** 2) * (a ** 2 - b ** 2) / c ** 2
        # )
        # if s3 != si:
        #     raise ValueError(...)
        s4 = cls._quad_s(h, a, g, c, f, b)
        # si = h * (
        #         f ** 2 + b ** 2 - h ** 2 + a ** 2 + g ** 2
        #         - 2 * c ** 2 + (f ** 2 - b ** 2) * (a ** 2 - g ** 2) / h ** 2
        # )
        # if s4 != si:
        #     raise ValueError(...)
        s5 = cls._quad_s(g, h, a, b, c, f)
        # si = g * (
        #         h ** 2 + a ** 2 - g ** 2 + c ** 2 + f ** 2
        #         - 2 * b ** 2 + (c ** 2 - f ** 2) * (h ** 2 - a ** 2) / g ** 2
        # )
        # if s5 != si:
        #     raise ValueError(...)
        s6 = cls._quad_s(f, g, c, a, b, h)
        # si = f * (
        #         g ** 2 + c ** 2 - f ** 2 + b ** 2 + h ** 2
        #         - 2 * a ** 2 + (b ** 2 - h ** 2) * (g ** 2 - c ** 2) / f ** 2
        # )
        # if s6 != si:
        #     raise ValueError(...)

        A1 = cls._quad_term(a, r2, r3, W2, s1) #a*(beta + gamma)*(1 + ((beta - gamma)**2) /a**2) * t
        A2 = cls._quad_term(b, r1, r3, W2, s2)
        A3 = cls._quad_term(c, r1, r2, W2, s3)
        A4 = cls._quad_term(h, r3, r4, W2, s4)
        A5 = cls._quad_term(g, r2, r4, W2, s5)
        A6 = cls._quad_term(f, r1, r4, W2, s6)

        A = (
                -np.pi * (r1 ** 2 + r2 ** 2 + r3 ** 2 + r4 ** 2)
                + 1 / 2 * (
                        A1 + A2 + A3
                        + A4 + A5 + A6
                        + A123 + A124
                        + A134 + A234
                )
        )

        return None, A

    @classmethod
    def sphere_area(cls, radii, axis=None):
        return 4*np.pi*np.sum(radii**2, axis=axis)

    @classmethod
    def sphere_union_surface_area(cls,
                                  centers, radii,
                                  include_doubles=True,
                                  include_triples=None,
                                  include_quadruples=None,
                                  # include_quintuples=None,
                                  return_terms=False,
                                  overlap_tolerance=0):
        if include_triples is None:
            include_triples = include_doubles
        if include_quadruples is None:
            include_quadruples = include_triples is not False
        # if include_quintuples is None:
        #     include_quintuples = include_quadruples is not False

        dm = nput.distance_matrix(centers)
        terms = {
            (i,):v
            for i,v in enumerate(cls.sphere_area(np.asanyarray(radii)[:, np.newaxis], axis=-1))
        }
        nc = len(centers)
        # visible = np.full((nc), True)
        # include_pairs = np.full((nc, nc), False)
        if include_doubles:
            for i,j in itertools.combinations(range(nc), 2):
                if not (
                        (i,) in terms
                        and (j,) in terms
                ): continue
                if (radii[i] + radii[j]) * (1+overlap_tolerance) > dm[i, j]:
                    overlaps, contrib = cls.sphere_double_intersection_area(
                        dm[i, j], radii[i], radii[j]
                    )
                    if overlaps is not None:
                        if len(overlaps) > 0:
                            k:int = [i, j][overlaps[0]]
                            # visible[k] = False
                            terms.pop((k,), None)
                    else:
                        # include_pairs[i, j] = True
                        terms[(i, j)] = -contrib

        if include_quadruples:
            intersection_points = np.full((nc, nc, nc, 2, 3), 0.0)
        else:
            intersection_points = None
        if include_triples or include_quadruples:
            for i,j,k in itertools.combinations(range(nc), 3):
                if not all(p in terms for p in itertools.combinations((i, j, k), 1)): continue
                if all(p in terms for p in itertools.combinations((i, j, k), 2)):
                    overlaps, contrib = cls.sphere_triple_intersection_area(
                        dm[j, k], dm[i, k], dm[i, j],
                        radii[i], radii[j], radii[k]
                    )
                    if overlaps is not None:
                        overlaps = tuple([i,j,k][x] for x in overlaps)
                        if len(overlaps) == 2:
                            i, j = overlaps
                            term_keys = list(terms.keys())
                            for p in term_keys:
                                if i in p and j in p:
                                    del terms[p]
                        elif len(overlaps) == 1:
                            l, = overlaps
                            term_keys = list(terms.keys())
                            for p in term_keys:
                                if l in p:
                                    del terms[p]
                    else:
                        if include_quadruples:
                            intersection_points[i, j, k] = cls.sphere_triple_intersection_point(
                                centers[(i, j, k),],
                                radii[(i, j, k),],
                                dists=(dm[i, j], dm[i, k])
                            )
                        terms[(i, j, k)] = contrib

        intersection_tests = None
        include_quartics = None
        if include_quadruples:
            intersection_tests = np.full((nc, nc, nc, nc, 2), False)
            # include_quartics = np.full((nc, nc, nc, nc), False)
            for i,j,k,l in itertools.combinations(range(nc), 4):
                if not all(p in terms for p in itertools.combinations((i, j, k, l), 1)): continue
                if not all(p in terms for p in itertools.combinations((i, j, k, l), 2)): continue
                if all(p in terms for p in itertools.combinations((i, j, k, l), 3)):
                    l_ints = intersection_tests[i, j, k, l] = (
                            np.linalg.norm(centers[(l,)] - intersection_points[i, j, k], axis=-1)
                             < radii[l] * (1 + overlap_tolerance)
                    )
                    k_ints = intersection_tests[i, j, l, k] = (
                            np.linalg.norm(centers[(k,)] - intersection_points[i, j, l], axis=-1)
                            < radii[k] * (1+overlap_tolerance)
                    )
                    j_ints = intersection_tests[i, k, l, j] = (
                            np.linalg.norm(centers[(j,)] - intersection_points[i, k, l], axis=-1)
                            < radii[j] * (1+overlap_tolerance)
                    )
                    i_ints = intersection_tests[j, k, l, i] = (
                            np.linalg.norm(centers[(i,)] - intersection_points[j, k, l], axis=-1)
                            < radii[i] * (1 + overlap_tolerance)
                    )
                    overlaps, contrib = cls.sphere_quadruple_intersection_area(
                        dm[j, k], dm[i, k], dm[i, j],
                        dm[i, l], dm[j, l], dm[k, l],
                        radii[i], radii[j], radii[k], radii[l],
                        terms[(i, j, k)], terms[(i,j,l)],
                        terms[(i, k, l)], terms[(j,k,l)],
                        l_ints, k_ints, j_ints, i_ints
                    )
                    if overlaps is not None:
                        overlaps = tuple([i, j, k, l][x] for x in overlaps)
                        if len(overlaps) == 3:
                            x, y, z = overlaps
                            term_keys = list(terms.keys())
                            for p in term_keys:
                                if x in p and y in p and z in p:
                                    del terms[p]
                        elif len(overlaps) == 2:
                            x, y, = overlaps
                            term_keys = list(terms.keys())
                            for p in term_keys:
                                if x in p and y in p:
                                    del terms[p]
                        elif len(overlaps) == 1:
                            term_keys = list(terms.keys())
                            x, = overlaps
                            for p in term_keys:
                                if x in p:
                                    del terms[p]
                    else:
                        terms[(i, j, k, l)] = -contrib

        if return_terms:
            return terms
        else:
            if include_doubles and include_triples and include_quadruples:
                return sum(terms.values())
            else:
                return sum(
                    v
                    for k,v in terms.items()
                    if (
                        len(k) == 1
                        or (include_doubles and len(k) == 2)
                        or (include_triples and len(k) == 3)
                        or (include_quadruples and len(k) == 4)
                    )
                )

    def surface_area(self, method='union', **opts):
        if method == 'union':
            return self.sphere_union_surface_area(self.centers, self.radii, **opts)
        elif method == 'sampling':
            expansion = opts.pop('expansion', self.expansion)
            scaling = opts.pop('scaling', self.scaling)
            generator_args = {
                'samples':opts.pop('samples', self.samples),
                'generator':opts.pop('sphere_point_generator', None)
            }
            opts['tolerance'] = opts.get('tolerance', self.tolerance)
            return self.sampling_point_surface_area(
                self.centers,
                self.radii * scaling + expansion,
                generator_args=generator_args,
                **opts
            )
        elif method == 'mesh':
            return self.get_triangulation().surface_area()
        elif method == 'pcmesh':
            return self.generate_mesh().surface_area()
        else:
            raise ValueError(f"unknown surface area method '{method}'")

    def volume(self, method='monte-carlo', **opts):
        if method == 'union':
            raise NotImplementedError("analytic sphere volume not yet implemented")
        elif method == 'sampling':
            expansion = opts.pop('expansion', self.expansion)
            scaling = opts.pop('scaling', self.scaling)
            generator_args = {
                'samples': opts.pop('samples', self.samples),
                'generator': opts.pop('sphere_point_generator', None)
            }
            opts['tolerance'] = opts.get('tolerance', self.tolerance)
            return self.sampling_point_volume(
                self.centers,
                self.radii * scaling + expansion,
                generator_args=generator_args,
                **opts
            )
        elif method == 'voxel':
            return self.volume_voxel(self.centers, self.radii, **opts)
        elif method == 'monte-carlo':
            return self.volume_union_mc(self.centers, self.radii, **opts)
        elif method == 'mesh':
            return self.get_triangulation().volume()
        elif method == 'pcmesh':
            return self.generate_mesh().volume()
        else:
            raise ValueError(f"unknown surface area method '{method}'")

    def plot(self,
             figure=None,
             *,
             points=None,
             function=None,
             sphere_color='white',
             sphere_style=None,
             point_style=None,
             point_values=None,
             distance_units='Angstroms',
             plot_intersections=False,
             **etc
             ):

        if points is None:
            points = self.sampling_points

        # TODO: move this to molecule specific class...
        conv = UnitsData.convert("BohrRadius", distance_units)
        if point_values is None and function is not None:
            point_values = function(points)

        if point_values is not None:
            etc['color'] = etc.get('color', None)

        return self.plot_sphere_points(
            points * conv,
            self.centers * conv,
            self.radii * conv,
            figure=figure,
            sphere_color=sphere_color,
            point_values=point_values,
            sphere_style=sphere_style,
            point_style=point_style,
            plot_intersections=plot_intersections,
            **etc
        )

    @classmethod
    def plot_sphere_points(cls,
                           points,
                           centers,
                           radii,
                           figure=None,
                           *,
                           color='black',
                           # transparency=.8,
                           backend='x3d',
                           return_objects=False,
                           sphere_color='white',
                           sphere_style=None,
                           point_colors=None,
                           point_values=None,
                           vertex_colormap='WarioColors',
                           rescale_color_values=True,
                           plot_intersections=False,
                           intersection_point_style=None,
                           intersection_circle_style=None,
                           **etc):
        from ... import Plots as plt

        if figure is None:
            figure = plt.Graphics3D(backend=backend)

        # func_vals = func(verts)
        if point_values is not None and rescale_color_values:
            if dev.is_list_like(rescale_color_values):
                point_values = nput.vec_rescale(point_values, rescale_color_values)
            else:
                point_values = nput.vec_rescale(point_values)

            colormap = plt.Colors.ColorPalette(vertex_colormap)
            point_colors = colormap(point_values)

        objs = []
        if sphere_style is None:
            sphere_style = etc if color is None else {}
            if sphere_color is not None:
                sphere_style['color'] = sphere_color
        if len(sphere_style) > 0:
            for c,r in zip(centers,radii):
                objs.append(
                    plt.Sphere(c, r, **sphere_style)
                )

        if plot_intersections:
            intersection_points, intersection_disks = cls.get_intersections(
                centers,
                radii
            )

            if intersection_circle_style is None:
                intersection_circle_style = {
                    'line_color': 'black',
                    'line_thickness':.02,
                    'subdivision':'64,64'
                }
            for disk in intersection_disks:
                circle_obj = plt.Disk(
                    disk.center,
                    radius=disk.radius,
                    normal=disk.normal,
                    **intersection_circle_style
                )
                objs.append(circle_obj)

            if len(intersection_points) > 0:
                if intersection_point_style is None:
                    intersection_point_style = {
                        'color':'red',
                        'point_size':30
                    }
                # for p in np.concatenate(intersection_points, axis=0):
                #     objs.append(plt.Sphere(p, .1, color='teal'))

                point_obj = plt.Point(
                    np.concatenate(intersection_points, axis=0),
                    **intersection_point_style
                )
                objs.append(point_obj)


        if point_colors is not None or color is not None:
            point_obj = plt.Point(
                points,
                color=color,
                vertex_colors=point_colors,
                **etc)
            objs.append(point_obj)


        for o in objs:
            o.plot(figure)

        if return_objects:
            return figure, objs
        else:
            return figure

class SphereUnionSurfaceMesh:
    def __init__(self, verts, inds, surf=None, densities=None, tri_map=None, vert_map=None, normals=None,
                 vertex_normals=None):
        self.surf = surf
        self.verts = verts
        self.inds = inds
        self.densities = densities
        self.vert_map = vert_map
        self.tri_map = tri_map
        self._normals = normals
        self.vertex_normals = vertex_normals
        self._derivative_term_cache = {}

    def surface_area(self, return_components=False):
        dm = nput.distance_matrix(self.verts)
        a = dm[self.inds[:, 0], self.inds[:, 1]]
        b = dm[self.inds[:, 1], self.inds[:, 2]]
        c = dm[self.inds[:, 0], self.inds[:, 2]]
        s = (a + b + c) /2
        tris = np.sqrt(s*(s-a)*(s-b)*(s-c))
        if return_components:
            return tris
        else:
            return np.sum(tris)

    def volume(self, return_components=False):
        """
        Exact volume of a closed mesh via the divergence theorem.
        Assumes outward-pointing face normals and watertight mesh.
        """
        v1 = self.verts[self.inds[:, 0], :]
        comps = np.sum((v1 * self.signed_volumes[:, np.newaxis] * self.normals), axis=-1) / 6
        if return_components:
            return comps
        else:
            return np.sum(np.abs(comps))

    def normal_derivatives(self, order=1):
        i_list, j_list, k_list = self.inds.T
        terms = [
            nput.normal_deriv(self.verts, i, j, k, order=order,
                              cache=self._derivative_term_cache) #TODO: handle the broadcasting properly in `normal_deriv`
            for i, j, k in zip(i_list, j_list, k_list)
        ]
        return [np.array(e) for e in zip(*terms)]
    def _dist_deriv(self, i_list, j_list, order):
        terms = [
            nput.dist_deriv(self.verts, i, j, order=order,
                              cache=self._derivative_term_cache)
            for i, j in zip(i_list, j_list)
        ]
        return [np.array(e) for e in zip(*terms)]

    def area_derivatives(self, order=1, return_components=False):
        i_list, j_list, k_list = self.inds.T
        terms = []
        for i, j, k in zip(i_list, j_list, k_list):
            n_a = nput.dist_deriv(self.verts, i, j, order=order, cache=self._derivative_term_cache)
            n_b = nput.dist_deriv(self.verts, j, k, order=order, cache=self._derivative_term_cache)
            n_c = nput.dist_deriv(self.verts, k, i, order=order, cache=self._derivative_term_cache)
            # no reason to handle a bunch of zeros
            subterms = [np.zeros_like(a) for a in n_a]

            # deriv contribs look like (n_verts*3, ...)
            # reshape each term and subsample only relevant portions
            indices = np.concatenate([np.arange(3) + 3*i, np.arange(3) + 3*j, np.arange(3) + 3*k], axis=0)
            n_a = [n[np.ix_(*[indices] * m)] if m > 0 else n for m,n in enumerate(n_a)]
            n_b = [n[np.ix_(*[indices] * m)] if m > 0 else n for m,n in enumerate(n_b)]
            n_c = [n[np.ix_(*[indices] * m)] if m > 0 else n for m,n in enumerate(n_c)]

            s = nput.scale_expansion(nput.add_expansions(n_a, n_b, n_c), 1/2)
            da, db, dc = (
                             nput.subtract_expansions(s, n_a),
                             nput.subtract_expansions(s, n_b),
                             nput.subtract_expansions(s, n_c)
            )
            tri_term = nput.scalarprod_deriv(
                nput.scalarprod_deriv(
                    nput.scalarprod_deriv(s, da, order),
                    db, order
                ),
                dc, order
            )
            tris = nput.scalarpow_deriv(tri_term, -1/2, order)

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

    def centroid_derivatives(self, order=1, return_components=False):
        i, j, k = self.inds.T
        # a scaled diagonal (3*n_verts, n_tris, 3)
        centroids = np.average(self.verts[self.inds], axis=-2)
        expansion = [centroids]
        if order > 0:
            dx = np.zeros((len(i), 3*len(self.verts), 3))
            n = np.arange(len(i))
            for a in range(3):
                dx[n, i*3+a, a] = 1/3
                dx[n, j*3+a, a] = 1/3
                dx[n, k*3+a, a] = 1/3
            expansion.append(dx)
        for m in range(2, order+1):
            dx = np.zeros((len(i), 3*len(self.verts),) + (3,) * m)
            expansion.append(dx)
        return expansion

    def volume_derivatives(self, order=1, return_components=False,
                           normal_order=None,
                           area_order=None,
                           centroid_order=None):
        # from ...Profilers import Timer
        # with Timer('normals'):
        nd = self.normal_derivatives(order=order if normal_order is None else normal_order)
        # with Timer('areas'):
        ad = self.area_derivatives(order=order if area_order is None else area_order, return_components=True)
        # with Timer('centroid'):
        cd = self.centroid_derivatives(order=order if centroid_order is None else centroid_order)

        # with Timer('mult'):
        #TODO: subsample this so only relevant tris are manipulated at once
        terms = nput.scale_expansion(
            nput.scalarprod_deriv(ad,
                                  nput.tensordot_deriv(cd, nd, order=order, axes=[-1, -1], shared=1),
                                  order=order),
            1/3
        )

        if return_components:
            return terms
        else:
            return [np.sum(t, axis=0) for t in terms]

    @property
    def normals(self):
        if self._normals is None:
            self._normals = self.get_normals()
        return self._normals[0]
    @property
    def signed_volumes(self):
        if self._normals is None:
            self._normals = self.get_normals()
        return self._normals[1]
    def get_normals(self, normalize=True):
        tri_pts = self.verts[self.inds]
        crosses = nput.vec_crosses(tri_pts[:, 2] - tri_pts[:, 1], tri_pts[:, 0] - tri_pts[:, 1])
        return nput.vec_normalize(crosses, return_norms=True)

    @classmethod
    def from_submeshes(cls, pts, submeshes, *, centers, radii,
                       occlusion_type='complete',
                       occlusion_tolerance=1e-2,
                       check_normals=True,
                       deduplicate_points=False,
                       duplicate_point_threshold=1e-14,
                       vert_map=None,
                       intersection_point_mask=None,
                       occlusion_intersection_tolerance=5e-2,
                       **etc):
        pts = np.asanyarray(pts)
        if deduplicate_points:
            pair_dists = nput.distance_matrix(pts, return_triu=True)
            dupes = pair_dists < duplicate_point_threshold
            dm = np.full((len(pts), len(pts)), False)
            r,c = np.triu_indices(len(pts), k=1)
            dm[r, c] = dm[c, r] = dupes
            ncomp, labels = scipy.sparse.csgraph.connected_components(dm, directed=False, return_labels=True)
            _, groups = nput.group_by(np.arange(len(labels)), labels)[0]
            remapping = np.arange(len(pts))
            for g in groups:
                remapping[g,] = g[0]
            _, u_map, inv = np.unique(remapping, return_index=True, return_inverse=True)
            pts = pts[u_map,]
            submeshes = [
                inv[s] for s in submeshes
            ]
            if vert_map is not None:
                vert_map = np.asanyarray(vert_map)
                if vert_map.ndim == 1:
                    max_group_len = max(len(g) for g in groups)
                    vert_map = np.broadcast_to(vert_map[:, np.newaxis], (len(vert_map), max_group_len)).copy()
                    for g in groups:
                        vert_map[g, :len(g)] = vert_map[g, 0]
                vert_map = vert_map[u_map,]
            if intersection_point_mask is not None:
                intersection_point_mask = intersection_point_mask[u_map,]
        # dedupes
        if occlusion_type is None:
            tri_map = np.concatenate([
                np.full(len(t), i)
                for i, t in enumerate(submeshes)
            ])
            return cls(
                pts,
                np.concatenate(submeshes, axis=0),
                tri_map=tri_map,
                **etc
            )
        elif dev.str_in(occlusion_type, ['complete', 'partial', 'centroid']):
            tri_map = np.concatenate([
                np.full(len(t), i)
                for i, t in enumerate(submeshes)
            ])
            all_tris = np.concatenate(submeshes, axis=0)
            if occlusion_type in ['entire', 'centroid']:
                centroids = np.average(pts[all_tris], axis=-2)
                centroid_mask = SphereUnionSurface.get_exterior_points(
                    centroids,
                    centers,
                    radii,
                    tolerance=occlusion_tolerance
                )
                all_tris = all_tris[centroid_mask]
                tri_map = tri_map[centroid_mask]
            points_mask = SphereUnionSurface.get_exterior_points(
                pts,
                centers,
                radii,
                vertex_map=vert_map,
                intersection_point_mask=intersection_point_mask,
                intersection_point_tolerance=occlusion_intersection_tolerance,
                tolerance=occlusion_tolerance
            )
            occlusion_count = 3 - np.sum(points_mask[all_tris], axis=-1)
            if occlusion_type in ['entire', 'complete']:
                submask = occlusion_count == 0
                all_tris = all_tris[submask]
                tri_map = tri_map[submask]
            elif occlusion_type == 'partial':
                submask = occlusion_count < 2
                all_tris = all_tris[submask]
                tri_map = tri_map[submask]

            point_indexing = np.unique(all_tris.flatten())

            pts = pts[point_indexing,]
            if vert_map is not None:
                vert_map = vert_map[point_indexing,]
            remapping = np.full(len(points_mask), -1, dtype=int)
            remapping[point_indexing] = np.arange(len(point_indexing))
            all_tris = remapping[all_tris]

            if len(all_tris) == 0:
                raise ValueError("all triangles pruned")

            if check_normals: # determine if the triangle normal points in or out from its radius, rotate if needed
                tri_pts = pts[all_tris]
                normals = nput.vec_crosses(tri_pts[:, 0] - tri_pts[:, 1], tri_pts[:, 2] - tri_pts[:, 1])
                centroids = np.average(tri_pts, axis=-2)
                centroid_vectors = centroids - centers[tri_map]
                normal_sign = np.sign(nput.vec_dots(normals, centroid_vectors))
                all_tris[normal_sign > 0] = all_tris[normal_sign > 0][:, (0, 2, 1)]
                normals[normal_sign < 0] *= -1
                # tri_pts = pts[all_tris]
                # normals = nput.vec_crosses(tri_pts[:, 0] - tri_pts[:, 1], tri_pts[:, 2] - tri_pts[:, 1])
                # normal_sign = np.sign(nput.vec_dots(normals, centroid_vectors))
            else:
                normals = None


            return cls(
                pts,
                all_tris,
                tri_map=tri_map,
                vert_map=vert_map,
                normals=normals,
                **etc
            )
        else:
            raise NotImplementedError(f"`occlusion_type` {occlusion_type} not supported")


    @classmethod
    def from_subclouds(cls, point_clouds, *, centers, radii, mesh_type='convex', occlusion_type='partial',
                       vert_map=None,
                       deduplicate_points=False,
                       mesh_kwargs=None,
                       intersection_point_mask=None,
                       **surface_options):
        if dev.str_is(mesh_type, 'convex'):
            mesh_type = spat.ConvexHull
        all_tris = []
        all_points = np.concatenate(point_clouds, axis=0)
        offset = 0
        if vert_map is None:
            vert_map = np.concatenate([
                    np.full(len(t), i)
                    for i, t in enumerate(point_clouds)
                ])
        if mesh_kwargs is None:
            mesh_kwargs = {}
        for t in point_clouds:
            if len(t) > 3:
                hull = mesh_type(t, **mesh_kwargs)
                all_tris.append(hull.simplices + offset)
            offset += len(t)
        if intersection_point_mask is not None and len(intersection_point_mask) != len(all_points):
            intersection_point_mask = np.concatenate(intersection_point_mask, axis=0)
        return cls.from_submeshes(
            all_points,
            all_tris,
            centers=centers,
            radii=radii,
            occlusion_type=occlusion_type,
            vert_map=vert_map,
            deduplicate_points=deduplicate_points,
            intersection_point_mask=intersection_point_mask,
            **surface_options
        )


    @classmethod
    def from_o3d(cls, mesh, densities=None, surf=None):
        return cls(
            np.array(mesh.vertices),
            np.array(mesh.triangles),
            densities=densities,
            surf=surf
        )

    def plot(self,
             figure=None,
             *,
             function=None,
             vertex_values=None,
             normals=None,
             invert_mesh=False,
             distance_units='Angstroms',
             **etc
             ):

        # TODO: move this to molecule specific class...
        conv = UnitsData.convert("BohrRadius", distance_units)
        if vertex_values is None and function is not None:
            vertex_values = function(self.verts)

        if vertex_values is not None:
            etc['color'] = etc.get('color', None)

        if normals is True:
            normals = self.normals

        inds = self.inds
        if invert_mesh:
            inds = inds[:, (0, 2, 1)]

        return self.plot_triangle_mesh(
            self.verts * conv,
            inds,
            figure=figure,
            normals=normals,
            vertex_values=vertex_values,
            **etc
        )

    @classmethod
    def plot_triangle_mesh(cls,
                           verts, indices,
                           figure=None,
                           *,
                           color='blue',
                           transparency=.8,
                           backend='x3d',
                           return_objects=False,
                           line_color='black',
                           line_transparency=.9,
                           line_style=None,
                           vertex_colors=None,
                           vertex_values=None,
                           vertex_colormap='WarioColors',
                           rescale_color_values=True,
                           normals=None,
                           centroids=None,
                           normal_color='black',
                           normal_radius=.01,
                           normal_scaling=.5,
                           **etc):
        from ... import Plots as plt

        if figure is None:
            figure = plt.Graphics3D(backend=backend)

        # func_vals = func(verts)
        if vertex_values is not None and rescale_color_values:
            if dev.is_list_like(rescale_color_values):
                vertex_values = nput.vec_rescale(vertex_values, rescale_color_values)
            else:
                vertex_values = nput.vec_rescale(vertex_values)

            colormap = plt.Colors.ColorPalette(vertex_colormap)
            vertex_colors = colormap(vertex_values)

        objs = []
        if vertex_colors is not None or color is not None:
            tri_obj = plt.Triangle(verts,
                                   indices=indices, transparency=transparency, color=color,
                                   vertex_colors=vertex_colors,
                                   **etc)
            objs.append(tri_obj)

        if line_style is None:
            line_style = etc if (color is None and vertex_colors is None) else {}
        else:
            line_style = line_style.copy()

        if line_color is not None or len(line_style) > 0:
            line_style['color'] = line_style.get('color', line_color)
            line_style['transparency'] = line_style.get('transparency', line_transparency)
            line_obj = plt.Line(verts, indices=indices, **line_style)
            objs.append(line_obj)

        if normals is not None:
            normals = np.asanyarray(normals) * normal_scaling
            if centroids is None:
                centroids = np.average(verts[indices], axis=-2)
            # print(centroids, normals)
            for p,n in zip(centroids, normals):
                objs.append(
                    plt.Arrow(p, p+n, color=normal_color, radius=normal_radius)
                )

        for o in objs:
            o.plot(figure)

        if return_objects:
            return figure, objs
        else:
            return figure

