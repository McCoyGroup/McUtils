"""
Module that provides a FiniteDifferenceDerivative class that does finite-difference derivatives
"""

from .FiniteDifferenceFunction import FiniteDifferenceFunction
import numpy as np, itertools as it, scipy.sparse as sparse

__all__ = [
    'FiniteDifferenceDerivative'
]


class FiniteDifferenceDerivative:
    """
    Provides derivatives for a function (scalar or vector valued).
    Can be indexed into or the entire tensor of derivatives may be requested.
    The potential for optimization undoubtedly exists, but the idea is to provide as _simple_ an interface as possible.
    Robustification needs to be done, but is currently used in `CoordinateSystem.jacobian` to good effect.
    """
    def __init__(self, f, function_shape=(0, 0), **fd_opts):
        """
        :param f: the function we would like to take derivatives of
        :type f: FunctionSpec | callable
        :param function_shape: the shape of the function we'd like to take the derivatives of
        :type function_shape: Iterable[Iterable[int] | int] | None
        :param fd_opts: the options to pass to the finite difference function
        :type fd_opts:
        """
        if not isinstance(f, FunctionSpec):
            f = FunctionSpec(f, *function_shape)
        self.f = f
        self._fd_opts = fd_opts

    def __call__(self, *args, **opts):
        return self.derivatives(*args, **opts)

    def derivatives(self, center,
                    displacement_function=None,
                    prep=None,
                    lazy=None,
                    mesh_spacing=None,
                    **fd_opts
                    ):
        """
        Generates a differencer object that can be used to get derivs however your little heart desires

        :param center: the center point around which to generate differences
        :type center: np.ndarray
        :param displacement_function:
        :type displacement_function:
        :param mesh_spacing:
        :type mesh_spacing:
        :param prep:
        :type prep:
        :param fd_opts:
        :type fd_opts:
        :return:
        :rtype:
        """

        f = self.f
        fd_opts = dict(self._fd_opts, **fd_opts)
        for k, v, d in zip(
                ("displacement_function", "prep", "lazy", "mesh_spacing"),
                (displacement_function, prep, lazy, mesh_spacing),
                (None, None, False, .001)
        ):
            if v is not None:
                fd_opts[k] = v
            elif k not in fd_opts:
                fd_opts[k] = d

        return DerivativeGenerator(
            f,
            center,
            **fd_opts
        )

class FunctionSpec:
    """
    Defines a general spec that specifies a function, what it takes as coordinate inputs, and what the dimensions of what it outputs
    """

    def __init__(self, f, input_shape, output_shape):
        """

        :param f:
        :type f:
        :param input_shape: the shape of the array that should be passed in
        :type input_shape:
        :param output_shape:
        :type output_shape:
        """
        self.f = f
        self.in_shape = input_shape
        self.output_shape = output_shape
    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)

