Implement the wave-2 module W2-DECIDE as
`src/minireason/loop/decide.py`, with its test file
`tests/loop/test_decide.py`, from the design entry and the wave-0 and wave-1
interfaces already in the sandbox. The module does not exist yet; you are its
author.

THE DESIGN ENTRY, verbatim from `design/design-s7-wave-plan.md`.

  purpose: The pre-registered stop/continue program: guard rails, then the five O/P clauses, then the decision record with would_reopen and losses_outside_P.

  public_interface: situation(harness, cycle) -> Situation; mark_triples(harness) -> frozenset; decide(prev, curr, cycle_index, config, obligations) -> Decision; render_decision(d) -> str; Decision.stop; Decision.reason; Decision.record_sentences

  depends_on: W0-TYPES, W1-OBLIGATIONS, W1-GRAPH

  acceptance: decide() is total and returns exactly one outcome; a protected loss stops and names the loss; an o satisfied without this cycle's own artifacts does not continue; identical mark-triple sets stop as a set identity and not as a count; a budget stop carries the boundary-not-exhaustion sentence and a would_reopen field; a block streak stops as instrument_fault and names it a fault in the instrument, not a finding about the material; no count of readings, marks, endpoints or differs appears in any clause; the module digest matches the one pinned in plan.json.

WHAT BINDS YOU.
* `notes/WAVE0-INTERFACE.md` is the integrator's record of the wave-0 public
  interface: which module owns each shared constant, what every exception carries,
  and the eleven open questions O1-O11. Import the shared vocabularies from the
  module that owns them; never retype one.
* `notes/WAVE1-INTEGRATION-DECISIONS.md` carries eight decisions the wave-2 modules
  are bound by. Read all eight before you design a signature.
* Every exception you raise is a `types.LoopError` subclass taking
  `(code, detail="")`, and every new failure code you raise is added to
  `types.FAILURE_CODES` — but you may not edit `src/minireason/loop/types.py` in
  this sandbox, so instead list the new codes at the top of your module in a
  module-level `NEW_CODES: tuple[str, ...]` and say in your final message which
  table each belongs in.
* Do not edit any file under `src/` other than the one you are creating. Nothing
  you write touches a frozen plan, a published occurrence or `src/creib/**`.
* No network. No provider call. The module must be importable and testable offline.

RUN IT:

    python3 run_tests.py tests.loop.test_decide

Iterate until it reports OK.

Write the module with the docstring discipline the wave-0 modules use: a module
docstring that states what the module promises and what it refuses, and a docstring
on every public callable naming the failure code it raises. `docs/examples/test_custody_example.py`
is the house test style.

Finish by stating: which acceptance clauses your implementation satisfies and how
each is tested; which parts of the public interface you implemented as stubs and
why; every place where the design entry, the wave-0 interface and the wave-1
decisions did not settle a question, what you decided, and what would change if the
decision went the other way.

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

Sandbox: /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/controls/c-04-decide/sandbox

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

      /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/controls/c-04-decide/FINAL.md

  plus whatever files the task above names inside the sandbox.
* End your final answer with a section headed "What I could not determine",
  naming what you could not settle, what you left out and what you could not
  cover. As the house rules above require: say "unresolved", or "I could not
  determine this and here is why", rather than inventing a finding.
