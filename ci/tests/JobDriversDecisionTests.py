import json
import os
import tempfile
import unittest

from McUtils.JobDrivers import (validate_answer, check_schema, parse_json_answer, ScriptedClient, ModelClient,
                                Budget, BudgetExceeded, PriceTable, Ledger, DecisionCache, DecisionRecord,
                                DecisionPoint, DecisionRunner, Evidence, CheckResult, EvidenceTooLarge,
                                ToolSet, HarnessConfig)
from McUtils.JobDrivers.ModelClient import ModelClientError


class ValidateAnswerTests(unittest.TestCase):
    def test_types(self):
        self.assertEqual(validate_answer({"type": "string"}, "a"), [])
        self.assertTrue(validate_answer({"type": "string"}, 3))
        self.assertEqual(validate_answer({"type": ["string", "null"]}, None), [])
        self.assertEqual(validate_answer({"type": "integer"}, 3), [])
        self.assertEqual(validate_answer({"type": "integer"}, 3.0), [])
        self.assertTrue(validate_answer({"type": "integer"}, 3.5))
        self.assertTrue(validate_answer({"type": "integer"}, True), "a bool is not an integer")
        self.assertEqual(validate_answer({"type": "number"}, 3.5), [])
        self.assertEqual(validate_answer({"type": "boolean"}, False), [])
        self.assertTrue(validate_answer({"type": "array"}, {}))

    def test_enum_const(self):
        self.assertEqual(validate_answer({"enum": ["a", "b"]}, "a"), [])
        errs = validate_answer({"enum": ["a", "b"]}, "c")
        self.assertIn("$", errs[0])
        self.assertIn("'a'", errs[0])
        self.assertTrue(validate_answer({"enum": [1]}, True), "True is not 1")
        self.assertEqual(validate_answer({"const": 3}, 3), [])
        self.assertTrue(validate_answer({"const": 3}, 4))

    def test_object(self):
        schema = {"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "string"}},
                  "required": ["a"], "additionalProperties": False}
        self.assertEqual(validate_answer(schema, {"a": 1}), [])
        self.assertIn("missing required property 'a'", validate_answer(schema, {"b": "x"})[0])
        self.assertIn("unexpected property 'c'", validate_answer(schema, {"a": 1, "c": 2})[0])
        errs = validate_answer(schema, {"a": "no"})
        self.assertTrue(errs[0].startswith("$.a:"))
        self.assertEqual(validate_answer({"type": "object", "properties": {}}, {"extra": 1}), [])

    def test_array(self):
        schema = {"type": "array", "items": {"type": "integer"}, "minItems": 1, "maxItems": 3, "uniqueItems": True}
        self.assertEqual(validate_answer(schema, [1, 2]), [])
        self.assertTrue(validate_answer(schema, []))
        self.assertTrue(validate_answer(schema, [1, 2, 3, 4]))
        self.assertIn("duplicate", validate_answer(schema, [1, 1])[0])
        self.assertTrue(validate_answer(schema, [1, "x"])[0].startswith("$[1]:"))

    def test_string_and_number_bounds(self):
        self.assertTrue(validate_answer({"type": "string", "maxLength": 3}, "abcd"))
        self.assertTrue(validate_answer({"type": "string", "minLength": 2}, "a"))
        self.assertTrue(validate_answer({"type": "number", "minimum": 0}, -1))
        self.assertTrue(validate_answer({"type": "number", "maximum": 10}, 11))
        self.assertEqual(validate_answer({"type": "number", "minimum": 0, "maximum": 10}, 5), [])

    def test_nested_paths(self):
        schema = {"type": "object", "properties": {"items": {"type": "array", "items": {
            "type": "object", "properties": {"n": {"type": "integer"}}}}}}
        errs = validate_answer(schema, {"items": [{"n": 1}, {"n": "x"}]})
        self.assertTrue(errs[0].startswith("$.items[1].n:"))

    def test_unsupported_keywords_fail_loudly(self):
        for bad in ({"pattern": "a"}, {"oneOf": []}, {"type": "object", "properties": {"a": {"format": "date"}}},
                    {"type": "array", "items": {"anyOf": []}}, {"type": "bogus"}, {"additionalProperties": {}}):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    validate_answer(bad, 1)
                with self.assertRaises(ValueError):
                    check_schema(bad)

    def test_annotations_are_ignored(self):
        self.assertEqual(validate_answer({"type": "string", "description": "d", "title": "t", "default": "x"}, "a"), [])


