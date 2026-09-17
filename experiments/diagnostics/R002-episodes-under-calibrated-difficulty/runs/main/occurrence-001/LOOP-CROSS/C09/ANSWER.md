# Working answer

Using the transition rules, I label B=(0,1), G=(2,0), H=(2,1), K=(3,1), C=(0,2). A dynamic count over the 12 states tracks the number of strings with k ones. Iterating the transition recurrence to length 10 gives K coefficient 37 at k=5, C coefficient 8 at k=7, and H coefficient 14 at k=6. At length 11, B coefficient at k=6 is 37, because K with one additional 1 goes to B; G coefficient at k=7 is 8+14=22, because C with a 0 and H with a 1 both go to G. Since B with a final 1 and G with a final 0 both go to H=(2,1), the number of seven-1 strings reaching (2,1) is 37+22=59. Exactly 59 seven-1 bit strings reach the final state (2,1). The exact joint probability is 59*(3/5)^7*(2/5)^5=4129056/244140625.

Stop reason: `CEILING_HIT`.
