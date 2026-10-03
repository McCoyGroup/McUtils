import collections, abc
import functools
import numpy as np
import itertools

from .. import Devutils as dev

# from scipy.optimize.linesearch import line_search_armijo
from . import VectorOps as vec_ops
from . import Misc as misc
from . import TransformationMatrices as tfs
from . import SetOps as set_ops

__all__ = [
    "iterative_step_minimize",
    "iterative_chain_minimize",
    "string_method_minimize",
    "scipy_minimize",
    "GradientDescentStepFinder",
    "NewtonStepFinder",
    "QuasiNewtonStepFinder",
    "ConjugateGradientStepFinder",
    "EigenvalueFollowingStepFinder",
    "NudgedElasticBandStepFinder",
    "StringMethodStepFinder",
    "InterpolatingReparametrizer",
    "jacobi_maximize",
    "LineSearchRotationGenerator",
    "GradientDescentRotationGenerator",
    "OperatorMatrixRotationGenerator",
    "displacement_localizing_rotation_generator",
    "polyfit_maxima",
    "polyfit_minima",
    "polyfit_critical_points",
    "peak_fit_maxiumum"
]
default_jacobian_step_finder = 'conjugate-gradient'
default_hessian_step_finder = 'newton'
def lookup_method_name(method):
    """
    **LLM Docstring**

    Map a step-finder method name to its class.

    :param method: the method name (e.g. `'newton'`, `'conjugate-gradient'`)
    :type method: str
    :return: the step-finder class, or `None` if the name is unknown
    :rtype: type | None
    """
    return {
        'conjugate-gradient':ConjugateGradientStepFinder,
        'newton':NewtonStepFinder,
        'quasi-newton':QuasiNewtonStepFinder,
        'gradient-descent':GradientDescentStepFinder,
        'eigenvalue-following':EigenvalueFollowingStepFinder,
        'eigenvector-following':EigenvalueFollowingStepFinder,
        'string':StringMethodStepFinder,
        'neb':NudgedElasticBandStepFinder
    }.get(method)
def get_step_finder(spec,
                    method=None,
                    jacobian=None,
                    hessian=None,
                    **extra_init):
    """
    **LLM Docstring**

    Resolve a step-finder specification into a ready-to-call step-finder instance.

    Accepts a bare function (plus `method`/`jacobian`/`hessian`), a spec dict, or an
    already-built step finder. A method name is looked up via `lookup_method_name`,
    defaulting to the Newton finder when a Hessian is available and the
    conjugate-gradient finder otherwise.

    :param spec: a function, spec dict, or existing step finder
    :type spec: Callable | dict | object
    :param method: the optimization method name or class
    :type method: str | type | None
    :param jacobian: the gradient function
    :type jacobian: Callable | None
    :param hessian: the Hessian function
    :type hessian: Callable | None
    :param extra_init: extra keyword arguments forwarded to the finder constructor
    :return: the step-finder instance
    :rtype: object
    """
    if not (isinstance(spec, dict) or hasattr(spec, 'supports_hessian')) and (
            jacobian is not None
            or method is not None
    ):
        spec = {
            'method':method,
            'func':spec,
            'jacobian':jacobian,
            'hessian':hessian
        }
    if isinstance(spec, dict):
        spec = spec.copy() # don't mutate user data
        method = spec.pop('method', method)
        func = spec.pop('func')
        if jacobian is None:
            jacobian = spec.pop('jacobian')
        else:
            jacobian = spec.pop('jacobian', jacobian)
        hessian = spec.pop('hessian', hessian)
        if method is None:
            if hessian is not None:
                method = default_hessian_step_finder
            else:
                method = default_jacobian_step_finder
        if isinstance(method, str):
            test_method = lookup_method_name(method)
            if test_method is None:
                raise ValueError(f"can't determine appropriate step finder for '{method}")
            method = test_method
        if hessian is not None and method.supports_hessian:
            spec = method(func, jacobian, hessian, **dict(spec, **extra_init))
        else:
            spec = method(func, jacobian, **dict(spec, **extra_init))
    return spec
oscillation_overlap_cutoff_min = 0.95
oscillation_overlap_cutoff_max = 1.05
def iterative_step_minimize_step(step_predictor,
                                 guess, mask, tol,
                                 orthogonal_projector, orthogonal_projection_generator,
                                 region_constraints, unitary, max_displacement, max_displacement_norm,
                                 generate_rotation, prev_steps, max_gradient_error, termination_function,
                                 is_climbing
                                 ):
    """
    **LLM Docstring**

    Take a single minimization step for the still-active members of a batch.

    Applies any orthogonal/unitary projector to the predicted step and gradient,
    caps the displacement, enforces region constraints, checks convergence (and any
    termination function), damps oscillating steps, and returns the accepted step
    together with the updated active mask.

    :param step_predictor: the step-finder producing `(step, gradient)`
    :type step_predictor: Callable
    :param guess: current parameters for the active members, shape `(batch, n)`
    :type guess: np.ndarray
    :param mask: indices of the active batch members
    :type mask: np.ndarray | tuple
    :param tol: gradient convergence tolerance
    :type tol: float
    :param orthogonal_projector: fixed projector applied to steps
    :type orthogonal_projector: np.ndarray | None
    :param orthogonal_projection_generator: per-guess projector generator
    :type orthogonal_projection_generator: Callable | None
    :param region_constraints: `(min, max)` bounds per coordinate
    :type region_constraints: np.ndarray | None
    :param unitary: constrain steps to the unit sphere
    :type unitary: bool
    :param max_displacement: cap on the max per-coordinate step
    :type max_displacement: float | None
    :param max_displacement_norm: cap on the step norm
    :type max_displacement_norm: float | None
    :param generate_rotation: also build the rotation for unitary steps (unsupported >3D)
    :type generate_rotation: bool
    :param prev_steps: recent steps, used for oscillation detection
    :type prev_steps: np.ndarray | None
    :param max_gradient_error: use the max-abs gradient (vs. its norm) as the error
    :type max_gradient_error: bool
    :param termination_function: optional early-termination predicate
    :type termination_function: Callable | None
    :param is_climbing: per-member climbing-image flags (for chain methods)
    :type is_climbing: np.ndarray | None
    :return: `(step, errors, new_mask, done)`
    :rtype: tuple
    """
    if unitary:
        projector = vec_ops.orthogonal_projection_matrix(guess.T)
        if orthogonal_projector is not None:
            projector = projector @ orthogonal_projector[np.newaxis]
        if orthogonal_projection_generator is not None:
            projector = projector @ orthogonal_projection_generator(guess)
    elif orthogonal_projector is not None:
        projector = orthogonal_projector[np.newaxis]
        if orthogonal_projection_generator is not None:
            projector = projector @ orthogonal_projection_generator(guess)
    elif orthogonal_projection_generator is not None:
        projector = orthogonal_projection_generator(guess)
    else:
        projector = None
    if is_climbing is None:
        step, grad = step_predictor(guess, mask, projector=projector)
    else:
        step, grad = step_predictor(guess, mask, projector=projector, is_climbing=is_climbing)
    if projector is not None:
        # just in case, will usually lead to non-convergence
        step = (step[..., np.newaxis, :] @ projector).reshape(step.shape)
        grad = (grad[..., np.newaxis, :] @ projector).reshape(step.shape)

    if max_displacement is not None:
        step_sizes = np.max(np.abs(step), axis=1)
        step *= (max_displacement / np.clip(
            step_sizes, max_displacement, None
        ))[:, np.newaxis]
    if max_displacement_norm is not None:
        step_sizes = np.linalg.norm(step, axis=1)
        step *= (max_displacement_norm / np.clip(
            step_sizes, max_displacement_norm, None
        ))[:, np.newaxis]
    if region_constraints is not None:
        #TODO: introduce this as a scaling
        max_step = region_constraints[np.newaxis, :, 1] - guess
        min_step = region_constraints[np.newaxis, :, 0] - guess
        step = np.clip(step, min_step, max_step)
    if isinstance(mask, tuple):
        mask = mask[0]

    if max_gradient_error:
        errs = np.max(np.abs(grad), axis=1)
    else:
        errs = np.linalg.norm(grad, axis=1)
    rem = np.arange(len(mask))
    done = np.where(errs < tol)[0]
    if len(done) > 0:  # easy check
        rem = np.delete(rem, done)
        mask = np.delete(mask, done)
        if len(mask) == 0:
            return step[:0], errs, np.array([], dtype=int), done
    if termination_function is not None:
        stopped = np.flatnonzero(termination_function(guess[rem], step[rem], mask))
        if len(stopped) > 0:
            done = np.concatenate([done, rem[stopped]])
            rem = np.delete(rem, stopped)
            mask = np.delete(mask, stopped)
            if len(mask) == 0:
                return step[:0], errs, np.array([], dtype=int), done

    step = step[rem,]

    if prev_steps is not None:
        prev_steps = prev_steps[mask,]
        cur_norms = np.linalg.norm(step, axis=1)[:, np.newaxis]
        pre_norms = np.linalg.norm(prev_steps, axis=2)
        overlaps = vec_ops.vec_tensordot(step, prev_steps, axes=[-1, -1], shared=1) / (cur_norms * pre_norms)
        overlaps = np.reshape(overlaps, prev_steps.shape[:2])
        osc = np.where(
            np.all(
                np.logical_and(
                    oscillation_overlap_cutoff_min < abs(overlaps),
                    abs(overlaps) < oscillation_overlap_cutoff_max
                ),
                axis=1
            )
        )

        if len(osc[0]) > 0:
            dist = np.reshape(overlaps[osc][:, np.newaxis, :] @ pre_norms[osc][:, :, np.newaxis], cur_norms.shape)
            osc2 = np.where(dist < 0)[:1]
            if len(osc2[0]) > 0:
                osc = osc[0][osc2]
                scaling = np.min([cur_norms[osc2], -dist[osc2] / 2], axis=0) / cur_norms[osc2]
                step[osc,] = step[osc,] * scaling

    if unitary:
        step = step
        norms = np.linalg.norm(step, axis=1)
        # norms = norms[rem,]
        v = np.linalg.norm(guess[rem,], axis=-1)
        r = np.sqrt(norms ** 2 + v ** 2)
        step = guess[rem,] * (1/r[:, np.newaxis] - 1) + step / r[:, np.newaxis]
        if generate_rotation:
            raise NotImplementedError(">3D rotations are complicated")
            axis = vec_ops.vec_crosses(g, guess[mask,])[0]
            ang = np.arctan2(norms / r, v / r)
            rot = tfs.rotation_matrix(axis, ang)
            rotations = rot @ rotations
    return step, errs, mask, done

def iterative_step_minimize(
        guess,
        step_predictor,
        jacobian=None,
        hessian=None,
        *,
        method=None,
        unitary=False,
        generate_rotation=False,
        dtype='float64',
        orthogonal_directions=None,
        orthogonal_projection_generator=None,
        region_constraints=None,
        function=None,
        max_displacement=None,
        max_displacement_norm=None,
        oscillation_damping_factor=None,
        termination_function=None,
        prevent_oscillations=None,
        tol=1e-8,
        use_max_for_error=True,
        max_iterations=100,
        convergence_metric=None,
        track_best=False,
        return_trajectory=False,
        logger=None,
        log_guess=True
):
    """
    **LLM Docstring**

    Minimize a function over a batch of starting guesses by repeatedly applying a
    step finder until the gradient converges or the iteration cap is hit.

    Supports batched guesses, orthogonal/unitary projection, region constraints,
    oscillation damping, best-point tracking, and optional trajectory return. Each
    iteration only advances the members that have not yet converged.

    :param guess: starting guesses, shape `(..., n)`
    :type guess: np.ndarray
    :param step_predictor: a step finder, spec, or function
    :type step_predictor: Callable | dict | object
    :param jacobian: the gradient function
    :type jacobian: Callable | None
    :param hessian: the Hessian function
    :type hessian: Callable | None
    :param method: the optimization method name/class
    :type method: str | type | None
    :param unitary: constrain the optimization to the unit sphere
    :type unitary: bool
    :param generate_rotation: also return the accumulated unitary rotation
    :type generate_rotation: bool
    :param dtype: working dtype for the guesses
    :type dtype: str
    :param orthogonal_directions: directions to project out of every step
    :type orthogonal_directions: np.ndarray | None
    :param orthogonal_projection_generator: per-guess projector generator
    :type orthogonal_projection_generator: Callable | None
    :param region_constraints: `(min, max)` bounds per coordinate
    :type region_constraints: np.ndarray | None
    :param function: the objective (needed for best-value tracking)
    :type function: Callable | None
    :param max_displacement: cap on the max per-coordinate step
    :type max_displacement: float | None
    :param max_displacement_norm: cap on the step norm
    :type max_displacement_norm: float | None
    :param oscillation_damping_factor: adaptive damping factor for oscillating steps
    :type oscillation_damping_factor: float | None
    :param termination_function: optional early-termination predicate
    :type termination_function: Callable | None
    :param prevent_oscillations: keep this many prior steps for oscillation detection
    :type prevent_oscillations: bool | int | None
    :param tol: gradient convergence tolerance
    :type tol: float
    :param use_max_for_error: use max-abs gradient rather than its norm as the error
    :type use_max_for_error: bool
    :param max_iterations: maximum number of iterations
    :type max_iterations: int
    :param convergence_metric: unused placeholder
    :type convergence_metric: Callable | None
    :param track_best: keep the best point/value seen per member
    :type track_best: bool
    :param return_trajectory: also return the per-iteration trajectory
    :type return_trajectory: bool
    :param logger: optional logger
    :type logger: object | None
    :param log_guess: log the guess at each iteration
    :type log_guess: bool
    :return: `(result, converged, (errors, iterations))` (plus trajectory if requested)
    :rtype: tuple
    """
    logger = dev.Logger.lookup(logger)

    if return_trajectory:
        traj = []
    else:
        traj = None

    step_predictor = get_step_finder(step_predictor,
                                     method=method,
                                     jacobian=jacobian,
                                     hessian=hessian,
                                     logger=logger)
    guess = np.array(guess, dtype=dtype)
    base_shape = guess.shape[:-1]
    guess = guess.reshape(-1, guess.shape[-1])
    if track_best:
        best = guess.copy()
        best_errs = np.full(guess.shape[0], -1, dtype=float)
        if function is not None:
            best_vals = np.full(guess.shape[0], np.inf, dtype=float)
        else:
            best_vals = None
    else:
        best = None
        best_errs = None
        best_vals = None
    its = np.zeros(guess.shape[0], dtype=int)
    errs = np.zeros(guess.shape[0], dtype=float)
    mask = np.arange(guess.shape[0])
    if orthogonal_directions is not None:
        orthogonal_directions = vec_ops.orthogonal_projection_matrix(orthogonal_directions)
    if unitary and generate_rotation:
        rotations = vec_ops.identity_tensors(guess.shape[:-1], guess.shape[-1])
    else:
        rotations = None

    if prevent_oscillations is None:
        prevent_oscillations = (
                unitary
                or orthogonal_projection_generator is not None
                or orthogonal_directions is not None
        )
    if prevent_oscillations is True:
        prevent_oscillations = 1
    prev_step = None
    prev_errs = None

    converged = True
    for i in range(max_iterations):
        with logger.block(tag=f"Iteration {i}"):
            step, step_errs, new_mask, _ = iterative_step_minimize_step(
                step_predictor, guess[mask,],
                mask, tol,
                orthogonal_directions, orthogonal_projection_generator,
                region_constraints, unitary, max_displacement, max_displacement_norm,
                generate_rotation, prev_step, use_max_for_error, termination_function,
                is_climbing=None
            )
            fvals = None
            if best is not None:
                if i == 0:
                    if best_vals is not None:
                        fvals = function(guess[mask,], mask)
                        best_vals[mask,] = fvals
                    best_errs[mask,] = step_errs
                    best[mask,] = guess[mask,]
                else:
                    if best_vals is not None:
                        fvals = function(guess[mask,], mask)
                        new_vals = fvals
                        improved = np.where(new_vals < best_vals[mask,])
                        if len(improved[0]) > 0:
                            imp_mask = mask[improved]
                            best_vals[imp_mask,] = new_vals[improved,]
                            best[imp_mask,] = guess[imp_mask,]
                            best_errs[imp_mask,] = step_errs[improved,]
                    else:
                        improved = np.where(step_errs < best_errs[mask,])
                        if len(improved[0]) > 0:
                            imp_mask = mask[improved]
                            best_errs[imp_mask,] = step_errs[improved,]
                            best[imp_mask,] = guess[imp_mask,]


            if log_guess:
                logger.log_print("Guess: {guess}", guess=guess[mask,])
            logger.log_print("Predicted steps: {step}", step=step)
            logger.log_print("Step errors: {errs}", errs=step_errs)
            if fvals is not None:
                logger.log_print("Function values: {fvals}", fvals=fvals)
            if best_vals is not None:
                logger.log_print("Best value found: {mins}", mins=best_vals[mask,])
            elif best_errs is not None:
                logger.log_print("Best error found: {mins}", mins=best_errs[mask,])
            if prevent_oscillations:
                if prev_step is None:
                    prev_step = np.random.uniform(size=(step.shape[0], prevent_oscillations, step.shape[1])).astype(step.dtype)
                p = i % prevent_oscillations
                prev_step[new_mask, p] = step
            if (not unitary) and oscillation_damping_factor is not None:
                if prev_errs is None:
                    prev_errs = step_errs
                else:
                    prev_errs[new_mask,] = step_errs

                inc_err = np.where(step_errs >= prev_errs[new_mask] - 1e-6) # add some flexibility
                if len(inc_err[0]) > 0:
                    oscillation_damping_factor /= 2
                else:
                    oscillation_damping_factor = np.min([oscillation_damping_factor * 1.2, 1.0])
                step = step * oscillation_damping_factor
                logger.log_print("Oscillation damping factor: {damp}", damp=oscillation_damping_factor)

            errs[mask,] = step_errs
            if len(new_mask) == 0:
                break

            mask = new_mask
            guess[mask,] += step
            its[mask,] += 1
            if return_trajectory:
                traj.append((mask, guess[mask,].copy()))
    else:
        converged = False
        its[mask,] = max_iterations
        if best is not None:
            guess[mask,] = best[mask,]
            errs[mask,] = best_errs[mask,]

    guess = guess.reshape(base_shape + (guess.shape[-1],))
    errs = errs.reshape(base_shape)
    its = its.reshape(base_shape)

    if unitary and generate_rotation:
        res = (guess, rotations), converged, (errs, its)
    else:
        res = guess, converged, (errs, its)

    if return_trajectory:
        return res, traj
    else:
        return res