class ParseJSONTests(unittest.TestCase):
    def test_plain_fenced_and_prose(self):
        self.assertEqual(parse_json_answer('{"a": 1}'), ({"a": 1}, None))
        self.assertEqual(parse_json_answer('```json\n{"a": 1}\n```')[0], {"a": 1})
        self.assertEqual(parse_json_answer('Sure! Here is the answer: {"a": {"b": 2}} Hope that helps.')[0],
                         {"a": {"b": 2}})

    def test_first_object_wins(self):
        self.assertEqual(parse_json_answer('{"a": 1} {"a": 2}')[0], {"a": 1})

    def test_garbage(self):
        value, err = parse_json_answer("no json here")
        self.assertIsNone(value)
        self.assertIn("no JSON object", err)
        self.assertIsNone(parse_json_answer("{broken")[0])
        self.assertIsNotNone(parse_json_answer(None)[1])


def make_point(name="pick", post_check=None, default="fallback", escalate_to=(), max_revisions=1, cap=1500,
               text="the evidence"):
    return DecisionPoint(
        name, "Pick one.", lambda state: Evidence(text if not callable(text) else text(state)),
        {"type": "object", "properties": {"choice": {"enum": ["a", "b"]}}, "required": ["choice"]},
        default=default, prompt_version="t1", post_check=post_check, max_revisions=max_revisions,
        escalate_to=escalate_to, max_evidence_tokens=cap)


class ScriptedClientTests(unittest.TestCase):
    def test_list_and_callable(self):
        c = ScriptedClient([{"x": 1}, "text only"])
        r = c.complete([{"role": "user", "content": "abcdefgh"}])
        self.assertEqual(r.value, {"x": 1})
        self.assertEqual(r.tokens_in, 2)
        self.assertEqual(c.complete([{"role": "user", "content": "q"}]).value, None)
        with self.assertRaises(ModelClientError):
            c.complete([{"role": "user", "content": "q"}])
        self.assertEqual(len(c.calls), 3)
        c2 = ScriptedClient(lambda messages, schema: {"n": len(messages)})
        self.assertEqual(c2.complete([{"role": "user", "content": "q"}]).value, {"n": 1})
        c3 = ScriptedClient([RuntimeError("boom")])
        with self.assertRaises(RuntimeError):
            c3.complete([])


