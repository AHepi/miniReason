# Baseline readings

Same problem and conjecturer; one logical call per mode, with recorded attempts. No computed comparison.

## bare

Outcome: `CEILING_HIT`.

Thinking: off; completion ceiling: 8192; declared reasoning effort: medium.

Baseline did not complete; loop execution continues.

## native

Outcome: `COMPLETE`.

Thinking: native; completion ceiling: 32768; declared reasoning effort: medium.

The exact number is 41.

Derivation using Burnside's lemma on the dihedral group D12 of 24 symmetries (12 rotations and 12 reflections).

1) Identity symmetry.
Count proper colorings of a 12-cycle with four A, four B, four C. Fix position 1 as C. Then the other three C's must be placed nonadjacently, creating four positive gaps L1,L2,L3,L4 with sum 8. In each gap the A/B beads must alternate. Tracking A-B difference, an even-length gap contributes factor 2; an odd-length gap contributes z+z^{-1}. Summing over ordered positive compositions of 8 into four parts, grouped by the number k of odd gaps:
- k=0: 1 composition, contribution 16;
- k=2: 24 compositions, contribution 8 each -> 192;
- k=4: 10 compositions, contribution 6 each -> 60.
So number with position 1 fixed as C is 268. By color symmetry, total identity-fixed colorings = 3*268 = 804.

2) Rotations.
- Half-turn r^6: opposite pairs are equal, giving a proper 6-cycle with two beads of each color. Count = 24.
- Rotations r^3 and r^9: the three 4-cycles must receive distinct colors; all adjacent positions are in different cycles, so each has 3! = 6 fixed colorings.
- All other rotations fix none, because their cycle lengths do not divide the required color count 4.
Rotation contribution = 804 + 24 + 6 + 6 = 840.

3) Reflections.
- Vertex-axis reflections (6 of them): the two fixed opposite vertices must have the same color, say X. The remaining five paired positions form a path X-a-b-c-d-e-X. For a fixed X, the sequence a,b,c,d,e must contain one X and two each of the other two colors, with endpoints not X. This gives 8 possibilities per X (X at positions 2,3,4 contributes 2+4+2). Thus 3*8 = 24 fixed colorings per vertex reflection, total 6*24 = 144.
- Edge-axis reflections (6 of them): an edge on the axis has its two adjacent endpoints swapped, forcing them to be equal, which is forbidden. So each fixes 0.
Reflection contribution = 144.

Burnside count:
(840 + 144) / 24 = 984 / 24 = 41.

Assumptions: the 12 positions are initially labeled, the only equivalences are rotations and reflections (turning over), and color names A,B,C are fixed and not permuted. Under these stated rules the number of distinct necklaces is 41.

