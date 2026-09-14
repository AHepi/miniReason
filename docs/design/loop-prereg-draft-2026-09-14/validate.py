"""Validate the L001 pre-registration bundle. Offline; makes no provider call."""
import json, hashlib, sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
REPO = Path("/home/user/miniReason")

from minireason.loop.types import LoopConfig, loop_plan_id, LoopError, CONFIG_SCHEMA
from minireason.loop import standard, receipts
from deepreason_core.canonical import canonical_json, sha256_hex

ok = lambda m: print("PASS  " + m)

# --- 1. the config loads against types.LoopConfig ---------------------------
cfg = LoopConfig.load(BUNDLE / "config.json")
ok(f"LoopConfig.load(config.json) -> schema {CONFIG_SCHEMA}, run_id {cfg.run_id}")
ok(f"cycle_budget={cfg.cycle_budget} max_calls={cfg.max_calls} provider_mode={cfg.provider_mode} "
   f"max_per_key={cfg.max_per_key} publish_ref={cfg.publish_ref!r}")
ok(f"audit={cfg.audit.as_dict()}")
ok(f"contrast={cfg.contrast.as_dict()}")

# --- 2. identity is a pure function of the declared values ------------------
raw = json.loads((BUNDLE / "config.json").read_bytes())
assert LoopConfig.from_mapping(raw).canonical_bytes() == cfg.canonical_bytes()
pins = {"src/minireason/data/endpoints.json": "0" * 64}
a = loop_plan_id(cfg, pins); b = loop_plan_id(raw, pins)
assert a == b
c = loop_plan_id(cfg, {"src/minireason/data/endpoints.json": "1" + "0" * 63})
assert c != a
ok(f"loop_plan_id is one id from file and object ({a[:16]}...); a changed pin changes it ({c[:16]}...)")

# --- 3. negative controls: the loader is strict -----------------------------
for mutate, code in (
        (lambda d: d.__setitem__("unexpected_key", 1), "CONFIG_UNKNOWN_KEY"),
        (lambda d: d.pop("audit"), "CONFIG_MISSING_KEY"),
        (lambda d: d["audit"].pop("judge_err_max"), "CONFIG_MISSING_KEY"),
        (lambda d: d.__setitem__("provider_mode", "dry"), "CONFIG_INVALID_VALUE"),
        (lambda d: d.__setitem__("max_per_key", 6), "CONFIG_INVALID_VALUE"),
        (lambda d: d["reading_set"].append(d["reading_set"][0]), "CONFIG_INVALID_VALUE")):
    d = json.loads(json.dumps(raw)); mutate(d)
    try:
        LoopConfig.from_mapping(d); raise SystemExit("loader accepted a bad config")
    except LoopError as exc:
        assert exc.code == code, (exc.code, code)
        ok(f"refused as {code}")

# --- 4. every seat exists in endpoints.json; G0 holds -----------------------
reg = {e["name"]: e for e in json.loads((REPO / "src/minireason/data/endpoints.json").read_bytes())["endpoints"]}
seats = {"critic": cfg.seats.critic, "defender": cfg.seats.defender,
         "variator": cfg.seats.variator,
         "judge-1": cfg.seats.judges[0], "judge-2": cfg.seats.judges[1]}
for role, name in seats.items():
    e = reg[name]
    ok(f"seat {role:9s} {name:24s} family={e['family']:22s} key_env={e['key_env']:18s} "
       f"timeout_seconds={e['timeout_seconds']}")
jf = {reg[n]["family"] for n in cfg.seats.judges}
assert len(cfg.seats.judges) == 2 and len(jf) == 2
assert reg[cfg.seats.critic]["family"] not in jf
assert reg[cfg.seats.defender]["family"] != reg[cfg.seats.critic]["family"]
assert reg[cfg.seats.defender]["family"] not in jf
assert len({reg[n]["family"] for n in seats.values()}) == 5
ok("G0 constitution: 2 judge families distinct; critic not in judge families; "
   "defender distinct from critic and from judge families; 5 distinct families over 5 seats")

