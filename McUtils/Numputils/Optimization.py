import collections, abc
import functools
import numpy as np
import itertools

# from scipy.optimize.linesearch import line_search_armijo
from . import VectorOps as vec_ops
from . import Misc as misc
from . import TransformationMatrices as tfs

__all__ = [
    "iterative_step_minimize",
    "GradientDescentStepFinder",
    "NewtonStepFinder",
    "QuasiNewtonStepFinder",
    "ConjugateGradientStepFinder",
    "jacobi_maximize",
    "LineSearchRotationGenerator",
    "GradientDescentRotationGenerator",
    "OperatorMatrixRotationGenerator",
    "displacement_localizing_rotation_generator"
]
default_jacobian_step_finder = 'conjugate-gradient'
default_hessian_step_finder = 'newton'
def lookup_method_name(method):
    return {
        'conjugate-gradient':ConjugateGradientStepFinder,
        'newton':NewtonStepFinder,
        'quasi-newton':QuasiNewtonStepFinder,
        'gradient-descent':GradientDescentStepFinder,
    }.get(method)
def get_step_finder(spec):
    if isinstance(spec, dict):
        spec = spec.copy() # don't mutate user data
        method = spec.pop('method', None)
        func = spec.pop('func')
        jacobian = spec.pop('jacobian')
        hessian = spec.pop('hessian', None)
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
            spec = method(func, jacobian, hessian, **spec)
        else:
            spec = method(func, jacobian, **spec)
    return spec
def iterative_step_minimize(guess, step_predictor,
                            unitary=False,
                            generate_rotation=False,
                            dtype='float64',
                            orthogonal_directions=None,
                            convergence_metric=None,
                            max_displacement=None,
                            tol=1e-8, max_iterations=100):
    step_predictor = get_step_finder(step_predictor)

    guess = np.array(guess, dtype=dtype)
    base_shape = guess.shape[:-1]
    guess = guess.reshape(-1, guess.shape[-1])
    its = np.zeros(guess.shape[0], dtype=int)
    errs = np.zeros(guess.shape[0], dtype=float)
    mask = np.arange(guess.shape[0])
    if orthogonal_directions is not None:
        orthogonal_directions = vec_ops.orthogonal_projection_matrix(orthogonal_directions)
    if unitary and generate_rotation:
        rotations = vec_ops.identity_tensors(guess.shape[:-1], guess.shape[-1])
    else:
        rotations = None

    converged = True
    for i in range(max_iterations):
        if unitary:
            projector = vec_ops.orthogonal_projection_matrix(guess[mask,].T)
            if orthogonal_directions is not None:
                projector = projector @ orthogonal_directions[np.newaxis]
        elif orthogonal_directions is not None:
            projector = orthogonal_directions[np.newaxis]
        else:
            projector = None
        step, grad = step_predictor(guess[mask,], mask, projector=projector)
        if projector is not None:
            # just in case, will usually lead to non-convergence
            step = (step[..., np.newaxis, :] @ projector).reshape(step.shape)
            grad = (grad[..., np.newaxis, :] @ projector).reshape(step.shape)

        if max_displacement is not None:
            step_sizes = np.linalg.norm(step, axis=1)
            step *= max_displacement / np.clip(step_sizes, max_displacement, None)
        norms = np.linalg.norm(grad, axis=1)
        errs[mask,] = norms
        done = np.where(norms < tol)[0]
        if len(done) > 0: # easy check
            rem = np.delete(np.arange(len(mask)), done)
            mask = np.delete(mask, done)
        else:
            rem = np.arange(len(mask))
        if not unitary:
            guess[mask,] += step[rem,]
        else:
            step = step[rem,]
            norms = np.linalg.norm(step, axis=1)
            # norms = norms[rem,]
            g = guess[mask,].copy()
            v = np.linalg.norm(g, axis=-1)
            r = np.sqrt(norms[rem,]**2 + v**2)
            guess[mask,] = (g + step) / r[:, np.newaxis]
            if generate_rotation:
                raise NotImplementedError(">3D rotations are complicated")
                axis = vec_ops.vec_crosses(g, guess[mask,])[0]
                ang = np.arctan2(norms/r, v/r)
                rot = tfs.rotation_matrix(axis, ang)
                rotations = rot @ rotations
        its[mask,] += 1
        if len(mask) == 0:
            break
    else:
        converged = False
        its[mask] = max_iterations

    guess = guess.reshape(base_shape + (guess.shape[-1],))
    errs = errs.reshape(base_shape)
    its = its.reshape(base_shape)

    if unitary and generate_rotation:
        res = (guess, rotations), converged, (errs, its)
    else:
        res = guess, converged, (errs, its)

    return res

