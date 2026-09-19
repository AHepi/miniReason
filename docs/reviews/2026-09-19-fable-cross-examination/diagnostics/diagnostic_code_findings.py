# What this file does: checks five claims the code-bug witnesses made about
# experiment 1, on the unchanged frozen code.
#  (a) On the one-thing history (H_neutral), does a slot's "unconfirmed count" ever
#      exceed 0, so that the forgetting parameter tau could ever act?  If not, the
#      four-way tie is forced by the code, not found in the world.
#  (b) Do the four tau values make byte-identical predictions on H_neutral (same
#      signature), or only equal scores?
#  (c) Is M2 on H_full the same number as M1 on H_full?
#  (d) Is the swap change bit-for-bit the same as the identity change in the
#      sensory and true sequences?
#  (e) Does a fairer lookup baseline (fall back to shorter keys, majority vote,
#      no all-zero default) close the gap to the slot tracker on H_full?
import json
from collections import defaultdict, Counter
import kinds_from_selection as k

out = {}
def history(n_things, kinds):
    return k.build_history(6, n_things, kinds)
H_neutral = history(1, {"identity", "displace", "set_velocity"})
H_full = history(6 and 2, {"identity", "displace", "set_velocity", "occlude", "swap"})
def arch(name):
    for a in k.enumerate_architectures():
        if k.architecture_name(a) == name:
            return a
    raise KeyError(name)

# (a) and (b)
exp_n, eval_n = k.split_history(H_neutral, 6, 1)
counts_over_zero = {}
predictions = {}
for tau in ("0", "2", "5", "inf"):
    for r in ("2", "5"):
        name = f"slots=1:persist(tau={tau},r={r},jump_keeps_v=T)"
        a = arch(name)
        p = k.Predictor(a, 6, None)
        over = 0; preds = []
        for _, change, seq in eval_n:
            p.reset()
            for t in range(k.RUN_LENGTH):
                p.observe(seq[t]["sensory"])
                over += sum(1 for s in p.slots if s is not None and s["count"] > 0)
                preds.append(p.predict())
        counts_over_zero[name] = over
        predictions[name] = preds
out["a_unconfirmed_count_events_on_H_neutral_evaluation_half"] = counts_over_zero
ident = {}
for r in ("2", "5"):
    names = [f"slots=1:persist(tau={tau},r={r},jump_keeps_v=T)" for tau in ("0", "2", "5", "inf")]
    ident[f"r={r}"] = all(predictions[n] == predictions[names[0]] for n in names)
out["b_tau_family_predictions_identical_on_H_neutral"] = ident

# (c) and (d)
R = json.load(open("../out/12c results raw.json"))
rows = R["table"]
def num(x): return x["fitness"] if isinstance(x, dict) else x
out["c_M1_equals_M2_on_H_full_rows"] = sum(1 for row in rows if abs(num(row["M1"]["H_full"]) - num(row["M2"]["H_full"])) < 1e-12)
out["c_rows_total"] = len(rows)
by_conf = defaultdict(dict)
for conf, change, seq in H_full:
    if change[0] in ("identity", "swap"):
        by_conf[json.dumps(conf)][change[0]] = [(s["sensory"], s["true"]) for s in seq]
same = sum(1 for d in by_conf.values() if "swap" in d and d["swap"] == d["identity"])
out["d_swap_sequences_identical_to_identity"] = {"configurations_with_both": sum(1 for d in by_conf.values() if "swap" in d), "identical": same}

# (e) fairer lookup
exposure, evaluation = k.split_history(H_full, 6, 2)
def fair_table(kk, hist):
    votes = defaultdict(Counter)
    marginal = Counter()
    for _, _, seq in hist:
        buf = []
        for t in range(k.RUN_LENGTH):
            buf = (buf + [seq[t]["sensory"]])[-kk:]
            for L in range(1, len(buf) + 1):
                votes[tuple(buf[-L:])][seq[t + 1]["true"]] += 1
            marginal[seq[t + 1]["true"]] += 1
    table = {key: c.most_common(1)[0][0] for key, c in votes.items()}
    return table, marginal.most_common(1)[0][0]
def fair_lookup_fitness(kk, table, default, hist):
    correct = total = 0
    for _, _, seq in hist:
        buf = []
        for t in range(k.RUN_LENGTH):
            buf = (buf + [seq[t]["sensory"]])[-kk:]
            if t + 1 >= k.FIRST_SCORED_STEP:
                pred = default
                for L in range(len(buf), 0, -1):
                    if tuple(buf[-L:]) in table:
                        pred = table[tuple(buf[-L:])]; break
                correct += (pred == seq[t + 1]["true"]); total += 1
    return correct / total
fair = {}
for kk in (1, 2, 3):
    table, default = fair_table(kk, exposure)
    fair[f"k={kk}"] = round(fair_lookup_fitness(kk, table, default, evaluation), 4)
a_frozen = arch("lookup(k=3)")
t_frozen = k.expose_lookup(a_frozen, exposure, 6)
fair["frozen_lookup_k3"] = round(k.evaluate(a_frozen, t_frozen, evaluation, 6)[0], 4)
a_slot = arch("slots=2:persist(tau=inf,r=5,jump_keeps_v=F)")
fair["slot_tracker_tau_inf"] = round(k.evaluate(a_slot, None, evaluation, 6)[0], 4)
fair["ceiling_evaluation_half_in_sample"] = round(k.sensory_ceiling(evaluation)[0] if isinstance(k.sensory_ceiling(evaluation), tuple) else k.sensory_ceiling(evaluation)["fitness"], 4)
out["e_fairer_lookup_on_H_full_evaluation_half"] = fair
json.dump(out, open("results_out_code_findings.json", "w"), indent=1)
print(json.dumps(out, indent=1))
