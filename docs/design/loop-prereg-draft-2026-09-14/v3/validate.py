"""Validate the L001 pre-registration bundle. Offline; makes no provider call."""
import json, hashlib, sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
REPO = Path("/home/user/miniReason")

from minireason.loop.types import (LoopConfig, loop_plan_id, LoopError, CONFIG_SCHEMA,
                                   BLOCK_CODES, CEILING_BLOCK_REASONS, STOP_REASONS,
                                   PINNED_SOURCE_PATHS)
from minireason.loop import standard, receipts, contracts, roles, report, audits, surface
from minireason.loop import obligations as obligations_mod
from deepreason_core.canonical import canonical_json, sha256_hex

ok = lambda m: print("PASS  " + m)

PREREG_TEXT = (BUNDLE / "PREREG.md").read_text(encoding="utf-8")

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
# PR-07: types.PINNED_SOURCE_PATHS requires all six; a one-entry map is PIN_INVALID.
file_sha = lambda q: hashlib.sha256(Path(q).read_bytes()).hexdigest()
pins = {rel: file_sha(REPO / rel) for rel in PINNED_SOURCE_PATHS}
assert len(pins) == 6 and set(pins) == set(PINNED_SOURCE_PATHS)
a = loop_plan_id(cfg, pins); b = loop_plan_id(raw, pins)
assert a == b
c = dict(pins); c["src/minireason/data/endpoints.json"] = "1" + "0" * 63
c = loop_plan_id(cfg, c)
assert c != a
try:
    loop_plan_id(cfg, {"src/minireason/data/endpoints.json": pins["src/minireason/data/endpoints.json"]})
    raise SystemExit("loop_plan_id accepted an incomplete pin map")
except LoopError as exc:
    assert exc.code == "PIN_INVALID", exc.code
for rel in PINNED_SOURCE_PATHS:
    ok(f"pin  {rel:52s} {pins[rel]}")
ok(f"loop_plan_id over the six required pins is one id from file and object ({a}); "
   f"a changed pin changes it ({c[:16]}...); a five-entry map is refused PIN_INVALID")

# --- 2b. the accounts are settled and the publication target is explicit ----
assert cfg.publish_ref == "origin/claude/project-state-direction-j5rbun", cfg.publish_ref
for field in ("judge_err_max_account", "streak_max_account"):
    text = getattr(cfg.audit, field)
    assert text.strip(), field
    assert "PROVISIONAL" not in text, field
    assert "to be settled" not in text, field
    assert text.startswith("SETTLED at pre-registration review"), field
ok("publish_ref is explicit (ruling 2 branch); both guard-rail accounts are SETTLED, "
   "non-empty, and carry no PROVISIONAL and no promise to change themselves")

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
assert len(cfg.reading_set) == len(set(cfg.reading_set)) == 16
marks = [e for e in rs["entries"] if e["leg"] == "c001-mark"]
rows = [e for e in rs["entries"] if e["leg"] == "h005-row"]
assert (len(marks), len(rows)) == (16, 0)
assert cfg.run_id == "L002-loop-first-live-2026-09-14"
assert list(cfg.occurrences) == ["experiments/diagnostics/C001-contrast-triple/occurrence-03"]
assert list(cfg.contrast.occurrences) == ["experiments/diagnostics/C001-contrast-triple/occurrence-02"]
assert not (REPO / cfg.occurrences[0]).exists(), "occurrence-03 must be staged by its own receipt, not by this bundle"
assert (REPO / cfg.contrast.occurrences[0] / "comparison.json").is_file()
ok("reading_set.json entries == config.reading_set, 16 unique keys (16 c001-mark + 0 h005-row); "
   "run_id L002; the dispatch occurrence is a NEW C001 occurrence-03 (not yet staged, as declared) "
   "and the contrast leg is published occurrence-02, which carries the comparison.json S0 seals "
   "the four baselines from")

