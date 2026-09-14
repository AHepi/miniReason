# kimi-k3 worker battery — design, pairing and operation

Twenty-five tasks across six families of this project's real work, plus the
harness's own packed-context exercise. The question the battery answers is not
"how good is kimi-k3" in the abstract. It is: **if the orchestrator hands this
piece of the miniReason loop to kimi-k3 instead of to an Opus 5 subagent, what
comes back, and where does it differ?** Every task is phrased exactly as the
orchestrator would phrase it to an Opus subagent — same house rules, same exact
file paths, same verification commands, no metrics, no scalar meters — so the two
transcripts are comparable sentence for sentence.

kimi-k3 here is a **worker**, not a study subject. Nothing produced by a run is a
finding about any model family, and nothing in `runs/` may be published as one.
The battery's own output is evidence about a tool, in the same sense that
`docs/lessons/operations.md` records evidence about an instrument.

---

## 1. Layout

```
battery/
  tasks.json          26 TaskSpec objects, exactly the fields kimi_agent.TaskSpec declares
  evaluation.json     family, opus_control, timebox and the structured evaluation, keyed by task id
  rubric.md           the scoring rubric, the judge instruction and the verdict schema
  README.md           this file
  MANIFEST.sha256     sha256 of every file under material/, 432 files
  material/           the frozen corpus every sandbox is cut from      <- workers see this
  reference/          answer keys, withheld test files, gold paragraphs <- judge only
  build/              the generator for tasks.json and the manifest tool
```

**`material/` is a frozen corpus, not a live tree.** It was copied read-only from
`/home/user/miniReason` and from the wave-0/wave-1 staging clone at
`scratchpad/loop-impl/repo` at battery build time. Nothing in the battery ever
reads the live repository during a run, and no task can touch it: every task
declares `repo_root` = the absolute path of `battery/material`, and the harness
copies only the declared `context_paths` out of that root into a fresh sandbox.
The live repository is READ-ONLY for this work and was never written to.

Freezing matters for fairness and for reproducibility. The staging clone is being
edited by other agents while this battery runs; if a task read it live, the worker
run and the Opus control run would see different bytes and the comparison would be
worthless. `MANIFEST.sha256` pins what both of them saw; `python3
build/manifest.py --check` says whether the corpus has moved.

**`reference/` is never a `context_path`.** It holds the answer keys, the project's
own test files for the wave-1 modules under test in family B, the two gold receipt
paragraphs, the wave-0 adversarial review, and the withheld `audit.json` files.
Copying any of it into a sandbox destroys the task it belongs to.

### Regenerating

```
cd battery
python3 build/make_battery.py     # rewrites tasks.json and evaluation.json
python3 build/manifest.py         # rewrites MANIFEST.sha256
```

### Running

```
cd scratchpad/kimi
python3 run_battery.py --tasks battery/tasks.json --runs-dir runs --workers 8
python3 run_battery.py --tasks battery/tasks.json --only c-04-decide   # one task
```

---

## 2. The sandbox contract every prompt assumes

Each task's sandbox is a small, self-consistent mini-repository:

```
run_tests.py                      helper: puts the sandbox root and src/ on sys.path
src/minireason/loop/*.py          the frozen wave-0 / wave-1 modules the task needs
src/minireason/, src/deepreason_core/   the import closure those modules need
tests/loop/                       empty but importable; the worker's tests go here
docs/, design/, notes/, evidence/, factsheets/, staging/, experiments/
```

`run_command` in this harness accepts only `python3` forms, so there is no shell,
no `git` and no way to set `PYTHONPATH` on a command line. That is why
`run_tests.py` exists and why every code task's prompt names it:

```
python3 run_tests.py tests.loop.test_<name>
```

This was verified end to end at build time: four task sandboxes were populated
through `kimi_agent.Sandbox.populate`, a probe test was written into each, and
`run_tests.py` ran it green. All twelve loop modules import in a populated sandbox.