# class NetwonHessianGenerator(metaclass=typing.Protocol):
#     def jacobian(self, guess, mask):
#         raise NotImplementedError("abstract interface")
#     def hessian_inverse(self, guess, mask):
#         raise NotImplementedError("abstract interface")
#
#     def __call__(self, guess, mask):
#         raise NotImplementedError("abstract interface")

class Damper:
    def __init__(self, damping_parameter=None, damping_exponent=None, restart_interval=10):
        self.n = 0
        self.u = damping_parameter
        self.exp = damping_exponent
        self.restart = restart_interval

    def get_damping_factor(self):
        u = self.u
        if u is not None:
            if self.exp is not None:
                u = np.power(u, self.n*self.exp)
                self.n = (self.n + 1) % self.restart
        return u

class LineSearcher(metaclass=abc.ABCMeta):
    """
    Adapted from scipy.optimize to handle multiple structures at once
    """

    def __init__(self, func, min_alpha=0, **opts):
        self.func = func
        self.opts = opts
        self.min_alpha = min_alpha

    @abc.abstractmethod
    def check_scalar_converged(self, phi_vals, alphas, **opts):
        raise NotImplementedError("abstract")

    @abc.abstractmethod
    def update_alphas(self,
                      phi_vals, alphas, iteration,
                      old_phi_vals, old_alphas_vals,
                      mask,
                      **opts
                      ):
        raise NotImplementedError("abstract")

    def scalar_search(self,
                      scalar_func,
                      guess_alpha,
                      min_alpha=None,
                      max_iterations=100,
                      history_length=1,
                      **opts):
        if min_alpha is None:
            min_alpha = self.min_alpha

        alphas = np.asanyarray(guess_alpha)
        mask = np.arange(len(alphas))

        phi_vals = scalar_func(alphas, mask)
        if history_length > 0:
            history = collections.deque(maxlen=history_length)
        else:
            history = None

        is_converged = np.full(len(mask), False)
        converged = np.where(self.check_scalar_converged(phi_vals, alphas, **opts))[0]
        if len(converged) > 0:
            is_converged[converged,] = True
            mask = np.delete(mask, converged)
            if len(mask) == 0:
                return alphas,  (phi_vals, is_converged)

        for i in range(max_iterations):
            if history is not None:
                phi_vals_old = [p[mask,] for p,a in history]
                alpha_vals_old = [a[mask,] for p,a in history]
            else:
                phi_vals_old = None
                alpha_vals_old = None

            new_alphas = self.update_alphas(phi_vals, alphas, i,
                                            phi_vals_old, alpha_vals_old,
                                            mask,
                                            **opts
                                            )
                # mask = np.delete(mask, problem_alphas)
                # if len(mask) == 0:
                #     break  # alphas, (phi_vals, is_converged)

            history.append([phi_vals.copy(), alphas.copy()])

            new_phi = scalar_func(new_alphas, mask)
            phi_vals[mask,] = new_phi
            # prev_alphas = alphas[mask,].copy()
            alphas[mask,] = new_alphas

            problem_alphas = np.where(new_alphas < min_alpha)[0]
            if len(problem_alphas) > 0:
                alphas[mask[problem_alphas,],] = min_alpha
                new_alphas = np.delete(new_alphas, problem_alphas)
                new_phi = np.delete(new_phi, problem_alphas)
                mask = np.delete(mask, problem_alphas)
                if len(mask) == 0:
                    break

            converged = np.where(self.check_scalar_converged(new_phi, new_alphas, **opts))[0]
            if len(converged) > 0:
                is_converged[mask[converged,],] = True
                mask = np.delete(mask, converged)
                if len(mask) == 0:
                    break

            # problem_alphas = np.where(np.abs(prev_alphas - alphas[mask,]) < 1e-8)[0]
            # if len(problem_alphas) > 0:
            #     mask = np.delete(mask, problem_alphas)
            #     if len(mask) == 0:
            #         break# alphas, (phi_vals, is_converged)
        return alphas, (phi_vals, is_converged)

    def prep_search(self, initial_geom, search_dir, guess_alpha=1, **opts):
        return np.full(len(initial_geom), guess_alpha), opts, self._dir_func(self.func, initial_geom, search_dir)

    @classmethod
    def _dir_func(cls, func, initial_geom, search_dir):
        @functools.wraps(func)
        def phi(alphas, mask):
            return func(initial_geom[mask,] + alphas[:, np.newaxis] * search_dir[mask,], mask)

        return phi

    def __call__(self, initial_geom, search_dir, **base_opts):
        opts = dict(self.opts, **base_opts)
        guess_alpha, opts, phi = self.prep_search(initial_geom, search_dir, **opts)
        conv = self.scalar_search(
            phi,
            guess_alpha,
            **opts
        )
        return conv

