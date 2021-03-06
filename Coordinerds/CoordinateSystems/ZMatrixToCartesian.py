from .CoordinateSystemConverter import CoordinateSystemConverter
from .CommonCoordinateSystems import CartesianCoordinateSystem, ZMatrixCoordinateSystem
from ...Numputils import *
import numpy as np
# this import gets bound at load time, so unfortunately PyCharm can't know just yet
# what properties its class will have and will try to claim that the files don't exist

class ZMatrixToCartesianConverter(CoordinateSystemConverter):
    """
    A converter class for going from ZMatrix coordinates to Cartesian coordinates
    """

    @property
    def types(self):
        return (ZMatrixCoordinateSystem, CartesianCoordinateSystem)

    @staticmethod
    def zmatrix_affine_transforms(centers, vecs1, vecs2, angles, dihedrals, return_comps=False):
        """Builds a single set of affine transformation matrices to apply to the vecs1 to get the next set of points

        :param centers: central coordinates
        :type centers: np.ndarray
        :param vecs1: vectors coming off of the centers
        :type vecs1: np.ndarray
        :param vecs2: vectors coming off of the centers
        :type vecs2: np.ndarray
        :param angles: angle values
        :type angles: np.ndarray
        :param dihedrals: dihedral values
        :type dihedrals: np.ndarray | None
        :return:
        :rtype:
        """
        crosses = vec_crosses(vecs2, vecs1)
        rot_mats_1 = rotation_matrix(crosses, angles)
        if dihedrals is not None:
            rot_mats_2 = rotation_matrix(vecs1, -dihedrals)
            rot_mat = np.matmul(rot_mats_2, rot_mats_1)
        else:
            rot_mat = rot_mats_1
            rot_mats_2 = None
        transfs = affine_matrix(rot_mat, centers)

        if return_comps:
            comps = (-crosses, rot_mats_2, rot_mats_1)
        else:
            comps = None
        return transfs, comps

    def build_next_points(self, refs1, dists, refs2, angles, refs3, dihedrals,
                          ref_axis = None,
                          return_comps = False
                          ):
        v = refs2 - refs1
        vecs1 = vec_normalize(v)
        if dihedrals is not None:
            v2 = refs3 - refs2
        else:
            # if no dihedral, for now we'll let our new axis be some random things in the x-y plane
            if ref_axis is None:
                v2 = np.concatenate((np.random.uniform(.5, 1, (len(refs1), 2)), np.zeros((len(refs1), 1))), axis=-1)
            elif ref_axis.ndim == 1:
                v2 = np.broadcast_to(ref_axis[np.newaxis, :], (len(refs1), 2))
            else:
                v2 = ref_axis
        vecs2 = vec_normalize(v2)

        transfs, comps = self.zmatrix_affine_transforms(refs1, vecs1, vecs2, angles, dihedrals, return_comps=return_comps)
        newstuff = affine_multiply(transfs, dists*vecs1)
        if return_comps:
            comps = (v, v2) + comps
        else:
            comps = None
        return newstuff, comps

    def default_ordering(self, coordlist):
        if coordlist.shape[-1] == 6:
            ordering = coordlist[:, :, (0, 2, 4)]
            coordlist = coordlist[:, :, (1, 3, 5)]
        else:
            r = np.arange(len(coordlist[0]))
            ordering = np.broadcast_to(
                np.array([r, np.roll(r, 1), np.roll(r, 2)]).T[np.newaxis],
                coordlist.shape[:2] + (3,)
            )
        return ordering, coordlist

    def _fill_deriv(self, i, derivs, r, q, f, ia, ib, ic, v, u, n, R1, R2):
        """

        Gets the derivatives for the current set of coordinates
        :param i:
        :type i: int
        :param derivs:
        :type derivs: np.ndarray
        :param r:
        :type r: np.ndarray
        :param q:
        :type q: np.ndarray | None
        :param f:
        :type f: np.ndarray | None
        :param ia:
        :type ia: np.ndarray(int)
        :param ib:
        :type ib: np.ndarray(int) | None
        :param ic:
        :type ic: np.ndarray(int) | None
        :param v:
        :type v: np.ndarray
        :param u:
        :type u: np.ndarray | None
        :param n:
        :type n: np.ndarray | None
        :param R1:
        :type R1: None
        :param R2:
        :type R2: None
        :return:
        :rtype:
        """

        i3 = np.broadcast_to(np.eye(3), (len(derivs), 3, 3))
        e3 = np.broadcast_to(levi_cevita3, (len(derivs), 3, 3, 3))

        # print(i, r, q, f, ia, ib, ic)
        zorks = np.arange(len(ia))

        nv = vec_norms(v)
        v = v/nv[..., np.newaxis]
        if i > 0:
            nu = vec_norms(u)
            u = u/nu[..., np.newaxis]
            nn = vec_norms(n)
            n = n/nn[..., np.newaxis]
            if R1 is None:
                Q = R2
            else:
                Q = np.matmul(R1, R2)

        for z in range(i+1): # Lower-triangle is 0
            for m in range(3):
                dx1 = derivs[zorks, z, m, ia]

                # Get derivatives for the v-vector

                if i > 0:
                    dx2 = derivs[zorks, z, m, ib]
                    dv = dx2 - dx1

                    dv = (1/nv[..., np.newaxis])*(dv - v*vec_dots(dv, v)[..., np.newaxis])

                    # Get derivatives for the u-vector
                    if i > 1:
                        dx3 = derivs[zorks, z, m, ic]
                        du = dx3 - dx2
                        du = 1/nu[..., np.newaxis]*(du - u*vec_dots(du, u)[..., np.newaxis])
                    else:
                        du = np.zeros(dx1.shape)
                else:
                    dv = np.zeros(dx1.shape)
                    du = np.zeros(dx1.shape)

                delta_rn = z==i and m==0
                delta_qn = z==i and m==1
                delta_fn = z==i and m==2


                if i > 0:
                    sq = np.sin(q)[..., np.newaxis]
                    cq = np.cos(q)[..., np.newaxis]

                    dn = vec_crosses(dv, u) + vec_crosses(v, du)
                    dn = 1/nn[..., np.newaxis]*(dn - n*vec_dots(dn, n)[..., np.newaxis])
                    dR2 = (
                            (vec_outer(dn, n) + vec_outer(n, dn))*(1-cq)[..., np.newaxis]
                            - vec_tdot(e3, dn)*sq[..., np.newaxis]
                    )
                    if delta_qn:
                        # component that only gets subtracted if m==1
                        dR2 -= (i3 - vec_outer(n, n))*sq[..., np.newaxis] + vec_tdot(e3, n)*cq[..., np.newaxis]

                    if i > 1:
                        sf = np.sin(f)[..., np.newaxis]
                        cf = np.cos(f)[..., np.newaxis]
                        dR1 = (
                                (vec_outer(dv, v) + vec_outer(v, dv)) * (1 - cf)[..., np.newaxis]
                                - vec_tdot(e3, dv)*sf[..., np.newaxis]
                        )
                        if delta_fn:
                            dR1 -= (i3 - vec_outer(v, v))*sf[..., np.newaxis] + vec_tdot(e3, v) * cf[..., np.newaxis]

                        dQ = np.matmul(dR1, R2) + np.matmul(R1, dR2)
                    elif i == 1:
                        if R1 is None:
                            dQ = dR2
                        else:
                            dQ = np.matmul(R1, dR2)

                dvr = (v if delta_rn else np.zeros(v.shape))
                if i > 0:
                    dQr = vec_tdot(dQ, r*v)
                    Qdr = vec_tdot(Q, r*dv + dvr)
                    d = dx1 + dQr + Qdr
                    derivs[zorks, z, m, i+1] = d
                else:
                    derivs[zorks, z, m, i+1] = dx1 + dvr

    def convert_many(self,
                     coordlist,
                     ordering=None, origins=None, axes=None, use_rad=True,
                     return_derivs = False,
                     **kw
                     ):
        """Expects to get a list of configurations
        These will look like:
            [
                [dist, angle, dihedral]
                ...
            ]
        and ordering will be
            [
                [pos, point, line, plane]
                ...
            ]
        **For efficiency it is assumed that all configurations have the same length**

        :param coordlist:
        :type coordlist:
        :param origins:
        :type origins:
        :param axes:
        :type axes:
        :param use_rad:
        :type use_rad:
        :param kw:
        :type kw:
        :param ordering:
        :type ordering:
        :param return_derivs:
        :type return_derivs:
        :return:
        :rtype:
        """
        # make sure we have the ordering stuff in hand
        if ordering is None:
           ordering, coordlist = self.default_ordering(coordlist)
        else:
            ordering = np.array(ordering)
        coordlist = np.asarray(coordlist)


        if np.min(ordering) > 0:
            ordering = ordering - 1
        dim_diff = coordlist.ndim - ordering.ndim
        if dim_diff > 0:
            missing = coordlist.shape[:dim_diff]
            ordering = np.broadcast_to(ordering, missing + ordering.shape )

        if ordering.shape[-1] == 4:
            atom_ordering = ordering[:, :, 0]
            ordering = ordering[:, 1:, 1:]
        else:
            atom_ordering = None

        sysnum = len(coordlist)
        coordnum = len(coordlist[0])
        total_points = np.empty((sysnum, coordnum+1, 3))
        if return_derivs:
            derivs = np.zeros((sysnum, coordnum, 3, coordnum + 1, 3))

        # gotta build the first three points by hand but everything else can be constructed iteratively

        # first we put the origin whereever the origins are specified
        if origins is None:
            origins = [0, 0, 0]
        if not isinstance(origins, np.ndarray):
            origins = np.array(origins)
        if len(origins.shape) < 2:
            origins = np.broadcast_to(origins, (sysnum, 3))
        total_points[:, 0] = origins

        # set up the next points by just setting them along the x-axis by default
        if axes is None:
            axes = [1, 0, 0]
        if not isinstance(axes, np.ndarray):
            axes = np.array(axes)
        if axes.ndim == 1:
            axes = np.array([axes, [0, 1, 0]])#np.concatenate((np.random.uniform(low=.5, high=1, size=(2,)), np.zeros((1,)) ))])
        if axes.ndim == 2:
            axes = np.broadcast_to(axes[np.newaxis], (sysnum, 2, 3))
        x_axes = vec_normalize(axes[:, 0])

        dists = coordlist[:, 0, 0]
        ref_points_1 = np.reshape(dists, (sysnum, 1)) * x_axes
        ref_points_1 += origins
        total_points[:, 1] = ref_points_1


        if return_derivs:
            i = 0
            r = dists
            q = None
            f = None
            ia = np.zeros((len(dists),)).astype(int)
            ib = None
            ic = None
            R1 = None
            R2 = None
            v = axes[:, 0]
            u = None
            n = None
            self._fill_deriv(i, derivs, r, q, f, ia, ib, ic, v, u, n, R1, R2)

         # iteratively build the rest of the coords with one special cases for n=2
        for i in range(1, coordnum):
            # Get the distances away
            # raise Exception(coordlist[:, i, [0, 2, 4]])
            ref_coords1 = ordering[:, i, 0] # reference atom numbers for first coordinate
            refs1 = total_points[np.arange(sysnum), ref_coords1.astype(int)] # get the actual reference coordinates
            dists = np.reshape(coordlist[:, i, 0], (sysnum, 1)) # pull the requisite distances

            ref_coords2 = ordering[:, i, 1] # reference atom numbers for second coordinate
            refs2 = total_points[np.arange(sysnum), ref_coords2.astype(int)] # get the actual reference coordinates for the angle
            angle = coordlist[:, i, 1] # pull the requisite angle values
            if not use_rad:
                angle = np.deg2rad(angle)

            if i == 1:
                refs3 = None
                dihed = None
                ref_coords3 = None
            else:
                ref_coords3 = ordering[:, i, 2] # reference atom numbers for dihedral ref coordinate
                refs3 = total_points[np.arange(sysnum), ref_coords3.astype(int)] # get the actual reference coordinates for the dihed
                dihed = coordlist[:, i, 2] # pull proper dihedral values
                if not use_rad:
                    dihed = np.deg2rad(dihed)

            ref_points, comps = self.build_next_points(refs1, dists, refs2, angle, refs3, dihed,
                                                ref_axis=axes[:, 1],
                                                return_comps = return_derivs
                                                ) # iteratively build z-mat
            if return_derivs:
                self._fill_deriv(i, derivs, dists, angle, dihed, ref_coords1, ref_coords2, ref_coords3, *comps)

            total_points[:, i+1] = ref_points

        if atom_ordering is not None:
            rev_ord = np.argsort(atom_ordering, axis=1)
            total_points = total_points[np.arange(len(atom_ordering))[:, np.newaxis], rev_ord]

        converter_opts = dict(use_rad=use_rad, ordering=ordering)
        if return_derivs:
            converter_opts['derivs'] = derivs
        return total_points, converter_opts

    def convert(self, coords, **kw):
        """dipatches to convert_many but only pulls the first"""
        total_points, opts = self.convert_many(coords[np.newaxis], **kw)
        return total_points[0], opts

__converters__ = [ ZMatrixToCartesianConverter() ]