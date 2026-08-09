"""
Defines classes for providing different approaches to fitting.
For the most part, the idea is to use `scipy.optimize` to do the actual fitting process,
but we layer on conveniences w.r.t. specification of bases and automation of the actual fitting process
"""
from __future__ import annotations

import abc

from .. import Devutils as dev

import numpy as np, scipy.optimize as opt, enum
import json
from dataclasses import dataclass, field
import scipy.stats
import typing

__all__ = [
    "FittedModel",
    "DistributionKernel",
    "MixtureDistribution",
    "fit_distribution_mixture_model"
]

class FittedModel:
    def __init__(self,
                 fit_basis,
                 expansion_coeffs=None,
                 basis_parameters=None,
                 **kwargs
                 ):
        self.fit_basis, self.basis_parameters = self.canonicalize_basis(fit_basis, basis_parameters)
        self.coeffs = expansion_coeffs
        self.opts = kwargs

    @classmethod
    def canonicalize_basis(cls, fit_basis, basis_parameters):
        if callable(fit_basis):
            fit_basis = [fit_basis]
        if basis_parameters is None or dev.is_dict_like(basis_parameters):
            basis_parameters = [basis_parameters] * len(fit_basis)

        return fit_basis, basis_parameters

    def __call__(self, pts, order=None, **opts):
        opts = dict(self.opts, **opts)
        return self.evaluate_kernel(
            self.fit_basis,
            self.basis_parameters,
            pts,
            coeffs=self.coeffs,
            order=order,
            **opts
        )

    @classmethod
    def evaluate_kernel(cls,
                        fit_basis,
                        basis_parameters,
                        pts,
                        coeffs=None,
                        order=None,
                        **opts
                        ):
        if order is None:
            kernel_expansions = [
                [
                    f(pts, **(params if params is not None else {}), **opts)
                    for f, params in zip(fit_basis, basis_parameters)
                ]
            ]
        else:
            kernel_expansions = [
                f(pts, order=order, **(params if params is not None else {}), **opts)
                for f, params in zip(fit_basis, basis_parameters)
            ]
            kernel_expansions = [
                [k[o] for k in kernel_expansions]
                for o in range(order + 1)
            ]

        if coeffs is not None:
            val_expansions = [np.dot(coeffs, k) for k in kernel_expansions]
        else:
            val_expansions = [sum(k) for k in kernel_expansions]

        if order is None:
            return val_expansions[0]
        else:
            return val_expansions

    @classmethod
    def _handle_nl_fit_params(cls,
                              params,
                              kernels,
                              param_names,
                              include_expansion_coefficients=True
                              ):
        if include_expansion_coefficients:
            n = len(kernels)
            coeffs, params = params[-n:], params[:-n]
        else:
            coeffs = None

        parameter_lists = []
        k = 0
        for pl in param_names:
            e = k+len(pl)
            parameter_lists.append(
                zip(pl, params[k:e])
            )
            k = e
        if k < len(params) - 1:
            raise ValueError(f"params of len {len(params)} don't distribute into names {param_names}")

        return coeffs, parameter_lists

    @classmethod
    def get_kernel_and_opts(cls, k):
        func, opts = k  # TODO: make this more flexible down the line
        if dev.is_dict_like(opts):
            names = list(opts.keys())
            vals = list(opts.values())
        else:
            names = list(opts)
            vals = [None] * len(names)
        vals = [
            v
                if v is not None else
            np.random.rand()
            for v in vals
        ]
        return func, names, vals
    @classmethod
    def parse_kernel_specs(cls, kernels):
        if dev.is_dict_like(kernels):
            kernels = [kernels]
        funcs = []
        param_names = []
        param_defaults = []
        for k in kernels:
            f, n, d = cls.get_kernel_and_opts(k)
            funcs.append(f)
            param_names.append(n)
            param_defaults.extend(d)

        return funcs, param_names, param_defaults

    @classmethod
    def nonlinear_fit(cls,
                      kernel_specs,
                      pts,
                      observations,
                      include_expansion_coefficients=True,
                      **fit_params
                      ):
        kernels, param_names, param_defaults = cls.parse_kernel_specs(kernel_specs)
        if include_expansion_coefficients:
            param_defaults = np.concatenate([np.array(param_defaults, dtype=float), np.ones(len(kernels), dtype=float)])
        def f(x, params):
            coeffs, basis_parameters = cls._handle_nl_fit_params(
                params,
                kernels,
                param_names,
                include_expansion_coefficients=include_expansion_coefficients
            )
            return cls.evaluate_kernel(
                kernels,
                basis_parameters,
                x,
                coeffs=coeffs
            )
        # def jac():

        opt_params, _ = opt.curve_fit(
            f,
            pts,
            observations,
            param_defaults,
            fit_params,
            full_output=False
        )

        coeffs, param_dicts = cls._handle_nl_fit_params(
            opt_params, kernels, param_names,
            include_expansion_coefficients=include_expansion_coefficients
        )

        return cls(
            kernels,
            expansion_coeffs=coeffs,
            basis_parameters=param_dicts
        )
        # return cls.from_fit(
        #     kernels,
        #     param_names,
        #     fit
        # )

    @classmethod
    def get_fit_methods(cls):
        return {
            'nonlinear_fit':cls.nonlinear_fit
        }

    _fit_dispatch = dev.uninitialized
    default_fit_method = 'nonlinear_fit'
    @classmethod
    def get_fit_dispatch(cls):
        cls._fit_dispatch = dev.handle_uninitialized(
            cls._fit_dispatch,
            dev.OptionsMethodDispatch,
            args=(cls.get_fit_methods,),
            kwargs=dict(
                default_method=cls.default_fit_method,
                # attributes_map=cls.get_evaluators_by_attributes()
            )
        )
        return cls._fit_dispatch
    @classmethod
    def fit(cls,
            kernels,
            pts,
            observations,
            method=None,
            **opts
            ):

        fit_method, method_opts = cls.get_fit_dispatch().resolve(method)
        return fit_method(
            kernels,
            pts,
            observations,
            **dict(method_opts, **opts)
        )

