"""
What this file does
-------------------
Runs the experiment frozen in "13 Test design - construction".

The world from experiment 1 gains a law its predictor grammar has no machinery
for: two things that would meet stay put and exchange velocities. Starting from
the architecture experiment 1's occlusion world selected (A0), three processes
try to cope: C builds rules from itemised records of what went wrong;
B searches the same rule language blindly, guided only by a fitness number;
S0 picks the best of the old closed grammar. Then we test whether the records
of what went wrong were really on C's route (scramble them; C should break,
B should not notice), whether the built rules are faithful components, and
whether what was built stays usable when a second new law arrives.

Everything exact; fixed seeds for the blind search.

Run:  python3 construction.py --controls      (section 6 checks)
      python3 construction.py results_dir     (full run)
"""

import itertools
import json
import os
import random
import sys
import hashlib
from collections import defaultdict

import kinds_from_selection as base
from kinds_from_selection import (step_kinematics, occupancy_bits, Predictor, RUN_LENGTH,
                                  CHANGE_STEP, FIRST_SCORED_STEP, enumerate_architectures,
                                  architecture_name, expose_lookup, evaluate, sensory_ceiling)

NUM_CELLS = 6
A0 = {"use_lookup": False, "k": None, "num_slots": 2, "rule": ("persist", "inf", 5, False)}
MAX_RULES = 3

# ---------------------------------------------------------------------------
# The world with new laws
# ---------------------------------------------------------------------------

def next_state(p, v, laws):
    """Base kinematics (reflect-and-move), then the sticky-wall law if present."""
    n, w = step_kinematics(p, v, NUM_CELLS)
    if "sticky_wall" in laws and w != v:
        return p, 0, "wall_stop"
    return n, w, None


def world_step(things, laws):
    """things: list of two (cell, vel). Kinematics first, then the pairwise law
    on the kinematic next-states. Returns (new_things, event)."""
    (p1, v1), (p2, v2) = things
    n1, w1, e1 = next_state(p1, v1, laws)
    n2, w2, e2 = next_state(p2, v2, laws)
    if "collision" in laws and (n1 == n2 or (n1 == p2 and n2 == p1)):
        event = "same" if n1 == n2 else "cross"
        return [(p1, w2), (p2, w1)], event   # hold positions, exchange outgoing velocities
    return [(n1, w1), (n2, w2)], e1 or e2


def enumerate_configurations_distinct():
    states = [(c, v) for c in range(NUM_CELLS) for v in (-1, 0, 1)]
    return [list(pair) for pair in itertools.combinations(states, 2) if pair[0][0] != pair[1][0]]


def enumerate_changes(configuration):
    changes = [("identity",)]
    other = {0: configuration[1][0], 1: configuration[0][0]}
    for i in range(2):
        for c in range(NUM_CELLS):
            if c != other[i] and c != configuration[i][0]:
                changes.append(("displace", i, c))
    for i in range(2):
        for v in (-1, 0, 1):
            changes.append(("set_velocity", i, v))
    return changes


def apply_change(things, change):
    things = [list(t) for t in things]
    if change[0] == "displace":
        things[change[1]][0] = change[2]
    elif change[0] == "set_velocity":
        things[change[1]][1] = change[2]
    return [tuple(t) for t in things]


def generate_sequence(configuration, change, laws):
    things = [tuple(t) for t in configuration]
    out = []
    for t in range(RUN_LENGTH + 1):
        if t == CHANGE_STEP:
            things = apply_change(things, change)
            if things[0][0] == things[1][0]:
                return None  # displace onto the other thing: not admitted
        bits = occupancy_bits(things, NUM_CELLS)
        out.append({"sensory": bits, "true": bits, "things": list(things), "event": None})
        things, event = world_step(things, laws)
        out[-1]["event"] = event  # event on the transition t -> t+1
    return out


def build_history(laws):
    seqs = []
    for configuration in enumerate_configurations_distinct():
        for change in enumerate_changes(configuration):
            seq = generate_sequence(configuration, change, laws)
            if seq is not None:
                seqs.append((configuration, change, seq))
    return seqs