scipy_no_hessian_methods = {'cg', 'bfgs'}
scipy_no_grad_methods = {'nelder-mead'}
use_scipy_linesearch = False
def scipy_minimize(
        coords,
        function,
        jacobian=None,
        hessian=None,
        optimizer_settings=None,
        unitary=True,
        orthogonal_projector=None,
        orthogonal_projection_generator=None,
        line_search=None,
        return_trajectory=False,
        method='bfgs',
        max_iterations=None,
        tol=1e-8,
        line_search_step=None,
        max_displacement=.01,
        region_constraints=None,
        logger=None
):
    """
    **LLM Docstring**

    Minimize a function with `scipy.optimize.minimize`, wired up for this module's
    conventions (batched-style flattening, optional unitary/orthogonal projection,
    displacement capping, trajectory logging).

    When line search is disabled, `scipy`'s Wolfe line search is temporarily
    monkey-patched with a fixed-max-displacement step so each step size is bounded.

    :param coords: the starting coordinates
    :type coords: np.ndarray
    :param function: the objective function
    :type function: Callable
    :param jacobian: the gradient function
    :type jacobian: Callable | None
    :param hessian: the Hessian function
    :type hessian: Callable | None
    :param optimizer_settings: extra options passed through to `scipy`
    :type optimizer_settings: dict | None
    :param unitary: apply a unit-sphere projection to the gradient
    :type unitary: bool
    :param orthogonal_projector: fixed projector applied to the gradient
    :type orthogonal_projector: np.ndarray | None
    :param orthogonal_projection_generator: per-guess projector generator
    :type orthogonal_projection_generator: Callable | None
    :param line_search: whether to use `scipy`'s line search (else fixed steps)
    :type line_search: bool | None
    :param return_trajectory: also return the optimization trajectory
    :type return_trajectory: bool
    :param method: the `scipy` method (`'quasi-newton'` maps to BFGS)
    :type method: str
    :param max_iterations: maximum iterations
    :type max_iterations: int | None
    :param tol: gradient tolerance
    :type tol: float
    :param line_search_step: fixed step to return when line search is off
    :type line_search_step: float | None
    :param max_displacement: cap on the max per-coordinate step
    :type max_displacement: float
    :param region_constraints: per-coordinate bounds
    :type region_constraints: dict | None
    :param logger: optional logger
    :type logger: object | None
    :return: `(success, result[, scipy_result])`, with a trajectory when requested
    :rtype: tuple
    """
    from scipy.optimize import minimize, _optimize, _minimize

    optimizer_settings = {} if optimizer_settings is None else dict(optimizer_settings)
    method = method.lower()

    if not line_search:
        optimizer_settings = {'c1': 0.00001, 'c2': 0.999} | optimizer_settings

    callback = optimizer_settings.pop('callback', None)
    if return_trajectory:
        traj = []
        if callback is None:
            def callback(x):
                """
                **LLM Docstring**

                Trajectory callback: append the current iterate to the trajectory list.

                :param x: the current iterate from `scipy`
                :type x: np.ndarray
                """
                traj.append(x)
        else:
            def append_callback(intermediate_result, cb):
                """
                **LLM Docstring**

                Trajectory callback that records the iterate and then chains to a user callback.

                :param intermediate_result: the current `scipy` intermediate result
                :type intermediate_result: object
                :param cb: the wrapped user callback
                :type cb: Callable
                :return: the wrapped callback's return value
                :rtype: object
                """
                traj.append(intermediate_result)
                return cb(intermediate_result)

            callback = functools.partial(append_callback, cb=callback)
    if logger is not None:
        if logger.active:
            prev_re = [coords.flatten().view(np.ndarray)]
            if callback is None:
                def log_callback(intermediate_result, prev_re):
                    """
                    **LLM Docstring**

                    Logging callback: record the current structure and step, then (when wrapping a
                    user callback) chain to it.

                    :param intermediate_result: the current `scipy` intermediate result
                    :type intermediate_result: object
                    :return: the wrapped callback's return value, when chaining
                    :rtype: object
                    """
                    logger.log_print(
                        [
                            "Struct: {intermediate_result}",
                            "Step: {intermediate_step}"
                        ],
                        intermediate_result=intermediate_result,
                        intermediate_step=intermediate_result - prev_re[-1]
                    ),
                    prev_re.append(intermediate_result)

                callback = functools.partial(log_callback, prev_re=prev_re)
            else:
                def log_callback(intermediate_result, cb, prev_re):
                    """
                    **LLM Docstring**

                    Logging callback: record the current structure and step, then (when wrapping a
                    user callback) chain to it.

                    :param intermediate_result: the current `scipy` intermediate result
                    :type intermediate_result: object
                    :return: the wrapped callback's return value, when chaining
                    :rtype: object
                    """
                    logger.log_print(
                        [
                            "Struct: {intermediate_result}",
                            "Step: {intermediate_step}"
                        ],
                        intermediate_result=intermediate_result,
                        intermediate_step=intermediate_result - prev_re[-1]
                    ),
                    prev_re.append(intermediate_result)
                    return cb(intermediate_result)

                callback = functools.partial(log_callback, cb=callback, prev_re=prev_re)

    min_ops = {}
    if max_iterations is not None:
        min_ops['maxiter'] = max_iterations
    method = 'bfgs' if method == 'quasi-newton' else method
    if method in scipy_no_hessian_methods or method in scipy_no_grad_methods:
        hessian = None
    if method in scipy_no_grad_methods:
        jacobian = None

    if region_constraints is not None:
        # Dictionary regions are offsets from the starting coordinates. Explicit
        # optimizer bounds take precedence on either side, as intended previously.
        bounds = optimizer_settings.pop('bounds', [(None, None)] * coords.size)
        min_ops['bounds'] = [
            (
                c + region_constraints[i][0] if lo is None and region_constraints[i][0] is not None else lo,
                c + region_constraints[i][1] if hi is None and region_constraints[i][1] is not None else hi
            ) if i in region_constraints else (lo, hi)
            for i, (c, (lo, hi)) in enumerate(zip(coords.flatten(), bounds))
        ]

    if (
            unitary
            or orthogonal_projector is not None
            or orthogonal_projection_generator is not None
    ):
        def jacobian(guess, _jacobian=jacobian):
            """
            **LLM Docstring**

            Gradient wrapper that applies the configured unitary/orthogonal projection to
            the raw gradient before returning it.

            :param guess: the current point
            :type guess: np.ndarray
            :return: the projected gradient
            :rtype: np.ndarray
            """
            if unitary:
                projector = vec_ops.orthogonal_projection_matrix(guess[..., np.newaxis])
                if orthogonal_projector is not None:
                    projector = projector @ orthogonal_projector[np.newaxis]
                if orthogonal_projection_generator is not None:
                    projector = projector @ orthogonal_projection_generator(guess)
            elif orthogonal_projector is not None:
                projector = orthogonal_projector[np.newaxis]
                if orthogonal_projection_generator is not None:
                    projector = projector @ orthogonal_projection_generator(guess)
            elif orthogonal_projection_generator is not None:
                projector = orthogonal_projection_generator(guess)
            else:
                projector = None

            base = _jacobian(guess)
            if projector is not None:
                base = (projector @ base[:, np.newaxis]).reshape(base.shape)
            return base

    scipy_meth = 'bfgs' if method == 'quasi-newton' else method
    if scipy_meth == 'newton-cg':
        min_ops['xtol'] = tol
    elif scipy_meth not in scipy_no_grad_methods:
        min_ops['gtol'] = tol
        # min_ops['ftol'] = 0
        # min_ops['xtol'] = 0
    min_ops = dict(
        min_ops,
        **optimizer_settings
    )
    bounds = min_ops.pop('bounds', None)
    constraints = min_ops.pop('constraints', ())
    try:
        if not line_search:
            old_wolfe = _optimize.line_search_wolfe1

            def _find_max_displacement_step(
                    f, fprime, xk, pk, gfk=None,
                    old_fval=None, old_old_fval=None,
                    args=(), c1=1e-4, c2=0.9, amax=50, amin=1e-8,
                    xtol=1e-14
            ):
                """
                **LLM Docstring**

                Drop-in replacement for `scipy`'s Wolfe line search that returns a fixed step
                capped so the largest coordinate displacement equals `max_displacement`.

                :param f: the objective (unused)
                :param fprime: the gradient (unused)
                :param xk: the current point (unused)
                :param pk: the search direction
                :type pk: np.ndarray
                :return: the `scipy` line-search result tuple with the capped step size
                :rtype: tuple
                """
                if line_search_step is not None:
                    return line_search_step, None, None, old_fval, old_old_fval, None
                else:
                    max_pk = np.max(np.abs(pk))
                    if max_pk < 1e-6:
                        return max_displacement, None, None, old_fval, old_old_fval, None
                    else:
                        return max_displacement / max_pk, None, None, old_fval, old_old_fval, None

            _optimize.line_search_wolfe1 = _find_max_displacement_step
        min = minimize(function,
                       coords.flatten(),
                       method=scipy_meth,
                       tol=tol,
                       jac=jacobian,
                       hess=hessian,
                       callback=callback,
                       bounds=bounds,
                       constraints=constraints,
                       options=min_ops)
    finally:
        if not line_search:
            _optimize.line_search_wolfe1 = old_wolfe
    if return_trajectory:
        return min.success, (
            min.x.reshape(coords.shape),
            [t.reshape(coords.shape) for t in traj],
        ), min
    else:
        return min.success, min.x.reshape(coords.shape), min

def _find_peak(v):
    """
    **LLM Docstring**

    Return the index of the maximum-energy image in a chain (the transition-state
    guess).

    :param v: the per-image values
    :type v: np.ndarray
    :return: the index of the peak
    :rtype: int
    """
    return np.argmax(v)
# def _find_second_valley(error):
#     # find the point where curvature swaps
#     a1 = np.diff(e)

default_chain_step_finder='neb'
def iterative_chain_minimize(
        chain_guesses, step_predictors,
        jacobian=None,
        hessian=None,
        *,
        method=None,
        unitary=False,
        function=None,
        climb=None,
        climbing_nodes=None,
        climbing_node_identifier=None,
        generate_rotation=False,
        dtype='float64',
        orthogonal_directions=None,
        orthogonal_projection_generator=None,
        prevent_oscillations=None,
        region_constraints=None,
        convergence_metric=None,
        termination_function=None,
        reparametrizer=None,
        max_displacement=None,
        max_displacement_norm=None,
        tol=1e-8,
        max_iterations=100,
        use_max_for_error=True,
        periodic=False,
        reembed=None,
        embedding_options=None,
        fixed_images=None,
        return_trajectory=False,
        logger=None,
        log_guess=False,
):
    """
    **LLM Docstring**

    Minimize a chain of images (e.g. a reaction path) by applying per-image step
    finders, with optional climbing-image, spring/NEB, reparametrization, and
    re-embedding support.

    Generalizes `iterative_step_minimize` to a `(batch, n_images, n)` chain: each
    image is stepped by its own step finder (which sees its neighbours through the
    chain step-finder wrappers), climbing images are handled specially, and the
    chain can be reparametrized/re-embedded between iterations.

    :param chain_guesses: the initial chain(s), shape `(..., n_images, n)`
    :type chain_guesses: np.ndarray
    :param step_predictors: one step finder (broadcast) or one per image
    :type step_predictors: Callable | Iterable
    :param jacobian: the per-image gradient function
    :type jacobian: Callable | None
    :param hessian: the per-image Hessian function
    :type hessian: Callable | None
    :param method: the optimization method name/class
    :type method: str | type | None
    :param unitary: constrain images to the unit sphere
    :type unitary: bool
    :param function: the image objective (for climbing detection / tracking)
    :type function: Callable | None
    :param climb: enable climbing-image behavior
    :type climb: bool | None
    :param climbing_nodes: explicit climbing-image indices
    :type climbing_nodes: Iterable[int] | None
    :param climbing_node_identifier: callable choosing the climbing image(s)
    :type climbing_node_identifier: Callable | None
    :param generate_rotation: also return unitary rotations (unsupported)
    :type generate_rotation: bool
    :param dtype: working dtype
    :type dtype: str
    :param orthogonal_directions: directions to project out of every step
    :type orthogonal_directions: np.ndarray | None
    :param orthogonal_projection_generator: per-guess projector generator
    :type orthogonal_projection_generator: Callable | None
    :param prevent_oscillations: oscillation-detection history length
    :type prevent_oscillations: bool | int | None
    :param region_constraints: per-coordinate bounds
    :type region_constraints: np.ndarray | None
    :param convergence_metric: unused placeholder
    :type convergence_metric: Callable | None
    :param termination_function: optional early-termination predicate
    :type termination_function: Callable | None
    :param reparametrizer: callable redistributing images along the path
    :type reparametrizer: Callable | None
    :param max_displacement: cap on the max per-coordinate step
    :type max_displacement: float | None
    :param max_displacement_norm: cap on the step norm
    :type max_displacement_norm: float | None
    :param tol: gradient convergence tolerance
    :type tol: float
    :param max_iterations: maximum iterations
    :type max_iterations: int
    :param use_max_for_error: use max-abs gradient rather than its norm as the error
    :type use_max_for_error: bool
    :param periodic: treat the chain as periodic (wrap endpoints)
    :type periodic: bool
    :param reembed: re-embed images between iterations
    :type reembed: bool | None
    :param embedding_options: options for the re-embedding
    :type embedding_options: dict | None
    :param fixed_images: image indices to hold fixed (e.g. endpoints)
    :type fixed_images: Iterable[int] | None
    :param return_trajectory: also return the trajectory
    :type return_trajectory: bool
    :param logger: optional logger
    :type logger: object | None
    :param log_guess: log each image guess
    :type log_guess: bool
    :return: `(chain, converged, (errors, iterations))` (plus trajectory if requested)
    :rtype: tuple
    """
    if unitary and generate_rotation:
        raise NotImplementedError(...)

    guesses = np.array(chain_guesses, dtype=dtype)
    base_shape = guesses.shape[:-2]
    guesses = guesses.reshape((-1,) + guesses.shape[-2:])
    vals = np.zeros(guesses.shape[:-1])
    if reembed is None:
        reembed = embedding_options is not None
    if embedding_options is None:
        embedding_options = {}

    try:
        iter(step_predictors)
    except TypeError:
        step_predictors = [step_predictors] * guesses.shape[-2]
    step_predictors = [
        get_step_finder(predictor,
                        method=default_chain_step_finder if method is None else method,
                        jacobian=jacobian,
                        hessian=hessian)
        for predictor in step_predictors
    ]
    its = np.zeros(guesses.shape[0], dtype=int)
    errs = np.zeros(guesses.shape[0], dtype=float)
    submasks = np.full(guesses.shape[:2], True, dtype=bool)
    if fixed_images is not None:
        submasks[..., fixed_images] = False
    mask = np.arange(guesses.shape[0])
    if orthogonal_directions is not None:
        orthogonal_directions = vec_ops.orthogonal_projection_matrix(orthogonal_directions)
    # if unitary and generate_rotation:
    #     rotations = vec_ops.identity_tensors(guess.shape[:-1], guess.shape[-1])
    # else:
    #     rotations = None

    if prevent_oscillations is None:
        prevent_oscillations = (
                unitary
                or orthogonal_projection_generator is not None
                or orthogonal_directions is not None
        )
    if prevent_oscillations:
        prev_step = np.zeros_like(guesses)
    else:
        prev_step = None
    nimg = guesses.shape[-2]
    n = nimg - 1

    if fixed_images is None:
        fixed_images = []

    if reparametrizer is not None:
        image_numbers = np.full(guesses.shape[0], nimg, dtype=int)
    else:
        image_numbers = None

    if return_trajectory:
        traj = []

    if climb is None:
        climb = (
                climbing_nodes is not None
                or climbing_node_identifier is not None
        )
    if climb and function is not None:
        vals = function(guesses, mask)
        if dev.str_is(climbing_node_identifier, 'first'):
            climbing_nodes = [
                _find_peak(v)
                for v in vals
            ]
        function = None

    logger = dev.Logger.lookup(logger)

    converged = True
    climbing_nodes_og = climbing_nodes
    for i in range(max_iterations):
        with logger.block(tag=f"Iteration {i}"):
            # for each unoptimized chain, we only move image `j` if
            # or it's neihbors weren't optimized at the last step, every time an image is moved
            # it's neighbors are marked as moveable again

            errs[mask,] = 0
            if climb:
                if climbing_nodes is None:
                    if climbing_node_identifier is None:
                        if function is not None:
                            climbing_nodes = [
                                _find_peak(v)
                                for v in vals
                            ]
                        else:
                            climbing_nodes = [
                                _find_second_valley(e)
                                for e in errs
                            ]
                    else:
                        climbing_nodes = climbing_node_identifier(vals, errs)
            else:
                climbing_nodes = None
            for j in range(nimg):
                submask = mask[submasks[mask,][:, j]]
                prev_im = j-1
                next_im = j+1
                if j == 0:
                    if periodic:
                        prev_im = n
                    else:
                        prev_im = None
                elif j == n:
                    if periodic:
                        next_im = 0
                    else:
                        next_im = None

                # if log_guess:
                logger.log_print("Moving node {j} from {submask}", j=j, submask=submask)

                step_predictor = step_predictors[j]
                ps = prev_step[submask,][:, j] if prev_step is not None else prev_step
                g = guesses[submask]
                if climbing_nodes is None:
                    is_climbing = [False] * len(g)
                else:
                    is_climbing = [
                        c == j
                        for c in [climbing_nodes[m] for m in submask]
                    ]

                if climb and any(is_climbing):
                    logger.log_print("Climbing nodes: {is_climbing}", is_climbing=is_climbing)
                if len(submask) == 0: continue
                step, step_errs, new_mask, done = iterative_step_minimize_step(
                    step_predictor, g,
                    (submask, (j, prev_im, next_im)), tol,
                    orthogonal_directions, orthogonal_projection_generator,
                    region_constraints, unitary, max_displacement, max_displacement_norm,
                    generate_rotation, ps,
                    use_max_for_error, termination_function, is_climbing
                )
                if isinstance(step, tuple) and len(step) == 2:
                    step, subvals = step
                    vals[new_mask,] = subvals
                elif function is not None:
                    subvals = function(g)
                    vals[new_mask,] = subvals

                if prevent_oscillations:
                   prev_step[new_mask, j] = step

                # set which chains are done or not
                done = submask[done]
                submasks[done, j] = False
                if j not in fixed_images:
                    submasks[new_mask, j] = True
                if j == 0:
                    if j + 1 not in fixed_images:
                        submasks[new_mask, j+1] = True
                    if periodic and n not in fixed_images: #TODO: add O(1) check
                        submasks[new_mask, n] = True
                elif j == n:
                    if j-1 not in fixed_images:
                        submasks[new_mask, j-1] = True
                    if periodic and 0 not in fixed_images:
                        submasks[new_mask, 0] = True
                else:
                    if j+1 not in fixed_images:
                        submasks[new_mask, j+1] = True
                    if j-1 not in fixed_images:
                        submasks[new_mask, j-1] = True

                errs[submask,] += step_errs
                guesses[new_mask, j] += step
                if reembed and len(new_mask) > 0: # implies Cartesian
                    from .CoordinateFrames import eckart_embedding

                    if j == 0:
                        if periodic:
                            ref = n
                        else:
                            ref = 1
                    else:
                        ref = j-1
                    ref = guesses[new_mask, ref]
                    coords = guesses[new_mask, j]
                    emb = eckart_embedding(
                        ref.reshape(ref.shape[0], -1, 3),
                        coords.reshape(coords.shape[0], -1, 3),
                        **embedding_options
                    )
                    guesses[new_mask, j] = emb.coordinates.reshape(coords.shape[0], -1)

            climbing_nodes = climbing_nodes_og
            if reparametrizer is not None:
                new_chains, moved_images, fixed_images = reparametrizer(guesses[mask,], fixed_images)
                nimg_new = new_chains.shape[1]
                if nimg_new != nimg:
                    raise ValueError("reparametrization must preserve the number of images")
                guesses[mask,] = new_chains
                submasks[mask,] |= np.any(moved_images, axis=1)[:, np.newaxis]
                if len(fixed_images) > 0:
                    submasks[mask[:, np.newaxis], fixed_images] = False

                if prev_step is not None:
                    prev_step = np.zeros_like(guesses)

            done = np.where(
                np.logical_not(np.any(submasks[mask,], axis=1))
            )[0]
            if len(done) > 0:  # easy check
                mask = np.delete(mask, done)
                if len(mask) == 0:
                    break
            its[mask,] += 1

            if return_trajectory:
                traj.append(guesses.copy())
    else:
        converged = False
        its[mask,] = max_iterations

    guesses = guesses.reshape(base_shape + guesses.shape[-2:])
    errs = errs.reshape(base_shape)
    its = its.reshape(base_shape)

    if return_trajectory:
        guesses = (guesses, [g.reshape(base_shape + g.shape[-2:]) for g in traj])

    if unitary and generate_rotation:
        raise NotImplementedError(...)
        res = (guess, rotations), converged, (errs, its)
    else:
        res = (guesses, image_numbers), converged, (errs, its)


    return res

