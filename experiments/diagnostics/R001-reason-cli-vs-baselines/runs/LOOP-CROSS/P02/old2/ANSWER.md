# Working answer

Use Burnside's lemma on the dihedral group D12 (24 symmetries: 12 rotations, 12 reflections), with the three color names fixed. Let a valid coloring mean a cyclic arrangement of 12 beads using A,B,C exactly four times each, with no equal adjacent colors.

Identity. Count valid labeled colorings. Fix position 1 to be A. The other three A's split the remaining 8 positions into four positive gaps g1,g2,g3,g4 between consecutive A's, so g1+g2+g3+g4=8. For a fixed gap composition, let m be the number of odd gaps. The even gaps each have 2 alternating B/C choices and contribute the same number of B's either way. For the odd gaps, to make the total number of B's equal 4, exactly m/2 of them must start with B, giving C(m,m/2) choices; the even gaps give a factor 2^{4-m}. Thus the number for a gap composition is C(m,m/2)2^{4-m} when m is even, and 0 otherwise. Among the 35 compositions of 8 into 4 positive parts, the parity counts are: m=0 has 1 composition, m=2 has 24, m=4 has 10. So the fixed-position-1-A count is 1*16 + 24*8 + 10*6 = 268. By color symmetry multiply by 3, giving 804 fixed by the identity.

Rotations. Rotations by 1,5,7,11 force all beads equal or a single period, impossible. Rotations by 2 or 10 give two cycles of length 6, forcing counts 6 and 6, impossible. Rotations by 4 or 8 give four cycles of length 3, so every color count would be a multiple of 3, impossible. Rotation by 3 or 9 gives three cycles of length 4; each cycle must receive a different color, giving 3! = 6 each, hence 12 total. Rotation by 6 gives six cycles of length 2; this is equivalent to proper colorings of a 6-cycle with each color twice. Fixing one bead as A, the other A can be opposite (gaps 2,2: 4 B/C assignments) or at distance 2 in either direction (gaps 1,3 or 3,1: 2 each), giving 8 for fixed first color and 24 total. Rotation contribution: 804 + 12 + 24 = 840.

Reflections. Edge-axis reflections: the axis passes through two opposite edges, and a fixed coloring would require the two adjacent beads of each such edge to have the same color, impossible. So these 6 reflections contribute 0. Vertex-axis reflections: the axis fixes two opposite beads and swaps five pairs. If the two fixed beads had different colors, those two colors would occur an odd number of times, impossible because each total is 4. So they must have the same color x. Then the five pairs must be one pair x, two pairs of the second color, and two pairs of the third color. The five pair-colors form a path c1,c2,c3,c4,c5 with adjacent terms unequal and c1,c5 not equal to x. For fixed x, the single x can be in position 2, 3, or 4, giving respectively 2, 4, and 2 valid sequences, total 8. There are 3 choices for x, so each vertex-axis reflection fixes 24 colorings. Six such reflections contribute 144.

Burnside sum: (804 + 12 + 24 + 144)/24 = 984/24 = 41.

Thus, under rotations and reflections with fixed color names, the exact number of distinct necklaces is 41.

Assumptions: the 12 positions are initially labeled for counting and the equivalence is exactly the dihedral action D12; colors A,B,C are not permuted. The arithmetic above assumes the standard Burnside fixed-point counts for each symmetry type. Uncertainty is minimal; the main delicate step is the vertex-axis reflection count, which was checked by parity and by enumerating the five pair-color sequences.

## Open objections

No open objection is recorded; this does not establish correctness.


This is a personal working tool. Its output is a working answer with its objections, not a finding.

Stop reason: `TRANSPORT_OR_RESPONSE_ERROR`. Read TRACE.md for open objections.