def split_history(history):
    confs = enumerate_configurations_distinct()
    even = {tuple(map(tuple, c)) for i, c in enumerate(confs) if i % 2 == 0}
    exposure = [s for s in history if tuple(map(tuple, s[0])) in even]
    evaluation = [s for s in history if tuple(map(tuple, s[0])) not in even]
    return exposure, evaluation


# ---------------------------------------------------------------------------
# The rule language (meta-grammar)
# ---------------------------------------------------------------------------

TERM_NAMES = ["c_i", "v_i", "n_i", "w_i", "c_j", "v_j", "n_j", "w_j"]


def term_values(ci, vi, cj, vj):
    """n, w = the slot's own kinematic next cell and next velocity."""
    ni, wi = step_kinematics(ci, vi, NUM_CELLS)
    nj, wj = step_kinematics(cj, vj, NUM_CELLS)
    return (ci, vi, ni, wi, cj, vj, nj, wj)


ATOMS = [(a, b, op) for a in range(len(TERM_NAMES)) for b in range(a + 1, len(TERM_NAMES)) for op in ("==", "!=")]
CONDITIONS = [("atom", k) for k in range(len(ATOMS))]
CONDITIONS += [("and", k1, k2) for k1 in range(len(ATOMS)) for k2 in range(k1 + 1, len(ATOMS))]
CONDITIONS += [("or", k1, k2) for k1 in range(len(ATOMS)) for k2 in range(k1 + 1, len(ATOMS))]
ACTION_KINDS = ["swap_next_v", "swap_v", "reverse_both", "reverse_i", "reverse_j", "stop_both", "stop_i", "stop_j"]
ACTIONS = [(kind, hold) for kind in ACTION_KINDS for hold in (True, False)]


def atom_true(k, tv):
    a, b, op = ATOMS[k]
    return (tv[a] == tv[b]) if op == "==" else (tv[a] != tv[b])


def condition_true(cond, tv):
    if cond[0] == "atom":
        return atom_true(cond[1], tv)
    x, y = atom_true(cond[1], tv), atom_true(cond[2], tv)
    return (x and y) if cond[0] == "and" else (x or y)


def condition_atoms(cond):
    return 1 if cond[0] == "atom" else 2


def atom_name(k):
    a, b, op = ATOMS[k]
    return f"{TERM_NAMES[a]} {op} {TERM_NAMES[b]}"


def condition_name(cond):
    if cond[0] == "atom":
        return atom_name(cond[1])
    return f"({atom_name(cond[1])}) {cond[0].upper()} ({atom_name(cond[2])})"


def rule_name(rule):
    cond, (kind, hold) = rule
    return f"IF {condition_name(cond)} THEN {kind}{' + hold' if hold else ''}"


def apply_action(kind, vi, vj, wi=None, wj=None):
    if kind == "swap_next_v":
        return wj, wi
    if kind == "swap_v":
        return vj, vi
    if kind == "reverse_both":
        return -vi, -vj
    if kind == "reverse_i":
        return -vi, vj
    if kind == "reverse_j":
        return vi, -vj
    if kind == "stop_both":
        return 0, 0
    if kind == "stop_i":
        return 0, vj
    return vi, 0


def action_touches(kind, i, j):
    if kind in ("swap_next_v", "swap_v", "reverse_both", "stop_both"):
        return {i, j}
    return {i} if kind.endswith("_i") else {j}


def apply_rules(states, rules):
    """states: [(c,v)|None, (c,v)|None]. Returns (new_states, held_set, fired_list)."""
    states = list(states)
    held = set()
    fired = []
    if states[0] is None or states[1] is None or not rules:
        return states, held, fired
    for rule in rules:
        cond, (kind, hold) = rule
        for i, j in ((0, 1), (1, 0)):
            tv = term_values(states[i][0], states[i][1], states[j][0], states[j][1])
            if condition_true(cond, tv):
                vi, vj = apply_action(kind, states[i][1], states[j][1], tv[3], tv[7])
                states[i] = (states[i][0], vi)
                states[j] = (states[j][0], vj)
                if hold:
                    held |= action_touches(kind, i, j)
                fired.append((rule, i, j))
                break
    return states, held, fired


