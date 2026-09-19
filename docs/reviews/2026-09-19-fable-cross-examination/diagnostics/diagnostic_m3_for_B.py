# What this file does: three checks the cross-examination asked for and the frozen
# run (14a construction.py) never did.
#   1. Runs the thing-tracking test (M3) for B's rule from every seed, not only C's.
#   2. Reports the unconditional pass rate (passed / total), counting unbound as failed,
#      next to the given-bound rate the results file reported.
#   3. Re-buckets pairs by the FIRST collision after the change step instead of
#      "any crossing after the change", so a crossing failure is not mixed with an
#      earlier same-target failure.
# The frozen code is imported unchanged; only this file is new.
import json, re, sys
from collections import defaultdict
import construction as c

def parse_rule(name):
    m = re.match(r"IF (.+) THEN (\w+)( \+ hold)?$", name)
    cond_text, kind, hold = m.group(1), m.group(2), m.group(3) is not None
    atoms = re.findall(r"(\w+) (==|!=) (\w+)", cond_text)
    idx = [c.atom_index(a, op, b) for a, op, b in atoms]
    if len(idx) == 1:
        cond = ("atom", idx[0])
    else:
        joiner = "and" if " AND " in cond_text else "or"
        k1, k2 = sorted(idx)
        cond = (joiner, k1, k2)
    rule = (cond, (kind, hold))
    assert c.rule_name(rule) == name, (c.rule_name(rule), name)
    return rule

def thing_signature_first_collision(rules, laws, history_pairs):
    """Same procedure as construction.thing_signature, but the bucket is the first
    collision event after the change step, and unconditional rates are reported."""
    p = c.RulePredictor(rules)
    tot = defaultdict(lambda: [0, 0, 0])
    for configuration, change in history_pairs:
        unchanged = c.generate_sequence(configuration, ("identity",), laws)
        changed = c.generate_sequence(configuration, change, laws)
        if changed is None:
            continue
        first = next((changed[t]["event"] for t in range(c.CHANGE_STEP, c.RUN_LENGTH)
                      if changed[t]["event"] in ("same", "cross")), None)
        tag = {"cross": "first_cross", "same": "first_same", None: "no_collision_after"}[first]
        tot[tag][1] += 1
        p.reset()
        for t in range(c.CHANGE_STEP):
            p.observe(unchanged[t]["sensory"])
        things = unchanged[c.CHANGE_STEP - 1]["things"]
        binding, used, ok = {}, set(), True
        for si, st in enumerate(p.states()):
            if st is None:
                ok = False; break
            found = next((ti for ti, th in enumerate(things) if ti not in used and tuple(th) == st), None)
            if found is None:
                ok = False; break
            binding[si] = found; used.add(found)
        if not ok or len(binding) != 2:
            tot[tag][2] += 1
            continue
        p.advance_slots()
        inverse = {t_: s_ for s_, t_ in binding.items()}
        if change[0] == "displace":
            s = p.slots[inverse[change[1]]]
            s["cell"] = change[2]; s["prev_cell"] = change[2]
        elif change[0] == "set_velocity":
            p.slots[inverse[change[1]]]["vel"] = change[2]
        p.reconcile_slots(changed[c.CHANGE_STEP]["sensory"])
        p.previous_field = changed[c.CHANGE_STEP]["sensory"]
        tracking = True
        for t in range(c.CHANGE_STEP, c.RUN_LENGTH + 1):
            if t > c.CHANGE_STEP:
                p.observe(changed[t]["sensory"])
            st = p.states()
            for si, ti in binding.items():
                if st[si] is None or st[si] != tuple(changed[t]["things"][ti]):
                    tracking = False; break
            if not tracking:
                break
        if tracking:
            tot[tag][0] += 1
    out = {}
    for tag, (passed, total, unbound) in tot.items():
        bound = total - unbound
        out[tag] = {"total": total, "unbound": unbound, "passed": passed,
                    "given_bound": round(passed / bound, 4) if bound else None,
                    "unconditional": round(passed / total, 4)}
    return out

def with_unconditional(d):
    return {k: dict(v, given_bound=round(v["given_bound"], 4) if v["given_bound"] is not None else None,
                    unconditional=round(v["passed"] / v["total"], 4)) for k, v in d.items()}

R = json.load(open("results_out/results.json"))
laws = {"collision"}
h = c.build_history(laws)
exposure, evaluation = c.split_history(h)
pairs_eval = [(cfg, ch) for cfg, ch, _ in evaluation]
c_rules = [parse_rule(n) for n in R["C"]["rules"]]
b_rules = {b["seed"]: [parse_rule(n) for n in b["rules"]] for b in R["B"]}
out = {"note": "M3 for B by seed; unconditional = passed/total with unbound counted as failed; "
               "first_collision buckets classify by the first collision after the change step."}
sets = {"A0": [], "A0_C": c_rules, "A0_hand": [c.HAND_SAME, c.HAND_CROSS]}
for seed, rs in b_rules.items():
    sets[f"A0_B_seed{seed}"] = rs
out["any_crossing_bucket_as_frozen"] = {k: with_unconditional(c.thing_signature(v, laws, pairs_eval)) for k, v in sets.items()}
out["first_collision_bucket"] = {k: thing_signature_first_collision(v, laws, pairs_eval) for k, v in sets.items()}
json.dump(out, open("results_out/diagnostic_m3_for_B.json", "w"), indent=1)
for section in ("any_crossing_bucket_as_frozen", "first_collision_bucket"):
    print("==", section)
    for k, v in out[section].items():
        print(f"{k:12s}", {t: (d["given_bound"], d["unconditional"], d["passed"], d["total"], d["unbound"]) for t, d in v.items()})
