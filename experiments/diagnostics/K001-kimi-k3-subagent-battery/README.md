# K001 — Kimi K3 as a subagent: the battery, its runs, its controls

Published under **REC-20260914-AC**. This directory is the evidence; the deliverable that reads it
is [`docs/reviews/kimi-k3-subagent-2026-09-14/REPORT.md`](../../../docs/reviews/kimi-k3-subagent-2026-09-14/REPORT.md).
The harness that produced every run is [`tools/kimi_harness/`](../../../tools/kimi_harness/).

## What the study was

Session ruling 11, on explicit owner instruction, deployed **Kimi K3** (endpoint `ollama/kimi-k3`
via the Ollama cloud API) as roughly half of this session's subagents, for a bounded experiment of
at least twenty tasks, **as a worker and not as a study subject**, with the results feeding a
strengths-and-weaknesses report. That is what this is. It is an *operations* record: it says what a
worker did on this project's own work, so that work can be routed. It is **not** a finding about
Mini, about FW5, or about any hypothesis in `PURPOSE.md`; it defines no metric, publishes no score
and ranks nothing (`battery/README.md` §5). Ruling 11 records it as a declared deviation from the
Opus-only subagent rule in `CLAUDE.md`, authorised by that rule's author, with **Opus 5 remaining
the verifier of every Kimi output that touches the record**. Ruling 16 then made Kimi K3 the default
worker for mechanical and scripted tasks, which is why the harness is published as an instrument
rather than discarded as a scratch script. Both rulings, verbatim, are in
[`docs/reviews/session-rulings-2026-09-14.md`](../../../docs/reviews/session-rulings-2026-09-14.md).

The battery is **twenty-six tasks**: twenty-five across six families of this project's real work —
A code review (6), B test writing (4), C implementation (4), D document work (4), E adversarial /
verification (4), F data / tool use (3) — plus `b-004`, the harness's own packed-context self-check,
which belongs to no family. Every task was phrased as the orchestrator would phrase it to an Opus
subagent, and every task ran against a **frozen corpus**, never the live repository.

## The passes

| | pass 1 (`runs/`) | pass 2 (`runs-pass2/`) | pass 3 (`runs-pass3/`) | pass 4 (`runs-pass4/`, `runs-pass4-retry/`) |
|---|---|---|---|---|
| dispatched | 26, plus a live smoke run | 17 — every pass-1 non-COMPLETE | 4 — every pass-2 `HTTP_500` | 14 ceiling losses, plus `b-02-seats-fixed`; one retry |
| per-turn `max_tokens` | 32,768 | 8,192 | 8,192 | 24,576 |
| transport | `/v1` (OpenAI-compatible) | `/v1` | `/v1` | **native `/api/chat`** |
| task file | `battery/tasks.json` | `battery/tasks-pass2.json` | `battery/tasks-pass3.json` | `battery/tasks-pass4.json`, `-b02`, `-c03` |

Pass 1 lost twelve runs to a **300 s gateway wall** on the Ollama host (rulings 13 and 14: five
closes in a 183 ms band across two model families and two client processes — a host limit, not a
client timeout). Passes 2 and 3 cut the per-turn budget to 8,192 to stay inside it, and hit the
opposite boundary: this model's native reasoning is billed against the per-turn budget, so sixteen
runs spent **the entire 8,192 tokens on reasoning** and returned no text, no tool call and no file.
Pass 4 re-ran those fourteen tasks on the raised budget and the ported transport; all fourteen then
delivered every declared output.

`prod-runs/` and `prod-runs-smoke/` are not battery runs: they are the first **production** tasks
given to Kimi under ruling 16, with their task specs in `prod-tasks/`. `prod-runs-w3/` is the
wave-3 drafting battery, which was **still running** when this checkpoint was published — see
"What is not here" below.

## The harness fix, and the transport port

Two infrastructure changes happened *because of* what the battery showed, and both are part of the
record rather than background:

* **The labelling defect.** The harness originally ended its loop on any assistant turn with no
  tool call and recorded that as `COMPLETE`. Sixteen runs that had spent their whole turn budget on
  reasoning and written nothing were therefore labelled as having done the work. The status rules
  were split — `COMPLETE` now requires both that the final turn finished on its own *and* that every
  declared `expected_output` exists — and `INCOMPLETE_TURN`, `NO_DELIVERABLE` and `ITERATION_CAP`
  each name a distinct way a run stopped short. The recorded runs were **not rewritten**:
  [`reclassify.py`](../../../tools/kimi_harness/reclassify.py) re-reads them under the new rules and
  writes [`RUNS-RECLASSIFIED.md`](../../../docs/reviews/kimi-k3-subagent-2026-09-14/RUNS-RECLASSIFIED.md),
  one row per (pass, task), recorded label beside reclassified label.
* **The transport port.** `/v1` accepts `reasoning_effort` and ignores it. Ollama's native
  `/api/chat` honours `think` — measured in
  [`PROBE-REASONING.md`](../../../tools/kimi_harness/PROBE-REASONING.md) — so the loop was ported to
  the native surface with `/v1` still selectable per task, one translation layer, and a single
  recorded fallback that is refused once a tool call has been made. Pass 4 ran there.