class DecisionRunnerTests(unittest.TestCase):
    def runner(self, small, large=None, **kw):
        clients = {"small": small}
        if large is not None:
            clients["large"] = large
        return DecisionRunner(clients, **kw)

    def test_valid_first_answer(self):
        small = ScriptedClient([{"choice": "a"}])
        r = self.runner(small)
        out = r.decide(make_point(), None)
        self.assertEqual(out.answer, {"choice": "a"})
        self.assertEqual((out.source, out.record.outcome), ("model", "applied"))
        self.assertEqual(len(small.calls), 1)
        msgs = small.calls[0][0]
        self.assertEqual([m["role"] for m in msgs], ["system", "user"])
        self.assertIn("Answer with one JSON object only", msgs[0]["content"])
        self.assertIn("Pick one.", msgs[0]["content"])
        self.assertIn('"choice"', msgs[0]["content"])
        self.assertEqual(msgs[1]["content"], "the evidence")
        self.assertEqual(len(r.ledger), 1)

    def test_invalid_json_then_valid_shows_the_error(self):
        small = ScriptedClient(["I think it is a", {"choice": "b"}])
        out = self.runner(small).decide(make_point(), None)
        self.assertEqual(out.answer, {"choice": "b"})
        self.assertEqual(len(small.calls), 2)
        second = small.calls[1][0]
        self.assertEqual([m["role"] for m in second], ["system", "user", "assistant", "user"])
        self.assertIn("no JSON object found", second[-1]["content"])
        self.assertEqual(len(out.record.attempts), 2)
        self.assertTrue(out.record.attempts[0]["errors"])
        self.assertEqual(out.record.attempts[1]["errors"], [])

    def test_schema_error_is_listed_verbatim(self):
        small = ScriptedClient([{"choice": "z"}, {"choice": "a"}])
        self.runner(small).decide(make_point(), None)
        self.assertIn("$.choice: 'z' is not one of", small.calls[1][0][-1]["content"])

    def test_post_check_failure_twice_then_escalates(self):
        def check(state, ans):
            return CheckResult(ans["choice"] == "b", [] if ans["choice"] == "b" else ["must be b"])
        small = ScriptedClient([{"choice": "a"}, {"choice": "a"}])
        large = ScriptedClient([{"choice": "b"}], name="big")
        r = self.runner(small, large)
        out = r.decide(make_point(post_check=check, escalate_to=("large",)), None)
        self.assertEqual(out.answer, {"choice": "b"})
        self.assertEqual(out.record.outcome, "escalated")
        self.assertEqual(out.record.escalated_to, "large")
        self.assertEqual((len(small.calls), len(large.calls)), (2, 1))
        self.assertEqual(out.record.model, "big")
        self.assertEqual(len(out.record.attempts), 3)

    def test_all_failures_default(self):
        small = ScriptedClient([{"choice": "z"}, "junk"])
        out = self.runner(small).decide(make_point(), None)
        self.assertEqual(out.answer, "fallback")
        self.assertEqual((out.source, out.record.outcome), ("default", "defaulted"))
        self.assertIn("no accepted answer", out.record.reason)

    def test_failed_call_is_recorded_and_defaults(self):
        small = ScriptedClient([RuntimeError("server down")])
        out = self.runner(small).decide(make_point(), None)
        self.assertEqual(out.record.outcome, "defaulted")
        self.assertIn("call failed: RuntimeError: server down", out.record.attempts[0]["errors"][0])

    def test_missing_tier_is_skipped_and_no_clients_default(self):
        small = ScriptedClient([{"choice": "z"}, {"choice": "z"}])
        out = self.runner(small).decide(make_point(escalate_to=("large",)), None)   # no 'large' client
        self.assertEqual(out.record.outcome, "defaulted")
        out = DecisionRunner({}).decide(make_point(), None)
        self.assertEqual(out.record.outcome, "defaulted")
        self.assertIn("no client", out.record.reason)

    def test_budget_exceeded_defaults(self):
        small = ScriptedClient([{"choice": "a"}] * 5)
        r = self.runner(small, budget=Budget(max_calls=1))
        self.assertEqual(r.decide(make_point(text="one"), None).source, "model")
        out = r.decide(make_point(text="two"), None)
        self.assertEqual(out.record.outcome, "defaulted")
        self.assertIn("budget", out.record.reason)
        self.assertEqual(len(small.calls), 1)

    def test_calls_per_decision_cap(self):
        small = ScriptedClient(["junk"] * 5)
        r = self.runner(small, budget=Budget(max_calls_per_decision=1))
        out = r.decide(make_point(), None)
        self.assertEqual(len(small.calls), 1)
        self.assertIn("budget", out.record.reason)
        r.decide(make_point(text="other"), None)           # a new decision starts a new count
        self.assertEqual(len(small.calls), 2)

    def test_cost_cap_and_price_table(self):
        small = ScriptedClient([{"choice": "a"}] * 3, name="m")
        budget = Budget(max_cost_units=0.0001, prices=PriceTable({"m": (1.0, 1.0)}))
        r = self.runner(small, budget=budget)
        out = r.decide(make_point(), None)
        self.assertGreater(budget.cost_units, 0.0001)
        self.assertGreater(out.record.cost["cost_units"], 0)
        self.assertEqual(r.decide(make_point(text="x2"), None).record.outcome, "defaulted")
        self.assertEqual(budget.totals["calls"], 1)

    def test_cache_hit_makes_no_call(self):
        small = ScriptedClient([{"choice": "a"}])
        r = self.runner(small)
        r.decide(make_point(), None)
        out = r.decide(make_point(), None)
        self.assertEqual((out.source, out.record.outcome), ("cache", "applied"))
        self.assertEqual(out.answer, {"choice": "a"})
        self.assertEqual(len(small.calls), 1)
        self.assertEqual(len(r.ledger), 2)
        self.assertEqual(r.decide(make_point(text="different evidence"), None).source, "default")  # script exhausted

    def test_cache_depends_on_prompt_version_and_policy(self):
        small = ScriptedClient([{"choice": "a"}, {"choice": "b"}, {"choice": "a"}])
        r = self.runner(small)
        p = make_point()
        r.decide(p, None)
        p.prompt_version = "t2"
        self.assertEqual(r.decide(p, None).source, "model")
        self.assertEqual(r.decide(p, None, policy="unchecked").source, "model")
        self.assertEqual(len(small.calls), 3)

    def test_cached_answer_must_pass_current_checks(self):
        small = ScriptedClient([{"choice": "a"}, {"choice": "b"}])
        r = self.runner(small)
        r.decide(make_point(), None)
        strict = make_point(post_check=lambda s, a: CheckResult(a["choice"] == "b", [] if a["choice"] == "b" else ["must be b"]))
        out = r.decide(strict, None)
        self.assertEqual((out.source, out.answer), ("model", {"choice": "b"}))

    def test_one_record_per_decide_on_every_path(self):
        small = ScriptedClient([{"choice": "a"}, "junk", "junk", {"choice": "a"}])
        r = self.runner(small)
        r.decide(make_point(text="1"), None)          # applied
        r.decide(make_point(text="2"), None)          # defaulted (two junk answers)
        r.decide(make_point(text="1"), None)          # cache
        r.decide(make_point(text="3"), None)          # applied
        self.assertEqual([x.outcome for x in r.ledger], ["applied", "defaulted", "applied", "applied"])
        self.assertEqual([x.source for x in r.ledger], ["model", "default", "cache", "model"])
        self.assertTrue(all(x.evidence_text and x.evidence_hash and x.policy == "grounded" for x in r.ledger))

    def test_dynamic_schema_and_default(self):
        point = DecisionPoint("dyn", "q", lambda s: Evidence("e"),
                              lambda s: {"type": "object", "properties": {"x": {"enum": s}}, "required": ["x"]},
                              default=lambda s: {"x": s[0]})
        small = ScriptedClient([{"x": "q"}, {"x": "q"}])
        out = self.runner(small).decide(point, ["m", "n"])
        self.assertEqual(out.answer, {"x": "m"})
        self.assertEqual(small.calls[0][1]["properties"]["x"]["enum"], ["m", "n"])

    def test_evidence_cap(self):
        with self.assertRaises(EvidenceTooLarge):
            self.runner(ScriptedClient([])).decide(make_point(cap=10, text="x" * 100), None)

    def test_unsupported_schema_raises(self):
        point = DecisionPoint("bad", "q", lambda s: Evidence("e"), {"pattern": "a"})
        with self.assertRaises(ValueError):
            self.runner(ScriptedClient([])).decide(point, None)