"""
A general framework for fitting k-component mixture distributions with
swappable, per-component kernels (e.g. some components Gaussian, some
Cauchy, mixed freely in one model), in-core or out-of-core.

Architecture
------------
`Kernel` is a strategy object: it knows how to compute its own log-density
and how to update its own parameters from responsibility-weighted data. The
EM loop (`_fit_em_over_slices`) is entirely kernel-agnostic -- it just:

  1. E-step: asks each component's kernel for log_pdf(x, params), combines
     them with mixture weights via log-sum-exp to get responsibilities.
  2. M-step: asks each component's kernel to accumulate sufficient
     statistics from (x, responsibility), then finalize() them into new
     parameters.

Because every kernel's sufficient statistics are additive across chunks,
this same loop handles in-core, out-of-core, and sampled fitting exactly
as before -- see `_iter_slices` / `_resolve_chunk_size` for that mechanism,
unchanged from the Gaussian-only version.

Kernels included
-----------------
  GaussianKernel       : linear, light (exponential) tails.
  CauchyKernel          : linear, heavy (1/x^2) tails -- fit via the
                          Student-t(nu=1) scale-mixture EM trick.
  VonMisesKernel        : periodic analogue of Gaussian.
  WrappedCauchyKernel   : periodic analogue of Cauchy -- its weighted MLE
                          turns out to be *exactly* the mean resultant
                          vector (no iterative trick needed at all; see
                          its docstring).

All linear kernels can be freely mixed with each other; all periodic
kernels can be freely mixed with each other. Mixing linear and periodic
kernels in the same model is rejected (they don't describe the same
sample space).

Write your own kernel by subclassing `Kernel` and implementing its four
abstract methods -- it will work with in-core, out-of-core, sampled
fitting and `.update()` for free.
"""




# ---------------------------------------------------------------------------
# Kernel interface
# ---------------------------------------------------------------------------
class DistributionKernel(abc.ABC):
    """
    Strategy interface for one mixture component's distribution family.
    `params` is always a 2-tuple (location, scale-like) -- what "scale-like"
    means is kernel-specific (std, Cauchy scale, von Mises kappa, wrapped
    Cauchy rho), but every kernel takes exactly two parameters so they can
    be swapped in and out of a model uniformly.
    """

    name: str
    __slots__ = ("params",)

    # Registry mapping kernel class name -> class, used by Kernel.from_state to
    # reconstruct the right kernel type from a serialized state dict.
    registry: dict = {}
    @classmethod
    def register(cls, name, kernel=None):
        if kernel is not None:
            kernel.name = name
            cls.registry[name] = kernel
            return kernel
        else:
            def register(kernel):
                return cls.register(name, kernel)
            return register
    @classmethod
    def resolve(cls, name, *args):
        return cls.registry[name](*args)

    #: True for kernels defined on a circle (mixing periodic and
    #: non-periodic kernels in one model is rejected).
    periodic: bool = False

    param_names: typing.Tuple[str]

    @abc.abstractmethod
    def log_pdf(self, x: np.ndarray, params: tuple[float, float]) -> np.ndarray:
        """Log-density at each point in `x` given this component's params."""

    @abc.abstractmethod
    def pdf(self, x: np.ndarray, params: tuple[float, float]) -> np.ndarray:
        """Density at each point in `x` given this component's params."""

    @abc.abstractmethod
    def cdf(self, x: np.ndarray, params: tuple[float, float]) -> np.ndarray:
        """CDF at each point in `x` given this component's params. Always
        required (used both for mixture .cdf() and as the fallback root-
        finding target when a kernel has no closed-form .ppf)."""

    def ppf(self, q: np.ndarray, params: tuple[float, float]=None) -> np.ndarray:
        """
        Closed-form inverse CDF for this *single* kernel (not the overall
        mixture, which never has one). Override this in a subclass when
        scipy provides one directly (see GaussianKernel/CauchyKernel/etc).
        The default raises NotImplementedError, which signals
        `MixtureDistribution` to fall back to numeric root-finding against
        `cdf` when determining grid bounds for a kernel of this type.
        """
        raise NotImplementedError

    def copy(self):
        return type(self).from_state(self.to_state())

    def to_state(self) -> dict:
        """Serialize this kernel's identity/config to a plain (JSON-able)
        dict. The default assumes no constructor arguments; override
        alongside `from_state` if a subclass needs to save extra config."""
        return {"type": self.name, 'params':self.params}

    @classmethod
    def from_state(cls, state: dict) -> "DistributionKernel":
        """Reconstruct a kernel instance from a dict produced by
        `to_state`. Looks the type up in the kernel registry, so any
        `Kernel` subclass works automatically as long as it's been
        defined (and decorated with `@_register_kernel`, or otherwise
        registered) before this is called."""
        kernel_cls = cls.registry[state["type"]]
        return kernel_cls(*state["params"])

    @abc.abstractmethod
    def new_stats(self) -> dict:
        """Zero-initialized accumulator dict for one EM pass."""

    @abc.abstractmethod
    def accumulate(self, stats: dict, x: np.ndarray, resp: np.ndarray, params) -> None:
        """Add one chunk's contribution to `stats`, in place."""

    @abc.abstractmethod
    def finalize(self, stats: dict, min_scale: float) -> tuple[float, float]:
        """Compute updated (loc, scale-like) from accumulated `stats`."""


@DistributionKernel.register('normal')
class GaussianKernel(DistributionKernel):
    """Light (exponential) tails. params = (mean, std)."""

    param_names = ("mean", "std")
    def __init__(self, mean: float, std: float):
        self.params = (mean, std)

    def log_pdf(self, x, params=None):
        if params is None: params = self.params
        mean, std = params
        var = std**2
        return -0.5 * np.log(2 * np.pi * var) - 0.5 * (x - mean) ** 2 / var

    def pdf(self, x, params=None):
        if params is None: params = self.params
        mean, std = params
        return scipy.stats.norm.pdf(x, loc=mean, scale=std)

    def cdf(self, x, params=None):
        if params is None: params = self.params
        mean, std = params
        return scipy.stats.norm.cdf(x, loc=mean, scale=std)

    def ppf(self, q, params=None):
        if params is None: params = self.params
        mean, std = params
        return scipy.stats.norm.ppf(q, loc=mean, scale=std)

    def new_stats(self):
        return {"N": 0.0, "S": 0.0, "SS": 0.0}

    def accumulate(self, stats, x, resp, params):
        stats["N"] += resp.sum()
        stats["S"] += (resp * x).sum()
        stats["SS"] += (resp * x**2).sum()

    def finalize(self, stats, min_scale):
        N = max(stats["N"], 1e-12)
        mean = stats["S"] / N
        var = max(stats["SS"] / N - mean**2, min_scale**2)
        return (mean, np.sqrt(var))


