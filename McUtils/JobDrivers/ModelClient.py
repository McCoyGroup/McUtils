"""
Model clients: one ``complete`` call that returns text, an optional parsed JSON value and the token/time cost.

Only the offline `ScriptedClient` lives here for now (tests and replay); live providers register themselves with
`ModelClient.register_provider`.
"""

import time

from .Answers import parse_json_answer

__all__ = ["ModelResponse", "ModelClient", "ScriptedClient", "ModelClientError"]


class ModelClientError(RuntimeError):
    """A client could not produce an answer (not a bad answer: a failed call)."""


class ModelResponse:
    """
    :ivar text: the raw reply
    :ivar value: the parsed JSON object, or ``None`` if there wasn't one
    :ivar tokens_in: prompt tokens
    :ivar tokens_out: reply tokens
    :ivar wall_s: wall-clock seconds
    :ivar model: the model name
    :ivar raw: provider-specific extras
    """

    def __init__(self, text, value=None, tokens_in=0, tokens_out=0, wall_s=0.0, model=None, raw=None):
        self.text, self.value = text, value
        self.tokens_in, self.tokens_out, self.wall_s = tokens_in, tokens_out, wall_s
        self.model, self.raw = model, dict(raw or {})

    def __repr__(self):
        return f"ModelResponse(model={self.model!r}, tokens={self.tokens_in}/{self.tokens_out}, text={self.text[:40]!r})"


class ModelClient:
    """Base class. Subclasses implement `complete`."""
    name = "model"
    _providers = {}

    @classmethod
    def register_provider(cls, provider, factory):
        """Register ``factory(name, spec_dict) -> ModelClient`` for a config ``provider`` name."""
        cls._providers[provider] = factory

    @classmethod
    def from_spec(cls, name, spec):
        provider = spec.get("provider")
        if provider not in cls._providers:
            raise ValueError(f"model {name!r}: unknown provider {provider!r}; registered: {sorted(cls._providers)}")
        return cls._providers[provider](name, spec)

    def complete(self, messages, schema=None, max_tokens=512, temperature=0.0):
        """
        :param messages: ``[{"role": "system"|"user"|"assistant", "content": str}, ...]``
        :param schema: an optional answer schema (clients that support constrained decoding use it)
        :rtype: ModelResponse
        """
        raise NotImplementedError


def _text_tokens(text):
    return len(text) // 4


class ScriptedClient(ModelClient):
    """
    A client that replays prepared answers.

    :param answers: a list consumed in order (each item a dict/list that is sent as JSON, a string sent as is,
        or an ``Exception`` instance that is raised), or a callable ``(messages, schema) -> obj | str``
    :param name: the model name

    Tokens are counted as ``len(text) // 4`` (prompt: all message contents). ``calls`` records ``(messages, schema)``.
    """

    def __init__(self, answers, name="scripted"):
        self.name = name
        self.answers = answers
        self.calls = []
        self._i = 0

    def complete(self, messages, schema=None, max_tokens=512, temperature=0.0):
        import json
        start = time.time()
        self.calls.append(([dict(m) for m in messages], schema))
        if callable(self.answers):
            item = self.answers(messages, schema)
        else:
            if self._i >= len(self.answers):
                raise ModelClientError(f"{self.name}: the script has no answer for call {self._i + 1}")
            item = self.answers[self._i]
            self._i += 1
        if isinstance(item, Exception):
            raise item
        text = item if isinstance(item, str) else json.dumps(item)
        value, _ = parse_json_answer(text)
        tin = sum(_text_tokens(m["content"]) for m in messages)
        return ModelResponse(text, value, tin, _text_tokens(text), time.time() - start, self.name)