def kinematics(states, held):
    out = []
    for idx, st in enumerate(states):
        if st is None:
            out.append(None)
        elif idx in held:
            out.append(st)
        else:
            out.append(step_kinematics(st[0], st[1], NUM_CELLS))
    return out


def simulate_next(states, rules):
    s2, held, _ = apply_rules(states, rules)
    return kinematics(s2, held)


def field_of(states):
    bits = 0
    for st in states:
        if st is not None:
            bits |= 1 << st[0]
    return bits


class RulePredictor(Predictor):
    def __init__(self, rules):
        super().__init__(A0, NUM_CELLS, {})
        self.rules = list(rules)

    def states(self):
        return [None if s is None else (s["cell"], s["vel"]) for s in self.slots]

    def advance_slots(self):
        nxt = simulate_next(self.states(), self.rules)
        for idx, s in enumerate(self.slots):
            if s is None:
                continue
            s["prev_cell"] = s["cell"]
            s["cell"], s["vel"] = nxt[idx]

    def predict(self):
        return field_of(simulate_next(self.states(), self.rules))


# ---------------------------------------------------------------------------
# Evaluation with collision / non-collision split
# ---------------------------------------------------------------------------

def is_collision_step(seq, t):
    return seq[t]["event"] in ("same", "cross", "wall_stop")


def evaluate_rules(rules, history):
    p = RulePredictor(rules)
    tot = defaultdict(lambda: [0, 0])
    for _, change, seq in history:
        p.reset()
        for t in range(RUN_LENGTH):
            p.observe(seq[t]["sensory"])
            if t + 1 >= FIRST_SCORED_STEP:
                ok = p.predict() == seq[t + 1]["true"]
                key = "collision" if is_collision_step(seq, t) else "other"
                tot[key][0] += ok
                tot[key][1] += 1
                tot["all"][0] += ok
                tot["all"][1] += 1
    return {k: (v[0] / v[1] if v[1] else None) for k, v in tot.items()}


def ceiling_split(history):
    counts = {}
    for _, _, seq in history:
        for t in range(RUN_LENGTH):
            key = tuple(s["sensory"] for s in seq[:t + 1])
            counts.setdefault(key, defaultdict(int))[seq[t + 1]["true"]] += 1
    best = {k: max(c.items(), key=lambda kv: (kv[1], -kv[0]))[0] for k, c in counts.items()}
    tot = defaultdict(lambda: [0, 0])
    for _, _, seq in history:
        for t in range(RUN_LENGTH):
            if t + 1 < FIRST_SCORED_STEP:
                continue
            key = tuple(s["sensory"] for s in seq[:t + 1])
            ok = best[key] == seq[t + 1]["true"]
            k = "collision" if is_collision_step(seq, t) else "other"
            tot[k][0] += ok; tot[k][1] += 1; tot["all"][0] += ok; tot["all"][1] += 1
    return {k: v[0] / v[1] for k, v in tot.items()}


# ---------------------------------------------------------------------------
# C: construction from defect records
# ---------------------------------------------------------------------------

def collect_records(rules, history):
    """V = defects, N = non-defects. Each record: (state_after_existing_rules, held, predicted, true)."""
    p = RulePredictor(rules)
    V, N = [], []
    for _, change, seq in history:
        p.reset()
        for t in range(RUN_LENGTH):
            p.observe(seq[t]["sensory"])
            if t + 1 < FIRST_SCORED_STEP:
                continue
            st = p.states()
            if st[0] is None or st[1] is None:
                continue
            s2, held, _ = apply_rules(st, rules)
            pred = field_of(kinematics(s2, held))
            true = seq[t + 1]["true"]
            rec = (tuple(s2), frozenset(held), pred, true)
            (V if pred != true else N).append(rec)
    return V, N


def cond_true_any_order(cond, states):
    for i, j in ((0, 1), (1, 0)):
        if condition_true(cond, term_values(states[i][0], states[i][1], states[j][0], states[j][1])):
            return True
    return False


def predict_with_new_rule(states, held, rule):
    s2, held2, _ = apply_rules(states, [rule])
    return field_of(kinematics(s2, held | held2))