class ArmijoSearch(LineSearcher):

    def __init__(self, func, c1=1e-4, min_alpha=None, fixed_step_cutoff=1e-8, der_max=1e6, guess_alpha=1):
        super().__init__(func, min_alpha=min_alpha, c1=c1)
        self.func = func
        self.der_max = der_max
        self.fixed_step_cutoff = fixed_step_cutoff
        self.guess_alpha = guess_alpha

    def prep_search(self, initial_geom, search_dir, *, initial_grad, min_alpha=None, **rest):
        mask = np.arange(len(initial_geom))
        derphi0 = np.reshape(initial_grad[:, np.newaxis, :] @ search_dir[:, :, np.newaxis], (-1,))
        # derphi0 = np.clip(derphi0, -self.der_max, self.der_max)
        if min_alpha is None:
            min_alpha = self.min_alpha

        a0, opts, phi = super().prep_search(initial_geom, search_dir, **rest)
        if self.fixed_step_cutoff is None:
           if min_alpha is None:
               min_alpha = 1e-8
        else:
           if min_alpha is None:
               min_alpha = 0 if np.max(np.abs(derphi0)) > self.fixed_step_cutoff else 1e-8
           a0 = (
                   (np.abs(derphi0) > self.fixed_step_cutoff) + (np.abs(derphi0) <= self.fixed_step_cutoff) * 1e-4
           ).astype(float)
        # print(a0)

        phi0 = phi(np.zeros_like(a0), mask)
        return a0, dict(opts, phi0=phi0, derphi0=derphi0, min_alpha=min_alpha), phi

    def check_scalar_converged(self, phi_vals, alphas, *, phi0, c1, derphi0):
        return phi_vals <= phi0 + c1 * alphas * derphi0

    def update_alphas(self,
                      phi_vals, alphas, iteration,
                      old_phi_vals, old_alphas_vals,
                      mask,
                      *,
                      phi0, c1, derphi0,
                      zero_cutoff=1e-16
                      ):
        phi0 = phi0[mask,]
        derphi0 = derphi0[mask,]
        if iteration == 0:
            factor = (phi_vals - phi0 - derphi0 * alphas)
            # alpha1 = alphas.copy()
            # safe_pos = np.where(np.abs(factor) > zero_cutoff)
            # alpha1[safe_pos,] = -(derphi0[safe_pos,]) * alphas[safe_pos] ** 2 / 2.0 / factor[safe_pos]
            # TODO: ensure stays numerically stable
            # print(".>>", phi0)
            alpha1 = -(derphi0) * alphas ** 2 / 2.0 / factor
            return alpha1
        else:
            phi_a0 = old_phi_vals[0]
            phi_a1 = phi_vals
            alpha0 = old_alphas_vals[0]
            alpha1 = alphas

            # da = (alpha1 - alpha0)

            # safe_pos = np.where(np.abs(factor) < zero_cutoff)
            # factor = alpha0 ** 2 * alpha1 ** 2 * (alpha1 - alpha0)
            # a = alpha0 ** 2 * (phi_a1 - phi0 - derphi0 * alpha1) - \
            #     alpha1 ** 2 * (phi_a0 - phi0 - derphi0 * alpha0)
            # a = a / factor
            # b = -alpha0 ** 3 * (phi_a1 - phi0 - derphi0 * alpha1) + \
            #     alpha1 ** 3 * (phi_a0 - phi0 - derphi0 * alpha0)
            # b = b / factor

            # scaling = 1
            n0 = (phi_a0 - phi0 - derphi0 * alpha0)
            n1 = (phi_a1 - phi0 - derphi0 * alpha1)
            d0 = alpha0 ** 2 * (alpha1 - alpha0)
            d1 = alpha1 ** 2 * (alpha1 - alpha0)
            # if d0 < 1e-8 or d1 < 1e-8:
            #     scaling = 1e6
            #     d0 = d0 * scaling
            #     d1 = d1 * scaling
            f1 = n1 / d1
            f0 = n0 / d0

            a = f1 - f0
            b = alpha1 * f0 - alpha0 * f1

            alpha2 = (-b + np.sqrt(abs(b ** 2 - 3 * a * derphi0))) / (3.0 * a)
            # alpha2 = alpha2 / scaling

            halved_alphas = np.where(
                np.logical_or(
                    (alpha1 - alpha2) > alpha1 / 2.0,
                    (1 - alpha2 / alpha1) < 0.96
                )
            )
            alpha2[halved_alphas] = alpha1[halved_alphas] / 2.0

            return alpha2

