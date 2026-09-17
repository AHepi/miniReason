# Working answer

Exactly 59 seven-1 bit strings reach the final state (2,1). The exact joint probability is 4,129,056/244,140,625. Derivation: each specified 12-bit string has probability (3/5)^7(2/5)^5; a dynamic count over the 12-state automaton with seven 1s and five 0s gives 59 such strings; therefore the joint probability is 59*3^7*2^5/5^12 = 4,129,056/244,140,625.

Stop reason: `CEILING_HIT`.
