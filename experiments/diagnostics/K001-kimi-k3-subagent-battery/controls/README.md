# controls/ — the Opus-5 control side of the worker battery

One directory per task that `battery/evaluation.json` marks `opus_control: true`.
Each holds the prompt the control is given, a sandbox populated exactly as the
battery harness populates a worker sandbox for the same task, and the place the
control's final answer goes.

```
controls/
  INDEX.json              one row per control: id, family, prompt, sandbox,
                          expected outputs, verify command
  README.md               this file
  <task_id>/
    PROMPT.md             the task prompt verbatim + the fixed operating note
    sandbox/              populated by kimi_agent.Sandbox.populate
    FINAL.md              written by the control: its final answer text
  build/                  the three generators, plus the snapshots and the
                          population diff they produced
```

## 1. What is in a control sandbox, and why it is trustworthy

`build/populate.py` imports `kimi_agent` and calls
`kimi_agent.Sandbox(root).populate(task["repo_root"], task["context_paths"])` —
the harness's own method, not a reimplementation. So the control sandbox inherits,
by construction, the same `repo_root` (`battery/material`), the same declared
`context_paths` in the same order, the same `SANDBOX_EXCLUDES`
(`.env`, `.env.local`, `.git`, `__pycache__`, `.venv`, `venv`, `.mypy_cache`,
`.pytest_cache`), the same `*.pyc` drop, and the same `symlinks=False`.

Three checks were run and are recorded:

1. **Against the worker sandboxes.** `build/compare.py` diffs each control sandbox
   against `runs/<task_id>/sandbox` file-by-file on sha256. Results in
   `build/compare.json`. For every task whose worker run had already been
   populated, the two file lists and every sha256 matched exactly; the only
   entries either side did not share were files the worker itself wrote after
   population.
2. **Against the corpus manifest.** Every file in all fifteen sandboxes appears in
   `battery/MANIFEST.sha256` at the identical hash. No file in a control sandbox
   is absent from the manifest, and none differs from it.
3. **Nothing withheld leaked in.** No path under `battery/reference/` is present in
   any control sandbox, and no `.env`, `.git`, `__pycache__` or `.pyc` survived.

The sandboxes were re-hashed after verification and are byte-identical to their
population-time state.

## 2. PROMPT.md

Each `PROMPT.md` is the task's `prompt` field from `battery/tasks.json`,
**verbatim and entire** — body, TOOLING paragraph, HOUSE RULES paragraph, nothing
added inside it and nothing removed. `INDEX.json` carries `prompt_sha256` and
`prompt_chars` for the prompt string so verbatimness can be re-checked:

```
python3 -c "import json,hashlib; t={x['id']:x for x in json.load(open('battery/tasks.json'))}; \
  print(hashlib.sha256(t['a-01-types']['prompt'].encode()).hexdigest())"
```

and the file begins with exactly that string.

Below the prompt sits a horizontal rule and one **OPERATING NOTE**, identical in
wording across all fifteen controls; the only tokens that differ between them are
the two absolute paths it names. It states the sandbox path, that all reads and
writes happen inside it, the `python3`-only command rule (`python3 -m unittest`,
`python3 -m pytest`, `python3 -c`, `python3 <file>.py`, plus `python3 run_tests.py`
where the sandbox provides that helper), that no file outside the sandbox may be
read or written apart from the final answer file, where the final answer goes, and
that the answer must end with a section headed **"What I could not determine"**.
That last requirement mirrors the prompt's own house rule — *say "unresolved", or
"I could not determine this and here is why", rather than inventing a finding* —
and the closing self-report family B asks for in its own words ("which clauses you
could not cover and why") and `d-04` in its own ("every figure … you left out and
why").

The note names no other model, no comparison, no reference role, and no part of
`rubric.md` or `evaluation.json`.

**One residual signal, stated rather than hidden.** The absolute paths run through
a directory named `kimi/`, because that is where this work was required to live.
A control can therefore see that directory name in its own sandbox path. Nothing
in `PROMPT.md` says what it means, but the judge should know the signal exists
rather than assume it does not.

## 3. Running a control

Spawn one Opus 5 subagent per task. Give it `PROMPT.md` and nothing else: not
`evaluation.json`, not anything under `battery/reference/`, not `rubric.md`, not
this file. Do not tell it a comparison is happening. Do not answer its questions —
the prompt says the worker cannot ask questions, and the control is under the same
rule. Record its final message to `FINAL.md` and leave every file it wrote in
place inside `sandbox/`.

## 4. Pairing a control with its worker run

For one `task_id`, the judge assembles:

| side | prompt | sandbox | final answer | files written |
|---|---|---|---|---|
| worker | `battery/tasks.json` → `prompt` | `runs/<task_id>/sandbox` | `runs/<task_id>/result.json` → final text, and `transcript.jsonl` | `result.json` → the change list, each with sha256 |
| control | `controls/<task_id>/PROMPT.md` (same string) | `controls/<task_id>/sandbox` | `controls/<task_id>/FINAL.md` | diff `sandbox/` against `build/snapshots.json` |

The pairing is sound because both sandboxes were cut from the same frozen
`battery/material` through the same `populate`, and `build/compare.json` records
that they were identical before either side wrote anything.

**Before judging**, diff both sandboxes against `battery/MANIFEST.sha256`:

* every file that still matches the manifest is untouched material;
* every file that differs or is new is that side's own output — that is the change
  list the judge reads;
* a *modified* file under `src/` on either side is the "edited a file it was told
  not to edit" finding, recorded and not silently fixed.

`build/snapshots.json` gives the control's population-time hash for every file, so
the control's change list can be derived without re-running `populate`.

Then apply `rubric.md` §2 (the judge instruction and its verdict schema) and the
per-family rules in §3, with `evaluation.json[task_id]` as the index. The control
is a reference, not a ceiling: rubric.md requires the judge to reproduce the
control's claims too, and to record in `overall_note` any control claim it could
not reproduce.

## 5. Which tasks are here

Fifteen, which is every task carrying `opus_control: true`: `a-01` … `a-06`
(code review), `c-01` … `c-04` (implementation), `d-01` … `d-04` (document work),
and `f-02-commit-tree`. Both `battery/README.md` §4 and `rubric.md` §1 introduce
this same list with the word "Ten"; the list itself, and `evaluation.json`, are
the authority, and the flag is set on fifteen task ids.

## 6. Regenerating

```
cd scratchpad/kimi
python3 controls/build/populate.py       # sandboxes + build/snapshots.json
python3 controls/build/write_prompts.py  # PROMPT.md + build/prompt-hashes.json
python3 controls/build/write_index.py    # INDEX.json
python3 controls/build/compare.py        # build/compare.json vs runs/
python3 controls/build/verify.py         # the per-sandbox verification table
```

`populate.py` deletes and rebuilds each `sandbox/`, so do not run it after a
control has started work.