@DistributionKernel.register('cauchy')
class CauchyKernel(DistributionKernel):
    """
    Heavy (1/x^2) tails. params = (loc, scale).

    Cauchy is Student-t with 1 degree of freedom, which is a Gaussian
    scale-mixture: x | u ~ N(loc, scale^2/u). The E-step for this latent
    weight, given current params, is u_i = 2 / (1 + ((x_i-loc)/scale)^2)
    (the nu=1 case of the general Student-t EM weight (nu+1)/(nu+z^2)).
    The M-step is then a responsibility-*and*-u-weighted Gaussian update.
    This is the standard ECM algorithm for a t-mixture (McLachlan &
    Peel, "Finite Mixture Models", ch. 7) specialized to nu=1; it
    monotonically increases the likelihood just like ordinary EM.
    """

    param_names = ("loc", "scale")
    def __init__(self, loc: float, scale: float):
        self.params = (loc, scale)

    def log_pdf(self, x, params=None):
        if params is None: params = self.params
        loc, scale = params
        z = (x - loc) / scale
        return -np.log(np.pi * scale) - np.log1p(z**2)

    def pdf(self, x, params=None):
        if params is None: params = self.params
        loc, scale = params
        return scipy.stats.cauchy.pdf(x, loc=loc, scale=scale)

    def cdf(self, x, params=None):
        if params is None: params = self.params
        loc, scale = params
        return scipy.stats.cauchy.cdf(x, loc=loc, scale=scale)

    def ppf(self, q, params=None):
        if params is None: params = self.params
        loc, scale = params
        return scipy.stats.cauchy.ppf(q, loc=loc, scale=scale)

    def new_stats(self):
        return {"N": 0.0, "Nu": 0.0, "Sxu": 0.0, "Sxxu": 0.0}

    def accumulate(self, stats, x, resp, params):
        loc, scale = params
        z = (x - loc) / scale
        u = 2.0 / (1.0 + z**2)  # E[latent precision] for Cauchy (nu=1)
        ru = resp * u
        stats["N"] += resp.sum()
        stats["Nu"] += ru.sum()
        stats["Sxu"] += (ru * x).sum()
        stats["Sxxu"] += (ru * x**2).sum()

    def finalize(self, stats, min_scale):
        N = max(stats["N"], 1e-12)
        Nu = max(stats["Nu"], 1e-12)
        loc = stats["Sxu"] / Nu
        # Expand sum(r*u*(x-loc)^2) algebraically so no second data pass
        # is needed: = Sxxu - 2*loc*Sxu + loc^2*Nu
        resid = stats["Sxxu"] - 2 * loc * stats["Sxu"] + loc**2 * Nu
        scale2 = max(resid / N, min_scale**2)
        return (loc, np.sqrt(scale2))


@DistributionKernel.register('vonmises')
class VonMisesKernel(DistributionKernel):
    """Periodic analogue of Gaussian. params = (mean, kappa)."""

    periodic = True
    param_names = ("mean", "kappa")
    def __init__(self, mean: float, kappa: float):
        self.params = (mean, kappa)

    def log_pdf(self, x, params=None):
        if params is None: params = self.params
        mean, kappa = params
        from scipy.special import ive
        # cos(x - mean) is already periodic, so x needs no manual wrapping
        return (
            kappa * (np.cos(x - mean) - 1.0)
            - np.log(2 * np.pi)
            - np.log(ive(0, kappa) + 1e-300)
        )

    def pdf(self, x, params=None):
        if params is None: params = self.params
        mean, kappa = params
        xw = np.mod(x + np.pi, 2 * np.pi) - np.pi
        muw = np.mod(mean + np.pi, 2 * np.pi) - np.pi
        return scipy.stats.vonmises.pdf(xw, kappa=kappa, loc=muw)

    def cdf(self, x, params=None):
        if params is None: params = self.params
        mean, kappa = params
        xw = np.mod(x + np.pi, 2 * np.pi) - np.pi
        muw = np.mod(mean + np.pi, 2 * np.pi) - np.pi
        return scipy.stats.vonmises.cdf(xw, kappa=kappa, loc=muw)

    def ppf(self, q, params=None):
        if params is None: params = self.params
        mean, kappa = params
        muw = np.mod(mean + np.pi, 2 * np.pi) - np.pi
        return scipy.stats.vonmises.ppf(q, kappa=kappa, loc=muw)

    def new_stats(self):
        return {"N": 0.0, "C": 0.0, "S": 0.0}

    def accumulate(self, stats, x, resp, params):
        stats["N"] += resp.sum()
        stats["C"] += (resp * np.cos(x)).sum()
        stats["S"] += (resp * np.sin(x)).sum()

    def finalize(self, stats, min_scale):
        N = max(stats["N"], 1e-12)
        mean = np.arctan2(stats["S"], stats["C"])
        R = np.sqrt(stats["C"] ** 2 + stats["S"] ** 2) / N
        kappa = min(_kappa_from_R(R), 1.0 / min_scale**2)
        return (mean, kappa)


