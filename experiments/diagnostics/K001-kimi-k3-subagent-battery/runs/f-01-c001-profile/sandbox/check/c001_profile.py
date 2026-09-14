#!/usr/bin/env python3
"""Failure profile of C001 occurrence-01, by failure code and per model family.

Reads every receipt under
  experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/
and the endpoint registry at src/minireason/data/endpoints.json, then writes
  out/c001-profile.md

There are two code-bearing fields per receipt: `failure_type` (provider-side)
and `validation_failure_type` (validation-side). A receipt may carry both.
Counts are information, never a warrant: no rates, no shares, no rankings
between families, arms or endpoints are computed here.

Run:  python3 check/c001_profile.py
"""

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESP_DIR = ROOT / "experiments" / "diagnostics" / "C001-contrast-triple" / "occurrence-01" / "responses"
ENDPOINTS_FILE = ROOT / "src" / "minireason" / "data" / "endpoints.json"
OUT_FILE = ROOT / "out" / "c001-profile.md"

CODE_FIELDS = ("failure_type", "validation_failure_type")
FIELD_GLOSS = {
    "failure_type": "provider-side",
    "validation_failure_type": "validation-side",
}
STATUS_ORDER = ["COMPLETE", "PARTIAL", "FAILED"]


def load_receipts():
    files = sorted(RESP_DIR.rglob("*.json"))
    receipts = []
    for f in files:
        r = json.loads(f.read_text(encoding="utf-8"))
        r["_path"] = str(f.relative_to(ROOT))
        receipts.append(r)
    return receipts


def fmt_values(values):
    """Format a set of observed values, separating recorded null from values."""
    non_null = sorted(v for v in values if v is not None)
    parts = [str(v) for v in non_null]
    out = ", ".join(parts)
    if None in values:
        out = (out + " and " if out else "") + "null (no recorded value)"
    return out