class _WolfeLineSearch(LineSearcher):
    """
    Adapted from scipy.optimize
    """

    def __init__(self, func, grad, **opts):
        super().__init__(func)
        self.grad = grad

    @classmethod
    def _grad_func(cls, jac, initial_geom, search_dir):
        @functools.wraps(jac)
        def derphi(alphas, mask):
            pk = search_dir[mask,]
            grad = jac(initial_geom[mask,] + alphas[:, np.newaxis] * pk, mask)
            return (grad[: np.newaxis, :] @ pk[:, :, np.newaxis]).reshape(-1)

        return derphi

    def prep_search(self, initial_geom, search_dir):
        a_guess, opts, phi = super().prep_search(initial_geom, search_dir)
        derphi = self._grad_func(self.grad, initial_geom, search_dir)
        gfk = self.grad(initial_geom)
        derphi0 = derphi(np.zeros_like(a_guess), np.arange(len(a_guess)))

        # stp, fval, old_fval = scalar_search_wolfe1(
        #     phi, derphi, old_fval, old_old_fval, derphi0,
        #     c1=c1, c2=c2, amax=amax, amin=amin, xtol=xtol)

        # return stp, fc[0], gc[0], fval, old_fval, gval[0]

    def check_scalar_converged(self, phi_vals, alphas, **opts):
        ...

class GradientDescentStepFinder:
    supports_hessian = False
    line_search = ArmijoSearch

    def __init__(self, func, jacobian, damping_parameter=None, damping_exponent=None,
                 line_search=True, restart_interval=10):
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

    def __call__(self, guess, mask, projector=None):
        # jac = -self.jac(guess, mask)
        # u = self.damper.get_damping_factor()
        # if u is not None:
        #     jac = u * jac
        # return jac, jac


        jacobian = self.jac(guess, mask)

        new_step_dir = -jacobian
        if projector is not None:
            new_step_dir = (new_step_dir[..., np.newaxis, :] @ projector).reshape(new_step_dir.shape)

        if self.searcher is not None:
            alpha, (fvals, is_converged) = self.searcher(guess, new_step_dir, initial_grad=jacobian)
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
        if mode == 'direct':
            @functools.wraps(func)
            def hessian_inverse(guess, mask):
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

    def __call__(self, guess, mask, projector=None):

        jacobian, hessian_inv = self.jacobian(guess, mask), self.hessian_inverse(guess, mask)

        new_step_dir = -(hessian_inv @ jacobian[:, :, np.newaxis]).reshape(jacobian.shape)
        if projector is not None:
            new_step_dir = (new_step_dir[:, np.newaxis, :] @ projector).reshape(new_step_dir.shape)
        if self.searcher is not None:
            alpha, (fvals, is_converged) = self.searcher(guess, new_step_dir, initial_grad=jacobian)
            new_step_dir = alpha[:, np.newaxis] * new_step_dir

        # h = func(guess, mask)
        u = self.damper.get_damping_factor()
        if u is not None:
            new_step_dir = new_step_dir * u

        return new_step_dir, jacobian

class NewtonStepFinder:
    supports_hessian = True
    def __init__(self, func, jacobian=None, hessian=None, *, check_generator=True, **generator_opts):
        if check_generator:
            generator = self._prep_generator(func, jacobian, hessian, generator_opts)
        else:
            generator = jacobian
        self.generator = generator

    @classmethod
    def _prep_generator(cls, func, jac, hess, opts):
        if (hasattr(func, 'jacobian') and hasattr(func, 'hessian_inverse')):
            return func
        else:
            if hess is None:
                raise ValueError(
                    "Direct Netwon requires a Hessian or a generator for the Jacobian and Hessian inverse. "
                    "Consider using Quasi-Newton if only the Jacobian is fast to compute.")
            return NetwonDirectHessianGenerator(func, jac, hess, **opts)

    def __call__(self, guess, mask, projector=None):
        return self.generator(guess, mask, projector=projector)