## The controls and the judges

`controls/` holds **fifteen Opus controls** — all six family-A tasks, all four of C, all four of D,
and `f-02-commit-tree` — each an Opus 5 subagent given the *same prompt against the same frozen
bytes*, with `INDEX.json` pinning each prompt's sha256 and naming the Kimi run it pairs with. Ruling
15 records all fifteen complete, and records what the six family-A controls found: ten blockers the
original wave-0 review had missed.

Judging was **seven separate Opus 5 subagents** — one per family, plus one for pass 4 — instructed
to re-execute what they certify rather than read it (`battery/rubric.md` §2), and to name what they
did *not* run. Their reports are
[`docs/reviews/kimi-k3-subagent-2026-09-14/judgements/`](../../../docs/reviews/kimi-k3-subagent-2026-09-14/judgements/):
`family-A.md` … `family-F.md` and `pass4.md`. A Kimi judge of Kimi would not have been independent
(ruling 16), so none was used.

## What is here

```
battery/          tasks.json and the four pass task files, evaluation.json, README.md, rubric.md,
                  MANIFEST.sha256 (432 files), reference/ (answer keys, withheld tests, gold
                  paragraphs — judge-only, never a context path)
prod-tasks/       the task specs for prod-runs/ and prod-runs-w3/
runs/ …           per run: result.json, and the directories the worker itself wrote
                  (out/, check/, probe/, review/, smoke/, _scratch/); each run set's SUMMARY.md
controls/         INDEX.json, README.md, and per control FINAL.md, PROMPT.md and its own written
                  directories
TRANSCRIPTS.md    the index of all 81 transcripts, which are not published
```

Run counts staged: `runs/` 27, `runs-pass2/` 17, `runs-pass3/` 4, `runs-pass4/` 15,
`runs-pass4-retry/` 1, `prod-runs/` 13, `prod-runs-smoke/` 1, `prod-runs-w3/` 2.

## What is not here, and why

* **`battery/material/` — the frozen corpus itself.** It is a read-only copy of 432 files from this
  repository and from the wave-0/wave-1 staging clone, made at battery build time so that the worker
  run and its Opus control would see identical bytes while other agents edited the live tree. Every
  one of those 432 files is pinned by name and sha256 in `battery/MANIFEST.sha256`, so the corpus is
  **reproducible from the manifest** against this repository's history; copying 4.2 MB of duplicated
  repository files into the repository would add nothing the manifest does not already fix.
  `battery/build/` (its generator) is likewise omitted.
* **The transcripts.** 81 files, 444 MB — larger than this entire working tree. `TRANSCRIPTS.md`
  records every one by path, byte size, line count and sha256, states that they stay in the
  ephemeral session scratchpad, and gives the total. The publishing instruction admitted the judged
  battery transcripts if those alone came in under 80 MB; they are 246 MB, so none is published.
* **The sandboxes' copies of `src/`, `tests/`, `docs/` and material.** A sandbox is a copy of the
  declared context paths, and some workers made scoped edits inside those copies. Those are modified
  copies of repository files, not worker deliverables, and they are not republished here; every
  change a worker made is listed in that run's `result.json` with its path, sha256, byte size and
  whether it was added, modified or removed.
* **`prod-runs-w3/w3-audits`.** The wave-3 battery was still running at
  **2026-09-14T16:33:03+00:00**, the instant this publisher looked. `w3-trial` and `w3-report` had
  finished and are here; `w3-audits` had not and has no `result.json`, so it has no record here, and
  `prod-runs-w3/` has no `SUMMARY.md` because `run_battery.py` writes one when the whole battery
  ends. Those records belong to the next checkpoint, not to a later edit of this one.
* **`prod-runs/SUMMARY.md` covers only the last launch.** `run_battery.py` rewrites `SUMMARY.md` per
  launch, and the production tasks were dispatched in six launches, so that file describes `p6`
  alone. The other twelve production runs are complete in their own `result.json`.

Three small additions were made beyond the paths the publishing instruction enumerated, each because
omitting it would have left a published record unreadable or unverifiable: the workers' own
`probe/`, `review/`, `smoke/` and `_scratch/` directories alongside `out/` and `check/` (all four are
worker-authored, none is a copy of repository material, and `probe/` is where four family-A runs put
everything they produced); `controls/PROMPT.md` and `controls/README.md` (without the prompt text,
`INDEX.json`'s `prompt_sha256` pins nothing a reader can check); and `prod-tasks/` plus
`battery/tasks-smoke-native.json` (the task specs of published run records). Together they are under
a megabyte.

## What this record cannot establish

Section 7 of the report is the full statement; the short form is that every sentence about the
worker is about **these occasions on this corpus**, not about a model in general. There is no
control for prompt phrasing, no repetition of a task under identical conditions, no metric and no
ranking. Fifteen of the twenty-six tasks had no genuinely complete run before pass 4, and most of
what looks like failure in families A, B and C was the per-turn ceiling rather than the worker's
judgement — which is exactly why the reclassification exists and why pass 4 was run. The routing
table in the report is a **decision aid for this orchestrator**, not a result.