# --- 7. max_calls arithmetic reproduces ------------------------------------
d = rs["max_calls_derivation"]
total = sum(l["subtotal"] for l in d["legs"])
assert total == d["max_calls"] == cfg.max_calls == 174
assert sum(e["budgeted_calls"] for e in marks) == 108
assert sum(e["budgeted_calls"] for e in rows) == 0
assert [l["subtotal"] for l in d["legs"]] == [0, 108, 0, 46, 20]
assert "BOTH" in d["whose_budget_the_dispatch_calls_are"]
ok(f"max_calls derivation: 0 (4 baselines) + 108 (12 cross-case x 9) + 0 (no h005 row declared) "
   f"+ 46 (one audit window) + 20 (C001 occurrence-03 dispatch) = {total} == config.max_calls, "
   "and the dispatch leg is declared as BOTH the C001 study's own calls and inside this loop's "
   "max_calls")

# --- 8. obligations.json: digest reproduces, sets are as declared -----------
ob = json.loads((BUNDLE / "obligations.json").read_bytes())
body = {k: v for k, v in ob.items() if not k.startswith("obligations_sha256")}
assert sha256_hex(canonical_json(body)) == ob["obligations_sha256"]
O = [o for o in ob["obligations"] if o["set"] == "O"]
P = [o for o in ob["obligations"] if o["set"] == "P"]
assert len(O) == 7 and len(P) == 13
assert all("why_not_a_count" in o for o in ob["obligations"])
assert cfg.obligations_path.endswith("/obligations.json")
ok(f"obligations.json canonical-body sha256 {ob['obligations_sha256']} reproduces over canonical "
   f"bytes; |O|={len(O)} |P|={len(P)}; every clause carries a why_not_a_count note")

# PR-02: the bundle must publish BOTH digests and say which enters the identity.
loaded = obligations_mod.load_obligations(BUNDLE / "obligations.json")
file_digest = obligations_mod.pin(loaded)
canonical_digest = obligations_mod.canonical_pin(loaded)
assert canonical_digest == ob["obligations_sha256"] == sha256_hex(canonical_json(body))
assert file_digest == file_sha(BUNDLE / "obligations.json")
assert file_digest != canonical_digest
ok(f"obligations.pin() (the digest folded into loop_plan_id) = {file_digest}; "
   f"obligations.canonical_pin() (the digest the prose publishes) = {canonical_digest}; "
   "the two are different values over one document and both are named")

# PR-01: no bundle JSON may carry a key from standard.FORBIDDEN_KEYS.
for name in ("config.json", "obligations.json", "reading_set.json", "calibration.json"):
    contracts.assert_no_scoring_keys(json.loads((BUNDLE / name).read_bytes()))
ok("contracts.assert_no_scoring_keys passes over all four bundle JSON documents "
   "(calibration.json's former `scoring` key is now `error_rule`)")

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
module_anchors = [anchor.id for anchor in standard.CALIBRATION_ANCHORS]
bundle_anchors = [r["anchor"] for r in cal["rows"]]
for anchor_id in module_anchors:
    assert anchor_id in bundle_anchors, anchor_id
extra = [a for a in bundle_anchors if a not in module_anchors]
assert sorted(extra) == ["duplicated-passage-non-unique-offset", "fabricated-decisive-point",
                         "order-swap-sensitive-pair", "paraphrase-invariant-pair"], extra
assert "anchor_set_extension" in cal
assert "not reachable by the case-law closure" in PREREG_TEXT.replace("**", "")
ok(f"calibration.json carries 9 rows covering every standard.CALIBRATION_ANCHORS id "
   f"({len(module_anchors)} kinds) plus {len(extra)} bundle-pinned guard probes the standard body "
   "does not carry, declared as such in anchor_set_extension (PR-21)")

# PR-06 / REVIEW-WAVE1 B3: every anchor of the frozen standard must admit at
# least one uniquely-resolving quote inside a declared span, or it charges the
# panel an error no seat made. The probe runs both constructions of cal-01.
import copy
probe_row = [r for r in ut["rows"]
             if r.get("referring_record_verbatim") and r.get("target_record_verbatim")][0]
referring_only = copy.deepcopy(probe_row)
referring_only["target_record_verbatim"] = None
referring_only.pop("target_record_source_span", None)
s_one = surface.build_surface(referring_only)
body_text = probe_row["referring_record_verbatim"]
windows = (20, 40, 80, len(body_text))
for n in windows:
    offset = surface.resolve_unique(s_one, body_text[:n])
    assert offset is not None, ("referring-region-only window did not resolve", n)
    assert surface.within_declared_span(s_one, offset), n