class LedgerTests(unittest.TestCase):
    def test_jsonl_round_trip_and_cache_from_ledger(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "sub", "ledger.jsonl")
            r = DecisionRunner({"small": ScriptedClient([{"choice": "a"}])}, ledger=Ledger(path))
            r.decide(make_point(), None)
            lines = open(path).read().strip().split("\n")
            self.assertEqual(len(lines), 1)
            row = json.loads(lines[0])
            self.assertEqual(row["decision"], "pick")
            self.assertEqual(row["answer"], {"choice": "a"})
            self.assertIn("evidence_text", row)
            # a new process: the ledger seeds the cache
            r2 = DecisionRunner({"small": ScriptedClient([])}, ledger=Ledger(path))
            out = r2.decide(make_point(), None)
            self.assertEqual(out.source, "cache")
            self.assertEqual(len(Ledger.read(path)), 2)   # the cache hit appended a record too

    def test_record_rejects_unknown_fields(self):
        with self.assertRaises(TypeError):
            DecisionRecord("x", bogus=1)
        self.assertEqual(DecisionRecord.from_dict({"decision": "x", "extra": 1}).decision, "x")


class ToolSetTests(unittest.TestCase):
    class Coded(Exception):
        code, detail = "my_code", "something specific"

        def to_dict(self):
            return {"code": self.code, "detail": self.detail, "extra": 1}

    def tools(self):
        ts = ToolSet()
        ts.add("add", lambda a, b=0: a + b, {"type": "object", "properties": {"a": {"type": "integer"},
               "b": {"type": "integer"}}, "required": ["a"], "additionalProperties": False}, "Add numbers.")

        def coded():
            raise self.Coded()
        ts.add("coded", coded, {"type": "object", "properties": {}})
        ts.add("crash", lambda: 1 / 0, {"type": "object", "properties": {}})
        return ts

    def test_listing(self):
        listing = self.tools().tools()
        self.assertEqual([t["name"] for t in listing], ["add", "coded", "crash"])
        self.assertEqual(listing[0]["description"], "Add numbers.")
        self.assertIn("inputSchema", listing[0])

    def test_calls(self):
        ts = self.tools()
        self.assertEqual(ts.call("add", {"a": 1, "b": 2}).value, 3)
        bad = ts.call("add", {"b": 2})
        self.assertFalse(bad.ok)
        self.assertEqual(bad.error["code"], "bad_arguments")
        self.assertIn("missing required property 'a'", bad.error["detail"])
        self.assertEqual(ts.call("add", {"a": 1, "zzz": 2}).error["code"], "bad_arguments")
        self.assertEqual(ts.call("nope").error["code"], "unknown_tool")
        self.assertEqual(ts.call("coded").error, {"code": "my_code", "detail": "something specific", "extra": 1})
        crash = ts.call("crash")
        self.assertEqual(crash.error["code"], "internal")
        self.assertIn("ZeroDivisionError", crash.error["detail"])

    def test_duplicate_and_bad_schema(self):
        ts = self.tools()
        with self.assertRaises(ValueError):
            ts.add("add", lambda: 1, {"type": "object"})
        with self.assertRaises(ValueError):
            ts.add("new", lambda: 1, {"pattern": "x"})


