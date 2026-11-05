"""
Decision points and the runner that asks a model to settle each one.

A `DecisionPoint` is one bounded question: it builds a small, capped body of *evidence*, defines a closed *answer
schema*, and has a *default* to fall back on. `DecisionRunner.decide` asks the model (propose), validates the answer
against the schema and the point's own post-check (verify), asks again once with the errors listed if it failed
(revise), moves to a larger tier if one is configured (escalate), and otherwise uses the default. Every call to
``decide`` appends exactly one `DecisionRecord` to the ledger.
"""

import hashlib
import json

from .Answers import validate_answer, check_schema, parse_json_answer, describe_schema
from .Budget import Budget, BudgetExceeded
from .Ledger import Ledger, DecisionCache, DecisionRecord, cache_key

__all__ = ["Evidence", "CheckResult", "DecisionPoint", "DecisionOutcome", "DecisionRunner", "EvidenceTooLarge"]

PREAMBLE = ("Answer with one JSON object only, matching the schema. "
            "Use only information in the evidence.")


class EvidenceTooLarge(ValueError):
    """An evidence builder produced more than the decision point's token cap (a bug in the builder)."""


class Evidence:
    """The text a model is shown for one decision. ``tokens`` is ``len(text) // 4``."""

    def __init__(self, text):
        self.text = text
        self.hash = hashlib.md5(text.encode("utf-8")).hexdigest()
        self.tokens = len(text) // 4

    def __repr__(self):
        return f"Evidence({self.tokens} tokens, {self.hash[:8]})"


class CheckResult:
    def __init__(self, ok=True, errors=()):
        self.errors = list(errors)
        self.ok = bool(ok) and not self.errors

    def to_dict(self):
        return {"ok": self.ok, "errors": list(self.errors)}

    def __repr__(self):
        return f"CheckResult(ok={self.ok}, errors={self.errors})"


class DecisionPoint:
    """
    :param name: the decision's name (``'select_content'``)
    :param question: one to three sentences, versioned with ``prompt_version``
    :param evidence: ``state -> Evidence``
    :param answer_schema: a schema dict, or ``state -> dict`` for schemas built from the current state
    :param default: the answer to use when no model answer is accepted, or ``state -> answer``
    :param post_check: ``(state, answer) -> CheckResult`` for checks the schema can't express
    :param max_revisions: extra attempts per tier after a rejected answer (each shows the errors)
    :param tier: the client tier tried first
    :param escalate_to: tiers tried after it; empty means "use the default"
    """

    def __init__(self, name, question, evidence, answer_schema, default=None, prompt_version="v1", post_check=None,
                 max_revisions=1, tier="small", escalate_to=(), max_evidence_tokens=1500, max_tokens=512):
        self.name, self.question, self.evidence = name, question, evidence
        self.answer_schema, self.default = answer_schema, default
        self.prompt_version, self.post_check = prompt_version, post_check
        self.max_revisions, self.tier, self.escalate_to = max_revisions, tier, tuple(escalate_to)
        self.max_evidence_tokens, self.max_tokens = max_evidence_tokens, max_tokens


class DecisionOutcome:
    """``answer``; ``source`` is ``model`` | ``cache`` | ``default``; ``record`` is what was written to the ledger."""

    def __init__(self, answer, source, record):
        self.answer, self.source, self.record = answer, source, record

    @property
    def defaulted(self):
        return self.source == "default"

    def __repr__(self):
        return f"DecisionOutcome({self.record.decision!r}, source={self.source!r})"