The wave-0 test files that ship as house-style exemplars live at
`docs/examples/test_custody_example.py` and `docs/examples/test_standard_example.py`,
**not** under `tests/`, so that test discovery never picks them up: they assert
repository-layout facts a sandbox does not reproduce, and the prompts say so.

Two tasks (`e-01-refute`, `f-01-c001-profile`) hold more than 200 files, which is
where the harness's own file-list rendering truncates. Their prompts say the list is
truncated, describe the directory layout explicitly, and tell the worker to use
`list_dir`, `grep` and an aggregation script.

### Reading budget

Every task runs in `tools` mode, where nothing is packed into the prompt — the
worker reads what it chooses. The budget that matters is therefore what a task
*directs* the worker to read, and every task stays under roughly 80k tokens of
directed reading: one loop module (7-80 KB) plus the interface note (30 KB) plus
one or two design slices (4-26 KB), or one document set. The bulk of a code
sandbox is import-closure runtime the worker never has to open. Four tasks are also
small enough to run in `packed` mode unchanged if the harness ever falls back:
`d-01`, `d-03`, `d-04` (16-22k tokens) and `f-03` (12k).

---

## 3. The six families, and why each is grounded the way it is

| family | tasks | what it measures | ground truth |
|---|---|---|---|
| A. CODE REVIEW | 6 | adversarial reading of a published seam: does the worker execute a probe or recite a pattern | Opus control on identical bytes, with `REVIEW-WAVE0.md` as a staleness anchor |
| B. TEST WRITING | 4 | can it write an oracle that would actually fail | the suite runs green; clause coverage; two judge-chosen mutations must turn it red |
| C. IMPLEMENTATION | 4 | can it build a wave-2 module from an interface it cannot negotiate | Opus control; each side's test file run against the other's module |
| D. DOCUMENT WORK | 4 | house voice, factual discipline, and the refusals the house imposes | two gold published paragraphs, two fact sheets, Opus control on all four |
| E. ADVERSARIAL / VERIFICATION | 4 | will it refute, and will it refuse to invent a refutation | three executed answer keys and one lens-1 table |
| F. DATA / TOOL USE | 3 | does it aggregate with a script instead of reading 240 files | two withheld `audit.json` files and an executed commit/tree join |

### A — code review (6 tasks: `a-01` … `a-06`)

One wave-0 module each: types, contracts, standard, custody, receipts, publish.
Every finding must be executed inside the sandbox and reported with the probe
output verbatim; a "Tried, and could not break" section is required, because an
attack that fails is evidence about the module.

**Grounding deviation, and why.** The orchestrator's plan was to score family A by
overlap with `REVIEW-WAVE0.md`. That is no longer sound, and the battery says so
rather than pretending otherwise. While the battery was being built, the wave-0
fixer was applying that review's own repairs to the staging clone. Fifteen of its
findings were probed against the frozen snapshot at build time; eleven are
**already repaired**, two are partly addressed, and two remain live. The evidence
is in `reference/A-CODE-staleness-note.md`, one row per finding with the probe and
its result. Scoring against a stale document would punish a correct reading of the
current bytes and reward recitation. So family A carries an **Opus control on the
same frozen bytes**, and `REVIEW-WAVE0.md` is used in two narrower ways: a finding
that reproduces a still-live row is a confirmed hit whoever found it, and a finding
that restates a repaired row is a **false positive, named as such**. That second
use is the battery's sharpest single test of whether a worker read the code.

### B — test writing (4 tasks: `b-01` … `b-04`)

Wave-1 modules: surface, seats, obligations, steps. The project's own test file for
each is withheld (`reference/withheld-test_*.py`) and the sandbox has none, so the
worker writes from the module, its docstrings and the design's acceptance clauses,
which are quoted verbatim into the prompt. Three gates: the suite runs green;
an Opus judge maps tests to acceptance clauses; the judge applies two mutations —
one inverting a guard condition, one weakening a refusal to a silent pass — and
records whether the suite turns red. A suite that passes every mutation has pinned
nothing.