# --- 5. the guard parameters agree with the pinned standard -----------------
assert tuple(cfg.reopen_reasons) == standard.REOPEN_REASONS
assert cfg.seats.paraphrase_n == standard.GUARD_PARAMETERS["paraphrase_n"] == 2
assert cfg.seats.schema_repair_budget == standard.GUARD_PARAMETERS["schema_repair_budget"] == 0
assert cfg.seats.min_judge_families == standard.GUARD_PARAMETERS["min_judge_families"] == 2
ok("reopen_reasons, paraphrase_n, schema_repair_budget and min_judge_families "
   "equal standard.REOPEN_REASONS / standard.GUARD_PARAMETERS")

# --- 6. reading_set.json agrees with the config -----------------------------
rs = json.loads((BUNDLE / "reading_set.json").read_bytes())
assert [e["key"] for e in rs["entries"]] == list(cfg.reading_set)
assert len(cfg.reading_set) == len(set(cfg.reading_set)) == 38
marks = [e for e in rs["entries"] if e["leg"] == "c001-mark"]
rows = [e for e in rs["entries"] if e["leg"] == "h005-row"]
assert (len(marks), len(rows)) == (16, 22)
ok("reading_set.json entries == config.reading_set, 38 unique keys (16 c001-mark + 22 h005-row)")

# --- 7. max_calls arithmetic reproduces ------------------------------------
d = rs["max_calls_derivation"]
total = sum(l["subtotal"] for l in d["legs"])
assert total == d["max_calls"] == cfg.max_calls == 396
assert sum(e["budgeted_calls"] for e in marks) == 108
assert sum(e["budgeted_calls"] for e in rows) == 242
ok(f"max_calls derivation: 0 (baseline) + 108 (12 cross-case x 9) + 242 (22 rows x 11) "
   f"+ 46 (one audit window) + 0 (dispatch) = {total} == config.max_calls")

# --- 8. obligations.json: digest reproduces, sets are as declared -----------
ob = json.loads((BUNDLE / "obligations.json").read_bytes())
body = {k: v for k, v in ob.items() if not k.startswith("obligations_sha256")}
assert sha256_hex(canonical_json(body)) == ob["obligations_sha256"]
O = [o for o in ob["obligations"] if o["set"] == "O"]
P = [o for o in ob["obligations"] if o["set"] == "P"]
assert len(O) == 7 and len(P) == 12
assert all("why_not_a_count" in o for o in ob["obligations"])
assert cfg.obligations_path.endswith("/obligations.json")
ok(f"obligations.json sha256 {ob['obligations_sha256']} reproduces over canonical bytes; "
   f"|O|={len(O)} |P|={len(P)}; every clause carries a why_not_a_count note")

# --- 9. calibration anchors re-resolve against published bytes -------------
cal = json.loads((BUNDLE / "calibration.json").read_bytes())
ut = json.loads((REPO / "experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14"
                 "/use-table-golden/use_table.json").read_bytes())
recs = {}
for r in ut["rows"]:
    for side in ("referring", "target"):
        rid, ck = r[f"{side}_record_id"], r[f"{side}_coordinate_key"]
        if r[f"{side}_record_verbatim"]:
            recs[f"{ck}#{rid}"] = r[f"{side}_record_verbatim"]
sha = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()
checked = 0
for row in cal["rows"]:
    for s in row["source_bytes"]:
        if "record" in s:
            assert sha(recs[s["record"]]) == s["sha256"], s["record"]; checked += 1
        elif s.get("field") == "banner":
            assert sha(ut["banner"]) == s["sha256"]; checked += 1
    for q in row.get("quoted_spans", ()):
        assert recs[q["from"]].count(q["text"]) == 1, q
ok(f"calibration.json: {checked} source-byte digests re-verify against the published files; "
   "every quoted span occurs exactly once in its source record")
banner_q = "A lexical overlap is not evidence of use."
assert ut["banner"].count(banner_q) == 1
assert all(v.count(banner_q) == 0 for v in recs.values())
dup_q = "Load imbalance or resentment can coexist with reduced friction on specified items"
assert recs["daily/mini_fcl/cycle01/objection#o2"].count(dup_q) == 1
ok("cal-05's framing-only quote occurs once in the banner and in no record; "
   "cal-07's duplicated sentence occurs once in o2 before the construction adds its second copy")
