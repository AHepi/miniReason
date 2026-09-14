## Orchestration rule (session-wide, user-mandated)

- The top-level Claude Code session is an **orchestrator only**: it assigns work to subagents, interprets their results, and decides what to do next. It does no repository work itself beyond that.
- **Every subagent and every Workflow `agent()` call MUST use Opus 5** (`model: "opus"`). Never spawn Fable 5.1 (or any non-Opus) subagents. Set the model explicitly on every spawn; do not rely on inheritance.
- API keys supplied by the user (Ollama, DeepSeek) are secrets: read them from environment variables or a gitignored local file only. Never write them into a tracked file, a commit, a log, or a report.

## Session continuity (compaction fail-safe)

- After any context compaction, the orchestrator reads, before acting: the scratchpad file `ORCHESTRATOR-STATE.md` (path: `/tmp/claude-0/-home-user-miniReason/b114dbee-c9cd-5a0b-b695-8d39dd13d756/scratchpad/ORCHESTRATOR-STATE.md`, if the container still holds it) and the published rulings `docs/reviews/session-rulings-2026-09-14.md`.
- No claim about the repository carried by a compaction summary is a premise until an agent has verified it from bytes and named the file. Task prompts state where each repository premise was verified.
- Owner ruling 16 (2026-09-14) supersedes the Opus-only bullet above: Kimi K3 via `tools/kimi_harness` is the default worker for mechanical and draft work; Opus is used for semantic argument over FW5, independent judging, integration and review, and publication.
