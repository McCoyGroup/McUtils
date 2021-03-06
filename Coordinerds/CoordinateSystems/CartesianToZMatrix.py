from .CoordinateSystemConverter import CoordinateSystemConverter
from .CommonCoordinateSystems import CartesianCoordinateSystem, ZMatrixCoordinateSystem
from ...Numputils import vec_norms, vec_angles, pts_dihedrals, dist_deriv, angle_deriv, dihed_deriv
import numpy as np
# this import gets bound at load time, so unfortunately PyCharm can't know just yet
# what properties its class will have and will try to claim that the files don't exist

class CartesianToZMatrixConverter(CoordinateSystemConverter):
    """A converter class for going from Cartesian coordinates to ZMatrix coordinates

    """

    @property
    def types(self):
        return (CartesianCoordinateSystem, ZMatrixCoordinateSystem)

    def canonicalize_order_list(self, ncoords, order_list):
        """Normalizes the way the ZMatrix coordinates are built out

        :param ncoords:
        :type ncoords:
        :param order_list: the basic ordering to apply for the
        :type order_list: iterable or None
        :return:
        :rtype: iterator of int triples
        """
        if order_list is None:
            normalized_list = np.array( (
                   np.arange(ncoords),
                   np.arange(-1, ncoords-1),
                   np.arange(-2, ncoords-2),
                   np.arange(-3, ncoords-3),
                ) ).T
        else:
            normalized_list = [None] * len(order_list)
            for i, el in enumerate(order_list):
                if isinstance(el, int):
                    spec = (
                        el,
                        normalized_list[i-1][0] if i > 0 else -1,
                        normalized_list[i-2][0] if i > 1 else -1,
                        normalized_list[i-3][0] if i > 2 else -1
                    )
                else:
                    spec = tuple(el)
                    # if len(spec) < 4:
                    #     spec = (i,) + spec + (
                    #     normalized_list[i-1][0] if i > 0 else -1,
                    #     normalized_list[i-2][0] if i > 1 else -1,
                    #     normalized_list[i-3][0] if i > 2 else -1
                    # )
                    # spec = spec[:4]
                    if len(spec) < 4:
                        raise ValueError(
                            "Z-matrix conversion spec {} not long enough. Expected ({}, {}, {}, {})".format(
                                el,
                                "atomNum", "distAtomNum", "angleAtomNum", "dihedAtomNum"
                            ))

                normalized_list[i] = spec
        return np.asarray(normalized_list, dtype=np.int8)

    @staticmethod
    def get_dists(points, centers):
        return vec_norms(centers-points)
    @staticmethod
    def get_angles(lefts, centers, rights):
        # need to look up again what the convention is for which atom is the central one...
        v1s = centers-lefts
        v2s = centers-rights
        return vec_angles(v1s, v2s)[0]
    @staticmethod
    def get_diheds(points, centers, seconds, thirds):
        return pts_dihedrals(points, centers, seconds, thirds)

    def convert_many(self, coords, ordering=None, use_rad=True, return_derivs=False, **kw):
        """
        We'll implement this by having the ordering arg wrap around in coords?
        """
        if ordering is None:
            ordering = range(len(coords[0]))
        base_shape = coords.shape
        new_coords = np.reshape(coords, (np.product(base_shape[:-1]),) + base_shape[-1:])
        new_coords, ops = self.convert(new_coords, ordering=ordering, use_rad=use_rad, return_derivs=return_derivs)
        single_coord_shape = (base_shape[-2]-1, new_coords.shape[-1])
        new_shape = base_shape[:-2] + single_coord_shape
        new_coords = np.reshape(new_coords, new_shape)
        if return_derivs:
            ders = ops['derivs']
            ders_shape = coords.shape + single_coord_shape
            ders = ders.reshape(ders_shape)
            ops['derivs'] = ders
        return new_coords, ops

    def convert(self, coords, ordering=None, use_rad=True, return_derivs=False, **kw):
        """The ordering should be specified like:

        [
            [n1],
            [n2, n1]
            [n3, n1/n2, n1/n2]
            [n4, n1/n2/n3, n1/n2/n3, n1/n2/n3]
            [n5, ...]
            ...
        ]

        :param coords:    array of cartesian coordinates
        :type coords:     np.ndarray
        :param use_rad:   whether to user radians or not
        :type use_rad:    bool
        :param ordering:  optional ordering parameter for the z-matrix
        :type ordering:   None or tuple of ints or tuple of tuple of ints
        :param kw:        ignored key-word arguments
        :type kw:
        :return: z-matrix coords
        :rtype: np.ndarray
        """
        ncoords = len(coords)
        orig_ol = self.canonicalize_order_list(ncoords, ordering)
        ol = orig_ol
        nol = len(ol)

        multiconfig = nol < ncoords
        if multiconfig:
            fsteps = ncoords / nol
            steps = int(fsteps)
            if steps != fsteps:
                raise ValueError(
                    "{}: Number of coordinates {} and number of specifed elements {} misaligned".format(
                        type(self),
                        ncoords,
                        nol
                    )
                )
            # broadcasts a single order spec to be a multiple order spec
            ol = np.reshape(
                np.broadcast_to(ol, (steps, nol, 4)) +
                np.reshape(np.arange(0, ncoords, nol), (steps, 1, 1)),
                (ncoords, 4)
            )
            mc_ol = ol.copy()

        # we define an order map that we'll index into to get the new indices for a
        # given coordinate
        om = 1+np.argsort(ol[:, 0])

        # need to check against the cases of like 1, 2, 3 atom molecules
        # annoying but not hard
        if return_derivs:
            derivs = np.zeros(coords.shape + (nol-1, 3))
        if not multiconfig:
            ix = ol[1:, 0]
            jx = ol[1:, 1]
            dists = self.get_dists(
                coords[ix],
                coords[jx]
            )
            if return_derivs:
                dist_derivs = dist_deriv(coords,ix, jx)
                drang = np.arange(len(ix))
                derivs[ix, :, drang, 0] = dist_derivs[0]
                derivs[jx, :, drang, 0] = dist_derivs[1]
            if len(ol) > 2:
                ix = ol[2:, 0]
                jx = ol[2:, 1]
                kx = ol[2:, 2]
                angles = np.concatenate( (
                    [0], self.get_angles(coords[ix], coords[jx], coords[kx])
                ) )
                if not use_rad:
                    angles = np.rad2deg(angles)
                if return_derivs:
                    angle_derivs = angle_deriv(coords, jx, ix, kx)
                    drang = 1+np.arange(len(ix))
                    derivs[jx, :, drang, 1] = angle_derivs[0]
                    derivs[ix, :, drang, 1] = angle_derivs[1]
                    derivs[kx, :, drang, 1] = angle_derivs[2]
            else:
                angles = np.array([0.])
            if len(ol) > 3:
                ix = ol[3:, 0]
                jx = ol[3:, 1]
                kx = ol[3:, 2]
                lx = ol[3:, 3]
                diheds = np.concatenate( (
                    [0, 0],
                    self.get_diheds(coords[ix], coords[jx], coords[kx], coords[lx])
                ) )
                if not use_rad:
                    diheds = np.rad2deg(diheds)
                if return_derivs:
                    dihed_derivs = -dihed_deriv(coords, ix, jx, kx, lx)
                    drang = 2+np.arange(len(ix))
                    derivs[ix, :, drang, 2] = dihed_derivs[0]
                    derivs[jx, :, drang, 2] = dihed_derivs[1]
                    derivs[kx, :, drang, 2] = dihed_derivs[2]
                    derivs[lx, :, drang, 2] = dihed_derivs[3]
            else:
                diheds = np.array([0, 0])
            ol = ol[1:]

        else: # multiconfig

            # we do all of this stuff with masking operations in the multiconfiguration cases
            mask = np.repeat(True, ncoords)
            mask[np.arange(0, ncoords, nol)] = False
            ix = ol[mask, 0]
            jx = ol[mask, 1]
            dists = self.get_dists(coords[ix], coords[jx])
            if return_derivs:
                dist_derivs = dist_deriv(coords, ix, jx)
                drang = np.arange(nol-1)
                nreps = int(len(ix)/(nol-1))
                drang = np.broadcast_to(drang[np.newaxis], (nreps,) + drang.shape).flatten()
                derivs[ix, :, drang, 0] = dist_derivs[0]
                derivs[jx, :, drang, 0] = dist_derivs[1]

            if nol>2:
                # set up the mask to drop all of the first bits
                mask[np.arange(1, ncoords, nol)] = False
                ix = ol[mask, 0]
                jx = ol[mask, 1]
                kx = ol[mask, 2]
                angles = self.get_angles(coords[ix], coords[jx], coords[kx])
                angles = np.append(angles, np.zeros(steps))
                insert_pos = np.arange(0, ncoords-1*steps-1, nol-2)
                angles = np.insert(angles, insert_pos, 0)
                angles = angles[:ncoords-steps]
                if not use_rad:
                    angles = np.rad2deg(angles)
                if return_derivs:
                    # we might need to mess with the masks akin to the insert call...
                    angle_derivs = angle_deriv(coords, jx, ix, kx)
                    drang = 1+np.arange(nol-2)
                    nreps = int(len(ix)/(nol-2))
                    drang = np.broadcast_to(drang[np.newaxis], (nreps,) + drang.shape).flatten()
                    derivs[jx, :, drang, 1] = angle_derivs[0]
                    derivs[ix, :, drang, 1] = angle_derivs[1]
                    derivs[kx, :, drang, 1] = angle_derivs[2]
            else:
                angles = np.zeros(ncoords-steps)

            if nol > 3:
                # set up mask to drop all of the second atom bits (wtf it means 'second')
                mask[np.arange(2, ncoords, nol)] = False
                ix = ol[mask, 0]
                jx = ol[mask, 1]
                kx = ol[mask, 2]
                lx = ol[mask, 3]
                diheds = self.get_diheds(coords[ix], coords[jx], coords[kx], coords[lx])
                # pad diheds to be the size of ncoords
                diheds = np.append(diheds, np.zeros(2*steps))

                # insert zeros where undefined
                diheds = np.insert(diheds, np.repeat(np.arange(0, ncoords-2*steps-1, nol-3), 2), 0)
                # take only as many as actually used
                diheds = diheds[:ncoords-steps]
                if not use_rad:
                    diheds = np.rad2deg(diheds)
                if return_derivs:
                    dihed_derivs = -dihed_deriv(coords, ix, jx, kx, lx)
                    drang = 2+np.arange(nol-3)
                    nreps = int(len(ix)/(nol-3))
                    drang = np.broadcast_to(drang[np.newaxis], (nreps,) + drang.shape).flatten()
                    derivs[ix, :, drang, 2] = dihed_derivs[0]
                    derivs[jx, :, drang, 2] = dihed_derivs[1]
                    derivs[kx, :, drang, 2] = dihed_derivs[2]
                    derivs[lx, :, drang, 2] = dihed_derivs[3]
            else:
                diheds = np.zeros(ncoords-steps)

            # after the np.insert calls we have the right number of final elements, but too many
            # ol and om elements and they're generally too large
            # so we need to shift them down and mask out the elements we don't want
            mask = np.repeat(True, ncoords)
            mask[np.arange(0, ncoords, nol)] = False
            ol = np.reshape(ol[mask], (steps, nol-1, 4))-np.reshape(np.arange(steps), (steps, 1, 1))
            ol = np.reshape(ol, (ncoords-steps, 4))
            om = np.reshape(om[mask], (steps, nol-1))-nol*np.reshape(np.arange(steps), (steps, 1))-1
            om = np.reshape(om, (ncoords-steps,))

        final_coords = np.array(
            [
                dists, angles, diheds
            ]
        ).T

        if multiconfig:
            # figure out what to use for the axes
            origins = coords[mc_ol[1::nol,  1]]
            x_axes  = coords[mc_ol[1::nol,  0]] - origins # the first displacement vector
            y_axes  = coords[mc_ol[2::nol,  0]] - origins # the second displacement vector (just defines the x-y plane, not the real y-axis)
            axes = np.array([x_axes, y_axes]).transpose((1, 0, 2))

            # raise Exception([x_axes, y_axes])
            # print(origins.shape, axes.shape)
            # print(axes)

        else:
            origins = coords[ol[0, 1]]
            axes = np.array([coords[ol[0, 0]] - origins, coords[ol[1, 0]] - origins])

        ol = orig_ol
        om = om - 1
        ordering = np.array(
                [
                    np.arange(len(ol)), om[ol[:, 1]], om[ol[:, 2]], om[ol[:, 3]]
                ]
            ).T

        opts = dict(use_rad=use_rad, ordering=ordering, origins=origins, axes=axes)

        # if we're returning derivs, we also need to make sure that they're ordered the same way the other data is...
        if return_derivs:
            opts['derivs'] = derivs

        return final_coords, opts

__converters__ = [ CartesianToZMatrixConverter() ]