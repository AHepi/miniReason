# Kimi battery pass 1, interim (18 of 26 results at ~11:50 UTC)

- COMPLETE 4 (a-04-custody 37 it / 2.49M tok / 540 s; d-03 7 it; d-04 8 it; smoke 6 it)
- ITERATION_CAP 4 (a-01, a-02, a-03, b-02): 40 iterations, 1.9M-3.75M tokens, 460-1054 s; the whole context is re-sent each turn (60k+ prompt), and the model kept exploring without closing.
- HARNESS_FAILURE 10, all "Remote end closed connection without response" at 300-301 s after a request (ruling 13): a-05, a-06, b-01, b-03, b-04, c-01, c-02, c-03, c-04, d-01. A reasoning-heavy turn on a large context does not finish inside the gateway's 300 s.
- Pass 2 (decided): re-run every non-COMPLETE task with max_tokens 8192 per turn (a tool-loop turn rarely needs more) and max_iterations 80, default reasoning_effort, recorded as pass 2 beside pass 1; judges receive both. The headline infra finding stands regardless: as deployed on Ollama cloud, Kimi K3's per-turn reasoning on a 60k-token context collides with the 300 s wall.

## Judge notes to carry into REPORT.md (from family E, 2026-09-14)

- Harness labelling defect: a turn that returns finish_reason=length with zero content and zero tool calls ends the loop and is recorded as status COMPLETE with files_written=[] (e-02 pass 2: 8192 completion tokens all reasoning, 35k reasoning chars). The report must reclassify such runs as INCOMPLETE_TURN (no deliverable), never COMPLETE, and the harness should be fixed before any further pass.
- Two answer keys quote figures that exist only outside the frozen corpus (F001 content bytes 288/7,080; the two 180 s timeout elapsed times). Judge E declined to score the worker down on those; the report must say so.
- Kimi (family E): found both decisive hits, left the three traps standing, aggregated by script every time, stated evidence gaps instead of filling them; weaknesses: prose transcription drift from its own verified values, errors concentrated in volunteered extras, 2-6x the key's length, shell syntax outside the allow-list (harness accepted it).
- Cost profile: 764k-1,262k prompt tokens for 21k-45k completion tokens per task because the whole context is re-sent each turn; 481-766 s wall for 20-24 iterations.
