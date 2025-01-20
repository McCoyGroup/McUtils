import collections, abc
import functools
import numpy as np
# from scipy.optimize.linesearch import line_search_armijo
from . import VectorOps as vec_ops
from . import Misc as misc
from . import TransformationMatrices as tfs

__all__ = [
    "iterative_step_minimize",
    "GradientDescentStepFinder",
    "NewtonStepFinder",
    "QuasiNewtonStepFinder",
    "ConjugateGradientStepFinder"
]

def get_step_finder(jacobian, hessian=None, **opts):
    if hessian is None:
        return QuasiNewtonStepFinder(jacobian, **opts)
    else:
        return NewtonStepFinder(jacobian)


def iterative_step_minimize(guess, step_predictor,
                            unitary=False,
                            generate_rotation=False,
                            dtype='float64', tol=1e-8, max_iterations=100):
    guess = np.array(guess, dtype=dtype)
    base_shape = guess.shape[:-1]
    guess = guess.reshape(-1, guess.shape[-1])
    its = np.zeros(guess.shape[0], dtype=int)
    errs = np.zeros(guess.shape[0], dtype=float)
    mask = np.arange(guess.shape[0])
    if unitary and generate_rotation:
        rotations = vec_ops.identity_tensors(guess.shape[:-1], guess.shape[-1])
    else:
        rotations = None
    converged = True
    for i in range(max_iterations):
        step = step_predictor(guess[mask,], mask)
        if unitary:
            step = vec_ops.project_out(step, guess[mask][:, np.newaxis, :])
        # print(step)
        norms = np.linalg.norm(step, axis=1)
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
            norms = norms[rem,]
            g = guess[mask,].copy()
            v = np.linalg.norm(g, axis=-1)
            r = np.sqrt(norms[rem,]**2 + v**2)
            guess[mask,] = (g + step) / r[:, np.newaxis]
            if generate_rotation:
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

    def __init__(self, func, **opts):
        self.func = func
        self.opts = opts

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
                      min_alpha=1e-8,
                      max_iterations=100,
                      history_length=1,
                      **opts):

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
                alpha_vals_old = [p[mask,] for p,a in history]
            else:
                phi_vals_old = None
                alpha_vals_old = None

            new_alphas = self.update_alphas(phi_vals, alphas, i,
                                            phi_vals_old, alpha_vals_old,
                                            mask,
                                            **opts
                                            )
            new_phi = scalar_func(new_alphas, mask)

            phi_vals[mask,] = new_phi
            alphas[mask,] = new_alphas

            converged = np.where(self.check_scalar_converged(new_phi, new_alphas, **opts))[0]
            if len(converged) > 0:
                is_converged[mask[converged,],] = True
                mask = np.delete(mask, converged)
                if len(mask) == 0:
                    return alphas, (phi_vals, is_converged)

            problem_alphas = np.where(alphas[mask,] < min_alpha)[0]
            if len(problem_alphas) > 0:
                mask = np.delete(mask, problem_alphas)
                if len(mask) == 0:
                    return alphas, (phi_vals, is_converged)

            history.append([phi_vals.copy(), alphas.copy()])

        return alphas, (phi_vals, is_converged)

    def prep_search(self, initial_geom, search_dir, **opts):
        return np.ones(len(initial_geom)), opts, self._dir_func(self.func, initial_geom, search_dir)

    @classmethod
    def _dir_func(cls, func, initial_geom, search_dir):
        @functools.wraps(func)
        def phi(alphas, mask):
            woof = func(initial_geom[mask,] + alphas[:, np.newaxis] * search_dir[mask,])
            return woof

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

    def __init__(self, func, c1=1e-4):
        super().__init__(func, c1=c1)
        self.func = func

    @classmethod
    def line_search_armijo(cls, f, xk, pk, gfk, c1=1e-4, alpha0=1):
        """
        Adapted from scipy linesearch for broadcasting
        """
        # xk = np.atleast_1d(xk)
        fc = np.zeros(len(xk), dtype=int)

        def phi(alpha1, mask):
            fc[mask] += 1
            return f(xk[mask,] + alpha1 * pk[mask,])

        mask = np.arange(len(xk))
        phi0 = phi(np.zeros(len(xk)), mask)

        derphi0 = np.reshape(gfk @ pk[:, :, np.newaxis], (-1,))
        alpha, phi1 = cls.scalar_search_armijo(phi, phi0, derphi0, mask, c1=c1, alpha0=alpha0)
        return alpha, fc[0], phi1

    def prep_search(self, initial_geom, search_dir, *, initial_grad, **rest):
        a0, opts, phi = super().prep_search(initial_geom, search_dir, **rest)
        mask = np.arange(len(initial_geom))
        derphi0 = np.reshape(initial_grad[:, np.newaxis, :] @ search_dir[:, :, np.newaxis], (-1,))
        phi0 = phi(np.zeros_like(a0), mask)
        return a0, dict(opts, phi0=phi0, derphi0=derphi0), phi

    def check_scalar_converged(self, phi_vals, alphas, *, phi0, c1, derphi0):
        return phi_vals <= phi0 + c1 * alphas * derphi0

    def update_alphas(self,
                      phi_vals, alphas, iteration,
                      old_phi_vals, old_alphas_vals,
                      mask,
                      *,
                      phi0, c1, derphi0
                      ):
        if iteration == 0:
            alpha1 = -(derphi0) * alphas ** 2 / 2.0 / (phi_vals - phi0[mask,] - derphi0[mask,] * alphas)
            return alpha1

        else:
            phi_a0 = old_phi_vals[0]
            phi_a1 = phi_vals
            alpha0 = old_alphas_vals[0]
            alpha1 = alphas

            factor = alpha0 ** 2 * alpha1 ** 2 * (alpha1 - alpha0)
            a = alpha0 ** 2 * (phi_a1 - phi0 - derphi0 * alpha1) - \
                alpha1 ** 2 * (phi_a0 - phi0 - derphi0 * alpha0)
            a = a / factor
            b = -alpha0 ** 3 * (phi_a1 - phi0 - derphi0 * alpha1) + \
                alpha1 ** 3 * (phi_a0 - phi0 - derphi0 * alpha0)
            b = b / factor

            alpha2 = (-b + np.sqrt(abs(b ** 2 - 3 * a * derphi0))) / (3.0 * a)

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
    def __init__(self, jacobian, damping_parameter=None, damping_exponent=None, restart_interval=10):
        self.jac = jacobian
        self.damper = Damper(
            damping_parameter=damping_parameter,
            damping_exponent=damping_exponent,
            restart_interval=restart_interval
        )

    def __call__(self, guess, mask):
        jac = -self.jac(guess, mask)
        u = self.damper.get_damping_factor()
        if u is not None:
            jac = u * jac
        return jac