class Damper:
    def __init__(self, damping_parameter=None, damping_exponent=None, restart_interval=10):
        """
        **LLM Docstring**

        Set up a step damper with a (possibly decaying) damping factor.

        :param damping_parameter: base damping factor (`None` disables damping)
        :type damping_parameter: float | None
        :param damping_exponent: exponent applied to grow/decay the factor over iterations
        :type damping_exponent: float | None
        :param restart_interval: iteration count after which the decay resets
        :type restart_interval: int
        """
        self.n = 0
        self.u = damping_parameter
        self.exp = 1.0 if damping_exponent is None else damping_exponent
        self.restart = restart_interval

    def get_damping_factor(self):
        """
        **LLM Docstring**

        Return the current damping factor, advancing (and periodically resetting) the
        internal iteration counter.

        :return: the damping factor, or `None` if damping is disabled
        :rtype: float | None
        """
        u = self.u
        if u is not None:
            if self.exp > 0:
                u = np.power(u, self.n*self.exp)
                self.n = (self.n + 1) % self.restart
        return u

class LineSearcher(metaclass=abc.ABCMeta):
    """
    Adapted from scipy.optimize to handle multiple structures at once
    """

    def __init__(self, func, min_alpha=0, **opts):
        """
        **LLM Docstring**

        Initialize a line searcher around an objective function.

        :param func: the objective, called as `func(points, mask)`
        :type func: Callable
        :param min_alpha: minimum allowed step length
        :type min_alpha: float
        :param opts: default options forwarded to the search
        """
        self.func = func
        self.opts = opts
        self.min_alpha = min_alpha

    @abc.abstractmethod
    def check_scalar_converged(self, phi_vals, alphas, **opts):
        """
        **LLM Docstring**

        Abstract: test whether the line-search values satisfy the convergence criterion.

        :param phi_vals: objective values along the search direction
        :type phi_vals: np.ndarray
        :param alphas: current step lengths
        :type alphas: np.ndarray
        :return: a boolean convergence mask
        :rtype: np.ndarray
        """
        raise NotImplementedError("abstract")

    @abc.abstractmethod
    def update_alphas(self,
                      phi_vals, alphas, iteration,
                      old_phi_vals, old_alphas_vals,
                      mask,
                      **opts
                      ):
        """
        **LLM Docstring**

        Abstract: propose new step lengths for the next line-search iteration.

        :param phi_vals: current objective values
        :type phi_vals: np.ndarray
        :param alphas: current step lengths
        :type alphas: np.ndarray
        :param iteration: the line-search iteration index
        :type iteration: int
        :param old_phi_vals: recent historical objective values
        :type old_phi_vals: list | None
        :param old_alphas_vals: recent historical step lengths
        :type old_alphas_vals: list | None
        :param mask: indices of the active members
        :type mask: np.ndarray
        :return: the updated step lengths
        :rtype: np.ndarray
        """
        raise NotImplementedError("abstract")

    default_alpha = 1e-3
    def get_default_alpha(self, am):
        """
        **LLM Docstring**

        Return the fallback step length used when the line search fails to converge.

        :param am: the current step lengths for the unconverged members
        :type am: np.ndarray
        :return: the default step lengths
        :rtype: np.ndarray
        """
        return np.full_like(am, self.default_alpha)
    def scalar_search(self,
                      scalar_func,
                      guess_alpha,
                      min_alpha=None,
                      max_iterations=15,
                      history_length=1,
                      **opts):
        """Search each batch member independently, returning zero on failure.

        The returned objective values always correspond to the returned alphas.
        Failed searches retain a false convergence flag and leave the point intact.
        """
        if min_alpha is None:
            min_alpha = self.min_alpha
        if min_alpha is None:
            min_alpha = 0

        alphas = np.array(guess_alpha, dtype=float, copy=True)
        mask = np.arange(len(alphas))
        phi_vals = np.array(scalar_func(alphas, mask), dtype=float, copy=True)
        history = collections.deque(maxlen=history_length) if history_length > 0 else None
        is_converged = np.full(len(mask), False)

        for i in range(max_iterations + 1):
            converged = np.where(self.check_scalar_converged(
                phi_vals[mask], alphas[mask], mask=mask, **opts
            ))[0]
            is_converged[mask[converged]] = True
            mask = np.delete(mask, converged)
            if len(mask) == 0 or i == max_iterations:
                break

            # A failed trial at the lower bound cannot be reduced further.
            mask = mask[alphas[mask] > min_alpha]
            if len(mask) == 0:
                break

            phi_vals_old = [p[mask] for p, a in history] if history is not None else None
            alpha_vals_old = [a[mask] for p, a in history] if history is not None else None
            new_alphas = self.update_alphas(
                phi_vals, alphas, i, phi_vals_old, alpha_vals_old, mask, **opts
            )
            if history is not None:
                history.append([phi_vals.copy(), alphas.copy()])
            new_alphas = np.maximum(new_alphas, min_alpha)
            phi_vals[mask] = scalar_func(new_alphas, mask)
            alphas[mask] = new_alphas

        failed = np.where(~is_converged)[0]
        if len(failed) > 0:
            alphas[failed] = 0
            phi_vals[failed] = scalar_func(alphas[failed], failed)
        return alphas, (phi_vals, is_converged)

    def prep_search(self, initial_geom, search_dir, guess_alpha=1, function_mask=None, **opts):
        """
        **LLM Docstring**

        Prepare the line search: build the initial step length, the option dict, and
        the directional objective function.

        :param initial_geom: the base points
        :type initial_geom: np.ndarray
        :param search_dir: the search directions
        :type search_dir: np.ndarray
        :param guess_alpha: initial step length
        :type guess_alpha: float
        :param opts: extra options
        :return: `(guess_alpha, opts, phi)`
        :rtype: tuple
        """
        return np.full(len(initial_geom), guess_alpha), opts, self._dir_func(self.func, initial_geom, search_dir, function_mask=function_mask)

    @classmethod
    def _dir_func(cls, func, initial_geom, search_dir, function_mask=None):
        """
        **LLM Docstring**

        Build the directional objective `phi(alphas, mask) = func(geom + alpha *
        search_dir)`.

        :param func: the objective function
        :type func: Callable
        :param initial_geom: the base points
        :type initial_geom: np.ndarray
        :param search_dir: the search directions
        :type search_dir: np.ndarray
        :return: the directional objective
        :rtype: Callable
        """
        @functools.wraps(func)
        def phi(alphas, mask):
            """
            **LLM Docstring**

            Evaluate the objective at `initial_geom + alphas * search_dir` for the active
            members.

            :param alphas: the step lengths
            :type alphas: np.ndarray
            :param mask: indices of the active members
            :type mask: np.ndarray
            :return: the objective values
            :rtype: np.ndarray
            """
            ids = mask if function_mask is None else np.asarray(function_mask)[mask]
            return func(initial_geom[mask] + alphas[:, None] * search_dir[mask], ids)

        return phi

    def __call__(self, initial_geom, search_dir, **base_opts):
        """
        **LLM Docstring**

        Run the line search for the given points and search directions.

        :param initial_geom: the base points
        :type initial_geom: np.ndarray
        :param search_dir: the search directions
        :type search_dir: np.ndarray
        :param base_opts: extra options merged over the searcher defaults
        :return: `(alphas, (phi_vals, is_converged))`
        :rtype: tuple
        """
        opts = dict(self.opts, **base_opts)
        guess_alpha, opts, phi = self.prep_search(initial_geom, search_dir, **opts)
        conv = self.scalar_search(
            phi,
            guess_alpha,
            **opts
        )
        return conv

class ArmijoSearch(LineSearcher):

    def __init__(self, func, c1=1e-4, min_alpha=None, fixed_step_cutoff=1e-8, der_max=1e2, guess_alpha=1):
        """
        **LLM Docstring**

        Initialize an Armijo (sufficient-decrease) line search.

        :param func: the objective function
        :type func: Callable
        :param c1: the Armijo sufficient-decrease parameter
        :type c1: float
        :param min_alpha: minimum allowed step length
        :type min_alpha: float | None
        :param fixed_step_cutoff: lower bound on the directional derivative magnitude used to scale the initial trial
        :type fixed_step_cutoff: float | None
        :param der_max: cap on the initial predicted objective change (`None` disables)
        :type der_max: float | None
        :param guess_alpha: initial step length
        :type guess_alpha: float
        """
        super().__init__(func, min_alpha=min_alpha, c1=c1)
        self.func = func
        self.der_max = der_max
        self.fixed_step_cutoff = fixed_step_cutoff
        self.guess_alpha = guess_alpha

    def prep_search(self, initial_geom, search_dir, *, initial_grad, min_alpha=None, **rest):
        """Use the actual directional derivative and bound the initial trial.

        ``der_max`` bounds the initial predicted objective change, rather than
        changing the derivative used by the Armijo test and interpolation.
        """
        mask = np.arange(len(initial_geom))
        derphi0 = np.einsum('ij,ij->i', initial_grad, search_dir)
        if min_alpha is None:
            min_alpha = self.min_alpha
        if min_alpha is None:
            min_alpha = 1e-8

        rest.setdefault('guess_alpha', self.guess_alpha)
        a0, opts, phi = super().prep_search(initial_geom, search_dir, **rest)
        if self.der_max is not None:
            cutoff = self.fixed_step_cutoff
            if cutoff is None:
                cutoff = np.finfo(float).tiny
            cutoff = max(cutoff, np.finfo(float).tiny)
            a0 = np.minimum(a0, self.der_max / np.maximum(np.abs(derphi0), cutoff))
        a0 = np.maximum(a0, min_alpha)
        phi0 = phi(np.zeros_like(a0), mask)
        return a0, dict(opts, phi0=phi0, derphi0=derphi0, min_alpha=min_alpha), phi

    converged_tolerance = 0
    def check_scalar_converged(self, phi_vals, alphas, *, phi0, c1, derphi0, tol=None, mask=None):
        """Apply the sufficient-decrease test separately to each active member."""
        if tol is None:
            tol = self.converged_tolerance
        if mask is not None:
            phi0 = phi0[mask]
            derphi0 = derphi0[mask]
        test = phi0 + c1 * alphas * derphi0
        return np.isfinite(phi_vals) & (phi_vals <= test + tol)

    def get_default_alpha(self, am, *, phi0, **etc):
        """
        **LLM Docstring**

        Return the fallback step length (scaled by the inverse baseline value) when the
        Armijo search fails to converge.

        :param am: current step lengths for the unconverged members
        :type am: np.ndarray
        :param phi0: baseline objective value
        :type phi0: np.ndarray
        :return: the default step lengths
        :rtype: np.ndarray
        """
        return np.full_like(am, self.default_alpha / np.abs(phi0))

    def update_alphas(self,
                      phi_vals, alphas, iteration,
                      old_phi_vals, old_alphas_vals, mask,
                      *, phi0, c1, derphi0, zero_cutoff=1e-16):
        """Safeguard interpolation; halve trials with nonfinite objective values."""
        phi0 = phi0[mask]
        derphi0 = derphi0[mask]
        phi_a1 = phi_vals[mask]
        alpha1 = alphas[mask]

        with np.errstate(over='ignore', divide='ignore', invalid='ignore'):
            if iteration == 0 or not old_phi_vals:
                factor = phi_a1 - phi0 - derphi0 * alpha1
                candidate = -derphi0 * alpha1 ** 2 / (2 * factor)
            else:
                phi_a0 = old_phi_vals[-1]
                alpha0 = old_alphas_vals[-1]
                delta = alpha1 - alpha0
                f0 = (phi_a0 - phi0 - derphi0 * alpha0) / (alpha0 ** 2 * delta)
                f1 = (phi_a1 - phi0 - derphi0 * alpha1) / (alpha1 ** 2 * delta)
                a = f1 - f0
                b = alpha1 * f0 - alpha0 * f1
                discriminant = b ** 2 - 3 * a * derphi0
                # Rationalized root avoids subtracting nearly equal quantities.
                candidate = -derphi0 / (b + np.sqrt(discriminant))

        valid = np.isfinite(phi_a1) & np.isfinite(candidate) & (candidate > 0)
        candidate = np.where(valid, candidate, alpha1 / 2)
        return np.clip(candidate, .1 * alpha1, .5 * alpha1)

class _WolfeLineSearch(LineSearcher):
    """
    Adapted from scipy.optimize
    """

    def __init__(self, func, grad, **opts):
        """
        **LLM Docstring**

        Initialize a Wolfe-condition line search (which also needs the gradient).

        :param func: the objective function
        :type func: Callable
        :param grad: the gradient function
        :type grad: Callable
        :param opts: default options
        """
        super().__init__(func)
        self.grad = grad

    @classmethod
    def _grad_func(cls, jac, initial_geom, search_dir):
        """
        **LLM Docstring**

        Build the directional-derivative function `derphi(alphas, mask)` from the
        gradient along the search direction.

        :param jac: the gradient function
        :type jac: Callable
        :param initial_geom: the base points
        :type initial_geom: np.ndarray
        :param search_dir: the search directions
        :type search_dir: np.ndarray
        :return: the directional-derivative function
        :rtype: Callable
        """
        @functools.wraps(jac)
        def derphi(alphas, mask):
            """
            **LLM Docstring**

            Directional derivative at `initial_geom + alphas * search_dir` along the search
            direction.

            :param alphas: the step lengths
            :type alphas: np.ndarray
            :param mask: indices of the active members
            :type mask: np.ndarray
            :return: the directional derivatives
            :rtype: np.ndarray
            """
            pk = search_dir[mask,]
            grad = jac(initial_geom[mask,] + alphas[:, np.newaxis] * pk, mask)
            return (grad[: np.newaxis, :] @ pk[:, :, np.newaxis]).reshape(-1)

        return derphi

    def prep_search(self, initial_geom, search_dir):
        """
        **LLM Docstring**

        Prepare the Wolfe search (not yet implemented).

        :param initial_geom: the base points
        :type initial_geom: np.ndarray
        :param search_dir: the search directions
        :type search_dir: np.ndarray
        :raises NotImplementedError: always
        """
        raise NotImplementedError()
        a_guess, opts, phi = super().prep_search(initial_geom, search_dir)
        derphi = self._grad_func(self.grad, initial_geom, search_dir)
        gfk = self.grad(initial_geom)
        derphi0 = derphi(np.zeros_like(a_guess), np.arange(len(a_guess)))

        # stp, fval, old_fval = scalar_search_wolfe1(
        #     phi, derphi, old_fval, old_old_fval, derphi0,
        #     c1=c1, c2=c2, amax=amax, amin=amin, xtol=xtol)

        # return stp, fc[0], gc[0], fval, old_fval, gval[0]

    def check_scalar_converged(self, phi_vals, alphas, **opts):
        """
        **LLM Docstring**

        Wolfe convergence test (not yet implemented).

        :param phi_vals: objective values
        :type phi_vals: np.ndarray
        :param alphas: step lengths
        :type alphas: np.ndarray
        """
        ...

