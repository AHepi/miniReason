"""Final verification: deliverables exist, JSON parses, every required key and
verdict marker present, and every check status is one of PASS/FAIL/NOT-CHECKABLE."""
import json
from pathlib import Path

errors = []

# 1. deliverables present
for p in ("out/prereg-checks.md", "out/prereg-checks.json"):
    if not Path(p).is_file() or Path(p).stat().st_size == 0:
        errors.append(f"missing or empty: {p}")

# 2. check/ scripts exist
expect_scripts = [f"check/check0{i}" for i in range(1, 10)]
have = sorted(str(p) for p in Path("check").glob("*.py"))
print("check scripts:", have)
for i in range(1, 10):
    if not any(f"check0{i}" in h for h in have):
        errors.append(f"no script for check {i}")

# 3. json parses and carries all nine checks + limits
r = json.loads(Path("out/prereg-checks.json").read_text(encoding="utf-8"))
need = ["1_validate_py_run", "2_sha256_vs_pins", "3_seats_vs_registry",
        "4_max_calls_arithmetic", "5_obligations", "6_referenced_paths_tracked",
        "7_vocabulary", "8_credential_scan", "9_dates_and_run_ids"]
for k in need:
    if k not in r["checks"]:
        errors.append(f"missing check key {k}")
    elif r["checks"][k]["status"] not in ("PASS", "FAIL", "NOT-CHECKABLE"):
        errors.append(f"bad status in {k}: {r['checks'][k]['status']}")
if not r.get("what_these_checks_cannot_establish"):
    errors.append("no cannot-establish list")
if not r.get("no_overall_score"):
    errors.append("no_overall_score flag missing")

# 4. md renders one section per check, each ending in a verdict
md = Path("out/prereg-checks.md").read_text(encoding="utf-8")
for i in range(1, 10):
    if f"## {i}." not in md:
        errors.append(f"md missing section {i}")
for verdict in md.count("> **PASS**"), md.count("> **FAIL**"), md.count("> **NOT-CHECKABLE**"):
    print("verdict counts:", verdict)
if md.count("> **PASS**") + md.count("> **FAIL**") + md.count("> **NOT-CHECKABLE**") != 9:
    errors.append("verdict block count != 9")
if "## What these checks cannot establish" not in md:
    errors.append("md missing limits section")

# 5. consistency spot-checks: statuses match the underlying evidence
c = r["checks"]
if c["1_validate_py_run"]["exit_code_root"] != 1: errors.append("check1 exit code wrong")
if c["2_sha256_vs_pins"]["n_mismatched"] != 1: errors.append("check2 mismatch count wrong")
if not c["2_sha256_vs_pins"]["obligations_canonical_digest"]["reproduces"]:
    errors.append("obligations canonical digest does not reproduce")
if c["3_seats_vs_registry"]["mismatches"]: errors.append("check3 mismatches nonempty")
if c["4_max_calls_arithmetic"]["leg_subtotal_sum"] != 396: errors.append("check4 sum != 396")
if (c["5_obligations"]["O_count_actual"], c["5_obligations"]["P_count_actual"]) != (7, 12):
    errors.append("check5 counts wrong")
if c["6_referenced_paths_tracked"]["missing"]: errors.append("check6 missing nonempty")
if c["8_credential_scan"]["hit_count"] != 0: errors.append("check8 hits nonzero")
if c["9_dates_and_run_ids"]["distinct_calendar_dates"] != ["2026-09-14"]:
    errors.append("check9 dates wrong")

print("statuses:", {k: v["status"] for k, v in c.items()})
print("ERRORS:" if errors else "ALL VERIFICATIONS PASSED")
for e in errors:
    print(" -", e)
raise SystemExit(1 if errors else 0)