The prompt forbids editing `src/`: if a test fails because the module is wrong, the
test stays red and the worker says so. That follows `docs/lessons/operations.md` on
E028 — a failing test that names a real defect is better evidence than a passing
suite bought by weakening the oracle — and it is itself a thing worth measuring.

### C — implementation (4 tasks: `c-01` … `c-04`)

W2-PACKS, W2-ROLES, W2-MARKPREP, W2-DECIDE, each from its design entry (quoted
verbatim: purpose, public interface, depends_on, acceptance), the wave-0 interface
note and the eight wave-1 integration decisions. None of the four exists yet, in
the clone or anywhere; the worker is the author. `opus_control` is true for all
four, and the conformance gate runs each side's test file against the other side's
module wherever the interfaces agree — which also measures how closely each side
held to the declared `public_interface`.

`types.py` may not be edited in the sandbox, so new failure codes are declared in a
module-level `NEW_CODES` tuple instead; the prompt says which table each belongs
in. That mirrors wave-1 integration decision 6.

### D — document work (4 tasks: `d-01` … `d-04`)

1. `d-01-receipt` — a publication-outcome receipt from `factsheets/D-DOC-1-fact-sheet.md`.
   The gold is the paragraph actually published as REC-20260914-V's publication
   outcome (`reference/D-DOC-1-gold.md`, 4,879 characters), so verbosity has a
   yardstick rather than an opinion.
2. `d-02-operator-page` — the W1-STEPS section of the operator page. Scored partly
   mechanically: the judge extracts every failure code `steps.py` can raise and
   diffs it against the codes the page names, in both directions.
3. `d-03-decision-record` — design section 5 condensed to one decision-record
   paragraph **with no count-shaped clause**. The design's clause 4 is a set
   identity over `(cell, register, mark)` triples and clause 5 is a declared budget;
   writing either as a count replaces the rule with a meter and fails the task. The
   judge greps for count-shaped language and reports every hit.
4. `d-04-f002-outcome` — the F002 closing-receipt outcome paragraph from the results
   table and `f001-unresolved-coordinates.txt`. The gold is REC-20260914-X's real
   closing paragraph.

Each fact sheet states the constraints the house imposes on that paragraph in the
house's own words, so a worker that has never read this ledger can still meet them —
and a worker that ignores them has ignored an instruction, not missed a convention.

### E — adversarial / verification (4 tasks)

1. `e-01-refute` — three named claims from section 4 of the session orchestration
   report. **One is refutable and two are not.** The refutable one attributes all
   twenty `INCOMPLETE_GENERATION` records of C001 occurrence-01 to the
   `deepseek-flash` × `fcl` cell; the twentieth is `ollama-glm-5.3 / fcl / control /
   rep2`, PARTIAL at `finish_reason: length` and 32,768 completion tokens. Declaring
   either of the other two refuted is an incorrect claim, not a miss. Key computed
   by execution at build time: `reference/E-ADV-1-key.md`.
2. `e-02-metric-creep` — every number in `standard.py` and `types.py` that reaches
   adjudication, a reading's standing, a rendered artifact, a docstring promise or a
   test oracle, classified A / F / C. Scored against the lens-1 table of
   `REVIEW-WAVE0.md`, **matched on module-plus-symbol and never on line number**,
   with repaired rows removed from the denominator and named.
3. `e-03-fw5-citations` — twenty FW5 line citations in the A001 staging document,
   listed explicitly in the prompt so the set is deterministic. **Nineteen verify;
   one does not** — `FW5:133` at `staging/a001-STAGING.md:109` points at an empty
   line. Three are deliberately awkward and none of the three is a defect; the most
   likely false positive (`FW5:210`, whose paragraph is titled Non-circular
   dependence but which does carry the contrast requirement) is called out in the
   key. Computed by slicing both files: `reference/E-ADV-3-key.md`.
4. `e-04-f001-classes` — classify every unresolved F001 coordinate as ceiling,
   timeout or blocked, after deriving the planned set of 89 from the arms and the
   node sequence. Ground truth is the project's own
   `f001-unresolved-coordinates.txt`.