@DistributionKernel.register('wrapcauchy')
class WrappedCauchyKernel(DistributionKernel):
    """
    Periodic analogue of Cauchy. params = (mean, rho), 0 <= rho < 1.

    Unlike linear Cauchy, this needs no scale-mixture trick: the wrapped
    Cauchy's characteristic function is rho^|n| * exp(i*n*mu), so its
    first trigonometric moment E[exp(i*theta)] = rho * exp(i*mu) *exactly*
    -- the mean resultant vector directly gives both parameters, the same
    simple sufficient statistics as VonMisesKernel, just without needing
    to invert a Bessel-function ratio for the concentration.
    """

    periodic = True
    param_names = ("mean", "rho")
    def __init__(self, mean: float, rho: float):
        self.params = (mean, rho)

    def log_pdf(self, x, params=None):
        if params is None: params = self.params
        mean, rho = params
        return (
            np.log1p(-(rho**2))
            - np.log(2 * np.pi)
            - np.log1p(rho**2 - 2 * rho * np.cos(x - mean))
        )

    def pdf(self, x, params=None):
        if params is None: params = self.params
        mean, rho = params
        xw = np.mod(x - mean, 2 * np.pi)
        return scipy.stats.wrapcauchy.pdf(xw, c=rho)

    def cdf(self, x, params=None):
        if params is None: params = self.params
        mean, rho = params
        xw = np.mod(x - mean, 2 * np.pi)
        return scipy.stats.wrapcauchy.cdf(xw, c=rho)

    def ppf(self, q, params=None):
        if params is None: params = self.params
        mean, rho = params
        # ppf of the shifted (loc=0) distribution, then re-add the mean;
        # wrapcauchy's own loc handling has the same wrap caveats as pdf,
        # so we shift manually instead.
        return mean + scipy.stats.wrapcauchy.ppf(q, c=rho)

    def new_stats(self):
        return {"N": 0.0, "C": 0.0, "S": 0.0}

    def accumulate(self, stats, x, resp, params):
        stats["N"] += resp.sum()
        stats["C"] += (resp * np.cos(x)).sum()
        stats["S"] += (resp * np.sin(x)).sum()

    def finalize(self, stats, min_scale):
        N = max(stats["N"], 1e-12)
        mean = np.arctan2(stats["S"], stats["C"])
        R = np.sqrt(stats["C"] ** 2 + stats["S"] ** 2) / N
        rho = min(R, 1.0 - min_scale)
        return (mean, rho)

@DistributionKernel.register('scipy')
class ScipyKernel(DistributionKernel):
    """
    Generic wrapper around *any* scipy.stats continuous location-scale
    distribution (e.g. `scipy.stats.laplace`, `scipy.stats.gumbel_r`,
    `scipy.stats.logistic`, `scipy.stats.t(df=3)` via a frozen dist).
    params = (loc, scale), same convention as every other kernel here.

    log_pdf / pdf / cdf / ppf all simply delegate to the wrapped
    distribution -- scipy already implements these correctly for
    essentially every distribution it has, so there's nothing to write.

    The one thing scipy doesn't hand you is a *weighted* update rule for
    the EM M-step -- a closed-form weighted MLE only exists for specific
    families (that's exactly why CauchyKernel needed the scale-mixture
    trick rather than just wrapping scipy.stats.cauchy directly). Rather
    than requiring a bespoke derivation per distribution, this kernel
    uses **method of moments** as a generic, streaming-friendly M-step:
    it reuses the same (N, S, SS) responsibility-weighted sums as
    GaussianKernel to get a weighted mean/variance, then inverts the
    distribution's own theoretical standardized mean/variance -- free
    from `dist.stats(moments='mv')` -- to solve for (loc, scale):

        mean_hat = loc + scale * std_mean
        var_hat  = scale^2 * std_var
        =>  scale = sqrt(var_hat / std_var),  loc = mean_hat - scale*std_mean

    This works for *any* scipy loc-scale distribution with finite
    mean/variance, needs no per-distribution derivation, and keeps the
    same O(chunk) memory footprint as every other kernel -- no need to
    retain raw data or run an optimizer during the M-step.

    Caveat: it's a moment-matching estimator, not the MLE -- exact only
    when mean/variance happen to be sufficient statistics (as for
    Gaussian). For skewed or heavy-tailed distributions it'll converge to
    a slightly different, less efficient answer than true MLE would. If
    you need the exact MLE and your data fits in memory (e.g. a
    `sample_size`-based fit, whose `_sample` is retained), you can
    refine afterward with `scipy.stats.<dist>.fit(sample, ...)`, or
    weighted via `scipy.optimize.minimize` on the negative weighted
    log-likelihood -- moment-matching's role here is just getting a
    fast, streaming-compatible EM to the right neighborhood.
    """

    __slots__ = ("params", "dist", "_std_mean", "_std_var")
    def __init__(self, dist, loc, scale):
        self.params = (loc, scale)
        self.dist = dist  # a scipy.stats.rv_continuous instance/frozen dist
        self._std_mean, self._std_var = dist.stats(moments="mv")

    def log_pdf(self, x, params=None):
        if params is None: params = self.params
        loc, scale = params
        return self.dist.logpdf(x, loc=loc, scale=scale)

    def pdf(self, x, params=None):
        if params is None: params = self.params
        loc, scale = params
        return self.dist.pdf(x, loc=loc, scale=scale)

    def cdf(self, x, params=None):
        if params is None: params = self.params
        loc, scale = params
        return self.dist.cdf(x, loc=loc, scale=scale)

    def ppf(self, q, params=None):
        if params is None: params = self.params
        loc, scale = params
        return self.dist.ppf(q, loc=loc, scale=scale)

    def new_stats(self):
        return {"N": 0.0, "S": 0.0, "SS": 0.0}

    def accumulate(self, stats, x, resp, params):
        stats["N"] += resp.sum()
        stats["S"] += (resp * x).sum()
        stats["SS"] += (resp * x**2).sum()

    def finalize(self, stats, min_scale):
        N = max(stats["N"], 1e-12)
        mean_hat = stats["S"] / N
        var_hat = max(stats["SS"] / N - mean_hat**2, min_scale**2)
        scale = max(np.sqrt(var_hat / self._std_var), min_scale)
        loc = mean_hat - scale * self._std_mean
        return (float(loc), float(scale))

    def to_state(self):
        return {"type": type(self).__name__,
                "dist_name": self.dist.name,
                "params":self.params}

    @classmethod
    def from_state(cls, state):
        return cls(getattr(scipy.stats, state["dist_name"]), *state["params"])


def _kappa_from_R(R):
    """Invert A(kappa) = I1(kappa)/I0(kappa) = R via the standard
    piecewise closed-form approximation (Best & Fisher, 1981)."""
    R = float(np.clip(R, 1e-8, 1 - 1e-8))
    if R < 0.53:
        return 2 * R + R**3 + 5 * R**5 / 6
    if R < 0.85:
        return -0.4 + 1.39 * R + 0.43 / (1 - R)
    return 1 / (R**3 - 4 * R**2 + 3 * R)