def _run_step_line_search(searcher, guess, direction, gradient, mask):
    options = {'initial_grad': gradient}
    if isinstance(searcher, LineSearcher):
        options['function_mask'] = mask
    return searcher(guess, direction, **options)

class GradientDescentStepFinder:
    supports_hessian = False
    line_search = ArmijoSearch

    def __init__(self, func, jacobian, damping_parameter=None, damping_exponent=None,
                 line_search=True, restart_interval=10, logger=None):
        """
        **LLM Docstring**

        Initialize a gradient-descent step finder.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param damping_parameter: base step-damping factor
        :type damping_parameter: float | None
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float | None
        :param line_search: `True` to use the default line search, `False`/`None` to disable
        :type line_search: bool | Callable
        :param restart_interval: damping restart interval
        :type restart_interval: int
        :param logger: optional logger
        :type logger: object | None
        """
        self.func = func
        self.jac = jacobian
        self.damper = Damper(
            damping_parameter=damping_parameter,
            damping_exponent=damping_exponent,
            restart_interval=restart_interval
        )

        if line_search is True:
            line_search = self.line_search(func)
        elif line_search is False:
            line_search = None
        self.searcher = line_search
        self.logger = logger

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce a gradient-descent step (the negative gradient, optionally projected,
        line-searched, and damped) for the active members.

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices (or `(mask, chain_data)` for chain minimizers)
        :type mask: np.ndarray | tuple
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        if return_vals: raise NotImplementedError(...)
        if isinstance(mask, tuple):  # for chain minimizers
            mask, (j, _, _) = mask
            guess = guess[:, j]

        jacobian = self.jac(guess, mask)
        if gradient_modifer is not None:
            jacobian = gradient_modifer(jacobian, guess, mask)

        new_step_dir = -jacobian
        if projector is not None:
            new_step_dir = (new_step_dir[..., np.newaxis, :] @ projector).reshape(new_step_dir.shape)

        if self.searcher is not None:
            alpha, (fvals, is_converged) = _run_step_line_search(self.searcher, guess, new_step_dir, jacobian, mask)
            new_step_dir = alpha[:, np.newaxis] * new_step_dir

        # h = func(guess, mask)
        u = self.damper.get_damping_factor()
        if u is not None:
            new_step_dir = new_step_dir * u

        return new_step_dir, jacobian

class NetwonDirectHessianGenerator:

    line_search = ArmijoSearch
    def __init__(self, func, jacobian, hessian, hess_mode='direct', line_search=True,
                 damping_parameter=None, damping_exponent=None, restart_interval=10
                 ):
        """
        **LLM Docstring**

        Initialize a direct-Hessian Newton step generator.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param hessian: the Hessian function
        :type hessian: Callable
        :param hess_mode: `'direct'` (invert the Hessian) or `'inverse'` (already inverse)
        :type hess_mode: str
        :param line_search: line-search setting
        :type line_search: bool | Callable
        :param damping_parameter: step-damping factor
        :type damping_parameter: float | None
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float | None
        :param restart_interval: damping restart interval
        :type restart_interval: int
        """
        hessian = self.wrap_hessian(hessian, hess_mode)
        self.jacobian = jacobian
        self.hessian_inverse = hessian
        self.damper = Damper(
            damping_parameter=damping_parameter,
            damping_exponent=damping_exponent,
            restart_interval=restart_interval
        )
        if line_search is True:
            line_search = self.line_search(func)
        elif line_search is False:
            line_search = None
        self.searcher = line_search

    def wrap_hessian(self, func, mode):
        """
        **LLM Docstring**

        Wrap the Hessian function so it returns the (inverse) Hessian in the form the
        step generator expects.

        :param func: the Hessian (or inverse-Hessian) function
        :type func: Callable
        :param mode: `'direct'` to invert the Hessian, otherwise pass through
        :type mode: str
        :return: a function returning the inverse Hessian
        :rtype: Callable
        """
        if mode == 'direct':
            @functools.wraps(func)
            def hessian_inverse(guess, mask):
                """
                **LLM Docstring**

                Return the inverse of the Hessian at the given point.

                :param guess: the current point
                :type guess: np.ndarray
                :param mask: active-member indices
                :type mask: np.ndarray
                :return: the inverse Hessian
                :rtype: np.ndarray
                """
                h = func(guess, mask)
                # u = self.damper.get_damping_factor()
                # if u is not None:
                #     h = h + u * vec_ops.identity_tensors(guess.shape[:-1], guess.shape[-1])
                return np.linalg.inv(h)
        else:
            hessian_inverse = func
            # @functools.wraps(func)
            # def hessian_inverse(guess, mask):
            #     return h

        return hessian_inverse

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce the Newton step `-H⁻¹ g` (optionally projected, line-searched, damped).

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param return_vals: unsupported
        :type return_vals: bool
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """

        jacobian, hessian_inv = self.jacobian(guess, mask), self.hessian_inverse(guess, mask)
        if gradient_modifer is not None:
            jacobian = gradient_modifer(jacobian, guess, mask)

        new_step_dir = -(hessian_inv @ jacobian[:, :, np.newaxis]).reshape(jacobian.shape)
        if projector is not None:
            new_step_dir = (new_step_dir[:, np.newaxis, :] @ projector).reshape(new_step_dir.shape)
        if self.searcher is not None:
            alpha, (fvals, is_converged) = _run_step_line_search(self.searcher, guess, new_step_dir, jacobian, mask)
            new_step_dir = alpha[:, np.newaxis] * new_step_dir

        # h = func(guess, mask)
        u = self.damper.get_damping_factor()
        if u is not None:
            new_step_dir = new_step_dir * u

        return new_step_dir, jacobian

class NewtonStepFinder:
    supports_hessian = True
    def __init__(self, func, jacobian=None, hessian=None, *, check_generator=True, logger=None, **generator_opts):
        """
        **LLM Docstring**

        Initialize a Newton step finder, building a direct-Hessian generator from the
        supplied Jacobian/Hessian unless one is already provided.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function (or a ready generator)
        :type jacobian: Callable | None
        :param hessian: the Hessian function
        :type hessian: Callable | None
        :param check_generator: build a generator when needed
        :type check_generator: bool
        :param logger: optional logger
        :type logger: object | None
        :param generator_opts: extra options for the generator
        """
        if check_generator:
            generator = self._prep_generator(func, jacobian, hessian, generator_opts)
        else:
            generator = jacobian
        self.generator = generator
        self.logger = logger

    @classmethod
    def _prep_generator(cls, func, jac, hess, opts):
        """
        **LLM Docstring**

        Return a step generator for the Newton method, requiring a Hessian (or a func
        that already exposes `jacobian`/`hessian_inverse`).

        :param func: the objective function
        :type func: Callable
        :param jac: the gradient function
        :type jac: Callable
        :param hess: the Hessian function
        :type hess: Callable | None
        :param opts: extra generator options
        :type opts: dict
        :return: the step generator
        :rtype: object
        """
        if (hasattr(func, 'jacobian') and hasattr(func, 'hessian_inverse')):
            return func
        else:
            if hess is None:
                raise ValueError(
                    "Direct Netwon requires a Hessian or a generator for the Jacobian and Hessian inverse. "
                    "Consider using Quasi-Newton if only the Jacobian is fast to compute.")
            return NetwonDirectHessianGenerator(func, jac, hess, **opts)

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce a Newton step for the active members.

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices (or chain-minimizer tuple)
        :type mask: np.ndarray | tuple
        :param return_vals: unsupported
        :type return_vals: bool
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        if return_vals: raise NotImplementedError(...)
        if isinstance(mask, tuple):  # for chain minimizers
            mask, (j, _, _) = mask
            guess = guess[:, j]
        options = dict(return_vals=return_vals, projector=projector)
        if gradient_modifer is not None:
            options['gradient_modifer'] = gradient_modifer
        return self.generator(guess, mask, **options)

class QuasiNewtonStepFinder:
    supports_hessian = False

    def __init__(self, func, jacobian, approximation_type='bfgs', logger=None, **generator_opts):
        """
        **LLM Docstring**

        Initialize a quasi-Newton step finder, selecting the Hessian-approximation
        scheme by name.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param approximation_type: the approximator name (e.g. `'bfgs'`, `'sr1'`)
        :type approximation_type: str
        :param logger: optional logger
        :type logger: object | None
        :param generator_opts: extra options for the approximator
        """
        self.hess_appx = self.hessian_approximations[approximation_type.lower()](func, jacobian, **generator_opts)
    @classmethod
    def get_hessian_approximations(cls):
        """
        **LLM Docstring**

        Return the mapping from approximation name to Hessian-approximator class.

        :return: the name-to-class mapping
        :rtype: dict
        """
        return {
            'bfgs': BFGSApproximator,
            'broyden': BroydenApproximator,
            'dfp': DFPApproximator,
            'sr1': SR1Approximator,
            'psb': PSBQuasiNewtonApproximator,
            'bofill': BofillApproximator,
            'schelegel': SchelgelApproximator,
            'greenstadt': GreenstadtNewtonApproximator
        }
    @property
    def hessian_approximations(self):
        """
        **LLM Docstring**

        The mapping from approximation name to Hessian-approximator class.

        :return: the name-to-class mapping
        :rtype: dict
        """
        return self.get_hessian_approximations()

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce a quasi-Newton step for the active members via the chosen approximator.

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices (or chain-minimizer tuple)
        :type mask: np.ndarray | tuple
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        if return_vals: raise NotImplementedError(...)
        if isinstance(mask, tuple):  # for chain minimizers
            mask, (j, _, _) = mask
            guess = guess[:, j]
        return self.hess_appx(guess, mask, return_vals=return_vals, gradient_modifer=gradient_modifer, projector=projector)

class QuasiNetwonHessianApproximator:
    orthogonal_dirs_cutoff = 1e-16#1e-8
    line_search = ArmijoSearch
    def __init__(self, func, jacobian, initial_beta=1,
                 damping_parameter=None, damping_exponent=None,
                 line_search=True, restart_interval=10,
                 restart_hessian_norm=1e-12,
                 # approximation_mode='direct'
                 approximation_mode='inverse'
                 ):
        """
        **LLM Docstring**

        Initialize a quasi-Newton Hessian approximator, tracking the previous
        gradient/step/Hessian across iterations.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param initial_beta: initial (inverse) Hessian scale
        :type initial_beta: float
        :param damping_parameter: step-damping factor
        :type damping_parameter: float | None
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float | None
        :param line_search: line-search setting
        :type line_search: bool | Callable
        :param restart_interval: damping restart interval
        :type restart_interval: int
        :param restart_hessian_norm: step-norm below which the Hessian is reset
        :type restart_hessian_norm: float
        :param approximation_mode: `'direct'` (Hessian) or `'inverse'` (inverse Hessian)
        :type approximation_mode: str
        """
        self.func = func
        self.jac = jacobian
        self.initial_beta = initial_beta
        self.base_hess = None
        self.prev_jac = None
        self.prev_step = None
        self.prev_guess = None
        self.prev_hess_inv = None
        self.eye_tensors = None
        self.damper = Damper(
            damping_parameter=damping_parameter,
            damping_exponent=damping_exponent,
            restart_interval=restart_interval
        )
        if line_search is True:
            line_search = self.line_search(func)
        elif line_search is False:
            line_search = None
        self.searcher = line_search
        self.restart_hessian_norm = restart_hessian_norm
        self.approximation_mode = approximation_mode

    def identities(self, guess, mask):
        """
        **LLM Docstring**

        Return (cached) identity matrices matching the active members' shape.

        :param guess: the current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :return: the identity tensors
        :rtype: np.ndarray
        """
        if self.eye_tensors is None:
            self.eye_tensors = vec_ops.identity_tensors(guess.shape[:-1], guess.shape[-1])
            return self.eye_tensors
        else:
            return self.eye_tensors[mask,]

    def initialize_hessians(self, guess, mask):
        """
        **LLM Docstring**

        Return the initial (inverse) Hessian estimate (a scaled identity).

        :param guess: the current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :return: the initial Hessian estimate
        :rtype: np.ndarray
        """
        if self.approximation_mode == 'direct':
            return self.initial_beta * self.identities(guess, mask)
        else:
            return (1/self.initial_beta) * self.identities(guess, mask)

    @classmethod
    def take_nonzero_norm_regions(cls, norms, tensors, cutoff=None):
        """
        **LLM Docstring**

        Select the members whose supplied norms are all above a cutoff, returning their
        indices and the correspondingly filtered tensors (to avoid divide-by-zero in the
        Hessian update).

        :param norms: the norm arrays that must be nonzero
        :type norms: list[np.ndarray]
        :param tensors: tensors to filter to the safe members
        :type tensors: list[np.ndarray]
        :param cutoff: the nonzero cutoff
        :type cutoff: float | None
        :return: `(good_positions, filtered_tensors)`
        :rtype: tuple
        """
        if cutoff is None:
            cutoff = cls.orthogonal_dirs_cutoff
        mask = np.full(norms[0].reshape(-1,).shape, True)
        if cutoff is not None:
            for n in norms:
                mask = np.logical_and(mask, np.abs(n.reshape(-1)) > cutoff)

        # good_pos = np.where(np.logical_and(*[
        #     np.abs(n.reshape(-1, )) > cutoff
        #     for n in norms
        # ]))
        good_pos = np.where(mask)
        return good_pos, [t[good_pos] for t in tensors]

    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Abstract: compute the updated (inverse) Hessian from the gradient/step
        differences.

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous (inverse) Hessian
        :type prev_hess: np.ndarray
        :return: the updated Hessian
        :rtype: np.ndarray
        """
        raise NotImplementedError("abstract")

    def get_jacobian_updates(self, guess, mask, gradient_modifer=None):
        """
        **LLM Docstring**

        Evaluate the current gradient and its difference from the previous gradient.

        :param guess: the current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :return: `(new_jacobians, jacobian_differences)`
        :rtype: tuple
        """
        new_jacs = self.jac(guess, mask)
        if gradient_modifer is not None:
            new_jacs = gradient_modifer(new_jacs, guess, mask)
        if self.prev_jac is None:
            jac_diffs = new_jacs
        else:
            prev_jacs = self.prev_jac[mask,]
            jac_diffs = new_jacs - prev_jacs
        return new_jacs, jac_diffs

    def restart_hessian_approximation(self, displacement=None):
        """
        **LLM Docstring**

        Decide whether to reset the Hessian approximation (on a near-zero previous step
        or a numerical blow-up).

        :param displacement: actual previous step, if available
        :type displacement: np.ndarray | None
        :return: whether to restart
        :rtype: bool
        """
        if displacement is None:
            displacement = self.prev_step
        if np.any(displacement > 1e80): # a divide by zero in a previous Hessian update
            return True
        prev_norm = np.linalg.norm(displacement, axis=-1)
        restart = np.any(prev_norm < self.restart_hessian_norm)
        return restart

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce a quasi-Newton step: update the (inverse) Hessian, form the step `-B g`,
        optionally project/line-search/damp it, and cache the state for the next
        iteration.

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        new_jacs, jacobian_diffs = self.get_jacobian_updates(guess, mask, gradient_modifer=gradient_modifer)
        if self.prev_guess is None:
            new_hess = self.initialize_hessians(guess, mask)
        else:
            # The outer minimizer can cap or project the proposed step. Use the
            # displacement it actually took for the secant equation.
            prev_steps = guess - self.prev_guess[mask,]
            if self.restart_hessian_approximation(prev_steps):
                new_hess = self.initialize_hessians(guess, mask)
            else:
                prev_hess = self.prev_hess_inv[mask,]
                new_hess = self.get_hessian_update(
                    self.identities(guess, mask), jacobian_diffs,
                    prev_steps, prev_hess
                )

        if self.approximation_mode == 'direct':
            B = np.linalg.inv(new_hess)
        else:
            B = new_hess
        new_step_dir = -(B @ new_jacs[:, :, np.newaxis]).reshape(new_jacs.shape)
        if projector is not None:
            new_step_dir = (new_step_dir[:, np.newaxis, :] @ projector).reshape(new_step_dir.shape)
        if self.searcher is not None:
            alpha, (fvals, is_converged) = _run_step_line_search(self.searcher, guess, new_step_dir, new_jacs, mask)
        else:
            alpha = np.ones(len(new_step_dir))
        # handle convergence issues?
        new_step = alpha[:, np.newaxis] * new_step_dir
        # print(np.isnan(guess).any(), np.isnan(alpha).any(), np.linalg.norm(new_step_dir))
        u = self.damper.get_damping_factor()
        if u is not None:
            new_step = new_step * u

        if self.prev_jac is None:
            self.prev_jac = new_jacs
        else:
            self.prev_jac[mask,] = new_jacs

        if self.prev_step is None:
            self.prev_step = new_step
        else:
            self.prev_step[mask,] = new_step

        if self.prev_guess is None:
            self.prev_guess = guess.copy()
        else:
            self.prev_guess[mask,] = guess

        if self.prev_hess_inv is None:
            self.prev_hess_inv = new_hess
        else:
            self.prev_hess_inv[mask,] = new_hess

        return new_step, new_jacs