class DerivativeGenerator:
    """A that generates specified derivatives, currently by FD but can be generalized out to do it other ways

    The lower-level class that takes the entire high-level spec and converts it into derivatives.
    Allows indexing for memory efficiency
    """
    def __init__(self,
                 f_spec,
                 center,
                 displacement_function = None,
                 prep = None,
                 lazy = False,
                 mesh_spacing = .001,
                 cache_evaluations = True,
                 **fd_opts
                 ):
        """

        :param f_spec: The function to use when evaluating at the various displacements
        :type f_spec: FunctionSpec | function
        :param center: The position to evaluate the derivatives at
        :type center: np.ndarray
        :param displacement_function: The function to generate displacements
        :type displacement_function: FunctionSpec | function | None
        :param prep:
        :type prep: function | None
        :param mesh_spacing:
        :type mesh_spacing: float
        :param symmetric:
        :type symmetric:
        :param cache_evaluations: whether or not to cache function evaluations for reuse in other derivatives
        :type cache_evaluations: bool
        :param fd_opts:
        :type fd_opts:
        """

        # set up the coordinate parameters
        if isinstance(center, (int, float, np.integer, np.float)):
            center = [center]
        center = np.asarray(center)

        input_shape = f_spec.in_shape if isinstance(f_spec, FunctionSpec) else 0
        # determine if center is multiple configurations or just one
        input_dims = (0 if isinstance(input_shape, (int, np.integer)) else len(input_shape))
        multiconfig = len(center.shape) > input_dims
        if not multiconfig:
            coords = np.array([center])
        else:
            coords = np.asarray(center)
            if len(coords.shape) == 1:
                coords = coords.reshape(coords.shape + (1,))
        if input_dims == 0:
            input_dims = 1

        # determine up the data shapes
        configs_dims = coords.shape[:-input_dims]
        coord_shape = tuple(coords.shape[-input_dims:])
        # coord_shape = tuple(shape if isinstance(input_shape, (int, np.integer)) else input_shape)

        # figure out how many dimensions we will have flattened for a multiconfiguration state
        flattened_dims = None
        if multiconfig:
            flattened_dims = configs_dims
            num_flattened = np.product(flattened_dims)
            # I think by being smarter I could have avoided this reshape and avoided a bunch of hassle
            coords = coords.reshape((num_flattened, ) + coord_shape)

        # configure the function for handling displacements
        if displacement_function is None:
            displacement_function = lambda c,a:a

        # define a function to prep the system
        if prep is None:
            prep = lambda c, a, b: (a, b)

        self.f = f_spec
        self.config_shape = configs_dims
        self.coord_shape = coord_shape

        self.center = coords
        self.multiconfig = multiconfig
        self.prep = prep

        self.lazy = lazy

        self.fd_opts = fd_opts
        self._flattend_dims = flattened_dims
        self.displacement_function = displacement_function
        self.mesh_spacing = mesh_spacing
        self._fdfs = {}

        self.cache_evaluations = cache_evaluations
        self._cache = {}

    def _get_fdf(self, ci, mesh_spacing):
        # create the different types of finite differences we'll compute for the different coordinates of interest
        dorder = self._dorder(ci)

        try:
            fdf = self._fdfs[(dorder, mesh_spacing)]
        except KeyError:
            fdf = FiniteDifferenceFunction.regular_difference(
                dorder,
                end_point_accuracy=0,
                only_core=False,
                only_center=True,
                contract=True,
                mesh_spacing = mesh_spacing,
                **self.fd_opts
            )
            self._fdfs[(dorder, mesh_spacing)] = fdf

        stencil_widths = tuple(len(cf[1]) if cf is not None else cf for cf in fdf.weights)
        stencil_shapes = tuple(w[1] if w is not None else w for w in fdf.widths)
        finite_difference = fdf#.get_FDF(shape = stencil_widths)

        return stencil_widths, stencil_shapes, finite_difference, dorder

    def _coord_index(self, coord):
        """Converts the coordinate spec into a linear index

        :param coord:
        :type coord:
        :return:
        :rtype:
        """
        # gotta re-linearize coord so we can use it to index into like fdfs and stuff...
        if coord.ndim == 1:
            raveled = np.ravel_multi_index(coord, self.coord_shape)
        else:
            raveled = [ np.ravel_multi_index(c, self.coord_shape) for c in coord ]
        return raveled

    def _dorder(self, raveled):
        """Computes the derivative order requested from the coordinate indices requested

        :param raveled:
        :type raveled:
        :return:
        :rtype:
        """
        unique, counts = np.unique(raveled, return_counts=True)
        pairs = np.array([unique, counts]).T
        sorting = np.argsort(pairs[:, 0])
        orders = pairs[sorting, 1]
        return tuple(orders)

    def get_displacement(self, coord, mesh_spacing = None):
        """
        Computes the displacement for the passed mesh spacing

        :param coord:
        :type coord:
        :param mesh_spacing:
        :type mesh_spacing:
        :return:
        :rtype:
        """
        if mesh_spacing is None:
            mesh_spacing = self.mesh_spacing
        displacement = self.displacement_function(coord, mesh_spacing)
        if isinstance(displacement, (float, np.float)):
            displacement = np.full(self.coord_shape, displacement)
        elif displacement.shape == self.coord_shape[-1:]:
            displacement = np.broadcast_to(displacement, self.coord_shape)

        return displacement

    def _get_displaced_coords(self, coord, stencil_widths, stencil_shapes, use_sparse = False):
        """
        Provides enough displacements of along `coord` to satisfy `stencil_widths` and `stencil_shapes`
        Does this by generating a big tensor of zeros, assigning parts of this for each displacement, then adding that

        :param coord:
        :type coord:
        :param stencil_widths:
        :type stencil_widths:
        :param stencil_shapes:
        :type stencil_shapes:
        :return:
        :rtype:
        """

        coords = self.center
        displacement = self.get_displacement(coord)

        # not too worried about looping over coordinates since the number of loops will be like max in the small hundreds
        num_displacements = np.product(stencil_widths)
        displacement_shape = (num_displacements, ) + displacement.shape

        if use_sparse:
            displacements = sparse.lil_matrix(displacement_shape)
        else:
            displacements = np.zeros(displacement_shape) # fuck ton of zeros
        base_roll = tuple(np.arange(len(stencil_widths)))

        coord = np.unique(coord, axis=0)

        for i, sc in enumerate(zip(stencil_shapes, coord)):
            stencil_shape, c = sc
            # coord can be like ((1, 1), (1, 2)) or ((0,), (1,)) in which case we have a 2D derivative
            # creates single displacement matrix
            # it can also just be like ((0,)) in which case we're working in 1D
            ctup = tuple(c)

            disp = displacement[ctup]

            steps = np.arange(-(stencil_shape[0]-1), stencil_shape[1]+1)
            disp = disp * steps
            full_disp = np.reshape(disp, disp.shape + (1,) * (len(stencil_widths) - disp.ndim))
            roll = np.roll(base_roll, -2+i) # why the -2???
            full_disp = full_disp.transpose(roll)
            to_set = np.broadcast_to(full_disp, stencil_widths).flatten()

            # in dimension 1 we want to have this repeat over the slowest moving indices, then the ones after those
            # then after those, etc.
            idx = (...,) + ctup
            displacements[idx] = to_set

        # then we broadcast *this* up to the total number of walkers we have
        full_target_shape = self.config_shape + displacement_shape
        coords_expanded = coords.reshape(
            self.config_shape
            + (1,) * (len(displacement_shape) - len(self.coord_shape))
            + self.coord_shape
        )
        displacements = displacements.reshape(
            (1,) * len(self.config_shape)
            + displacement_shape
        )
        displaced_coords = (
            np.broadcast_to(coords_expanded, full_target_shape) +
            np.broadcast_to(displacements, full_target_shape)
        )

        disp_spec = (tuple(tuple(x for x in c) for c in coord), displacement_shape)

        return disp_spec, displacements, displaced_coords

    def _get_fd_data(self, specs):
        """
        Takes the specs and returns a generator that will create the appropriate derivatives along each coordinate
        I should add an optimization that allows displacements along single coordinates to happen fast...

        :param specs:
        :type specs:
        :param stencil_widths:
        :type stencil_widths:
        :param stencil_shapes:
        :type stencil_shapes:
        :return:
        :rtype:
        """

        for spec in specs: # dumb for now but allows me to pick some optimal ordering in the future
            ci = self._coord_index(spec)
            fd_data = self._get_fdf(ci, self.mesh_spacing)
            disp_data = self._get_displaced_coords(spec, fd_data[0], fd_data[1])

            yield spec, disp_data, fd_data

    @staticmethod
    def _get_diff(c, disp):
        """Gets the mesh spacing along coordinate c from the displaced coordinates

        :param c:
        :type c:
        :param disp:
        :type disp:
        :return:
        :rtype:
        """

        # diffs = np.abs(np.diff()) # why do it like this...?????
        # return np.sort(diffs)[-1]  # get the only diff > 0 (assumes we have a regular grid)
        subgrid = sorted(np.unique(disp[(...,) + tuple(c)]))
        return abs(subgrid[1] - subgrid[0])

    def _get_single_deriv(self, spec, disp_data, fd_data, return_coords):

        if self.cache_evaluations:
            # we assume that evaluating the hash of the array will be faster
            # than evaluating f itself
            # this might not aways be the case,
            # but if it fails to be so that's likely not a cause for concern because it
            # means the overall process is already fast
            cache_key = disp_data[0]
            cached = cache_key in self._cache
            # if uncached:
            #     if not hasattr(self, "_cache_fails"):
            #         self._cache_fails = 0
            #     else:
            #         self._cache_fails += 1
            #     print(spec, disp_data[0], disp_data[1].shape)
            #     if self._cache_fails > 20:
            #         raise Exception("wat")
        else:
            cache_key = None
            cached = False


        f = self.f
        disp_spec, displacements, displaced_coords = disp_data
        stencil_widths, stencil_shapes, finite_difference, dorder = fd_data

            # TODO: sit down and add comments to this compact implementation...

        if cached:
            (disp, fvals) = self._cache[cache_key]
        else:
            config_shape = self.config_shape
            cdim = len(config_shape)
            roll = [cdim] + [a for a in np.arange(displaced_coords.ndim) if a != cdim]
            dcoords = displaced_coords.transpose(roll)
            function_values = f(dcoords)
            unroll = tuple(np.arange(cdim) + 1) + (0,) + tuple(np.arange(cdim+1, function_values.ndim))
            function_values = function_values.transpose(unroll)
            disp, fvals = self.prep(spec, displacements, function_values)

            # TODO: handle stuff like dipoles where we have an x, y, z component each of which should be handled separately...
            #       this might actually be handled naturally, though? I'm actually pretty hopeful it will be...

            # we now need to reformat the fvals so that they respect the stencil_shapes
            # not sure where the extra 1 is coming from here...?
            # I think maybe from the transpose call...?
            # Actually no that just puts the displacement back in the right spot...
            #   seems that it comes out of the way the coordinates get fed in/come out...
            #   the tested stuff all has an extra '1' because of the way the displacement
            #   gets generated
            out_shape = fvals.shape[1+len(self.config_shape):]
            out_dim = 1 if isinstance(out_shape, (int, np.integer)) else len(out_shape)
            fvals_shape = self.config_shape + stencil_widths
            if out_dim > 0:
                fvals_shape = fvals_shape + fvals.shape[-out_dim:]
            fvals = fvals.reshape(fvals_shape)

        h = [self._get_diff(c, disp) for c in spec]

        derivs = finite_difference(fvals, axes=len(self.config_shape), mesh_spacing=h)

        if self.cache_evaluations and not cached:
            self._cache[cache_key] = (disp, fvals)

        if return_coords:
            return displaced_coords, derivs
        else:
            return derivs

    def _spec_derivs(self, specs, return_coords=False):
        """
        Computes a specific derivative
        The derivative is specified by repeating a coordinate the number of times we'd like its derivative:
            e.g. `[[0], [0]]` for $dx_1^2$ or `[[0], [N]]` for $dx_1dx_N$ if we have a function $f:R_N \rightarrow R$
                or `[[0, 1], [1, 0]]` for $dA_1_2dA_2_1$ if we have a function $f:(R_M, R_N) \rightarrow R$

        :param spec: the derivative to take as specified by the given indices
        :type spec: Iterable[Iterable[int]]
        :return:
        :rtype:
        """

        for spec, disp_data, fd_data in self._get_fd_data(specs):
            yield self._get_single_deriv(spec, disp_data, fd_data, return_coords)

    def _get_specs(self, order, pos = (), coordinates = None):
        """
        We compute the positions defined by the total order of the derivative as they would show up in the total tensor
        If a given block of derivatives is specified **[NOTE: I didn't finish this docstring and have no idea what it was supposed to say...]**

        :param order:
        :type order: int
        :param pos:
        :type pos: Iterable[int]
        :param coordinates:
        :type coordinates:
        :return:
        :rtype:
        """
        if coordinates is None:
            coordinates = np.arange(np.product(self.coord_shape))
        elif not isinstance(coordinates[0], (int, np.integer)):
            coordinates = self._fidx(coordinates)

        pos = [slice(None, None, None) if a is None else a for a in pos]
        if len(pos) == order and all(isinstance(i, (int, np.integer)) for i in pos):
            # we're just asking for a single derivative (I think?)
            # basically when we have a derivative of order `n` and have something like `[i_1, i_2, ..., i_n]`
            # as the `pos`
            specs = [tuple(coordinates[c] for c in pos)]
        else:
            # we need to broadcast our specs
            sub_specs = [ tuple(coordinates[a]) if not isinstance(a, (int, np.integer)) else (coordinates[a],) for a in pos]
            sub_specs = sub_specs + [coordinates for i in range(order - len(pos))]
            unique = set()
            def test(p):
                # assumes derivative tensors are totally symmetric (good assumption in science)
                # filters out permutations by whether or not they are equivalent under sorting
                s = tuple(sorted(p))
                if s in unique:
                    return False
                else:
                    unique.add(s)
                    return True
            # we take the product space of the provided specs, since each spec targets a specific dimension
            # this is basically numpy broadcasting
            # then we filter by symmetry
            specs = [p for p in it.product(*sub_specs) if test(p)]

        return [self._idx(s) for s in specs], specs

    def compute_derivatives(self, order, pos=(), coordinates=None, lazy=None):
        """
        Computes the derivatives up to `order` filtered by `pos` over the `coordinates`

        :param order: the maximum total order of the derivatives to calculate
        :type order: int | Iterable[int]
        :param pos: the positions to filter on
        :type pos:
        :param coordinates: the coordinates to compute the tensor of derivatives over
        :type coordinates: Iterable[int] | None
        :param lazy: whether or not to return a generator
        :type lazy: bool | None
        :return:
        :rtype:
        """

        if isinstance(order, (int, np.integer)):
            single = True
            order = [order]
        else:
            single = False

        res = [None]*len(order)
        def lazy_derivs(ders):
            for d in ders:
                yield d
        for which, o in enumerate(order):
            specs, raw = self._get_specs(o, pos, coordinates)
            lazy = self.lazy if lazy is None else lazy
            derivs = self._spec_derivs(specs)
            if lazy:
                res[which] = lazy_derivs(derivs)
            else:
                res[which] = list(derivs)
        if single:
            res = res[0]
        return res

    def derivative_tensor(self, order, pos=(), coordinates=None):
        """
        Computes a given derivative tensor

        :param order:
        :type order: int | Iterable[int]
        :param pos:
        :type pos:
        :param coordinates:
        :type coordinates:
        :return:
        :rtype:
        """

        if isinstance(order, (int, np.integer)):
            single = True
            order = [order]
        else:
            single = False

        res = [None]*len(order)
        for which, o in enumerate(order):
            pos = [slice(None, None, None) if a is None else a for a in pos]
            if coordinates is None:
                coordinates = np.arange(np.product(self.coord_shape))
            elif not isinstance(coordinates[0], (int, np.integer)):
                coordinates = self._fidx(coordinates)
            sub_specs = [coordinates[a] if not isinstance(a, (int, np.integer)) else (coordinates[a],) for a in pos]
            sub_specs = sub_specs + [coordinates for i in range(o - len(pos))]
            specs, raw = self._get_specs(o, pos, coordinates)
            derivs = self._spec_derivs(specs)

            d_tensor = None
            # apply symmetry
            for s, d in zip(raw, derivs):
                if d_tensor is None:
                    d_tensor = np.ones(tuple(len(s) for s in sub_specs) + d.shape)

                for p in it.permutations(s, len(s)):
                    try:
                        d_tensor[p] = d
                    except IndexError:
                        pass

            res[which] = d_tensor

        if single:
            res = res[0]
        return res

    def _idx(self, c, coord_shape = None):
        if coord_shape is None:
            coord_shape = self.coord_shape
        return np.array(np.unravel_index(np.array(c), coord_shape)).T
    def _fidx(self, c, coord_shape = None):
        if coord_shape is None:
            coord_shape = self.coord_shape
        return np.ravel_multi_index(c, coord_shape)

    def __getitem__(self, item):
        """
        Returns a single derivative or block of derivatives, depending on how `item` is defined

        :param item: position spec
        :type item: int | tuple[int] | slice | tuple[int | slice]
        :return: derivs
        :rtype: float | np.ndarray
        """
        if isinstance(item, (int, np.integer)):
            item = (item,) # though the branches might differ...
        elif isinstance(item, slice):
            item = (item,)
        if any(not isinstance(i, (int, np.integer)) for i in item):
            return self.derivative_tensor(len(item), item)
        else:
            d = self.compute_derivatives(len(item), item, lazy=False)
            return d[0]