def main():
    registry = json.loads(ENDPOINTS_FILE.read_text(encoding="utf-8"))["endpoints"]
    # Receipts carry endpoint_slug, which is the registry `name` with `/` -> `-`.
    slug_to_name = {e["name"].replace("/", "-"): e["name"] for e in registry}
    slug_to_family = {e["name"].replace("/", "-"): e["family"] for e in registry}

    receipts = load_receipts()

    # Structural checks: count, coordinate/path agreement, slug coverage.
    assert len(receipts) == 240, f"expected 240 receipts, found {len(receipts)}"
    for r in receipts:
        c = r["coordinate"]
        expect_suffix = f"{c['endpoint_slug']}/{c['arm']}/{c['case']}/rep{c['replicate']}.json"
        assert r["_path"].endswith(expect_suffix), (r["_path"], expect_suffix)
        assert c["endpoint_slug"] in slug_to_family, c["endpoint_slug"]

    def family_of(r):
        return slug_to_family[r["coordinate"]["endpoint_slug"]]

    # ---- 1. Code census over all receipts -----------------------------------
    code_counts = Counter()  # (code, field) -> receipts carrying it
    for r in receipts:
        for field in CODE_FIELDS:
            if r.get(field):
                code_counts[(r[field], field)] += 1

    def has_provider(r):
        return bool(r.get("failure_type"))

    def has_validation(r):
        return bool(r.get("validation_failure_type"))

    n_both = sum(1 for r in receipts if has_provider(r) and has_validation(r))
    n_provider_only = sum(1 for r in receipts if has_provider(r) and not has_validation(r))
    n_validation_only = sum(1 for r in receipts if has_validation(r) and not has_provider(r))
    n_neither = sum(1 for r in receipts if not has_provider(r) and not has_validation(r))
    n_any = n_both + n_provider_only + n_validation_only

    codes_sorted = sorted(code_counts.items(), key=lambda kv: (kv[0][1], kv[0][0]))

    # ---- 2/3. Per-family and per-family-arm counts ---------------------------
    fam_receipts = Counter(family_of(r) for r in receipts)
    famarm_receipts = Counter((family_of(r), r["coordinate"]["arm"]) for r in receipts)
    fam_code = Counter()        # (family, code, field) -> count
    fam_both = Counter()
    fam_any = Counter()
    famarm_code = Counter()     # (family, arm, code, field) -> count
    famarm_both = Counter()
    famarm_any = Counter()
    for r in receipts:
        fam = family_of(r)
        arm = r["coordinate"]["arm"]
        for field in CODE_FIELDS:
            if r.get(field):
                fam_code[(fam, r[field], field)] += 1
                famarm_code[(fam, arm, r[field], field)] += 1
        if has_provider(r) and has_validation(r):
            fam_both[fam] += 1
            famarm_both[(fam, arm)] += 1
        if has_provider(r) or has_validation(r):
            fam_any[fam] += 1
            famarm_any[(fam, arm)] += 1

    # ---- 4. Status per endpoint ----------------------------------------------
    ep_status = Counter()  # (slug, status) -> count
    ep_total = Counter()
    for r in receipts:
        slug = r["coordinate"]["endpoint_slug"]
        ep_status[(slug, r["status"])] += 1
        ep_total[slug] += 1
    statuses_seen = sorted({s for (_, s) in ep_status},
                           key=lambda s: (STATUS_ORDER.index(s) if s in STATUS_ORDER else 99, s))

    # ---- 5. Receipts carrying a code ------------------------------------------
    coded = [r for r in receipts if has_provider(r) or has_validation(r)]
    coded.sort(key=lambda r: (r["coordinate"]["endpoint_slug"], r["coordinate"]["arm"],
                              r["coordinate"]["case"], r["coordinate"]["replicate"]))

    # ---- Evidence for ceiling notes -------------------------------------------
    slugs_present = sorted({r["coordinate"]["endpoint_slug"] for r in receipts})
    unresolved_texts = sorted({r["unresolved_reason"] for r in coded if r.get("unresolved_reason")})
    coded_by_slug = Counter(r["coordinate"]["endpoint_slug"] for r in coded)
    ep_coded_finish = {}       # slug -> set of finish_reason among coded receipts (incl None)
    ep_coded_ctoks = {}        # slug -> set of usage.completion_tokens among coded receipts (incl None)
    ep_timeout = {}            # slug -> set of timeout_seconds among all receipts
    for r in receipts:
        ep_timeout.setdefault(r["coordinate"]["endpoint_slug"], set()).add(r.get("timeout_seconds"))
    for r in coded:
        slug = r["coordinate"]["endpoint_slug"]
        usage = r.get("usage") or {}
        ep_coded_finish.setdefault(slug, set()).add(r.get("finish_reason"))
        ep_coded_ctoks.setdefault(slug, set()).add(usage.get("completion_tokens") if isinstance(usage, dict) else None)

    n_fcl_coded = sum(1 for r in coded if r["coordinate"]["arm"] == "fcl")
    n_prose_coded = sum(1 for r in coded if r["coordinate"]["arm"] == "prose")
    n_fcl = sum(1 for r in receipts if r["coordinate"]["arm"] == "fcl")
    n_prose = sum(1 for r in receipts if r["coordinate"]["arm"] == "prose")
    n_failed_coded = sum(1 for r in coded if r["status"] == "FAILED")
    n_partial_coded = sum(1 for r in coded if r["status"] == "PARTIAL")

    # ---- Compose the report ----------------------------------------------------
    L = []
    a = L.append
    a("# C001 occurrence-01 failure profile")
    a("")
    a("Produced by `python3 check/c001_profile.py` from the 240 response receipts under "
      "`experiments/diagnostics/C001-contrast-triple/occurrence-01/responses/` "
      "and the endpoint registry `src/minireason/data/endpoints.json`. "
      "Each receipt carries two code-bearing fields: `failure_type` (provider-side) and "
      "`validation_failure_type` (validation-side); one receipt may carry both.")
    a("")
    a("Counts below are information, never a warrant. No rate, share or ranking between "
      "families, arms or endpoints is computed; these are independent occasions under "
      "different declared ceilings, not competitors.")
    a("")
    a("## Endpoint-to-family mapping (derived)")
    a("")
    a("`endpoint_slug` in each receipt is the registry `name` with `/` replaced by `-`; "
      "`family` is then read from `src/minireason/data/endpoints.json`. The six endpoints "
      "present in this occurrence map as follows:")
    a("")
    a("| endpoint_slug | registry name | family | receipts |")
    a("|---|---|---|---|")
    for slug in slugs_present:
        a(f"| `{slug}` | `{slug_to_name[slug]}` | `{slug_to_family[slug]}` | {ep_total[slug]} |")
    a("")

    a("## 1. Failure-code census over all 240 receipts")
    a("")
    a("| failure code | source field | receipts carrying it |")
    a("|---|---|---|")
    for (code, field), n in codes_sorted:
        a(f"| `{code}` | `{field}` ({FIELD_GLOSS[field]}) | {n} |")
    a("")
    a("Co-carriage of the two code fields across the 240 receipts:")
    a("")
    a("| field combination | receipts |")
    a("|---|---|")
    a(f"| both `failure_type` and `validation_failure_type` | {n_both} |")
    a(f"| only `failure_type` | {n_provider_only} |")
    a(f"| only `validation_failure_type` | {n_validation_only} |")
    a(f"| neither field | {n_neither} |")
    a(f"| any code (union) | {n_any} |")
    a("")

    a("## 2. Failure codes per family")
    a("")
    hdr = "| family | receipts |"
    sep = "|---|---|"
    for (code, field), _ in codes_sorted:
        hdr += f" `{code}` (`{field}`) |"
        sep += "---|"
    hdr += " receipts with both fields | receipts with any code |"
    sep += "---|---|"
    a(hdr)
    a(sep)
    for fam in sorted(fam_receipts):
        row = f"| `{fam}` | {fam_receipts[fam]} |"
        for (code, field), _ in codes_sorted:
            row += f" {fam_code.get((fam, code, field), 0)} |"
        row += f" {fam_both.get(fam, 0)} | {fam_any.get(fam, 0)} |"
        a(row)
    a("")

    a("## 3. Failure codes per family and arm")
    a("")
    hdr = "| family | arm | receipts |"
    sep = "|---|---|---|"
    for (code, field), _ in codes_sorted:
        hdr += f" `{code}` (`{field}`) |"
        sep += "---|"
    hdr += " receipts with both fields | receipts with any code |"
    sep += "---|---|"
    a(hdr)
    a(sep)
    for fam, arm in sorted(famarm_receipts):
        row = f"| `{fam}` | `{arm}` | {famarm_receipts[(fam, arm)]} |"
        for (code, field), _ in codes_sorted:
            row += f" {famarm_code.get((fam, arm, code, field), 0)} |"
        row += f" {famarm_both.get((fam, arm), 0)} | {famarm_any.get((fam, arm), 0)} |"
        a(row)
    a("")

    a("## 4. Status distribution per endpoint")
    a("")
    hdr = "| endpoint_slug | family |"
    sep = "|---|---|"
    for s in statuses_seen:
        hdr += f" {s} |"
        sep += "---|"
    hdr += " total |"
    sep += "---|"
    a(hdr)
    a(sep)
    for slug in slugs_present:
        row = f"| `{slug}` | `{slug_to_family[slug]}` |"
        for s in statuses_seen:
            row += f" {ep_status.get((slug, s), 0)} |"
        row += f" {ep_total[slug]} |"
        a(row)
    a("")

    a("## 5. Receipts carrying a code")
    a("")
    a(f"{n_any} receipts carry at least one code ({n_partial_coded} with `status` = PARTIAL, "
      f"{n_failed_coded} with `status` = FAILED). Each is listed with its coordinate, "
      "the code(s) present, `finish_reason` and `usage.completion_tokens` "
      "(`null` means the receipt does not record a value).")
    a("")
    a("| endpoint_slug | arm | case | replicate | codes present | finish_reason | usage.completion_tokens |")
    a("|---|---|---|---|---|---|---|")
    for r in coded:
        c = r["coordinate"]
        carried = []
        for field in CODE_FIELDS:
            if r.get(field):
                carried.append(f"`{field}={r[field]}`")
        usage = r.get("usage")
        ctoks = usage.get("completion_tokens") if isinstance(usage, dict) else None
        fr = r.get("finish_reason")
        a(f"| `{c['endpoint_slug']}` | {c['arm']} | {c['case']} | {c['replicate']} "
          f"| {'; '.join(carried)} | {fr if fr is not None else 'null'} "
          f"| {ctoks if ctoks is not None else 'null'} |")
    a("")

    a("## 6. Where the codes are concentrated, and at what declared ceiling")
    a("")
    a(f"- `INCOMPLETE_GENERATION` (provider-side, `failure_type`) is concentrated on "
      f"`deepseek-flash`: {coded_by_slug['deepseek-flash']} of the {n_any} coded receipts are "
      "`deepseek-flash`, all in arm `fcl`; the remaining coded receipt is "
      "`ollama-glm-5.3/fcl/control/rep2`.")
    a(f"- On `deepseek-flash`, the coded receipts show `finish_reason` values "
      f"{fmt_values(ep_coded_finish['deepseek-flash'])} and `usage.completion_tokens` values "
      f"{fmt_values(ep_coded_ctoks['deepseek-flash'])}. Every coded `deepseek-flash` receipt that "
      "records a stopping point reports `finish_reason` = `length` with "
      "`usage.completion_tokens` = 8,192, and its `unresolved_reason` names an 8,192-token "
      "completion ceiling (quoted verbatim below). The recorded call timeout on "
      f"`deepseek-flash` is `timeout_seconds` = {fmt_values(ep_timeout['deepseek-flash'])} s. "
      "A token ceiling is a resource boundary; it is not evidence about the model's ability "
      "to solve the task.")
    a(f"- The single `ollama-glm-5.3` coded receipt (`fcl/control/rep2`) also reports "
      f"`finish_reason` = `length`; receipts on this endpoint record `timeout_seconds` = "
      f"{fmt_values(ep_timeout['ollama-glm-5.3'])} s. It reports `usage.completion_tokens` = 32,768, "
      "and its `unresolved_reason` names an 8,192-token ceiling; the two do not match "
      "(see section 7).")
    a("- `NO_PUBLIC_CONTENT` (validation-side, `validation_failure_type`) appears only on "
      "`deepseek-flash` arm `fcl`, and only together with the provider-side code: no receipt "
      "carries the validation-side code alone.")
    a(f"- No receipt in arm `prose` carries a code ({n_prose_coded} of {n_prose}); "
      f"arm `fcl` holds {n_fcl_coded} of {n_fcl} coded-cell receipts.")
    if unresolved_texts:
        a("")
        a("`unresolved_reason` text recorded on the coded receipts, quoted verbatim:")
        a("")
        for t in unresolved_texts:
            a(f"> {t}")
            a("")
    a("This concentration is a count under each endpoint's own declared conditions; it is not "
      "a comparison between endpoints and no rate or ranking is drawn from it.")
    a("")

    a("## 7. What the records do not settle")
    a("")
    a(f"- The {n_failed_coded} `FAILED` coded receipts (all `deepseek-flash` arm `fcl`) record "
      "`finish_reason` = null and `usage` = null (`usage_status` = `UNKNOWN`). Whether those "
      "calls stopped at the same 8,192-token completion ceiling, earlier, or for a different "
      "reason (a resource boundary such as the recorded 180-second call timeout, or a "
      "transport event) cannot be determined from these receipts.")
    a("- `ollama-glm-5.3/fcl/control/rep2` reports `usage.completion_tokens` = 32,768 with "
      "`finish_reason` = `length`, while its `unresolved_reason` text names an 8,192-token "
      "ceiling. Which completion ceiling was actually declared for that call is unresolved "
      "by these receipts; no C001 plan or config file is present in this sandbox under "
      "`experiments/diagnostics/C001-contrast-triple/occurrence-01/` to cross-check against.")
    a("- On the `FAILED` receipts, `provider_status`, `returned_model` and "
      "`strict_parse_would_succeed` are null, so the records do not settle whether the "
      "provider returned any usable content before validation recorded `NO_PUBLIC_CONTENT`.")
    a("- The receipts do not record why the provider-side and validation-side codes co-occur "
      f"exactly on the {n_both} `FAILED` receipts; they say what each field carries, not which "
      "check ran first or caused the other.")
    a("")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- Stdout verification summary ------------------------------------------
    print(f"receipts: {len(receipts)}  coded: {n_any}  both: {n_both}  "
          f"provider_only: {n_provider_only}  validation_only: {n_validation_only}  neither: {n_neither}")
    for (code, field), n in codes_sorted:
        print(f"  {field}: {code} = {n}")
    print("per-family coded receipts:")
    for fam in sorted(fam_receipts):
        print(f"  {fam}: receipts={fam_receipts[fam]} any_code={fam_any.get(fam, 0)} "
              f"both={fam_both.get(fam, 0)}")
    print("per-endpoint status:")
    for slug in slugs_present:
        print("  " + slug + ": " + ", ".join(f"{s}={ep_status.get((slug, s), 0)}" for s in statuses_seen))
    print(f"arm distribution of coded receipts: fcl={n_fcl_coded}/{n_fcl} prose={n_prose_coded}/{n_prose}")
    print(f"wrote {OUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