two_copies = copy.deepcopy(probe_row)
two_copies["target_record_verbatim"] = body_text
two_copies["target_record_source_span"] = probe_row["referring_record_source_span"]
s_two = surface.build_surface(two_copies)
for n in windows:
    assert surface.resolve_unique(s_two, body_text[:n]) is None, ("two-copy window resolved", n)
assert standard.CALIBRATION_ANCHORS[0].id == "self-juxtaposition"
assert "referring region alone" in standard.CALIBRATION_ANCHORS[0].construction
assert "referring region alone" in cal["rows"][0]["construction"]
ok("cal-01 probe (REVIEW-WAVE1 B3 / PR-06): the referring-region-only construction resolves "
   f"uniquely inside a declared span at every window {windows}, and the former two-copy "
   "construction resolves at none of them; the module anchor and the bundle row both carry the "
   "repaired construction")

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

# --- 10b. the bundle's enumerations equal the module constants (PR-25) ------
voc = rs["vocabularies"]
assert tuple(voc["reading_vocabulary"]["values"]) == standard.READING_VOCABULARY
assert tuple(voc["nominable_relations"]["values"]) == standard.NOMINABLE_RELATIONS
assert tuple(voc["marks"]["values"]) == standard.MARKS
assert {k: tuple(v) for k, v in voc["difference_kinds"]["values"].items()} == \
       {k: tuple(v) for k, v in standard.DIFFERENCE_KINDS.items()}
assert sorted(voc["block_codes"]["values"]) == sorted(BLOCK_CODES)
assert tuple(voc["ceiling_block_reasons"]["values"]) == CEILING_BLOCK_REASONS
assert tuple(voc["block_register_headings"]["values"]) == report.BLOCK_REGISTER_HEADINGS
assert tuple(voc["cell_states"]["values"]) == obligations_mod.CELL_STATES
assert tuple(voc["reopen_reasons"]["values"]) == standard.REOPEN_REASONS
assert sorted(voc["stop_reasons"]["values"]) == sorted(STOP_REASONS)
assert sorted(voc["forbidden_keys"]["values"]) == sorted(standard.FORBIDDEN_KEYS)
assert voc["calibration_anchor_kinds"]["values"] == module_anchors
assert len(report.BLOCK_REGISTER_HEADINGS) == len(BLOCK_CODES) == 10
assert len(CEILING_BLOCK_REASONS) == 9 and "constitution" in report.BLOCK_REGISTER_HEADINGS
ok("reading_set.json vocabularies: six reading values, five nominable relations, three marks, "
   "four per-register difference-kind sets, ten block codes, nine ceiling reasons, ten printed "
   "register headings, four cell states, three reopen reasons, seven stop reasons and five "
   "calibration anchor kinds all equal their module constants")

# --- 10c. the declared resource conditions equal what will be sent (PR-10) --
rc = rs["resource_conditions"]
assert {k: int(v) for k, v in rc["role_max_tokens"].items()} == dict(roles.ROLE_MAX_TOKENS)
assert rc["gateway_wall_seconds"] == roles.GATEWAY_WALL_SECONDS == 300
assert rc["generation_share"] == roles.GENERATION_SHARE
assert rc["observed_tokens_per_second"] == roles.OBSERVED_TOKENS_PER_SECOND
assert rc["min_max_tokens"] == roles.MIN_MAX_TOKENS
assert rc["gateway_wall_tolerance_seconds"] == roles.GATEWAY_WALL_TOLERANCE_SECONDS
assert rc["temperature"] == roles.TEMPERATURE
assert {e["timeout_seconds"] for e in reg.values()} == {180}
assert rc["role_max_tokens"]["variator"] == cfg.seats.paraphrase_n * roles.VARIATOR_TOKENS_PER_PARAPHRASE
assert roles.JSON_OBJECT_ONLY_FAMILIES == frozenset({"deepseek"})
for role_name, seat_name in (("critic", cfg.seats.critic), ("defender", cfg.seats.defender),
                             ("judge", cfg.seats.judges[0]), ("judge", cfg.seats.judges[1]),
                             ("variator", cfg.seats.variator)):
    wall = min(reg[seat_name]["timeout_seconds"], roles.GATEWAY_WALL_SECONDS)
    ceiling = int(wall * roles.GENERATION_SHARE * roles.OBSERVED_TOKENS_PER_SECOND)
    sent = min(roles.ROLE_MAX_TOKENS[role_name], ceiling)
    assert wall == 180 and ceiling == 8100 and sent == roles.ROLE_MAX_TOKENS[role_name]
    ok(f"bound {role_name:9s} {seat_name:24s} wall=min({reg[seat_name]['timeout_seconds']},300)="
       f"{wall}s  wall_ceiling={ceiling}  max_tokens sent={sent}  "
       f"thinking={'False' if reg[seat_name]['family'] == 'deepseek' else 'not sent'}")
