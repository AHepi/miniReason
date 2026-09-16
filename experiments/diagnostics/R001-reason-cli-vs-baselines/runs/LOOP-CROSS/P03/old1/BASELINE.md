# Baseline readings

Same problem and conjecturer; one logical call per mode, with recorded attempts. No computed comparison.

## bare

Outcome: `COMPLETE`.

Thinking: off; completion ceiling: 8192; declared reasoning effort: medium.

Initial: state A, x=2, y=5.

Trace table showing before-state, input, then after-state/new x/new y and emission. Arithmetic is mod 10.

1. A, L: new x = 2+5 = 7; new y = 2+3 = 5; state B. x<y => E.
2. B, R: new x = 7+5 = 12 mod10 = 2; new y = 7+2*5 = 17 mod10 = 7; state A. x<y => E.
3. A, R: new x = 2*2+7 = 11 mod10 = 1; new y = 7+4 = 11 mod10 = 1; state C. x=y => T.
4. C, L: new x = 3*1+1 = 4; new y = 1+6 = 7; state A. x<y => E.
5. Wait check pre-step state is C from step 3, then step 4 input L moved to A. Step 5 has state A, input L.
   A, L: new x = 4+7 = 11 mod10 = 1; new y = 4+3 = 7; state B. x<y => E.
6. B, R: new x = 1+5 = 6; new y = 1+2*7 = 15 mod10 = 5; state A. x>y => G.
7. A, R: new x = 2*6+5 = 17 mod10 = 7; new y = 5+4 = 9; state C. x<y => E.
8. C, L: new x = 3*7+9 = 30 mod10 = 0; new y = 9+6 = 15 mod10 = 5; state A. x<y => E.
9. A, R: new x = 2*0+5 = 5; new y = 5+4 = 9; state C. x<y => E.
10. C, L: new x = 3*5+9 = 24 mod10 = 4; new y = 9+6 = 15 mod10 = 5; state A. x<y => E.
11. A, R: new x = 2*4+5 = 13 mod10 = 3; new y = 5+4 = 9; state C. x<y => E.
12. C, L: new x = 3*3+9 = 18 mod10 = 8; new y = 9+6 = 15 mod10 = 5; state A. x>y => G.
13. A, R: new x = 2*8+5 = 21 mod10 = 1; new y = 5+4 = 9; state C. x<y => E.
14. C, L: new x = 3*1+9 = 12 mod10 = 2; new y = 9+6 = 15 mod10 = 5; state A. x<y => E.

Final state: A
Final x: 2
Final y: 5
Emitted word: EETEEGE EEEEGE E? Let's concatenate carefully:
Steps 1-14 emissions: E, E, T, E, E, G, E, E, E, E, E, G, E, E.
So complete 14-symbol word: EETEEGEEEEEGEE.

Check count: positions: 1 E, 2 E, 3 T, 4 E, 5 E, 6 G, 7 E, 8 E, 9 E, 10 E, 11 E, 12 G, 13 E, 14 E. Yes: EETEEGEEEEEGEE.

Assumptions/uncertainties: I assumed modulo 10 residues exactly as stated, and that each step's New x and New y formulas both use the pre-step x,y. The trace above is intended to make simultaneous updates checkable. No code used.

## native

Outcome: `COMPLETE`.

Thinking: native; completion ceiling: 32768; declared reasoning effort: medium.

Final state: A. Final x: 6. Final y: 3. Emitted word: GETEEGEEEEEEEG.

Trace (step: pre-state,input -> next-state; new (x,y); emit):
1: A,L -> B; (7,5); G
2: B,R -> A; (2,7); E
3: A,R -> C; (1,1); T
4: C,L -> A; (4,7); E
5: A,L -> B; (1,7); E
6: B,R -> A; (6,5); G
7: A,L -> B; (1,9); E
8: B,R -> A; (6,9); E
9: A,R -> C; (1,3); E
10: C,L -> A; (6,9); E
11: A,L -> B; (5,9); E
12: B,R -> A; (0,3); E
13: A,R -> C; (3,7); E
14: C,L -> A; (6,3); G

Assumptions: register updates are simultaneous using the pre-step x,y; all arithmetic is modulo 10. No uncertainties.

