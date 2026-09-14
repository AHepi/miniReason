Write the operator-page section for the wave-1 module W1-STEPS
(`src/minireason/loop/steps.py`) and write it to `out/steps-operator-section.md`.

This section will become part of `docs/workflows/automated-loop.md`, the operator
page the design of record requires at W6-DOC: "the command, the config, the
directory layout, every failure and block code, the pre-registration template, the
obligations template and the ceiling text". You are writing only the W1-STEPS
section of it.

`docs/workflows/provider-openai-compat.md` is the house exemplar for an operator
page: what the thing is, the exact invocation, the record layout on disk, every
refusal by code with the operator action for each, and the things the page
explicitly does not promise. Match it.

YOUR SECTION MUST CARRY, read off the module and not invented:
* what the step ledger is for, in three sentences: step_key, write-once receipts,
  and what resume means;
* the on-disk layout of a run's `steps/` directory, including the open-marker
  spelling, taken from `types.RunPaths.step_path` and the conventions section of
  `notes/WAVE0-INTERFACE.md`;
* the replayable / spending distinction and what each implies for a killed run;
* every failure code `steps.py` can raise, each with the operator action — what the
  operator does next, and what is refused until they do it;
* the halt-and-acknowledge rule, including that a halt is sticky and that an
  acknowledgement records a reason;
* what a `PublishPending` state blocks;
* `RunLock`, and what a second driver on the same run sees;
* what this module does NOT promise.

`design/design-s4-driver.md` section 4.3 and 4.4 give the step-receipt and
failure-handling design; `notes/WAVE1-INTEGRATION-DECISIONS.md` binds the module.
Where the module and the design disagree, follow the module and say in the page that
you did.

Quote no code block longer than ten lines. Every code you name must be one you found
in `steps.py`; grep for it and check. An operator page that lists a failure code the
module cannot raise is worse than one that lists fewer.

Finish, outside the file, by naming any failure code you found in the module that
you could not give an operator action for.

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

Sandbox: /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/controls/d-02-operator-page/sandbox

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

      /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/controls/d-02-operator-page/FINAL.md

  plus whatever files the task above names inside the sandbox.
* End your final answer with a section headed "What I could not determine",
  naming what you could not settle, what you left out and what you could not
  cover. As the house rules above require: say "unresolved", or "I could not
  determine this and here is why", rather than inventing a finding.
