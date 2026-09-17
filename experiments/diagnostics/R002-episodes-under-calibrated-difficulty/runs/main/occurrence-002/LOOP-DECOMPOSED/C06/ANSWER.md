# Working answer

Accepted partial steps (no synthesis):

1. Paths correspond bijectively to strings s in {R,D}^18 with exactly 9 R and 9 D. Lexicographic order is first-difference order with D<R. The lexicographically first valid move string is the least string in the later-constrained subset under this order.
2. The no-three-consecutive constraint is exactly: the move string contains neither RRR nor DDD as a substring.
3. For each forbidden cell (a,b), exclude strings where the prefix of length a+b has exactly a R moves (hence b D moves), i.e. the count-prefix (a,b) occurs. Concretely exclude: prefix length 4 with 2 R; length 7 with 4 R; length 11 with 5 R; length 12 with 7 R; length 16 with 8 R.

Stop reason: `step_budget`.