c001 = json.loads((REPO / "experiments/diagnostics/C001-contrast-triple/occurrence-02"
                   "/comparison.json").read_bytes())["tables"][0]
assert sorted(c001["cases"]["original"][1]["fcl"]["targets_named"]) == []
assert sorted(c001["cases"]["control"][0]["fcl"]["targets_named"]) == []
assert sorted(c001["cases"]["original"][3]["fcl"]["targets_named"]) == ["n1", "n2", "n4"]
assert sorted(c001["cases"]["control"][2]["fcl"]["targets_named"]) == ["n1", "n2"]
ok("cal-08's two order-swap pairs re-read from the published comparison.json: "
   "(empty, empty) -> same; ({n1,n2,n4}, {n1,n2}) -> differs")
assert len(cal["rows"]) == 9 and cal["calls_per_window"] == 9 * 2
for anchor in standard.CALIBRATION_ANCHORS:
    assert any(r["anchor"] == anchor.id for r in cal["rows"]), anchor.id
ok("calibration.json carries 9 rows (>= 8) and covers every standard.CALIBRATION_ANCHORS id")

# --- 10. the material the reading set names is as the published record says -
occ2_complete = sum(1 for case in c001["cases"].values() for r in case
                    if r["delivery_status"] == "COMPLETE")
assert occ2_complete == 20 and not json.loads(
    (REPO / "experiments/diagnostics/C001-contrast-triple/occurrence-02/comparison.json"
     ).read_bytes())["tables"][0]["unresolved_cells"]
ok("C001 occurrence-02: 20/20 replicates COMPLETE, unresolved_cells empty - the order rationale holds")
full = json.loads((REPO / "experiments/analyses/H005-occurrence-01-cycle01-snapshot-2026-09-14"
                   "/use-table-full/use_table.json").read_bytes())
assert full["rows"] == ut["rows"] and len(ut["rows"]) == 22
ok("H005 golden and full use tables carry byte-identical row lists (22 rows); "
   "the published 90-row figure counts them twice and the reading set names them once")

# --- 11. PREREG.md carries the frozen texts verbatim -----------------------
pre = (BUNDLE / "PREREG.md").read_text(encoding="utf-8")
assert standard.CEILING_TEXT in pre
assert not [s for s in standard.CEILING_REQUIRED_SENTENCES if s not in pre]
assert not [s for s in receipts.PREREGISTRATION_REQUIRED_SENTENCES if s not in pre]
assert ob["obligations_sha256"] in pre
ok(f"PREREG.md contains standard.CEILING_TEXT byte-for-byte, all "
   f"{len(standard.CEILING_REQUIRED_SENTENCES)} CEILING_REQUIRED_SENTENCES, all "
   f"{len(receipts.PREREGISTRATION_REQUIRED_SENTENCES)} PREREGISTRATION_REQUIRED_SENTENCES, "
   "and the obligations digest")
for f in sorted(BUNDLE.glob("*")):
    if f.suffix in (".md", ".json"):
        standard.assert_no_exhaustion_claim(f.read_text(encoding="utf-8"), f.name)
ok("every bundle file passes the standard's forbidden-stop-token scan")

# --- 12. no credential value anywhere --------------------------------------
blob = "\n".join(f.read_text(encoding="utf-8") for f in sorted(BUNDLE.glob("*"))
                 if f.suffix in (".md", ".json", ".py"))
import re, os
for env in ("DEEPSEEK_API_KEY", "OLLAMA_API_KEY"):
    for m in re.finditer(re.escape(env) + r"(.{0,4})", blob):
        assert not m.group(1).lstrip().startswith(("=", ":", "sk-")), m.group(0)
    val = os.environ.get(env)
    assert not val or val not in blob
assert not re.search(r"\bsk-[A-Za-z0-9]{8,}", blob)
ok("the bundle names DEEPSEEK_API_KEY and OLLAMA_API_KEY only as key_env names; "
   "no key value, no assignment form and no secret-shaped token appears anywhere")

print("\nALL CHECKS PASSED")
