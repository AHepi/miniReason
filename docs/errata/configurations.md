# Configuration errata

Original miniReason configuration failures will be recorded here and beside their experiment records. Existing upstream templates are being read as interface documentation only; none is reused as an experimental candidate. An upstream defect is not a result of an original miniReason template.

## CFG-001 — Output checker admitted booleans as integer quantities

The independent pre-run task audit constructed a correct program with zero/one integer results replaced by False/True. Python structural equality accepted them because booleans compare equal to those integers. This violated the declared exact output contract. The evaluator now compares values recursively with exact types; a regression test reaches the false acceptance. No live record was scored by the flawed checker.

## CFG-002 — Expression steps did not bound primitive work

The independent task audit evaluated len(mul([0],100000)) in five charged expression steps. The arithmetic interpreter admitted list/string multiplication, so a small expression could allocate excessive memory. Unknown expression fields were also silently ignored despite an exact grammar promise. Arithmetic now requires bounded numeric values, grammar fields are validated exactly, collection work is charged and size/depth/output caps enforced. Focused tests verify these paths. This is an interpreter limitation and repair, not evidence about model creativity.
