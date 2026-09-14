"""Step classification tables: disjoint? subsets? exhaustive?

The interface says REPLAYABLE_STEPS / SPENDING_STEPS are 'disjoint subsets of
STEP_KINDS'.  It does not claim they partition; report the leftover kinds with
the command that produced the count, as a NOTE for W1-STEPS (whose resume
semantics name only the two classes).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minireason.loop.types import (STEP_KINDS, REPLAYABLE_STEPS, SPENDING_STEPS)

kinds = set(STEP_KINDS)
print("kinds:", len(kinds), "dup in tuple?", len(kinds) != len(STEP_KINDS))
print("replayable subset:", REPLAYABLE_STEPS <= kinds)
print("spending subset:", SPENDING_STEPS <= kinds)
print("disjoint:", REPLAYABLE_STEPS.isdisjoint(SPENDING_STEPS))
leftover = kinds - REPLAYABLE_STEPS - SPENDING_STEPS
print("neither replayable nor spending:", sorted(leftover))
