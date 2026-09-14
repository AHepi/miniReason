Write the decision-ledger receipt paragraph that records the publication described
in `factsheets/D-DOC-1-fact-sheet.md`, and write it to `out/receipt.md`.

The fact sheet is the whole of your evidence. Every figure, hash, commit, tree,
path, suite number and constraint in your paragraph must come from it. Do not add a
fact it does not contain; do not drop a constraint it states.

FORM. `AGENTS.md` requires that every receipt carry, in prose, the choice, the
reason, the contribution to the end goal, and the pending-or-completed state with
its evidence. `docs/ledger/house-style-samples.md` and
`docs/ledger/REC-20260914-U.md` are real paragraphs from the ledger in the two forms
you need: an opening receipt and a publication outcome. Match that register — dense,
declarative, evidence-first, one paragraph, no bullet list, no heading, no table.
The paragraph opens exactly as the samples do:
`REC-20260914-V publication outcome at 2026-09-14 09:28 UTC: `.

`docs/lessons/operations.md` binds you on two points the fact sheet depends on: a
test count is only meaningful beside its invocation, and an append-only record is
appended to in byte mode. Where the fact sheet gives an invocation, keep it beside
its number.

WHAT THE PARAGRAPH MAY NOT DO. It may not describe a ceiling or a clock as
exhaustion. It may not compare the `fcl` and `prose` arms as better and worse, or
read anything semantic off the 8192 figures — the fact sheet requires those to be
called a resource observation and not a semantic one, in those terms. It may not
modify, reinterpret or supersede occurrence-01, which stands as published. It may
not contain a score, a rank or a scalar meter.

Finish, outside the file, by naming every fact from the sheet you deliberately left
out and why.

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

Sandbox: /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/controls/d-01-receipt/sandbox

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

      /tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/kimi/controls/d-01-receipt/FINAL.md

  plus whatever files the task above names inside the sandbox.
* End your final answer with a section headed "What I could not determine",
  naming what you could not settle, what you left out and what you could not
  cover. As the house rules above require: say "unresolved", or "I could not
  determine this and here is why", rather than inventing a finding.