class QuasiNewtonStepFinder:
    supports_hessian = False

    def __init__(self, func, jacobian, approximation_type='bfgs', **generator_opts):
        self.hess_appx = self.hessian_approximations[approximation_type.lower()](func, jacobian, **generator_opts)
    @property
    def hessian_approximations(self):
        return {
            'bfgs':BFGSApproximator
        }

    def __call__(self, guess, mask, projector=None):
        return self.hess_appx(guess, mask, projector=projector)

class QuasiNetwonHessianApproximator:

    line_search = ArmijoSearch
    def __init__(self, func, jacobian, initial_beta=1,
                 damping_parameter=None, damping_exponent=None,
                 line_search=True, restart_interval=10,
                 restart_hessian_norm=1e-5,
                 approximation_mode='direct'
                 # approximation_mode='inverse'
                 ):
        self.func = func
        self.jac = jacobian
        self.initial_beta = initial_beta
        self.base_hess = None
        self.prev_jac = None
        self.prev_step = None
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
        if self.eye_tensors is None:
            self.eye_tensors = vec_ops.identity_tensors(guess.shape[:-1], guess.shape[-1])
            return self.eye_tensors
        else:
            return self.eye_tensors[mask,]

    def initialize_hessians(self, guess, mask):
        if self.approximation_mode == 'direct':
            return self.initial_beta * self.identities(guess, mask)
        else:
            return (1/self.initial_beta) * self.identities(guess, mask)

    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        raise NotImplementedError("abstract")

    def get_jacobian_updates(self, guess, mask):
        new_jacs = self.jac(guess, mask)
        if self.prev_jac is None:
            jac_diffs = new_jacs
        else:
            prev_jacs = self.prev_jac[mask,]
            jac_diffs = new_jacs - prev_jacs
        return new_jacs, jac_diffs

    def restart_hessian_approximation(self):
        restart = np.any(
            np.linalg.norm(self.prev_step, axis=-1) < self.restart_hessian_norm
        )
        return restart

    def __call__(self, guess, mask, projector=None):
        new_jacs, jacobian_diffs = self.get_jacobian_updates(guess, mask)
        if self.prev_step is None or self.restart_hessian_approximation():
            new_hess = self.initialize_hessians(guess, mask)
        else:
            prev_steps = self.prev_step[mask,]
            prev_hess = self.prev_hess_inv[mask,]
            new_hess = self.get_hessian_update(self.identities(guess, mask), jacobian_diffs, prev_steps, prev_hess)

        if self.approximation_mode == 'direct':
            B = np.linalg.inv(new_hess)
        else:
            B = new_hess
        # print(new_hess)
        new_step_dir = -(B @ new_jacs[:, :, np.newaxis]).reshape(new_jacs.shape)
        if projector is not None:
            new_step_dir = (new_step_dir[:, np.newaxis, :] @ projector).reshape(new_step_dir.shape)
        if self.searcher is not None:
            alpha, (fvals, is_converged) = self.searcher(guess, new_step_dir, initial_grad=new_jacs)
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

        if self.prev_hess_inv is None:
            self.prev_hess_inv = new_hess
        else:
            self.prev_hess_inv[mask,] = new_hess

        return new_step, new_jacs