def construct_round(V, N, top_m=20):
    """Build one rule from itemised records. Never computes an aggregate fitness."""
    if not V:
        return None, {"reason": "no defects"}
    scores = []
    for idx, cond in enumerate(CONDITIONS):
        tp = sum(1 for rec in V if cond_true_any_order(cond, rec[0]))
        if tp == 0:
            continue
        fp = sum(1 for rec in N if cond_true_any_order(cond, rec[0]))
        scores.append((tp - fp, -condition_atoms(cond), idx))
    scores.sort(reverse=True)
    top = scores[:top_m]
    best = None
    for score, negatoms, idx in top:
        cond = CONDITIONS[idx]
        for action in ACTIONS:
            rule = (cond, action)
            fixed = sum(1 for rec in V if cond_true_any_order(cond, rec[0]) and predict_with_new_rule(rec[0], rec[1], rule) == rec[3])
            broken = sum(1 for rec in N if cond_true_any_order(cond, rec[0]) and predict_with_new_rule(rec[0], rec[1], rule) != rec[3])
            net = fixed - broken
            key = (net, negatoms)
            if best is None or key > best[0]:
                best = (key, rule, {"fixed": fixed, "broken": broken, "condition_score": score})
    if best is None or best[0][0] <= 0:
        return None, {"reason": "no rule with positive net", "best": best[2] if best else None}
    return best[1], best[2]


def construct(start_rules, exposure, max_rules=MAX_RULES, transform=None, log=None):
    rules = list(start_rules)
    rounds = []
    for r in range(max_rules - len(start_rules)):
        V, N = collect_records(rules, exposure)
        if transform is not None:
            V, N = transform(V, N)
        rule, info = construct_round(V, N)
        rounds.append({"round": r + 1, "defects": len(V), "non_defects": len(N),
                       "rule": rule_name(rule) if rule else None, "info": info})
        if rule is None:
            break
        rules.append(rule)
    return rules, rounds


# ---------------------------------------------------------------------------
# B: blind selection over the rule language
# ---------------------------------------------------------------------------

def blind_search(start_rules, exposure, seed, max_rules=MAX_RULES, pop=32, elite=4, gens=60, ignored_records=None):
    """Only input from the world is a fitness number per candidate. `ignored_records`
    exists solely to demonstrate that defect records are not on this route."""
    rng = random.Random(seed)
    rules = list(start_rules)
    cache = {}
    evaluations = 0
    rounds = []

    def fitness(rule):
        nonlocal evaluations
        key = (rule[0], rule[1])
        if key not in cache:
            cache[key] = evaluate_rules(rules + [rule], exposure)["all"]
            evaluations += 1
        return cache[key]

    def random_rule():
        return (rng.choice(CONDITIONS), rng.choice(ACTIONS))

    def mutate(rule):
        cond, action = rule
        if rng.random() < 0.5:
            return (rng.choice(CONDITIONS), action)
        return (cond, rng.choice(ACTIONS))

    for r in range(max_rules - len(start_rules)):
        cache.clear()
        baseline = evaluate_rules(rules, exposure)["all"]
        population = [random_rule() for _ in range(pop)]
        for g in range(gens):
            population.sort(key=fitness, reverse=True)
            elites = population[:elite]
            children = list(elites)
            while len(children) < pop:
                children.append(mutate(rng.choice(elites)))
            population = children
        population.sort(key=fitness, reverse=True)
        best = population[0]
        rounds.append({"round": r + 1, "best": rule_name(best), "exposure_fitness": fitness(best),
                       "baseline": baseline, "evaluations_so_far": evaluations})
        if fitness(best) <= baseline:
            break
        rules.append(best)
    return rules, rounds, evaluations


# ---------------------------------------------------------------------------
# M3: thing-signature through collisions
# ---------------------------------------------------------------------------