class BFGSApproximator(QuasiNetwonHessianApproximator):

    orthogonal_dirs_cutoff = 1e-16 #1e-8
    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Compute the BFGS (inverse) Hessian update from the gradient and step
        differences, guarding against zero curvature.

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous (inverse) Hessian
        :type prev_hess: np.ndarray
        :return: the updated Hessian
        :rtype: np.ndarray
        """
        I = identities
        dx = prev_steps[:, :, np.newaxis]
        dx_T = prev_steps[:, np.newaxis, :]
        y = jacobian_diffs[:, :, np.newaxis]
        y_T = jacobian_diffs[:, np.newaxis, :]
        B = prev_hess.copy()
        increment = False
        if self.approximation_mode == 'direct':
            diff_norm = y_T @ dx
            h_step = (B @ dx)
            h_norm = dx_T @ h_step
            good_pos, (
                I, H, dx, dx_T, y, y_T,
                h_step, h_norm, diff_norm
            ) = self.take_nonzero_norm_regions([diff_norm, h_norm],
                                               [I, B, dx, dx_T, y, y_T,
                                                h_step, h_norm, diff_norm])
            h_step_T = np.moveaxis(h_step, -1, -2)

            diff_outer = y_T * y
            step_outer = h_step_T * h_step
            diff_step = diff_outer / diff_norm
            step_step = step_outer / h_norm
            update = diff_step - step_step
            increment = True
        else:
            diff_norm = y_T @ dx
            good_pos, (
                I, H, dx, dx_T, y, y_T,
                diff_norm
            ) = self.take_nonzero_norm_regions([diff_norm],
                                               [I, B, dx, dx_T, y, y_T,
                                                diff_norm])

            diff_outer = np.moveaxis(dx_T * y, -1, -2)
            diff_step = I - diff_outer / diff_norm
            step_outer = dx_T * dx
            step_step = step_outer / diff_norm
            update = diff_step @ H @ np.moveaxis(diff_step, -1, -2) + step_step
            increment = False

        if increment:
            B[good_pos] += update
        else:
            B[good_pos] = update
        return B

class DFPApproximator(QuasiNetwonHessianApproximator):

    orthogonal_dirs_cutoff = 1e-8
    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """Apply the DFP secant equation, retaining members with singular denominators."""
        updated = prev_hess.copy()
        s, y = prev_steps, jacobian_diffs
        sy = np.einsum('bi,bi->b', s, y)
        valid = np.abs(sy) > self.orthogonal_dirs_cutoff
        if self.approximation_mode == 'direct':
            pos = np.flatnonzero(valid)
            if len(pos):
                sp, yp, denom = s[pos], y[pos], sy[pos]
                projector = identities[pos] - np.einsum('bi,bj->bij', yp, sp) / denom[:, None, None]
                updated[pos] = (
                    projector @ prev_hess[pos] @ np.swapaxes(projector, -1, -2)
                    + np.einsum('bi,bj->bij', yp, yp) / denom[:, None, None]
                )
        else:
            hy = np.einsum('bij,bj->bi', prev_hess, y)
            yhy = np.einsum('bi,bi->b', y, hy)
            pos = np.flatnonzero(valid & (np.abs(yhy) > self.orthogonal_dirs_cutoff))
            if len(pos):
                updated[pos] += (
                    np.einsum('bi,bj->bij', s[pos], s[pos]) / sy[pos, None, None]
                    - np.einsum('bi,bj->bij', hy[pos], hy[pos]) / yhy[pos, None, None]
                )
        return updated

class BroydenApproximator(QuasiNetwonHessianApproximator):

    orthogonal_dirs_cutoff = 1e-8
    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """Apply good Broyden in direct or inverse form, including nonsymmetric history."""
        updated = prev_hess.copy()
        s, y = prev_steps, jacobian_diffs
        if self.approximation_mode == 'direct':
            denominator = np.einsum('bi,bi->b', s, s)
            residual = y - np.einsum('bij,bj->bi', prev_hess, s)
            row = s
        else:
            hy = np.einsum('bij,bj->bi', prev_hess, y)
            denominator = np.einsum('bi,bi->b', s, hy)
            residual = s - hy
            # The right factor is s.T @ H, not (H @ s).T.
            row = np.einsum('bi,bij->bj', s, prev_hess)
        pos = np.flatnonzero(np.abs(denominator) > self.orthogonal_dirs_cutoff)
        if len(pos):
            updated[pos] += np.einsum('bi,bj->bij', residual[pos], row[pos]) / denominator[pos, None, None]
        return updated

class SR1Approximator(QuasiNetwonHessianApproximator):

    orthogonal_dirs_cutoff = 1e-8
    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Compute the symmetric-rank-one (SR1) (inverse) Hessian update.

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous (inverse) Hessian
        :type prev_hess: np.ndarray
        :return: the updated Hessian
        :rtype: np.ndarray
        """
        I = identities
        dx = prev_steps[:, :, np.newaxis]
        dx_T = prev_steps[:, np.newaxis, :]
        y = jacobian_diffs[:, :, np.newaxis]
        y_T = jacobian_diffs[:, np.newaxis, :]
        B = prev_hess.copy()
        if self.approximation_mode == 'direct':
            h_step = y - (B @ dx)
            h_step_T = np.moveaxis(h_step, -1, -2)
            h_norm = dx_T @ h_step
            good_pos, (
                I, H, dx, dx_T, y, y_T,
                h_step, h_step_T, h_norm
            ) = self.take_nonzero_norm_regions([h_norm],
                                               [I, B, dx, dx_T, y, y_T,
                                                h_step, h_step_T, h_norm])
            update = (h_step_T * h_step) / h_norm
        else:
            h_step = dx - (B @ y)
            h_step_T = np.moveaxis(h_step, -1, -2)
            h_norm = y_T @ h_step
            good_pos, (
                I, H, dx, dx_T, y, y_T,
                h_step, h_step_T, h_norm
            ) = self.take_nonzero_norm_regions([h_norm],
                                               [I, B, dx, dx_T, y, y_T,
                                                h_step, h_step_T, h_norm])
            update = (h_step_T * h_step) / h_norm

        B[good_pos] += update
        return B

class CompactQuasiNewtonApproximator(QuasiNetwonHessianApproximator):
    @classmethod
    def get_direct_hessian_update_vector(cls, H, dx, y):
        """
        **LLM Docstring**

        Abstract: the update vector for the direct (Hessian) form of a compact
        quasi-Newton update.

        :param H: the current Hessian
        :type H: np.ndarray
        :param dx: the step
        :type dx: np.ndarray
        :param y: the gradient difference
        :type y: np.ndarray
        :return: the update vector
        :rtype: np.ndarray
        """
        raise NotImplementedError("abstract")
    @classmethod
    def get_inverse_hessian_update_vector(cls, H, dx, y):
        """
        **LLM Docstring**

        Abstract: the update vector for the inverse form of a compact quasi-Newton
        update.

        :param H: the current inverse Hessian
        :type H: np.ndarray
        :param dx: the step
        :type dx: np.ndarray
        :param y: the gradient difference
        :type y: np.ndarray
        :return: the update vector
        :rtype: np.ndarray
        """
        raise NotImplementedError("abstract")

    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """Symmetric rank-two update satisfying the direct or inverse secant equation."""
        if self.approximation_mode == 'direct':
            displacement, difference = prev_steps, jacobian_diffs
            vector = self.get_direct_hessian_update_vector(
                prev_hess, prev_steps[..., None], jacobian_diffs[..., None]
            )[..., 0]
        else:
            displacement, difference = jacobian_diffs, prev_steps
            vector = self.get_inverse_hessian_update_vector(
                prev_hess, prev_steps[..., None], jacobian_diffs[..., None]
            )[..., 0]
        denominator = np.einsum('bi,bi->b', vector, displacement)
        pos = np.flatnonzero(np.abs(denominator) > self.orthogonal_dirs_cutoff)
        updated = prev_hess.copy()
        if len(pos):
            residual = difference[pos] - np.einsum('bij,bj->bi', prev_hess[pos], displacement[pos])
            v, denom = vector[pos], denominator[pos]
            overlap = np.einsum('bi,bi->b', residual, displacement[pos])
            updated[pos] += (
                (np.einsum('bi,bj->bij', residual, v) + np.einsum('bi,bj->bij', v, residual))
                / denom[:, None, None]
                - (overlap / denom**2)[:, None, None] * np.einsum('bi,bj->bij', v, v)
            )
        return updated

class PSBQuasiNewtonApproximator(CompactQuasiNewtonApproximator):
    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """Apply the symmetric PSB secant update in direct or inverse form."""
        updated = prev_hess.copy()
        if self.approximation_mode == 'direct':
            displacement, difference = prev_steps, jacobian_diffs
        else:
            displacement, difference = jacobian_diffs, prev_steps

        residual = difference - np.einsum('bij,bj->bi', updated, displacement)
        step_norm = np.einsum('bi,bi->b', displacement, displacement)
        valid = step_norm > self.orthogonal_dirs_cutoff
        safe_norm = np.where(valid, step_norm, 1)
        residual_step = np.einsum('bi,bi->b', residual, displacement)
        correction = (
            (np.einsum('bi,bj->bij', residual, displacement)
             + np.einsum('bi,bj->bij', displacement, residual)) / safe_norm[:, None, None]
            - (residual_step / safe_norm**2)[:, None, None]
            * np.einsum('bi,bj->bij', displacement, displacement)
        )
        updated[valid] += correction[valid]
        return updated

    @classmethod
    def get_direct_hessian_update_vector(cls, H, dx, y):
        """
        **LLM Docstring**

        The PSB compact update vector is the displacement.

        :param H: the current Hessian
        :param dx: the step
        :param y: the gradient difference
        :return: the displacement
        """
        return dx
    @classmethod
    def get_inverse_hessian_update_vector(cls, H, dx, y):
        """
        **LLM Docstring**

        The PSB (Powell symmetric Broyden) update vector, which is simply the step.

        :param H: the current inverse Hessian
        :type H: np.ndarray
        :param dx: the step
        :type dx: np.ndarray
        :param y: the gradient difference
        :type y: np.ndarray
        :return: the update vector (the step)
        :rtype: np.ndarray
        """
        return dx

class GreenstadtNewtonApproximator(CompactQuasiNewtonApproximator):
    @classmethod
    def get_direct_hessian_update_vector(cls, H, dx, y):
        """Return the gradient difference for the direct Greenstadt update."""
        return y

    @classmethod
    def get_inverse_hessian_update_vector(cls, H, dx, y):
        """
        **LLM Docstring**

        Not supported: Greenstadt only implements the direct update.

        :param H: the current inverse Hessian
        :param dx: the step
        :param y: the gradient difference
        :raises NotImplementedError: always
        """
        raise NotImplementedError("Greenstadt only does direct mode")