class BFGSApproximator(QuasiNetwonHessianApproximator):

    orthogonal_dirs_cutoff = 1e-8
    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        if self.approximation_mode == 'direct':
            H = prev_hess.copy()

            diff_norm = jacobian_diffs[:, np.newaxis, :] @ prev_steps[:, :, np.newaxis]
            h_step = (H @ prev_steps[:, :, np.newaxis])
            h_norm = prev_steps @ h_step
            h_step = h_step.reshape(prev_steps.shape)
            h_norm = h_norm.flatten()
            good_pos = np.where(np.logical_and(
                np.abs(diff_norm.reshape(-1, )) > self.orthogonal_dirs_cutoff,
                np.abs(h_norm.reshape(-1, )) > self.orthogonal_dirs_cutoff
            ))

            diff_norm = diff_norm[good_pos]
            identities = identities[good_pos]
            prev_steps = prev_steps[good_pos]
            jacobian_diffs = jacobian_diffs[good_pos]

            diff_outer = jacobian_diffs[:, np.newaxis, :] * jacobian_diffs[:, :, np.newaxis]
            step_outer = h_step[:, np.newaxis, :] * h_step[:, :, np.newaxis]
            # print("woof", np.linalg.norm(diff_step))
            diff_step = diff_outer / diff_norm
            step_step = step_outer / h_norm
            H[good_pos] += diff_step - step_step
        else:
            diff_norm = jacobian_diffs[:, np.newaxis, :] @ prev_steps[:, :, np.newaxis]
            good_pos = np.where(np.abs(diff_norm.reshape(-1,)) > self.orthogonal_dirs_cutoff)

            H = prev_hess.copy()

            diff_norm = diff_norm[good_pos]
            identities = identities[good_pos]
            prev_steps = prev_steps[good_pos]
            jacobian_diffs = jacobian_diffs[good_pos]

            diff_outer = jacobian_diffs[:, np.newaxis, :] * prev_steps[:, :, np.newaxis]
            diff_step = identities - diff_outer / diff_norm
            step_outer = prev_steps[:, np.newaxis, :] * prev_steps[:, :, np.newaxis]
            # print("woof", np.linalg.norm(diff_step))
            step_step = step_outer / diff_norm
            H[good_pos] = diff_step @ H[good_pos] @ np.moveaxis(diff_step, -1, -2) + step_step

        return H

class ConjugateGradientStepFinder:
    supports_hessian = False

    def __init__(self, func, jacobian, approximation_type='fletcher-reeves', **generator_opts):
        self.step_appx = self.beta_approximations[approximation_type.lower()](func, jacobian, **generator_opts)
    @property
    def beta_approximations(self):
        return {
            'fletcher-reeves':FletcherReevesApproximator
        }

    def __call__(self, guess, mask, projector=None):
        return self.step_appx(guess, mask, projector=projector)

class ConjugateGradientStepApproximator:
    line_search = ArmijoSearch

    def __init__(self, func, jacobian,
                 damping_parameter=None, damping_exponent=None,
                 restart_interval=50, restart_parameter=.2,
                 line_search=True):
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
        raise NotImplementedError("abstract")

    def determine_restart(self, new_jacs, mask):
        if self.n == 0: return True
        prev_jac = self.prev_jac[mask,]
        new_norm = np.abs(new_jacs[:, np.newaxis, :] @ prev_jac[:, :, np.newaxis]).flatten()
        old_norm = (prev_jac[:, np.newaxis, :] @ prev_jac[:, :, np.newaxis]).flatten()
        return np.any(
            self.restart_parameter * old_norm < new_norm
        )

    def __call__(self, guess, mask, projector=None):
        new_jacs = self.jac(guess, mask)

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
            alpha, (fvals, is_converged) = self.searcher(guess, new_step_dir, initial_grad=new_jacs)
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
        return (
                (new_jacs[:, np.newaxis, :] @new_jacs[:, :, np.newaxis]) /
                (prev_jac[:, np.newaxis, :] @ prev_jac[:, :, np.newaxis])
        ).reshape(len(new_jacs))

def jacobi_maximize(initial_matrix, rotation_generator, max_iterations=100, contrib_tol=1e-16, tol=1e-8):
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

            if delta > 0:
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
        self.one_e_func = column_function
        self.tol = tol
        self.max_iter = max_iterations

    @classmethod
    def quadratic_opt(self,
                  g0, g1, g2,
                  f0, f1, f2
                  ):
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
        c = np.cos(g)
        s = np.sin(g)
        f_i, f_j = (
            c * f_i + s * f_j,
            -s * f_i + c * f_j
        )
        val = sum(self.one_e_func(f) for f in [f_i, f_j])
        return val, (c, s), (f_i, f_j)

    def __call__(self, mat, col_i, col_j):
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
        self.one_e_func = one_e_func
        self.mat_func = matrix_func
    def __call__(self, mat, col_i, col_j):
        f_i, f_j = [mat[:, x] for x in [col_i, col_j]]
        cur_val = sum(self.one_e_func(f) for f in [f_i, f_j])
        a, b, c = self.mat_func(f_i, f_j)

        test_mat = np.array([[a, b], [b, c]])
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