### F — data / tool use (3 tasks)

1. `f-01-c001-profile` — the failure profile of C001 occurrence-01 across 240
   receipts, by code and per family. Two code-bearing fields, not one; the
   endpoint-slug-to-family mapping must be derived from `endpoints.json`. Ground
   truth is the withheld `audit.json` plus the executed key.
2. `f-02-commit-tree` — every commit and tree identity published in REC-20260914-U
   and REC-20260914-X, joined against a frozen `git log` extract. **Every pair
   verifies**, so the task measures whether a clean result is reported cleanly.
   *Deviation:* the orchestrator's phrasing assumed `VERIFIED <commit> TREE <tree>`
   lines in REC-20260914-U; that receipt predates the line and writes its identities
   in prose, and `run_command` allows no `git`, so the task names both receipts and
   supplies the log as `evidence/git-log-branch.txt` (`git log --format='%H %T %h %ad
   %an %s' --date=iso-strict 40bd5de..HEAD`, 122 rows, taken read-only).
3. `f-03-occ02-usage` — the usage and envelope profile of C001 occurrence-02 over 20
   receipts. The in-budget member of the family, and the one that checks whether a
   worker reports a range rather than reaching for a mean.

### The extra task: `b-004`

The harness's own packed-context fallback exercise, carried over unchanged from the
harness build. Its `repo_root` is the live repository and it belongs to no family;
`evaluation.json` marks it `G. HARNESS SELF-CHECK`. Its id resembles family B's
`b-01` … `b-04` only by coincidence of the harness's original numbering.

---

## 4. The pairing

Ten tasks carry `opus_control: true`: all six of family A, all four of family C, all
four of family D — and `f-02-commit-tree`. (The remaining fifteen have an executed
answer key or a withheld project artifact, which is a stronger and cheaper
reference than a control.)

An Opus control is run as an **Opus 5 subagent given the task's `prompt` verbatim**,
in a sandbox populated from the same `repo_root` and the same `context_paths`, with
the same five tools and the same `python3`-only command rule. It is not given the
task's evaluation entry, the reference directory, or any hint that a comparison is
happening. Both sides' sandboxes are diffed against `MANIFEST.sha256` before the
judge sees anything.

`rubric.md` carries the Opus-control instruction and the judge instruction in full,
including the required verdict schema.

---

## 5. What this battery deliberately does not do

* It produces no score, no rank and no aggregate figure across tasks. A per-task
  verdict is a set of named claims, not a number, and the summary the orchestrator
  writes is prose about strengths and weaknesses.
* It makes no claim about kimi-k3 beyond these twenty-five occasions on this
  corpus. A task is one occasion; two tasks in a family are two occasions.
* It never spends a provider call from inside a sandbox: there is no network, and
  the harness strips every credential environment variable from every subprocess it
  runs.
* No credential, and no fragment of one, appears anywhere in `material/`,
  `reference/` or `tasks.json`. `.env` is on the harness's own never-copy list and
  is not referenced by any task.

## 6. Tasks considered and left out

* **A wave-1 adversarial review scored by overlap.** There is no wave-1 review of
  record, so a sixth review family would have had no reference but a control, and
  family A already carries six controls. Left out rather than doubled.
* **An end-to-end dry-run task (W6-DRYRUN).** It depends on W5-DRIVER, which does
  not exist; there is nothing to run and no ground truth.
* **A task over `docs/DECISION_LEDGER.md` as a whole.** The file is 335 KB; only the
  four receipts a task actually needs are staged, each as its own file, per the
  instruction not to copy more of the ledger than needed.
* **A "recompute the C001 occurrence-02 audit" task.** Its `audit.json` records no
  failure at all, so the task reduced to copying zeroes; `f-03` asks for the usage
  and envelope profile instead, which the records do settle and the audit
  independently confirms.
* **Anything requiring `git` inside a sandbox.** The tool layer allows only
  `python3`, so every git-shaped question is answered against a frozen extract.
