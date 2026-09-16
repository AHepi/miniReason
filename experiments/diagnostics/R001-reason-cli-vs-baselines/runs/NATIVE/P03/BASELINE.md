# Baseline readings

Same problem and conjecturer; one logical call per mode, with recorded attempts. No computed comparison.

## bare

Outcome: `COMPLETE`.

Thinking: off; completion ceiling: 8192; declared reasoning effort: medium.

Assumptions: all register arithmetic is modulo 10 after each entry of the table, with residues 0–9; the comparison for the emitted symbol uses the new x and new y after simultaneous update; input length is 14, so the emitted word has 14 symbols.

Trace (pre-step state, input -> next state, new x, new y; emit):

Initial: state A, x=2, y=5.

1. A,L -> B, new x=(2+5) mod10=7, new y=(2+3) mod10=5. x=7,y=5 => G.
   State B, x=7, y=5.

2. B,R -> A, new x=(7+5) mod10=2, new y=(7+2*5) mod10=(7+10) mod10=7. x=2,y=7 => E.
   State A, x=2, y=7.

3. A,R -> C, new x=(2*2+7) mod10=11 mod10=1, new y=(7+4) mod10=11 mod10=1. x=1,y=1 => T.
   State C, x=1, y=1.

4. C,L -> A, new x=(3*1+1) mod10=4, new y=(1+6) mod10=7. x=4,y=7 => E.
   State A, x=4, y=7.

5. A,L -> B, new x=(4+7) mod10=11 mod10=1, new y=(4+3) mod10=7. x=1,y=7 => E.
   State B, x=1, y=7.

6. B,R -> A, new x=(1+5) mod10=6, new y=(1+2*7) mod10=(1+14) mod10=15 mod10=5. x=6,y=5 => G.
   State A, x=6, y=5.

7. A,L -> B, new x=(6+5) mod10=11 mod10=1, new y=(6+3) mod10=9. x=1,y=9 => E.
   State B, x=1, y=9.

8. B,R -> A, new x=(1+5) mod10=6, new y=(1+2*9) mod10=(1+18) mod10=19 mod10=9. x=6,y=9 => E.
   State A, x=6, y=9.

9. A,R -> C, new x=(2*6+9) mod10=(12+9) mod10=21 mod10=1, new y=(9+4) mod10=13 mod10=3. x=1,y=3 => E.
   State C, x=1, y=3.

10. C,L -> A, new x=(3*1+3) mod10=6, new y=(3+6) mod10=9. x=6,y=9 => E.
    State A, x=6, y=9.

11. A,R -> C, new x=(2*6+9) mod10=21 mod10=1, new y=(9+4) mod10=13 mod10=3. x=1,y=3 => E.
    State C, x=1, y=3.

12. C,R -> B, new x=(1+3+1) mod10=5, new y=(2*1+3) mod10=5. x=5,y=5 => T.
    State B, x=5, y=5.

13. B,L -> C, new x=(5+2*5) mod10=(5+10) mod10=15 mod10=5, new y=(5+5) mod10=10 mod10=0. x=5,y=0 => G.
    State C, x=5, y=0.

14. C,R -> B, new x=(5+0+1) mod10=6, new y=(2*5+0) mod10=10 mod10=0. x=6,y=0 => G.
    State B, x=6, y=0.

Emitted word: G E T E E G E E E E E T G G

Final state: B
Final x: 6
Final y: 0

Uncertainty note: no substantive ambiguity was found; the only interpretive point is that the next-state/register update is simultaneous, which was applied as stated.

## native

Outcome: `COMPLETE`.

Thinking: native; completion ceiling: 32768; declared reasoning effort: medium.

Assumption: all register arithmetic is modulo 10; new x and new y are computed from the same pre-step x,y. Initial: state A, x=2, y=5.

Trace (step, input, pre-state (x,y) -> next state, new (x,y), emit):
1 L A(2,5)->B (7,5) G
2 R B(7,5)->A (2,7) E
3 R A(2,7)->C (1,1) T
4 L C(1,1)->A (4,7) E
5 L A(4,7)->B (1,7) E
6 R B(1,7)->A (6,5) G
7 L A(6,5)->B (1,9) E
8 R B(1,9)->A (6,9) E
9 R A(6,9)->C (1,3) E
10 L C(1,3)->A (6,9) E
11 L A(6,9)->B (5,9) E
12 R B(5,9)->A (0,3) E
13 R A(0,3)->C (3,7) E
14 L C(3,7)->A (6,3) G

Final state: A; final x=6; final y=3. Emitted word: GETEEGEEEEEEEG (positions: G E T E E G E E E E E E E G). No further uncertainty.