class WeightedQuasiNewtonApproximator(QuasiNetwonHessianApproximator):

    base_approximators = None
    def __init__(
            self,
            func, jacobian, initial_beta=1,
            damping_parameter=None, damping_exponent=None,
            line_search=True, restart_interval=10,
            restart_hessian_norm=1e-5,
            approximation_mode='direct'
    ):
        """
        **LLM Docstring**

        Initialize a weighted quasi-Newton approximator that blends several base
        approximators by per-member weights.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param initial_beta: initial (inverse) Hessian scale
        :type initial_beta: float
        :param damping_parameter: step-damping factor
        :type damping_parameter: float | None
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float | None
        :param line_search: line-search setting
        :type line_search: bool | Callable
        :param restart_interval: damping restart interval
        :type restart_interval: int
        :param restart_hessian_norm: step-norm reset threshold
        :type restart_hessian_norm: float
        :param approximation_mode: `'direct'` or `'inverse'`
        :type approximation_mode: str
        """
        super().__init__(
            func, jacobian,
            initial_beta=initial_beta,
            damping_parameter=damping_parameter, damping_exponent=damping_exponent,
            line_search=line_search, restart_interval=restart_interval,
            restart_hessian_norm=restart_hessian_norm,
            approximation_mode=approximation_mode
        )
        self.approximators = [
            app(
                None, None,
                initial_beta=initial_beta,
                damping_parameter=damping_parameter, damping_exponent=damping_exponent,
                line_search=line_search, restart_interval=restart_interval,
                restart_hessian_norm=restart_hessian_norm,
                approximation_mode=approximation_mode
            )
            for app in self.base_approximators
        ]

    def get_direct_weights(self, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Abstract: the blending weights for the direct-form base updates.

        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous Hessian
        :type prev_hess: np.ndarray
        :return: the per-approximator weights
        :rtype: np.ndarray
        """
        raise NotImplementedError("abstract")
    def get_inverse_weights(self, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Abstract: the blending weights for the inverse-form base updates.

        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous inverse Hessian
        :type prev_hess: np.ndarray
        :return: the per-approximator weights
        :rtype: np.ndarray
        """
        raise NotImplementedError("abstract")


    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Compute a weighted average of the base approximators' Hessian updates.

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous (inverse) Hessian
        :type prev_hess: np.ndarray
        :return: the weighted Hessian update
        :rtype: np.ndarray
        """
        if self.approximation_mode == 'direct':
            weights = self.get_direct_weights(jacobian_diffs, prev_steps, prev_hess)
        else:
            weights = self.get_inverse_weights(jacobian_diffs, prev_steps, prev_hess)

        base_updates = np.array([
            app.get_hessian_update(identities, jacobian_diffs, prev_steps, prev_hess)
            for app in self.approximators
        ])

        # Each approximator supplies one (batch, n, n) update and one weight
        # per batch member. Blend the complete updates, not their increments.
        weights = np.asarray(weights)
        return np.einsum('kb,kbij->bij', weights, base_updates)

class BofillApproximator(WeightedQuasiNewtonApproximator):
    base_approximators = [
        SR1Approximator,
        PSBQuasiNewtonApproximator
    ]
    def get_direct_weights(self, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Return the direct-Hessian SR1 and PSB weights for each batch member.

        :param jacobian_diffs: gradient differences
        :param prev_steps: previous steps
        :param prev_hess: previous Hessian
        :return: `[psi, 1 - psi]`, where psi weights SR1
        :rtype: list[np.ndarray]
        """
        psi = self.get_psi(jacobian_diffs, prev_steps, prev_hess)
        return [psi, 1 - psi]

    def get_psi(self, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Compute the Bofill mixing parameter psi (the SR1/PSB blend weight) from the
        step and gradient-difference geometry.

        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous Hessian
        :type prev_hess: np.ndarray
        :return: the psi weights
        :rtype: np.ndarray
        """
        if self.approximation_mode == 'direct':
            displacement, difference = prev_steps, jacobian_diffs
        else:
            displacement, difference = jacobian_diffs, prev_steps
        residual = difference - np.einsum('bij,bj->bi', prev_hess, displacement)
        residual_norm = np.einsum('bi,bi->b', residual, residual)
        step_norm = np.einsum('bi,bi->b', displacement, displacement)
        residual_step = np.einsum('bi,bi->b', residual, displacement)
        denominator = residual_norm * step_norm
        psi = np.zeros(len(prev_steps), dtype=np.result_type(prev_hess, float))
        valid = np.logical_and(
            denominator > self.orthogonal_dirs_cutoff,
            np.abs(residual_step) > SR1Approximator.orthogonal_dirs_cutoff
        )
        psi[valid] = residual_step[valid]**2 / denominator[valid]
        return np.clip(psi, 0, 1)

    def get_inverse_weights(self, jacobian_diffs, prev_steps, prev_hess):
            """
            **LLM Docstring**

            Return the Bofill blend weights `[psi, 1 - psi]` over its two base
            approximators.

            :param jacobian_diffs: gradient differences
            :type jacobian_diffs: np.ndarray
            :param prev_steps: previous steps
            :type prev_steps: np.ndarray
            :param prev_hess: previous Hessian
            :type prev_hess: np.ndarray
            :return: the two blend weights
            :rtype: list[np.ndarray]
            """
            psi = self.get_psi(jacobian_diffs, prev_steps, prev_hess)
            return [psi, 1-psi]

class SchelgelApproximator(BofillApproximator):
    base_approximators = [
        SR1Approximator,
        BFGSApproximator
    ]
    def get_direct_weights(self, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Not supported: the Schlegel blend is only defined for the inverse form here.

        :param jacobian_diffs: gradient differences
        :param prev_steps: previous steps
        :param prev_hess: previous Hessian
        :raises NotImplementedError: always
        """
        raise NotImplementedError("only inverse supported")

    def get_psi(self, jacobian_diffs, prev_steps, prev_hess):
        """Square root of the Bofill residual-overlap weight."""
        return np.sqrt(super().get_psi(jacobian_diffs, prev_steps, prev_hess))

    def get_inverse_weights(self, jacobian_diffs, prev_steps, prev_hess):
        psi = self.get_psi(jacobian_diffs, prev_steps, prev_hess)
        return [psi, 1 - psi]

class ConjugateGradientStepFinder:
    supports_hessian = False

    def __init__(self, func, jacobian, approximation_type='polak-ribiere', logger=None, **generator_opts):
        """
        **LLM Docstring**

        Initialize a conjugate-gradient step finder, selecting the beta formula by name.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param approximation_type: beta scheme (`'polak-ribiere'` or `'fletcher-reeves'`)
        :type approximation_type: str
        :param logger: optional logger
        :type logger: object | None
        :param generator_opts: extra options for the step approximator
        """
        self.step_appx = self.beta_approximations[approximation_type.lower()](func, jacobian, **generator_opts)
        self.logger = logger
    @property
    def beta_approximations(self):
        """
        **LLM Docstring**

        Return the mapping from beta-formula name to its approximator class.

        :return: the name-to-class mapping
        :rtype: dict
        """
        return {
            'fletcher-reeves':FletcherReevesApproximator,
            'polak-ribiere':PolakRibiereApproximator
        }

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce a conjugate-gradient step for the active members.

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices (or chain-minimizer tuple)
        :type mask: np.ndarray | tuple
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        if return_vals: raise NotImplementedError(...)
        if isinstance(mask, tuple):  # for chain minimizers
            mask, (j, _, _) = mask
            guess = guess[:, j]
        return self.step_appx(guess, mask, return_vals=return_vals, gradient_modifer=gradient_modifer, projector=projector)

class ConjugateGradientStepApproximator:
    line_search = ArmijoSearch

    def __init__(self, func, jacobian,
                 damping_parameter=None, damping_exponent=None,
                 restart_interval=50, restart_parameter=0.9,
                 line_search=True):
        """
        **LLM Docstring**

        Initialize a conjugate-gradient step approximator, tracking the previous
        gradient and search direction.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param damping_parameter: step-damping factor
        :type damping_parameter: float | None
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float | None
        :param restart_interval: iterations between forced restarts
        :type restart_interval: int
        :param restart_parameter: Powell-style restart threshold on gradient overlap
        :type restart_parameter: float
        :param line_search: line-search setting
        :type line_search: bool | Callable
        """
        self.func = func
        self.jac = jacobian
        self.base_hess = None
        self.prev_jac = None
        self.prev_step_dir = None
        self.damper = Damper(
            damping_parameter=damping_parameter,
            damping_exponent=damping_exponent,
            restart_interval=restart_interval
        )
        self.n = 0
        self.restart_interval = restart_interval
        self.restart_parameter = restart_parameter
        if line_search is True:
            line_search = self.line_search(func)
        elif line_search is False:
            line_search = None
        self.searcher = line_search

    def get_beta(self, new_jacs, prev_jac, prev_step_dir):
        """
        **LLM Docstring**

        Abstract: compute the conjugate-gradient beta coefficient.

        :param new_jacs: the current gradient
        :type new_jacs: np.ndarray
        :param prev_jac: the previous gradient
        :type prev_jac: np.ndarray
        :param prev_step_dir: the previous search direction
        :type prev_step_dir: np.ndarray
        :return: the beta coefficient
        :rtype: np.ndarray
        """
        raise NotImplementedError("abstract")

    def determine_restart(self, new_jacs, mask):
        """
        **LLM Docstring**

        Decide whether to restart the conjugate-gradient direction (on the first step or
        when successive gradients are insufficiently orthogonal, Powell's criterion).

        :param new_jacs: the current gradient
        :type new_jacs: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :return: whether to restart
        :rtype: bool
        """
        if self.n == 0: return True
        if self.restart_parameter is not None:
            prev_jac = self.prev_jac[mask,]
            new_norm = np.abs(new_jacs[:, np.newaxis, :] @ prev_jac[:, :, np.newaxis]).flatten()
            old_norm = (prev_jac[:, np.newaxis, :] @ prev_jac[:, :, np.newaxis]).flatten()
            return np.any(
                self.restart_parameter * old_norm < new_norm
            )

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce a conjugate-gradient step: form `-g + beta * previous_direction` (or a
        plain steepest-descent step on restart), then optionally project/line-search/damp
        and cache the state.

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        new_jacs = self.jac(guess, mask)

        if gradient_modifer is not None:
            new_jacs = gradient_modifer(new_jacs, guess, mask)

        if self.prev_jac is None or self.determine_restart(new_jacs, mask):
            new_step_dir = -new_jacs
        else:
            prev_jac = self.prev_jac[mask,]
            prev_step_dir = self.prev_step_dir[mask,]
            beta = self.get_beta(new_jacs, prev_jac, prev_step_dir)
            new_step_dir = -new_jacs + beta[:, np.newaxis] * prev_step_dir

        if projector is not None:
            new_step_dir = (new_step_dir[:, np.newaxis, :] @ projector).reshape(new_step_dir.shape)

        if self.searcher is not None:
            alpha, (fvals, is_converged) = _run_step_line_search(self.searcher, guess, new_step_dir, new_jacs, mask)
        else:
            alpha = np.ones(len(new_step_dir))
        # handle convergence issues?
        new_step = alpha[:, np.newaxis] * new_step_dir

        u = self.damper.get_damping_factor()
        if u is not None:
            new_step = new_step * u

        if self.prev_jac is None:
            self.prev_jac = new_jacs
        else:
            self.prev_jac[mask,] = new_jacs

        if self.prev_step_dir is None:
            self.prev_step_dir = new_step_dir
        else:
            self.prev_step_dir[mask,] = new_step_dir

        self.n = (self.n + 1) % self.restart_interval

        return new_step, new_jacs

class FletcherReevesApproximator(ConjugateGradientStepApproximator):
    def get_beta(self, new_jacs, prev_jac, prev_step_dir):
        """
        **LLM Docstring**

        Compute the Fletcher-Reeves beta (ratio of current to previous squared gradient
        norms).

        :param new_jacs: the current gradient
        :type new_jacs: np.ndarray
        :param prev_jac: the previous gradient
        :type prev_jac: np.ndarray
        :param prev_step_dir: the previous search direction
        :type prev_step_dir: np.ndarray
        :return: the beta coefficient
        :rtype: np.ndarray
        """
        return (
                (new_jacs[:, np.newaxis, :] @ new_jacs[:, :, np.newaxis]) /
                (prev_jac[:, np.newaxis, :] @ prev_jac[:, :, np.newaxis])
        ).reshape(len(new_jacs))

class PolakRibiereApproximator(ConjugateGradientStepApproximator):
    def get_beta(self, new_jacs, prev_jac, prev_step_dir):
        """
        **LLM Docstring**

        Compute the Polak-Ribiere beta (current gradient dotted with the gradient
        difference, over the previous squared gradient norm).

        :param new_jacs: the current gradient
        :type new_jacs: np.ndarray
        :param prev_jac: the previous gradient
        :type prev_jac: np.ndarray
        :param prev_step_dir: the previous search direction
        :type prev_step_dir: np.ndarray
        :return: the beta coefficient
        :rtype: np.ndarray
        """
        return (
                (new_jacs[:, np.newaxis, :] @ (new_jacs[:, :, np.newaxis] - prev_jac[:, :, np.newaxis])) /
                (prev_jac[:, np.newaxis, :] @ prev_jac[:, :, np.newaxis])
        ).reshape(len(new_jacs))

class EigenvalueFollowingStepFinder:

    supports_hessian = True
    line_search = ArmijoSearch
    def __init__(self, func, jacobian, hessian, initial_beta=1,
                 damping_parameter=None, damping_exponent=None,
                 line_search=False, restart_interval=1,
                 restart_hessian_norm=1e-5,
                 hessian_approximator='bofill',
                 approximation_mode='direct',
                 target_mode=None,
                 logger=None
                 # approximation_mode='inverse'
                 ):
        """
        **LLM Docstring**

        Initialize an eigenvector-following step finder. The selected Hessian mode
        is ascended while the remaining modes are descended.

        :param func: the objective function
        :type func: Callable
        :param jacobian: the gradient function
        :type jacobian: Callable
        :param hessian: the Hessian function
        :type hessian: Callable
        :param initial_beta: initial Hessian scale
        :type initial_beta: float
        :param damping_parameter: step-damping factor
        :type damping_parameter: float | None
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float | None
        :param line_search: energy Armijo search; normally leave disabled for saddles
        :type line_search: bool | Callable
        :param restart_interval: damping restart interval
        :type restart_interval: int
        :param restart_hessian_norm: step-norm reset threshold
        :type restart_hessian_norm: float
        :param hessian_approximator: quasi-Newton scheme for Hessian updates
        :type hessian_approximator: str
        :param approximation_mode: use direct or inverse secant updates
        :type approximation_mode: str
        :param target_mode: index/vector of the eigenmode to follow
        :type target_mode: int | np.ndarray | None
        :param logger: optional logger
        :type logger: object | None
        """
        self.hessian_approximator = hessian_approximator.lower()
        self.approximation_mode = approximation_mode
        if approximation_mode not in ('direct', 'inverse'):
            raise ValueError("approximation_mode must be 'direct' or 'inverse'")
        approximator = QuasiNewtonStepFinder.get_hessian_approximations()[self.hessian_approximator]
        self.base_approximator = approximator(
            func, jacobian, approximation_mode=approximation_mode
        )
        self.logger = logger

        self.func = func
        self.jac = jacobian
        self.hess = hessian
        self.initial_beta = initial_beta
        self.base_hess = None
        self.prev_jac = None
        self.prev_step = None
        self.prev_guess = None
        self.prev_evec = None
        self.prev_hess = None
        self.eye_tensors = None
        self.damper = Damper(
            damping_parameter=damping_parameter,
            damping_exponent=damping_exponent,
            restart_interval=restart_interval
        )
        if line_search is True:
            line_search = self.line_search(func)
        elif line_search is False:
            line_search = None
        self.searcher = line_search
        self.restart_hessian_norm = restart_hessian_norm
        self.target_mode = target_mode

    def identities(self, guess, mask):
        """
        **LLM Docstring**

        Return identity matrices matching the active members' shape.

        :param guess: the current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :return: the identity tensors
        :rtype: np.ndarray
        """
        return vec_ops.identity_tensors(guess.shape[:-1], guess.shape[-1])

    def initialize_hessians(self, guess, mask):
        """
        **LLM Docstring**

        Return the exact Hessian at the current point as the initial estimate.

        :param guess: the current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :return: the Hessian
        :rtype: np.ndarray
        """
        return self.hess(guess, mask)

    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        """
        **LLM Docstring**

        Update the Hessian estimate using the configured quasi-Newton approximator.

        :param identities: identity matrices
        :type identities: np.ndarray
        :param jacobian_diffs: gradient differences
        :type jacobian_diffs: np.ndarray
        :param prev_steps: previous steps
        :type prev_steps: np.ndarray
        :param prev_hess: previous Hessian
        :type prev_hess: np.ndarray
        :return: the updated Hessian
        :rtype: np.ndarray
        """
        if self.approximation_mode == 'inverse':
            updated = self.base_approximator.get_hessian_update(
                identities, jacobian_diffs, prev_steps, np.linalg.pinv(prev_hess)
            )
            return np.linalg.pinv(updated)
        return self.base_approximator.get_hessian_update(
            identities, jacobian_diffs, prev_steps, prev_hess
        )

    negative_eigenvalue_offset = 0.015
    positive_eigenvalue_offset = 0.005
    mode_tracking_overlap_cutoff = 1e-5
    def get_shift(self, evals, tf_new, target_mode):
        """
        **LLM Docstring**

        Return per-mode shifts and the selected eigenvectors. The followed mode has
        negative effective curvature (ascent); all others have positive effective
        curvature (descent). Small curvatures are bounded away from zero.

        :param evals: the Hessian eigenvalues
        :type evals: np.ndarray
        :param tf_new: the eigenvectors
        :type tf_new: np.ndarray
        :param target_mode: the mode being followed (or `None`)
        :type target_mode: np.ndarray | None
        :return: `(shifts, followed_eigenvectors)`
        :rtype: tuple[np.ndarray, np.ndarray]
        """
        batch_size, dimensions = evals.shape
        if target_mode is None:
            mode_indices = np.zeros(batch_size, dtype=int)
        elif np.ndim(target_mode) == 0:
            mode_index = int(target_mode)
            if mode_index < 0 or mode_index >= dimensions:
                raise ValueError('target_mode index is outside the Hessian spectrum')
            mode_indices = np.full(batch_size, mode_index, dtype=int)
        else:
            target_mode = np.asarray(target_mode)
            if target_mode.shape == (dimensions,):
                target_mode = np.broadcast_to(target_mode, (batch_size, dimensions))
            if target_mode.shape != (batch_size, dimensions):
                raise ValueError('target_mode must be a vector or one vector per batch member')
            norms = np.linalg.norm(target_mode, axis=1)
            if np.any(norms == 0):
                raise ValueError('target_mode vectors must be nonzero')
            overlaps = np.abs(np.einsum('bij,bi->bj', tf_new, target_mode / norms[:, None]))
            mode_indices = np.argmax(overlaps, axis=1)
            mode_indices[overlaps[np.arange(batch_size), mode_indices] < self.mode_tracking_overlap_cutoff] = 0

        rows = np.arange(batch_size)
        effective_curvatures = np.maximum(np.abs(evals), self.positive_eigenvalue_offset)
        effective_curvatures[rows, mode_indices] = -np.maximum(
            np.abs(evals[rows, mode_indices]), self.negative_eigenvalue_offset
        )
        followed_eigenvectors = tf_new[rows, :, mode_indices]
        return effective_curvatures - evals, followed_eigenvectors

    def get_jacobian_updates(self, guess, mask, gradient_modifer=None):
        """
        **LLM Docstring**

        Evaluate the current gradient and its difference from the previous gradient.

        :param guess: the current parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :return: `(new_jacobians, jacobian_differences)`
        :rtype: tuple
        """
        new_jacs = self.jac(guess, mask)
        if gradient_modifer is not None:
            new_jacs = gradient_modifer(new_jacs, guess, mask)
        if self.prev_jac is None:
            jac_diffs = new_jacs
        else:
            prev_jacs = self.prev_jac[mask,]
            jac_diffs = new_jacs - prev_jacs
        return new_jacs, jac_diffs

    def restart_hessian_approximation(self, displacement):
        """
        **LLM Docstring**

        Decide whether to reset the Hessian approximation after a near-zero actual
        displacement.

        :param displacement: actual displacement since the last call
        :type displacement: np.ndarray
        :return: whether to restart
        :rtype: bool
        """
        restart = np.any(np.linalg.norm(displacement, axis=-1) < self.restart_hessian_norm)
        return restart

    def __call__(self, guess, mask, return_vals=False, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Produce an eigenvalue-following step: update the Hessian, diagonalize it, apply
        the eigenvalue shift, and build the step in the eigenbasis (optionally
        projected/line-searched/damped).

        :param guess: current parameters
        :type guess: np.ndarray
        :param mask: active-member indices (or chain-minimizer tuple)
        :type mask: np.ndarray | tuple
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        if return_vals: raise NotImplementedError(...)
        if isinstance(mask, tuple):  # for chain minimizers
            mask, (j, _, _) = mask
            guess = guess[:, j]

        new_jacs, jacobian_diffs = self.get_jacobian_updates(guess, mask, gradient_modifer=gradient_modifer)
        if self.prev_guess is None:
            new_hess = self.initialize_hessians(guess, mask)
        else:
            # The outer optimizer may cap or project the proposed step. Use the
            # displacement that was actually taken in the secant update.
            displacement = guess - self.prev_guess[mask,]
            if self.restart_hessian_approximation(displacement):
                new_hess = self.initialize_hessians(guess, mask)
            else:
                try:
                    new_hess = self.get_hessian_update(
                        self.identities(guess, mask), jacobian_diffs,
                        displacement, self.prev_hess[mask,]
                    )
                except np.linalg.LinAlgError:
                    # Inverse secant models can become singular or overflow.
                    # Rebuild from the supplied physical Hessian at this point.
                    new_hess = self.initialize_hessians(guess, mask)
        invalid = ~np.all(np.isfinite(new_hess), axis=(-2, -1))
        if np.any(invalid):
            new_hess[invalid] = self.initialize_hessians(guess[invalid], mask[invalid])
        new_hess = (new_hess + np.swapaxes(new_hess, -1, -2)) / 2

        evals, tf = np.linalg.eigh(new_hess)
        if self.prev_evec is not None and self.target_mode is not None:
            target_mode = self.prev_evec[mask,]
        else:
            target_mode = self.target_mode
            if isinstance(target_mode, np.ndarray) and target_mode.ndim == 2 and target_mode.shape[0] != len(mask):
                target_mode = target_mode[mask,]
        shift, followed_eigenvectors = self.get_shift(evals, tf, target_mode)

        mode_gradient = np.einsum('bij,bi->bj', tf, new_jacs)
        mode_step = -mode_gradient / (evals + shift)
        new_step_dir = np.einsum('bij,bj->bi', tf, mode_step)

        # print(new_hess)
        if projector is not None:
            new_step_dir = (new_step_dir[:, np.newaxis, :] @ projector).reshape(new_step_dir.shape)
        if self.searcher is not None:
            alpha, (fvals, is_converged) = _run_step_line_search(self.searcher, guess, new_step_dir, new_jacs, mask)
        else:
            alpha = np.ones(len(new_step_dir))
        # handle convergence issues?
        new_step = alpha[:, np.newaxis] * new_step_dir
        # print(np.isnan(guess).any(), np.isnan(alpha).any(), np.linalg.norm(new_step_dir))
        u = self.damper.get_damping_factor()
        if u is not None:
            new_step = new_step * u

        if self.prev_jac is None:
            self.prev_jac = new_jacs
        else:
            self.prev_jac[mask,] = new_jacs

        if self.prev_step is None:
            self.prev_step = new_step
        else:
            self.prev_step[mask,] = new_step

        if self.prev_guess is None:
            self.prev_guess = guess.copy()
        else:
            self.prev_guess[mask,] = guess

        if self.prev_evec is None:
            self.prev_evec = followed_eigenvectors
        else:
            self.prev_evec[mask,] = followed_eigenvectors

        if self.prev_hess is None:
            self.prev_hess = new_hess
        else:
            self.prev_hess[mask,] = new_hess

        return new_step, new_jacs

class ChainMinimizingStepFinder:
    supports_hessian = True
    def __init__(self,
                 func,
                 jacobian,
                 hessian=None,
                 step_finder='conjugate-gradient',
                 logger=None,
                 **opts
                 ):
        """
        **LLM Docstring**

        Initialize a chain step finder that minimizes each image with a base step
        finder while adding inter-image (neighbour) contributions.

        :param func: the per-image objective
        :type func: Callable
        :param jacobian: the per-image gradient
        :type jacobian: Callable
        :param hessian: the per-image Hessian
        :type hessian: Callable | None
        :param step_finder: the base per-image method
        :type step_finder: str
        :param logger: optional logger
        :type logger: object | None
        :param opts: extra options for the base step finder
        """
        self.step_finder = get_step_finder({
            'method':step_finder,
            'func':self.wrap_func(func),
            'jacobian':self.wrap_jac(jacobian),
            'hessian':self.wrap_hess(hessian),
            **opts
        })
        self._mask_data = None
        self.logger = logger

    def adjust_jacobian(self, jac, guess, mask, cur, prev, next):
        """
        **LLM Docstring**

        Hook to adjust the per-image gradient given its neighbours (identity by default).

        :param jac: the base gradient
        :type jac: np.ndarray
        :param guess: the full chain
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param cur: current image index
        :type cur: int
        :param prev: previous image index
        :type prev: int | None
        :param next: next image index
        :type next: int | None
        :return: the adjusted gradient
        :rtype: np.ndarray
        """
        return jac

    def adjust_hessian(self, hess, guess, mask, cur, prev, next):
        """
        **LLM Docstring**

        Hook to adjust the per-image Hessian given its neighbours (identity by default).

        :param hess: the base Hessian
        :type hess: np.ndarray
        :param guess: the full chain
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param cur: current image index
        :type cur: int
        :param prev: previous image index
        :type prev: int | None
        :param next: next image index
        :type next: int | None
        :return: the adjusted Hessian
        :rtype: np.ndarray
        """
        return hess

    @abc.abstractmethod
    def image_pairwise_contribution(self, guess, mask, cur, prev, next, order=0):
        """
        **LLM Docstring**

        Abstract: the inter-image (neighbour) contribution to the objective/gradient/
        Hessian at the requested derivative order.

        :param guess: the full chain
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param cur: current image index
        :type cur: int
        :param prev: previous image index
        :type prev: int | None
        :param next: next image index
        :type next: int | None
        :param order: derivative order (`0`=value, `1`=gradient, `2`=Hessian)
        :type order: int
        :return: the contribution
        :rtype: np.ndarray | int
        """
        raise NotImplementedError("abstract")

    def _image_geometries(self, guess, mask):
        """Reconstruct a trial chain by moving only the active image."""
        if np.ndim(guess) == 3:
            return guess
        ids = np.asarray(mask, dtype=int)
        order = np.argsort(self._current_mask)
        positions = np.searchsorted(self._current_mask[order], ids)
        if np.any(positions >= len(order)):
            raise ValueError('chain trial contains unknown member IDs')
        indices = order[positions]
        if not np.array_equal(self._current_mask[indices], ids):
            raise ValueError('chain trial contains unknown member IDs')
        trial = self._current_chain[indices].copy()
        trial[:, self._mask_data[0]] = guess
        return trial

    def wrap_func(self, func):
        """
        **LLM Docstring**

        Wrap the per-image objective so it also includes the inter-image contribution.

        :param func: the per-image objective
        :type func: Callable
        :return: the wrapped objective
        :rtype: Callable
        """
        @functools.wraps(func)
        def wrapped_func(guess, mask):
            """
            **LLM Docstring**

            Evaluate the per-image objective plus its inter-image contribution.

            :param guess: the full chain
            :type guess: np.ndarray
            :param mask: active-member indices
            :type mask: np.ndarray
            :return: the combined objective value
            :rtype: np.ndarray
            """
            j, prev, next = self._mask_data
            guess = self._image_geometries(guess, mask)
            return func(guess[:, j], mask) + self.image_pairwise_contribution(guess, mask, j, prev, next, order=0)
        return wrapped_func

    def wrap_jac(self, jac):
        """
        **LLM Docstring**

        Wrap the per-image gradient so it includes the adjusted base gradient plus the
        inter-image contribution.

        :param jac: the per-image gradient
        :type jac: Callable
        :return: the wrapped gradient
        :rtype: Callable
        """
        @functools.wraps(jac)
        def wrapped_jac(guess, mask):
            """
            **LLM Docstring**

            Evaluate the adjusted per-image gradient plus its inter-image contribution.

            :param guess: the full chain
            :type guess: np.ndarray
            :param mask: active-member indices
            :type mask: np.ndarray
            :return: the combined gradient
            :rtype: np.ndarray
            """
            j, prev, next = self._mask_data
            guess = self._image_geometries(guess, mask)
            base_jac = self.adjust_jacobian(
                jac(guess[:, j], mask),
                guess, mask, j, prev, next
            )
            new_jac = self.image_pairwise_contribution(guess, mask, j, prev, next, order=1)
            # print(base_jac)
            # print(new_jac)
            # print("-"*20)
            return base_jac + new_jac
        return wrapped_jac

    def wrap_hess(self, hess):
        """
        **LLM Docstring**

        Wrap the per-image Hessian so it includes the adjusted base Hessian plus the
        inter-image contribution (or `None` when no Hessian is provided).

        :param hess: the per-image Hessian
        :type hess: Callable | None
        :return: the wrapped Hessian (or `None`)
        :rtype: Callable | None
        """
        if hess is None:
            return hess
        @functools.wraps(hess)
        def wrapped_hess(guess, mask):
            """
            **LLM Docstring**

            Evaluate the adjusted per-image Hessian plus its inter-image contribution.

            :param guess: the full chain
            :type guess: np.ndarray
            :param mask: active-member indices
            :type mask: np.ndarray
            :return: the combined Hessian
            :rtype: np.ndarray
            """
            j, prev, next = self._mask_data
            guess = self._image_geometries(guess, mask)
            return self.adjust_hessian(
                hess(guess[:, j], mask),
                guess, mask, j, prev, next
            ) + self.image_pairwise_contribution(guess, mask, j, prev, next, order=2)
        return wrapped_hess

    def climbing_node_step(self, guess, mask, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Abstract: the step for a climbing image (not implemented in the base class).

        :param guess: the climbing-image parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector
        :type projector: np.ndarray | None
        :raises NotImplementedError: always in the base class
        """
        raise NotImplementedError(f"climbing not implemented for {type(self).__name__}")

    def __call__(self, guess, mask, projector=None, return_vals=False, gradient_modifer=None, is_climbing=None):
        """
        **LLM Docstring**

        Produce steps for a batch of chain images, routing climbing images through the
        climbing step and the rest through the base step finder.

        :param guess: the chain images
        :type guess: np.ndarray
        :param mask: `(mask, chain_data)` identifying active members and neighbours
        :type mask: tuple
        :param projector: optional projector applied to the step
        :type projector: np.ndarray | None
        :param return_vals: unsupported
        :type return_vals: bool
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param is_climbing: per-member climbing flags
        :type is_climbing: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        if return_vals: raise NotImplementedError(...)

        mask, self._mask_data = mask
        self._current_mask = np.asarray(mask, dtype=int)
        self._current_chain = np.asarray(guess)
        self._climbing_mask = self._current_mask[np.asarray(is_climbing, dtype=bool)] if is_climbing is not None else np.array([], dtype=int)
        guess = guess[:, self._mask_data[0]]

        if is_climbing is not None and np.any(is_climbing):
            if np.all(is_climbing):
                return self.climbing_node_step(guess, mask, gradient_modifer=gradient_modifer, projector=projector)
            else:
                submask = [m for m,c in zip(mask, is_climbing) if c]
                subguess = np.array([g for g,c in zip(guess, is_climbing) if c])
                rem_mask = [m for m,c in zip(mask, is_climbing) if not c]
                remguess = np.array([g for g,c in zip(guess, is_climbing) if not c])

                ord = np.argsort(np.argsort(is_climbing, kind='mergesort'))
                substep, subgrad = self.climbing_node_step(subguess, submask, gradient_modifer=gradient_modifer, projector=projector)
                remstep, remgrad = self.step_finder(remguess, rem_mask, gradient_modifer=gradient_modifer, projector=projector)

                return (
                    np.concatenate([remstep, substep], axis=0)[ord,],
                    np.concatenate([remgrad, subgrad], axis=0)[ord,]
                )
        else:
            return self.step_finder(guess, mask, gradient_modifer=gradient_modifer, projector=projector)

class NudgedElasticBandStepFinder(ChainMinimizingStepFinder):
    def __init__(self, func, jacobian, hessian=None, spring_constants=.1,
                 distance_function=None, step_finder='gradient-descent', logger=None,
                 step_size=None, line_search=None, **opts):
        """Relax NEB forces with fixed-step integration or a custom force search.

        NEB forces are not the gradient of the per-image energy. An energy Armijo
        search is therefore unsuitable, including for climbing images. The default
        gradient-descent integration scale is .001; adapt it to the potential's
        curvature, as with ``StringMethodStepFinder``.
        """
        if line_search is True:
            raise ValueError('NEB requires a force-compatible search; use line_search=False with step_size, or a custom searcher')
        if line_search is None:
            line_search = False
        if step_size is None and step_finder == 'gradient-descent' and 'damping_parameter' not in opts:
            step_size = .001
        if step_size is not None:
            opts.setdefault('damping_parameter', step_size)
            opts.setdefault('damping_exponent', 0)
        self.image_potential = func
        super().__init__(func, jacobian, hessian=hessian, step_finder=step_finder,
                         line_search=line_search, **opts)
        self.spring_constants = spring_constants
        self._spring_constants = None
        self.distance_function = distance_function
        self._last_tangent = None
        self.logger = logger

    def get_dist(self, p1, p2):
        """
        **LLM Docstring**

        Return the Euclidean distance between two image geometries.

        :param p1: the first geometry
        :type p1: np.ndarray
        :param p2: the second geometry
        :type p2: np.ndarray
        :return: the distance
        :rtype: np.ndarray
        """
        return np.linalg.norm(p1 - p2, axis=-1)

    def get_tangent(self, guess, mask, cur, prev, next):
        """Energy-weighted NEB tangents independently for each chain."""
        current, previous, following = guess[:, cur], guess[:, prev], guess[:, next]
        ep, ec, en = (self.image_potential(p, mask) for p in (previous, current, following))
        forward, backward = following - current, current - previous
        dn, dp = np.abs(en - ec), np.abs(ep - ec)
        high, low = np.maximum(dn, dp), np.minimum(dn, dp)
        weighted = np.where((en > ep)[:, None],
                            forward * high[:, None] + backward * low[:, None],
                            forward * low[:, None] + backward * high[:, None])
        tangent = np.where(((en > ec) & (ec > ep))[:, None], forward,
                           np.where(((en <= ec) & (ec <= ep))[:, None], backward, weighted))
        norm = np.linalg.norm(tangent, axis=-1, keepdims=True)
        fallback = following - previous
        tangent = np.where(norm > 1e-12, tangent, fallback)
        return tangent / np.maximum(np.linalg.norm(tangent, axis=-1, keepdims=True), 1e-12)

    def adjust_jacobian(self, jac, guess, mask, cur, prev, next):
        if prev is None or next is None:
            return jac
        tangent = self.get_tangent(guess, mask, cur, prev, next)
        projected = jac - np.sum(jac * tangent, axis=-1, keepdims=True) * tangent
        climbing = np.isin(mask, getattr(self, '_climbing_mask', []))
        # Climbing images need the original potential gradient before reflection.
        return np.where(climbing[:, None], jac, projected)

    def climbing_node_step(self, guess, mask, gradient_modifer=None, projector=None):
        """
        **LLM Docstring**

        Take a climbing-image step: invert the tangential force component so the image
        climbs toward the saddle along the path.

        :param guess: the climbing-image parameters
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param gradient_modifer: optional gradient transformation
        :type gradient_modifer: Callable | None
        :param projector: optional projector
        :type projector: np.ndarray | None
        :return: `(step, gradient)`
        :rtype: tuple
        """
        j, prev, next = self._mask_data
        tangent = self.get_tangent(self._image_geometries(guess, mask), mask, j, prev, next)
        def modify_gradient(subgrad, guess, mask):
            """
            **LLM Docstring**

            Flip the sign of the gradient's tangential component (the climbing-image force
            modification).

            :param subgrad: the gradient to modify
            :type subgrad: np.ndarray
            :param guess: the current parameters
            :type guess: np.ndarray
            :param mask: active-member indices
            :type mask: np.ndarray
            :return: the modified gradient
            :rtype: np.ndarray
            """
            if gradient_modifer is not None:
                subgrad = gradient_modifer(subgrad, guess, mask)
            sg = subgrad[..., np.newaxis, :]
            tg = tangent[..., :, np.newaxis]
            tangential_force = np.reshape(sg @ tg, tangent.shape[:-1] + (1,))
            return subgrad - 2 * tangential_force * tangent
        return self.step_finder(guess, mask, gradient_modifer=modify_gradient, projector=projector)

    def image_pairwise_contribution(self, guess, mask, cur, prev, next, order=0):
        """
        **LLM Docstring**

        Compute the NEB spring contribution to the objective/gradient/Hessian from the
        difference of the distances to the two neighbouring images.

        :param guess: the full chain
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param cur: current image index
        :type cur: int
        :param prev: previous image index
        :type prev: int | None
        :param next: next image index
        :type next: int | None
        :param order: derivative order (`0`=value, `1`=gradient, `2`=Hessian)
        :type order: int
        :return: the spring contribution
        :rtype: np.ndarray | int
        """
        if order > 2: return 0

        if prev is None or next is None:
            return 0

        cur_geom, prev_geom, next_geom = guess[:, cur], guess[:, prev], guess[:, next]

        prev_dist = self.get_dist(cur_geom, prev_geom)
        next_dist = self.get_dist(cur_geom, next_geom)

        dist = prev_dist - next_dist
        if misc.is_numeric(self.spring_constants):
            const = self.spring_constants
        else:
            const = self.spring_constants[cur]

        contribution = 0
        if order == 0:
            contribution = (const/2) * (dist**2)
        elif order == 1:
            tangent = self.get_tangent(guess, mask, cur, prev, next)
            contribution = const * dist[..., np.newaxis] * tangent
            climbing = np.isin(mask, getattr(self, '_climbing_mask', []))
            contribution[climbing] = 0
        elif order == 2:
            contribution = const * vec_ops.identity_tensors(guess.shape[0], guess.shape[-1])
        return contribution

class StringMethodStepFinder(NudgedElasticBandStepFinder):
    """Relax a string normal to its path; reparameterization controls spacing."""

    def __init__(self, func, jacobian, hessian=None, *, step_size=.001,
                 step_finder='gradient-descent', logger=None, **opts):
        super().__init__(
            func, jacobian, hessian=hessian, spring_constants=0,
            step_finder=step_finder, logger=logger,
            line_search=False, damping_parameter=step_size,
            damping_exponent=0, **opts
        )

    def get_tangent(self, guess, mask, cur, prev, next):
        tangent = guess[:, next] - guess[:, prev]
        norm = np.linalg.norm(tangent, axis=-1, keepdims=True)
        return tangent / np.maximum(norm, 1e-12)

    def adjust_jacobian(self, jac, guess, mask, cur, prev, next):
        if prev is None or next is None:
            return jac
        tangent = self.get_tangent(guess, mask, cur, prev, next)
        return jac - np.sum(jac * tangent, axis=-1, keepdims=True) * tangent

    def image_pairwise_contribution(self, guess, mask, cur, prev, next, order=0):
        return 0


class AdjustedChainStepFinder(ChainMinimizingStepFinder):
    def __init__(self,
                 pairwise_image_function,
                 func,
                 jacobian,
                 hessian=None,
                 logger=None,
                 **opts
                 ):
        """
        **LLM Docstring**

        Initialize a chain step finder whose inter-image contribution is supplied by an
        external pairwise function.

        :param pairwise_image_function: the inter-image contribution function
        :type pairwise_image_function: Callable
        :param func: the per-image objective
        :type func: Callable
        :param jacobian: the per-image gradient
        :type jacobian: Callable
        :param hessian: the per-image Hessian
        :type hessian: Callable | None
        :param logger: optional logger
        :type logger: object | None
        :param opts: extra options for the base step finder
        """
        super().__init__(
            func,
            jacobian,
            hessian=hessian,
            **opts
        )
        self.pairwise_function = pairwise_image_function
        self.logger = logger

    def image_pairwise_contribution(self,guess, mask, cur, prev, next, order=0):
        """
        **LLM Docstring**

        Delegate the inter-image contribution to the supplied pairwise function.

        :param guess: the full chain
        :type guess: np.ndarray
        :param mask: active-member indices
        :type mask: np.ndarray
        :param cur: current image index
        :type cur: int
        :param prev: previous image index
        :type prev: int | None
        :param next: next image index
        :type next: int | None
        :param order: derivative order
        :type order: int
        :return: the contribution
        :rtype: np.ndarray | int
        """
        return self.pairwise_function(guess, mask, cur, prev, next, order=order)

class ChainReparametrizer:
    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> '(np.ndarray, np.ndarray, np.ndarray)':
        """
        **LLM Docstring**

        Abstract: redistribute the images along the chain (implemented by subclasses).

        :param args: reparametrization inputs
        :param kwargs: reparametrization options
        :return: the reparametrized chain data
        :rtype: tuple
        """
        ...

class InterpolatingReparametrizer(ChainReparametrizer):
    def __init__(self, interpolator_type=None, movement_tolerance=1e-8):
        """
        **LLM Docstring**

        Initialize a reparametrizer that redistributes images by interpolation.

        :param interpolator_type: optional callable built from arc positions and images
        :type interpolator_type: type
        :param movement_tolerance: displacement below which an image need not relax again
        :type movement_tolerance: float
        """
        self.interpolator_type = interpolator_type
        self.movement_tolerance = movement_tolerance

    def __call__(self, images, fixed_positions):
        """
        **LLM Docstring**

        Redistribute each chain by arc length, holding fixed images in place.

        :param images: the current chain images
        :type images: np.ndarray
        :param fixed_positions: image indices to keep unchanged
        :type fixed_positions: Iterable[int]
        :return: `(images, moved_images, fixed_positions)`
        :rtype: tuple
        """
        images = np.asarray(images)
        if images.ndim != 3:
            raise ValueError("images must have shape (batch, n_images, n_coordinates)")
        fixed_positions = [] if fixed_positions is None else list(fixed_positions)
        boundaries = sorted(set([0, images.shape[1] - 1] + fixed_positions))
        new_images = images.copy()
        for batch in range(images.shape[0]):
            for first, last in zip(boundaries[:-1], boundaries[1:]):
                segment = images[batch, first:last + 1]
                distances = np.linalg.norm(np.diff(segment, axis=0), axis=-1)
                arc = np.concatenate(([0.], np.cumsum(distances)))
                if arc[-1] == 0:
                    continue
                # np.interp requires strictly increasing abscissae.
                unique_arc, unique_indices = np.unique(arc, return_index=True)
                nodes = segment[unique_indices]
                targets = np.linspace(0, arc[-1], len(segment))
                if self.interpolator_type is None:
                    new_images[batch, first:last + 1] = np.stack([
                        np.interp(targets, unique_arc, nodes[:, coord])
                        for coord in range(images.shape[-1])
                    ], axis=-1)
                else:
                    interpolator = self.interpolator_type(unique_arc, nodes)
                    new_images[batch, first:last + 1] = interpolator(targets)
                new_images[batch, first] = segment[0]
                new_images[batch, last] = segment[-1]
        moved = np.linalg.norm(new_images - images, axis=-1) > self.movement_tolerance
        moved[:, boundaries] = False
        return new_images, moved, fixed_positions


def string_method_minimize(start, end, function, jacobian, *, n_images=12,
                           initial_images=None, step_size=.001,
                           reparametrizer=None, **optimizer_options):
    """Interpolate endpoints, relax normal to the path, and redistribute nodes.

    Returns the same ``((images, image_counts), converged, (errors, iterations))``
    structure as ``iterative_chain_minimize``. Endpoints remain fixed.
    """
    if initial_images is None:
        start = np.asarray(start, dtype=float)
        end = np.asarray(end, dtype=float)
        if start.shape != end.shape or start.ndim < 1:
            raise ValueError("start and end must have matching coordinate shapes")
        if n_images < 3:
            raise ValueError("string methods require at least three images")
        positions = np.linspace(0, 1, n_images)
        initial_images = (
            start[..., np.newaxis, :] * (1 - positions)[..., np.newaxis]
            + end[..., np.newaxis, :] * positions[..., np.newaxis]
        )
    else:
        initial_images = np.asarray(initial_images, dtype=float)
        if initial_images.ndim < 2:
            raise ValueError("initial_images must contain image and coordinate axes")
        n_images = initial_images.shape[-2]
        if n_images < 3:
            raise ValueError("string methods require at least three images")
        if not (np.allclose(initial_images[..., 0, :], start)
                and np.allclose(initial_images[..., -1, :], end)):
            raise ValueError("initial_images must start and end at the supplied endpoints")
    if reparametrizer is None:
        reparametrizer = InterpolatingReparametrizer()
    finder = StringMethodStepFinder(function, jacobian, step_size=step_size)
    return iterative_chain_minimize(
        initial_images, finder, reparametrizer=reparametrizer,
        fixed_images=[0, n_images - 1], **optimizer_options
    )


def jacobi_maximize(initial_matrix, rotation_generator, max_iterations=100, contrib_tol=1e-16, tol=1e-8):
    """
    **LLM Docstring**

    Maximize an objective over an orthogonal transformation by sweeping 2x2
    (Jacobi) rotations over all column pairs until the gain converges (the standard
    orbital/vector localization scheme).

    :param initial_matrix: the matrix whose columns are rotated
    :type initial_matrix: np.ndarray
    :param rotation_generator: callable giving the optimal `(cos, sin, gain)` per pair
    :type rotation_generator: Callable
    :param max_iterations: maximum sweeps
    :type max_iterations: int
    :param contrib_tol: minimum per-pair gain to accept a rotation
    :type contrib_tol: float
    :param tol: convergence tolerance on the total per-sweep gain
    :type tol: float
    :return: `(rotated_matrix, accumulated_rotation, (total_gain, iterations))`
    :rtype: tuple
    """
    mat = np.asanyarray(initial_matrix).copy()

    k = initial_matrix.shape[1]
    perms = list(itertools.combinations(range(k), 2))
    U = np.eye(k)

    total_delta = -1
    iteration = -1
    for iteration in range(max_iterations):
        total_delta = 0
        for n, (p_i, q_i) in enumerate(perms):
            A, B, delta = rotation_generator(mat, p_i, q_i)

            if delta > contrib_tol:
                total_delta += delta

                new_pi = A * mat[:, p_i] + B * mat[:, q_i]
                new_qi = A * mat[:, q_i] - B * mat[:, p_i]
                mat[:, p_i] = new_pi
                mat[:, q_i] = new_qi

                rot_pi = A * U[:, p_i] + B * U[:, q_i]
                rot_qi = A * U[:, q_i] - B * U[:, p_i]
                U[:, p_i] = rot_pi
                U[:, q_i] = rot_qi

        if abs(total_delta) < tol:
            break

    return mat, U, (total_delta, iteration)

class LineSearchRotationGenerator:
    def __init__(self, column_function, tol=1e-16, max_iterations=10):
        """
        **LLM Docstring**

        Initialize a rotation generator that finds each optimal 2x2 rotation angle by a
        quadratic-interpolation line search.

        :param column_function: the per-column objective contribution
        :type column_function: Callable
        :param tol: convergence tolerance
        :type tol: float
        :param max_iterations: maximum line-search iterations
        :type max_iterations: int
        """
        self.one_e_func = column_function
        self.tol = tol
        self.max_iter = max_iterations

    @classmethod
    def quadratic_opt(self,
                  g0, g1, g2,
                  f0, f1, f2
                  ):
        """
        **LLM Docstring**

        Return the vertex of the parabola through three `(angle, value)` samples (the
        quadratic-interpolation optimum), or `None` when the samples are collinear.

        :param g0: first angle
        :type g0: float
        :param g1: second angle
        :type g1: float
        :param g2: third angle
        :type g2: float
        :param f0: value at the first angle
        :type f0: float
        :param f1: value at the second angle
        :type f1: float
        :param f2: value at the third angle
        :type f2: float
        :return: the interpolated optimum angle, or `None`
        :rtype: float | None
        """
        g02 = g0**2
        g12 = g1**2
        g22 = g2**2
        denom = (2*f1*g0 - 2*f2*g0 - 2*f0*g1 + 2*f2*g1 + 2*f0*g2 - 2*f1*g2)
        if abs(denom) < 1e-8:
            return None
        else:
            return (
                    (f1*g02 - f2*g02 - f0*g12 + f2*g12 + f0*g22 - f1*g22)
                      / denom
            )

    def _phi(self, g, f_i, f_j):
        """
        **LLM Docstring**

        Evaluate the objective for the pair of columns rotated by an angle, returning the
        value, the `(cos, sin)`, and the rotated columns.

        :param g: the rotation angle
        :type g: float
        :param f_i: the first column
        :type f_i: np.ndarray
        :param f_j: the second column
        :type f_j: np.ndarray
        :return: `(value, (cos, sin), (rotated_i, rotated_j))`
        :rtype: tuple
        """
        c = np.cos(g)
        s = np.sin(g)
        f_i, f_j = (
            c * f_i + s * f_j,
            -s * f_i + c * f_j
        )
        val = sum(self.one_e_func(f) for f in [f_i, f_j])
        return val, (c, s), (f_i, f_j)

    def __call__(self, mat, col_i, col_j):
        """
        **LLM Docstring**

        Find the optimal 2x2 rotation for a pair of columns by quadratic-interpolation
        line search over the rotation angle.

        :param mat: the matrix being localized
        :type mat: np.ndarray
        :param col_i: the first column index
        :type col_i: int
        :param col_j: the second column index
        :type col_j: int
        :return: `(cos, sin, gain)` for the optimal rotation
        :rtype: tuple
        """
        f_i, f_j = [mat[:, x] for x in [col_i, col_j]]
        phi0 = sum(self.one_e_func(f) for f in [f_i, f_j])

        g0 = 0
        g1 = np.pi
        g2 = 2*np.pi

        f0 = phi0
        f1, (c, s), _ = self._phi(g1, f_i, f_j)
        f2 = phi0

        prev = max([f0, f1, f2])
        for it in range(self.max_iter):
            g = self.quadratic_opt(
                  g0, g1, g2,
                  f0, f1, f2
                  )
            if g is None or g < g0 or g > g2:
                if f2 > f0:
                    g0 = g1
                    f0 = f1
                else:
                    g2 = g1
                    f2 = f1
                g = (g0 + g2) / 2
                f, (c, s), _ = self._phi(g, f_i, f_j)
            else:
                f, (c, s), _ = self._phi(g, f_i, f_j)
                if f <= min([f0, f1, f2]):
                    if f2 > f0:
                        g0 = g1
                        f0 = f1
                    else:
                        g2 = g1
                        f2 = f1
                    g = (g0 + g2) / 2
                    f, (c, s), _ = self._phi(g, f_i, f_j)
                else:
                    if g < g1:
                        g2 = g1
                        f2 = f1
                    else:
                        g0 = g1
                        f0 = f1
            # if abs(f - prev) < self.tol:
            #     break
            f1 = f
            g1 = g

        return c, s, f1 - prev

class GradientDescentRotationGenerator:
    def __init__(self, column_function, gradient, tol=1e-16, max_iterations=10,
                 damping_parameter=.9,
                 damping_exponent=1.1,
                 restart_interval=3
                 ):
        """
        **LLM Docstring**

        Initialize a rotation generator that finds each optimal 2x2 rotation angle by
        damped gradient descent.

        :param column_function: the per-column objective contribution
        :type column_function: Callable
        :param gradient: the per-column gradient of the objective
        :type gradient: Callable
        :param tol: convergence tolerance on the step
        :type tol: float
        :param max_iterations: maximum iterations
        :type max_iterations: int
        :param damping_parameter: step-damping factor
        :type damping_parameter: float
        :param damping_exponent: damping decay exponent
        :type damping_exponent: float
        :param restart_interval: damping restart interval
        :type restart_interval: int
        """
        self.one_e_func = column_function
        self.grad = gradient
        self.tol = tol
        self.max_iter = max_iterations
        self.damper = Damper(
            damping_parameter=damping_parameter,
            damping_exponent=damping_exponent,
            restart_interval=restart_interval
        )

    def __call__(self, mat, col_i, col_j):
        """
        **LLM Docstring**

        Find the optimal 2x2 rotation for a pair of columns by damped gradient descent
        over the rotation angle.

        :param mat: the matrix being localized
        :type mat: np.ndarray
        :param col_i: the first column index
        :type col_i: int
        :param col_j: the second column index
        :type col_j: int
        :return: `(cos, sin, gain)` for the optimal rotation
        :rtype: tuple
        """
        f_i, f_j = [mat[:, x] for x in [col_i, col_j]]
        cur_val = sum(self.one_e_func(f) for f in [f_i, f_j])

        g = 0
        c = 1
        s = 0
        cur_grads = np.array([self.grad(f) for f in [f_i, f_j]])

        new_i, new_j = f_i, f_j
        for it in range(self.max_iter):
            grads = [np.dot(f, g) for f,g in zip([new_i, new_j], cur_grads)]
            step = sum(grads)
            if abs(step) < self.tol:
                break
            else:
                u = self.damper.get_damping_factor()
                if u is not None:
                    step *= u
                g = (g + step) % (2*np.pi)
                # if abs(g) > np.pi/2: g = np.sign(g) * np.pi/2
                c = np.cos(g)
                s = np.sin(g)
                new_i, new_j = (
                    c * f_i + s * f_j,
                    -s * f_i + c * f_j
                )
                cur_grads = np.array([self.grad(f) for f in [new_i, new_j]])


        new_vals = sum(self.one_e_func(f) for f in [new_i, new_j])
        return c, s, new_vals - cur_val

class OperatorMatrixRotationGenerator:
    def __init__(self, one_e_func, matrix_func):
        """
        **LLM Docstring**

        Initialize a rotation generator that solves each optimal 2x2 rotation
        analytically from a supplied 2x2 operator matrix.

        :param one_e_func: the per-column objective contribution
        :type one_e_func: Callable
        :param matrix_func: callable giving the `(a, b, c)` operator-matrix entries for a pair
        :type matrix_func: Callable
        """
        self.one_e_func = one_e_func
        self.mat_func = matrix_func
    def __call__(self, mat, col_i, col_j):
        """
        **LLM Docstring**

        Find the optimal 2x2 rotation for a pair of columns by analytically diagonalizing
        the supplied 2x2 operator matrix (the closed-form Jacobi angle).

        :param mat: the matrix being localized
        :type mat: np.ndarray
        :param col_i: the first column index
        :type col_i: int
        :param col_j: the second column index
        :type col_j: int
        :return: `(cos, sin, gain)` for the optimal rotation
        :rtype: tuple
        """
        f_i, f_j = [mat[:, x] for x in [col_i, col_j]]
        cur_val = sum(self.one_e_func(f) for f in [f_i, f_j])
        a, b, c = self.mat_func(f_i, f_j)

        # test_mat = np.array([[a, b], [b, c]])
        # rot = np.linalg.eigh(test_mat)[1] # do this analytically...
        # print(rot)
        # cos_g = rot[0, 0]
        # sin_g = np.sign(rot[0, 0] * rot[1, 1]) * rot[1, 0]
        # new_rot = np.array([
        #     [cos_g, -sin_g],
        #     [sin_g, cos_g]
        # ])
        # explicit 2x2 form
        tau = (c - a) / (2 * b)
        t = np.sign(tau) / (abs(tau) + np.sqrt(1 + tau ** 2))
        cos_g = 1 / np.sqrt(1 + t ** 2)
        sin_g = -cos_g * t
        # new_rot = np.array([
        #         [cos_g, -sin_g],
        #         [sin_g, cos_g]
        #     ])
        # print(new_rot.T @ test_mat @ new_rot)

        f_i, f_j = (
            cos_g * f_i + sin_g * f_j,
            -sin_g * f_i + cos_g * f_j
        )
        new_val = sum(self.one_e_func(f) for f in [f_i, f_j])


        return cos_g, sin_g, new_val - cur_val

def displacement_localizing_rotation_generator(mat, col_i, col_j):
    """
    **LLM Docstring**

    Compute the optimal 2x2 Foster-Boys localizing rotation for a pair of
    displacement columns (each a set of 3-vectors), returning the closed-form
    `(cos, sin, gain)`.

    :param mat: the matrix of displacement columns
    :type mat: np.ndarray
    :param col_i: the first column index
    :type col_i: int
    :param col_j: the second column index
    :type col_j: int
    :return: `(cos, sin, gain)` for the localizing rotation
    :rtype: tuple
    """
    # Foster-Boys localization

    p = mat[:, col_i].reshape(-1, 3)
    q = mat[:, col_j].reshape(-1, 3)
    pq_norms = vec_ops.vec_dots(p, q, axis=-1)
    pp_norms = vec_ops.vec_dots(p, p, axis=-1)
    qq_norms = vec_ops.vec_dots(q, q, axis=-1)

    pqpq = np.dot(pq_norms, pq_norms)
    pppp = np.dot(pp_norms, pp_norms)
    qqqq = np.dot(qq_norms, qq_norms)
    ppqq = np.dot(pp_norms, qq_norms)
    pppq = np.dot(pp_norms, pq_norms)
    qqqp = np.dot(qq_norms, pq_norms)

    A = pqpq - (pppp + qqqq - 2 * ppqq) / 4
    B = pppq - qqqp

    AB_norm = np.sqrt(A ** 2 + B ** 2)

    return A / AB_norm, B / AB_norm, A

def polyfit_critical_points(x, y, fit_order=2, check_curvature=None, curvature_test=None):
    """
    **LLM Docstring**

    Fit a polynomial to `(x, y)` and return the critical points of the fit (roots of
    its derivative), optionally filtered by a curvature test.

    :param x: the sample abscissae
    :type x: np.ndarray
    :param y: the sample values
    :type y: np.ndarray
    :param fit_order: the polynomial degree
    :type fit_order: int
    :param check_curvature: also compute the curvature at each critical point
    :type check_curvature: bool | None
    :param curvature_test: predicate selecting critical points by curvature sign
    :type curvature_test: Callable | None
    :return: `(roots, values[, curvature])`
    :rtype: tuple
    """
    coeffs = np.polyfit(x, y, fit_order)
    target_poly = np.poly1d(coeffs)
    pd = target_poly.deriv()
    roots = pd.roots
    if check_curvature is None:
        check_curvature = curvature_test is not None
    if check_curvature:
        curvature = pd.deriv()(roots)
        if curvature_test:
            mask = curvature_test(curvature)
            roots = roots[mask]
            curvature = curvature[mask]
        return roots, target_poly(roots), curvature
    else:
        return roots, target_poly(roots)

def polyfit_maxima(x, y, fit_order=2):
    """
    **LLM Docstring**

    Fit a polynomial to `(x, y)` and return its maxima (critical points with negative
    curvature).

    :param x: the sample abscissae
    :type x: np.ndarray
    :param y: the sample values
    :type y: np.ndarray
    :param fit_order: the polynomial degree
    :type fit_order: int
    :return: `(maxima_x, maxima_values, curvature)`
    :rtype: tuple
    """
    return polyfit_critical_points(x, y, fit_order=fit_order, curvature_test=lambda c: c < 0)
def polyfit_minima(x, y, fit_order=2):
    """
    **LLM Docstring**

    Fit a polynomial to `(x, y)` and return its minima (critical points with positive
    curvature).

    :param x: the sample abscissae
    :type x: np.ndarray
    :param y: the sample values
    :type y: np.ndarray
    :param fit_order: the polynomial degree
    :type fit_order: int
    :return: `(minima_x, minima_values, curvature)`
    :rtype: tuple
    """
    return polyfit_critical_points(x, y, fit_order=fit_order, curvature_test=lambda c: c > 0)

def get_peak_fitting_region(
        energies,
        *,
        peak_energy_cutoff,
        min_nodes  # at least 3 nodes for the quadratic fit
):
    """
    **LLM Docstring**

    Select the indices around the peak of an energy profile to use for a peak fit:
    scan outward from the maximum while the energy stays above a cutoff, padding to a
    minimum node count.

    :param energies: the per-point energies
    :type energies: np.ndarray
    :param peak_energy_cutoff: the cutoff below which points are excluded
    :type peak_energy_cutoff: float
    :param min_nodes: minimum number of points to keep (for the fit)
    :type min_nodes: int
    :return: the selected indices
    :rtype: list[int]
    """
    energies = np.array(energies)
    ts = np.argmax(energies)

    # scan left and right from the TS until we have either gone below the offset or have reached our node cutoff
    left_points = []
    for i in range(ts-1): # scan in reverse
        if energies[ts - i - 1] > peak_energy_cutoff:
            left_points.append(ts - i - 1)
    right_points = []
    for i in range(ts+1, len(energies)):
        if energies[i] > peak_energy_cutoff:
            right_points.append(i)

    all_points = list(reversed(left_points)) + [ts] + right_points
    if len(all_points) < min_nodes:
        pad = (len(all_points) - min_nodes) // 2
        left_pad = min([pad + (len(all_points) - min_nodes) % 2, all_points[0]])
        right_pad = min([pad, len(energies) - all_points[-1]])
        all_points = (
            list(range(all_points[0] - left_pad, all_points[0]))
            + all_points
            + list(range(all_points[-1] + 1, all_points[-1] + right_pad))
        )

    return all_points

def peak_fit_maxiumum(x, y, *,
                      fit_order=2,
                      peak_cutoff,
                      min_nodes=3  # at least 3 nodes for the quadratic fit
                      ):
    """
    **LLM Docstring**

    Estimate the location and height of a peak by fitting a polynomial to the points
    around it (falling back to the raw argmax if the fit has no maximum).

    :param x: the abscissae
    :type x: np.ndarray
    :param y: the values
    :type y: np.ndarray
    :param fit_order: the polynomial degree
    :type fit_order: int
    :param peak_cutoff: the cutoff for selecting the fit region
    :type peak_cutoff: float
    :param min_nodes: minimum number of points in the fit region
    :type min_nodes: int
    :return: `(peak_x, peak_value)`
    :rtype: tuple
    """
    x = np.asanyarray(x)
    y = np.asanyarray(y)
    pos = get_peak_fitting_region(y, peak_energy_cutoff=peak_cutoff, min_nodes=min_nodes)

    max_pos, max_fit, _ = polyfit_maxima(x[pos,], y[pos,], fit_order=fit_order)
    if len(max_pos) == 0:
        root = np.argmax(y)
        return x[root], y[root]
    else:
        root = np.argmax(max_fit)
        return max_pos[root], max_fit[root]