# ---------------------------------------------------------------------------
# Result objects
# ---------------------------------------------------------------------------
@dataclass(kw_only=True)
class MixtureDistribution:
    """
    A k-component mixture distribution with a (possibly heterogeneous)
    kernel per component -- the "just the math" parent class. Knows how
    to evaluate pdf/cdf, build and use a numeric ppf (inverse CDF), and
    save/load that ppf to disk. Doesn't know or care how it was produced;
    see `FittedMixtureDistribution` for the subclass that adds that.

    Attributes
    ----------
    kernels : list[Kernel], length k
        One kernel instance per component; may be different types (but
        all must agree on `.periodic`).
    params : list[tuple[float, float]], length k
        (loc, scale-like) parameters per component, matching
        `kernels[j].param_names`.
    weights : np.ndarray, shape (k,)
    """

    kernels: list
    weights: np.ndarray
    _ppf_grid: np.ndarray = field(default=None, repr=False)
    _ppf_values: np.ndarray = field(default=None, repr=False)

    def __post_init__(self):
        self.weights = np.asarray(self.weights, dtype=np.float64)
        self.weights = self.weights / np.sum(self.weights)

    @property
    def k(self) -> int:
        return len(self.kernels)

    @property
    def periodic(self) -> bool:
        return self.kernels[0].periodic

    def component_pdfs(self, x):
        """Weighted per-component densities at `x`, shape (*, k). Useful
        for plotting each colored component curve individually."""
        x = np.asarray(x, dtype=np.float64)
        return np.stack(
            [self.weights[j] * self.kernels[j].pdf(x) for j in range(self.k)],
            axis=-1,
        )

    def pdf(self, x):
        """Mixture density at `x`: sum of weighted per-component densities."""
        return self.component_pdfs(x).sum(axis=-1)

    def component_cdfs(self, x):
        """Weighted per-component CDFs at `x`, shape (*, k)."""
        x = np.asarray(x, dtype=np.float64)
        return np.stack(
            [self.weights[j] * self.kernels[j].cdf(x) for j in range(self.k)],
            axis=-1,
        )

    def cdf(self, x):
        """
        Mixture CDF at `x`: sum of weighted per-component CDFs. Always
        available in closed form (every kernel supplies `.cdf` via
        scipy), even for kernels/mixtures with no closed-form `.ppf`.

        Note: for a periodic mixture this is itself periodic --
        cdf(x) == cdf(x + 2*pi) exactly, since they're the same physical
        angle. That's correct for density/mass questions (and matches
        pdf's periodicity), but it is *not* usable as a monotonic
        quantile map across a full period -- see `unwrapped_cdf` for
        that.
        """
        return self.component_cdfs(x).sum(axis=-1)

    def unwrapped_cdf(self, x, grid_size=2000, eps=1e-9, rebuild=False):
        """
        A monotonically increasing "unwrapped" CDF across one full
        period (0 -> 1 as x sweeps from the period's start to its end),
        for periodic mixtures. Non-periodic mixtures just delegate to
        the ordinary `.cdf()`, which is already monotonic.

        Built from the same (q, x) PPF grid used by `.ppf()` (lazily
        built on first call, exactly like `.ppf()`), inverted the other
        way via interpolation -- i.e. this and `.ppf()` are exact
        inverses of each other by construction, which `.cdf()` is not
        for a periodic mixture.

        This exists for callers that need a proper quantile map spanning
        a full period (e.g. truncated-quantile encoding schemes) rather
        than the periodic `.cdf()`, which wraps back to its starting
        value before reaching 1.
        """
        if not self.periodic:
            return self.cdf(x)
        if self._ppf_grid is None or rebuild:
            self._build_ppf_grid(grid_size=grid_size, eps=eps)
        x = np.asarray(x, dtype=np.float64)
        return np.interp(x, self._ppf_values, self._ppf_grid)

    def _support_bounds(self, eps):
        """
        Determine (lo, hi) x-bounds covering ~all the mixture's mass, for
        building the ppf grid. Periodic mixtures use their fixed domain
        directly. For linear mixtures, each component contributes its own
        [eps, 1-eps] range -- via that kernel's closed-form `.ppf` if it
        has one, else via a generic expanding-bracket search against
        `.cdf` -- and the overall bounds are the union across components.
        """
        if self.periodic:
            return 0.0, 2 * np.pi

        los, his = [], []
        for kernel in self.kernels:
            try:
                lo = float(kernel.ppf(eps))
                hi = float(kernel.ppf(1 - eps))
            except NotImplementedError:
                lo, hi = self._bisect_support_bounds(kernel, eps)
            los.append(lo)
            his.append(hi)
        return min(los), max(his)

    def _build_ppf_grid(self, grid_size=2000, eps=1e-9, per_component_grid_size=2000):
        """
        Populate `_ppf_grid` (q values) / `_ppf_values` (corresponding x
        values) by: (1) building a fine x-grid, (2) evaluating the
        mixture CDF on it, (3) inverting at a coarser, evenly-spaced set
        of q values via linear interpolation. Storing the *inverted*
        (q, x) pairs -- rather than the raw (x, cdf) grid -- means
        `.ppf()` and the saved file are a direct, cheap lookup with no
        re-inversion needed later.

        The fine x-grid is *not* uniformly spaced in x for linear
        mixtures: with a heavy-tailed component in the mix (e.g. Cauchy),
        a handful of extreme-quantile points can be many orders of
        magnitude beyond where nearly all the probability mass actually
        sits, and a uniform grid between them wastes almost all its
        resolution on essentially-empty tails. Instead, the fine grid is
        built as the union of each component's *own* ppf evaluated on a
        fine q grid -- this naturally concentrates points near wherever
        each component has mass, at whatever scale that is, while still
        reaching into the tails via q close to eps/1-eps.
        """
        if self.periodic:
            lo, hi = self._support_bounds(eps)
            x_fine = np.linspace(lo, hi, per_component_grid_size * max(self.k, 1))
            # Periodic kernels' own .cdf() is correct for single-point
            # queries (deliberately periodic: cdf(x) == cdf(x + 2*pi)),
            # but that means it's *discontinuous* when swept continuously
            # across a full period -- exactly what building this grid
            # needs. Building the cumulative distribution by numerically
            # integrating the (always-correct, genuinely periodic) pdf
            # instead sidesteps that, and works for any kernel without
            # needing a kernel-specific "unwrapped cdf" implementation.
            pdf_fine = self.pdf(x_fine)
            segment_areas = 0.5 * (pdf_fine[:-1] + pdf_fine[1:]) * np.diff(x_fine)
            cdf_fine = np.concatenate(([0.0], np.cumsum(segment_areas)))
            if cdf_fine[-1] > 0:
                cdf_fine = cdf_fine / cdf_fine[-1]
        else:
            qs = np.linspace(eps, 1 - eps, per_component_grid_size)
            x_points = []
            for kernel in self.kernels:
                try:
                    x_points.append(np.atleast_1d(kernel.ppf(qs)))
                except NotImplementedError:
                    lo, hi = self._bisect_support_bounds(kernel, eps)
                    x_points.append(np.linspace(lo, hi, per_component_grid_size))
            x_fine = np.unique(np.concatenate(x_points))
            cdf_fine = self.cdf(x_fine)

        # guard against tiny numerical non-monotonicity before inverting
        cdf_fine = np.maximum.accumulate(cdf_fine)
        cdf_fine = np.clip(cdf_fine, 0.0, 1.0)

        q_grid = np.linspace(eps, 1 - eps, grid_size)
        x_values = np.interp(q_grid, cdf_fine, x_fine)

        self._ppf_grid = q_grid
        self._ppf_values = x_values

    def ppf(self, q, grid_size=2000, eps=1e-9, rebuild=False):
        """
        Inverse CDF, via grid-based linear interpolation over precomputed
        (q, x) pairs -- built lazily on first call (or forced with
        `rebuild=True`), since a mixture's CDF essentially never has a
        closed-form inverse even when every component's CDF does.
        """
        if self._ppf_grid is None or rebuild:
            self._build_ppf_grid(grid_size=grid_size, eps=eps)
        q = np.asarray(q, dtype=np.float64)
        return np.interp(q, self._ppf_grid, self._ppf_values)

    def save_ppf_grid(self, path, grid_size=2000, eps=1e-9):
        """
        Save the ppf grid to an NPZ file: `ppf_grid` (q values),
        `ppf_values` (corresponding x values), and `metadata` (a JSON
        string describing each component's kernel type, params, and
        weight -- enough to fully reconstruct this mixture via
        `MixtureDistribution.load_ppf_grid`).
        """
        if self._ppf_grid is None:
            self._build_ppf_grid(grid_size=grid_size, eps=eps)

        metadata = {
            "components": [
                {
                    "kernel": self.kernels[j].to_state(),
                    "weight": float(self.weights[j]),
                }
                for j in range(self.k)
            ]
        }
        np.savez(
            path,
            metadata=json.dumps(metadata),
            ppf_grid=self._ppf_grid,
            ppf_values=self._ppf_values,
        )

    @classmethod
    def load_ppf_grid(cls, path) -> "MixtureDistribution":
        """
        Reconstruct a `MixtureDistribution` (kernels, params, weights,
        and the precomputed ppf grid) from a file written by
        `save_ppf_grid`. The result supports `.pdf`/`.cdf`/`.ppf`
        immediately; `.ppf` uses the loaded grid without recomputing it.
        """
        with np.load(path, allow_pickle=False) as data:
            metadata = json.loads(data["metadata"].item())
            ppf_grid = data["ppf_grid"]
            ppf_values = data["ppf_values"]

        kernels = [DistributionKernel.from_state(c["kernel"]) for c in metadata["components"]]
        weights = np.array([c["weight"] for c in metadata["components"]])

        obj = cls(kernels=kernels, weights=weights)
        obj._ppf_grid = ppf_grid
        obj._ppf_values = ppf_values
        return obj

    def __repr__(self):
        header = f"{type(self).__name__}(k={self.k})"
        rows = []
        for j in range(self.k):
            kernel = self.kernels[j]
            pname0, pname1 = kernel.param_names
            p0, p1 = kernel.params
            rows.append(
                f"  [{j}] {kernel.__class__.__name__:<20s} weight={self.weights[j]:.4f}  "
                f"{pname0}={p0:.4f}  {pname1}={p1:.4f}"
            )
        return "\n".join([header, *rows])

    @staticmethod
    def _bisect_support_bounds(kernel, eps, max_expansions=200):
        """
        Generic fallback for kernels with no closed-form `.ppf`: find x-bounds
        such that kernel.cdf(lo) <= eps and kernel.cdf(hi) >= 1-eps, by
        expanding a bracket outward from the kernel's own location parameter.
        Only used when a custom kernel doesn't override `Kernel.ppf`.
        """
        loc, scale = kernel.params #TODO: make this less specific
        scale = max(abs(scale), 1e-6)

        lo, step = loc, scale
        for _ in range(max_expansions):
            if kernel.cdf(np.array([lo]))[0] <= eps:
                break
            lo -= step
            step *= 2

        hi, step = loc, scale
        for _ in range(max_expansions):
            if kernel.cdf(np.array([hi]))[0] >= 1 - eps:
                break
            hi += step
            step *= 2

        return lo, hi