def thing_signature(rules, laws, history_pairs):
    """history_pairs: list of (configuration, change). Returns fractions by
    whether a crossing happened after the change step."""
    p = RulePredictor(rules)
    tot = defaultdict(lambda: [0, 0, 0])  # passed, total, unbound
    for configuration, change in history_pairs:
        unchanged = generate_sequence(configuration, ("identity",), laws)
        changed = generate_sequence(configuration, change, laws)
        if changed is None:
            continue
        crossing_after = any(changed[t]["event"] == "cross" for t in range(CHANGE_STEP, RUN_LENGTH))
        collision_after = any(changed[t]["event"] in ("same", "cross") for t in range(CHANGE_STEP, RUN_LENGTH))
        tag = "cross_after" if crossing_after else ("same_after" if collision_after else "no_collision_after")
        tot[tag][1] += 1
        p.reset()
        for t in range(CHANGE_STEP):
            p.observe(unchanged[t]["sensory"])
        things = unchanged[CHANGE_STEP - 1]["things"]
        binding, used, ok = {}, set(), True
        for si, st in enumerate(p.states()):
            if st is None:
                ok = False
                break
            found = next((ti for ti, th in enumerate(things) if ti not in used and tuple(th) == st), None)
            if found is None:
                ok = False
                break
            binding[si] = found
            used.add(found)
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
        p.reconcile_slots(changed[CHANGE_STEP]["sensory"])
        p.previous_field = changed[CHANGE_STEP]["sensory"]
        tracking = True
        for t in range(CHANGE_STEP, RUN_LENGTH + 1):
            if t > CHANGE_STEP:
                p.observe(changed[t]["sensory"])
            st = p.states()
            for si, ti in binding.items():
                if st[si] is None or st[si] != tuple(changed[t]["things"][ti]):
                    tracking = False
                    break
            if not tracking:
                break
        if tracking:
            tot[tag][0] += 1
    out = {}
    for tag, (passed, total, unbound) in tot.items():
        bound = total - unbound
        out[tag] = {"total": total, "unbound": unbound, "passed": passed,
                    "given_bound": (passed / bound) if bound else None}
    return out


# ---------------------------------------------------------------------------
# Controls (section 6) and main
# ---------------------------------------------------------------------------

def atom_index(a_name, op, b_name):
    a, b = TERM_NAMES.index(a_name), TERM_NAMES.index(b_name)
    if a > b:
        a, b = b, a
    return ATOMS.index((a, b, op))


HAND_SAME = (("atom", atom_index("n_i", "==", "n_j")), ("swap_next_v", True))
HAND_CROSS = (("and", atom_index("n_i", "==", "c_j"), atom_index("n_j", "==", "c_i")), ("swap_next_v", True))
HAND_WALL = (("atom", atom_index("v_i", "!=", "w_i")), ("stop_i", True))


def g0_best(history_exposure, history_evaluation):
    """Returns (best overall, top5 overall, best slot-only by collision-step fidelity)."""
    best = None
    rows = []
    best_slot_only = None
    for a in enumerate_architectures():
        table = expose_lookup(a, history_exposure, NUM_CELLS)
        f, _ = evaluate(a, table, history_evaluation, NUM_CELLS)
        rows.append((f, architecture_name(a)))
        if best is None or f > best[0]:
            best = (f, architecture_name(a), a)
        if a["num_slots"] and not a["use_lookup"]:
            sp = g0_split(a, table, history_evaluation)
            if best_slot_only is None or sp["collision"] > best_slot_only[0]:
                best_slot_only = (sp["collision"], architecture_name(a), sp)
    return best, sorted(rows, reverse=True)[:5], best_slot_only


def g0_split(architecture, table, history):
    p = Predictor(architecture, NUM_CELLS, table)
    tot = defaultdict(lambda: [0, 0])
    for _, change, seq in history:
        p.reset()
        for t in range(RUN_LENGTH):
            p.observe(seq[t]["sensory"])
            if t + 1 >= FIRST_SCORED_STEP:
                ok = p.predict() == seq[t + 1]["true"]
                k = "collision" if is_collision_step(seq, t) else "other"
                tot[k][0] += ok; tot[k][1] += 1; tot["all"][0] += ok; tot["all"][1] += 1
    return {k: v[0] / v[1] for k, v in tot.items()}


