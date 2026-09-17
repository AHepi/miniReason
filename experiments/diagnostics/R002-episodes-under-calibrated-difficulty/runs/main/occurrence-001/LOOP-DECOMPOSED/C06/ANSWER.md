# Working answer

Accepted partial steps (no synthesis):

1. State (x,y,s,k,vP,vQ): x,y in 0..9; s = last move (or start); k in {0,1,2} current run length; vP,vQ checkpoint flags, which are not determined by (x,y) alone. A next move m in {R,D} is legal iff it does not extend a run of m to length 3, the new cell is in-grid, and it is not in F. Accept iff at (9,9), no forbidden cell visited, and exactly one of P,Q visited (vP+vQ=1). Outputs: count N of accepting strings and the lexicographically first accepting string under D<R.

Stop reason: `SCHEMA_FAILURE`.
