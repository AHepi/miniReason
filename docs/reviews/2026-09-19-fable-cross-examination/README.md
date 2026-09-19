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
| `15d Supplement 3 - after the cross-examination of the revision.md` | Project story additions after file 21. |
| `15c Supplement 2 - after the revision.md` | Project story additions after the revision. |
| `18`, `19` | Witness profiles: where each model was strong and weak, under what conditions, with evidence. |
| `miniReason - project story.md` | The user-facing narrative with a numbered log (entries 1–31). |
| `diagnostics/` | Scripts that import the frozen code unchanged and check one witness claim each, with their outputs. |
| `witness-replies/` | The harness (`cross_examine.py`, keys from the environment only), the three batteries, every public reply as text (`<model>__<item>.txt`), and `usage_summary.json` (tokens, finish reasons, seconds). Hidden reasoning text was captured for diagnosis and is **not** published. |

Witnesses (files 10–17): `deepseek-flash` (three samples per item at the 131,072-token cap, plus audits) and `Atria-Dawn-Preview` (one to two samples per item at its 65,536-token cap; 25 of 26 items answered; later replies and rulings are in the supplement 15b, never by editing the published files). The author adjudicated; the witnesses' statements are evidence, not verdicts.

Headline outcomes, all with their evidence in files 15–17: experiment 1's "tracker beats memoriser" was an artefact of a crippled baseline (a fair memoriser ties it, 0.801 to 0.801) and its "neutral" tie was forced by the code; experiment 2's construction-versus-selection contrast was true by construction and phase 2 breached the frozen stopping rule; the semantics has a definitional cycle, a hidden decomposition parameter, an inverted transport orientation and two derivations that are false or vacuous as stated. Lessons are in `docs/lessons/` under the 2026-09-19 headings.