class DecisionRunner:
    """
    :param clients: ``{tier: ModelClient}``
    :param budget: a `Budget` (default: no caps)
    :param ledger: a `Ledger` (default: in memory)
    :param cache: a `DecisionCache` (default: one seeded from the ledger)
    :param policy: recorded on every record and part of the cache key
    """

    def __init__(self, clients, budget=None, ledger=None, cache=None, policy="grounded"):
        self.clients = dict(clients)
        self.budget = Budget() if budget is None else budget
        self.ledger = Ledger() if ledger is None else ledger
        self.cache = DecisionCache(self.ledger) if cache is None else cache
        self.policy = policy

    # ------------------------------------------------------------------------------------------ #
    @staticmethod
    def _resolve(value, state):
        return value(state) if callable(value) else value

    def _messages(self, point, schema, evidence):
        system = f"{PREAMBLE}\n\n{point.question}\n\nSchema: {describe_schema(schema)}"
        return [{"role": "system", "content": system}, {"role": "user", "content": evidence.text}]

    def _check(self, point, state, schema, answer):
        errors = validate_answer(schema, answer)
        if errors:
            return CheckResult(False, errors)
        if point.post_check is not None:
            res = point.post_check(state, answer)
            return res if isinstance(res, CheckResult) else CheckResult(bool(res))
        return CheckResult(True)

    def decide(self, point, state, stage=None, policy=None):
        policy = self.policy if policy is None else policy
        evidence = point.evidence(state)
        if not isinstance(evidence, Evidence):
            evidence = Evidence(str(evidence))
        if evidence.tokens > point.max_evidence_tokens:
            raise EvidenceTooLarge(f"decision {point.name!r}: evidence is {evidence.tokens} tokens; "
                                   f"the cap is {point.max_evidence_tokens}")
        schema = self._resolve(point.answer_schema, state)
        check_schema(schema)
        default = self._resolve(point.default, state)
        tiers = (point.tier,) + point.escalate_to
        first = self.clients.get(point.tier)
        model_name = getattr(first, "name", point.tier)
        key = cache_key(point.name, point.prompt_version, policy, model_name, evidence.hash)

        rec = DecisionRecord(point.name, evidence_hash=evidence.hash, model=model_name, answer=None,
                             prompt_version=point.prompt_version, policy=policy, stage=stage or point.name,
                             evidence_text=evidence.text, cache_key=key)

        # a cached answer is only used if it still passes today's checks
        if self.cache.has(key):
            cached = self.cache.get(key)
            res = self._check(point, state, schema, cached)
            if res.ok:
                rec.answer, rec.source, rec.outcome = cached, "cache", "applied"
                rec.post_check = res.to_dict()
                self.ledger.append(rec)
                return DecisionOutcome(cached, "cache", rec)

        messages = self._messages(point, schema, evidence)
        self.budget.begin(point.name)
        attempts, answer, last_check, default_reason = [], None, None, None
        spent = {"calls": 0, "tokens_in": 0, "tokens_out": 0, "wall_s": 0.0, "cost_units": 0.0}
        accepted_tier = None
        try:
            for tier_index, tier in enumerate(tiers):
                client = self.clients.get(tier)
                if client is None:
                    continue
                convo = list(messages)
                for _ in range(1 + point.max_revisions):
                    self.budget.check(point.name)
                    entry = {"tier": tier, "model": getattr(client, "name", tier), "tokens_in": 0, "tokens_out": 0,
                             "wall_s": 0.0, "errors": []}
                    attempts.append(entry)
                    try:
                        resp = client.complete(convo, schema=schema, max_tokens=point.max_tokens)
                    except BudgetExceeded:
                        raise
                    except Exception as e:     # a failed call, not a bad answer
                        entry["errors"] = [f"call failed: {type(e).__name__}: {e}"]
                        break
                    cost = self.budget.charge(entry["model"], resp.tokens_in, resp.tokens_out, resp.wall_s)
                    entry.update(tokens_in=resp.tokens_in, tokens_out=resp.tokens_out, wall_s=resp.wall_s)
                    spent["calls"] += 1
                    spent["tokens_in"] += resp.tokens_in
                    spent["tokens_out"] += resp.tokens_out
                    spent["wall_s"] += resp.wall_s
                    spent["cost_units"] += cost
                    value, perr = parse_json_answer(resp.text)
                    if perr is None:
                        last_check = self._check(point, state, schema, value)
                    else:
                        last_check = CheckResult(False, [perr])
                    entry["errors"] = list(last_check.errors)
                    if last_check.ok:
                        answer, accepted_tier = value, (tier, tier_index)
                        break
                    convo = convo + [{"role": "assistant", "content": resp.text},
                                     {"role": "user", "content": "That answer was rejected:\n- "
                                      + "\n- ".join(last_check.errors)
                                      + "\nReply with one corrected JSON object."}]
                if accepted_tier is not None:
                    break
        except BudgetExceeded as e:
            default_reason = f"budget: {e}"

        rec.attempts, rec.cost = attempts, spent
        rec.post_check = None if last_check is None else last_check.to_dict()
        if accepted_tier is not None:
            tier, tier_index = accepted_tier
            rec.answer, rec.source = answer, "model"
            rec.model = attempts[-1]["model"]
            rec.outcome = "escalated" if tier_index > 0 else "applied"
            rec.escalated_to = tier if tier_index > 0 else None
            self.cache.put(key, answer)
        else:
            rec.answer, rec.source, rec.outcome = default, "default", "defaulted"
            if default_reason is None:
                if not attempts:
                    default_reason = f"no client for tiers {list(tiers)}"
                else:
                    errs = last_check.errors if last_check is not None else attempts[-1]["errors"]
                    default_reason = "no accepted answer: " + "; ".join(errs)[:300]
            rec.reason = default_reason
        self.ledger.append(rec)
        return DecisionOutcome(rec.answer, rec.source, rec)