def run_controls():
    laws = {"collision"}
    h = build_history(laws)
    exposure, evaluation = split_history(h)
    out = {"sequences": {"exposure": len(exposure), "evaluation": len(evaluation)},
           "rule_language_size": {"atoms": len(ATOMS), "conditions": len(CONDITIONS), "actions": len(ACTIONS),
                                  "rules": len(CONDITIONS) * len(ACTIONS)},
           "ceiling_evaluation": ceiling_split(evaluation)}
    events = defaultdict(int)
    for _, _, seq in evaluation:
        for t in range(RUN_LENGTH):
            if seq[t]["event"]:
                events[seq[t]["event"]] += 1
    out["collision_events_in_evaluation_half"] = dict(events)
    out["A0_alone"] = evaluate_rules([], evaluation)
    out["A0_plus_hand_same"] = evaluate_rules([HAND_SAME], evaluation)
    out["A0_plus_hand_same_and_cross"] = evaluate_rules([HAND_SAME, HAND_CROSS], evaluation)
    best, top5, best_slot = g0_best(exposure, evaluation)
    table = expose_lookup(best[2], exposure, NUM_CELLS)
    out["best_of_G0"] = {"architecture": best[1], "split": g0_split(best[2], table, evaluation), "top5_overall": top5}
    out["best_slot_only_in_G0_by_collision"] = {"architecture": best_slot[1], "split": best_slot[2]}
    hand = out["A0_plus_hand_same_and_cross"]
    out["expressibility_check_passes"] = hand["collision"] >= 0.9 * out["ceiling_evaluation"]["collision"]
    out["closedness_check"] = {
        "structural: best slot-only G0 on collision steps < hand - 0.1": best_slot[2]["collision"] < hand["collision"] - 0.1,
        "overall: best-of-G0 (any) overall < hand overall - 0.1": out["best_of_G0"]["split"]["all"] < hand["all"] - 0.1,
        "note": "G0's lookup memorises local sensory patterns of collisions; its collision-step figure is reported, not thresholded"}
    out["closedness_check_passes"] = all(v for k, v in out["closedness_check"].items() if k != "note")
    return out