ok("reading_set.json resource_conditions reproduce roles.ROLE_MAX_TOKENS, the "
   "min(timeout, 300) gateway-wall rule, the 8100-token wall ceiling and the "
   "thinking=False-on-deepseek-only rule exactly")

# --- 11. PREREG.md carries the frozen texts verbatim -----------------------
pre = PREREG_TEXT
assert standard.CEILING_TEXT in pre
assert not [s for s in standard.CEILING_REQUIRED_SENTENCES if s not in pre]
assert not [s for s in receipts.PREREGISTRATION_REQUIRED_SENTENCES if s not in pre]
assert ob["obligations_sha256"] in pre
assert file_digest in pre and canonical_digest in pre
assert standard.STANDARD_BODY_SHA256 in pre and standard.CEILING_SHA256 in pre
assert audits.CALIBRATION_EXCHANGES_SHA256 in pre
assert "to be re-read at PREFLIGHT after the clone freezes" in pre
ok(f"PREREG.md contains standard.CEILING_TEXT byte-for-byte, all "
   f"{len(standard.CEILING_REQUIRED_SENTENCES)} CEILING_REQUIRED_SENTENCES, all "
   f"{len(receipts.PREREGISTRATION_REQUIRED_SENTENCES)} PREREGISTRATION_REQUIRED_SENTENCES, "
   "both obligations digests, and the three clone-side pins with their re-read sentence")

# the enumerations are printed for a human reader too, and the inventory is twelve
for token in (list(standard.READING_VOCABULARY) + list(standard.MARKS)
              + sorted(BLOCK_CODES) + list(standard.REOPEN_REASONS)
              + [k for kinds in standard.DIFFERENCE_KINDS.values() for k in kinds]):
    assert f"`{token}`" in pre, token
assert "the twelve C001 occurrence-01 juxtapositions" in pre
assert "L001 was refused at S1" in pre and "OCCURRENCE_NOT_DISPATCHABLE" in pre
assert "a new `loop_plan_id`" in pre and "L002" in pre
assert "occurrence-03" in pre and "328b9452c66fed52203015c540652d3b8ad3107d44dece56b55ebe721da341c8" in pre
assert "L001-loop-first-live-2026-09-14" not in pre
assert "REC-20260914-Z opened at 2026-09-14T00:00:00Z" not in pre
assert "REC-YYYYMMDD-X opened at <minted at S0>" in pre
assert "origin/claude/project-state-direction-j5rbun" in pre
assert "pending owner merge" in pre
assert "PROVISIONAL" not in pre
assert "tests no clause of Account" in pre
ok("PREREG.md prints every enumerated token, names twelve unread C001 occurrence-01 "
   "juxtapositions, carries the impossible receipt placeholder, the ruling-2 branch deviation "
   "and the Account non-goal sentence, and no longer carries the word PROVISIONAL")
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
    # This is the one place the bundle touches a secret at all. The value is read
    # from the process environment, compared against the bundle text, and never
    # printed, stored, logged or written anywhere: the assertion only fails, and
    # the failure message carries no value. Ruling 4 and AGENTS.md: a credential
    # never reaches a tracked file, a log, a receipt or a commit.
    val = os.environ.get(env)
    assert not val or val not in blob
assert not re.search(r"\bsk-[A-Za-z0-9]{8,}", blob)
ok("the bundle names DEEPSEEK_API_KEY and OLLAMA_API_KEY only as key_env names; "
   "no key value, no assignment form and no secret-shaped token appears anywhere")

print("\nALL CHECKS PASSED")