@dataclass(kw_only=True)
class FittedMixtureDistribution(MixtureDistribution):
    """
    A `MixtureDistribution` that also remembers how it was fit, so it can
    be refined with `.update()` -- see `fit_mixture`.

    Additional attributes
    ----------------------
    log_likelihood, n_iter, n_samples, method :
        Same meaning as in the earlier Gaussian-only version. `method` is
        one of "in-core", "out-of-core", "sampled".
    """

    log_likelihood: float
    n_iter: int
    n_samples: int
    method: str
    _fit_kwargs: dict = field(default_factory=dict, repr=False)
    _sample: np.ndarray = field(default=None, repr=False)

    def __repr__(self):
        header = (
            f"FittedMixtureDistribution(method={self.method!r}, k={self.k}, "
            f"n_samples={self.n_samples}, n_iter={self.n_iter}, "
            f"log_likelihood={self.log_likelihood:.4f})"
        )
        rows = []
        for j in range(self.k):
            kernel = self.kernels[j]
            pname0, pname1 = kernel.param_names
            p0, p1 = kernel.params
            rows.append(
                f"  [{j}] {kernel.__class__.__name__:<20s} weight={self.weights[j]:.4f}  "
                f"{pname0}={p0:.4f}  {pname1}={p1:.4f}"
            )
        return "\n".join([header, *rows])

    def update(
        self,
        additional_sample_size=None,
        more_data=None,
        seed=None,
        max_iter=100,
        tol=1e-6,
        min_scale=1e-6,
        verbose=False,
    ):
        """
        Refine this fit in place using more data, warm-started from the
        current parameters. Semantics mirror the Gaussian-only version:

        - method == "sampled": draw `additional_sample_size` more values
          from the original source (or pass already-sampled `more_data`),
          concatenate with the retained sample, refit exactly on the
          combined sample.
        - method in ("in-core", "out-of-core"): refit over the (possibly
          grown) source -- pass `more_data` if it's a new/bigger object,
          otherwise the original reference is reused (e.g. if it was
          resized in place). Warm-started, so this typically converges in
          far fewer iterations than a cold start.

        Returns `self` for chaining.
        """
        if self.method == "sampled":
            if more_data is not None:
                new_x = np.asarray(more_data, dtype=np.float64)
            elif additional_sample_size is not None:
                new_x = sample_masked_values(
                    self._fit_kwargs["data"],
                    additional_sample_size,
                    mask_fn=self._fit_kwargs.get("mask_fn"),
                    vals_key=self._fit_kwargs.get("vals_key", "vals"),
                    chunk_size=self._fit_kwargs.get("chunk_size"),
                    seed=seed,
                )
            else:
                raise ValueError(
                    "Provide additional_sample_size or more_data to update "
                    "a sampled fit."
                )

            combined = np.concatenate([self._sample, new_x])
            params, weights, ll, n_iter, n_used = _fit_em_over_slices(
                data=combined,
                vals=combined,
                mask_fn=_no_mask,
                n=combined.shape[0],
                chunk_size=None,
                kernels=self.kernels,
                params=self.params,
                weights=self.weights.copy(),
                max_iter=max_iter,
                tol=tol,
                min_scale=min_scale,
                verbose=verbose,
            )
            self.params, self.weights = params, weights
            self.log_likelihood, self.n_iter, self.n_samples = ll, n_iter, n_used
            self._sample = combined
            return self

        data = more_data if more_data is not None else self._fit_kwargs["data"]
        updated = fit_distribution_mixture_model(
            data,
            kernels=self.kernels,
            params_init=self.params,
            weights_init=self.weights,
            mask_fn=self._fit_kwargs.get("mask_fn"),
            vals_key=self._fit_kwargs.get("vals_key", "vals"),
            chunk_size=self._fit_kwargs.get("chunk_size"),
            max_iter=max_iter,
            tol=tol,
            min_scale=min_scale,
            verbose=verbose,
        )
        self.params, self.weights = updated.params, updated.weights
        self.log_likelihood = updated.log_likelihood
        self.n_iter = updated.n_iter
        self.n_samples = updated.n_samples
        self._fit_kwargs["data"] = data
        return self

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def fit_distribution_mixture_model(
    data,
    kernels,
    weights_init=None,
    mask_fn=None,
    vals_key="vals",
    chunk_size=None,
    sample_size=None,
    seed=None,
    max_iter=100,
    tol=1e-6,
    min_scale=1e-6,
    verbose=False,
) -> FittedMixtureDistribution:
    """
    Fit a k-component mixture, with a (possibly different) kernel per
    component, to (optionally masked) values in `data`.

    Works identically whether `data` is in memory or a chunked,
    out-of-core store, and whether `sample_size` is set -- see the module
    docstring of the earlier Gaussian-specific version for how `data` /
    `chunk_size` are resolved; that mechanism is unchanged here.

    Parameters
    ----------
    kernels : list[Kernel], length k
        One kernel instance per component -- e.g.
        `[CauchyKernel(), GaussianKernel(), GaussianKernel()]` for one
        heavy-tailed component and two light-tailed ones. All kernels
        must agree on `periodic` (can't mix linear and circular kernels).
    params_init : list[tuple[float, float]], length k
        Initial (loc, scale-like) guess per component, matching each
        kernel's `param_names` (e.g. (mean, std) for Gaussian,
        (loc, scale) for Cauchy, (mean, kappa) for von Mises).
    weights_init : array-like, shape (k,), optional
        Initial mixture weights (default: uniform).
    min_scale : float
        Regularization floor preventing a component from collapsing onto
        a single point (interpreted per-kernel: a scale/std floor for
        linear kernels, an equivalent concentration cap for periodic
        ones).
    (all other parameters as in the Gaussian-only `fit_gaussian_mixture`)

    Returns
    -------
    FittedMixtureDistribution
    """
    kernels = [k.copy() if hasattr(k, "cdf") else DistributionKernel.resolve(k['name'], *k['params']) for k in kernels]
    k = len(kernels)
    periodic_flags = {kernel.periodic for kernel in kernels}
    if len(periodic_flags) > 1:
        raise ValueError(
            "Cannot mix periodic and non-periodic kernels in one model "
            f"(got periodic flags: {[k.periodic for k in kernels]})."
        )

    params = [tuple(float(v) for v in k.params) for k in kernels]
    weights = (
        np.full(k, 1.0 / k)
        if weights_init is None
        else np.asarray(weights_init, dtype=np.float64).copy()
    )

    if sample_size is not None:
        x = sample_masked_values(
            data, sample_size, mask_fn=mask_fn, vals_key=vals_key,
            chunk_size=chunk_size, seed=seed,
        )
        if x.size == 0:
            raise ValueError("No values passed the mask; nothing to fit.")

        params, weights, ll, n_iter, n_used = _fit_em_over_slices(
            data=x, vals=x, mask_fn=_no_mask, n=x.shape[0], chunk_size=None,
            kernels=kernels, params=params, weights=weights,
            max_iter=max_iter, tol=tol, min_scale=min_scale, verbose=verbose,
        )
        method = "sampled"
        fit_kwargs = dict(data=data, mask_fn=mask_fn, vals_key=vals_key, chunk_size=chunk_size)
        sample_for_storage = x
    else:
        vals = _resolve_vals(data, vals_key)
        n = vals.shape[0]
        resolved_chunk_size = _resolve_chunk_size(vals, chunk_size)
        mfn = mask_fn if mask_fn is not None else _no_mask

        params, weights, ll, n_iter, n_used = _fit_em_over_slices(
            data=data, vals=vals, mask_fn=mfn, n=n, chunk_size=resolved_chunk_size,
            kernels=kernels, params=params, weights=weights,
            max_iter=max_iter, tol=tol, min_scale=min_scale, verbose=verbose,
        )
        method = "in-core" if resolved_chunk_size is None else "out-of-core"
        fit_kwargs = dict(data=data, mask_fn=mask_fn, vals_key=vals_key, chunk_size=chunk_size)
        sample_for_storage = None

    for k,p in zip(kernels, params):
        k.params = p

    return FittedMixtureDistribution(
        kernels=kernels, weights=weights,
        log_likelihood=ll, n_iter=n_iter, n_samples=n_used, method=method,
        _fit_kwargs=fit_kwargs, _sample=sample_for_storage,
    )


