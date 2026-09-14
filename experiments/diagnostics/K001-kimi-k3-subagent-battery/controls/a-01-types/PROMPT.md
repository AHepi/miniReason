Review `src/minireason/loop/types.py` — the wave-0 module W0-TYPES: config schema and loader, `loop_plan_id`, step receipts, the run layout and the four closed code tables —
for bugs and design violations, adversarially, against what it claims of itself.

The sandbox is a frozen snapshot of the staging clone. Read
`notes/WAVE0-INTERFACE.md` first: it is the integrator's record of what the six
wave-0 modules expose, which module owns each shared constant, what every exception
carries, and the eleven open questions O1-O11. Then read the module, and read
`design/design-s2-roles-and-guard.md` and `design/design-s7-wave-plan.md` for the
acceptance clauses W0-TYPES is answerable to. The other wave-0 modules in the
sandbox are there so you can check a cross-module claim rather than assume one.

METHOD. Every finding must be executed, not asserted. Write probe scripts under
`probe/` and run them with `python3 probe/<name>.py`; the whole package imports in
this sandbox. For each finding give:
  * a heading and a one-line claim;
  * the exact file and line range the defect lives at;
  * the docstring sentence, interface entry or design clause the code contradicts,
    quoted;
  * the probe you ran and what it printed, verbatim;
  * the repair, and the test that would hold the repair.
Rank nothing. Order findings as BLOCKER (a published seam that is unsound, or a
pre-registered guard that does not fire), SHOULD-FIX, and NOTE.

Also write one short section, "Tried, and could not break", recording at least three
attacks that failed. An attack that fails is evidence about the module and belongs in
the review.

Do not edit `src/minireason/loop/types.py` or any other file under `src/`. Write
your review to `review/types.md` and your probes to `probe/`.

A defect you cannot reproduce is not a finding; say you suspected it and could not
reproduce it, and move on. Do not report a defect that the code in this sandbox does
not have.

TOOLING. You have read_file, list_dir, grep, write_file and run_command inside a
sandbox. `run_command` accepts only `python3 ...` forms: `python3 -m unittest ...`,
`python3 -m pytest ...`, `python3 -c ...` and `python3 <file.py> ...`. There is no
shell, no `git`, no `ls`, no `cat`, and you cannot set environment variables on a
command line. The sandbox has no network. To run a test module, use the helper that
is already in the sandbox:

    python3 run_tests.py tests.loop.test_<name>

It puts the sandbox root and `src` on `sys.path` and nothing else. You cannot ask
questions; everything you need is in the sandbox.

HOUSE RULES, which hold for every sentence you write.
* No score, no rank, no scalar progress meter, no "better"/"worse" between model
  families, arms, endpoints or modules. Endpoints and arms are independent
  occasions, never competitors.
* A token ceiling, a call budget, a wall clock or a connection close is a RESOURCE
  BOUNDARY. It is never described as exhaustion of the inquiry.
* `unresolved` is a first-class outcome. Say "unresolved", or "I could not
  determine this and here is why", rather than inventing a finding. A finding you
  cannot point at a file and a line for is not a finding.
* Never modify a published observation, and never edit a file to make your own
  claim true.
* Counts are information, never a warrant. Report a count with the command or file
  that produced it beside it.

---

OPERATING NOTE

Sandbox: /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/controls/a-01-types/sandbox

* All reads and all writes happen inside that directory. Every path named above
  is relative to the sandbox root, and the sandbox root is the working directory
  for everything you run. No file outside the sandbox may be read or written —
  the one exception is the final answer file named below.
* The only commands that may be run are `python3 -m unittest ...`,
  `python3 -m pytest ...`, `python3 -c ...` and `python3 <file>.py ...`, each run
  inside the sandbox. Where the sandbox provides `run_tests.py`, that is how a
  test module is run: `python3 run_tests.py tests.loop.test_<name>`. Nothing else
  runs — no shell, no `git`, no `ls`, no `cat`, no `pip`, no network, and no
  environment variable set on a command line.
* The deliverable is your final answer text, written to

      /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/controls/a-01-types/FINAL.md

  plus whatever files the task above names inside the sandbox.
* End your final answer with a section headed "What I could not determine",
  naming what you could not settle, what you left out and what you could not
  cover. As the house rules above require: say "unresolved", or "I could not
  determine this and here is why", rather than inventing a finding.