class ConfigTests(unittest.TestCase):
    TOML = """
policy = "structure_only"
[models.local]
provider = "fake"
model = "tiny"
cost_per_1k_in = 0.5
[models.big]
provider = "fake"
model = "huge"
[tiers]
small = "local"
large = "big"
[budget]
max_calls = 7
[limits]
max_blocks = 5
"""

    def test_from_toml(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "h.toml")
            open(path, "w").write(self.TOML)
            cfg = HarnessConfig.from_toml(path)
        self.assertEqual((cfg.policy, cfg.limits, cfg.budget), ("structure_only", {"max_blocks": 5}, {"max_calls": 7}))
        budget = cfg.make_budget()
        self.assertEqual(budget.max_calls, 7)
        self.assertEqual(budget.prices.cost("local", 1000, 0), 0.5)
        with self.assertRaises(ValueError):
            cfg.clients()          # no 'fake' provider registered yet
        ModelClient.register_provider("fake", lambda name, spec: ScriptedClient([], name=f"{name}:{spec['model']}"))
        try:
            clients = cfg.clients()
        finally:
            ModelClient._providers.pop("fake")
        self.assertEqual({t: c.name for t, c in clients.items()}, {"small": "local:tiny", "large": "big:huge"})

    def test_unknown_model_in_tier(self):
        with self.assertRaises(ValueError):
            HarnessConfig(models={}, tiers={"small": "ghost"})


if __name__ == "__main__":
    unittest.main()