class NetwonDirectHessianGenerator:
    def __init__(self, jacobian, hessian, hess_mode='direct',
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

    def wrap_hessian(self, func, mode):
        if mode == 'direct':
            @functools.wraps(func)
            def hessian_inverse(guess, mask):
                h = func(guess, mask)
                u = self.damper.get_damping_factor()
                if u is not None:
                    h = h + u * vec_ops.identity_tensors(guess.shape[:-1], guess.shape[-1])
                return np.linalg.inv(h)
        else:
            @functools.wraps(func)
            def hessian_inverse(guess, mask):
                h = func(guess, mask)
                u = self.damper.get_damping_factor()
                if u is not None:
                    h = h * u
                return h

        return hessian_inverse

    def __call__(self, guess, mask):
        return self.jacobian(guess, mask), self.hessian_inverse(guess, mask)

class NewtonStepFinder:

    def __init__(self, jacobian, hessian=None, check_generator=True, **generator_opts):
        if check_generator:
            generator = self._prep_generator(jacobian, hessian, generator_opts)
        else:
            generator = jacobian
        self.generator = generator

    @classmethod
    def _prep_generator(cls, jac, hess, opts):
        if (hasattr(jac, 'jacobian') and hasattr(jac, 'hessian_inverse')):
            return jac
        else:
            if hess is None:
                raise ValueError(
                    "Direct Netwon requires a Hessian or a generator for the Jacobian and Hessian inverse. "
                    "Consider using Quasi-Newton if only the Jacobian is fast to compute.")
            return NetwonDirectHessianGenerator(jac, hess, **opts)

    def __call__(self, guess, mask):
        jacobian, hessian_inv = self.generator(guess, mask)
        return -(hessian_inv @ jacobian[:, :, np.newaxis]).reshape(jacobian.shape)

class QuasiNewtonStepFinder:

    def __init__(self, func, jacobian, approximation_type='bfgs', **generator_opts):
        self.hess_appx = self.hessian_approximations[approximation_type.lower()](func, jacobian, **generator_opts)
    @property
    def hessian_approximations(self):
        return {
            'bfgs':BFGSApproximator
        }

    def __call__(self, guess, mask):
        gen = self.hess_appx(guess, mask)
        if isinstance(gen, tuple): # uncommon case...
            jacobian, hessian_inv = gen
            return -(hessian_inv @ jacobian)
        else:
            return gen

class QuasiNetwonHessianApproximator:

    line_search = ArmijoSearch
    def __init__(self, func, jacobian, initial_beta=1, damping_parameter=None, damping_exponent=None, restart_interval=10):
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
        self.searcher = self.line_search(func)

    def identities(self, guess, mask):
        if self.eye_tensors is None:
            self.eye_tensors = vec_ops.identity_tensors(guess.shape[:-1], guess.shape[-1])
            return self.eye_tensors
        else:
            return self.eye_tensors[mask,]

    def initialize_hessians(self, guess, mask):
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

    def __call__(self, guess, mask):
        new_jacs, jacobian_diffs = self.get_jacobian_updates(guess, mask)
        if self.prev_step is None:
            new_hess = self.initialize_hessians(guess, mask)
        else:
            prev_steps = self.prev_step[mask,]
            prev_hess = self.prev_hess_inv[mask,]
            new_hess = self.get_hessian_update(self.identities(guess, mask), jacobian_diffs, prev_steps, prev_hess)

        u = self.damper.get_damping_factor()
        if u is not None:
            new_hess = u * new_hess

        # print(new_hess)
        new_step_dir = -(new_hess @ new_jacs[:, :, np.newaxis]).reshape(new_jacs.shape)
        # raise Exception(self.func(guess, mask), new_jacs[:, np.newaxis, :] @ new_step_dir[:, :, np.newaxis])
        alpha, (fvals, is_converged) = self.searcher(guess, new_step_dir, initial_grad=new_jacs)
        # handle convergence issues?
        new_step = alpha[:, np.newaxis] * new_step_dir

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

        return new_step

class BFGSApproximator(QuasiNetwonHessianApproximator):
    def get_hessian_update(self, identities, jacobian_diffs, prev_steps, prev_hess):
        diff_outer = jacobian_diffs[:, np.newaxis, :] * prev_steps[:, :, np.newaxis]
        diff_norm = jacobian_diffs[:, np.newaxis, :] @ prev_steps[:, :, np.newaxis]
        diff_step = identities - diff_outer / diff_norm
        step_outer = prev_steps[:, np.newaxis, :] * prev_steps[:, :, np.newaxis]
        step_step = step_outer / diff_step
        H = diff_step @ prev_hess @ np.moveaxis(diff_step, -1, -2) + step_step
        return H

class ConjugateGradientStepFinder:

    def __init__(self, func, jacobian, approximation_type='fletcher-reeves', **generator_opts):
        self.step_appx = self.beta_approximations[approximation_type.lower()](func, jacobian, **generator_opts)
    @property
    def beta_approximations(self):
        return {
            'fletcher-reeves':FletcherReevesApproximator
        }

    def __call__(self, guess, mask):
        gen = self.step_appx(guess, mask)
        return gen

class ConjugateGradientStepApproximator:
    line_search = ArmijoSearch

    def __init__(self, func, jacobian,
                 # damping_parameter=None, damping_exponent=None,
                 restart_interval=10):
        self.func = func
        self.jac = jacobian
        self.base_hess = None
        self.prev_jac = None
        self.prev_step_dir = None
        # self.damper = Damper(
        #     damping_parameter=damping_parameter,
        #     damping_exponent=damping_exponent,
        #     restart_interval=restart_interval
        # )
        self.n = 0
        self.restart_interval = restart_interval
        self.searcher = self.line_search(func)

    def get_beta(self, new_jacs, prev_jac, prev_step_dir):
        raise NotImplementedError("abstract")

    def __call__(self, guess, mask):
        new_jacs = self.jac(guess, mask)

        if self.prev_jac is None or self.n == 0:
            new_step_dir = -new_jacs
        else:
            prev_jac = self.prev_jac[mask,]
            prev_step_dir = self.prev_step_dir[mask,]
            beta = self.get_beta(new_jacs, prev_jac, prev_step_dir)
            new_step_dir = -new_jacs + beta[:, np.newaxis] * prev_step_dir

        alpha, (fvals, is_converged) = self.searcher(guess, new_step_dir, initial_grad=new_jacs)
        # handle convergence issues?
        new_step = alpha[:, np.newaxis] * new_step_dir

        if self.prev_jac is None:
            self.prev_jac = new_jacs
        else:
            self.prev_jac[mask,] = new_jacs

        if self.prev_step_dir is None:
            self.prev_step_dir = new_step_dir
        else:
            self.prev_step_dir[mask,] = new_step_dir

        self.n = (self.n + 1) % self.restart_interval

        return new_step


class FletcherReevesApproximator(ConjugateGradientStepApproximator):
    def get_beta(self, new_jacs, prev_jac, prev_step_dir):
        return (
                (new_jacs[:, np.newaxis, :] @new_jacs[:, :, np.newaxis]) /
                (prev_jac[:, np.newaxis, :] @ prev_jac[:, :, np.newaxis])
        ).reshape(len(new_jacs))
