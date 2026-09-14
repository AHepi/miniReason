Condense `design/design-s5-decision-rule.md` — the pre-registered stop/continue rule
of the automated loop — into ONE decision-record paragraph, and write it to
`out/decision-record.md`.

The paragraph is for the decision ledger. It records what the rule is, why it is
this rule, and what it refuses to be. It must be readable by someone who has not
read the design.

IT MUST CARRY: that O and P are published and pinned before cycle 1 and may not
shift inside an assessment; what O is and what P is; that exactly one outcome is
returned; the guard rails that are evaluated first; the ordering of the clauses and
what each stops or continues on; that `losses_outside_P` is written every cycle and
is present even when empty; that every stop carries a `would_reopen` field; and that
changing any threshold after first look mints a new `loop_plan_id` and is a new
pre-registration.

THE CONSTRAINT THAT DECIDES THIS TASK. No clause of your paragraph may be
count-shaped. The design's own clause 4 is a SET-IDENTITY test over `(cell,
register, mark)` triples, not a count of them, and clause 5 is a declared budget —
an attention-and-spend question, never an adjudication. If you write "if the number
of new marks is zero" or "when enough obligations are discharged" or "the majority
of cells", you have replaced the rule with a meter and failed the task. The
vocabulary has no order: `repairs` does not outrank `retains`, the four registers
are never summed, and no quantity of readings, marks, agreeing endpoints or `differs`
appears anywhere.

Say also, in the paragraph, why this is not a scalar meter — in the design's own
terms, not in your own.

One paragraph. No bullets, no headings, no table. Dense and declarative, in the
register of `docs/ledger/house-style-samples.md`.

Finish, outside the file, by listing every sentence of the design section you
dropped and why dropping it does not change the rule.

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

Sandbox: /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/controls/d-03-decision-record/sandbox

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

      /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/controls/d-03-decision-record/FINAL.md

  plus whatever files the task above names inside the sandbox.
* End your final answer with a section headed "What I could not determine",
  naming what you could not settle, what you left out and what you could not
  cover. As the house rules above require: say "unresolved", or "I could not
  determine this and here is why", rather than inventing a finding.
