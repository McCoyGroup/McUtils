"""Harness configuration read from TOML (``tomllib``): models, tiers, budget, policy and limits."""

from .Budget import Budget
from .ModelClient import ModelClient

__all__ = ["HarnessConfig"]


class HarnessConfig:
    """
    .. code-block:: toml

        policy = "grounded"
        [models.local]
        provider = "ollama"
        model = "gemma4:12b"
        cost_per_1k_in = 0.0
        [tiers]
        small = "local"
        [budget]
        max_calls = 100
        [limits]
        max_blocks = 12
    """

    def __init__(self, models=None, tiers=None, budget=None, policy="grounded", limits=None):
        self.models = dict(models or {})
        self.tiers = dict(tiers or {})
        self.budget = dict(budget or {})
        self.policy = policy
        self.limits = dict(limits or {})
        for tier, model in self.tiers.items():
            if model not in self.models:
                raise ValueError(f"tier {tier!r} uses model {model!r}, which isn't in models {sorted(self.models)}")

    @classmethod
    def from_dict(cls, d):
        return cls(d.get("models"), d.get("tiers"), d.get("budget"), d.get("policy", "grounded"), d.get("limits"))

    @classmethod
    def from_toml(cls, path):
        import tomllib
        with open(path, "rb") as f:
            return cls.from_dict(tomllib.load(f))

    def make_budget(self):
        prices = {m: (s.get("cost_per_1k_in", 0.0), s.get("cost_per_1k_out", 0.0)) for m, s in self.models.items()}
        return Budget(prices=prices, **self.budget)

    def clients(self):
        """``{tier: ModelClient}``; providers other than registered ones are an error (live providers come later)."""
        cache = {}
        out = {}
        for tier, model in self.tiers.items():
            if model not in cache:
                cache[model] = ModelClient.from_spec(model, self.models[model])
            out[tier] = cache[model]
        return out