def sha256_of_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    R = {"design": "13 Test design - construction", "code_sha256": sha256_of_file(__file__),
         "base_code_sha256": sha256_of_file(base.__file__)}
    laws = {"collision"}
    h = build_history(laws)
    exposure, evaluation = split_history(h)
    pairs_eval = [(c, ch) for c, ch, _ in evaluation]
    R["sizes"] = {"exposure": len(exposure), "evaluation": len(evaluation)}
    R["ceiling_evaluation"] = ceiling_split(evaluation)

    # M1 baselines
    R["A0"] = evaluate_rules([], evaluation)
    R["A0_hand"] = {"rules": [rule_name(HAND_SAME), rule_name(HAND_CROSS)],
                    "fitness": evaluate_rules([HAND_SAME, HAND_CROSS], evaluation)}
    best, top5, best_slot = g0_best(exposure, evaluation)
    table = expose_lookup(best[2], exposure, NUM_CELLS)
    R["S0_best_of_G0"] = {"architecture": best[1], "fitness": g0_split(best[2], table, evaluation), "top5": top5,
                          "best_slot_only_by_collision": {"architecture": best_slot[1], "fitness": best_slot[2]}}

    # C
    c_rules, c_rounds = construct([], exposure)
    R["C"] = {"rules": [rule_name(r) for r in c_rules], "rounds": c_rounds,
              "fitness": evaluate_rules(c_rules, evaluation)}

    # B
    R["B"] = []
    for seed in range(6):
        b_rules, b_rounds, evals = blind_search([], exposure, seed)
        R["B"].append({"seed": seed, "rules": [rule_name(r) for r in b_rules], "rounds": b_rounds,
                       "evaluations": evals, "fitness": evaluate_rules(b_rules, evaluation)})

    # M3
    R["M3_A0"] = thing_signature([], laws, pairs_eval)
    R["M3_A0_C"] = thing_signature(c_rules, laws, pairs_eval)
    R["M3_A0_hand"] = thing_signature([HAND_SAME, HAND_CROSS], laws, pairs_eval)

    # M4 scramble
    def scramble(V, N, seed=0):
        rng = random.Random(seed)
        trues = [rec[3] for rec in V]
        rng.shuffle(trues)
        V2 = [(rec[0], rec[1], rec[2], tr) for rec, tr in zip(V, trues)]
        return V2, N
    s_rules, s_rounds = construct([], exposure, transform=scramble)
    R["M4_scrambled_C"] = {"rules": [rule_name(r) for r in s_rules], "rounds": s_rounds,
                           "fitness": evaluate_rules(s_rules, evaluation)}
    b_rules_again, _, _ = blind_search([], exposure, 0, ignored_records="scrambled records passed and ignored")
    R["M4_B_seed0_with_scrambled_records_passed"] = {"rules": [rule_name(r) for r in b_rules_again],
                                                     "identical_to_B_seed0": [rule_name(r) for r in b_rules_again] == R["B"][0]["rules"]}

    # M5 recoding
    def reverse_order(V, N):
        return list(reversed(V)), list(reversed(N))
    def relabel(V, N):
        f = lambda rec: ((rec[0][1], rec[0][0]), frozenset({1 - i for i in rec[1]}), rec[2], rec[3])
        return [f(r) for r in V], [f(r) for r in N]
    r1, _ = construct([], exposure, transform=reverse_order)
    r2, _ = construct([], exposure, transform=relabel)
    R["M5_recoding"] = {"reversed_order_rules": [rule_name(r) for r in r1],
                        "relabelled_rules": [rule_name(r) for r in r2],
                        "reversed_identical": [rule_name(r) for r in r1] == R["C"]["rules"],
                        "relabelled_identical": [rule_name(r) for r in r2] == R["C"]["rules"]}

    # M6 ablation
    e1, e1_rounds = construct([], exposure, transform=lambda V, N: ([], N))
    e2, e2_rounds = construct([], exposure, transform=lambda V, N: ([(a, b, c, c) for a, b, c, d in V], N))
    R["M6_ablation"] = {"empty_V_rules": [rule_name(r) for r in e1], "empty_V_rounds": e1_rounds,
                        "no_content_V_rules": [rule_name(r) for r in e2], "no_content_V_rounds": e2_rounds}

    # Phase 2
    laws2 = {"collision", "sticky_wall"}
    h2 = build_history(laws2)
    exposure2, evaluation2 = split_history(h2)
    R["phase2"] = {"ceiling_evaluation": ceiling_split(evaluation2),
                   "A0_plus_phase1_rules": evaluate_rules(c_rules, evaluation2)}
    p2_rules, p2_rounds = construct(c_rules, exposure2, max_rules=len(c_rules) + 2)
    R["phase2"]["C_continued"] = {"rules": [rule_name(r) for r in p2_rules], "rounds": p2_rounds,
                                  "fitness": evaluate_rules(p2_rules, evaluation2),
                                  "fitness_on_collision_only_world": evaluate_rules(p2_rules, evaluation)}
    wall_steps = defaultdict(lambda: [0, 0])
    p = RulePredictor(p2_rules)
    for _, _, seq in evaluation2:
        p.reset()
        for t in range(RUN_LENGTH):
            p.observe(seq[t]["sensory"])
            if t + 1 >= FIRST_SCORED_STEP and seq[t]["event"] == "wall_stop":
                wall_steps["with_phase2_rules"][0] += p.predict() == seq[t + 1]["true"]; wall_steps["with_phase2_rules"][1] += 1
    p = RulePredictor(c_rules)
    for _, _, seq in evaluation2:
        p.reset()
        for t in range(RUN_LENGTH):
            p.observe(seq[t]["sensory"])
            if t + 1 >= FIRST_SCORED_STEP and seq[t]["event"] == "wall_stop":
                wall_steps["phase1_rules_only"][0] += p.predict() == seq[t + 1]["true"]; wall_steps["phase1_rules_only"][1] += 1
    R["phase2"]["wall_stop_steps"] = {k: v[0] / v[1] for k, v in wall_steps.items()}

    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(R, f, indent=1, default=str)
    return R


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--controls":
        print(json.dumps(run_controls(), indent=1, default=str))
    else:
        R = main(sys.argv[1] if len(sys.argv) > 1 else ".")
        print(json.dumps({"A0": R["A0"], "C": R["C"]["fitness"], "C_rules": R["C"]["rules"],
                          "S0": R["S0_best_of_G0"]["fitness"], "B_fitness": [b["fitness"]["all"] for b in R["B"]]},
                         indent=1, default=str))
