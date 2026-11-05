"""Cost bookkeeping for model calls: a price table, and caps on total cost, total calls and calls per decision."""

__all__ = ["PriceTable", "Budget", "BudgetExceeded"]


class BudgetExceeded(RuntimeError):
    """A cap was reached; the decision falls back to its default."""


class PriceTable:
    """Per-model cost per 1000 tokens in and out (cost units; 0 for models that aren't listed)."""

    def __init__(self, prices=None):
        self.prices = dict(prices or {})   # model -> (cost_per_1k_in, cost_per_1k_out)

    def set(self, model, cost_per_1k_in=0.0, cost_per_1k_out=0.0):
        self.prices[model] = (cost_per_1k_in, cost_per_1k_out)

    def cost(self, model, tokens_in, tokens_out):
        pin, pout = self.prices.get(model, (0.0, 0.0))
        return pin * tokens_in / 1000 + pout * tokens_out / 1000


class Budget:
    """
    Caps on a run. ``check`` is called before every model call and raises `BudgetExceeded` when the total cost
    or call count has already reached its cap, or when the current decision has used its ``max_calls_per_decision``.
    ``begin(decision)`` starts a new decision's per-decision count.
    """

    def __init__(self, max_cost_units=None, max_calls=None, max_calls_per_decision=4, prices=None):
        self.max_cost_units, self.max_calls = max_cost_units, max_calls
        self.max_calls_per_decision = max_calls_per_decision
        self.prices = prices if isinstance(prices, PriceTable) else PriceTable(prices)
        self.calls = self.tokens_in = self.tokens_out = 0
        self.cost_units = 0.0
        self.wall_s = 0.0
        self._decision_calls = 0

    def begin(self, decision_name=None):
        self._decision_calls = 0

    def check(self, decision_name=None):
        if self.max_calls is not None and self.calls >= self.max_calls:
            raise BudgetExceeded(f"call cap reached ({self.calls} of {self.max_calls})")
        if self.max_cost_units is not None and self.cost_units >= self.max_cost_units:
            raise BudgetExceeded(f"cost cap reached ({self.cost_units:.4g} of {self.max_cost_units})")
        if self.max_calls_per_decision is not None and self._decision_calls >= self.max_calls_per_decision:
            raise BudgetExceeded(f"decision {decision_name!r} used its {self.max_calls_per_decision} calls")

    def charge(self, model, tokens_in, tokens_out, wall_s=0.0):
        self.calls += 1
        self._decision_calls += 1
        self.tokens_in += tokens_in
        self.tokens_out += tokens_out
        self.wall_s += wall_s
        cost = self.prices.cost(model, tokens_in, tokens_out)
        self.cost_units += cost
        return cost

    @property
    def totals(self):
        return {"calls": self.calls, "tokens_in": self.tokens_in, "tokens_out": self.tokens_out,
                "wall_s": round(self.wall_s, 4), "cost_units": self.cost_units}
