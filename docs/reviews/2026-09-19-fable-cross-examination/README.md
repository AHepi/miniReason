# 2026-09-19 — FW5 rewrite, two frozen experiments, and their adversarial cross-examination

What this folder is: a self-contained review thread from one session (Claude Code, 2026-09-18/19), kept whole so its numbered files can be cited from the lessons. It is not part of the H-series experiments and does not use the Mini harness. The user's instruction for the session was to read only PURPOSE.md and FW5, form a view without the rest of the repository, and test it.

| File | What it is |
|---|---|
| `10 Claude Fable Semantics - standalone theory.md` | A standalone rewrite of FW5's semantics around kinds as edit-signatures. Not FW5; under revision (see file 15 §G). |
| `11`, `12`, `12a–c` | Experiment 1 (do kinds emerge from selection): frozen design, results, code, freeze record, raw results. Frozen; not edited. |
| `13`, `14`, `14a–c` | Experiment 2 (construction): the same. Frozen; not edited. |
| `15 Adversarial cross-examination - findings and adjudication.md` | Every witness finding with a verdict; §0 the failure modes of the cross-examination itself; §E the audits of the adjudication; §F the second witness; §G the consolidated revision list for file 10. |
| `16`, `17` | Errata: what each experiment is still allowed to claim, sentence by sentence with its concession, plus post-freeze diagnostics labelled as such. |
| `15b Adjudication supplement - after publication.md` | Everything added to files 15, 16, 17 and the story after the folder was first published: the last DeepSeek items, the whole second witness on the experiments, the corrected timing account, the consolidated revision list's amendments. The published files are unchanged. |
| `20 Claude Fable Semantics - revised standalone theory.md` | The semantics revised against the whole consolidated list (file 15 §G as amended). Standalone, no history in it. Not yet cross-examined. |
| `20a Revision ledger - where each item landed.md` | Which item of the list landed in which section of file 20, what went beyond the list, and what was not done. |
| `21 Adjudication - cross-examination of the revised semantics.md` | Rulings on what both witnesses found in file 20, grouped by defect, with the second revision list (16 items, not started). |
| `22 Claude Fable Semantics - second revision.md` | File 20 revised against file 21 §4 by sixty-nine exact replacements. Standalone. Under cross-examination at publication. |
| `22a Revision ledger 2 - where each item of file 21 landed.md` | The mapping for the second revision. |
| `23 Adjudication - second cross-examination round.md` | Rulings on round two (file 22), including my own four misses, and the third revision list. |
| `24 Claude Fable Semantics - third revision.md` | File 22 revised against file 23 by forty-three exact replacements. Under cross-examination at publication. |
| `24a Revision ledger 3 - where each item of file 23 landed.md` | The mapping for the third revision. |
| `25 Adjudication - third cross-examination round, and a verdict on the loop.md` | Rulings on round three (file 24) and the judgement that patch-revision has reached diminishing returns; what a rewrite from the core would be. |
| `26 Skill experiment - two method skills on file 20.md` | The file-20 cross-examination run twice more with a method skill as the witnesses' system prompt (the user's hard-to-vary skill, then the user's story-critique skill), compared with the plain run of file 21: recall of the known defects, new findings ruled, false findings, kind of finding, verdict (better, not incapacitated, on DeepSeek; Atria half open). |
| `26a Skill experiment - design frozen before reading.md` | The design and four predictions, published before any reply was read. |
| `26b Working notes - reply by reply.md` | The per-reply working log behind file 26, appended to as replies land. |
| `15f Supplement 5 - after the skill experiment.md` | Project story additions after the skill experiment. |
| `15e Supplement 4 - after rounds two and three.md` | Project story additions after rounds two and three. |
| `15d Supplement 3 - after the cross-examination of the revision.md` | Project story additions after file 21. |
| `15c Supplement 2 - after the revision.md` | Project story additions after the revision. |
| `18`, `19` | Witness profiles: where each model was strong and weak, under what conditions, with evidence. |
| `miniReason - project story.md` | The user-facing narrative with a numbered log (entries 1–31). |
| `diagnostics/` | Scripts that import the frozen code unchanged and check one witness claim each, with their outputs. |
| `witness-replies/` | The harness (`cross_examine.py`, keys from the environment only; `cross_examine_skill.py` loads a method skill as the system prompt), the batteries, `skill-runs/` (the skill-experiment replies and their usage), `method-skills/` (the two skills verbatim), `compare_runs.py`, every public reply as text (`<model>__<item>.txt`), and `usage_summary.json` (tokens, finish reasons, seconds). Hidden reasoning text was captured for diagnosis and is **not** published. |

Witnesses (files 10–17): `deepseek-flash` (three samples per item at the 131,072-token cap, plus audits) and `Atria-Dawn-Preview` (one to two samples per item at its 65,536-token cap; 25 of 26 items answered; later replies and rulings are in the supplement 15b, never by editing the published files). The author adjudicated; the witnesses' statements are evidence, not verdicts.

Headline outcomes, all with their evidence in files 15–17: experiment 1's "tracker beats memoriser" was an artefact of a crippled baseline (a fair memoriser ties it, 0.801 to 0.801) and its "neutral" tie was forced by the code; experiment 2's construction-versus-selection contrast was true by construction and phase 2 breached the frozen stopping rule; the semantics has a definitional cycle, a hidden decomposition parameter, an inverted transport orientation and two derivations that are false or vacuous as stated. Lessons are in `docs/lessons/` under the 2026-09-19 headings.