def sample_masked_values(data, sample_size, mask_fn=None, vals_key="vals", chunk_size=None, seed=None):
    """
    Draw an exact, unbiased simple random sample (without replacement) of
    up to `sample_size` values from the masked entries of `data`, in a
    single pass, via one-pass priority (reservoir) sampling. See the
    Gaussian-only version's docstring for the full unbiasedness argument
    -- unchanged here.
    """
    mfn = mask_fn if mask_fn is not None else _no_mask
    vals = _resolve_vals(data, vals_key)
    n = vals.shape[0]
    resolved_chunk_size = _resolve_chunk_size(vals, chunk_size)
    rng = np.random.default_rng(seed)

    best_keys = np.full(sample_size, np.inf)
    best_vals = np.full(sample_size, np.nan)
    filled = 0

    for sl in _iter_slices(n, resolved_chunk_size):
        m = np.asarray(mfn(data, sl), dtype=bool)
        if not m.any():
            continue

        x = np.asarray(vals[sl])[m].astype(np.float64, copy=False)
        keys = rng.random(x.shape[0])

        cand_keys = np.concatenate([best_keys[:filled], keys])
        cand_vals = np.concatenate([best_vals[:filled], x])

        if cand_keys.shape[0] <= sample_size:
            best_keys[: cand_keys.shape[0]] = cand_keys
            best_vals[: cand_vals.shape[0]] = cand_vals
            filled = cand_keys.shape[0]
        else:
            idx = np.argpartition(cand_keys, sample_size)[:sample_size]
            best_keys[:] = cand_keys[idx]
            best_vals[:] = cand_vals[idx]
            filled = sample_size

    return best_vals[:filled]


