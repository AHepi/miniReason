# Cycle 2 stopped

Reason: `SCHEMA_FAILURE`. Partial call evidence is retained in calls/.

## Visible working: c0002-k01/a01

I re-verified the entire trace step-by-step to ensure no calculation errors exist. Step 1: A,L -> B, x=7, y=5 (G). Step 2: B,R -> A, x=2, y=7 (E). Step 3: A,R -> C, x=1, y=1 (T). Step 4: C,L -> A, x=4, y=7 (E). Step 5: A,L -> B, x=1, y=7 (E). Step 6: B,R -> A, x=6, y=5 (G). Step 7: A,L -> B, x=1, y=9 (E). Step 8: B,R -> A, x=6, y=9 (E). Step 9: A,R -> C, x=1, y=3 (E). Step 10: C,L -> A, x=6, y=9 (E). Step 11: A,L -> B, x=5, y=9 (E). Step 12: B,R -> A, x=0, y=3 (E). Step 13: A,R -> C, x=3, y=7 (E). Step 14: C,L -> A, x=6, y=3 (G). All calculations match the working answer. The emitted word GETEEGEEEEEEEG and final state A, x=6, y=3 are correct.

