# Configuration errata

Original miniReason configuration failures will be recorded here and beside their experiment records. Existing upstream templates are being read as interface documentation only; none is reused as an experimental candidate. An upstream defect is not a result of an original miniReason template.

## CFG-001 — Output checker admitted booleans as integer quantities

The independent pre-run task audit constructed a correct program with zero/one integer results replaced by False/True. Python structural equality accepted them because booleans compare equal to those integers. This violated the declared exact output contract. The evaluator now compares values recursively with exact types; a regression test reaches the false acceptance. No live record was scored by the flawed checker.

## CFG-002 — Expression steps did not bound primitive work

The independent task audit evaluated len(mul([0],100000)) in five charged expression steps. The arithmetic interpreter admitted list/string multiplication, so a small expression could allocate excessive memory. Unknown expression fields were also silently ignored despite an exact grammar promise. Arithmetic now requires bounded numeric values, grammar fields are validated exactly, collection work is charged and size/depth/output caps enforced. Focused tests verify these paths. This is an interpreter limitation and repair, not evidence about model creativity.

## CFG-003 — E001 completion allowance prevented native final output

All three native-mode arms in E001 ended their first call at the 8192-token ceiling, with INCOMPLETE_GENERATION retained in their response and terminal records. No finished answer could be evaluated. The direct native and Mini-native comparison therefore remains unavailable in E001. E002 raises only that ceiling to 32768; it does not revise the reasoning template or withdraw the original failures.

## CFG-004 — E002 separates some completion failures from nested encoding failures

E002 retained the task and templates and raised the per-call completion ceiling to 32768. The direct native response finished and survived the recorded cases; the Mini-native first call still ended at the new ceiling. This one repetition cannot establish an inherent Mini penalty. Bare and Mini candidates repeated duplicate `do` keys in embedded program JSON. The staged native final retained extra data after the program JSON value. The staged non-native final failed outer-record parsing with extra data. Full call bytes and partition-specific errors are retained beside the record; none licenses dismissal of the accompanying prose. The nested JSON representation and the strict interpreter contract are part of the tested conjunction. Further encoding repair is deferred while the user’s expressibility study becomes the active task.

## CFG-005 — Frozen language invention embedded source translations

E004's setup explicitly requested no corpus quotations or per-fragment translations in the language declarations. Both returned languages nevertheless quote source clauses and explain their representation; the Lean proposal also embeds a task-specific computational account. This is an instruction-following and design limitation, not an admission failure for the semantic specimens. E005–E007 retain the exact initial packet and explicitly treat the middle stage as source-field withholding with possible information leakage. A later language-only reading control can ask what the actual expression adds. The packet is not silently cleaned or repaired. See the E004 independent review for exact evidence and other proposed limitations.

## CFG-006 — Real frozen packet exceeded two inherited Mini inline limits

E005's full P0 packet is 33,995 Unicode characters (34,096 UTF-8 bytes), exceeding Mini's 8,192-character `problem` limit. Both Mini arms stopped during manifest compilation before any model call. The language adapter's smaller mocked fixtures did not exercise this boundary. A second static check shows the selected Lean and non-Lean texts also exceed the 4,000-character kind-instruction limit, so increasing only the problem allowance would not repair the route. Direct arms continued and are retained; the intended Mini comparison is unavailable in E005. The repair will use supported file sources and deterministic full-source artifacts with explicit ports, preserving all original bytes and inherited schema limits. It will add real-packet preflight before any paid arm starts. E006 and E007 are not to run their known-invalid route; successor plans get new identities after the repair.