# ---------------------------------------------------------------------------
# Internals (kernel-agnostic)
# ---------------------------------------------------------------------------
def _resolve_vals(data, vals_key):
    if hasattr(data, "shape"):
        return data
    return data[vals_key]


def _resolve_chunk_size(vals, chunk_size):
    if chunk_size is not None:
        return chunk_size
    chunks = getattr(vals, "chunks", None)
    if chunks is not None:
        return chunks[0]
    return None


def _iter_slices(n, chunk_size):
    if chunk_size is None:
        yield slice(0, n)
        return
    for start in range(0, n, chunk_size):
        yield slice(start, min(start + chunk_size, n))


def _no_mask(data, sl):
    return np.ones(sl.stop - sl.start, dtype=bool)


def _e_step(x, kernels, params, weights):
    """Log responsibilities and total log-likelihood, combining each
    component's own kernel.log_pdf via log-sum-exp -- fully kernel-agnostic."""
    k = len(kernels)
    log_prob = np.empty((x.shape[0], k))
    for j in range(k):
        log_prob[:, j] = np.log(weights[j] + 1e-300) + kernels[j].log_pdf(x, params[j])
    max_lp = log_prob.max(axis=1, keepdims=True)
    log_norm = max_lp[:, 0] + np.log(np.exp(log_prob - max_lp).sum(axis=1))
    log_resp = log_prob - log_norm[:, None]
    return log_resp, log_norm.sum()


def _fit_em_over_slices(
    data, vals, mask_fn, n, chunk_size, kernels, params, weights,
    max_iter, tol, min_scale, verbose,
):
    """
    Shared, kernel-agnostic EM loop. Each iteration walks
    `_iter_slices(n, chunk_size)`, computes responsibilities via `_e_step`,
    and asks each component's kernel to accumulate + finalize its own
    sufficient statistics. Identical structure to the Gaussian-only
    version; only the per-component math has been delegated to `kernels`.
    """
    k = len(kernels)
    prev_ll = -np.inf
    n_iter_done = 0
    total_ll = 0.0
    total_count = 0

    for iteration in range(max_iter):
        Nk = np.zeros(k)
        stats = [kernels[j].new_stats() for j in range(k)]
        total_ll = 0.0
        total_count = 0

        for sl in _iter_slices(n, chunk_size):
            m = np.asarray(mask_fn(data, sl), dtype=bool)
            if not m.any():
                continue

            x = np.asarray(vals[sl])[m].astype(np.float64, copy=False)

            log_resp, chunk_ll = _e_step(x, kernels, params, weights)
            resp = np.exp(log_resp)

            for j in range(k):
                Nk[j] += resp[:, j].sum()
                kernels[j].accumulate(stats[j], x, resp[:, j], params[j])

            total_ll += chunk_ll
            total_count += x.size

        if total_count == 0:
            raise ValueError("No values passed the mask; nothing to fit.")

        weights = Nk / total_count
        params = [kernels[j].finalize(stats[j], min_scale) for j in range(k)]

        n_iter_done = iteration + 1
        if verbose:
            print(f"iter {n_iter_done:3d}  ll={total_ll:.6f}  weights={np.round(weights, 4)}")
            for j in range(k):
                print(f"    [{j}] {kernels[j].__class__.__name__}: {np.round(params[j], 4)}")

        if np.isfinite(prev_ll) and abs(total_ll - prev_ll) < tol * abs(prev_ll):
            break
        prev_ll = total_ll

    return params, weights, total_ll, n_iter_done, total_count

