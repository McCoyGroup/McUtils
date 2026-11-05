"""The decision ledger (JSONL, append-only) and the decision cache."""

import json
import os
import hashlib

__all__ = ["DecisionRecord", "Ledger", "DecisionCache", "cache_key"]


def cache_key(name, prompt_version, policy, model, evidence_hash):
    return hashlib.md5("|".join(str(x) for x in (name, prompt_version, policy, model, evidence_hash)).encode()
                       ).hexdigest()


class DecisionRecord:
    """
    One line of the ledger: what was decided, from which evidence, by which model, and what it cost.

    ``outcome`` is ``applied`` | ``escalated`` | ``defaulted`` (| ``overturned``, set later by a reviewer);
    ``source`` is ``model`` | ``cache`` | ``default``; ``reason`` says why a default was used.
    ``evidence_text`` is kept so a decision can be replayed against another model.
    """
    FIELDS = ("decision", "job_identity", "evidence_hash", "model", "prompt_version", "answer", "rationale",
              "confidence", "post_check", "escalated_to", "cost", "outcome", "policy", "stage", "attempts",
              "evidence_text", "source", "reason", "cache_key")

    def __init__(self, decision, **kw):
        self.decision = decision
        for f in self.FIELDS[1:]:
            setattr(self, f, kw.pop(f, None))
        if kw:
            raise TypeError(f"unknown DecisionRecord fields: {sorted(kw)}")
        self.attempts = self.attempts or []
        self.cost = self.cost or {}

    def to_dict(self):
        return {f: getattr(self, f) for f in self.FIELDS}

    @classmethod
    def from_dict(cls, d):
        return cls(**{k: v for k, v in d.items() if k in cls.FIELDS})

    def __repr__(self):
        return f"DecisionRecord({self.decision!r}, outcome={self.outcome!r}, source={self.source!r})"


class Ledger:
    """Appends `DecisionRecord`s as JSON lines to ``path``, or keeps them in memory when ``path`` is ``None``."""

    def __init__(self, path=None):
        self.path = None if path is None else os.fspath(path)
        self.records = []
        if self.path is not None and os.path.exists(self.path):
            self.records = self.read(self.path)

    @staticmethod
    def read(path):
        with open(path, encoding="utf-8") as f:
            return [DecisionRecord.from_dict(json.loads(line)) for line in f if line.strip()]

    def append(self, record):
        self.records.append(record)
        if self.path is not None:
            os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record.to_dict(), default=str) + "\n")

    def __len__(self):
        return len(self.records)

    def __iter__(self):
        return iter(self.records)


class DecisionCache:
    """Answers keyed by ``cache_key``; when given a ledger, it starts from that ledger's applied answers."""

    def __init__(self, ledger=None):
        self._d = {}
        if ledger is not None:
            for r in ledger.records:
                if r.cache_key and r.source == "model" and r.outcome in ("applied", "escalated"):
                    self._d[r.cache_key] = r.answer

    def get(self, key):
        return self._d.get(key)

    def has(self, key):
        return key in self._d

    def put(self, key, answer):
        self._d[key] = answer

    def __len__(self):
        return len(self._d)
